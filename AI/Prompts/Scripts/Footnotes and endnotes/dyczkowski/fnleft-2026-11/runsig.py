import json, collections
from sig import signal, byid
from tl import full
S = json.load(open('part1-salvage.json')); st = {r['id']: r for r in S}
out = {}
for it in full:
    r = signal(it)
    if r is None: out[it['id']] = {'sig': 'nolocate'}; continue
    pre = r['pre']
    out[it['id']] = {'sig': 'something' if len(pre) >= 2 else ('nothing' if len(pre) <= 1 else '?'), 'pre': pre, 'K': r['K'], 'n': r['n'], 'bbox': r['bbox']}
json.dump(out, open('sig.json', 'w'), ensure_ascii=False, indent=0)
c = collections.Counter()
for i, o in out.items():
    s = st[i]['status'].split(' (')[0]
    c[(s, o['sig'])] += 1
for k, v in sorted(c.items()): print(k, v)
print('--- disagreements on read items')
for i, o in out.items():
    s = st[i]['status'].split(' (')[0]
    if (s == 'strip' and o['sig'] != 'nothing') or (s == 'fill' and o['sig'] != 'something') or (s == 'one reading only' and (o['sig'] == 'something') != bool(st[i].get('A'))):
        print(i, s, o['sig'], o.get('pre'), byid[i]['label'], byid[i]['first_words'][:30])
