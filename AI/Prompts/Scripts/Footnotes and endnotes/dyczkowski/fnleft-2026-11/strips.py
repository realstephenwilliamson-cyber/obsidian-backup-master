# strips.py: for the items still to read, a strip around the line where the footnote's first words begin (two lines above,
# a little below; the page's text column), 200 dpi; ten strips to a sheet with the item id above each. Items the text layer
# could not place get the lower 60 % of each candidate page as its own image. -> sheets/, tasks.json
import json, re, random, pymupdf
from PIL import Image, ImageDraw, ImageFont
from tl import P, full, byid, docs
S = {r['id']: r for r in json.load(open('part1-salvage.json'))}
sig = json.load(open('sig.json'))
todo = [it for it in full if S[it['id']]['status'].split(' (')[0] in ('unread', 'one reading only')]
font = ImageFont.load_default(size=22) if hasattr(ImageFont, 'load_default') else None
import os; os.makedirs('sheets', exist_ok=True)
def col(doc, K):
    xs = [b[:4] for b in doc[K-1].get_text('blocks') if b[4].strip()]
    return min(b[0] for b in xs), max(b[2] for b in xs)
strips, pages = [], []
for it in todo:
    doc = docs.setdefault(it['vol'], pymupdf.open(P % it['vol']))
    o = sig[it['id']]
    if o['sig'] == 'nolocate':
        pages.append(it); continue
    K = o['K']; x0, y0, x1, y1 = o['bbox']; h = min(max(y1 - y0, 8), 14)
    c0, c1 = col(doc, K); pr = doc[K-1].rect
    clip = pymupdf.Rect(max(pr.x0, c0 - 6), max(pr.y0, y0 - 2.4 * h), min(pr.x1, c1 + 6), min(pr.y1, y1 + 0.5 * h))
    pix = doc[K-1].get_pixmap(dpi=200, clip=clip)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    strips.append((it['id'], im))
# sheets of 10, in page order; shuffle within nothing (readers get ids, not answers)
sheets = []
for s in range(0, len(strips), 10):
    grp = strips[s:s+10]; W = max(im.width for _, im in grp) + 20
    H = sum(im.height + 34 for _, im in grp) + 10
    sh = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(sh); y = 5
    for iid, im in grp:
        d.rectangle([0, y, W, y + 28], fill=(225, 225, 225)); d.text((10, y + 2), 'CASE ' + iid, fill='black', font=font)
        y += 30; sh.paste(im, (10, y)); y += im.height + 4
    fn = 'sheet%02d.png' % (len(sheets) + 1); sh.save('sheets/' + fn)
    sheets.append({'file': fn, 'ids': [i for i, _ in grp], 'size': sh.size})
pagefiles = []
for it in pages:
    doc = docs[it['vol']]; fl = []
    for K in it['pages']:
        r = doc[K-1].rect; clip = pymupdf.Rect(r.x0, r.y0 + r.height * 0.40, r.x1, r.y1)
        fn = 'v%s-p%04d-low.png' % (it['vol'], K)
        doc[K-1].get_pixmap(dpi=150, clip=clip).save('sheets/' + fn); fl.append(fn)
    pagefiles.append({'id': it['id'], 'files': fl})
clean = lambda s: re.sub(r'^(\\\[illegible\\\]\s*)+', '', s).replace('\\[illegible\\]', '…')
T = {it['id']: {'label': it['label'], 'first_words': ' '.join(clean(S[it['id']]['after'] if False else it['first_words']).split()[:8])} for it in todo}
json.dump({'sheets': sheets, 'pages': pagefiles, 'items': T}, open('tasks.json', 'w'), ensure_ascii=False, indent=0)
print(len(todo), 'items;', len(strips), 'strips in', len(sheets), 'sheets;', len(pages), 'items on page images;',
      'sheet sizes', min(s['size'][1] for s in sheets), max(s['size'][1] for s in sheets), max(s['size'][0] for s in sheets))
