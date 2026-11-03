# supnum3.py (2 Nov 2026, vol. 6 Chapter Nine): reads each start's superscript number by template matching of its digits.
# Templates are learnt from the starts whose two Tesseract readings (supnum2.py) agree and have as many digits as the
# token has segments. Each start gets num3 (the template reading) and conf3 (lowest digit score).
# Usage: supnum3.py STARTS(supnum2 output).json OUT.json
import json, sys, numpy as np
from PIL import Image
sys.path.insert(0, '/home/claude/lost/ch09/scripts'); from digseg import segments, norm
D = '/home/claude/lost/ch09'
S = json.load(open(sys.argv[1], encoding='utf-8'))
segs = {}
for k in S:
    if not S[k]['starts']: continue
    im = Image.open(f'{D}/img300/p-{int(k):03d}.png').convert('L')
    for i, s in enumerate(S[k]['starts']):
        if 'box' not in s: continue
        segs[(k, i)] = [(x, seg.shape, norm(seg)) for x, seg in segments(im, s['box'])]
tmpl = {str(d): [] for d in range(10)}
for (k, i), sg in segs.items():
    s = S[k]['starts'][i]; a, b = s.get('num2', ''), s.get('num2b', '')
    if a and a == b and len(a) == len(sg):
        for ch, (x, shp, v) in zip(a, sg):
            if 14 <= shp[0] <= 24: tmpl[ch].append(v)
print({d: len(v) for d, v in tmpl.items()})
T = {d: np.mean(v, axis=0) for d, v in tmpl.items() if v}
T = {d: t / np.linalg.norm(t) for d, t in T.items()}
for (k, i), sg in segs.items():
    s = S[k]['starts'][i]; digs, confs = [], []
    for x, shp, v in sg:
        if not (12 <= shp[0] <= 26): continue   # not a superscript-sized mark
        sc = sorted(((float(v @ t), d) for d, t in T.items()), reverse=True)
        digs.append(sc[0][1]); confs.append(round(sc[0][0] - (sc[1][0] if len(sc) > 1 else 0), 3))
    s['num3'] = ''.join(digs); s['conf3'] = min(confs) if confs else 0
json.dump(S, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
seq = [(int(k), s.get('num3', ''), s.get('conf3', 0)) for k in sorted(S, key=int) for s in S[k]['starts']]
print(' '.join('%d:%s' % (k, n) for k, n, c in seq))
