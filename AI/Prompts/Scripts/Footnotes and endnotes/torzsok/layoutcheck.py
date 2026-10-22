# Layout check: every output paragraph without a footnote must be an original paragraph verbatim (trailing spaces
# aside) or a piece of one. Lists the exceptions (merges or rewritten paragraphs). usage: layoutcheck.py ORIG OUT
import sys, os, glob, re
O, N = sys.argv[1], sys.argv[2]
def paras(t):
    out, cur = [], []
    for l in t.split('\n'):
        if l.strip(): cur.append(l.rstrip())
        elif cur: out.append('\n'.join(cur)); cur = []
    if cur: out.append('\n'.join(cur))
    return out
bad = 0; tot = 0
for f in sorted(glob.glob(os.path.join(glob.escape(N), '*.md'))):
    a = paras(open(os.path.join(O, os.path.basename(f)), encoding='utf-8').read())
    sa = set(a); joined = '\n\n'.join(a)
    for p in paras(open(f, encoding='utf-8').read()):
        if '[^' in p or p.startswith('text_source:') or p.startswith('---'): continue
        tot += 1
        if p in sa or p.strip() in joined: continue
        bad += 1
        print(os.path.basename(f)[:32], '|', p[:120].replace('\n', ' / '))
print('paragraphs without footnotes checked', tot, 'not found in the original:', bad)
