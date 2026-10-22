# Torzsok, Markdown side: per page, align the note's words with the PDF layer, split run-together notes,
# put each image-confirmed call where the layer has it, and turn each called note into a Markdown footnote.
# usage: python transform.py [pages]   -> writes out/<note>.md, report.json
import sys, os, re, json, glob, difflib, collections, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from pdfside import page, norm, LAY, num
from raised import Img, raised_cols
from callocr import raised_marks, marks_after, Reader
READER = Reader(); MODE = 'apply'

VAULT = r'C:\Vaults\Obsidian Vault'
FOLDER = os.path.join(VAULT, r".work\backup-footnotes-2026-10-18\Torzsok\Library\Trika\The Doctrine of Magic Female Spirits' (Torzsok)")   # the originals (the vault holds the first apply)
PDF = os.path.join(VAULT, r'Library\Trika\Torzsok - The Doctrine of Magic Female Spirits (1999).pdf')
SCOPE = set(range(1, 91)) | set(range(201, 354))      # files 01-02 and 06-09; 03-05 are the edition (apparatus only)
MARK = re.compile(r'^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$')
LABEL = re.compile(r'^[\dOolI]{1,3}$')
STD_TAIL = re.compile(r'^[.,;:]*$')
KEEPC = set('.,;:)]}\\') | set('\'’”"‘“')
def is_mark(ch):
    """a character that may be an OCR reading of a raised note number: digits and stray symbols"""
    return not ch.isalpha() and not ch.isspace() and ch not in KEEPC and ch not in '-–—/([{'
JUNKC = None
NOT_AFTER = re.compile(r'^(chapter|chapters|part|verse|verses|p|pp|no|vol|cf|ch|fig|note|notes|n|patala|paṭala)\W*$', re.I)
QUOTES = set('\'’”"‘“')

def load_md():
    files = {}
    for f in sorted(glob.glob(os.path.join(glob.escape(FOLDER), '*.md'))):
        L = open(f, encoding='utf-8').read().split('\n')
        marks = [(i, m.group(1), int(m.group(2))) for i, l in enumerate(L) for m in [MARK.match(l)] if m]
        files[os.path.basename(f)] = dict(L=L, marks=marks)
    return files

def paras_of(lines):
    """split page lines into paragraphs (blocks separated by blank lines); returns list of block texts"""
    out, cur = [], []
    for l in lines:
        if l.strip(): cur.append(l)
        elif cur: out.append('\n'.join(cur)); cur = []
    if cur: out.append('\n'.join(cur))
    return out

def toks(t):
    return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r'\S+', t)]

def split_tail(w):
    """word -> (letters part, tail) where tail is everything after the last letter (or after a closing bracket that follows it)"""
    m = re.match(r'^(.*[^\W\d_][\)\]\}]?)(.*)$', w)
    return (m.group(1), m.group(2)) if m else ('', w)

LM = {'s': '5', 'S': '5', 'l': '1', 'I': '1', 'i': '1', 't': '1', 'z': '2', 'Z': '2', 'o': '0', 'O': '0', 'b': '6', 'g': '9', 'q': '9', 'B': '8'}
MARKCLS = r'[^\w\s.,;:\'’”"‘“\-–—/(\[{)\]}\\]'
LETTER_JUNK = re.compile(r'^(.*[^\W\d_][\)\]]?)(' + MARKCLS + r'[A-Za-z0-9]{0,2}|\d[A-Za-z0-9]{0,2})([.,;:]*)$')
def lj_digits(core):
    return ''.join(LM.get(ch, ch) for ch in core if ch.isdigit() or ch in LM)

