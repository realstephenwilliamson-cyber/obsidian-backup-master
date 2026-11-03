# tsvlines.py K [Y0]: the Tesseract lines of page K (300 dpi) below Y0, with their top and left
import sys, csv
k = int(sys.argv[1]); y0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
lines = {}
for r in csv.DictReader(open('/home/claude/lost/ch09/tsv/p-%03d.tsv' % k, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
    if r['level'] != '5' or not r['text'].strip(): continue
    key = (r['block_num'], r['par_num'], r['line_num']); e = lines.setdefault(key, [int(r['top']), int(r['left']), []])
    e[0] = min(e[0], int(r['top'])); e[1] = min(e[1], int(r['left'])); e[2].append(r['text'])
for t, l, w in sorted(lines.values()):
    if t >= y0: print(t, l, ' '.join(w)[:90])
