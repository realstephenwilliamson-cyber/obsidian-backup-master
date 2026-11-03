# pass2.py: the placeholder runs that the 27 Oct boxes do not cover: located on the page by the text layer (the words before or
# after the gap), a strip of that line (and the one above and below), 200 dpi, ten to a sheet. -> sheets3/, tasks3.json, runs2.json
import json, re, unicodedata, pymupdf, os
from PIL import Image, ImageDraw, ImageFont
N = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/xfer/dy-notes.json'))
M = json.load(open('matched.json'))
P = '/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. %s.pdf'
PH = r'\\\[illegible\\\]'; RUN = re.compile(PH + r'(?:[ \t]*' + PH + r')*')
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'\[\^[^\]]*\]|\\|\*|<[^>]+>|' + PH, ' ', s)).strip()
fold = lambda s: ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if c.isascii() and c.isalnum())
covered = set((v['path'], v['start']) for v in M.values())
runs = []
for p, t in N.items():
    vol = re.search(r'vol (\d\d)', p).group(1)
    for m in RUN.finditer(t):
        if (p, m.start()) in covered: continue
        Ks = re.findall(r'\^pg(\d+)', t[:m.start()])
        if not Ks: continue
        b = norm(t[max(0, m.start() - 160):m.start()]).split(' ')[-6:]; a = norm(t[m.end():m.end() + 160]).split(' ')[:6]
        runs.append({'path': p, 'start': m.start(), 'end': m.end(), 'n': m.group(0).count('[illegible'), 'vol': vol, 'K': int(Ks[-1]),
                     'before': ' '.join(b), 'after': ' '.join(a)})
print(len(runs), 'runs left uncovered,', sum(r['n'] for r in runs), 'placeholders')
docs = {}; os.makedirs('sheets3', exist_ok=True); font = ImageFont.load_default(size=22)
def lines(pg):
    L = []
    for bl in pg.get_text('dict')['blocks']:
        for l in bl.get('lines', []):
            tx = ''.join(s['text'] for s in l['spans'])
            if tx.strip(): L.append((fold(tx), l['bbox']))
    return L
strips, nf = [], 0
for i, r in enumerate(runs):
    r['id'] = 'H%04d' % i
    d = docs.setdefault(r['vol'], pymupdf.open(P % r['vol'])); hit = None
    bw = [w for w in r['before'].split(' ') if fold(w)]; aw = [w for w in r['after'].split(' ') if fold(w)]
    for K in (r['K'], r['K'] + 1):
        if K > len(d): continue
        L = lines(d[K - 1])
        for key, side in ((fold(' '.join(bw[-3:]))[-14:], 'b'), (fold(' '.join(aw[:3]))[:14], 'a'), (fold(' '.join(bw[-2:]))[-10:], 'b'), (fold(' '.join(aw[:2]))[:10], 'a')):
            if len(key) < 6: continue
            h = [bb for tx, bb in L if key in tx]
            if len(h) == 1: hit = (K, h[0]); break
        if hit: break
    if not hit: nf += 1; r['located'] = False; continue
    r['located'] = True; K, (x0, y0, x1, y1) = hit; pg = d[K - 1]; pr = pg.rect; h = min(max(y1 - y0, 9), 15)
    xs = [bl[:4] for bl in pg.get_text('blocks') if bl[4].strip()]
    clip = pymupdf.Rect(min(b[0] for b in xs) - 6, max(pr.y0, y0 - 1.6 * h), max(b[2] for b in xs) + 6, min(pr.y1, y1 + 1.6 * h))
    pix = pg.get_pixmap(dpi=200, clip=clip); strips.append((r['id'], Image.frombytes('RGB', (pix.width, pix.height), pix.samples)))
    r['page'] = K
sheets = []
for n in range(0, len(strips), 10):
    g = strips[n:n + 10]; W = max(im.width for _, im in g) + 10; H = sum(im.height + 34 for _, im in g) + 6
    sh = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(sh); y = 3
    for iid, im in g:
        dr.rectangle([0, y, W, y + 28], fill=(225, 225, 225)); dr.text((8, y + 2), 'ID ' + iid, fill='black', font=font)
        y += 30; sh.paste(im, (5, y)); y += im.height + 4
    nm = 'T%03d' % (len(sheets) + 1); sh.save('sheets3/%s.png' % nm); sheets.append({'sheet': nm, 'ids': [i for i, _ in g]})
json.dump(runs, open('runs2.json', 'w'), ensure_ascii=False)
json.dump({'sheets': sheets}, open('tasks3.json', 'w'))
print('located', len(strips), 'not located', nf, 'sheets', len(sheets))
