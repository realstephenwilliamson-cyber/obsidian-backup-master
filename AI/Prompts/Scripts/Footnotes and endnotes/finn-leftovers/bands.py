import pymupdf, os, json, glob
PDF = glob.glob(r'C:\Vaults\Obsidian Vault\Library\Trika\KULACUDAMANI*.pdf')[0]
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'bands'); os.makedirs(OUT, exist_ok=True)
J = json.load(open(os.path.join(HERE, 'leftovers.json')))
d = pymupdf.open(PDF)
for K in sorted(int(k) for k in J):
    p = d[K - 1]; r = p.rect
    for i, (a, b) in enumerate([(0.0, 0.55), (0.45, 1.0)]):
        clip = pymupdf.Rect(r.x0, r.y0 + r.height * a, r.x1, r.y0 + r.height * b)
        z = min(1300 / clip.width, 1500 / clip.height)
        p.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip, colorspace=pymupdf.csGRAY).save(os.path.join(OUT, 'p%03d-%d.jpg' % (K, i + 1)), jpg_quality=75)
ks = sorted(int(k) for k in J)
n = len(ks); parts = [ks[i * n // 5:(i + 1) * n // 5] for i in range(5)]
for i, part in enumerate(parts):
    json.dump({str(k): J[str(k)]['notes'] for k in part}, open(os.path.join(HERE, 'task%d.json' % (i + 1)), 'w'))
    print('task', i + 1, len(part), 'pages', part[0], '-', part[-1], 'notes', sum(len(J[str(k)]['notes']) for k in part))
