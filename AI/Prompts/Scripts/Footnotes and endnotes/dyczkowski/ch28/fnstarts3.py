# fnstarts3.py (2 Nov 2026, Chapter Twenty-Eight; from fnstarts2.py of 28 Oct). Adds sup_ok: whether the line's first glyph
# is a raised digit-sized mark (bottom above the baseline, 12-26 px high at 300 dpi); a token start whose first glyph sits on
# the baseline (a wrapped line beginning with '13ab).' or '2009:') is dropped, and a raised start the token test missed is added.
# fnstarts2.py (28 Oct 2026, Chapter Two pre-pass): footnote starts on each page image, from Tesseract's TSV (300 dpi).
# Zone: the footnote text is set smaller (line pitch about 46-48 px against the body's 51-54 at 300 dpi), below a rule.
# A line is in the zone from the first line after which the pitch stays footnote-sized (or after a detected rule).
# A footnote start: a line at the left margin whose first token is not a word (the superscript number misread: *, °, 'S,
# ”', ©, digits ...) or whose first ink is a small raised mark. Usage: fnstarts2.py IMGDIR TSVDIR OUT.json
import sys, os, csv, json, re
import numpy as np, cv2
from PIL import Image
imgd, tsvd, outf = sys.argv[1:4]
TOK = re.compile(r"^[^A-Za-z]*$|^[^A-Za-z]{1,3}[A-Za-z]$")   # no letters, or 1-3 marks + one letter ('S, *S, “S)
res = {}
for fn in sorted(os.listdir(imgd)):
    if not fn.endswith('.png'): continue
    k = int(fn[2:-4]); im = np.array(Image.open(os.path.join(imgd, fn)).convert('L')); h, w = im.shape; dark = im < 128
    rule = None
    for y in range(int(h * 0.1), h - 20):
        row = dark[y]; xs = np.where(row)[0]
        if len(xs) < w * 0.1: continue
        runs = np.split(xs, np.where(np.diff(xs) > 2)[0] + 1); r = max(runs, key=len)
        if w * 0.12 < len(r) < w * 0.55 and r[0] < w * 0.2:
            a = dark[max(0, y - 7), r[0]:r[-1]].mean(); b = dark[min(h - 1, y + 7), r[0]:r[-1]].mean()
            if a < 0.08 and b < 0.08: rule = y; break
    lines = {}
    for r in csv.DictReader(open(os.path.join(tsvd, fn[:-4] + '.tsv'), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        if r['level'] != '5' or not r['text'].strip(): continue
        key = (r['block_num'], r['par_num'], r['line_num'])
        L, T, W, H = int(r['left']), int(r['top']), int(r['width']), int(r['height'])
        e = lines.setdefault(key, {'l': L, 't': T, 'r': L + W, 'b': T + H, 'words': [], 'boxes': []})
        e['l'] = min(e['l'], L); e['t'] = min(e['t'], T); e['r'] = max(e['r'], L + W); e['b'] = max(e['b'], T + H); e['words'].append(r['text']); e['boxes'].append((L, T, W, H))
    ls = sorted([e for e in lines.values() if e['t'] > 220], key=lambda e: e['t'])   # skip the running head
    if not ls: res[k] = {'rule': rule, 'zone_y': None, 'starts': [], 'lines': 0}; continue
    margin = float(np.percentile([e['l'] for e in ls], 15))
    pitch = [ls[i + 1]['t'] - ls[i]['t'] for i in range(len(ls) - 1)]
    # zone start: rule if found; else the first line i such that the median pitch of the following lines (up to 8) is < 49.5
    zy = rule
    if zy is None:
        for i in range(len(ls) - 1):
            nxt = [p for p in pitch[i:i + 8] if p < 90]
            prv = [p for p in pitch[max(0, i - 6):i] if p < 90]
            if len(nxt) >= 3 and np.median(nxt) < 49.5 and (not prv or np.median(prv) >= 49.5 or i == 0):
                zy = ls[i]['t'] - 5 if i > 0 or not prv else ls[0]['t'] - 5; break
    def sup_ok(e, dbg=False):
        # True: the first glyph is raised and digit-sized; False: it sits on the baseline (or is a small mark); None: unknown
        y0, y1 = max(0, e['t'] - 8), min(h, e['t'] + 50); x0 = max(0, e['l'] - 8)
        full = (im[y0:y1, x0:e['r'] + 2] < 200).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(full, connectivity=8)
        bots = [st[i][1] + st[i][3] for i in range(1, n) if 10 <= st[i][3] <= 30 and st[i][1] >= 1 and st[i][1] + st[i][3] < full.shape[0] - 1 and 45 < st[i][0] < 260]   # near the start: the pages are skewed
        if len(bots) < 4: return None
        base = int(np.median(bots)) + y0
        reg = full[:, :90]
        n, lab, st, _ = cv2.connectedComponentsWithStats(reg, connectivity=8)
        cs = [st[i] for i in range(1, n) if st[i][4] >= 8 and st[i][1] >= 1 and st[i][1] + st[i][3] + y0 <= base + 12]
        if not cs: return None
        cs.sort(key=lambda c: c[0]); first = cs[0]
        group = [c for c in cs if c[0] <= first[0] + first[2] + 2]
        top = min(c[1] for c in group) + y0; bot = max(c[1] + c[3] for c in group) + y0; hh = bot - top
        if dbg: print('   base', base, 'first', top, bot, hh, [list(c) for c in group])
        if bot <= base - 6 and 12 <= hh <= 26: return True
        if bot >= base - 3: return False
        return None
    starts = []
    for e in ls:
        if zy is None or e['t'] < zy: continue
        if e['l'] > margin + 30: continue
        t0 = e['words'][0]
        raised = False
        band = dark[e['t'] - 3:e['b'] + 3, max(0, e['l'] - 6):e['l'] + 60]
        cols = np.where(band.any(axis=0))[0]
        if len(cols):
            c0 = cols[0]; c1 = c0
            for c in cols[1:]:
                if c - c1 > 4: break
                c1 = c
            rows = np.where(band[:, c0:c1 + 1].any(axis=1))[0]
            raised = len(rows) and rows[-1] < band.shape[0] * 0.6 and (c1 - c0) < 40
        tok = bool(TOK.match(t0)) and t0 not in ('—', '-', '(', '[', '‘', '“')
        sup = sup_ok(e, os.environ.get('DBG') == str(k))
        if os.environ.get('DBG') == str(k): print(e['t'], e['l'], sup, ' '.join(e['words'])[:40])
        if (tok or (raised and not re.match(r'^[‘“\'"(]?[A-Za-z]', t0))) and sup is not False or sup is True:
            starts.append({'y': e['t'], 'tok': t0, 'raised': bool(raised), 'sup_ok': sup, 'ocr': ' '.join(e['words'])[:120]})
    res[k] = {'rule': rule, 'zone_y': zy, 'starts': starts, 'lines': len(ls)}
json.dump(res, open(outf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot = 0
for k in sorted(res):
    tot += len(res[k]['starts']); print(k, res[k]['rule'], res[k]['zone_y'], len(res[k]['starts']), ' | '.join(s['ocr'][:28] for s in res[k]['starts']))
print('total', tot)
