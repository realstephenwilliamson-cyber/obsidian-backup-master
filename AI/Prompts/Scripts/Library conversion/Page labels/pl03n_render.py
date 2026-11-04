# pl03n_render.py (3 Nov 2026, night; page labels, the 14 readable held entries). Renders pages for two blind readers with PyMuPDF (no pdftoppm, no Obsidian).
# Usage: python3 pl03n_render.py LIBRARY_DIR OUT_DIR SEED full|zoom BOOK:PDFPATH:K1-K2,K3 [BOOK:PDFPATH:...]
#   full: whole pages at 110 dpi (the method of 28 Oct); zoom: the top 16 % and bottom 12 % of each page at 250 dpi, joined by a red bar
#   (for pages the full-page readers read unclear or differently; put a few pages whose number is known among them as controls).
# Writes OUT_DIR/img001.png ... (or z01.png ...) in an order shuffled with SEED, and OUT_DIR/key.json {image: [book, K, width, height]}.
# On 3 Nov the zoom strips settled Technics and Time PDF 23 (11 in old-style figures, read "ii" by one full-page reader) and Cyril I PDF 56
# (lii; both full-page readers had read liii). They missed the bottom folios of Technics (cut by the 12 % strip), so use full pages first.
import sys, json, random, fitz
lib, out, seed, mode = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
items = []; pdfs = {}
for arg in sys.argv[5:]:
    book, path, ks = arg.split(':', 2); pdfs[book] = path
    for part in ks.split(','):
        a, _, b = part.partition('-'); items += [(book, k) for k in range(int(a), int(b or a) + 1)]
random.Random(seed).shuffle(items)
key = {}
for n, (book, k) in enumerate(items, 1):
    pg = fitz.open(lib + '/' + pdfs[book])[k - 1]
    if mode == 'full':
        pix = pg.get_pixmap(dpi=110); name = f'img{n:03d}.png'
    else:
        r = pg.rect
        a = pg.get_pixmap(dpi=250, clip=fitz.Rect(r.x0, r.y0, r.x1, r.y0 + r.height * 0.16), colorspace=fitz.csRGB, alpha=False)
        c = pg.get_pixmap(dpi=250, clip=fitz.Rect(r.x0, r.y1 - r.height * 0.12, r.x1, r.y1), colorspace=fitz.csRGB, alpha=False)
        pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, max(a.width, c.width), a.height + c.height + 20), False); pix.set_rect(pix.irect, (255, 0, 0))
        a.set_origin(0, 0); pix.copy(a, a.irect); c.set_origin(0, a.height + 20); pix.copy(c, c.irect); name = f'z{n:02d}.png'
    pix.save(out + '/' + name); key[name] = [book, k, pix.width, pix.height]
json.dump(key, open(out + '/key.json', 'w'), indent=0)
print(len(items), 'images; about', int(sum(w * h for _, _, w, h in key.values()) / 750), 'image tokens per reader')
