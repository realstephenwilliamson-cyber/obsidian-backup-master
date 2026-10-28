# crop.py VOL PDFPAGE "word1 word2" OUT.png : crops a strip of the page around the first line whose OCR words contain the phrase.
import sys, subprocess, re, html
from PIL import Image
vol, pg, phrase, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
pdf = f'/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. {vol}.pdf'
x = subprocess.run(['pdftotext', '-f', str(pg), '-l', str(pg), '-bbox-layout', pdf, '-'], capture_output=True, text=True).stdout
W = phrase.lower().split()
best = None
for ln in re.findall(r'<line[^>]*>(.*?)</line>', x, re.S):
    ws = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', ln)
    toks = [html.unescape(w[4]).lower() for w in ws]
    if all(any(t.startswith(w[:6]) for t in toks) for w in W):
        best = ws; break
pw = float(re.search(r'<page width="([\d.]+)"', x).group(1))
subprocess.run(['pdftoppm', '-f', str(pg), '-l', str(pg), '-r', '200', '-gray', '-png', '-singlefile', pdf, '/tmp/_crop'], check=True)
im = Image.open('/tmp/_crop.png'); s = im.width / pw
if not best: print('not found'); sys.exit(1)
y0 = min(float(w[1]) for w in best); y1 = max(float(w[3]) for w in best)
im.crop((0, max(0, int((y0 - 14) * s)), im.width, min(im.height, int((y1 + 14) * s)))).save(out)
print(out)
