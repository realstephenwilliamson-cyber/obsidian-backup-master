# packet.py (27 Oct 2026, Dyczkowski footnotes night 1): builds a page reader's folder for one note from prepass.py's output.
# Usage: packet.py PREDIR PDF OUTDIR  -> OUTDIR/note.txt (pre.md with line numbers), OUTDIR/pages.txt (per PDF page with
# footnotes: its marker line, the definitions on it, the body lines, the definitions' lines, hints), OUTDIR/p-KKK.png (200 dpi,
# greyscale, margins trimmed) for those pages.
import sys, json, os, re, subprocess
from PIL import Image, ImageOps
pre, pdf, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
R = json.load(open(os.path.join(pre, 'pre.json'), encoding='utf-8'))
P = open(os.path.join(pre, 'pre.md'), encoding='utf-8').read().split('\n')
open(os.path.join(out, 'note.txt'), 'w', encoding='utf-8').write(open(os.path.join(pre, 'pre-numbered.txt'), encoding='utf-8').read())
# hints: marks that the OCR often makes of a superscript (straight quotes, ?, \*, °, ™, ®, », digits glued to a word),
# and a closing curly quote with no opening one before it in the same paragraph
H1 = re.compile(r'(?<=[^\s(\[])(\?|\'|"|\\\*|°|™|®|»|«|\^)(?=[\s,.;:)\]]|$)')
H2 = re.compile(r'(?<=[^\W\d_])(\d{1,3})(?=[\s,.;:)\]]|$)')
H3 = re.compile(r'(?<=\S)(”|’)')
def hints(s):
    h = []
    for m in H1.finditer(s):
        if m.group(1) == '?' and re.search(r'\b(what|why|how|who|whom|which|where|when|is|are|can|does|do)\b[^.?!]{0,80}$', s[:m.start()], re.I): continue
        h.append((m.start(), m.end()))
    for m in H2.finditer(s): h.append((m.start(), m.end()))
    for m in H3.finditer(s):
        opener = '‘' if m.group(1) == '’' else '“'
        before = s[max(0, m.start() - 400):m.start()]
        if before.count(opener) <= before.count(m.group(1)) and not (m.group(1) == '’' and m.end() < len(s) and s[m.end()].isalpha()):
            h.append((m.start(), m.end()))
    return [s[max(0, a - 30):b + 2] for a, b in sorted(h)]
lines = []
pages = R['pages']
for p in pages:
    defs = ', '.join('%d (line %d)' % (d['n'], d['line']) for d in p['defs'])
    body = p['body']
    rng = ('%d-%d' % (body[0], body[-1])) if body else 'none'
    lines.append('PDF %d (printed p. %s), marker line %d: footnotes defined here: %s' % (p['pdf'], p['label'], p['marker_line'], defs or 'none'))
    lines.append('  body lines %s%s' % (rng, ('; continuation lines indented by the script: ' + ', '.join(map(str, p['cont']))) if p['cont'] else ''))
    if p.get('after_defs'): lines.append('  non-indented lines after the definitions: ' + ', '.join(map(str, p['after_defs'])))
    hs = []
    for ln in body:
        for h in hints(P[ln - 1]): hs.append('L%d «%s»' % (ln, h))
    if hs: lines.append('  hints (may be garbled calls; not complete, not certain): ' + ' | '.join(hs))
extra = []
if R['fixes']: extra.append('Definition numbers fixed by the script from the sequence: ' + json.dumps(R['fixes']))
if R['flags']: extra.append('Sequence flags (look at these pages closely): ' + json.dumps(R['flags']))
if R['clash']: extra.append('Clashes (left plain by the script): ' + json.dumps(R['clash']))
if R['real_defs_before']: extra.append('Footnotes that were already real before tonight (their calls are in place; check nothing): ' + ', '.join(map(str, R['real_defs_before'])))
open(os.path.join(out, 'pages.txt'), 'w', encoding='utf-8').write('\n'.join(extra + [''] + lines) + '\n')
for p in pages:
    k = p['pdf']; dst = os.path.join(out, 'p-%03d.png' % k)
    if os.path.exists(dst): continue
    tmp = os.path.join(out, '_t')
    subprocess.run(['pdftoppm', '-f', str(k), '-l', str(k), '-r', '200', '-gray', '-png', '-singlefile', pdf, tmp], check=True)
    im = Image.open(tmp + '.png').convert('L')
    bb = ImageOps.invert(im).point(lambda v: 255 if v > 60 else 0).getbbox()
    if bb: im = im.crop((max(0, bb[0] - 12), max(0, bb[1] - 12), min(im.width, bb[2] + 12), min(im.height, bb[3] + 12)))
    im.save(dst, optimize=True); os.remove(tmp + '.png')
print(out, len(pages), 'pages')
