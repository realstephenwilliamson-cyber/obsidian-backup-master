# C-01(b) planner v2 (28 Oct 2026). For each page block K whose footnote zone holds footnotes called on page K+1:
# the run starts at the first such footnote number, extended back over the pieces (a print-page number, an unnumbered text,
# trailing words) that the next PDF page has and this page lacks; it ends at the end of block K. Checked against both PDF pages.
import json, re, sys, unicodedata
D = json.load(open(sys.argv[1])); PT = json.load(open(sys.argv[2]))['text']; C = json.load(open('cands.json'))
PG = re.compile(r'^\*\[p\. [^\]]+\]\* \^pg(\d+)\s*$')
def pdf(p): return re.search(r'^source_pdf: "?([^"\n]+)"?$', D[p], re.M).group(1)
def vis(s): s = re.sub(r'\[\[([^\]|]*)\|([^\]]*)\]\]', r'\2', s); s = re.sub(r'\[\[([^\]]*)\]\]', r'\1', s); return s.replace('\\', '').replace('*', '')
def norm(s): return ''.join(ch for ch in unicodedata.normalize('NFD', s).lower() if ch.isalnum() and not unicodedata.combining(ch))
def pnorm(t): return norm(re.sub(r'-\n', '', t))
def blocks_of(path):
    L = D[path].split('\n'); out = {}; cur = None
    for i, s in enumerate(L):
        m = PG.match(s)
        if m:
            if cur: out[cur[0]] = (cur[1], i)
            cur = (int(m.group(1)), i)
    if cur: out[cur[0]] = (cur[1], len(L))
    return L, out
plans, flags = [], []
for c in C:
    p, K, p2, K2 = c['path'], c['K'], c['nextpath'], c['nextK']
    L, B = blocks_of(p); a, e = B[K]
    while e - 1 > a and not L[e - 1].strip(): e -= 1
    seg = '\n'.join(L[a + 1:e])
    hits = sorted({n for _, h in c['hits'] for n in h})
    nK, nK2 = pnorm(PT[pdf(p)][str(K)]), pnorm(PT[pdf(p2)][str(K2)])
    # position of the first hit number as a standalone token in the zone part of the block
    zstart = min(m.start() for m in re.finditer(r'(?m)^(\d{1,4} |\[\^\d+\]:)', seg)) if re.search(r'(?m)^(\d{1,4} |\[\^\d+\]:)', seg) else 0
    pos = [m.start() for h in hits[:1] for m in re.finditer(r'(?<![\d.\w^#-])%d(?![\d\]|])' % h, seg) if m.start() >= zstart]
    why = []
    if not pos: why.append('first number not found'); flags.append({**c, 'why': why}); continue
    s0 = pos[0]
    # walk back over words
    cut = s0; back = seg[zstart:s0]
    words = list(re.finditer(r'\S+', back))
    for w in reversed(words):
        t = w.group(0); nt = norm(vis(t))
        if not nt: cut = zstart + w.start(); continue  # pure punctuation
        if re.fullmatch(r'\d{1,4}', nt):  # a bare number: print page (never a footnote number of page K)
            if re.search(r'(?m)(^|\D)%s\D' % nt, PT[pdf(p2)][str(K2)]) and not re.search(r'(?m)^%s ' % nt, PT[pdf(p)][str(K)]): cut = zstart + w.start(); continue
            break
        if len(nt) >= 3 and nt in nK2 and nt not in nK: cut = zstart + w.start(); continue
        break
    run = seg[cut:].strip(); rn = norm(vis(run))
    # checks: every word of 5+ letters of the run is on page K2; the run's footnote numbers are not footnotes of page K
    ws = [norm(x) for x in re.findall(r'[^\W\d_]{5,}', vis(run))]
    miss = [w for w in ws if w not in nK2]
    if ws and len(miss) > max(1, len(ws) // 20): why.append(f'{len(miss)}/{len(ws)} words not on next page')
    nums = [int(x) for x in re.findall(r'(?<![\d.])\b(\d{2,4})\b', vis(run))]
    onK = [n for n in nums if re.search(r'(?m)^%d ' % n, PT[pdf(p)][str(K)])]
    if onK: why.append(f'numbers that are footnotes of page K: {onK[:5]}')
    tail = seg[:cut].rstrip()[-40:]
    rec = {**c, 'cut': cut, 'zstart': zstart, 'run': run, 'before': tail, 'why': why, 'line_a': a, 'line_e': e}
    (flags if why else plans).append(rec)
json.dump(plans, open('plans2.json', 'w'), ensure_ascii=False, indent=1); json.dump(flags, open('flags2.json', 'w'), ensure_ascii=False, indent=1)
print('plans', len(plans), 'flags', len(flags))
from collections import Counter
print(Counter(re.sub(r'[\d/\[\], ]+', ' ', w).strip() for f in flags for w in f['why']))
