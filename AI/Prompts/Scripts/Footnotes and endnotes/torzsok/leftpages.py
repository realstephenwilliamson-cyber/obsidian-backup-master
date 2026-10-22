# Törzsök pages that still have notes not converted: the layer's notes zone has more note starts than the vault page has
# definitions. Writes task files for image readers and renders the page bands.
import sys, os, re, json, glob, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from pdfside import page
VAULT = r'C:\Vaults\Obsidian Vault'
FOLDER = os.path.join(VAULT, r"Library\Trika\The Doctrine of Magic Female Spirits' (Torzsok)")
PDF = os.path.join(VAULT, r'Library\Trika\Torzsok - The Doctrine of Magic Female Spirits (1999).pdf')
SCOPE = set(range(1, 91)) | set(range(201, 354))
defs = {}
for f in glob.glob(os.path.join(glob.escape(FOLDER), '*.md')):
    K = None
    for l in open(f, encoding='utf-8').read().split('\n'):
        m = re.search(r'\^pg(\d+)$', l)
        if m and l.startswith('*['): K = int(m.group(1)); defs[K] = 0; continue
        if K and re.match(r'^\[\^[^\]]+\]:', l): defs[K] += 1
todo = []
for K in sorted(SCOPE):
    p = page(K - 1)
    if not p or not p['notes']: continue
    starts = sum(1 for n in p['notes'] if n['start'])
    if starts > defs.get(K, 0): todo.append(K)
print('pages with unconverted notes', len(todo))
d = pymupdf.open(PDF); OUT = os.path.join(HERE, 'bands'); os.makedirs(OUT, exist_ok=True)
for K in todo:
    p = d[K - 1]; r = p.rect
    for i, (a, b) in enumerate([(0.0, 0.55), (0.45, 1.0)]):
        clip = pymupdf.Rect(r.x0 + r.width * 0.2, r.y0 + r.height * a, r.x1 - r.width * 0.05, r.y0 + r.height * b)
        z = min(1300 / clip.width, 1500 / clip.height)
        p.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip, colorspace=pymupdf.csGRAY).save(os.path.join(OUT, 'p%03d-%d.jpg' % (K, i + 1)), jpg_quality=75)
n = len(todo); parts = [todo[i * n // 6:(i + 1) * n // 6] for i in range(6)]
for i, part in enumerate(parts):
    json.dump(part, open(os.path.join(HERE, 'vtask%d.json' % (i + 1)), 'w'))
    print('task', i + 1, len(part), part[0], '-', part[-1])
