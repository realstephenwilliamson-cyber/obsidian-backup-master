# prepass.py (27 Oct 2026, Dyczkowski footnotes night 1). For one note of the library copy of Dyczkowski's Tantraloka
# (Library/Trika/Tantraloka (Dyczkowski)/), whose footnotes are still plain paragraphs `971\. text` (sometimes `500?\. text`):
#  (a) turns each numbered plain paragraph into a `[^n]: ` definition; a number off the main sequence is fixed from its
#      neighbours when they leave exactly one gap, otherwise left plain and flagged (numbered list items); a number that clashes with a real footnote already in the
#      note is listed and the paragraph left plain;
#  (b) indents (four spaces) the same-page continuation paragraphs: non-numbered paragraphs that follow a definition made here,
#      up to the next definition, page marker or heading;
#  (c) lists, for every PDF page (`*[p. N]* ^pgK`), the footnote numbers whose definitions fall on it, the body lines, and
#      the marks in the body that may be garbled calls (hints only; the page image decides).
# Usage: prepass.py NOTE OUTDIR  -> OUTDIR/pre.md (the note after (a) and (b)), OUTDIR/pre.json (pages, fixes, flags),
#        OUTDIR/pre-numbered.txt (pre.md with line numbers, for the reader).
import sys, re, json, os
note, outdir = sys.argv[1:3]
os.makedirs(outdir, exist_ok=True)
text = open(note, encoding='utf-8').read()
L = text.split('\n')
PLAIN = re.compile(r'^(\d+)(\S{0,2})\\\. ')
REAL = re.compile(r'^\[\^(\d+)\]:')
PAGE = re.compile(r'^\*\[p\. ([^\]]*)\]\* \^pg(\d+)\s*$')
HEAD = re.compile(r'^#{1,6} ')
CALL = re.compile(r'\[\^(\d+)\](?!:)')
fm_end = 0
if L and L[0] == '---':
    for i in range(1, len(L)):
        if L[i] == '---': fm_end = i + 1; break
real_defs = {int(m.group(1)) for l in L if (m := REAL.match(l))}
real_calls = [int(m.group(1)) for l in L for m in CALL.finditer(l)]
# (a) the definitions, in document order (plain and real), and the sequence fix
seq = []  # (line index, number, kind)
for i, l in enumerate(L):
    if i < fm_end: continue
    if (m := PLAIN.match(l)): seq.append([i, int(m.group(1)), 'plain', m.group(0)])
    elif (m := REAL.match(l)): seq.append([i, int(m.group(1)), 'real', None])
fixes, flags = [], []
# the main sequence: the longest chain of definitions whose numbers rise by 1 to 10 at each step (a chain may skip lines);
# a plain paragraph off that chain whose number does not fit between its neighbours (e.g. a numbered list item `1\. ` among
# notes 727-741) is left plain and flagged as an outlier
nseq = len(seq)
best = [1] * nseq; prv = [-1] * nseq
for b in range(nseq):
    for a in range(b):
        if 1 <= seq[b][1] - seq[a][1] <= 10 and best[a] + 1 > best[b]: best[b] = best[a] + 1; prv[b] = a
chain = set()
if nseq:
    k = max(range(nseq), key=lambda i: best[i])
    while k >= 0: chain.add(k); k = prv[k]
outliers = set()
for k in range(nseq):
    if k in chain: continue
    lo = max([seq[a][1] for a in chain if a < k], default=None); hi = min([seq[a][1] for a in chain if a > k], default=None)
    x = seq[k][1]
    fits = (lo is None or x > lo) and (hi is None or x < hi)
    if seq[k][2] == 'plain' and not fits and lo is not None and hi is not None and hi - lo == 2:
        fixes.append({'line': seq[k][0] + 1, 'was': x, 'now': lo + 1}); seq[k][1] = lo + 1
    elif seq[k][2] == 'plain' and not fits:
        outliers.add(seq[k][0]); flags.append({'line': seq[k][0] + 1, 'number': x, 'between': [lo, hi], 'why': 'off the sequence: left plain (a numbered list item, or a garbled number the reader must give)'})
