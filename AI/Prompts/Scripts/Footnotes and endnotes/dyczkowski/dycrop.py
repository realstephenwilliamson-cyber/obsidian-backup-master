"""dycrop.py (12 Nov 2026): page strips for Dyczkowski gap fills. For each edit id (gaps-spec / gaps3-spec), find the fill in the note
as it is now, take the PDF page from the last ^pgN mark above it, locate the words before the fill in the page's OCR layer, and cut a
full-width strip (3 lines above, 3 below) at 150 dpi; strips are stacked six to a sheet with the id and the note's text around the fill.
Where the words before the fill occur more than once, it takes the occurrence followed by the note's words after the fill.
Usage: python3 -I dycrop.py VAULT ids.txt OUTDIR"""
import json, re, sys, os, pymupdf
from PIL import Image, ImageDraw
V, IDS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
E = {e['id']: e for f in ('gaps-spec.json', 'gaps3-spec.json') for e in json.load(open(V + '/.work/edits/fnleft-2026-11/' + f, encoding='utf-8'))}
docs, info, strips = {}, [], []
def fill_of(e):
    o, n = e['old'], e['new']; a = 0
    while a < min(len(o), len(n)) and o[a] == n[a]: a += 1
    b = 0
    while b < min(len(o), len(n)) - a and o[-1 - b] == n[-1 - b]: b += 1
    return n[:a], n[a:len(n) - b], n[len(n) - b:]
for gid in open(IDS).read().split():
    parts = gid.split('+'); e = E[parts[0]]; pre, fill, post = fill_of(e)
    t = open(V + '/' + e['path'], encoding='utf-8').read(); k = t.find(e['new'])
    if k < 0: info.append({'id': gid, 'error': 'not found in note'}); continue
    pos = k + len(pre); pg = [int(m.group(1)) for m in re.finditer(r'\^pg(\d+)', t[:pos])][-1]
    src = re.search(r'^source_pdf: (.+)$', t, re.M).group(1).strip()
    d = docs.setdefault(src, pymupdf.open(V + '/' + src))
    words = re.findall(r'[A-Za-z]{4,}', pre)[-3:]; page = None; rect = None
    after = re.findall(r'[A-Za-z]{4,}', re.sub(r'\[\^[^\]]*\]:?|#+[^\n]*|\(\d+\)', ' ', post))[:3]
    toks = pre.split()
    best = (-1, None, None)   # (score, page, rect): the hit whose next words on the page are the note's words after the fill
    for pno in (pg, pg + 1, pg - 1):
        p = d[pno - 1]
        for w in (' '.join(toks[-3:]), ' '.join(toks[-2:]), ' '.join(words), ' '.join(words[-2:]), words[-1] if words else ''):
            if not w: continue
            for r in p.search_for(w):
                box = p.get_textbox(pymupdf.Rect(r.x1, r.y0 - 2, p.rect.width, r.y1 + 30)) + ' ' + p.get_textbox(pymupdf.Rect(0, r.y1, p.rect.width, r.y1 + 30))
                sc = sum(a in box for a in after) + (1 if pno == pg else 0)
                if sc > best[0]: best = (sc, pno, r)
            if best[1]: break
        if best[0] >= len(after) + 1: break
    page, rect = best[1], best[2]
    rec = {'id': gid, 'path': e['path'].split('/')[-1], 'fill': fill, 'ctx': (pre[-60:] + '⟦' + fill + '⟧' + post[:40]).replace('\n', ' '), 'pdf_page': page or pg, 'located': bool(rect), 'score': best[0], 'next': (d[(page or pg) - 1].get_textbox(pymupdf.Rect(rect.x1, rect.y0 - 2, d[(page or pg) - 1].rect.width, rect.y1 + 2)) if rect else '')[:60]}
    p = d[(page or pg) - 1]; W = p.rect.width
    clip = pymupdf.Rect(0, max(0, rect.y0 - 40), W, min(p.rect.height, rect.y1 + 45)) if rect else pymupdf.Rect(0, 0, W, p.rect.height)
    pix = p.get_pixmap(dpi=150 if rect else 70, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    strips.append((rec, im)); info.append(rec)
json.dump(info, open(OUT + '/info.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for s in range(0, len(strips), 6):
    grp = strips[s:s + 6]; Wd = max(im.width for _, im in grp); H = sum(im.height + 22 for _, im in grp)
    sheet = Image.new('RGB', (Wd, H), 'white'); dr = ImageDraw.Draw(sheet); y = 0
    for rec, im in grp:
        dr.text((4, y + 4), f"{rec['id']}  p{rec['pdf_page']}  fill: {rec['fill']}", fill='red'); y += 22
        sheet.paste(im, (0, y)); y += im.height
    sheet.save(f'{OUT}/sheet{s // 6 + 1}.png')
print(json.dumps(info, ensure_ascii=False, indent=0))
