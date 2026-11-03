# mk.py: sheets for the placed [illegible] gaps of 27 Oct (leftovers.json, box400/line400 at 400 dpi): each strip is the printed
# line (the union with the box, for gaps over a line end), 200 dpi, the gap boxed in red, ID on a grey bar; 12 strips a sheet.
import json, os, pymupdf
from PIL import Image, ImageDraw, ImageFont
P = '/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. %02d.pdf'
L = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/edits/illeg-2026-10-27/leftovers.json'))
M = json.load(open('matched.json')); items = [r for r in L if 'box400' in r and 'G%04d' % r['id'] in M]
items.sort(key=lambda r: (r['vol'], r['pdf_page'], r['line400'][1]))
os.makedirs('sheets2', exist_ok=True); font = ImageFont.load_default(size=22); docs = {}
k = 72 / 400; DPI = 200; s = DPI / 400
strips = []
for r in items:
    d = docs.setdefault(r['vol'], pymupdf.open(P % r['vol'])); pg = d[r['pdf_page'] - 1]
    bx, ln = r['box400'], r['line400']
    x0, y0 = min(bx[0], ln[0]) - 30, min(bx[1], ln[1]) - 28; x1, y1 = max(bx[2], ln[2]) + 30, max(bx[3], ln[3]) + 22
    clip = pymupdf.Rect(x0 * k, y0 * k, x1 * k, y1 * k) & pg.rect
    pix = pg.get_pixmap(dpi=DPI, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im); ox, oy = clip.x0 / k * s, clip.y0 / k * s
    dr.rectangle([bx[0] * s - ox - 3, bx[1] * s - oy - 3, bx[2] * s - ox + 3, bx[3] * s - oy + 3], outline=(220, 0, 0), width=3)
    strips.append((r, im))
sheets = []
for n in range(0, len(strips), 12):
    g = strips[n:n + 12]; W = max(im.width for _, im in g) + 10; H = sum(im.height + 34 for _, im in g) + 6
    sh = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(sh); y = 3
    for r, im in g:
        dr.rectangle([0, y, W, y + 28], fill=(225, 225, 225)); dr.text((8, y + 2), 'ID G%04d' % r['id'], fill='black', font=font)
        y += 30; sh.paste(im, (5, y)); y += im.height + 4
    name = 'S%03d' % (len(sheets) + 1); sh.save('sheets2/%s.png' % name)
    sheets.append({'sheet': name, 'ids': ['G%04d' % r['id'] for r, _ in g], 'size': sh.size})
T = {}
for r in items:
    b, _, a = r['context'].partition('[?]')
    T['G%04d' % r['id']] = {'before': ' '.join(b.split()[-8:]), 'after': ' '.join(a.split()[:8]), 'n': r['placeholders']}
json.dump({'sheets': sheets, 'items': T}, open('tasks2.json', 'w'), ensure_ascii=False)
print(len(items), 'items', len(sheets), 'sheets; max size', max(s['size'][0] for s in sheets), max(s['size'][1] for s in sheets))
