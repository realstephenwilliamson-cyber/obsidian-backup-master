"""Units and commentary ranges in the current library copy of Dyczkowski's Tantraloka (22 Oct 2026)."""
import json, re, sys, collections
exec(open('seg.py').read().split("# ---- find each unit")[0])   # NOTES, norm, dz, uf, um, vf
found = json.load(open('found.json'))

def is_marker_para(p):
    return p['kind'] == 'prose' and dz.TAIL.search(p['text']) and len(dz.DEVA.findall(p['text'][-150:])) < 8

def unit_end_from(paras, i0, limit=14):
    n = 0
    for i in range(i0, len(paras)):
        p = paras[i]
        if p['kind'] in ('page', 'foot', 'nav'): continue
        if p['kind'] == 'verse' and i > i0: return None
        if is_marker_para(p): return i
        n += 1
        if n > limit: return None
    return None

ENG = re.compile(r"\b(the|and|of|is|in|to|that|this|which|with|he|it|as|by|for|are|be)\b", re.I)
def sanskritish(t):
    """a paragraph of the verse block the line classifier missed: Devanagari, or IAST without English words"""
    if len(t) > 500: return False
    letters = re.findall(r'[A-Za-zĀ-ſḀ-ỿ]', t); deva = dz.DEVA.findall(t)
    if deva and len(deva) >= 0.3 * (len(deva) + len(letters)): return True
    if not letters or ENG.search(t): return False
    return bool(dz.IAST_C.search(t)) or bool(re.search(r'(\||॥)\s*\d*\s*(\||॥)?\s*$', t))
def verse_start_before(paras, i):
    """first paragraph of the verse block standing before paragraph i (skipping page/foot/headings); i if none"""
    j = i - 1; first = None
    while j >= 0:
        p = paras[j]
        if p['kind'] in ('page', 'foot', 'nav'): j -= 1; continue
        if p['kind'] == 'verse' or sanskritish(p['text']): first = j; j -= 1; continue
        if p['kind'] == 'prose' and dz.is_heading(p['text']) and first is None: j -= 1; continue
        break
    return first if first is not None else i

UNITS = collections.defaultdict(list)   # note -> [{'pv','ps','pe','uid'}]
# 1. marker-based units
for name, n in NOTES.items():
    ps = n['paras']; last_end = -1
    for i, p in enumerate(ps):
        if not is_marker_para(p): continue
        # translation start: walk back over prose pieces of this translation (stop at verse, marker, lead-in ':' or heading)
        s = i; j = i - 1
        while j > last_end:
            q = ps[j]
            if q['kind'] in ('page', 'foot', 'nav'): j -= 1; continue
            if q['kind'] != 'prose' or is_marker_para(q) or dz.is_heading(q['text']) or re.search(r'[:—–]\s*$', q['text']): break
            if dz.sanskrit_dense(q['text']): break
            if re.search(r'[.!?’”")]\s*$', q['text']): break     # a finished sentence before: not part of this translation
            s = j; j -= 1
        pv = verse_start_before(ps, s)
        UNITS[name].append({'pv': pv, 'ps': s, 'pe': i, 'uid': None, 'src': 'marker'})
        last_end = i
# 2. the phase-5 units, placed by their text; attach ids, add missing boundaries
fix = collections.Counter()
for uid, r in found.items():
    if not r or r['status'] not in ('ok', 'weak'): fix[r['status'] if r else 'none'] += 1; continue
    ps = NOTES[r['note']]['paras']
    pe = unit_end_from(ps, r['p_start']) or r['p_end']
    cand = [u for u in UNITS[r['note']] if u['ps'] <= r['p_start'] <= u['pe'] or u['pe'] == pe]
    if cand:
        u = cand[0]
        if u['uid'] is None: u['uid'] = [uid]
        else: u['uid'].append(uid)
        fix['joined'] += 1
    else:
        UNITS[r['note']].append({'pv': verse_start_before(ps, r['p_start']), 'ps': r['p_start'], 'pe': pe, 'uid': [uid], 'src': 'text'}); fix['added'] += 1
print(fix)
# 3. order, and the commentary range of each unit: after its translation, up to the next unit's verse block
order = sorted(NOTES)
out = []
for k, name in enumerate(order):
    us = sorted(UNITS[name], key=lambda u: u['ps'])
    ps = NOTES[name]['paras']
    for j, u in enumerate(us):
        nxt = us[j + 1]['pv'] if j + 1 < len(us) else len(ps)
        u['cs'], u['ce'] = u['pe'] + 1, nxt - 1      # inclusive; may be empty
        body = [ps[i] for i in range(u['cs'], u['ce'] + 1)] if u['ce'] >= u['cs'] else []
        u['prose_chars'] = sum(len(p['text']) for p in body if p['kind'] == 'prose')
        u['foot_chars'] = sum(len(p['text']) for p in body if p['kind'] == 'foot')
        u['note'] = name
        out.append(u)
json.dump(out, open('units-pos.json', 'w'), ensure_ascii=False)
c = collections.Counter((u['src'], u['uid'] is not None) for u in out); print(c)
print('total units', len(out), 'with commentary prose', sum(1 for u in out if u['prose_chars'] > 0), 'chars', sum(u['prose_chars'] for u in out), 'foot', sum(u['foot_chars'] for u in out))
