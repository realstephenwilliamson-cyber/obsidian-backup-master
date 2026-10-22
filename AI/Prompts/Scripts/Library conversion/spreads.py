#!/usr/bin/env python3
"""For two-page spread scans: printed page pairs per PDF page, from the numbers printed in the top or bottom corners.
usage: spreads.py JOB -> prints summary and writes jobs/<JOB>.spreads.json {pdfpage: "a–b"}"""
import sys, json, re, collections
import pymupdf as fitz
k = sys.argv[1]
j = json.load(open(f'/home/claude/p4/jobs/{k}.json')); d = fitz.open(j['pdf'])
N = len(d); cs = {}
for i in range(N):
    p = d[i]; W, H = p.rect.width, p.rect.height
    if W < H * 1.15: continue
    vals = []
    for w in p.get_text('words'):
        r = fitz.Rect(w[:4]) * p.rotation_matrix   # words come in unrotated coordinates; page.rect is the rotated (shown) page
        x0, y0, x1, y1, t = r.x0, r.y0, r.x1, r.y1, w[4]
        if not re.fullmatch(r'\d{1,3}', t): continue
        if not (y0 < H * 0.1 or y1 > H * 0.92): continue
        n = int(t); k1 = i + 1
        if x1 < W * 0.25: vals.append(n - 2 * k1)          # left page number (left corner)
        elif x0 > W * 0.75: vals.append(n - 1 - 2 * k1)    # right page number (right corner)
        elif x1 < W * 0.5: vals.append(n - 2 * k1)
        else: vals.append(n - 1 - 2 * k1)
    if vals:
        c = collections.Counter(vals).most_common(1)[0][0]; cs[i + 1] = c
# fill: a page takes the offset of its neighbours when both nearest readings agree
off = {}
pages = sorted(cs)
for a in range(1, N + 1):
    if a in cs and (sum(1 for b in range(a - 3, a + 4) if cs.get(b) == cs[a]) >= 2): off[a] = cs[a]
for a in range(1, N + 1):
    if a in off: continue
    l = next((off[b] for b in range(a - 1, max(0, a - 8), -1) if b in off), None)
    r = next((off[b] for b in range(a + 1, min(N + 1, a + 8)) if b in off), None)
    if l is not None and l == r: off[a] = l
res = {str(a): f'{2 * a + c}–{2 * a + c + 1}' for a, c in sorted(off.items()) if 2 * a + c > 0}
runs = []
for a, c in sorted(off.items()):
    if runs and runs[-1][2] == c and runs[-1][1] == a - 1: runs[-1][1] = a
    else: runs.append([a, a, c])
print(k, N, 'pages; spread pages with offsets', len(off), 'runs', [(r[0], r[1], f'left=2k{r[2]:+d}') for r in runs])
json.dump(res, open(f'/home/claude/p4/jobs/{k}.spreads.json', 'w'))
