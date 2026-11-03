# prepass_ch09.py (2 Nov 2026): vol. 6 Chapter Nine, adapted from prepass_ch2.py (28 Oct 2026), the Chapter Two pre-pass. Chapter Two's footnotes (vol. 2 notes 02-03) stand as plain
# paragraphs whose numbers the OCR lost or garbled, so prepass.py does not see them. This script finds each footnote's
# start in the note from the page images (fnstarts2.py + the token filter + supnum.py: starts4.json, each start with its
# OCR'd first words and, where Tesseract could read it, the superscript number), numbers them through the chapter
# (OCR'd numbers as anchors, the rest by sequence; flags where the two disagree), and writes the note with each matched
# start made a numbered plain paragraph `N\. text` (the garbled leading token dropped; a start inside a line split off
# into its own paragraph), which prepass.py then turns into definitions as on the nights.
# Usage: prepass_ch2.py STARTS.json OUTDIR ID=NOTE [ID=NOTE ...]  (notes in chapter order)
#   -> OUTDIR/ID.num.md (input for prepass.py), OUTDIR/ch2-map.json (every start: page, number, line, how matched, flags)
import sys, json, re, unicodedata, difflib, os
startsf, outdir = sys.argv[1:3]; notes = [a.split('=', 1) for a in sys.argv[3:]]
S = json.load(open(startsf, encoding='utf-8')); os.makedirs(outdir, exist_ok=True)
PAGE = re.compile(r'^\*\[p\. ([^\]]*)\]\* \^pg(\d+)\s*$')
REAL = re.compile(r'^\[\^(\d+)\]:\s*')
GTOK = re.compile(r"^(?:[^\w\s‘“(\[]{1,3}\w?|\d{1,3}[^\w\s]{0,3}|[‘“][\dSs§°*!'’”]{1,2}|।\S{0,3}|\\\*\S{0,3}|[^\w\s]{0,2}\d{1,3}[^\w\s]{0,2})\s+")
def fold(s):
    s = unicodedata.normalize('NFKD', s); return ''.join(c for c in s if c.isascii() and c.isalnum()).lower()
def norm_map(line):
    out, pos = [], []
    for i, ch in enumerate(line):
        f = fold(ch)
        for c in f: out.append(c); pos.append(i)
    return ''.join(out), pos
# ch09: garbled superscripts glued into a token with a letter, seen on the page images (2 Nov 2026): 41 (PDF 32), 54 (38),
# 124 (72), 441 (230), 454 (235)
FORCEDROP = {'“l', '5i', '1TM', '45t'}
# ch09: marks that stand at the head of a footnote's text in place of its number (dropped only there, not before a start)
LEADDROP = {'\\^', '\\`\\^', '¶', '||', '+:', "'", '"', '”', '%t'}
def droppable(t):
    # a garbled superscript number: digits and marks, at most one trailing S/s/l/I; never a parenthesised or
    # punctuated reference ("(122)", "70).", "105.") or a closing quote
    if t in ('TM', '™'): return True
    if t in FORCEDROP: return True
    if re.fullmatch(r'[%#*°©®™§>+»«$&\\]+[’”\'"]+', t): return True   # ch09: '%”', '*’' (a mark and a quote: a garble, not a closing quote)
    if '-' in t or '/' in t or '–' in t: return False
    if t.startswith('(') or re.search(r'[).,;:’”\]]$', t) and not re.fullmatch(r'\d{1,3}[!?%#$*]?', t): return False
    if re.search(r'[A-RT-Za-rt-z]', t.replace('l', '').replace('I', '')): return False
    if re.fullmatch(r'[’”\'"]+', t): return False
    return bool(re.search(r'[\d*°©®§!?%#$>™\'"।॥&+€~<=]', t)) and not re.fullmatch(r'[‘“]+', t)
rows = []   # all starts in chapter order
for k in sorted(S, key=int):
    for s in S[k]['starts']:
        t = s['ocr'].split(' ', 1); words = t[1] if len(t) > 1 else ''
        rows.append({'pdf': int(k), 'y': s['y'], 'tok': s['tok'], 'num_ocr': s.get('num3', ''), 'target': fold(words)[:28], 'ocr': s['ocr'][:70]})
texts = {nid: open(p, encoding='utf-8').read().split('\n') for nid, p in notes}
# page blocks: pdf -> (nid, first line idx, last line idx)
blocks = {}
for nid, _ in notes:
    L = texts[nid]; cur = None
    for i, l in enumerate(L):
        m = PAGE.match(l)
        if m: cur = int(m.group(2)); blocks[cur] = [nid, i + 1, len(L) - 1]
        if cur and i > blocks[cur][1]: blocks[cur][2] = i
