# Render each body page as three overlapping horizontal bands (JPEG, long side <= 1500 px) for reading the calls.
import pymupdf, os
PDF = r'C:\Vaults\Obsidian Vault\Library\Trika\G. T. Deshpande - Abhinavagupta-Sahitya Akademi (1995).pdf'
OUT = os.path.expanduser(r'~\fnwork\desh\bands')
os.makedirs(OUT, exist_ok=True)
d = pymupdf.open(PDF)
for K in range(14, 165):
    p = d[K - 1]; r = p.rect
    for i, (a, b) in enumerate([(0.03, 0.40), (0.35, 0.70), (0.65, 0.99)]):
        clip = pymupdf.Rect(r.x0 + r.width * 0.04, r.y0 + r.height * a, r.x1 - r.width * 0.02, r.y0 + r.height * b)
        z = min(1300 / clip.width, 1500 / clip.height)
        p.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip, colorspace=pymupdf.csGRAY).save(os.path.join(OUT, 'p%03d-%d.jpg' % (K, i + 1)), jpg_quality=80)
print(len(os.listdir(OUT)), 'bands')
