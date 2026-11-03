# build2.py: pass 1 (boxed, read/) and pass 2 (text-layer strips, read2/) -> fills where both readers agree exactly and neither
# is low or flags the spot; edits clustered per note so each old string occurs once. -> gaps-spec.json, gaps-decisions.json
import json, glob, re, unicodedata, collections
N = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/xfer/dy-notes.json'))
loc = {}
for g, m in json.load(open('matched.json')).items(): loc[g] = (m['path'], m['start'], m['end'])
for r in json.load(open('runs2.json')):
    if r.get('located'): loc[r['id']] = (r['path'], r['start'], r['end'])
ctx = {}
for g, v in json.load(open('tasks2.json'))['items'].items(): ctx[g] = (v['before'], v['after'])
for r in json.load(open('runs2.json')): ctx[r['id']] = (r['before'], r['after'])
def load(d):
    R = {}
    for f in glob.glob(d + '/*.jsonl'):
        for l in open(f, encoding='utf-8'):
            l = l.strip()
            if l:
                try: x = json.loads(l); R[x.get('id')] = x
                except Exception: pass
    return R
A = {**load('read/A'), **load('read2/A')}; B = {**load('read/B'), **load('read2/B')}
nf = lambda s: unicodedata.normalize('NFC', (s or '').strip()).replace("'", '’').replace('"', '”')
fw = lambda s: re.sub(r'[^\wāīūṛṝḷṅñṭḍṇśṣḥṁĀĪŪŚṢṬḌṆ]', '', s.lower())
flag = re.compile(r'wrong|empty|blank|not (?:on|found)|cannot|can.t find|missing|cropped|other line', re.I)
dec, why = {}, collections.Counter()
for g, (p, s, e) in loc.items():
    a, b = A.get(g), B.get(g)
    if not a or not b: why['missing reading'] += 1; continue
    if a.get('conf') == 'low' or b.get('conf') == 'low': why['low'] += 1; continue
    if flag.search(a.get('note') or '') or flag.search(b.get('note') or ''): why['flagged in a note'] += 1; continue
    pa, pb = nf(a.get('printed')), nf(b.get('printed'))
    if pa != pb: why['readers differ'] += 1; continue
    if not pa or '?' in pa: why['empty or ?'] += 1; continue
    f = re.sub(r'\^\d+', '', pa).strip()
    if not re.search(r'[A-Za-zĀ-ſḀ-ỿ]', f): why['no letters'] += 1; continue
    bw, aw = ctx[g]; words = f.split()
    lb = fw(bw.split()[-1]) if bw.split() else ''; la = fw(aw.split()[0]) if aw.split() else ''
    if (lb and words and fw(words[0]) == lb and len(lb) > 2) or (la and words and fw(words[-1]) == la and len(la) > 2): why['repeats a neighbour word'] += 1; continue
    if len(words) > 6: why['long (over 6 words)'] += 1; continue
    dec[g] = f
print(len(loc), 'located gaps;', len(dec), 'fills;', dict(why))
E, per = [], collections.defaultdict(list)
for g, f in dec.items(): p, s, e = loc[g]; per[p].append((s, e, f, g))
for p, L in per.items():
    t = N[p]; L.sort()
    def fixed(s, e, f):
        before = t[:s].rstrip(' '); after = t[e:].lstrip(' ')
        if f and before and f[0] in '([‘“' and before[-1] == f[0]: f = f[1:]
        if f and after and f[-1] in ')].,;:’”|' and after[0] == f[-1]: f = f[:-1]
        ls = t.rfind('\n', 0, s) + 1; le = t.find('\n', e); line = t[ls:le if le >= 0 else len(t)]
        if '॥' in line: f = f.replace('||', '॥')
        return f
    cl = []
    for s, e, f, g in L:
        f = fixed(s, e, f)
        if cl and s - cl[-1][-1][1] < 80: cl[-1].append((s, e, f, g))
        else: cl.append([(s, e, f, g)])
    for c in cl:
        S, Ee = c[0][0], c[-1][1]; k = 40
        while True:
            a0, b1 = max(0, S - k), min(len(t), Ee + k); old = t[a0:b1]
            if t.count(old) == 1 or k > 600: break
            k += 40
        new = t[a0:S]
        for i, (s, e, f, g) in enumerate(c): new += f + (t[e:c[i + 1][0]] if i + 1 < len(c) else t[e:b1])
        assert t.count(old) == 1 and '\\[illegible\\]' not in new[S - a0:S - a0 + 3]
        E.append({'id': '+'.join(x[3] for x in c), 'path': p, 'old': old, 'new': new})
json.dump(E, open('gaps-spec.json', 'w'), ensure_ascii=False, indent=0)
json.dump({g: {'fill': f, 'path': loc[g][0]} for g, f in dec.items()}, open('gaps-decisions.json', 'w'), ensure_ascii=False, indent=0)
print(len(E), 'edits,', sum(len(e['id'].split('+')) for e in E), 'gaps,', len(per), 'notes;', round(len(json.dumps(E)) / 1e6, 1), 'MB')
