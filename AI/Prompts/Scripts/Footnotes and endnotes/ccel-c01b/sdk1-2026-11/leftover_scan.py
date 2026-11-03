# leftover_scan.py (SDK 1): for each case, is the text of a footnote of the page (from the PDF text) standing, without its number,
# in the last 400 characters of the block BEFORE (the 28 Oct moves left the first note's text of some pages behind)?
# usage: py leftover_scan.py NOTES.json c080-c122
import json, re, sys, unicodedata
N = json.load(open(sys.argv[1], encoding='utf-8')); idx = json.load(open('cases.json', encoding='utf-8'))
P = json.load(open('pdftext.json', encoding='utf-8'))['text']
x, y = sys.argv[2].split('-'); ids = {'c%03d' % i for i in range(int(x[1:]), int(y[1:]) + 1)}
def k(s): s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)); return re.sub(r'[\s\*]', '', s)
def fn(pdf, K, n):
    L = P[pdf][str(K)].split('\n'); out = None
    for i, l in enumerate(L):
        if re.match(r'%d\s' % n, l):
            out = [l[len(str(n)):].strip()]
            for l2 in L[i + 1:]:
                if re.match(r'\d{1,4}(\s|$)', l2): break
                out.append(l2.strip())
            return ' '.join(out)
for c in idx:
    if c['id'] not in ids: continue
    t = N[c['path']]; m = re.search(r'^\*\[[^\]]+\]\* \^pg%d\s*$' % c['K'], t, re.M)
    tail = k(t[max(0, m.start() - 400): m.start()])
    for n in c['nums']:
        T = fn(c['pdf'], c['K'], n)
        if T and len(k(T)) >= 5 and k(T) in tail and not re.search(r'%d' % n, t[max(0, m.start() - 400): m.start()]):
            print(c['id'], c['K'], n, repr(T[:60]))
