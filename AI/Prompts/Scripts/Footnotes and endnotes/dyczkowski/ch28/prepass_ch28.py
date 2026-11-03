# prepass_ch28.py (2 Nov 2026): prepass_ch2.py adapted for Chapter Twenty-Eight of vol. 10 (notes v10-02 to v10-07):
# the superscript readings come from supnum2.py (num2, template matching; good for 3 digits too), MAXN 700, a one-digit
# misreading costs 0.5, and the lead's decisions on the page images are OVERRIDE (start / not a start) and EXTRA (a start
# the detector missed: (pdf, first words of the TSV line)).
# prepass_ch2.py (28 Oct 2026): the Chapter Two pre-pass. Chapter Two's footnotes (vol. 2 notes 02-03) stand as plain
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
def droppable(t):
    # a garbled superscript number: digits and marks, at most one trailing S/s/l/I; never a parenthesised or
    # punctuated reference ("(122)", "70).", "105.") or a closing quote
    if t in ('TM', '™'): return True
    if '-' in t or '/' in t or '–' in t: return False
    if t.startswith('(') or re.search(r'[).,;:’”\]]$', t) and not re.fullmatch(r'\d{1,3}[!?%#$*]?', t): return False
    if re.search(r'[A-RT-Za-rt-z]', t.replace('l', '').replace('I', '')): return False
    if re.fullmatch(r'[’”\'"]+', t): return False
    return bool(re.search(r'[\d*°©®§!?%#$>™\'"।॥&+€~<=]', t)) and not re.fullmatch(r'[‘“]+', t)
# EXTRA: starts the detector missed, found by the lead on the page images: (pdf, the start of the TSV line's text, number
# as printed or None). The line is looked up in the page's TSV; the garbled first token is dropped as for any start.
EXTRA = [(23, '"The tradition and scripture', 9), (67, 'Read saptakrtvakarane', 129), (83, "'! Abhinava tells us", 161),
         (188, 'Instead of yesar punar', 374), (194, 'Read vitti- for', 394)]
