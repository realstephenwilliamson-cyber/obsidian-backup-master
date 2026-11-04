# build3.py: the edits for the third round of gap fills (3 Nov 2026, evening), on the notes as pf679 left them (dy-after.json):
#  - rule.json (the two readers agree once footnote marks and copied neighbours are set aside; F = a stray footnote number,
#    taken out), rule3.json (two of three readers agree; F3 as F);
#  - the square brackets of 32 fills of pf679 escaped (\[ \]) as the converter writes them elsewhere in these notes.
# Edits are clustered as in build2.py so that each old string occurs once. -> tb/gaps3-spec.json, tb/gaps3-decisions.json
import json, re, collections
N1 = json.load(open('dy-after.json')); pos = json.load(open('tb/pos.json'))
R = {**json.load(open('tb/rule.json')), **json.load(open('tb/rule3.json'))}
R.pop('H0605', None)                       # 'oṁ hāṁ' before an OCR 'hāhn' that may be the same word: left
R['G3088'] = dict(R['G3088'], fill='kṣaṇāt')  # the bars after it are already in the note (as a \\ garble)
esc = lambda f: re.sub(r'(?<!\\)([\[\]])', r'\\\1', f)
ch = collections.defaultdict(list)   # path -> [(s, e, new, id)]
for g, v in R.items():
    p, s, e = pos[g]; t = N1[p]
    if v['fill'] == '':
        ls = t.rfind('\n', 0, s) + 1; le = t.find('\n', e); le = len(t) if le < 0 else le
        if t[ls:le].strip() == t[s:e]:            # the placeholder is a paragraph of its own: take out the line and one blank line
            a, b = ls, le + 1
            if t[a - 2:a] == '\n\n' and t[b:b + 1] == '\n': b += 1
            ch[p].append((a, b, '', g))
        else:                                       # inline: take out the run and one space next to it
            a, b = s, e
            if t[b:b + 1] == ' ': b += 1
            elif t[a - 1:a] == ' ': a -= 1
            ch[p].append((a, b, '', g))
        continue
    f = v['fill']; before = t[:s].rstrip(' '); after = t[e:].lstrip(' ')
    if f and before and f[0] in '([‘“' and before[-1] == f[0]: f = f[1:]
    if f and after and f[-1] in ')].,;:’”|' and after[0] == f[-1]: f = f[:-1]
    ls = t.rfind('\n', 0, s) + 1; le = t.find('\n', e); line = t[ls:le if le >= 0 else len(t)]
    if '॥' in line: f = f.replace('||', '॥')
    ch[p].append((s, e, esc(f), g))
# the brackets of pf679's fills
old = json.load(open('gaps-spec.json')); dec = json.load(open('gaps-decisions.json'))
nb = 0
for ed in old:
    gs = [g for g in ed['id'].split('+') if re.search(r'[\[\]]', dec[g]['fill'])]
    if not gs: continue
    t = N1[ed['path']]; q = t.find(ed['new'])
    if q < 0 or t.count(ed['new']) != 1: print('not found once', ed['id']); continue
    seg = ed['new']
    for g in gs:
        f = dec[g]['fill']
        for m in re.finditer(r'(?<!\\)[\[\]]', seg):
            pass
        # every unescaped bracket in this edit's new text that is not in the old text's escaped form is from a fill
    for m in re.finditer(r'(?<!\\)[\[\]]', seg):
        k = q + m.start()
        if t[k - 1:k] == '\\' or re.match(r'\[\^|\[\[|\]\]', t[k:k + 2]) or t[k - 1:k + 1] == ']]' or re.match(r'\[\^\d+\]', t[max(0, k - 6):k + 1]): continue
        if re.search(r'\[\^\d*$', t[max(0, k - 6):k + 1]) or re.match(r'\]', t[k:k + 1]) and re.search(r'\[\^\d+$', t[max(0, k - 8):k]): continue
        ch[ed['path']].append((k, k + 1, '\\' + t[k], 'esc:' + ed['id'])); nb += 1
print('bracket escapes', nb)
E = []
for p, L in ch.items():
    t = N1[p]; L.sort()
    for i in range(1, len(L)): assert L[i][0] >= L[i - 1][1], (p, L[i - 1], L[i])
    cl = []
    for c in L:
        if cl and c[0] - cl[-1][-1][1] < 80: cl[-1].append(c)
        else: cl.append([c])
    for c in cl:
        S, Ee = c[0][0], c[-1][1]; k = 40
        while True:
            a0, b1 = max(0, S - k), min(len(t), Ee + k); o = t[a0:b1]
            if t.count(o) == 1 or k > 600: break
            k += 40
        new = t[a0:S]
        for i, (s, e, f, g) in enumerate(c): new += f + (t[e:c[i + 1][0]] if i + 1 < len(c) else t[e:b1])
        assert t.count(o) == 1
        E.append({'id': '+'.join(x[3] for x in c), 'path': p, 'old': o, 'new': new})
json.dump(E, open('tb/gaps3-spec.json', 'w'), ensure_ascii=False, indent=0)
json.dump({g: {'fill': v['fill'], 'kind': v['kind'], 'path': pos[g][0]} for g, v in R.items()}, open('tb/gaps3-decisions.json', 'w'), ensure_ascii=False, indent=0)
T = {p: N1[p] for p in ch}
for ed in E: assert T[ed['path']].count(ed['old']) == 1; T[ed['path']] = T[ed['path']].replace(ed['old'], ed['new'])
PH = r'\\\[illegible\\\]'
print(len(E), 'edits in', len(ch), 'notes;', collections.Counter(v['kind'] for v in R.values()),
      '; placeholders in these notes', sum(len(re.findall(PH, N1[p])) for p in ch), '->', sum(len(re.findall(PH, T[p])) for p in ch))
