# lost_plan.py (28 Oct 2026, fourth session): the CCEL footnotes whose number (or whole note) the converter dropped.
# usage: python3 lost_plan.py pdftext.json notes.json lost-numbers-pf472.json OUTDIR
# Inputs: pdftext.json (pf495: {text: {pdf: {K: text}}}), notes.json (pf495: {path: text}), the pf472 list of lost calls.
# For each lost call N: the PDF page K whose footnote list (a run of consecutive numbers at line starts) holds N, and N's text T_N
# (to the next number, the print-page line or the page end); then, in the note's page block ^pgK, compared without whitespace,
# hyphens, link markup, *, \, <sup> calls and accents (mode "base"), or also without Greek letters (mode "skel", tried second,
# because the converter dropped some accented Greek letters):
#   A   T_N is in the block right after the end of N-1's text            -> insert "N " before it
#   A1  N is the page's first footnote; T_N is in the block, right after the page's last body words, at the block's end -> "N " before it
#   B   T_N is not in the block; N-1's text ends once in the block, followed by the block's end or by N+1's text -> insert " N T_N" after it
#   B1  N is the page's only footnote, not in the block, and the block ends with the page's last body words -> new paragraph "N T_N"
# anything else is held with a reason. Output: plan.json and held.json.
import json, re, sys, collections, unicodedata
P = json.load(open(sys.argv[1]))['text']; NOTES = json.load(open(sys.argv[2])); LOST = json.load(open(sys.argv[3]))['lost']
OUT = sys.argv[4]
AUG = [k for k in P if 'Augustine' in k][0]; CHR = [k for k in P if 'Chrysostom' in k][0]
byname = {p.split('/')[-1]: p for p in NOTES}
MODE = 'base'

def entries(pdf):
    E = {}
    for K, t in P[pdf].items():
        for i, x in enumerate(t.split('\n')):
            m = re.match(r'\s*(\d{1,4})\s+(\S.*)$', x)
            if m: E.setdefault(int(m.group(1)), []).append((int(K), i))
    return E
ENT = {AUG: entries(AUG), CHR: entries(CHR)}

_PF = {}
def page_fns(pdf, K):
    """the page's footnote list: the longest run of consecutive numbers at line starts; {num: line index}; the body's last line"""
    if (pdf, K) in _PF: return _PF[(pdf, K)]
    L = P[pdf][str(K)].split('\n'); best = []; cur = []
    for i, x in enumerate(L):
        m = re.match(r'\s*(\d{1,4})\s+\S', x)
        if not m: continue
        v = int(m.group(1))
        if cur and v == cur[-1][0] + 1: cur.append((v, i))
        else: cur = [(v, i)]
        if len(cur) >= len(best): best = list(cur)
    nums = [v for v, i in best]; LIDX = dict(best)
    body = ' '.join(L[:best[0][1]]) if best else ' '.join(L)
    _PF[(pdf, K)] = (nums, LIDX, body)
    return _PF[(pdf, K)]

def fn_lines(pdf, K, i, n):
    L = P[pdf][str(K)].split('\n')
    parts = [re.match(r'\s*\d{1,4}\s+(\S.*)$', L[i]).group(1)]
    for x in L[i + 1:]:
        if re.fullmatch(r'\s*\d{1,4}\s*', x) or not x.strip(): break
        m = re.match(r'\s*(\d{1,4})\s+\S', x)
        if m and n < int(m.group(1)) <= n + 4: break
        parts.append(x.strip())
    return parts

def keyc(c):
    """compare key of one character: accents dropped; in mode skel, Greek letters dropped too"""
    b = ''.join(x for x in unicodedata.normalize('NFD', c) if not unicodedata.combining(x))
    if MODE == 'skel': b = ''.join(x for x in b if not ('Ͱ' <= x <= 'Ͽ' or 'ἀ' <= x <= '῿'))
    return b

def plain(t, a=0, b=None):
    b = len(t) if b is None else b
    ch, idx, ib = [], [], []
    i = a; mstart = None
    while i < b:
        if t.startswith('<sup>', i):
            i = t.find('</sup>', i) + 6; mstart = None; continue
        if t.startswith('[[', i):
            j = t.find(']]', i); k = t.find('|', i, j)
            if mstart is None: mstart = i
            i = (k + 1) if k >= 0 else i + 2; continue
        if t.startswith(']]', i): i += 2; continue
        c = t[i]
        if c in '*\\':
            if mstart is None: mstart = i
            i += 1; continue
        if c.isspace() or c in '-‐':
            if c.isspace(): mstart = None
            i += 1; continue
        k = keyc(c)
        if not k:
            if mstart is None: mstart = i
            i += 1; continue
        for x in k: ch.append(x); idx.append(i); ib.append(mstart if mstart is not None else i)
        mstart = None; i += 1
    return ''.join(ch), idx, ib

def norm(s): return plain(s)[0]
def nodig(s): return re.sub(r'\d', '', s)

