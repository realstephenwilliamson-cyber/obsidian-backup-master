import json, sys, pymupdf
from PIL import Image
from tl import P, byid, docs
sig = json.load(open('sig.json'))
def strip(i, above=3.5, below=1.5, dpi=200):
    it = byid[i]; o = sig[i]; doc = docs.setdefault(it['vol'], pymupdf.open(P % it['vol']))
    K = o['K']; x0, y0, x1, y1 = o['bbox']; h = min(max(y1 - y0, 8), 14); pr = doc[K-1].rect
    xs = [b[:4] for b in doc[K-1].get_text('blocks') if b[4].strip()]
    clip = pymupdf.Rect(min(b[0] for b in xs) - 6, max(pr.y0, y0 - above * h), max(b[2] for b in xs) + 6, min(pr.y1, y1 + below * h))
    pix = doc[K-1].get_pixmap(dpi=dpi, clip=clip); return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
ids = sys.argv[2:]; ims = [strip(i) for i in ids]
W = max(im.width for im in ims); H = sum(im.height + 12 for im in ims)
sh = Image.new('RGB', (W, H), 'white'); y = 0
for im in ims: sh.paste(im, (0, y)); y += im.height + 12
sh.save(sys.argv[1]); print(sh.size, [(i, byid[i]['label'], byid[i]['first_words'][:40]) for i in ids])
