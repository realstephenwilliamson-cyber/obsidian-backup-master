# Dhvanyaloka: every footnote reference with a quote mark right before it; crop the printed line of each call from the
# PDF and lay the crops out on numbered contact sheets for a visual check (is a quotation mark printed there?).
import os, re, json, glob, difflib, unicodedata, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = r'C:\Vaults\Obsidian Vault'
FOLDER = os.path.join(VAULT, r'Library\Trika\The Dhvanyaloka of Anandavardhana with the Locana (Anandavardhana)')
PDF = os.path.join(VAULT, r'Library\Trika\Anandavardhana - The Dhvanyaloka, with the Locana of Abhinavagupta (1990).pdf')
LAY = json.load(open(os.path.join(HERE, 'layer.json'), encoding='utf-8'))
def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)
cases = []
for f in sorted(glob.glob(os.path.join(glob.escape(FOLDER), '*Translation and Notes*.md'))):
    t = open(f, encoding='utf-8').read(); K = None
    for line in t.split('\n'):
        m = re.search(r'\^pg(\d+)$', line)
        if m and line.startswith('*['): K = int(m.group(1)); continue
        for mm in re.finditer(r'(\S*?)([’\'”"]+)\[\^([A-Z]\d+[a-z]?-\d+)\](?!:)', line):
            pre = line[max(0, mm.start() - 60):mm.start()].split()[-3:] + [mm.group(1)]
            cases.append(dict(f=os.path.basename(f), K=K, id=mm.group(3), word=mm.group(1), quotes=mm.group(2), context=pre))
d = pymupdf.open(PDF)
crops = []
for c in cases:
    K = c['K']; target = [norm(w) for w in c['context'] if norm(w)]
    if not target: continue
    best = None
    for Kp in (K, K + 1, K - 1):
        if not Kp or Kp > len(LAY): continue
        for l in LAY[Kp - 1]['lines']:
            ws = [norm(w['t']) for w in l['w'] if norm(w['t'])]
            words = [x for w in l['w'] for x in w['t'].split()]
            for k in range(len(words)):
                if norm(words[k]) and difflib.SequenceMatcher(None, norm(words[k]), target[-1]).ratio() > 0.85:
                    ctx = ''.join(norm(x) for x in words[max(0, k - 3):k + 1])
                    r = difflib.SequenceMatcher(None, ctx, ''.join(target[-4:])).ratio()
                    if not best or r > best[0]: best = (r, Kp, l)
    if not best or best[0] < 0.6: c['crop'] = None; continue
    c['crop'] = (best[1], best[2]['y'], best[2]['y1'])
    crops.append(c)
# contact sheets: 12 crops per sheet
out = os.path.join(HERE, 'qsheets'); os.makedirs(out, exist_ok=True)
sheet = None; n = 0
for i, c in enumerate(crops):
    if i % 12 == 0:
        if sheet: sheet[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(os.path.join(out, 'sheet%02d.jpg' % (i // 12)), jpg_quality=80)
        doc = pymupdf.open(); pg = doc.new_page(width=700, height=12 * 62 + 20); sheet = (pg, doc)
    pg, doc = sheet
    Kp, y0, y1 = c['crop']; src = d[Kp - 1]; r = src.rect
    clip = pymupdf.Rect(r.x0 + 15, y0 - 4, r.x1 - 10, y1 + 3)
    pix = src.get_pixmap(matrix=pymupdf.Matrix(4, 4), clip=clip)
    row = i % 12; top = 10 + row * 62
    pg.insert_text((5, top + 25), '%d' % (i + 1), fontsize=14)
    pg.insert_image(pymupdf.Rect(40, top, 695, top + 55), pixmap=pix, keep_proportion=True)
    c['n'] = i + 1
if sheet: sheet[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(os.path.join(out, 'sheet%02d.jpg' % ((len(crops) - 1) // 12 + 1)), jpg_quality=80)
json.dump(cases, open(os.path.join(HERE, 'quotecases.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('cases', len(cases), 'cropped', len(crops), 'sheets', len(os.listdir(out)))
