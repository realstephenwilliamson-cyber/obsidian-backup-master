# supnum2.py (2 Nov 2026, Chapter Twenty-Eight): reads the superscript number at each footnote start (fnstarts2.py's
# output) by cutting the superscript into digit glyphs and matching them against templates (TeX Gyre Termes digits at
# first; with --tpl, templates averaged from the book's own glyphs). supnum.py's Tesseract reading fails for 3 digits.
# Usage: supnum2.py STARTS.json OUT.json [--tpl TPL.npz] [--dump GLYPHS.npz]
import sys, json, csv, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
IMG = '/home/claude/lost/ch28/img300/p-%03d.png'; TSV = '/home/claude/lost/ch28/tsv/p-%03d.tsv'
args = sys.argv[1:]; S = json.load(open(args[0])); out = args[1]
tplf = args[args.index('--tpl') + 1] if '--tpl' in args else None
dumpf = args[args.index('--dump') + 1] if '--dump' in args else None
CW, CH = 16, 24   # canvas for comparison
def norm(g):
    # g: bool array of one glyph (tight); scale to height CH keeping aspect, centre on a CW x CH canvas
    h, w = g.shape; s = CH / h; nw = max(1, min(CW, int(round(w * s))))
    r = cv2.resize(g.astype(np.float32), (nw, CH), interpolation=cv2.INTER_AREA)
    c = np.zeros((CH, CW), np.float32); x = (CW - nw) // 2; c[:, x:x + nw] = r; return c
def font_tpl():
    f = ImageFont.truetype('/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-regular.otf', 120)
    T = {}
    for d in '0123456789':
        im = Image.new('L', (200, 200), 255); ImageDraw.Draw(im).text((40, 20), d, font=f, fill=0)
        a = np.array(im) < 128; ys, xs = np.where(a); T[d] = norm(a[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    return T
T = font_tpl()
if tplf:
    z = np.load(tplf)
    for d in '0123456789':
        if d in z.files: T[d] = z[d]
def classify(g):
    v = norm(g); best = []
    for d, t in T.items():
        a = v - v.mean(); b = t - t.mean(); sc = float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-6))
        best.append((sc, d))
    best.sort(reverse=True); return best[0][1], best[0][0], best[1][0]
def lines_of(k):
    L = {}
    for r in csv.DictReader(open(TSV % k, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        if r['level'] != '5' or not r['text'].strip(): continue
        key = (r['block_num'], r['par_num'], r['line_num'])
        L.setdefault(key, []).append((int(r['left']), int(r['top']), int(r['width']), int(r['height']), r['text']))
    return L
dump = []
for k in sorted(S, key=int):
    if not S[k]['starts']: continue
    im = np.array(Image.open(IMG % int(k)).convert('L')); dark = im < 200; L = lines_of(int(k))
    for s in S[k]['starts']:
        ws = None
        for key, w in L.items():
            if min(x[1] for x in w) == s['y'] and ' '.join(x[4] for x in w)[:60] == s['ocr'][:60]: ws = sorted(w); break
        s['num2'] = ''; s['conf2'] = 0
        if not ws: continue
        x0 = ws[0][0] - 4
        # the first real word: the first word box (after the first) that starts with a letter; else the second box
        x1 = ws[1][0] - 2 if len(ws) > 1 else ws[0][0] + ws[0][2]
        top = min(x[1] for x in ws); bot = max(x[1] + x[3] for x in ws[1:3]) if len(ws) > 1 else top + 40
        reg = dark[max(0, top - 6):bot + 2, max(0, x0):x1 + 30]
        n, lab, st, _ = cv2.connectedComponentsWithStats(reg.astype(np.uint8), connectivity=8)
        comps = [st[i] for i in range(1, n) if st[i][4] >= 6]
        if not comps: continue
        # baseline: the bottom most common among components right of x1-x0 (the word), else the region bottom
        wb = [c[1] + c[3] for c in comps if c[0] >= x1 - x0 - 2 and c[3] >= 12]
        base = int(np.median(wb)) if wb else reg.shape[0]
        sup = [c for c in comps if c[1] + c[3] <= base - 6 and c[3] >= 8 and c[0] < x1 - x0 + 4]
        sup.sort(key=lambda c: c[0])
        # keep the leftmost run of superscript components (gap < 9 px)
        run = []
        for c in sup:
            if run and c[0] > run[-1][0] + run[-1][2] + 9: break
            run.append(c)
        if not run: continue
        # merge components whose x-ranges overlap (a thin stroke broken: the two arcs of a 0, the foot of a 2)
        mg = []
        for c in run:
            c = [int(v) for v in c]
            if mg and c[0] < mg[-1][0] + mg[-1][2] - 1:
                m = mg[-1]; xa, ya = min(m[0], c[0]), min(m[1], c[1]); xb, yb = max(m[0] + m[2], c[0] + c[2]), max(m[1] + m[3], c[1] + c[3])
                mg[-1] = [xa, ya, xb - xa, yb - ya, m[4] + c[4]]
            else: mg.append(c)
        run = mg
        hs = [c[3] for c in run]; H = max(hs)
        digits = []
        for c in run:
            if c[3] < 0.6 * H: continue     # a dot or mark, not a digit
            x, y, w, h = c[0], c[1], c[2], c[3]
            g = reg[y:y + h, x:x + w]
            nd = max(1, int(round(w / (0.62 * H)))) if w > 0.95 * H else 1
            for j in range(nd):
                gg = g[:, j * w // nd:(j + 1) * w // nd]
                cols = np.where(gg.any(axis=0))[0]; rows = np.where(gg.any(axis=1))[0]
                if not len(cols): continue
                gg = gg[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
                d, sc, sc2 = classify(gg); digits.append((d, sc, sc2)); dump.append((int(k), s['y'], len(digits) - 1, norm(gg)))
        s['num2'] = ''.join(d for d, a, b in digits); s['conf2'] = round(min([a - b for d, a, b in digits] or [0]), 3)
        s['sup_h'] = int(H)
json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1)
if dumpf:
    np.savez_compressed(dumpf, keys=np.array([[a, b, c] for a, b, c, _ in dump]), g=np.array([g for *_, g in dump]))
seq = [(int(k), s['num2'], s['conf2']) for k in sorted(S, key=int) for s in S[k]['starts']]
print(len(seq)); print(' '.join('%d:%s' % (k, n or '?') for k, n, c in seq))
