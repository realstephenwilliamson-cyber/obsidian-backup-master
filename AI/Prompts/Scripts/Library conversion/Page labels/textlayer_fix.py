# textlayer_fix.py (3 Nov 2026, audit corrections, D-06): for a book converted from a BORN-DIGITAL PDF whose printed page number is
# PDF page minus a constant, settle every marker off that constant from the PDF's own text layer, and recompute each chapter
# note's page_range and its index label. Used on The Apostolic Fathers (Roberts; offset 40): 235 markers, 14 ranges, 14 labels
# (pf628-pf630). Two blind readers had confirmed the method on 31 of those pages first (all agreed with the text layer).
#   python3 textlayer_fix.py PDF BOOKFOLDER INDEXNOTE OFFSET FIRST LAST OUT.json
#     BOOKFOLDER: the vault folder of the chapter notes (vault-relative, run from the vault root); chapter notes FIRST..LAST by number.
# A page is accepted only if the LAST standalone number line of `pdftotext -layout` (the bottom-centre folio in CCEL books; a margin
# icon or footnote number may stand before it) equals PDF - OFFSET; any other page stops the script. Writes an edits-job2 spec.
# Scanned (OCR) PDFs: do not use; read the pages instead (read_compare.py).
import glob, json, re, subprocess, sys
pdf, folder, index, off, first, last, out = sys.argv[1], sys.argv[2].rstrip('/') + '/', sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
MRE = re.compile(r'^\*\[(?:p\. ([^\]]+)|PDF (\d+))\]\* \^pg(\d+)\s*$', re.M)
idx = open(folder + index, encoding='utf-8').read(); edits = {}; idx_edits = []
for f in sorted(glob.glob(folder + '* [0-9][0-9] - *.md')):
    n = int(re.search(r' (\d\d) - ', f).group(1))
    if not first <= n <= last: continue
    t = open(f, encoding='utf-8').read(); u = t; E = []
    for m in MRE.finditer(t):
        k = int(m.group(3)); lab = m.group(1) or 'PDF'
        if lab.isdigit() and int(lab) == k - off: continue
        txt = subprocess.run(['pdftotext', '-f', str(k), '-l', str(k), '-layout', pdf, '-'], capture_output=True, text=True).stdout
        nums = [x.strip() for x in txt.splitlines() if re.fullmatch(r'\s*\d{1,4}\s*', x)]
        if not nums or nums[-1] != str(k - off): sys.exit(f'stop: {f} PDF {k} marker {lab} text-layer numbers {nums}')
        o = m.group(0).rstrip() + '\n'; nw = f'*[p. {k - off}]* ^pg{k}\n'; E.append([o, nw]); u = u.replace(o, nw)
    labs = [m.group(1) for m in MRE.finditer(u) if m.group(1)]; want = f'{labs[0]}–{labs[-1]}'
    prl = re.search(r'^page_range:.*$', u, re.M).group(0); cur = prl.split(':', 1)[1].strip().strip('"')
    if cur != want:
        E.append([prl + '\n', f'page_range: "{want}"\n' if '"' in prl else f'page_range: {want}\n'])
        name = f.split('/')[-1][:-3]
        m2 = re.search(r'^- \[\[' + re.escape(name) + r'\|[^\]]*\]\] \(pp\. ' + re.escape(cur) + r'\)$', idx, re.M)
        if m2: idx_edits.append([m2.group(0) + '\n', m2.group(0).replace(f'(pp. {cur})', f'(pp. {want})') + '\n'])
    if E: edits[f] = E
if idx_edits: edits[folder + index] = idx_edits
json.dump({'backup': '.work/backup-<task>-<date>', 'edits': edits}, open(out, 'w'), ensure_ascii=False, indent=1)
print(sum(len(v) for v in edits.values()), 'edits in', len(edits), 'notes')
