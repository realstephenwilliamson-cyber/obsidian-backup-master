# Deshpande: link each endnote call (read from the page images) to its endnote's block id in the appendix note.
import sys, os, re, json, glob, difflib, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import anchors as A
VAULT = A.VAULT; ORIG = A.ORIG; APPX = A.APPX
MARK = re.compile(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg(\d+)$')
CHAPTERS = [(1, 14, 23), (2, 24, 29), (3, 30, 65), (4, 66, 100), (5, 101, 128), (6, 129, 138), (7, 139, 164)]
SUP = str.maketrans('0123456789ABab', '⁰¹²³⁴⁵⁶⁷⁸⁹ᴬᴮᵃᵇ')
QUOTE = str.maketrans({'’': "'", '‘': "'", '`': "'", '”': '"', '“': '"', '„': '"'})
norm = A.norm

def chapter_of(K):
    return next(c for c, a, b in CHAPTERS if a <= K <= b)

def load_calls():
    calls = []
    for f in sorted(glob.glob(os.path.join(HERE, 'calls_*.json'))):
        calls += json.load(open(f, encoding='utf-8'))
    # verse labels the readers flagged (raised numbers ending Sanskrit couplets) are not note calls
    return [c for c in calls if not (not c.get('certain', True) and re.search(r'(?i)verse', c.get('note', '')))]

def tail(w):
    m = re.search(r'[^\W\d_]', w[::-1])
    return w[len(w) - m.start():] if m else w

def run():
    calls = load_calls()
    # sequence check per chapter: numbers must rise 1, 2, 3 ... in reading order (gaps allowed, no repeats, no going back)
    by_ch = collections.defaultdict(list)
    for c in calls: by_ch[chapter_of(c['pdf'])].append(c)
    seqrep = {}
    def key(s):
        m = re.fullmatch(r'\s*(\d+)\s*([A-Za-z]?)\s*', s)
        return (int(m.group(1)), m.group(2).lower()) if m else None
    for ch, cs in by_ch.items():
        cnt = collections.Counter(key(c['number']) for c in cs)
        keep = [c for c in cs if key(c['number']) and cnt[key(c['number'])] == 1]
        dropped = [c for c in cs if c not in keep]
        # longest strictly increasing run (in reading order)
        ks = [key(c['number']) for c in keep]; best = []; back = []
        for i, k in enumerate(ks):
            b_, j_ = 1, None
            for j in range(i):
                if ks[j] < k and best[j] + 1 > b_: b_, j_ = best[j] + 1, j
            best.append(b_); back.append(j_)
        lis = set()
        if ks:
            i = max(range(len(ks)), key=lambda i: best[i])
            while i is not None: lis.add(i); i = back[i]
        dropped += [c for i, c in enumerate(keep) if i not in lis]
        for c in dropped: c['dropped'] = True
        seqrep[ch] = dict(numbers=[c['number'] for c in cs], in_order=True,
                          dropped=[(c['pdf'], c['number'], c['before']) for c in dropped])
    L, paras, notes, anchors, report, splits = A.run()
    files = {}
    for f in sorted(glob.glob(os.path.join(glob.escape(ORIG), '*.md'))):
        T = open(f, encoding='utf-8').read().split('\n')
        files[os.path.basename(f)] = T
    # page -> (file, line range)
    where = {}
    for fn, T in files.items():
        marks = [(i, int(m.group(1))) for i, l in enumerate(T) for m in [MARK.match(l)] if m]
        for j, (i, K) in enumerate(marks):
            where[K] = (fn, i, marks[j + 1][0] if j + 1 < len(marks) else len(T))
    out = {fn: list(T) for fn, T in files.items()}
    log = []
    edits = collections.defaultdict(list)     # (file, line) -> [(start, end, replacement)]
    for c in calls:
        ch = chapter_of(c['pdf']); num = c['number'].strip().replace('-', '')
        m = re.fullmatch(r'(\d+)([A-Za-z]?)', num)
        if not m: log.append((c, 'number not usable')); continue
        bid = 'n-%d-%d%s' % (ch, int(m.group(1)), m.group(2).lower())
        if bid not in anchors: log.append((c, 'endnote %s has no anchor' % bid)); continue
        if c.get('dropped'): log.append((c, 'dropped: repeated, unreadable or out of order in chapter %d' % ch)); continue
        # find the words before the call in the page's md (and the previous page, for a call at a page top)
        before = [w for w in c['before'].split() if norm(w)]
        if not before: log.append((c, 'no words before')); continue
        best = None
        for K in (c['pdf'], c['pdf'] - 1):
            if K not in where: continue
            fn, a, b = where[K]
            toks = [(li, mm.start(), mm.end(), mm.group(0)) for li in range(a + 1, b) for mm in re.finditer(r'\S+', files[fn][li])
                    if norm(mm.group(0))]
            tn = [norm(t[3]) for t in toks]; bn = [norm(w) for w in before]
            for e in range(len(toks)):
                s = max(0, e - len(bn) + 1)
                r = difflib.SequenceMatcher(None, ''.join(tn[s:e + 1]), ''.join(bn)).ratio()
                last = difflib.SequenceMatcher(None, tn[e], bn[-1]).ratio()
                sc = r + last
                if best is None or sc > best[0]: best = (sc, r, last, fn, toks[e], K)
            if best and best[1] >= 0.75 and best[2] >= 0.7: break
        if not best or best[1] < 0.75 or best[2] < 0.7:
            log.append((c, 'words not found (%.2f/%.2f)' % (best[1], best[2]) if best else 'words not found')); continue
        _, r, last, fn, (li, s, e, w), K = best
        if files[fn][li].startswith('#'): log.append((c, 'call on a heading: left alone')); continue
        # junk at the call: md tail beyond the printed punctuation, if it has no letters or digits other than the call's
        pt_ = tail(before[-1]).translate(QUOTE); mt_ = tail(w).translate(QUOTE)
        cut = e; keep_after = ''
        if mt_ != pt_:
            rem = tail(w)[len(pt_):] if mt_.startswith(pt_) else None
            if rem is not None and not re.search(r'[^\W\d_]', unicodedata.normalize('NFKC', rem).replace('TM', '')):
                # punctuation printed after the call stays, unless the printed word already ends in punctuation
                # (then whatever follows in the md is the OCR's reading of the number)
                mp = re.search(r'[.,;:]', rem)
                keep_after = '' if re.search(r'[.,;:!?\'"’”]$', before[-1]) or not mp else rem[mp.start():]
                cut = e - len(rem)                                     # drop the junk that stood for the call
            elif pt_.startswith(mt_):
                pass                                       # the md lacks some printed punctuation: insert after the word
            else:
                log.append((c, 'punctuation differs: md %r printed %r' % (w, before[-1]))); continue
        lab = (m.group(1) + m.group(2)).translate(SUP)
        link = '[[%s#^%s|%s]]' % (APPX[:-3], bid, lab) + keep_after
        edits[(fn, li)].append((cut, e, link, c, bid))
        log.append((c, 'linked %s in %s line %d%s' % (bid, fn[:20], li + 1, '' if cut == e else ' (junk %r removed)' % w[cut - s:])))
    for (fn, li), es in edits.items():
        t = out[fn][li]
        for cut, e, link, c, bid in sorted(es, key=lambda x: -x[0]):
            t = t[:cut] + link + t[e:]
        out[fn][li] = t
    used = {bid for (fn, li), es in edits.items() for (_, _, _, _, bid) in es}
    out[APPX], sp_log = rebuild_appendix(out[APPX], paras, anchors, used)
    log += sp_log
    return files, out, log, seqrep, anchors, used

def rebuild_appendix(AP, paras, anchors, used):
    """Block ids for the linked endnotes. A note that starts inside a paragraph splits it there; each id goes at the
    end of the stretch of text that belongs to its note (up to the next split in that paragraph or the paragraph end)."""
    AP = list(AP); log = []
    cuts_by_para = collections.defaultdict(list)
    for bid, an in anchors.items():
        if bid in used: cuts_by_para[an['pi']].append(((an['li'], 0) if an['at_start'] else (an['li'], an['cut']), bid, an['at_start']))
    for pi in sorted(cuts_by_para, reverse=True):
        lines = paras[pi]
        cs = sorted(cuts_by_para[pi])
        # positions in the paragraph text (lines joined by \n)
        text = '\n'.join(AP[li] for li in lines)
        offs = {}; o = 0
        for li in lines: offs[li] = o; o += len(AP[li]) + 1
        pts = [(offs[li] + c, bid) for (li, c), bid, st_ in cs]
        bounds = [p for p, b in pts] + [len(text)]
        segs = []
        if pts[0][0] > 0: segs.append((text[:pts[0][0]].rstrip(), None))
        for k, (p, bid) in enumerate(pts):
            segs.append((text[p:bounds[k + 1]].rstrip(), bid))
        newtext = '\n\n'.join(s + (' ^' + b if b else '') for s, b in segs if s.strip() or b)
        if len(segs) > 1 or (pts[0][0] > 0): log.append(({'pdf': 0, 'number': ','.join(b for p, b in pts)}, 'paragraph split in the appendix'))
        AP[lines[0]] = newtext
        for li in lines[1:]: AP[li] = None
    return [l for l in AP if l is not None], log

def _unused():
    AP = []; used = set(); anchors = {}; paras = []; log = []
    by_line = collections.defaultdict(list)
    for bid, an in anchors.items(): by_line[an['li']].append((an['cut'], bid, an))
    para_end = {}
    for pi, lines in enumerate(paras): para_end[pi] = lines[-1]
    ins = collections.defaultdict(list)      # line -> list of (pos, text) inserts
    for bid, an in anchors.items():
        if bid not in used: continue          # only notes that a call links to get an id
        if an['at_start']:
            ins[para_end[an['pi']]].append((None, bid))         # id at the end of the paragraph
        else:
            ins[an['li']].append((an['cut'], bid))               # split: the note's part ends where the next begins
    newAP = []
    for i, l in enumerate(AP):
        if i not in ins: newAP.append(l); continue
        items = ins[i]
        ends = [b for p, b in items if p is None]
        splits_ = sorted([(p, b) for p, b in items if p is not None])
        # paragraph splits on this line: text before the cut stays (closing the previous paragraph); the note starts a new one
        pieces = []; prev = 0; bids = []
        for p, b in splits_:
            pieces.append(l[prev:p].rstrip()); prev = p; bids.append(b)
        pieces.append(l[prev:])
        # the id of a split note goes at the end of its piece if the note ends on this line, else at its paragraph's end
        line_out = [pieces[0]]
        for k, b in enumerate(bids):
            line_out.append(pieces[k + 1])
        # assemble: each piece after the first starts a new paragraph
        text = line_out[0]
        for k, b in enumerate(bids):
            nxt_piece = line_out[k + 1]
            text += '\n\n' + nxt_piece
        # where do the split notes' ids go? if this line is the end of the paragraph, at the end of each piece except
        # the last, which gets the paragraph-end ids (and its own id) ; split notes whose paragraph continues: at para end
        parts = text.split('\n\n')
        for k, b in enumerate(bids):
            if k + 1 < len(parts) - 1: parts[k + 1] = parts[k + 1].rstrip() + ' ^' + b
            else: ends.append(b)
        if ends:
            if any(i == para_end[pi] for pi in range(len(paras))):
                parts[-1] = parts[-1].rstrip() + ''.join(' ^' + b for b in ends[:1])
                for extra in ends[1:]: log.append(({'pdf': 0, 'number': extra}, 'two ids on one paragraph, extra dropped: ' + extra))
            else:
                # the paragraph continues on the next lines: the id goes at the paragraph end (handled below)
                pass
        newAP.append('\n\n'.join(parts))
    return newAP

if __name__ == '__main__':
    files, out, log, seqrep, anchors, used = run()
    for ch, v in sorted(seqrep.items()): print('chapter', ch, 'in order' if v['in_order'] else 'NOT IN ORDER', ' '.join(v['numbers']))
    c = collections.Counter(x[1].split(' ')[0] for x in log)
    print(c)
    for cc, why in log:
        if not why.startswith('linked'): print('  ', cc.get('pdf'), cc.get('number'), cc.get('before'), '->', why)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    for fn, T in out.items():
        if T != files[fn]:
            txt = '\n'.join(T)
            SUF = '; endnote calls linked from the page images 18 Oct 2026'
            txt = re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1) + (m.group(2)[:-1] + SUF + '"' if m.group(2).endswith('"') else m.group(2) + SUF), txt, count=1, flags=re.M)
            open(os.path.join(HERE, 'out', fn), 'w', encoding='utf-8', newline='\n').write(txt)
    json.dump([(cc, why) for cc, why in log], open(os.path.join(HERE, 'linklog.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
