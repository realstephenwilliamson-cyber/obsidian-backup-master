# dump.py (SDK 1, 3 Nov 2026): PyMuPDF text of every page of the two CCEL PDFs and the notes of the two books, read from disk,
# in the format of the 28 Oct dump (pf525): pdftext.json {when, text: {pdf: {K: text}}, err}, notes.json {path: text}.
# PyMuPDF gives a footnote number, a superscript call or a margin page number as a line of its own; pdf.js (which the ccel-c01b
# scripts were built on) put them on the line they stand on. So text lines whose vertical extents overlap are merged, in x order:
# with a space where there is a gap between them (a footnote number and its text), otherwise as they touch; a small number in
# the right margin is put at the end of the line before it, as pdf.js had it.
# usage: py dump.py VAULT OUTDIR
import sys, os, json, datetime, pymupdf
V, OUT = sys.argv[1], sys.argv[2]
PDFS = ['Library/Christianity/Augustine - Sermon on the Mount, Harmony of the Gospels, Homilies (NPNF1 6).pdf',
        'Library/Christianity/Chrysostom - Homilies on Matthew (NPNF1 10, 1888).pdf']
DIRS = ['Library/Christianity/Sermon on the Mount, Harmony of the Gospels, Homilies (Augustine)/',
        'Library/Christianity/Homilies on Matthew (Chrysostom)/']

def page_text(pg):
    L = []; pend = []
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            s = ''.join(sp['text'] for sp in l['spans'])
            if not s.strip(): continue
            if s.strip().isdigit() and l['bbox'][0] > 520 and max(sp['size'] for sp in l['spans']) < 7:
                # a margin number: pdf.js put it at the end of the line before (at the start of the first line of the page)
                if L: L[-1][2].append((9999, 9999, s.strip()))
                else: pend.append(s.strip())
                continue
            if pend: s = ''.join(pend) + s; pend.clear()
            L.append([l['bbox'][1], l['bbox'][3], [(l['bbox'][0], l['bbox'][2], s)]])
    out = []
    for y0, y1, segs in L:
        if out:
            p = out[-1]; ov = min(p[1], y1) - max(p[0], y0)
            if ov > 0.5 * min(p[1] - p[0], y1 - y0):
                p[2] += segs; p[0] = min(p[0], y0); p[1] = max(p[1], y1); continue
        out.append([y0, y1, list(segs)])
    lines = []
    for y0, y1, segs in out:
        segs.sort(key=lambda x: x[0]); s = ''; px1 = None
        for i, (x0, x1, t) in enumerate(segs):
            if i and x0 < 9999 and x0 - px1 > 1 and not s.endswith(' ') and not t.startswith(' '): s += ' '
            s += t; px1 = x1
        lines.append(s)
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    T = {}; err = []
    for p in PDFS:
        doc = pymupdf.open(os.path.join(V, p)); T[p] = {}
        for i, pg in enumerate(doc):
            try: T[p][str(i + 1)] = page_text(pg)
            except Exception as e: err.append(f'{p} {i+1}: {e}')
        print(p.split('/')[-1], len(doc))
    json.dump({'when': datetime.datetime.now().isoformat(), 'text': T, 'err': err}, open(os.path.join(OUT, 'pdftext.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    N = {}
    for d in DIRS:
        for f in sorted(os.listdir(os.path.join(V, d))):
            if f.endswith('.md'):
                with open(os.path.join(V, d, f), encoding='utf-8', newline='') as fh: N[d + f] = fh.read()
    json.dump(N, open(os.path.join(OUT, 'notes.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('notes', len(N), 'errors', len(err))