def candidate(word, prevword, rowfirst):
    """Is this layer word a possible call position? returns (letters_len, call_len, trail_len, digits) or None"""
    m = LETTER_JUNK.match(word)
    if m and any(ch.isalpha() for ch in m.group(2)) and all(ch in LM for ch in m.group(2) if ch.isalpha()):
        return (len(m.group(1)), len(m.group(2)), len(m.group(3)), re.sub(r'\D', '', lj_digits(m.group(2))))
    if re.fullmatch(r'\d{1,3}[.,;:]*', word):
        if rowfirst or prevword is None: return None
        d = re.match(r'\d+', word).group(0); return (0, len(d), len(word) - len(d), d)
    let, tail = split_tail(word)
    if not let:
        m = re.match(r'^(.*[\)\]])([^\)\]]+)$', word)          # '[...]3.'
        if not m: return None
        let, tail = m.group(1), m.group(2)
    if not tail:
        # a closing bracket glued to the letters may hide the call (')2' read as '}'): test from the bracket on
        if let[-1] in ')]}': return (len(let) - 1, 1, 0, '', 'bracket')
        return None
    m = re.match(r'^(.*?)([.,;:]*)$', tail); core, trail = m.group(1), m.group(2)
    if not core or any(ch.isalpha() or ch in '-–—/' for ch in core): return None
    if not any(is_mark(ch) for ch in core): return None
    return (len(let), len(core), len(trail), re.sub(r'\D', '', core))

def agrees(x, n):
    """does a read label x fit note number n? exact, first digit lost, one digit misread, or one stray digit added"""
    if x is None: return True
    s, sx = str(n), str(x)
    return (sx == s or (len(sx) < len(s) and s.endswith(sx)) or (len(sx) == len(s) and sum(a != b for a, b in zip(sx, s)) <= 1)
            or (len(sx) == len(s) + 1 and sx.startswith(s)))

def placed_fail(info, n, why):
    info.setdefault('place_fail', []).append((n, why))

def dp_assign(cands, numbers):
    """monotonic assignment of candidates (reading order) to note numbers (in order); score by digit agreement"""
    def sc(c, n):
        d, s = c['digits'], str(n)
        return 3 if d == s else 0        # strict (after the image check of 18 Oct): a call needs its digits read exactly
    C, N = len(cands), len(numbers)
    best = [[0.0] * (N + 1) for _ in range(C + 1)]; ch = [[None] * (N + 1) for _ in range(C + 1)]
    for i in range(C - 1, -1, -1):
        for j in range(N - 1, -1, -1):
            opts = [(best[i + 1][j], 'skipc'), (best[i][j + 1] - 0.01, 'skipn')]
            s = sc(cands[i], numbers[j])
            if s >= 1: opts.append((best[i + 1][j + 1] + s, 'take'))
            best[i][j], ch[i][j] = max(opts)
        ch[i][N] = 'skipc'
    i = j = 0; out = {}
    while i < C and j < N:
        c = ch[i][j]
        if c == 'take': out[numbers[j]] = cands[i]; i += 1; j += 1
        elif c == 'skipc': i += 1
        else: j += 1
    return out

def run(pages_only=None):
    files = load_md(); doc = pymupdf.open(PDF)
    report = dict(pages={}, totals=collections.Counter())
    prev_last = None
    newfiles = {}
    for fname, F in files.items():
        L, marks = F['L'], F['marks']
        if not marks: continue
        out = L[:marks[0][0]]
        used = set(re.findall(r'\[\^([^\]]+)\]', '\n'.join(L)))
        last_def = None          # (index in out, note number) of the last definition written in this file
        for mi, (li, plabel, K) in enumerate(marks):
            le = marks[mi + 1][0] if mi + 1 < len(marks) else len(L)
            sec = L[li:le]
            res = None
            if K in SCOPE and (pages_only is None or K in pages_only) and not any('[^' in x for x in sec):
                res, prev_last = do_page(K, sec, doc, prev_last, used, plabel)
            elif K in SCOPE:
                p = page(K - 1)
                if p and p['notes']:   # keep the numbering running over pages left alone
                    st_ = [n for n in p['notes'] if n['start']]
                    if st_: prev_last = (prev_last or 0) + len(st_)
            if not res or not res.get('new'):
                if res: report['pages'][K] = res['info']
                out += sec; last_def = None; continue
            info = res['info']; report['pages'][K] = info
            for k, v in info.items():
                if isinstance(v, int): report['totals'][k] += v
            # continuation of the previous page's last note
            if res['cont'] and last_def is not None and res['cont_num'] == last_def[1]:
                out[last_def[0]] = out[last_def[0]].rstrip() + ' ' + res['cont']
                info['continuation_appended'] = 1; report['totals']['continuation_appended'] += 1
            elif res['cont']:
                for k_, para_ in enumerate(res['cont_paras']):        # kept as it was written: its own paragraphs
                    res['new'][res['body_end'] + 2 * k_:res['body_end'] + 2 * k_] = [para_, '']
                info['continuation_kept'] = 1; report['totals']['continuation_kept'] += 1
            base = len(out)
            out += res['new']
            if res['last_def_idx'] is not None: last_def = (base + res['last_def_idx'], res['last_def_num'])
            elif res['info'].get('notes', 0): last_def = None
        txt = '\n'.join(out)
        if txt != '\n'.join(L):
            SUF = '; footnotes restored from the PDF text layer and page images 18 Oct 2026'
            txt = re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1) + (m.group(2)[:-1] + SUF + '"' if m.group(2).endswith('"') else m.group(2) + SUF), txt, count=1, flags=re.M)
            newfiles[fname] = txt
    return files, newfiles, report

