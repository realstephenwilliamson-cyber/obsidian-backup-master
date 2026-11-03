# ctx.py: the note text around each start the pre-pass did not apply (or all starts with numbers given as arguments)
import json, sys
M = json.load(open('/home/claude/lost/ch28/num/ch28-map.json'))
T = {'v10-' + i: open('/home/claude/dyfn/src/v10-%s.md' % i).read().split('\n') for i in '02 03 04 05 06 07'.split()}
want = {int(a) for a in sys.argv[1:]}
for r in M:
    if (r.get('how') == 'not applied' and not want) or r.get('n') in want:
        if not r['match']: print(r['n'], 'no match'); continue
        nid, i, c, pdf = r['match']; l = T[nid][i]; print(r['n'], nid, i + 1, c, repr(l[max(0, c - 70):c + 50]))
