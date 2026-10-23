import json, re, collections, os
exec(open('seg.py').read().split("# ---- find each unit")[0])
units = json.load(open('units-pos.json'))

# ---- 22 Oct, third pass: where a unit's verse block was not found right before its translation (a translation in several
# paragraphs, or footnotes between the verse and the translation), the heading goes before the verse block, found by
# looking back for the Devanagari; a block broken by a page's footnotes is followed back over them; the book's subheading
# just before a verse block goes with that verse.
def _deva_block(p):
    t = p['text']; d = len(dz.DEVA.findall(t)); l = len(re.findall(r'[A-Za-zĀ-ſḀ-ỿ]', t))
    return p['kind'] in ('verse', 'prose') and d >= 15 and d >= 0.3 * (d + l)
def _skippable(p):
    t = p['text']
    return p['kind'] in ('page', 'foot', 'nav') or bool(dz.FOOT.match(t)) or bool(re.match(r'^(?:\\\*|\*)\s', t)) or dz.footnote_like(t)
ENGW = re.compile(r"\b(the|and|of|is|in|to|that|this|which|with|he|it|as|by|for|are|be)\b", re.I)
def _versey(p):
    t = p['text']
    if p['kind'] == 'verse' or _deva_block(p): return True
    if len(t) > 700: return False
    letters = re.findall(r'[A-Za-zĀ-ſḀ-ỿ]', t)
    if not letters or ENGW.search(t): return False
    return bool(dz.IAST_C.search(t)) or bool(re.search(r'(\||॥)\s*\d*\s*(\||॥)?\s*$', t))
def _extend_back(paras, j, lo):
    k, start = j - 1, j
    while k >= lo:
        p = paras[k]
        if _skippable(p): k -= 1; continue
        if _versey(p): start = k; k -= 1; continue
        break
    k = start - 1
    while k >= lo and paras[k]['kind'] == 'prose' and dz.is_heading(paras[k]['text']) and '|' not in paras[k]['text']: start = k; k -= 1
    return start
REFINED = collections.Counter()
_bynote = collections.defaultdict(list)
for u in units: _bynote[u['note']].append(u)
for name, us in _bynote.items():
    us.sort(key=lambda u: u['ps']); paras = NOTES[name]['paras']
    for j, u in enumerate(us):
        lo = us[j - 1]['pe'] + 1 if j else 0
        old = u['pv']
        if u['pv'] == u['ps']:
            d = next((k for k in range(u['ps'] - 1, lo - 1, -1) if _deva_block(paras[k])), None)
            if d is not None: u['pv'] = _extend_back(paras, d, lo); REFINED['verse block found before the translation'] += 1
        else:
            nv = _extend_back(paras, u['pv'], lo)
            if nv < u['pv']: u['pv'] = nv; REFINED['verse block or subheading extended back'] += 1
        u['_oldpv'] = old
    for j, u in enumerate(us):
        nxt = us[j + 1]['pv'] if j + 1 < len(us) else len(paras)
        u['ce'] = nxt - 1