for r in rows:
    if r['pdf'] not in blocks: r['match'] = None; r['_cl'] = []; continue
    best = (0, None); cl = []
    for pdf in (r['pdf'], r['pdf'] + 1, r['pdf'] - 1):
        if pdf not in blocks: continue
        nid, a, b = blocks[pdf]; L = texts[nid]
        for i in range(a, b + 1):
            l = L[i]
            if not l.strip() or re.match(r'^#{1,6} ', l) or PAGE.match(l): continue   # (ch09: '#10 text' is a garbled superscript, not a heading)
            n, pos = norm_map(l)
            cands = set([0])
            for m in re.finditer(r'(?<=\s)\S', l): cands.add(m.start())
            for c in sorted(cands):
                j = next((q for q, p in enumerate(pos) if p >= c), None)
                if j is None: continue
                seg = n[j:j + len(r['target'])]
                if len(r['target']) < 5: continue
                sc = difflib.SequenceMatcher(None, seg, r['target']).ratio() - (0.03 if pdf != r['pdf'] else 0)
                if sc >= 0.6: cl.append((sc, (nid, i, c, pdf)))
                if sc > best[0]: best = (sc, (nid, i, c, pdf))
    r['_cl'] = cl
# ch09: the choice is made in chapter order, so that two starts with the same first words (e.g. 'Read with the MV KSTS
# edition' for 30 and 31) take different places: a place already taken (within 3 characters) is not offered again, and
# among the best-scoring places (within 0.02) the first one after the previous start's place is preferred.
nidx = {nid: k for k, (nid, _) in enumerate(notes)}
def dkey(m): return (nidx[m[0]], m[1], m[2])
def clean(m):
    nid, i, c, pdf = m; l = texts[nid][i]
    if c == 0: return 2
    tk = l[:c].split()
    return 1 if tk and droppable(tk[-1]) else 0
used = []; prevkey = None
for r in rows:
    cl = [x for x in r.pop('_cl', []) if not any(x[1][0] == u[0] and x[1][1] == u[1] and abs(x[1][2] - u[2]) <= 3 for u in used)]
    if not cl:
        r['score'] = r.get('score', 0) if 'score' in r else 0; r['match'] = None
        if 'score' not in r: r['score'] = 0
        continue
    bs = max(x[0] for x in cl)
    top = [x for x in cl if x[0] >= bs - 0.02]
    after = [x for x in top if prevkey is None or dkey(x[1]) > prevkey]
    best = min(after, key=lambda x: dkey(x[1])) if after else max(top, key=lambda x: x[0])
    near = [x for x in cl if x[0] >= best[0] - 0.05 and x[1][:2] == best[1][:2] and (prevkey is None or not after or dkey(x[1]) > prevkey)]
    near.sort(key=lambda x: (-clean(x[1]), -x[0], x[1][2]))
    if near: best = (best[0], near[0][1])
    r['score'] = round(best[0], 3)
    r['match'] = best[1] if best[0] >= 0.75 else None
    if r['match']: used.append(r['match']); prevkey = dkey(r['match'])
# ch09: footnote starts the image pass missed or could not match, placed by hand from the page images (2 Nov 2026):
# (pdf, y on the 300 dpi image, printed number, exact text in the note where the footnote begins, the garble at its head
# that is dropped). A manual entry replaces an image start on the same page within 12 px.
MANUAL = [(21, 2230, 7, '7 In other words, if there is only one', '7 '),
          (32, 2400, 40, '+“ 7 2/4/3-4.', '+“ '),
          (68, 1096, 102, '02 Read kālordhve for kalordhve.', '02 '),
          (71, 1806, 116, '! The sequence taught in these verses', '! '),
          (75, 1692, 134, '1 We have observed many times', '1 '),
          (80, 2298, 151, '151 Cf. BhoKā 3:', '151 '),
          (84, 2184, 162, '162 Read —viṣayallehanonmukhatāmātraṁ', '162 '),
          (105, 1956, 205, '५ ऽक सव कोप,', ''),
          (112, 2430, 227, 'what sense are they so? To answer', ''),
          (140, 2476, 275, '75 Above, 9/618.', '75 '),
          (169, 2347, 340, '% Read kalām for kalā.', '% '),
          (174, 1809, 349, '\\[illegible\\] Here vidyā is referred to', ''),
          (249, 2262, 481, '#1 Ibid. 39.', '#1 '),
          (255, 2661, 494, '+ See above, 9/233.', '+ '),
          (259, 2522, 502, '5? karaṇapūrvikā', '5? '),
          (264, 2523, 510, '510 Read \\[illegible\\] for cāmsa-.', '510 '),
          (274, 2453, 526, '5% MV 1/31.', '5% ')]
