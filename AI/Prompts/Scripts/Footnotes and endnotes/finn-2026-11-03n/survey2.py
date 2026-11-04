# survey2.py: per page, (1) layer note numbers vs definition numbers, with text comparison of every definition against the
# layer note of the same number; (2) each [^X] call's preceding word against the layer's raised call of the same number.
import json, re, glob, os, sys, unicodedata, difflib
sys.path.insert(0, '.')
import pdfside
def norm(s):
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]+', ' ', s).strip()
def nw(w): return re.sub(' ', '', norm(w))
pages = {}
for f in sorted(glob.glob('md/The Kulacudamani Tantra [0-9]*.md')):
    T = open(f, encoding='utf-8').read().split('\n'); K = None
    for i, l in enumerate(T):
        m = re.match(r'^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$', l)
        if m: K = int(m.group(2)); pages[K] = dict(f=os.path.basename(f), pp=m.group(1), lines=[]); continue
        if K: pages[K]['lines'].append(l)
def labnum(s):
    m = re.fullmatch(r'(\d{1,3})[.,*»]?', (s or '').strip()); return int(m.group(1)) if m else None
def base(x): return int(re.match(r'\d+', x).group(0))
OUT = {}
for K in sorted(pages):
    pg = pages[K]; p = pdfside.page(K - 1); text = '\n'.join(pg['lines'])
    if not p: continue
    defs = {m.group(1): norm(m.group(2)) for x in pg['lines'] for m in [re.match(r'^\[\^([^\]]+)\]: ?(.*)$', x)] if m}
    lnotes = [(labnum(n['label']), n['label'], ' '.join(n['words'])) for n in p['notes'] if n['label'] is not None and n['words']]
    issues = []
    L = {}
    for num, raw, w in lnotes:
        if num is not None: L[num] = w
    # definitions vs layer notes of the same number
    for x, t in defs.items():
        b = base(x)
        if b in L:
            r = difflib.SequenceMatcher(None, L[b][:60], t[:65]).ratio()
            if r < 0.6:
                # which layer note does it match?
                best = max(((difflib.SequenceMatcher(None, w[:60], t[:65]).ratio(), num, raw) for num, raw, w in lnotes), default=(0, None, None))
                issues.append(('def-text', x, round(r, 2), 'best', best[1], best[2], round(best[0], 2)))
        else:
            best = max(((difflib.SequenceMatcher(None, w[:60], t[:65]).ratio(), num, raw) for num, raw, w in lnotes), default=(0, None, None))
            if not (best[0] >= 0.6 and best[1] is None):   # a garbled layer label matching by text is fine
                issues.append(('def-not-in-layer', x, 'best', best[1], best[2], round(best[0], 2)))
    for num, raw, w in lnotes:
        if num is not None and not any(base(x) == num for x in defs):
            issues.append(('layer-note-no-def', num, w[:40]))
    # calls: preceding word
    calls = [(m.group(1), text[:m.start()]) for m in re.finditer(r'\[\^([^\]]+)\](?!:)', text)]
    refs = {}
    for r in p['refs']:
        d = re.sub(r'\D', '', r['raw'])
        if d and r['after'] >= 0: refs.setdefault(int(d), []).append(nw(p['body'][r['after']]['raw']))
    for x, before in calls:
        b = base(x); ws = [nw(w) for w in before.split()[-3:] if nw(w)]
        mw = ws[-1] if ws else ''
        if b in refs:
            if not any(difflib.SequenceMatcher(None, mw, lw).ratio() >= 0.6 for lw in refs[b]):
                issues.append(('call-word', x, mw, refs[b]))
    if issues: OUT[K] = dict(f=pg['f'][24:26], pp=pg['pp'], issues=issues)
json.dump(OUT, open('survey2.json', 'w'), ensure_ascii=False, indent=0)
import collections
c = collections.Counter(i[0] for v in OUT.values() for i in v['issues']); print(len(OUT), c)
for k, v in OUT.items():
    for i in v['issues']:
        if i[0] != 'layer-note-no-def': print(k, v['f'], v['pp'], i)
