# tsvlines.py PDF Y0 Y1: the TSV lines (top, left, text) of a page between two heights
import csv, sys
k, y0, y1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
L = {}
for r in csv.DictReader(open('/home/claude/lost/ch28/tsv/p-%03d.tsv' % k, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
    if r['level'] != '5' or not r['text'].strip(): continue
    e = L.setdefault((r['block_num'], r['par_num'], r['line_num']), {'t': int(r['top']), 'l': int(r['left']), 'w': []})
    e['t'] = min(e['t'], int(r['top'])); e['l'] = min(e['l'], int(r['left'])); e['w'].append(r['text'])
for e in sorted(L.values(), key=lambda e: e['t']):
    if y0 <= e['t'] <= y1: print(k, e['t'], e['l'], ' '.join(e['w'])[:100])
