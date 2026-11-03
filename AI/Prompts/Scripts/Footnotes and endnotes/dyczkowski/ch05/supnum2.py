# supnum2.py (2 Nov 2026, ch05): supnum.py with the superscript's extent found by height, not by a 5 px gap (the narrow 1
# of 134 left the crop at the 1 alone): from the first ink at the start, take columns whose ink stays above the
# superscript's bottom (+4 px) until a column reaches lower (the text) or a gap > 14 px. Then digits-only OCR as before.
# Usage: supnum2.py STARTS.json OUT.json
import json, subprocess, sys
import numpy as np
from PIL import Image
S = json.load(open(sys.argv[1])); out = sys.argv[2]; TMP = '/home/claude/lost/ch05/_s2.png'
def ocr(img, psm):
    img.save(TMP)
    r = subprocess.run(['tesseract', TMP, '-', '--psm', str(psm), '-c', 'tessedit_char_whitelist=0123456789'], capture_output=True, text=True, errors='replace')
    return r.stdout.strip()
for k in sorted(S, key=int):
    im = Image.open(f'/home/claude/lost/ch05/img300/p-{int(k):03d}.png').convert('L'); a = np.array(im) < 128
    for s in S[k]['starts']:
        y = s['y']; band = a[y - 2:y + 45, :]
        xs = np.where(band.any(axis=0))[0]
        if not len(xs): s['num'] = ''; continue
        x0 = xs[0]
        # bottom of the first glyph
        c = x0; bot = 0
        while c < x0 + 12 and band[:, c].any(): bot = max(bot, np.where(band[:, c])[0][-1]); c += 1
        lim = bot + 4; x1 = x0; gap = 0
        for c in range(x0, min(band.shape[1], x0 + 120)):
            col = band[:, c]
            if not col.any():
                gap += 1
                if gap > 14: break
                continue
            if np.where(col)[0][-1] > lim: break
            gap = 0; x1 = c
        top = max(0, y - 6); bt = y - 2 + lim + 4
        crop = im.crop((x0 - 6, top, x1 + 6, bt))
        crop = crop.resize((crop.width * 4, crop.height * 4), Image.LANCZOS)
        pad = Image.new('L', (crop.width + 80, crop.height + 80), 255); pad.paste(crop, (40, 40))
        n = ocr(pad, 7)
        if not n: n = ocr(pad, 8)
        s['num'] = n; s['sup_w'] = int(x1 - x0); s['sup_h'] = int(bot)
json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1)
seq = [(int(k), s['num']) for k in sorted(S, key=int) for s in S[k]['starts']]
print(len(seq)); print(' '.join('%d:%s' % (k, n or '?') for k, n in seq))