def do_page(K, sec, doc, prev_last, used, plabel):
    p = page(K - 1)
    info = dict(K=K)
    if not p or not p['notes']: return dict(info=info), prev_last
    starts = [j for j, n in enumerate(p['notes']) if n['start']]
    # note numbers: label when it fits the running sequence, else the next number
    # the page's first number: the base with which most read labels agree (+ small bonuses: continuing, restarting)
    labs_ = [(r, num(p['notes'][j]['label'])) for r, j in enumerate(starts) if num(p['notes'][j]['label']) is not None]
    cand_bases = {1} | ({prev_last + 1} if prev_last is not None else set()) | {x - r for r, x in labs_ if x - r >= 1}
    def bscore(b):
        return sum(agrees(x, b + r) for r, x in labs_) + (0.6 if prev_last is not None and b == prev_last + 1 else 0) + (0.3 if b == 1 else 0) \
               + 0.01 * sum(x == b + r for r, x in labs_)
    base = max(sorted(cand_bases), key=bscore) if starts else 1
    numbers = {j: base + r for r, j in enumerate(starts)}
    info['label_agree'] = sum(1 for r, j in enumerate(starts) if num(p['notes'][j]['label']) == base + r)
    info['labels_read'] = sum(1 for j in starts if num(p['notes'][j]['label']) is not None)
    prev = base + len(starts) - 1
    new_last = prev if starts else prev_last
    info.update(notes=len(starts))
    # ---- align the md words with the layer's (body, then notes)
    marker = sec[0]
    paras = paras_of(sec[1:])
    mt = []
    for pi, t in enumerate(paras):
        for (a, b, w) in toks(t):
            n = norm(w)
            if n: mt.append((pi, a, b, w, n))
    pt = [('B', k, x['n']) for k, x in enumerate(p['body']) if x['n']]
    pidx = [k for k, x in enumerate(p['body']) if x['n']]       # pt index -> body token index
    for j, nn in enumerate(p['notes']):
        pt += [('N', j, w) for w in nn['n']]
    sm = difflib.SequenceMatcher(None, [x[2] for x in pt], [x[4] for x in mt], autojunk=False)
    amap = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for d in range(i2 - i1): amap[i1 + d] = j1 + d
    info['align'] = round(len(amap) / max(1, len(pt)), 3)
    body_tok_to_pt = {bk: i for i, bk in enumerate(pidx)}
    # ---- calls: candidates from the layer word or the aligned md word, confirmed by raised ink
    img = Img(doc, K - 1)
    from pdfside import rows
    R = rows(K - 1)
    bw = []
    for j, r in enumerate(R[:p['zone']]):
        for q, w in enumerate(r['w']):
            for t in w['t'].split():
                bw.append(dict(t=t, w=w, rowfirst=(q == 0 and t == w['t'].split()[0])))
    assert len(bw) == len(p['body'])
    cands = []
    for k, b in enumerate(bw):
        c = candidate(b['t'], bw[k - 1]['t'] if k else None, b['rowfirst'])
        i_ = body_tok_to_pt.get(k)
        mdw = mt[amap[i_]][3] if i_ is not None and i_ in amap else None
        c2 = candidate(mdw, None, True) if mdw else None
        if c2 and (not c or (not c[3] and c2[3])): c = c2         # the md reading has the mark (or its digits)
        if not c: continue
        if len(b['w']['t'].split()) > 1: continue        # multi-token span: positions unreliable
        lone = c[0] == 0
        if lone and (k == 0 or NOT_AFTER.match(bw[k - 1]['t'])): continue
        ok, frac, hr = raised_cols(img, b['w'], c[0], c[1], c[2], bw[k - 1]['w'] if lone else None)
        if lone and frac < 0.6: ok = False                    # a lone number must be wholly raised
        if len(c) > 4 and frac < 0.45: ok = False             # call hidden behind a bracket: stricter
        if ok: cands.append(dict(tok=k, nlet=c[0], raw=b['t'], digits=c[3], ncall=c[1], ntrail=c[2], frac=frac, lone=lone,
                                 bracket=len(c) > 4, follow=not norm(b['t'][:c[0]]) if c[0] else True))
        info.setdefault('cand_log', []).append((b['t'], ok, frac, hr))
    # ---- where the notes begin in the md: the first md word aligned to a note word (walking back over its label)
    tokcls = {}
    for i, j in amap.items():
        tokcls[j] = 'B' if pt[i][0] == 'B' else ('N', pt[i][1])
    firstNtok = next((k for k in range(len(mt)) if isinstance(tokcls.get(k), tuple)), None)
    if firstNtok is None: return dict(info=dict(info, skip='notes not found in md')), new_last
    pcut = mt[firstNtok][0]
    allt = toks(paras[pcut]); wi = [q for q, a in enumerate(allt) if a[0] == mt[firstNtok][1]][0]
    while wi > 0 and LABEL.match(allt[wi - 1][2]): wi -= 1
    ocut = allt[wi][0]
    body_paras = paras[:pcut] + ([paras[pcut][:ocut].rstrip()] if paras[pcut][:ocut].strip() else [])
    NP = [paras[pcut][ocut:]] + paras[pcut + 1:]
    # an md paragraph inside the notes with no word aligned at all may be body text out of place: leave the page
    for qi in range(len(NP)):
        pi_ = pcut + qi
        ks = [k for k in range(len(mt)) if mt[k][0] == pi_ and (pi_ > pcut or mt[k][1] >= ocut)]
        if len(ks) >= 5 and not any(isinstance(tokcls.get(k), tuple) for k in ks):
            return dict(info=dict(info, skip='unaligned paragraph among the notes')), new_last
    NT = [(qi, a, b, w) for qi, t in enumerate(NP) for (a, b, w) in toks(t)]
    pos2nt = {(qi, a): t for t, (qi, a, b, w) in enumerate(NT)}
    def md2nt(k):
        pi_, s_ = mt[k][0], mt[k][1]
        if pi_ < pcut or (pi_ == pcut and s_ < ocut): return None
        return pos2nt.get((pi_ - pcut, s_ - (ocut if pi_ == pcut else 0)))
    nt_cls = {}
    for k, c in tokcls.items():
        t = md2nt(k)
        if t is not None and isinstance(c, tuple): nt_cls[t] = c[1]
    # ---- note labels: numbers at a paragraph start or after a sentence end, followed by a capital or an opening mark;
    # and the labels the layer reads at the start of a note row (placed before the md word aligned to the note's first word)
    labc = {}
    LOOK = {'I': '1', 'l': '1', '|': '1', '!': '1', 'O': '0'}
    for t, (qi, a, b, w) in enumerate(NT):
        mg = re.fullmatch(r'(\d{1,3})([A-Z][a-z]\S*)', w)       # a label glued to the note's first word: '31Described'
        if mg and (a == 0 or (t > 0 and NT[t - 1][0] == qi and re.search(r'[.)\]’\'"”!?;]$', NT[t - 1][3]))):
            labc[t] = dict(n=int(mg.group(1)), src='md glued'); continue
        if not re.fullmatch(r'[\dIl|!O]{1,3}', w): continue
        if not (re.search(r'\d', w) or (len(w) >= 2 and set(w) <= set('Il|!'))): continue   # never the pronoun 'I'
        w = ''.join(LOOK.get(ch, ch) for ch in w)
        first_in_para = a == 0
        prev_ok = first_in_para or (t > 0 and NT[t - 1][0] == qi and re.search(r'[.)\]’\'"”!?;]$', NT[t - 1][3]))
        nxt = NT[t + 1][3] if t + 1 < len(NT) else ''
        if prev_ok and nxt and (nxt[0].isupper() or nxt[0] in '‘\'"“([*') and not re.match(r'\d', nxt):
            labc[t] = dict(n=int(w), src='md')
    for j, nn in enumerate(p['notes']):
        L_ = p['notes'][j]['label']
        if not (nn['start'] and L_ and re.fullmatch(r'\d{1,3}', L_)): continue
        i0 = next((i for i, x in enumerate(pt) if x[0] == 'N' and x[1] == j), None)
        if i0 is None or i0 not in amap: continue
        t1 = md2nt(amap[i0])
        if t1 is None: continue
        if t1 > 0 and (t1 - 1) in labc and NT[t1 - 1][0] == NT[t1][0]:
            if labc[t1 - 1]['n'] != int(L_): labc[t1 - 1]['conflict'] = True
            else: labc[t1 - 1]['src'] = 'md+layer'
        elif t1 not in labc and NT[t1][1] == 0:
            # a label only the layer read marks a boundary only where the md has a paragraph break too
            labc[t1] = dict(n=int(L_), src='layer', virtual=True)
    lc = sorted((t, v) for t, v in labc.items() if not v.get('conflict'))
    # longest chain of labels with increasing numbers in reading order (consecutive numbers preferred)
    best = []; back = []
    for i, (t, v) in enumerate(lc):
        b_, k_ = 1.0, None
        for k, (t2, v2) in enumerate(lc[:i]):
            if v2['n'] < v['n']:
                s_ = best[k] + 1 + (0.5 if v2['n'] == v['n'] - 1 else 0)
                if s_ > b_: b_, k_ = s_, k
        best.append(b_); back.append(k_)
    chain = []
    if lc:
        i = max(range(len(lc)), key=lambda i: (best[i], -i))
        while i is not None: chain.append(lc[i]); i = back[i]
        chain.reverse()
    if not chain: return dict(info=dict(info, unchanged='no note number read'), new=None), new_last
    chain_nums = [v['n'] for t, v in chain]
    # every number this page can have (labels unread included), so that a call is never forced onto a neighbour
    nums_in_order = list(range(chain_nums[0], chain_nums[-1] + 2))
    new_last = chain_nums[-1]
    info['chain'] = chain_nums
    # which chain notes have both ends confirmed
    def pdf_note_after(t):
        return next((nt_cls[u] for u in range(t, len(NT)) if u in nt_cls), None)
    last_start = max((j for j, n in enumerate(p['notes']) if n['start']), default=-1)
    accepted = set()
    for i, (t, v) in enumerate(chain):
        if i + 1 < len(chain):
            if chain[i + 1][1]['n'] == v['n'] + 1: accepted.add(v['n'])
        else:
            later = [u for u in labc if u > t]
            jn = pdf_note_after(t + (0 if v.get('virtual') else 1))
            if not later and jn is not None and jn >= last_start: accepted.add(v['n'])
    info['notes'] = len(chain); info['accepted_boundaries'] = len(accepted)
    # segments of the notes text: before the first label, then label to label
    cuts = [(NT[t][0], NT[t][1]) for t, v in chain]
    def slice_text(a, b):
        """text of NP from position a=(qi,off) to b (exclusive) as a list of paragraph pieces"""
        out = []
        for qi in range(a[0], (b[0] if b else len(NP) - 1) + 1):
            s_ = a[1] if qi == a[0] else 0
            e_ = b[1] if b and qi == b[0] else len(NP[qi])
            piece = NP[qi][s_:e_].strip()
            if piece: out.append(piece)
        return out
    pre = slice_text((0, 0), cuts[0])
    segs = [slice_text(cuts[i], cuts[i + 1] if i + 1 < len(cuts) else None) for i in range(len(cuts))]
    # ---- read call digits by shape where the OCR did not read them
    for c in cands:
        b = bw[c['tok']]
        rm = raised_marks(img, b['w'], max(c['nlet'], 0), c['ncall'], c['ntrail'], bw[c['tok'] - 1]['w'] if c['lone'] else None)
        if not rm: continue
        grids = rm[0]
        if MODE == 'learn':
            if c['digits'] and int(c['digits']) in nums_in_order: READER.learn(grids, c['digits'])
            continue
        if not c['digits'] or int(c['digits']) not in nums_in_order:
            v_ = READER.verify(grids, nums_in_order)
            info.setdefault('ocr_log', []).append((b['t'],) + (tuple(round(x, 3) for x in v_) if v_ else ()))
            if v_ and v_[1] <= 0.22 and v_[2] >= 0.06: c['digits'] = str(v_[0]); c['ocr'] = True
    if MODE == 'learn': return dict(info=info), new_last
    # calls neither OCR read: raised digit-sized marks after a word, read by shape, equal to a note number here
    have = {c['tok'] for c in cands} | {c['tok'] - 1 for c in cands if c['lone']}
    found_n = {int(c['digits']) for c in cands if c['digits'] and c['digits'].isdigit()}
    for k, b in enumerate(bw):
        if k in have or not p['body'][k]['n'] or len(b['w']['t'].split()) > 1: continue
        if NOT_AFTER.match(b['t']): continue
        nxt = bw[k + 1]['w'] if k + 1 < len(bw) and bw[k + 1]['w'] is not b['w'] else None
        rm = marks_after(img, b['w'], nxt)
        if not rm: continue
        v_ = READER.verify(rm[0], [x for x in nums_in_order if x not in found_n])
        if not v_ or len(rm[0]) != len(str(v_[0])): continue
        d, worst, margin = str(v_[0]), v_[1], v_[2]
        if worst <= 0.2 and margin >= 0.08:
            m_ = re.search(r'[^\W\d_](?=[^\w]*$)', b['t'])
            cands.append(dict(tok=k, nlet=m_.end(), raw=b['t'], digits=d, ncall=0, ntrail=len(b['t']) - m_.end(), frac=1, lone=False,
                              bracket=False, follow=False, ocr=True, image_only=True))
            info.setdefault('image_only', []).append((b['t'], d, round(margin, 3), round(worst, 3)))
    cands.sort(key=lambda c: c['tok'])
    amap_calls = dp_assign(cands, nums_in_order)            # exact digits only
    # a number read twice in the body (two candidates with the same digits) is ambiguous: drop it
    dup = collections.Counter(c['digits'] for c in cands if c['digits'])
    amap_calls = {n: c for n, c in amap_calls.items() if n in accepted and dup[str(n)] == 1}
    info.update(cands=len(cands), calls=len(amap_calls))
    # ---- place the calls in the body
    bodyp = list(body_paras)
    edits = collections.defaultdict(list)
    placed = {}
    KEEP = set('.,;:)]}\\') | QUOTES
    for n, c in amap_calls.items():
        follow = c['follow']        # the call token has no letters ('7', '[...]3.'): anchor on the previous word
        k0 = c['tok'] - 1 if follow else c['tok']
        while follow and k0 >= 0 and not p['body'][k0]['n']: k0 -= 1
        i = body_tok_to_pt.get(k0)
        if i is None or i not in amap: placed_fail(info, n, 'not aligned'); continue
        pi, s, e, w, nw = mt[amap[i]]
        if pi >= len(bodyp) or e > len(bodyp[pi]): placed_fail(info, n, 'not in body'); continue
        ptxt = bodyp[pi]; s2, e2 = s, e
        if follow:
            m3 = re.match(r'(\s+)(\S*?[\)\]]|)([^\s\w.,;:)\]}\\\'’”"‘“\-–—/(\[{]{1,3}|\d{1,3})([.,;:]*)(?=\s|$)', ptxt[e2:])
            if not m3 or (m3.group(2) == '' and m3.group(3) != c['digits']):
                placed_fail(info, n, 'lone token not found in md'); continue
            if m3.group(2):
                repl = ptxt[e2:e2 + m3.end()].replace(m3.group(2) + m3.group(3) + m3.group(4), m3.group(2) + '[^@%d]' % n + m3.group(4), 1)
                edits[pi].append((e2, e2 + m3.end(), repl)); placed[n] = 'after bracket'
            else:
                edits[pi].append((e2, e2 + m3.end(), '[^@%d]' % n + m3.group(4))); placed[n] = 'lone number'
            continue
        mlj = LETTER_JUNK.match(w)
        if mlj and any(ch.isalpha() for ch in mlj.group(2)):
            core, sn = mlj.group(2), str(n)
            ok_ = len(core) <= len(sn) + 1 and all(
                (not ch.isalpha()) or (k_ < len(sn) and LM.get(ch) == sn[-1 - k_]) for k_, ch in enumerate(reversed(core)))
            if not ok_: placed_fail(info, n, 'letters in mark ' + core); continue
            edits[pi].append((s2, e2, mlj.group(1) + '[^@%d]' % n + mlj.group(3))); placed[n] = 'glued (letters read for digits: %s)' % core
            info.setdefault('letters_removed', []).append((n, w)); continue
        let, tail = split_tail(w)
        if c['bracket']:
            if tail and not re.fullmatch(r'[.,;:]+', tail): placed_fail(info, n, 'bracket word differs in md'); continue
            edits[pi].append((s2, e2, let + '[^@%d]' % n + tail)); placed[n] = 'after bracket'; continue
        mt_ = re.match(r'^(.*?)([.,;:]*)$', tail); core, trail = mt_.group(1), mt_.group(2)
        if not let: placed_fail(info, n, 'md word has no letters'); continue
        core_u = re.sub(r'\\(?=[^\[\]\(\)])', '', core)
        if core_u.count('\\') and not re.fullmatch(r'(\\[\[\]])*[^\\]*', core_u): placed_fail(info, n, 'escape ' + core); continue
        keep = ''.join(ch for ch in core_u if ch in KEEP)
        drop = ''.join(ch for ch in core_u if ch not in KEEP)
        if any(ch.isalpha() for ch in drop): placed_fail(info, n, 'md tail ' + core); continue
        if not core.startswith(keep): placed_fail(info, n, 'mark before punctuation ' + core); continue
        edits[pi].append((s2, e2, let + keep + '[^@%d]' % n + trail)); placed[n] = 'glued' if drop else 'inserted'
    for pi, es in edits.items():
        t = bodyp[pi]
        for s2, e2, r in sorted(es, key=lambda x: -x[0]): t = t[:s2] + r + t[e2:]
        bodyp[pi] = t
    # ---- definitions (numbers read at both ends and a call placed); everything else stays as it was written
    defs = []; vis = []; lab = {}; last_def_num = None
    cont = None; cont_num = None
    lifted = [[False] * len(t) for t in NP]      # characters moved into a definition (or to the previous page)
    def mark(a, b):
        for qi in range(a[0], (b[0] if b else len(NP) - 1) + 1):
            s_ = a[1] if qi == a[0] else 0
            e_ = b[1] if b and qi == b[0] else len(NP[qi])
            for x in range(s_, e_): lifted[qi][x] = True
    if pre:
        j0 = pdf_note_after(chain[0][0])
        if p['notes'] and not p['notes'][0]['start'] and j0 is not None and all(not p['notes'][jj]['start'] for jj in range(j0)) \
                and not any(u < chain[0][0] for u in labc) and not re.match(r'\s*[\dIl|!]', pre[0]) \
                and not (ocut > 0 and paras[pcut][:ocut].strip()):          # not the tail of a paragraph begun in the body
            cont = ' '.join(x.replace('\n', ' ') for x in pre); cont_num = chain[0][1]['n'] - 1
            mark((0, 0), cuts[0])
    for i_, ((t, v), seg) in enumerate(zip(chain, segs)):
        n = v['n']
        if n in placed:
            mark(cuts[i_], cuts[i_ + 1] if i_ + 1 < len(cuts) else None)
            txt = ' '.join(x.replace('\n', ' ') for x in seg).strip()
            m = re.match(r'^(\d{1,3})(?:\s+|(?=[A-Z]))', txt)
            if m and int(m.group(1)) == n: txt = txt[m.end():]
            l_ = str(n) if str(n) not in used else '%d-p%s' % (n, re.sub(r'[^\w]', '', plabel))
            if l_ in used: l_ = '%d-pdf%d' % (n, K)          # a page printed twice (PDF 257/258 are both p. 160)
            used.add(l_); lab[n] = l_
            defs.append('[^%s]: %s' % (l_, txt)); last_def_num = n
        else:
            last_def_num = None
    # what stays visible keeps its original paragraphs: each paragraph minus the parts lifted out
    rejoin = None          # text that continues the body/notes cut paragraph (when nothing was lifted at the cut)
    for qi, t in enumerate(NP):
        if not any(lifted[qi]):
            if qi == 0 and ocut > 0 and paras[pcut][:ocut].strip(): rejoin = t; continue
            vis.append(t); continue                   # untouched paragraph: verbatim
        run = ''; first_run = True
        for x, ch in enumerate(t):
            if lifted[qi][x]:
                if run.strip():
                    if qi == 0 and first_run and ocut > 0 and paras[pcut][:ocut].strip() and not lifted[0][0]: rejoin = run.rstrip()
                    else: vis.append(run.strip())
                run = ''; first_run = False
            else: run += ch
        if run.strip(): vis.append(run.strip())
    if cont is not None and defs == [] and not vis: pass
    info.update(placed=len(placed), defs=len(defs), unreferenced=len(chain) - len(defs))
    if not defs:          # no footnote on this page: leave it exactly as it is
        return dict(info=dict(info, unchanged='no call placed'), new=None), new_last
    fix = lambda t: re.sub(r'\[\^@(\d+)\]', lambda m: '[^' + lab[int(m.group(1))] + ']', t)
    if rejoin is not None:      # the paragraph the cut ran through is written whole again
        gap = paras[pcut][len(paras[pcut][:ocut].rstrip()):ocut]
        bodyp[-1] = bodyp[-1] + gap + rejoin
    new = [marker, '']
    for t in bodyp: new += [fix(t), '']
    body_end = len(new)
    for t in vis: new += [t, '']
    for t in defs: new += [t, '']
    last_def_idx = len(new) - 2 if last_def_num is not None else None
    info['unplaced_calls'] = [n for n in chain_nums if n not in placed]
    info['placed_how'] = placed
    return dict(info=info, new=new, cont=cont, cont_paras=pre, cont_num=cont_num, body_end=body_end,
                last_def_idx=last_def_idx, last_def_num=last_def_num), new_last

if __name__ == '__main__':
    only = set(int(x) for x in sys.argv[1].split(',')) if len(sys.argv) > 1 else None
    import pickle
    TP = os.path.join(HERE, 'templates.pkl')
    if os.path.exists(TP): READER.T = pickle.load(open(TP, 'rb'))
    else:
        MODE = 'learn'; run(None); MODE = 'apply'
        pickle.dump(READER.T, open(TP, 'wb'))
    print('templates', {d: len(v) for d, v in sorted(READER.T.items())})
    files, newfiles, rep = run(only)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    for f, t in newfiles.items():
        open(os.path.join(HERE, 'out', f), 'w', encoding='utf-8', newline='\n').write(t)
    json.dump(rep, open(os.path.join(HERE, 'report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    print(dict(rep['totals']))
    sk = collections.Counter(v.get('skip') for v in rep['pages'].values() if v.get('skip'))
    print('skips', dict(sk))
