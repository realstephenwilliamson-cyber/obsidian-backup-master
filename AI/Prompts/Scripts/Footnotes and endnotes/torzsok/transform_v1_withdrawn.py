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
                res['new'].insert(res['body_end'], res['cont']); res['new'].insert(res['body_end'] + 1, '')
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
    nums_in_order = [numbers[j] for j in starts]
    # digit shapes: learn from calls whose digits were read and fit this page's notes; read the others
    for c in cands:
        b = bw[c['tok']]
        nl = c['nlet']
        rm = raised_marks(img, b['w'], max(nl, 0), c['ncall'], c['ntrail'], bw[c['tok'] - 1]['w'] if c['lone'] else None)
        if not rm: continue
        grids = rm[0]
        if MODE == 'learn':
            if c['digits'] and int(c['digits']) in nums_in_order: READER.learn(grids, c['digits'])
            continue
        if not c['digits'] or int(c['digits']) not in nums_in_order:
            d, margin, worst = READER.read(grids)
            info.setdefault('ocr_log', []).append((b['t'], d, round(margin, 3), round(worst, 3)))
            if d and margin >= 0.06 and worst <= 0.25: c['digits'] = d; c['ocr'] = True
    if MODE == 'learn': return dict(info=info), new_last
    # calls neither OCR read: raised digit-sized marks after a word, read by shape, equal to a note number here
    have = {c['tok'] for c in cands} | {c['tok'] for c in cands if c['lone']} | {c['tok'] - 1 for c in cands if c['lone']}
    found_n = {int(c['digits']) for c in cands if c['digits'] and c['digits'].isdigit()}
    for k, b in enumerate(bw):
        if k in have or not p['body'][k]['n'] or len(b['w']['t'].split()) > 1: continue
        if NOT_AFTER.match(b['t']): continue
        nxt = bw[k + 1]['w'] if k + 1 < len(bw) and bw[k + 1]['w'] is not b['w'] else None
        rm = marks_after(img, b['w'], nxt)
        if not rm: continue
        d, margin, worst = READER.read(rm[0])
        if d and d.isdigit() and margin >= 0.08 and worst <= 0.22 and int(d) in nums_in_order and int(d) not in found_n:
            m_ = re.search(r'[^\W\d_](?=[^\w]*$)', b['t'])
            cands.append(dict(tok=k, nlet=m_.end(), raw=b['t'], digits=d, ncall=0, ntrail=len(b['t']) - m_.end(), frac=1, lone=False,
                              bracket=False, follow=False, ocr=True, image_only=True))
            info.setdefault('image_only', []).append((b['t'], d, round(margin, 3), round(worst, 3)))
    cands.sort(key=lambda c: c['tok'])
    amap_calls = dp_assign(cands, nums_in_order)
    # safety: a call matched without digits stands only where the candidates between the nearest digit-confirmed
    # calls (or the page's first/last note) exactly fill the notes between them
    order = sorted(amap_calls.items()) if nums_in_order else []
    anchors = [] if not nums_in_order else[(-1, nums_in_order[0] - 1)] + [(c['tok'], n) for n, c in order if c['digits'] and (c['digits'] == str(n) or len(str(n)) >= 2)] + [(10 ** 9, nums_in_order[-1] + 1)]
    weak = []
    for n, c in order:
        if c['digits'] and (c['digits'] == str(n) or len(str(n)) >= 2): continue
        a = max(x for x in anchors if x[0] < c['tok']); b_ = min(x for x in anchors if x[0] > c['tok'])
        between_c = [cc for cc in cands if a[0] < cc['tok'] < b_[0]]
        between_n = [m for m in nums_in_order if a[1] < m < b_[1]]
        if len(between_c) != len(between_n): weak.append(n)
    for n in weak: del amap_calls[n]
    info['weak_dropped'] = weak
    info.update(cands=len(cands), calls=len(amap_calls))
    # classify md tokens: B or note j
    tokcls = {}
    for i, j in amap.items():
        tokcls[j] = ('B',) if pt[i][0] == 'B' else ('N', pt[i][1])
    # split paragraphs at the first token of each note (walking back over a label token)
    pieces = []      # (text, cls)
    for pi, t in enumerate(paras):
        tk = [(k, x) for k, x in enumerate(mt) if x[0] == pi]
        cl = [tokcls.get(k) for k, _ in tk]
        known = [c for c in cl if c]
        if not known: pieces.append([t, None, pi, 0]); continue
        cuts = []; cur = None
        for (k, x), c in zip(tk, cl):
            if c is None: continue
            if cur is not None and c != cur:
                # only cut forward: body->note, or note j -> note j' > j
                if (cur == ('B',) and c[0] == 'N') or (cur[0] == 'N' and c[0] == 'N' and c[1] > cur[1]):
                    pos = x[1]
                    allt = toks(t)
                    wi = [q for q, a in enumerate(allt) if a[0] == pos][0]
                    while wi > 0 and LABEL.match(allt[wi - 1][2]): wi -= 1
                    cuts.append((allt[wi][0], c))
                elif c != cur:
                    cuts.append(None)
            cur = c if cur is None or c != cur else cur
        if None in cuts:
            return dict(info=dict(info, skip='mixed paragraph (body after notes or notes out of order)')), new_last
        first = next(c for c in cl if c)
        prevpos = 0; prevc = first
        for pos, c in cuts:
            if pos > prevpos: pieces.append([t[prevpos:pos].rstrip(), prevc, pi, prevpos])
            prevpos = pos; prevc = c
        pieces.append([t[prevpos:], prevc, pi, prevpos])
    # unknown pieces: inherit from the piece before (inside notes) or count as body before notes
    for q, pc in enumerate(pieces):
        if pc[1] is None:
            pc[1] = pieces[q - 1][1] if q else ('B',)
    seq = [pc[1] for pc in pieces]
    firstN = next((q for q, c in enumerate(seq) if c[0] == 'N'), None)
    if firstN is None: return dict(info=dict(info, skip='notes not found in md')), new_last
    if any(c == ('B',) for c in seq[firstN:]):
        return dict(info=dict(info, skip='body text after the notes in md')), new_last
    ns = [c[1] for c in seq[firstN:]]
    if ns != sorted(ns): return dict(info=dict(info, skip='notes out of order in md')), new_last
    # ---- place the calls in the body pieces (only for notes whose text was found in the md)
    present = {numbers[pc[1][1]] for pc in pieces[firstN:] if pc[1][1] in numbers}
    info['notes_missing_in_md'] = [n for n in nums_in_order if n not in present]
    # strict boundaries (after the image check of 18 Oct): a note becomes a footnote only if its own number is read at
    # its start (layer label or the md's leading number) and the next note's start is confirmed the same way; for the
    # page's last note, its text must not contain the next number at a sentence start.
    firstpiece = {}
    for pc in pieces[firstN:]:
        firstpiece.setdefault(pc[1][1], pc[0])
    def own_label(j):
        mlab = re.match(r'^(\d{1,3})\s', (firstpiece.get(j) or '').strip() + ' ')
        return [x for x in (num(p['notes'][j]['label']), int(mlab.group(1)) if mlab else None) if x is not None]
    conf = {j: bool(own_label(j)) and all(x == numbers[j] for x in own_label(j)) for j in starts}
    alltext = {j: ' '.join(pc[0] for pc in pieces[firstN:] if pc[1][1] == j) for j in starts}
    ok_notes = set()
    for q, j in enumerate(starts):
        if not conf[j]: continue
        later = [k for k in range(j + 1, len(p['notes']))]           # any later note piece (start or not)
        if q + 1 < len(starts):
            if not conf[starts[q + 1]] or any(k for k in later if k < starts[q + 1]): continue
        else:
            if re.search(r'(^|[.)\]]\s+)%d\s+[A-Z‘\'"(]' % (numbers[j] + 1), alltext[j]): continue
            if later: continue
        ok_notes.add(numbers[j])
    info['boundary_unconfirmed'] = [numbers[j] for j in starts if numbers[j] not in ok_notes]
    present &= ok_notes
    amap_calls = {n: c for n, c in amap_calls.items() if n in present}
    edits = collections.defaultdict(list)    # piece index -> (start, end, replacement)
    placed = {}
    KEEP = set('.,;:)]}\\') | QUOTES
    for n, c in amap_calls.items():
        follow = c['follow']        # the call token has no letters ('7', '[...]3.'): anchor on the previous word
        k0 = c['tok'] - 1 if follow else c['tok']
        while follow and k0 >= 0 and not p['body'][k0]['n']: k0 -= 1
        i = body_tok_to_pt.get(k0)
        if i is None or i not in amap: placed_fail(info, n, 'not aligned'); continue
        j = amap[i]; pi, s, e, w, nw = mt[j]
        q = next((q for q, pc in enumerate(pieces) if pc[2] == pi and pc[1] == ('B',)), None)
        if q is None: placed_fail(info, n, 'not in body'); continue
        ptxt = pieces[q][0]; base = pieces[q][3]
        if not (base <= s < base + len(ptxt)): placed_fail(info, n, 'not in body piece'); continue
        s2, e2 = s - base, e - base
        if follow:
            # the next md token(s) must be the call token: digits/junk after an optional bracketed part
            m3 = re.match(r'(\s+)(\S*?[\)\]]|)([^\s\w.,;:)\]}\\\'’”"‘“\-–—/(\[{]{1,3}|\d{1,3})([.,;:]*)(?=\s|$)', ptxt[e2:])
            if not m3 or (m3.group(2) == '' and m3.group(3) != c['digits']):
                placed_fail(info, n, 'lone token not found in md'); continue
            if m3.group(2):
                repl = ptxt[e2:e2 + m3.end()].replace(m3.group(2) + m3.group(3) + m3.group(4), m3.group(2) + '[^@%d]' % n + m3.group(4), 1)
                edits[q].append((e2, e2 + m3.end(), repl)); placed[n] = 'after bracket'
            else:
                edits[q].append((e2, e2 + m3.end(), '[^@%d]' % n + m3.group(4))); placed[n] = 'lone number'
            continue
        mlj = LETTER_JUNK.match(w)
        if mlj and any(ch.isalpha() for ch in mlj.group(2)):
            # letters read for the call's digits: each must stand where that digit of the note's number stands
            core, sn = mlj.group(2), str(n)
            ok_ = len(core) <= len(sn) + 1 and all(
                (not ch.isalpha()) or (k_ < len(sn) and LM.get(ch) == sn[-1 - k_]) for k_, ch in enumerate(reversed(core)))
            if not ok_: placed_fail(info, n, 'letters in mark ' + core); continue
            edits[q].append((s2, e2, mlj.group(1) + '[^@%d]' % n + mlj.group(3))); placed[n] = 'glued (letters read for digits: %s)' % core
            info.setdefault('letters_removed', []).append((n, w)); continue
        let, tail = split_tail(w)
        if c['bracket']:
            if tail and not re.fullmatch(r'[.,;:]+', tail): placed_fail(info, n, 'bracket word differs in md'); continue
            edits[q].append((s2, e2, let + '[^@%d]' % n + tail)); placed[n] = 'after bracket'; continue
        mt_ = re.match(r'^(.*?)([.,;:]*)$', tail); core, trail = mt_.group(1), mt_.group(2)
        if not let: placed_fail(info, n, 'md word has no letters'); continue
        # remove only digits and junk marks; keep punctuation, brackets and quotes (they come before the call)
        core_u = re.sub(r'\\(?=[^\[\]\(\)])', '', core)        # a Markdown escape goes with the mark it escapes
        if core_u.count('\\') and not re.fullmatch(r'(\\[\[\]])*[^\\]*', core_u): placed_fail(info, n, 'escape ' + core); continue
        keep = ''.join(ch for ch in core_u if ch in KEEP)
        drop = ''.join(ch for ch in core_u if ch not in KEEP)
        if any(ch.isalpha() for ch in drop): placed_fail(info, n, 'md tail ' + core); continue
        if not core.startswith(keep): placed_fail(info, n, 'mark before punctuation ' + core); continue
        edits[q].append((s2, e2, let + keep + '[^@%d]' % n + trail)); placed[n] = 'glued' if drop else 'inserted'
    for q, es in edits.items():
        t = pieces[q][0]
        for s2, e2, r in sorted(es, key=lambda x: -x[0]): t = t[:s2] + r + t[e2:]
        pieces[q][0] = t
    # ---- definitions
    note_text = collections.OrderedDict()
    for pc in pieces[firstN:]:
        j = pc[1][1]; note_text.setdefault(j, []).append(pc[0].strip())
    cont = None; cont_num = None
    defs = []; vis = []; last_def_idx = None; last_def_num = None
    lab = {}
    for j, ps in note_text.items():
        if not p['notes'][j]['start']: continue
        mlab = re.match(r'^(\d{1,3})\s', ps[0].strip() + ' ')
        if not agrees(num(p['notes'][j]['label']), numbers[j]) or not agrees(int(mlab.group(1)) if mlab else None, numbers[j]):
            return dict(info=dict(info, skip='label conflict: note %d has label %s / %s' % (numbers[j], p['notes'][j]['label'], mlab.group(1) if mlab else '-'))), new_last
    for j, ps in note_text.items():
        txt = ' '.join(x.replace('\n', ' ') for x in ps).strip()
        if not p['notes'][j]['start']:
            if starts and conf[starts[0]]: cont = txt; cont_num = prev_last
            else: vis.append(txt)
            continue
        n = numbers.get(j)
        m = re.match(r'^(\d{1,3})\s+', txt)          # the note's own number (digits only: never strip a letter)
        if n in placed:
            if m: txt = txt[m.end():]
            l_ = str(n) if str(n) not in used else '%d-p%s' % (n, re.sub(r'[^\w]', '', plabel))
            if l_ in used: l_ = '%d-pdf%d' % (n, K)          # a page printed twice (PDF 257/258 are both p. 160)
            used.add(l_); lab[n] = l_
            defs.append('[^%s]: %s' % (l_, txt))
            last_def_num = n
        else:
            vis.append(txt); last_def_num = None
    info.update(placed=len(placed), defs=len(defs), unreferenced=len(vis))
    if not defs:          # no footnote on this page: leave it exactly as it is
        return dict(info=dict(info, unchanged='no call placed'), new=None), new_last
    body = [pc[0] for pc in pieces[:firstN]]
    fix = lambda t: re.sub(r'\[\^@(\d+)\]', lambda m: '[^' + lab[int(m.group(1))] + ']', t)
    new = [marker, '']
    for t in body: new += [fix(t), '']
    body_end = len(new)
    for t in vis: new += [t, '']
    for t in defs: new += [t, '']
    if defs: last_def_idx = len(new) - 2
    if defs and last_def_num is None: last_def_idx = None
    info['unplaced_calls'] = [n for n in nums_in_order if n not in placed]
    info['placed_how'] = placed
    return dict(info=info, new=new, cont=cont, cont_num=cont_num, body_end=body_end,
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
