# Dhvanyaloka: the section notes (numbered per K/A/L block) become Markdown footnotes, from the ABBYY text layer.
# A note becomes a footnote only if (1) its call's digits are read in the block's text, in order, (2) its label is in
# the layer's unbroken chain 1, 2, 3 ..., (3) its start is confirmed in the md (label or paragraph break) and its end
# is confirmed (the next note's confirmed start, or the next block's start), (4) the chain is not cut short.
import sys, os, re, json, glob, difflib, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import blocks as BL
VAULT = r'C:\Vaults\Obsidian Vault'
ORIG = os.path.join(VAULT, r'.work\backup-footnotes-2026-10-18\Dhvanyaloka\Library\Trika\The Dhvanyaloka of Anandavardhana with the Locana (Anandavardhana)')
MARK = re.compile(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg(\d+)$')
norm = BL.norm
LM = {'s': '5', 'S': '5', 'l': '1', 'I': '1', 'i': '1', 't': '1', 'z': '2', 'Z': '2', 'o': '0', 'O': '0', 'b': '6', 'g': '9', 'q': '9', 'B': '8'}
QUOTES = set('\'’”"‘“')
KEEP = set('.,;:)]}|\\') | QUOTES
A, B = 56, 745

def load_md():
    """md files of the translation: text, page sections, tokens with absolute offsets"""
    F = {}
    for f in sorted(glob.glob(os.path.join(glob.escape(ORIG), '*.md'))):
        t = open(f, encoding='utf-8').read()
        lines = t.split('\n'); offs = []; o = 0
        for l in lines: offs.append(o); o += len(l) + 1
        marks = [(i, int(m.group(1))) for i, l in enumerate(lines) for m in [MARK.match(l)] if m]
        if not marks or marks[-1][1] < A or marks[0][1] > B: continue
        F[os.path.basename(f)] = dict(t=t, lines=lines, offs=offs, marks=marks)
    return F

def page_tokens(F):
    """K -> (file, [md tokens (abs start, abs end, word, norm, is_para_start)])"""
    P = {}
    for fn, d in F.items():
        L, offs, marks = d['lines'], d['offs'], d['marks']
        for j, (i, K) in enumerate(marks):
            e = marks[j + 1][0] if j + 1 < len(marks) else len(L)
            toks = []
            for li in range(i + 1, e):
                l = L[li]
                if l.startswith('#') or MARK.match(l): continue
                para_start = li == i + 1 or not L[li - 1].strip() or L[li - 1].startswith('#')
                for k, m in enumerate(re.finditer(r'\S+', l)):
                    toks.append((offs[li] + m.start(), offs[li] + m.end(), m.group(0), norm(m.group(0)), para_start and k == 0))
            P[K] = (fn, toks)
    return P

def align_page(K, frs, P):
    """layer tokens of page K (list of (frag, tokidx)) -> md token index, by difflib over normalised words"""
    if K not in P: return {}, []
    fn, mt = P[K]
    lt = [(fi, ti, t) for fi, f in enumerate(frs) for ti, t in enumerate(f['toks'])]
    a = [norm(t) for (_, _, t) in lt]; b = [x[3] for x in mt]
    ai = [k for k, x in enumerate(a) if x]; bi = [k for k, x in enumerate(b) if x]
    sm = difflib.SequenceMatcher(None, [a[k] for k in ai], [b[k] for k in bi], autojunk=False)
    amap = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for d in range(i2 - i1): amap[(lt[ai[i1 + d]][0], lt[ai[i1 + d]][1])] = bi[j1 + d]
    return amap, mt

def split_tail(w):
    m = re.match(r'^(.*[^\W\d_][\)\]\}]?)(.*)$', w)
    return (m.group(1), m.group(2)) if m else ('', w)

def call_edit(w, n, drop_quotes=False, punct_first=False):
    """replacement for the md word w carrying call n (junk at its end removed), or None if not safe.
    drop_quotes: the layer shows no quote mark there, so quote marks in the md tail are the misread number;
    punct_first: the layer shows punctuation before the number ('absurdity.6'), so the reference goes after it."""
    md = re.match(r'^(.*?)([—–].*)$', w)
    if md and md.group(1) and norm(md.group(1)):          # 'properties’°—and': the call is before the dash
        r = call_edit(md.group(1), n, drop_quotes, punct_first)
        return r + md.group(2) if r else None
    let, tail = split_tail(w)
    if not let: return None
    m = re.match(r'^(.*?)([.,;:]*)$', tail); core, trail = m.group(1), m.group(2)
    core_u = re.sub(r'\\(?=[^\[\]\(\)])', '', core)
    keepset = KEEP - set(drop_quotes or ())
    keep = ''.join(ch for ch in core_u if ch in keepset); drop = ''.join(ch for ch in core_u if ch not in keepset)
    if any(ch.isalpha() for ch in drop) or not core_u.startswith(keep): return None
    if punct_first: return let + keep + trail + '[^@]'
    return let + keep + '[^@]' + trail

def open_quote(text, pos, word):
    """is there an unclosed opening quotation mark before this word in its paragraph (so a closing quote after the
    word can be real)? A closing quote with no opening one before it is the OCR's reading of the raised number."""
    start = text.rfind('\n\n', 0, pos) + 2
    before = text[start:pos] + word[:max((i for i, ch in enumerate(word) if ch.isalpha()), default=-1) + 1]
    dbl = before.count('“') + before.count('"') - before.count('”')
    sgl = len(re.findall(r'‘|(?:^|\s)\'', before)) - len(re.findall(r'’(?=\s|$)', before))
    return (dbl > 0, sgl > 0)

def quotes_to_drop(layer_t, text, pos, word):
    """the quote marks at the call that are the misread number: all of them if the layer shows none there;
    otherwise those of a kind (double / single) that has no open quotation before the word"""
    # only on the layer's evidence: where both OCRs read a quote mark it stays (a stray mark is better than
    # deleting a printed one; the quotation count of a paragraph proved unreliable, 18 Oct)
    # the layer, too, drops real quote marks beside a raised number, so no quote mark is ever removed (18 Oct)
    return set()

def layer_tail(t):
    """what the layer token shows between the word and the call digits"""
    m = BL.CALL.match(t)
    if not m: return ''
    g = m.group(1); k = max((i for i, ch in enumerate(g) if ch.isalpha()), default=-1)
    return g[k + 1:]

def run():
    F = load_md(); P = page_tokens(F)
    S = BL.stream(A, B)
    for i, f in enumerate(S): f['i'] = i
    blks = BL.blocks(S)
    byK = collections.defaultdict(list)
    for f in S: byK[f['K']].append(f)
    amaps = {}
    for K, frs in byK.items():
        am, mt = align_page(K, frs, P)
        for (fi, ti), j in am.items(): amaps[(frs[fi]['i'], ti)] = (K, j)
    def md_of(f, ti):
        v = amaps.get((f['i'], ti))
        if not v: return None
        K, j = v; return K, j, P[K][1][j]
    edits = collections.defaultdict(list)    # file -> [(abs start, abs end, replacement, kind)]
    rep = collections.Counter(); log = []; seen_blocks = {}
    for bi, b in enumerate(blks):
        if b['letter'] == '?': continue
        text, notes = BL.split_block(b)
        if not notes: rep['blocks without notes'] += 1; continue
        chain = BL.label_chain(notes)
        m = len(chain)
        cands = BL.calls_in(text)
        # calls: candidates with exact digits 1..m, strictly increasing in reading order (longest run)
        cs = [c for c in cands if 1 <= c[2] <= m]
        best = []; back = []
        for i, c in enumerate(cs):
            bb, kk = 1, None
            for k in range(i):
                if cs[k][2] < c[2] and best[k] + 1 > bb: bb, kk = best[k] + 1, k
            best.append(bb); back.append(kk)
        calls = {}
        if cs:
            i = max(range(len(cs)), key=lambda i: best[i])
            chosen = []
            while i is not None: chosen.append(i); i = back[i]
            chosen.reverse()
            # a number is ambiguous if another candidate with the same digits would also fit between its neighbours
            for q, i in enumerate(chosen):
                lo = chosen[q - 1] if q > 0 else -1; hi = chosen[q + 1] if q + 1 < len(chosen) else len(cs)
                if any(cs[k][2] == cs[i][2] for k in range(lo + 1, hi) if k != i):
                    rep['ambiguous call'] += 1; continue
                calls[cs[i][2]] = cs[i]
        # the chain must not be cut short
        higher = [c[2] for c in cands if c[2] > m and c[1] >= 0]
        rest_toks = [t for f in notes for t in f['toks']]
        cut_short = (m == 0) or any(int(c) == m + 1 for c in re.findall(r'(?:^|\s)(\d{1,2})\.(?=\s+[A-Z“"(\[])', ' ' + ' '.join(rest_toks)))
        # md positions of the note starts and of the block's end (the next block's first word)
        starts = {}
        for (fi, ti, n) in chain:
            f = notes[fi]
            # first word after the label, aligned in the md
            r = None
            for f2i in range(fi, len(notes)):
                t0 = ti + 1 if f2i == fi else 0
                for t2 in range(t0, len(notes[f2i]['toks'])):
                    if norm(notes[f2i]['toks'][t2]):
                        r = md_of(notes[f2i], t2); break
                    if f2i > fi or t2 > ti + 3: break
                if r is not None or f2i > fi: break
            if not r: continue
            K, j, tok = r
            mt = P[K][1]
            # walk back over the md label token (digits, escaped dot, look-alikes) right before
            if j > 0 and re.fullmatch(r'[\dIlOoSsz|!]{1,3}\\?[.,]?', mt[j - 1][2]) and mt[j - 1][1] <= tok[0]:
                lab = mt[j - 1][2]; digits = ''.join(LM.get(ch, ch) for ch in re.sub(r'[\\.,]', '', lab))
                if digits == str(n): starts[n] = (K, mt[j - 1][0], 'label')
                continue
            if tok[4]: starts[n] = (K, tok[0], 'paragraph')
        nb = next((x for x in blks[bi + 1:] if x['letter'] != '?' or x['frags']), None)
        block_end = None
        if nb and nb['frags']:
            f0 = nb['frags'][0]
            for ti, t in enumerate(f0['toks']):
                if norm(t):
                    r = md_of(f0, ti)
                    if r and r[2][4]: block_end = (r[0], r[2][0])
                    elif r:
                        # 'K Some have said' : the md has the margin letter first in the paragraph
                        K, j, tok = r; mt = P[K][1]
                        if j > 0 and mt[j - 1][4] and re.fullmatch(r'[KAL]', mt[j - 1][2]): block_end = (K, mt[j - 1][0])
                    break
        for n in range(1, m + 1):
            if n not in calls: rep['no call'] += 1; continue
            if n not in starts: rep['start not confirmed'] += 1; continue
            if n < m:
                if n + 1 not in starts: rep['end not confirmed'] += 1; continue
                end = starts[n + 1]
            else:
                if cut_short or higher or block_end is None: rep['last note not confirmed'] += 1; continue
                end = block_end
            st_ = starts[n]
            fn_s = P[st_[0]][0]; fn_e = P[end[0]][0]
            if fn_s != fn_e: rep['note crosses a file'] += 1; continue
            span = F[fn_s]['t'][st_[1]:end[1]]
            if end[1] <= st_[1] or re.search(r'(?m)^#', span) or len(span) > 6000: rep['span unusable'] += 1; continue
            # the call
            c = calls[n]; f = text[c[0]]
            if c[3] == 'glued':
                r = md_of(f, c[1])
                if not r: rep['call not aligned'] += 1; continue
                K, j, tok = r
                if P[K][0] != fn_s and False: pass
                lt = layer_tail(re.split(r'[—–]', f['toks'][c[1]])[0])
                new = call_edit(tok[2], n, drop_quotes=quotes_to_drop(lt, F[P[K][0]]['t'], tok[0], tok[2]),
                                punct_first=bool(re.search(r'[.,;:!?]$', lt)))
                if new is None: rep['call word unsafe'] += 1; continue
                cedit = (P[K][0], tok[0], tok[1], new)
            else:
                # a separate fragment ('.1'): anchor on the previous word with letters
                prev = None
                for back_i in range(c[1] - 1, -1, -1):
                    if norm(f['toks'][back_i]): prev = (c[0], back_i); break
                if prev is None:
                    for fi2 in range(c[0] - 1, -1, -1):
                        ws = [k for k, t in enumerate(text[fi2]['toks']) if norm(t)]
                        if ws: prev = (fi2, ws[-1]); break
                r = md_of(text[prev[0]], prev[1]) if prev else None
                if not r: rep['call not aligned'] += 1; continue
                K, j, tok = r; mt = P[K][1]
                nxt = mt[j + 1] if j + 1 < len(mt) else None
                lt_ = f['toks'][c[1]]
                if re.search(r'[)\]]', lt_):
                    # printed after a bracket ('[Bhāmaha 3.28]²'): the md token with the same bracket, within 3 words
                    br = ']' if ']' in lt_ else ')'
                    hit = next((x for x in mt[j:j + 4] if br in x[2].replace('\\]', ']')), None)
                    if not hit: rep['bracket call not found'] += 1; continue
                    w_ = hit[2]; k_ = w_.rfind(br) + 1
                    rest = w_[k_:]
                    if re.search(r'[^\W\d_]', rest): rep['bracket call not found'] += 1; continue
                    tr = ''.join(ch for ch in rest if ch in '.,;:' or ch in QUOTES)          # punctuation stays, junk goes
                    cedit = (P[K][0], hit[0], hit[1], w_[:k_] + '[^@]' + tr)
                elif nxt and re.fullmatch(r'[\d?!*°]{1,3}[.,;:]?', nxt[2]):
                    # the md has the call as a separate junk token: drop it, keep trailing punctuation
                    tr = re.search(r'[.,;:]*$', nxt[2]).group(0)
                    cedit = (P[K][0], tok[0], nxt[1], tok[2] + '[^@]' + tr)
                else:
                    dq = quotes_to_drop(lt_, F[P[K][0]]['t'], tok[0], tok[2])
                    new = call_edit(tok[2], n, drop_quotes=dq, punct_first=bool(re.search(r'^[.,;:!?]', lt_))) or (tok[2] + '[^@]')
                    cedit = (P[K][0], tok[0], tok[1], new)
            if cedit[0] != fn_s: rep['call and note in different files'] += 1; continue
            bl_id = '%s%d' % (b['letter'], b['K'])
            if bl_id in seen_blocks and seen_blocks[bl_id] != bi: bl_id += chr(ord('a') + list(seen_blocks).count(bl_id))
            seen_blocks.setdefault('%s%d' % (b['letter'], b['K']), bi)
            # a second block with the same letter starting on the same page gets a letter suffix
            if seen_blocks['%s%d' % (b['letter'], b['K'])] != bi: bl_id = '%s%db' % (b['letter'], b['K'])
            idl = '%s-%d' % (bl_id, n)
            edits[fn_s].append(('def', st_[1], end[1], idl, n))
            edits[cedit[0]].append(('call', cedit[1], cedit[2], cedit[3].replace('[^@]', '[^%s]' % idl), n))
            rep['footnotes'] += 1
        rep['notes'] += m; rep['blocks'] += 1
    return F, edits, rep

def apply(F, edits):
    out = {}
    for fn, es in edits.items():
        t = F[fn]['t']
        # resolve overlaps: a call inside a definition span is fine (calls are in block text, defs in notes)
        es = sorted(es, key=lambda e: -e[1])
        last_start = len(t) + 1
        for e in es:
            kind, s, en = e[0], e[1], e[2]
            if en > last_start: continue                      # overlapping edit: skip (logged by count)
            if kind == 'call':
                t = t[:s] + e[3] + t[en:]
            else:
                span = t[s:en]
                lines = span.split('\n')
                RH = re.compile(r'^\s*\\?\[?\s*[§S]\s*\d+[.\-]\d+|^\s*\d{1,3}\s*\\?\[?\s*[§S]\s*\d')      # running heads
                keep_lines = [l for l in lines if MARK.match(l) or l.startswith('#') or RH.match(l)]
                if any(l.startswith('#') for l in keep_lines): continue
                body = ' '.join(l.strip() for l in lines if l.strip() and not MARK.match(l) and not RH.match(l))
                ml = re.match(r'^\s*([\dIlOoSsz|!]{1,3})\\?[.,]\s+', body)
                if ml and ''.join(LM.get(ch, ch) for ch in ml.group(1)) == str(e[4]): body = body[ml.end():]   # the label
                rep_ = '[^%s]: %s' % (e[3], body.strip())
                pre = '' if s == 0 or t[:s].endswith('\n\n') else ('\n' if t[:s].endswith('\n') else '\n\n')
                post = ''.join('\n\n' + l for l in keep_lines)
                tail_ = t[en:]
                # an unconverted note now opening its own paragraph ('11. …') would show as a list: escape its dot
                tail_ = re.sub(r'^(\s*\d{1,3})\.(\s)', r'\1\\.\2', tail_, count=1)
                sep ='\n\n' if not tail_.startswith('\n') else ('\n' if not tail_.startswith('\n\n') else '')
                t = t[:s].rstrip(' ') + pre + rep_ + post + sep + tail_.lstrip(' ')
            last_start = s
        out[fn] = t
    return out

if __name__ == '__main__':
    F, edits, rep = run()
    print(dict(rep))
    out = apply(F, edits)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    for fn, t in out.items():
        SUF = '; section notes made Markdown footnotes from the PDF text layer 18 Oct 2026'
        t = re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1) + (m.group(2)[:-1] + SUF + '"' if m.group(2).endswith('"') else m.group(2) + SUF), t, count=1, flags=re.M)
        open(os.path.join(HERE, 'out', fn), 'w', encoding='utf-8', newline='\n').write(t)
    print('files', len(out))