print('refined', dict(REFINED))
ROMAN = {1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI',7:'VII',8:'VIII',9:'IX',10:'X',11:'XI'}
# uid -> vault verses
u2v = collections.defaultdict(list)
for vid, v in vf.items():
    for x in v['units']: u2v[str(x)].append(vid)
def vlabel(vids):
    vids = sorted(set(vids), key=lambda s: (int(s.split('.')[0]), int(s.split('.')[1])))
    a, b = vids[0], vids[-1]
    ca, va = int(a.split('.')[0]), int(a.split('.')[1]); cb, vb = int(b.split('.')[0]), int(b.split('.')[1])
    if a == b: return f'{ca}.{va}'
    if ca == cb: return f'{ca}.{va}–{vb}'
    return f'{ca}.{va}–{cb}.{vb}'
order = sorted(NOTES)
seq = []      # all units in reading order
for name in order:
    for u in sorted([u for u in units if u['note'] == name], key=lambda u: u['ps']): seq.append(u)
# labels
for u in seq:
    vids = [v for x in (u['uid'] or []) for v in u2v.get(str(x), [])]
    if vids: u['label'] = 'TĀ ' + vlabel(vids)
    else:
        mk = dz.TAIL.search(NOTES[u['note']]['paras'][u['pe']]['text'])
        m = (mk.group(2) or mk.group(1)) if mk else None
        u['label'] = f"Dyczkowski's verse {dz.fix_marker(m)}" if m else f"Unit {u['ps']}"

# ---- 22 Oct, second pass: units that are not Tantraloka verses (quotations Jayaratha gives with their own numbers,
# figure labels, numbers garbled by the OCR) are folded back into the commentary of the verse before them
vmax = collections.defaultdict(int)
for vid in vf:
    c_, v_ = vid.split('.'); vmax[int(c_)] = max(vmax[int(c_)], int(v_))
def tav(u):
    vids = sorted({v for x in (u['uid'] or []) for v in u2v.get(str(x), [])}, key=lambda s: (int(s.split('.')[0]), int(s.split('.')[1])))
    return int(vids[0].split('.')[0]), int(vids[0].split('.')[1]), int(vids[-1].split('.')[1])
FALSE = []
for i, u in enumerate(seq):
    if not u['label'].startswith("Dyczkowski's"): continue
    N = int(re.search(r'\d+', u['label'][len("Dyczkowski's verse"):]).group(0))
    prev = next((w for w in reversed(seq[:i]) if w['label'].startswith('TĀ')), None)
    nxt = next((w for w in seq[i + 1:] if w['label'].startswith('TĀ')), None)
    # only inside a chapter: at a chapter's start or end they may be Jayaratha's own verses or an appendix
    if prev is None or nxt is None: continue
    (c1, a1, b1), (c2, a2, b2) = tav(prev), tav(nxt)
    if c1 != c2: continue
    ok = b1 - 2 <= N <= a2 + 2
    if not ok: FALSE.append(i)
print('folded units', len(FALSE))
fset = set(FALSE); merged = collections.defaultdict(list)
real = []
for i, u in enumerate(seq):
    if i in fset and real:
        P = real[-1]; merged[id(P)].append(u)
        if u['note'] == P['note']:
            P['ce'] = max(P['ce'], u['ce'] if u['ce'] >= u['cs'] else u['pe'])
        else:
            P.setdefault('spill', []).append(u)
    else: real.append(u)
FOLDED = [seq[i] for i in FALSE]
seq = real
# headings per note, unique (second pass: in a stable order; a unit's text may run on over later notes)
order_notes = sorted(NOTES)
inserts = collections.defaultdict(list)   # note -> [(paragraph index, rank, heading line)]
used = collections.defaultdict(set)
def uniq(name, h):
    k, n = h, 2
    while k in used[name]: k = f'{h} ({n})'; n += 1
    used[name].add(k); return k
rank = 0
for i, u in enumerate(seq):
    name = u['note']; ps = NOTES[name]['paras']
    u['h_unit'] = uniq(name, u['label'])
    inserts[name].append((u['pv'], rank, '### ' + u['h_unit'])); rank += 1
    if u['ce'] >= u['cs']:
        u['h_viv'] = uniq(name, 'Viveka on ' + u['label'].replace('TĀ ', ''))
        inserts[name].append((u['cs'], rank, '#### ' + u['h_viv'])); rank += 1
    else: u['h_viv'] = None
    u['conts'] = []
    nxt = seq[i + 1] if i + 1 < len(seq) else None
    if nxt and nxt['note'] != name:
        # every later note up to the next unit's: its opening paragraphs (before the next unit, or all of it) belong here
        for nn in order_notes[order_notes.index(name) + 1: order_notes.index(nxt['note']) + 1]:
            nps = NOTES[nn]['paras']
            first = next((k for k, p in enumerate(nps) if p['kind'] not in ('nav',)), None)
            stop = nxt['pv'] if nn == nxt['note'] else len(nps)
            if first is not None and first < stop and any(p['kind'] == 'prose' for p in nps[first:stop]):
                h = uniq(nn, 'Viveka on ' + u['label'].replace('TĀ ', '') + ' (continued)')
                u['conts'].append((nn, h))
                inserts[nn].append((first, -1, '#### ' + h))
def _heading_like(t):
    # short, no sentence end, and mostly capitalised words (a subheading of the book), or OCR junk
    t2 = re.sub(r'(?:\[\^\d+\]|[\s”’"\'\\*®°]|TM)+$', '', t.strip())
    if len(t2) >= 100 or re.search(r'[.!?:;]$', t2): return False
    long = [w for w in re.findall(r"[A-Za-zĀ-ſḀ-ỿ]+", t2) if len(w) > 3]
    return not long or sum(1 for w in long if w[0].isupper()) >= 0.5 * len(long)
def prose_chars(name, a, b):
    # commentary prose only: a subheading of the book on its own is not commentary
    ps = NOTES[name]['paras']; return sum(len(ps[k]['text']) for k in range(a, b + 1) if ps[k]['kind'] == 'prose' and not _heading_like(ps[k]['text']))
for u in seq:
    u['has'] = (u['ce'] >= u['cs'] and prose_chars(u['note'], u['cs'], u['ce']) > 0) or bool(u['conts'])
def page_label(name, k):
    ps = NOTES[name]['paras']
    for j in range(min(k, len(ps) - 1), -1, -1):
        if ps[j]['kind'] == 'page': return ps[j]['label']
    return None
def vol_of(name): return int(re.search(r'v(\d\d) ', name).group(1))
# 2. the verse-note callouts
pos = {id(u): i for i, u in enumerate(seq)}
byuid = {}
for u in seq:
    for x in (u['uid'] or []): byuid[str(x)] = u
callouts = {}; stats = collections.Counter()
for vid, v in vf.items():
    us = []
    for x in v['units']:
        u = byuid.get(str(x))
        if u and u not in us: us.append(u)
    if not us: stats['no unit'] += 1; continue
    secs = []   # (embed link, label of the unit whose commentary it is, pages)
    for u in us:
        w = u; hops = 0
        while not w['has'] and hops < 3 and pos[id(w)] + 1 < len(seq):
            w = seq[pos[id(w)] + 1]; hops += 1
        if not w['has']: continue
        name = w['note']
        if w['h_viv']: secs.append((f"{name}#{w['h_viv']}", w, page_label(name, w['cs']), page_label(name, w['ce']), hops))
        for n2, h2 in w['conts']: secs.append((f"{n2}#{h2}", w, None, None, hops))
    seen = set(); secs = [s for s in secs if not (s[0] in seen or seen.add(s[0]))]
    if not secs: stats['no commentary'] += 1; continue
    pages = [p for s in secs for p in (s[2], s[3]) if p]
    vol = ROMAN[vol_of(secs[0][1]['note'])]
    pr = (f'p. {pages[0]}' if pages[0] == pages[-1] else f'pp. {pages[0]}–{pages[-1]}') if pages else ''
    after = [s for s in secs if s[4] > 0]
    title = f"Viveka in English (Dyczkowski, vol. {vol}{', ' + pr if pr else ''})"
    lines = [f"> [!viveka]- {title}"]
    if after:
        lines.append(f"> *No commentary follows this verse directly; shown here is the next, after {after[0][1]['label']}.*")
        lines.append('>')
    for k, s in enumerate(secs):
        if k: lines.append('>')
        lines.append(f"> ![[{s[0]}]]")
    callouts[v['path']] = '\n'.join(lines)
    stats['callout'] += 1; stats['after' if after else 'own'] += 1; stats[f'{len(secs)} sections'] += 1
print(stats)
# library inserts as offsets with a check prefix
lib = []
for name, ins in inserts.items():
    n = NOTES[name]; raw = n['raw']; ps = n['paras']
    def u16(i): return len(raw[:i].encode('utf-16-le')) // 2
    items = sorted([(raw.rfind('\n', 0, ps[k]['pos']) + 1, r, h) for k, r, h in ins], key=lambda t: (t[0], t[1]))
    lib.append({'path': 'Library/Trika/Tantraloka (Dyczkowski)/' + os.path.relpath(n['path'], 'lib'), 'len': u16(len(raw)),
                'ins': [[u16(o), h, raw[o:o + 24]] for o, r, h in items]})
json.dump(lib, open('lib-inserts-3.json', 'w'), ensure_ascii=False)
json.dump(callouts, open('verse-callouts-3.json', 'w'), ensure_ascii=False)
json.dump([{k: u.get(k) for k in ('note', 'label', 'h_unit', 'h_viv', 'pv', 'ps', 'pe', 'cs', 'ce', 'uid', 'has')} for u in seq], open('seq-3.json', 'w'), ensure_ascii=False)
print('notes', len(lib), 'headings', sum(len(x['ins']) for x in lib))

json.dump([{k: u.get(k) for k in ('note', 'label', 'pv', 'pe')} for u in FOLDED], open('folded-3.json', 'w'), ensure_ascii=False)
