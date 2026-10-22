import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import transform as T
F, edits, rep = T.run()
pat = sys.argv[1] if len(sys.argv) > 1 else ')"'
for fn, es in edits.items():
    t = F[fn]['t']
    for e in es:
        if e[0] != 'call': continue
        old = t[e[1]:e[2]]; new = re.sub(r'\[\^[^\]]+\]', '', e[3])
        rem = collections.Counter(old) - collections.Counter(new)
        if any(c in rem for c in pat):
            print(fn[15:40], repr(old), '->', repr(e[3]), dict(rem))