def after_end(t, e):
    while True:
        if t.startswith(']]', e): e += 2
        elif t.startswith('*', e): e += 1
        else: return e

def join_text(parts):
    s = parts[0]; flags = []
    for x in parts[1:]:
        if s.endswith('-') and x[:1].islower(): flags.append(s.split()[-1] + x.split()[0]); s = s + x   # keep the hyphen; flagged
        else: s = s + ' ' + x
    return s.strip(), flags

def fn_text(pdf, K, j):
    nums, LIDX, body = page_fns(pdf, K)
    return join_text(fn_lines(pdf, K, LIDX[j], j))[0] if j in LIDX else None

def page_of(pdf, n):
    ks = sorted({K for K, i in ENT[pdf].get(n, []) if n in page_fns(pdf, K)[1]})
    return ks

def block_span(t, K):
    m = re.search(r'^\*\[[^\]]+\]\* \^pg%d\s*$' % K, t, re.M)
    if not m: return None
    a = m.end(); m2 = re.search(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', t[a:], re.M); b = a + m2.start() if m2 else len(t)
    return m.start(), a, b

def attempt(t, pdf, K, n, T):
    s0, a, b = block_span(t, K)
    BP, BI, BB = plain(t, a, b)
    nT = norm(T)
    if len(nT) < (3 if MODE == 'base' else 6): return None, 'text too short in this mode'
    nums, LIDX, body = page_fns(pdf, K)
    pt = fn_text(pdf, K, n - 1) if (n - 1) in LIDX else None
    nt = fn_text(pdf, K, n + 1) if (n + 1) in LIDX else None
    prevT = norm(pt) if pt else None; nextT = norm(nt) if nt else None
    if prevT is not None and len(prevT) < 3: prevT = None
    btail = nodig(norm(body))[-18:]
    occ = [o.start() for o in re.finditer(re.escape(nT), BP)]
    if prevT:
        ptail = prevT[-24:]
        good = [o for o in occ if BP[:o].endswith(ptail)]
        if len(good) == 1: return {'cls': 'A', 'pos': BB[good[0]]}, None
    elif nums and nums[0] == n and btail:
        good = [o for o in occ if nodig(BP[:o]).endswith(btail) and (BP[o + len(nT):] == '' or (nextT and BP[o + len(nT):].startswith(str(n + 1) + nextT[:10])))]
        if len(good) == 1: return {'cls': 'A1', 'pos': BB[good[0]]}, None
    if prevT:
        ptail = prevT[-24:]
        cands = []
        for mm in re.finditer(re.escape(ptail), BP):
            e = mm.end(); rest = BP[e:]
            if rest == '' or (nextT and rest.startswith(str(n + 1) + nextT[:10])) or re.match(r'\d+$', rest): cands.append(e)
        if len(cands) == 1 and not any(BP[:o].endswith(ptail) for o in occ):
            return {'cls': 'B', 'pos': after_end(t, BI[cands[0] - 1] + 1)}, None
        return None, f'N-1 end found {len(cands)}x with the right follower; text found {len(occ)}x'
    if nums == [n] and not occ and btail and nodig(BP).endswith(btail):
        return {'cls': 'B1', 'pos': after_end(t, BI[-1] + 1)}, None
    return None, f'first on page; nums {nums[:4]}; text found {len(occ)}x; block ends with body: {bool(btail) and nodig(BP).endswith(btail)}'

# === MAIN ===
if __name__ == '__main__':
    plan, held = [], []
    cnt = collections.Counter()
    for name, n in LOST:
        path = byname[name]; t = NOTES[path]; pdf = AUG if 'Augustine' in name else CHR
        rec = {'path': path, 'N': n}
        ks = page_of(pdf, n)
        if len(ks) != 1:
            rec['why'] = f'{len(ks)} PDF pages list {n} in their footnote run'; held.append(rec); cnt['H pdf-pages'] += 1; continue
        K = ks[0]; rec['K'] = K
        T = fn_text(pdf, K, n); rec.update(T=T, hy=join_text(fn_lines(pdf, K, page_fns(pdf, K)[1][n], n))[1])
        if not block_span(t, K):
            rec['why'] = 'page block not in this note'; held.append(rec); cnt['H no block'] += 1; continue
        why = []
        for MODE in ('base', 'skel'):
            r, w = attempt(t, pdf, K, n, T)
            if r: rec.update(r); rec['mode'] = MODE; plan.append(rec); cnt[r['cls'] + ('' if MODE == 'base' else ' (skel)')] += 1; break
            why.append(f'{MODE}: {w}')
        else:
            rec['why'] = ' | '.join(why); held.append(rec); cnt['H'] += 1
        MODE = 'base'
    json.dump(plan, open(OUT + '/plan.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(held, open(OUT + '/held.json', 'w'), ensure_ascii=False, indent=0)
    print(dict(cnt), 'plan', len(plan), 'held', len(held), 'hyphen joins in inserted text', sum(1 for r in plan if r['cls'].startswith('B') and r.get('hy')))