for pg, y, n, exact, garb in MANUAL:
    rows = [r for r in rows if not (r['pdf'] == pg and abs(r['y'] - y) <= 12)]
    hit = []
    for q in (pg, pg + 1, pg - 1):
        if q not in blocks: continue
        nid, a, b = blocks[q]
        for i in range(a, b + 1):
            if exact in texts[nid][i]: hit.append((nid, i, texts[nid][i].index(exact), q))
    assert len(hit) == 1, (pg, n, exact, hit)
    rows.append({'pdf': pg, 'y': y, 'tok': garb.strip(), 'num_ocr': str(n), 'target': '', 'ocr': 'MANUAL: ' + exact[:60], 'score': 1.0,
                 'match': hit[0], 'manual_drop': len(garb), 'manual_n': n})
rows.sort(key=lambda r: (r['pdf'], r['y']))
# numbering (DP): each start is either footnote v (v > the previous start's number; a gap = footnotes whose start was not
# found, cost 0.6 each) or a false start (skipped, cost 0.8); an OCR'd number that disagrees costs 1 (a one-digit reading
# for v >= 10 counts as no reading); real labels are fixed.
for r in rows:
    r['real'] = None
    if r['match']:
        nid, i, c, pdf = r['match']; l = texts[nid][i]
        m = REAL.match(l)
        if m and c <= len(m.group(0)) + 40: r['real'] = int(m.group(1))
# the lead's decisions on the page images (28 Oct 2026): (pdf, start of the OCR line) -> True (a footnote start) / False (not one)
OVERRIDE = {(81, "'°° Kiranatantra"): True, (81, '332 (330cd'): False, (174, '234 n 326'): False}
for r in rows:
    r['force'] = next((v for (pg, pre), v in OVERRIDE.items() if r['pdf'] == pg and r['ocr'].startswith(pre)), None)
    if r.get('manual_n'): r['force'] = True
# PDF pages scanned twice (vol. 6: PDF 263-264 repeat PDF 261-262, printed pp. 244-245): their starts are kept out of the
# numbering and take the numbers of the source page's starts, in order; a copy in the same note as its source is not made.
DUP = {263: 261, 264: 262}
allrows = rows; rows = [r for r in allrows if r['pdf'] not in DUP]
INF = 1e9; N = len(rows); MAXN = 700
def mis(r, v):
    o = r['num_ocr']
    if not o.isdigit(): return 0.15
    if v >= 10 and len(o) == 1: return 0.15
    return 0.0 if int(o) == v else 1.0
cost = [[INF] * (MAXN + 1) for _ in range(N + 1)]; back = [[None] * (MAXN + 1) for _ in range(N + 1)]
cost[0][0] = 0
for i, r in enumerate(rows):
    for m in range(MAXN + 1):
        c0 = cost[i][m]
        if c0 >= INF: continue
        if not r['real'] and r['force'] is not True and c0 + 0.8 < cost[i + 1][m]: cost[i + 1][m] = c0 + 0.8; back[i + 1][m] = (m, None)
        for v in range(m + 1, min(MAXN, m + 5) + 1):
            if r['force'] is False: break
            if r['real'] and v != r['real']: continue
            c = c0 + 0.6 * (v - m - 1) + (0 if r['real'] else mis(r, v))
            if c < cost[i + 1][v]: cost[i + 1][v] = c; back[i + 1][v] = (m, v)
m = min(range(MAXN + 1), key=lambda v: cost[N][v])
for i in range(N, 0, -1):
    pm, v = back[i][m]; rows[i - 1]['n'] = v; m = pm
for dp, sp in DUP.items():
    cp = [r for r in allrows if r['pdf'] == dp]; src = [r for r in rows if r['pdf'] == sp and r.get('n') is not None]
    for j, r in enumerate(cp):
        r['n'] = src[j]['n'] if j < len(src) else None; r['dup_of'] = sp
rows = allrows
prev = 0
for r in rows:
    if r.get('dup_of'):
        r['flags'] = ['repeat of PDF %d (the same printed page scanned twice): copy of footnote %s' % (r['dup_of'], r['n'])]
        if r['match'] and r['n'] is not None and blocks.get(r['dup_of'], [None])[0] == r['match'][0]:
            r['flags'].append('the copy is in the same note as its source: left plain'); r['n_copy'] = r['n']; r['n'] = None
        continue
    flags = []
    if r['n'] is None: flags.append('taken as a false start (not a footnote)'); r['flags'] = flags; continue
    if r['n'] > prev + 1: flags.append('footnote(s) %s not found before this one' % ', '.join(str(x) for x in range(prev + 1, r['n'])))
    o = r['num_ocr']
    if o.isdigit() and not (r['n'] >= 10 and len(o) == 1) and int(o) != r['n']: flags.append('ocr %s, given %d' % (o, r['n']))
    if not r['match']: flags.append('no line in the note matched (score %.2f)' % r['score'])
    prev = r['n']; r['flags'] = flags
