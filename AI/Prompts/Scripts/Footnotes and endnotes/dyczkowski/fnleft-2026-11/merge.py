# merge.py: two new readers (A Fable, B Sonnet) + the text-layer signal -> decision per item; the 176 settled earlier kept.
import json, glob, collections, unicodedata
S = {r['id']: r for r in json.load(open('part1-salvage.json'))}
sig = json.load(open('sig.json'))
norm = lambda s: unicodedata.normalize('NFC', (s or '').strip().replace("'", '’').replace('"', '”'))
R = {}
for f in glob.glob('readers/g*-[AB].jsonl'):
    role = f[-7]
    for l in open(f, encoding='utf-8'):
        l = l.strip()
        if not l: continue
        try: d = json.loads(l)
        except Exception as e: print('bad line', f, l[:80]); continue
        R.setdefault(d['id'], {})[role] = d
dec = {}; c = collections.Counter(); look = []
for i, s in S.items():
    st = s['status'].split(' (')[0]
    if st in ('strip', 'fill'):
        dec[i] = {'decision': st, 'fill': s.get('fill', ''), 'how': 'SDK 3 readers, 3 Nov' + (' + lead' if i == 'i039' else '')}
        if i == 'i038': look.append((i, 'signal located a body line; SDK readers both nothing'))
        continue
    a, b = R.get(i, {}).get('A'), R.get(i, {}).get('B'); g = sig[i]['sig']
    if not a or not b: dec[i] = {'decision': 'missing reading'}; look.append((i, 'missing reading')); continue
    ea, eb = norm(a.get('between')), norm(b.get('between'))
    fa, fb = a.get('found') is True, b.get('found') is True
    if fa and fb and ea == eb == '':
        if g == 'something': dec[i] = {'decision': 'look'}; look.append((i, 'readers nothing, text layer something ' + str(sig[i]['pre'])))
        else: dec[i] = {'decision': 'strip', 'how': 'two readers + text layer ' + g}
    elif fa and fb and ea == eb and ea != 'unclear':
        if g == 'nothing': dec[i] = {'decision': 'look', 'both': ea}; look.append((i, f'readers {ea!r}, text layer nothing'))
        else: dec[i] = {'decision': 'fill', 'fill': ea, 'how': 'two readers + text layer ' + g}
    else:
        dec[i] = {'decision': 'look', 'A': (fa, ea), 'B': (fb, eb)}; look.append((i, f'A {fa} {ea!r} | B {fb} {eb!r} | sig {g} {sig[i].get("pre")}'))
    old = S[i].get('A')
    if old is not None and dec[i]['decision'] in ('strip', 'fill') and norm(old) != norm(dec[i].get('fill', '')):
        look.append((i, f'old single reading {old!r} differs from {dec[i]}'))
for v in dec.values(): c[v['decision']] += 1
json.dump(dec, open('decisions.json', 'w'), ensure_ascii=False, indent=0)
print(c); print(len(look), 'to look at')
for x in look: print(' ', x[0], S[x[0]]['label'], '|', x[1][:150])
print('fills:'); [print(' ', i, S[i]['label'], repr(v['fill'])) for i, v in sorted(dec.items()) if v['decision'] == 'fill']