FORCED = {}   # (pdf, start of the OCR line) -> printed number, the lead's reading
import csv
def tsv_line(k, pre):
    L = {}
    for r in csv.DictReader(open('/home/claude/lost/ch28/tsv/p-%03d.tsv' % k, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        if r['level'] != '5' or not r['text'].strip(): continue
        e = L.setdefault((r['block_num'], r['par_num'], r['line_num']), {'t': int(r['top']), 'w': []}); e['t'] = min(e['t'], int(r['top'])); e['w'].append(r['text'])
    for e in L.values():
        if ' '.join(e['w']).startswith(pre): return e['t'], ' '.join(e['w'])
    raise SystemExit('EXTRA not found: %d %s' % (k, pre))
for k, pre, num in EXTRA:
    y, o = tsv_line(k, pre)
    if num: FORCED[(k, ('§ ' + o)[:20])] = num
    S.setdefault(str(k), {'starts': []})['starts'].append({'y': y, 'tok': '§', 'ocr': ('§ ' + o)[:120], 'num2': str(num or ''), 'extra': True})
    S[str(k)]['starts'].sort(key=lambda s: s['y'])
def tsv_right(k, y):
    # the text of a TSV line that starts at the same height to the right (Tesseract cut the superscript off as a line)
    L = {}
    for r in csv.DictReader(open('/home/claude/lost/ch28/tsv/p-%03d.tsv' % k, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        if r['level'] != '5' or not r['text'].strip(): continue
        e = L.setdefault((r['block_num'], r['par_num'], r['line_num']), {'t': int(r['top']), 'w': []}); e['t'] = min(e['t'], int(r['top'])); e['w'].append(r['text'])
    c = [' '.join(e['w']) for e in L.values() if abs(e['t'] - y) <= 8 and ' '.join(e['w']).strip() and not ' '.join(e['w']).strip().isdigit()]
    return c[0] if c else ''
rows = []   # all starts in chapter order
for k in sorted(S, key=int):
    for s in S[k]['starts']:
        t = s['ocr'].split(' ', 1); words = t[1] if len(t) > 1 else ''
        if len(fold(words)) < 5:
            rt = tsv_right(int(k), s['y'])
            if rt: words = rt; s['ocr'] = (s['ocr'] + ' ' + rt)[:120]
        rows.append({'pdf': int(k), 'y': s['y'], 'tok': s['tok'], 'num_ocr': s.get('num2', ''), 'conf': s.get('conf2', 0), 'extra': s.get('extra', False),
                     'sup_ok': s.get('sup_ok'), 'target': fold(words)[:28], 'ocr': s['ocr'][:70]})
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
    if r['pdf'] not in blocks: r['match'] = None; continue
    best = (0, None); cl = []
    for pdf in (r['pdf'], r['pdf'] + 1, r['pdf'] - 1):
        if pdf not in blocks: continue
        nid, a, b = blocks[pdf]; L = texts[nid]
        for i in range(a, b + 1):
            l = L[i]
            if not l.strip() or l.startswith('#') or PAGE.match(l): continue
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
    if best[1]:
        def clean(m):
            nid, i, c, pdf = m; l = texts[nid][i]
            if c == 0: return 2
            tk = l[:c].split()
            return 1 if tk and droppable(tk[-1]) else 0
        near = [x for x in cl if x[0] >= best[0] - 0.12 and x[1][:2] == best[1][:2]]
        near.sort(key=lambda x: (-clean(x[1]), -x[0], x[1][2]))
        best = (best[0], near[0][1]) if near else best
    r['score'] = round(best[0], 3)
    r['amb'] = sorted({(x[1][0], x[1][1]) for x in cl if x[0] >= 0.75})   # every line where the start's words match well
    r['match'] = best[1] if best[0] >= 0.75 else None
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
OVERRIDE = {}   # Chapter Twenty-Eight: filled below by the lead
for r in rows:
    if r['extra']: OVERRIDE[(r['pdf'], r['ocr'][:20])] = True   # (a forced number below replaces it)
OVERRIDE.update(FORCED)
for r in rows:
    r['force'] = next((v for (pg, pre), v in OVERRIDE.items() if r['pdf'] == pg and r['ocr'].startswith(pre)), None)
INF = 1e9; N = len(rows); MAXN = 700
def mis(r, v):
    o = r['num_ocr']
    if not o.isdigit(): return 0.15
    if v >= 10 and len(o) == 1: return 0.15
    if int(o) == v: return 0.0
    sv = str(v)
    if len(o) == len(sv) and sum(a != b for a, b in zip(o, sv)) == 1: return 0.5
    return 1.0
cost = [[INF] * (MAXN + 1) for _ in range(N + 1)]; back = [[None] * (MAXN + 1) for _ in range(N + 1)]
cost[0][0] = 0
for i, r in enumerate(rows):
    for m in range(MAXN + 1):
        c0 = cost[i][m]
        if c0 >= INF: continue
        fnum = r['force'] if type(r['force']) is int else None   # the lead's printed number for this start
        if not r['real'] and r['force'] is None or r['force'] is False:
            if c0 + 0.8 < cost[i + 1][m]: cost[i + 1][m] = c0 + 0.8; back[i + 1][m] = (m, None)
        for v in range(m + 1, min(MAXN, m + 5) + 1):
            if r['force'] is False: break
            if fnum is not None and v != fnum: continue
            if r['real'] and v != r['real']: continue
            c = c0 + 0.6 * (v - m - 1) + (0 if r['real'] else mis(r, v))
            if c < cost[i + 1][v]: cost[i + 1][v] = c; back[i + 1][v] = (m, v)
m = min(range(MAXN + 1), key=lambda v: cost[N][v])
for i in range(N, 0, -1):
    pm, v = back[i][m]; rows[i - 1]['n'] = v; m = pm
prev = 0
for r in rows:
    flags = []
    if r['n'] is None: flags.append('taken as a false start (not a footnote)'); r['flags'] = flags; continue
    if r['n'] > prev + 1: flags.append('footnote(s) %s not found before this one' % ', '.join(str(x) for x in range(prev + 1, r['n'])))
    o = r['num_ocr']
    if o.isdigit() and not (r['n'] >= 10 and len(o) == 1) and int(o) != r['n']: flags.append('ocr %s, given %d' % (o, r['n']))
    if not r['match']: flags.append('no line in the note matched (score %.2f)' % r['score'])
    prev = r['n']; r['flags'] = flags
# MANUAL (the lead, 2 Nov 2026, from the page images and the note): number -> (note, 0-based line, text where the footnote
# begins, garble to drop just before it); None = the print's footnote has no text in the note (no definition made).
MANUAL = {21: ('v10-03', 213, 'Read anyai\\$ for', ''), 136: ('v10-04', 499, 'Dhaniṣthā. 137', '1%'),
          209: ('v10-05', 80, 'The rite of worship (which', '%'), 264: ('v10-05', 1090, 'Read, as the context demands', '%t'),
          295: ('v10-06', 406, 'Literally ‘made of Siva’', 'S'), 307: ('v10-06', 665, 'Abhinava’s commentary on BhG', 'W'),
          424: ('v10-07', 938, '81ज 3/21.', '+\\^'), 236: None, 347: None,
          146: ('v10-04', 602, 'kṣīrābdhimathanodbhūtaviṣanidrāvimūrcchitaḥ | 18', '1%'),
          147: ('v10-04', 602, 'nāgarājaḥ svabhuvane meghakāle sma nāvasat ॥ 114 ॥ cf.', '1'),
          149: ('v10-04', 614, 'nāgar nijajatājūṭa', '19')}
ILL = '\\[illegible\\]'
for r in rows:
    if r.get('n') in MANUAL:
        mm = MANUAL[r['n']]; r['flags'] = [f for f in r['flags'] if not f.startswith('start not made') and not f.startswith('no line')]
        if mm is None: r['match'] = None; r['flags'].append('no text for this footnote in the note (the lead looked)'); continue
        nid, i, sub, drop = mm; l = texts[nid][i]; assert l.count(sub) == 1, (r['n'], sub)
        c = l.index(sub); r['match'] = (nid, i, c, r['pdf']); r['manual_drop'] = drop; r['flags'].append('placed by the lead')
# write the numbered notes
edits = {}
for r in rows:
    if not r['match'] or r.get('real') or r.get('n') is None: continue
    nid, i, c, pdf = r['match']; edits.setdefault((nid, i), []).append((c, r))
done = []
for (nid, i), lst in edits.items():
    l = texts[nid][i]
    for c, r in sorted(lst, key=lambda x: -x[0]):
        if c == 0:
            rest = l; dr = []
            for _ in range(1):   # ch28: one token only ("172 108 x 3", "%5 810 8/6-7ab": the second is text)
                m = re.match(r'(\S+)\s+', rest)
                if m and droppable(m.group(1)) and not REAL.match(rest): dr.append(m.group(1)); rest = rest[m.end():]
                else: break
            r['dropped'] = ' '.join(dr)
            l = '%d\\. %s' % (r['n'], rest); r['how'] = 'paragraph start'
        elif 'manual_drop' in r:
            pre = l[:c].rstrip(); drop = r['manual_drop']
            if drop:
                assert pre.endswith(drop), (r['n'], pre[-20:]); pre = pre[:-len(drop)].rstrip()
            if pre.endswith(ILL): pre = pre[:-len(ILL)].rstrip(); c2 = ILL + ' '
            else: c2 = ''
            r['dropped'] = drop
            if not pre.strip(): l = '%d\\. %s' % (r['n'], c2 + l[c:]); r['how'] = 'paragraph start'
            else: l = pre + '\n\n' + '%d\\. %s' % (r['n'], c2 + l[c:]); r['how'] = 'split from line'
        else:
            pre = l[:c].rstrip(); tokm = re.search(r'(\s|^)(\S+)$', pre); drop = ''
            if pre.endswith(ILL) and not pre[:-len(ILL)].strip():
                l = '%d\\. %s' % (r['n'], l); r['how'] = 'paragraph start'; r['dropped'] = ''; r['line'] = i + 1; r['note'] = nid; continue
            if pre.endswith(ILL):
                # the superscript was read as illegible: the placeholder goes with the new footnote (kept, not dropped)
                pre = pre[:-len(ILL)].rstrip(); r['dropped'] = ''; l = pre + '\n\n' + '%d\\. %s' % (r['n'], ILL + ' ' + l[c:])
                r['how'] = 'split from line'; r['ill'] = True; r['line'] = i + 1; r['note'] = nid; continue
            if tokm and droppable(tokm.group(2)):
                drop = tokm.group(2); pre = pre[:tokm.start(2)].rstrip()
            elif tokm and re.search(r'[A-Za-z]', tokm.group(2)) and not re.search(r'[.,;:!?’”)\]]$', tokm.group(2)):
                r['how'] = 'not applied'; r['flags'].append('start not made: the word before it (%s) may be part of it' % tokm.group(2)); continue
            rest = l[c:]
            for _ in range(0 if drop else 1):   # ch28: one token only ("172 108 x 3", "%5 810 8/6-7ab": the second is text)
                m2 = re.match(r'(\S+)\s+', rest)
                if m2 and droppable(m2.group(1)): drop = (drop + ' ' + m2.group(1)).strip(); rest = rest[m2.end():]
                else: break
            r['dropped'] = drop; l = l[:c] + rest
            if not pre.strip(): l = '%d\\. %s' % (r['n'], l[c:]); r['how'] = 'paragraph start'
            else: l = pre + '\n\n' + '%d\\. %s' % (r['n'], l[c:]); r['how'] = 'split from line'
        r['line'] = i + 1; r['note'] = nid
    texts[nid][i] = l
for nid, p in notes:
    open(os.path.join(outdir, nid + '.num.md'), 'w', encoding='utf-8').write('\n'.join(texts[nid]))
json.dump(rows, open(os.path.join(outdir, 'ch28-map.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('starts', len(rows), 'matched', sum(1 for r in rows if r['match']), 'real', sum(1 for r in rows if r.get('real')),
      'split', sum(1 for r in rows if r.get('how') == 'split from line'), 'flagged', sum(1 for r in rows if r['flags']), 'last', rows[-1].get('n'))
for r in rows:
    if r['flags'] or not r['match']: print(' ', r['pdf'], r.get('n'), r['ocr'][:40], '|', '; '.join(r['flags']))
