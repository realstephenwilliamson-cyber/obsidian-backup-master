# C-01(b) spec builder (28 Oct 2026): moves each accepted run (ok.json) from the end of page block K to page block K+1
# (before that block's own footnote zone, or at its end if it has none). Emits whole-block exact-text edits for edits-job2.
import json, re, sys
D = json.load(open(sys.argv[1])); OK = json.load(open(sys.argv[2])); OUT = sys.argv[3]; BK = sys.argv[4]
PG = re.compile(r'^\*\[p\. [^\]]+\]\* \^pg(\d+)\s*$'); Z = re.compile(r'^(\d{1,4} |\[\^\d+\]:)')
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
    if p not in notes:
        L = D[p].split('\n'); notes[p] = {'L': L, 'B': blocks(L), 'new': {}}
    return notes[p]
# block contents as line lists (without trailing blanks)
def content(n, K):
    if K in n['new']: return n['new'][K]
    a, e = n['B'][K]; ls = n['L'][a:e]
    while ls and not ls[-1].strip(): ls.pop()
    n['new'][K] = list(ls); return n['new'][K]
moves = []
for r in sorted(OK, key=lambda r: (r['path'], r['K'])):
    A = get(r['path']); ls = content(A, r['K']); seg = '\n'.join(ls)
    # the run in the current block content: cut offset computed on the original block text from line_a+1
    a, e = A['B'][r['K']]; orig = '\n'.join(A['L'][a:r['line_e']])
    assert orig == seg or seg.startswith(orig[:r['cut']]), ('block changed before removal', r['path'], r['K'])
    head, run = seg[:r['cut']].rstrip(), seg[r['cut']:].strip()
    assert run == r['run'].strip(), ('run mismatch', r['path'], r['K'])
    A['new'][r['K']] = head.split('\n') if head else []
    moves.append((r, run))
for r, run in moves:
    Bn = get(r['nextpath']); ls = content(Bn, r['nextK'])
    z = next((i for i, s in enumerate(ls) if Z.match(s)), None)
    if z is None: ls[len(ls):] = ['', run] if ls else [run]
    else: ls[z:z] = [run, '']
edits = {}; stats = {'runs': len(moves), 'blocks': 0}
for p, n in notes.items():
    E = []
    for K, new in n['new'].items():
        a, e = n['B'][K]; old = n['L'][a:e]
        while old and not old[-1].strip(): old.pop()
        o, nw = '\n'.join(old), '\n'.join(new)
        if o == nw: continue
        if not o.strip(): raise SystemExit(f'empty block {p} {K}')
        assert D[p].count(o) == 1, ('block text not unique', p, K)
        E.append([o, nw]); stats['blocks'] += 1
    if E: edits[p] = E
# simulate and verify
def nums(t): return sorted(re.findall(r'\d+', t))
for p, E in edits.items():
    t = D[p]
    for o, nw in E:
        assert t.count(o) == 1; t = t.replace(o, nw)
    notes[p]['final'] = t
tot_b = sum(len(D[p]) for p in edits); tot_a = sum(len(notes[p]['final']) for p in edits)
allb = ''.join(sorted(D[p] for p in edits)); alla = ''.join(sorted(notes[p]['final'] for p in edits))
assert sorted(re.sub(r'\s', '', allb)) == sorted(re.sub(r'\s', '', alla)), 'characters differ'
for p in edits: assert len(re.findall(r'\^pg\d+', D[p])) == len(re.findall(r'\^pg\d+', notes[p]['final']))
json.dump({'backup': BK, 'edits': edits}, open(OUT, 'w'), ensure_ascii=False)
print(stats, 'notes', len(edits), 'chars', tot_b, '->', tot_a)
