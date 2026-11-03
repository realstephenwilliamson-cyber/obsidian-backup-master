# mktpl.py (2 Nov 2026): digit templates from the book's own superscripts. For every start that the numbering gave a number
# whose digit count equals the number of glyphs cut, each glyph is taken as that digit; the mean glyph per digit is saved.
# Usage: mktpl.py GLYPHS.npz MAP.json OUT.npz
import sys, json, numpy as np
z = np.load(sys.argv[1]); K = z['keys']; G = z['g']; M = json.load(open(sys.argv[2], encoding='utf-8'))
num = {(r['pdf'], r['y']): r.get('n') for r in M}
byk = {}
for i, (k, y, j) in enumerate(K): byk.setdefault((int(k), int(y)), []).append((int(j), G[i]))
acc = {d: [] for d in '0123456789'}
for key, gl in byk.items():
    n = num.get(key)
    if not n or len(str(n)) != len(gl): continue
    for (j, g), d in zip(sorted(gl, key=lambda x: x[0]), str(n)): acc[d].append(g)
out = {d: np.mean(v, axis=0).astype(np.float32) for d, v in acc.items() if len(v) >= 3}
np.savez(sys.argv[3], **out); print({d: len(v) for d, v in acc.items()})
