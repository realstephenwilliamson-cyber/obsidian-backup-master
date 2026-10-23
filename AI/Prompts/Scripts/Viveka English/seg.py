"""Locate each phase-5 unit's translation paragraph(s) in the current library notes, and derive the commentary ranges."""
import json, re, glob, os, unicodedata, collections, sys
sys.path.insert(0, '/home/claude/viv')
import importlib.util
spec = importlib.util.spec_from_file_location('dz', '/home/claude/viv/dz_units2.py'); dz = importlib.util.module_from_spec(spec); spec.loader.exec_module(dz)
P5 = '/mnt/user-data/uploads/Obsidian Vault/.work/plan/phase-5-work/'
uf = json.load(open(P5 + '12oct/units-final.json'))['units']
um = json.load(open(P5 + 'units-matched.json'))
vf = json.load(open(P5 + '12oct/verses-final.json'))

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower())

# ---- paragraphs of every chapter note, with kinds and the page they sit on
NOTES = {}
for f in sorted(glob.glob('lib/*/*.md')):
    name = os.path.basename(f)[:-3]
    raw = open(f, encoding='utf-8').read()
    m = re.match(r'^---\n.*?\n---\n', raw, flags=re.S)
    off = m.end() if m else 0
    paras = []; K = None; label = None; in_foot = False
    # split keeping positions
    for mm in re.finditer(r'(?:[^\n]|\n(?!\s*\n))+', raw[off:]):
        p = mm.group(0).strip()
        if not p: continue
        g = mm.group(0); start = off + mm.start() + (len(g) - len(g.lstrip()))
        pm = dz.PAGE.match(p)
        if pm:
            label, K = pm.group(1), int(pm.group(2)); in_foot = False
            paras.append({'kind': 'page', 'K': K, 'label': label, 'pos': start, 'text': p}); continue
        if p.startswith('[[') and '|contents]]' in p:
            paras.append({'kind': 'nav', 'K': K, 'pos': start, 'text': p}); continue
        if in_foot:
            paras.append({'kind': 'foot', 'K': K, 'pos': start, 'text': p}); continue
        if dz.FOOT.match(p) or dz.footnote_like(p):
            in_foot = True; paras.append({'kind': 'foot', 'K': K, 'pos': start, 'text': p}); continue
        lines = [l for l in p.split('\n') if l.strip()]
        kinds = [dz.line_kind(l) for l in lines]
        if lines and all(kinds):
            paras.append({'kind': 'verse', 'K': K, 'pos': start, 'text': p}); continue
        paras.append({'kind': 'prose', 'K': K, 'pos': start, 'text': p})
    for i, p in enumerate(paras): p['i'] = i; p['n'] = norm(p['text'])
    NOTES[name] = {'path': f, 'paras': paras, 'raw': raw}

# ---- find each unit
def find(uid):
    t = uf.get(str(uid))
    if t is None: return None
    if isinstance(uid, str) or str(uid).startswith('n'): return {'uid': uid, 'status': 'new (not in the library copy)'}
    u = dict(um[int(uid)])
    note = NOTES.get(u['note'])
    if not note:
        alt = [os.path.basename(v['chapter_note'])[:-3] for v in vf.values() if uid in v['units'] and v.get('chapter_note')]
        if alt and alt[0] in NOTES: u['note'] = alt[0]; note = NOTES[alt[0]]
        else:
            pre = u['note'][:len('Tantraloka Dyczkowski v09')]
            cands = [n for n in NOTES if n.startswith(pre)]
            # search every note of the volume
            u['note'] = None
            for n in cands:
                if norm(t)[:45] in ''.join(p['n'] for p in NOTES[n]['paras']): u['note'] = n; note = NOTES[n]; break
            if not note: return {'uid': uid, 'status': 'note missing'}
    nt = norm(t)
    if u['note'] not in (um[int(uid)]['note'],): ks_override = True
    else: ks_override = False
    head, tail = nt[:45], nt[-45:]
    ks = {u['K_start'], u['K'], u['K_verse']} - {None}
    lo, hi = (min(ks) - 1, max(ks) + 1) if ks and not ks_override else (-10**9, 10**9)
    cand = [p for p in note['paras'] if p['kind'] in ('prose', 'verse') and p['K'] is not None and lo <= p['K'] <= hi] or [p for p in note['paras'] if p['kind'] in ('prose', 'verse')]
    def best(s, which):
        bestp, bs = None, 0
        for p in cand:
            if s and s in p['n']: return p, 1.0
        # fuzzy: share of 3-grams
        g = {s[i:i + 3] for i in range(len(s) - 2)}
        for p in cand:
            pn = p['n'][:len(s) + 80] if which == 'head' else p['n'][-(len(s) + 80):]
            h = {pn[i:i + 3] for i in range(len(pn) - 2)}
            sc = len(g & h) / max(1, len(g))
            if sc > bs: bestp, bs = p, sc
        return bestp, bs
    ph, sh = best(head, 'head'); pt, st = best(tail, 'tail')
    if not ph or not pt: return {'uid': uid, 'status': 'not found'}
    if pt['i'] < ph['i']: pt, st = ph, min(sh, st)
    return {'uid': uid, 'note': u['note'], 'p_start': ph['i'], 'p_end': pt['i'], 'score': round(min(sh, st), 2), 'status': 'ok' if min(sh, st) >= 0.6 else 'weak'}

used = []
for v in vf.values():
    for x in v['units']:
        if x not in used: used.append(x)
res = {str(x): find(x) for x in used}
c = collections.Counter(r['status'] if r else 'none' for r in res.values()); print(c)
json.dump(res, open('found.json', 'w'), ensure_ascii=False)

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'show':
    import random
    random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    for k, r in random.sample([x for x in res.items() if x[1] and x[1]['status'] == (sys.argv[3] if len(sys.argv) > 3 else 'ok')], 6):
        n = NOTES[r['note']]; t = uf[k]
        print('UNIT', k, r['score'], r['note'][22:], r['p_start'], r['p_end'])
        print('  final:', t[:110], '...', t[-60:])
        print('  start:', n['paras'][r['p_start']]['text'][:110].replace('\n', ' '))
        print('  end  :', n['paras'][r['p_end']]['text'][-110:].replace('\n', ' '))
