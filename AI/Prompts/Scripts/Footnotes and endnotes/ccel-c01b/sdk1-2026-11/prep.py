# prep.py (SDK 1): case files for the readers: for each differing page block, cases/cNNN.block.txt (the note's page block, raw),
# cNNN.pdf.txt (the PDF's text of that page), cNNN.jpg (the page at 110 dpi, JPEG). Index: cases.json.
import json, re, os, sys, pymupdf
V = 'C:/Vaults/Obsidian Vault/'
P = json.load(open('pdftext.json', encoding='utf-8'))['text']; NOTES = json.load(open('notes.json', encoding='utf-8'))
rows = json.load(open('diff-blocks.json', encoding='utf-8'))
extra = json.load(open('extra.json', encoding='utf-8')) if os.path.exists('extra.json') else []
os.makedirs('cases', exist_ok=True)
docs = {k: pymupdf.open(V + k) for k in P}
def block(t, K):
    m = re.search(r'^\*\[[^\]]+\]\* \^pg%d\s*$' % K, t, re.M)
    m2 = re.search(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', t[m.end():], re.M)
    return t[m.start(): m.end() + m2.start() if m2 else len(t)]
idx = []
for i, r in enumerate(rows + extra):
    cid = 'c%03d' % i; pdf = [k for k in P if ('Augustine' in k) == ('Augustine' in r['path'])][0]
    b = block(NOTES[r['path']], r['K'])
    open(f'cases/{cid}.block.txt', 'w', encoding='utf-8', newline='').write(b)
    open(f'cases/{cid}.pdf.txt', 'w', encoding='utf-8').write(P[pdf][str(r['K'])])
    pg = docs[pdf][r['K'] - 1]; pix = pg.get_pixmap(dpi=110); pix.save(f'cases/{cid}.jpg', jpg_quality=75)
    idx.append(dict(r, id=cid, pdf=pdf))
json.dump(idx, open('cases.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(idx), 'cases')