# write the numbered notes
edits = {}
for r in rows:
    if not r['match'] or r.get('real') or r.get('n') is None: continue
    nid, i, c, pdf = r['match']; edits.setdefault((nid, i), []).append((c, r))
done = []
for (nid, i), lst in edits.items():
    l = texts[nid][i]
    for c, r in sorted(lst, key=lambda x: -x[0]):
        if r.get('manual_n'):
            if r['n'] != r['manual_n']: r['flags'].append('MANUAL start numbered %s, not %s' % (r['n'], r['manual_n']))
            k = r['manual_drop']; r['dropped'] = l[c:c + k].strip(); l = l[:c] + l[c + k:]
            pre = l[:c].rstrip()
            if not pre.strip(): l = '%d\\. %s' % (r['n'], l[c:]); r['how'] = 'paragraph start'
            else: l = pre + '\n\n' + '%d\\. %s' % (r['n'], l[c:]); r['how'] = 'split from line'
            r['line'] = i + 1; r['note'] = nid; continue
        ill = False
        while c > 0 and l[:c].rstrip().endswith('\\[illegible\\]'):   # ch09: the placeholder(s) before a start stay with the footnote
            c = l[:c].rstrip().rfind('\\[illegible\\]'); ill = True
        if ill: r['flags'].append('starts with the \\[illegible\\] placeholder before it')
        # ch09: where the image's footnote begins with IP (Isvarapratyabhijna), which the OCR reads as '7', '7?', '7P' or a
        # Devanagari letter, the last garble-like token before the text is that word, not the superscript: it is kept.
        words0 = (r['ocr'].split(' ', 2) + ['', ''])[1]
        ipfirst = bool(re.match(r'^[TIĪ]Pv?$', words0))
        def lead(t): return droppable(t) or t in LEADDROP
        if c == 0:
            rest = l; dr = []
            for _ in range(2):
                m = re.match(r'(\S+)\s+', rest)
                if m and lead(m.group(1)) and not REAL.match(rest): dr.append(m.group(1)); rest = rest[m.end():]
                else: break
            if ipfirst and dr and not re.match(r'^([TIĪ]Pv?\b|\\\[illegible)', rest): rest = dr.pop() + ' ' + rest; r['flags'].append('IP: kept the token before the text')
            r['dropped'] = ' '.join(dr)
            l = '%d\\. %s' % (r['n'], rest); r['how'] = 'paragraph start'
        else:
            pre = l[:c].rstrip(); tokm = re.search(r'(\s|^)(\S+)$', pre); drop = []
            if tokm and droppable(tokm.group(2)):
                drop = [tokm.group(2)]; pre = pre[:tokm.start(2)].rstrip()
            elif tokm and not ill and re.search(r'[A-Za-z]', tokm.group(2)) and not re.search(r'[.,;:!?’”)\]]$', tokm.group(2)):
                r['how'] = 'not applied'; r['flags'].append('start not made: the word before it (%s) may be part of it' % tokm.group(2)); continue
            rest = l[c:]; pre_drop = len(drop)
            for _ in range(2):
                m2 = re.match(r'(\S+)\s+', rest)
                if m2 and lead(m2.group(1)): drop.append(m2.group(1)); rest = rest[m2.end():]
                else: break
            if ipfirst and drop and not re.match(r'^([TIĪ]Pv?\b|\\\[illegible)', rest):
                if len(drop) > pre_drop: rest = drop.pop() + ' ' + rest
                else: c = tokm.start(2); rest = l[c:]; drop.pop()
                r['flags'].append('IP: kept the token before the text')
            r['dropped'] = ' '.join(drop); l = l[:c] + rest
            if not pre.strip(): l = '%d\\. %s' % (r['n'], l[c:]); r['how'] = 'paragraph start'
            else: l = pre + '\n\n' + '%d\\. %s' % (r['n'], l[c:]); r['how'] = 'split from line'
        r['line'] = i + 1; r['note'] = nid
    texts[nid][i] = l
for nid, p in notes:
    open(os.path.join(outdir, nid + '.num.md'), 'w', encoding='utf-8').write('\n'.join(texts[nid]))
json.dump(rows, open(os.path.join(outdir, 'ch09-map.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('starts', len(rows), 'matched', sum(1 for r in rows if r['match']), 'real', sum(1 for r in rows if r.get('real')),
      'split', sum(1 for r in rows if r.get('how') == 'split from line'), 'flagged', sum(1 for r in rows if r['flags']), 'last', rows[-1].get('n'))
for r in rows:
    if r['flags'] or not r['match']: print(' ', r['pdf'], r.get('n'), r['ocr'][:40], '|', '; '.join(r['flags']))
