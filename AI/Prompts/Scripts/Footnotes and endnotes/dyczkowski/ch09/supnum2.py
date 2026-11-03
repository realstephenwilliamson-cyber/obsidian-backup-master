# supnum2.py (2 Nov 2026, vol. 6 Chapter Nine): reads the superscript number at each footnote start, like supnum.py, but crops
# Tesseract's own box of the line's first word (the misread superscript; 3-digit numbers are about 33 x 18 px at 300 dpi),
# scaled x5, and reads it with digits only (psm 7 and 8; both kept). Usage: supnum2.py STARTS.json OUT.json
import json, subprocess, sys, csv
import numpy as np
from PIL import Image, ImageOps
D = '/home/claude/lost/ch09'
S = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]
def ocr(img, psm):
    img.save('/tmp/_s09b.png')
    r = subprocess.run(['tesseract', '/tmp/_s09b.png', '-', '--psm', str(psm), '-c', 'tessedit_char_whitelist=0123456789'], capture_output=True, text=True)
    return r.stdout.strip()
for k in sorted(S, key=int):
    if not S[k]['starts']: continue
    im = Image.open(f'{D}/img300/p-{int(k):03d}.png').convert('L')
    rows = [r for r in csv.DictReader(open(f'{D}/tsv/p-{int(k):03d}.tsv', encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE) if r['level'] == '5' and r['text'].strip()]
    for s in S[k]['starts']:
        ws = [r for r in rows if abs(int(r['top']) - s['y']) < 14 and r['text'] == s['tok']]
        if not ws: ws = [r for r in rows if abs(int(r['top']) - s['y']) < 14]
        if not ws: s['num2'] = ''; continue
        w = min(ws, key=lambda r: int(r['left']))
        L, T, W, H = (int(w[x]) for x in ('left', 'top', 'width', 'height'))
        if H > 24 or W > 60:   # the superscript ran into a word: keep the top band, up to 45 px
            H = 20; W = min(W, 45)
        crop = im.crop((L - 4, T - 4, L + W + 4, T + H + 4))
        crop = crop.resize((crop.width * 5, crop.height * 5), Image.LANCZOS).point(lambda v: 0 if v < 150 else 255)
        pad = Image.new('L', (crop.width + 100, crop.height + 100), 255); pad.paste(crop, (50, 50))
        s['num2'] = ocr(pad, 7); s['num2b'] = ocr(pad, 8); s['box'] = [L, T, W, H]
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
seq = [(int(k), s.get('num2', ''), s.get('num2b', '')) for k in sorted(S, key=int) for s in S[k]['starts']]
print(len(seq)); print(' '.join('%d:%s/%s' % x for x in seq))
