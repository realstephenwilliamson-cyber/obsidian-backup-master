# mkpackets.py (2 Nov 2026, ch05): builds the reader folders /home/claude/dyfn/rd/ID-x for Chapter Five with packet_ch05.py
# and writes TASK.txt in each from reader-task-ch05.txt. Prints the packet list.
import json, subprocess, os
H = '/home/claude/dyfn'; C = '/home/claude/lost/ch05'
PDF = '/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. 04.pdf'
TITLES = {'v04-03': 'Tantraloka Dyczkowski v04 03 - Chapter Five, part 1', 'v04-04': 'Tantraloka Dyczkowski v04 04 - Chapter Five, part 2',
          'v04-05': 'Tantraloka Dyczkowski v04 05 - Chapter Five, part 3', 'v04-06': 'Tantraloka Dyczkowski v04 06 - Chapter Five, part 4',
          'v04-07': 'Tantraloka Dyczkowski v04 07 - Chapter Five, part 5'}
RNG = {'v04-03': [(16, 29), (30, 43), (44, 57)], 'v04-04': [(58, 71), (72, 85), (86, 99)], 'v04-05': [(100, 113), (114, 127), (128, 141)],
       'v04-06': [(142, 155), (156, 169), (170, 183)], 'v04-07': [(184, 197), (198, 211), (212, 224)]}
EXTRA = {('v04-04', 58): ' Footnotes 84-86 (PDF 58) stand in a heading line the pre-pass could not touch: see the addendum, point 4.',
         ('v04-06', 142): ' Footnote 297: see the addendum, point 4 (its call is on PDF 156, in the next reader\'s range; look on PDF 151-155 for its text).',
         ('v04-06', 156): ' Footnote 297: see the addendum, point 4 (its call is on your PDF 156).',
         ('v04-07', 198): ' 391, 392 and 403 were made real earlier tonight (calls in place); check the footnotes split off from them (393-395, 404).',
         ('v04-07', 212): ' 409 was made real earlier tonight (call in place); check the footnotes split off from it (410-414). Chapter Five ends on PDF 224 (Chapter Six begins on PDF 225, in the next note).'}
R = json.load(open(C + '/num/ch05-map.json', encoding='utf-8'))
T = open(C + '/reader-task-ch05.txt', encoding='utf-8').read()
out = []
for nid, rs in RNG.items():
    pre = json.load(open(f'{H}/work/{nid}/pre.json', encoding='utf-8'))
    for x, (a, b) in zip('abc', rs):
        pid = f'{nid}-{x}'; d = f'{H}/rd/{pid}'
        subprocess.run(['python3', C + '/scripts/packet_ch05.py', nid, PDF, str(a), str(b), d], check=True)
        ns = sorted(r['n'] for r in R if r['n'] is not None and a <= r['pdf'] <= b)
        defs = sorted(dd['n'] for p in pre['pages'] if a <= p['pdf'] <= b for dd in p['defs'])
        gaps = sorted(set(range(ns[0], ns[-1] + 1)) - set(defs))
        dtxt = '%d-%d' % (defs[0], defs[-1]) + (' (none for %s)' % ', '.join(map(str, gaps)) if gaps else '')
        t = (T.replace('__ID__', pid).replace('__TITLE__', TITLES[nid]).replace('__A__', str(a)).replace('__B__', str(b))
             .replace('__PA__', str(a - 15)).replace('__PB__', str(b - 15)).replace('__DEFS__', dtxt)
             .replace('__N1__', str(ns[0])).replace('__N2__', str(ns[-1])).replace('__EXTRA__', EXTRA.get((nid, a), '')))
        open(d + '/TASK.txt', 'w', encoding='utf-8').write(t)
        out.append((pid, a, b, a - 15, b - 15, ns[0], ns[-1], len(defs), dtxt))
json.dump(out, open(C + '/packets.json', 'w'), indent=1)
for o in out: print(o)
