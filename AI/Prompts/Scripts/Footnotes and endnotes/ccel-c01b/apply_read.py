# C-01(b) held cases (28 Oct 2026): apply the readers' cut points. A case with decision "move" whose start_quote occurs once in its
# page block is cut there; the run (to the block's end) goes to the next page block as in build_spec.py. Checked against the pdf.js text.
import json, re, sys, unicodedata
D = json.load(open(sys.argv[1])); PT = json.load(open(sys.argv[2]))['text']; C = {c['case']: c for c in json.load(open('cases.json'))}
dec = {}
for f in sys.argv[4:]:
    for l in open(f):
        if l.strip(): d = json.loads(l); dec[d['case']] = d
PG = re.compile(r'^\*\[p\. [^\]]+\]\* \^pg(\d+)\s*$'); Z = re.compile(r'^(\d{1,4} |\[\^\d+\]:)')
def pdf(p): return re.search(r'^source_pdf: "?([^"\n]+)"?$', D[p], re.M).group(1)
def vis(s): s = re.sub(r'\[\[([^\]|]*)\|([^\]]*)\]\]', r'\2', s); s = re.sub(r'\[\[([^\]]*)\]\]', r'\1', s); return s.replace('\\', '').replace('*', '')
def norm(s): return re.sub(r'\d', '', ''.join(ch for ch in unicodedata.normalize('NFD', s).lower() if ch.isalnum() and not unicodedata.combining(ch)))
def blocks(L):
    out = {}; cur = None
    for i, s in enumerate(L):
        m = PG.match(s)
        if m:
            if cur: out[cur[0]] = [cur[1] + 1, i]
            cur = (int(m.group(1)), i)
    if cur: out[cur[0]] = [cur[1] + 1, len(L)]
    return out
notes = {}
def get(p):
    if p not in notes: L = D[p].split('\n'); notes[p] = {'L': L, 'B': blocks(L), 'new': {}}
    return notes[p]
def content(n, K):
    if K not in n['new']:
        a, e = n['B'][K]; ls = n['L'][a:e]
        while ls and not ls[-1].strip(): ls.pop()
        n['new'][K] = list(ls)
    return n['new'][K]
done, held = [], []
moves = []
for cid, d in sorted(dec.items()):
    c = C[cid]
    if d.get('decision') != 'move': held.append((cid, d.get('decision'), d.get('note', ''))); continue
    q = d.get('start_quote', ''); A = get(c['path']); seg = '\n'.join(content(A, c['K']))
    if not q or seg.count(q) != 1: held.append((cid, 'quote not found once', q[:40])); continue
    cut = seg.index(q); run = seg[cut:].strip(); head = seg[:cut].rstrip()
    nK, nK2 = norm(PT[pdf(c['path'])][str(c['K'])]), norm(PT[pdf(c['nextpath'])][str(c['nextK'])])
    ws = [norm(w) for w in re.findall(r'[^\W\d_]{5,}', vis(run))]; miss = [w for w in ws if w not in nK2]
    if ws and len(miss) > max(1, len(ws) // 20): held.append((cid, f'{len(miss)}/{len(ws)} words not on page B', '')); continue
    tail = norm(vis(head))[-30:]
    if len(tail) >= 10 and tail not in nK: held.append((cid, 'text before the cut not on page A', '')); continue
    A['new'][c['K']] = head.split('\n') if head else []
    moves.append((c, run)); done.append(cid)
for c, run in moves:
    Bn = get(c['nextpath']); ls = content(Bn, c['nextK'])
    z = next((i for i, s in enumerate(ls) if Z.match(s)), None)
    if z is None: ls[len(ls):] = ['', run] if ls else [run]
    else: ls[z:z] = [run, '']
edits = {}
for p, n in notes.items():
    for K, new in n['new'].items():
        a, e = n['B'][K]; old = n['L'][a:e]
        while old and not old[-1].strip(): old.pop()
        o, nw = '\n'.join(old), '\n'.join(new)
        if o != nw: assert D[p].count(o) == 1, (p, K); edits.setdefault(p, []).append([o, nw])
allb = ''.join(sorted(D[p] for p in edits)); fin = {}
for p, E in edits.items():
    t = D[p]
    for o, nw in E: t = t.replace(o, nw)
    fin[p] = t
assert sorted(re.sub(r'\s', '', allb)) == sorted(re.sub(r'\s', '', ''.join(sorted(fin.values())))), 'characters differ'
json.dump({'backup': '.work/backup-c01b-2026-10-28b', 'edits': edits}, open(sys.argv[3], 'w'), ensure_ascii=False)
json.dump({'moved': done, 'held': held}, open('read-result.json', 'w'), ensure_ascii=False, indent=1)
print('moved', len(done), 'held', len(held), 'notes', len(edits)); [print('  ', h) for h in held]
