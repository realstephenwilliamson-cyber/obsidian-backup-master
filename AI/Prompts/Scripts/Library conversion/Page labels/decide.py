# Item 4 decision rule (28 Oct 2026, after-28-Oct session). An edit is kept when no page it depends on reads a different number
# and the pages that carry its evidence read as marked: a fill needs one of its page or its two neighbours read as marked;
# a range or label needs its first marker (or the second, when the first prints none and the two agree by distance) and its last
# marker (or the second-to-last, likewise) read as marked.
import json, re
D = json.load(open('deps.json')); K = {k['id']: k for k in json.load(open('key.json'))}
rd = {}
for i in (1, 2, 3, 4):
    for l in open(f'read{i}.jsonl'):
        if l.strip(): d = json.loads(l); rd[d['id']] = d
byPK = {(k['path'], k['K']): rd.get(k['id'], {}).get('printed') for k in K.values()}
R2I = lambda s: (lambda v: sum(v[i] if i + 1 == len(s) or v[i] >= v[i + 1] else -v[i] for i in range(len(s))))([{'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}[c] for c in s])
def val(N):
    N = str(N).strip().lower()
    if re.fullmatch(r'\d+', N): return ('a', int(N))
    if re.fullmatch(r'[ivxlcdm]+', N): return ('r', R2I(N))
    return None
def st(p, K, N):
    r = byPK.get((p, K))
    if r is None: return 'missing'
    r = str(r).strip().lower()
    if r in ('none', 'unclear', 'noimage', ''): return r or 'none'
    return 'ok' if r == str(N).strip().lower() else 'diff'
keep, hold, contra = [], [], {}
for e in D['edits']:
    S = {role: (st(p, K, N), p, K, N) for p, K, N, role in e['deps']}
    diffs = [(v[1], v[2], v[3], byPK.get((v[1], v[2]))) for v in S.values() if v[0] == 'diff']
    for d in diffs: contra[(d[0], d[1])] = d
    why = []
    if diffs: why.append('a page reads a different number')
    if e['kind'] == 'fill':
        if not any(v[0] == 'ok' for v in S.values()): why.append('no page reads as marked')
    elif e['deps']:
        def end(a, b):
            if a not in S: return False
            if S[a][0] == 'ok': return True
            if S[a][0] == 'none' and b in S and S[b][0] == 'ok':
                va, vb = val(S[a][3]), val(S[b][3])
                return bool(va and vb and va[0] == vb[0] and abs(vb[1] - va[1]) == abs(S[b][2] - S[a][2]))
            return False
        if not end('first', 'first2'): why.append('first page not confirmed')
        if not end('last', 'last2'): why.append('last page not confirmed')
    else: why.append('no printed marker')
    (hold if why else keep).append({**e, 'status': {k: v[0] for k, v in S.items()}, 'why': why})
json.dump({'keep': keep, 'hold': hold, 'contradicted': [list(v) for v in contra.values()]}, open('decided.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('keep', len(keep), Counter(e['kind'] for e in keep)); print('hold', len(hold), Counter(w for e in hold for w in e['why']))
print('contradicted pages', len(contra))
print(Counter(str(rd[i].get('printed')).lower() if str(rd[i].get('printed')).lower() in ('none','unclear','noimage') else 'number' for i in rd))
