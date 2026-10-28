# supnum.py: read the superscript number at each footnote start (starts3.json) by cropping it and OCR with digits only.
import json, subprocess, sys
import numpy as np
from PIL import Image
S = json.load(open(sys.argv[1])); out = sys.argv[2]
for k in sorted(S, key=int):
    im = Image.open(f'img300/p-{int(k):03d}.png').convert('L'); a = np.array(im) < 128
    for s in S[k]['starts']:
        y = s['y']; band = a[y - 4:y + 45, :]
        xs = np.where(band.any(axis=0))[0]
        if not len(xs): s['num'] = ''; continue
        x0 = xs[0]; x1 = x0
        for c in xs[1:]:
            if c - x1 > 5: break
            x1 = c
        crop = im.crop((x0 - 6, y - 8, x1 + 6, y + 30)).resize(((x1 - x0 + 12) * 4, 38 * 4), Image.LANCZOS)
        pad = Image.new('L', (crop.width + 80, crop.height + 80), 255); pad.paste(crop, (40, 40)); pad.save('/tmp/_s.png')
        r = subprocess.run(['tesseract', '/tmp/_s.png', '-', '--psm', '7', '-c', 'tessedit_char_whitelist=0123456789'], capture_output=True, text=True)
        s['num'] = r.stdout.strip(); s['sup_w'] = int(x1 - x0)
json.dump(S, open(out, 'w'), ensure_ascii=False, indent=1)
seq = [(int(k), s['num'], s['tok'], s['ocr'][2:22]) for k in sorted(S, key=int) for s in S[k]['starts']]
print(len(seq)); print(' '.join('%d:%s' % (k, n or '?') for k, n, t, o in seq))
