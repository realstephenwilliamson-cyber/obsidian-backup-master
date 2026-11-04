# third_decide.py: the 44 gaps the two readers' cores still disagreed on, with a third blind reader (C). Filled where C's core
# equals A's or B's core (two of three readers), with the same tests as before. -> tb/rule3.json
import json, glob, re, collections
exec(open('tb/resolve2.py').read().split('rule, third, why')[0])
C = load('read3/C'); third = json.load(open('tb/third.json'))
flag = re.compile(r'wrong|empty|blank|not (?:on|found)|cannot|can.t find|missing|cropped|other line', re.I)
out, why = {}, collections.Counter()
for g in third:
    c = C.get(g)
    if not c: why['no reading'] += 1; continue
    if c.get('conf') == 'low' or flag.search(c.get('note') or ''): why['C low or flagged'] += 1; continue
    p, s, e = pos[g]; t = N1[p]; before = clean(t[max(0, s - 300):s]); after = clean(t[e:e + 300])
    co = lambda r, f: core(f(nf(r)), before, after)
    cs = {co(c['printed'], marks), co(c['printed'], caret)}
    hit = None
    for r in (A[g]['printed'], B[g]['printed']):
        for f in (marks, caret):
            x = co(r, f)
            if x and x in cs: hit = hit or x
    if not hit: why['C agrees with neither'] += 1; continue
    nx = re.match(r'\s*\[\^(\d+)\]:', t[e:e + 20]); pv = re.search(r'\[\^(\d+)\]:?[ \t]*$', t[max(0, s - 20):s])
    if re.fullmatch(r'\d+', hit):
        if (nx and nx.group(1) == hit) or (pv and pv.group(1) == hit): out[g] = {'kind': 'F3', 'fill': ''}; continue
        why['number, not by its label'] += 1; continue
    if '?' in hit or not re.search(r'[A-Za-zĀ-ſḀ-ỿ]', hit) or len(hit.split()) > 6: why['fails a test'] += 1; continue
    out[g] = {'kind': 'T', 'fill': hit, 'A': A[g]['printed'], 'B': B[g]['printed'], 'C': c['printed']}
print(len(out), 'settled;', dict(why))
json.dump(out, open('tb/rule3.json', 'w'), ensure_ascii=False, indent=0)
for g, v in out.items():
    p, s, e = pos[g]; t = N1[p]
    print(g, v['kind'], repr(t[max(0, s - 26):s].replace('\n', '¶')), '«' + v['fill'] + '»', repr(t[e:e + 18].replace('\n', '¶')), '| A', v.get('A'), '| B', v.get('B'), '| C', v.get('C'))
