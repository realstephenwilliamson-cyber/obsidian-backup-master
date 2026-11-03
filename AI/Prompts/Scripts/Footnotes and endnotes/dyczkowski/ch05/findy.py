# findy.py PDF "words": the y (top) and text of the TSV lines on that page containing the words (case-insensitive)
import sys, csv
k, w = int(sys.argv[1]), sys.argv[2].lower()
lines = {}
for r in csv.DictReader(open('/home/claude/lost/ch05/tsv/p-%03d.tsv' % k, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
    if r['level'] != '5' or not r['text'].strip(): continue
    key = (r['block_num'], r['par_num'], r['line_num']); e = lines.setdefault(key, [10**6, 0, []])
    e[0] = min(e[0], int(r['top'])); e[1] = int(r['left']) if not e[2] else e[1]; e[2].append(r['text'])
for t, l, ws in sorted(lines.values()):
    s = ' '.join(ws)
    if w in s.lower(): print(k, t, l, s[:90])