main = [s for k, s in enumerate(seq) if s[0] not in outliers]
for k in range(1, len(main)):
    i, x, kind, _ = main[k]; prev = main[k - 1][1]
    if x != prev + 1: flags.append({'line': i + 1, 'number': x, 'prev': prev, 'why': 'gap of %d before this one (a missing definition, two notes run together, or a new numbering)' % (x - prev - 1) if x > prev else 'out of order'})
seq = main
plain_nums = {}
for i, x, kind, _ in seq:
    if kind == 'plain': plain_nums.setdefault(x, []).append(i + 1)
clash = []
for x, lines in plain_nums.items():
    if x in real_defs: clash.append({'number': x, 'lines': lines, 'why': 'a real footnote [^%d] already exists in the note' % x})
    if len(lines) > 1: clash.append({'number': x, 'lines': lines, 'why': 'two plain paragraphs with this number'})
clash_lines = {l for c in clash for l in c['lines']}
new = list(L)
made = set()
for i, x, kind, head in seq:
    if kind != 'plain' or (i + 1) in clash_lines: continue
    new[i] = '[^%d]: ' % x + L[i][len(head):]
    made.add(i)
# (b) same-page continuations
indented = []
for i in sorted(made):
    j = i + 1
    while j < len(new):
        s = new[j]
        if s.strip() == '': j += 1; continue
        if PAGE.match(s) or HEAD.match(s) or REAL.match(s) or PLAIN.match(s) or s.startswith('    '): break
        new[j] = '    ' + s; indented.append(j + 1); j += 1
# (c) pages
pages = []
cur = None
for i, l in enumerate(new):
    if (m := PAGE.match(l)):
        cur = {'label': m.group(1), 'pdf': int(m.group(2)), 'marker_line': i + 1, 'defs': [], 'body': [], 'cont': [], 'hints': []}
        pages.append(cur); continue
    if cur is None or i < fm_end: continue
    if (m := REAL.match(l)): cur['defs'].append({'n': int(m.group(1)), 'line': i + 1, 'new': i in made}); continue
    if l.startswith('    ') and (i + 1) in indented: cur['cont'].append(i + 1); continue
    if l.strip() and not HEAD.match(l) and not cur['defs']: cur['body'].append(i + 1)
    elif l.strip() and not HEAD.match(l) and cur['defs']: cur.setdefault('after_defs', []).append(i + 1)
GARB = re.compile(r'(?<=[\w\)\].,;:!’”\'"])(\?|”|’|\'|"|\\\*|°|™|®|»|«|\^|\d{1,3})(?=[\s,.;:)\]]|$)')
for p in pages:
    for ln in p['body']:
        s = new[ln - 1]
        for m in GARB.finditer(s):
            if m.group(1).isdigit():
                pre = s[max(0, m.start() - 1):m.start()]
                if not pre.isalpha(): continue   # digits after punctuation are usually verse numbers; only glued digits
            p['hints'].append([ln, s[max(0, m.start() - 25):m.end() + 3]])
R = {'note': os.path.basename(note), 'lines': len(L), 'fm_end': fm_end, 'plain_found': sum(1 for s in seq if s[2] == 'plain'),
     'converted': len(made), 'real_defs_before': sorted(real_defs), 'real_calls_before': real_calls,
     'numbers': [s[1] for s in seq], 'fixes': fixes, 'flags': flags, 'clash': clash, 'indented': indented,
     'pages': [p for p in pages if p['defs'] or p.get('after_defs')], 'pages_all': [[p['pdf'], p['label'], p['marker_line']] for p in pages]}
open(os.path.join(outdir, 'pre.md'), 'w', encoding='utf-8').write('\n'.join(new))
open(os.path.join(outdir, 'pre-numbered.txt'), 'w', encoding='utf-8').write('\n'.join('%d\t%s' % (i + 1, l) for i, l in enumerate(new)))
json.dump(R, open(os.path.join(outdir, 'pre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
nums = R['numbers']
print(json.dumps({'note': R['note'][:60], 'plain': R['plain_found'], 'converted': len(made), 'range': [min(nums), max(nums)] if nums else None,
                  'fixes': len(fixes), 'flags': len(flags), 'clash': len(clash), 'indented': len(indented),
                  'pages_with_defs': len(R['pages'])}, ensure_ascii=False))
