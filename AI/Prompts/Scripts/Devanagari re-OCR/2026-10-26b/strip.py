# Remove every text layer from a scanned PDF (BT..ET in page content; OCR form XObjects), keeping the page images byte-identical.
# Usage: python3 strip.py in.pdf out.pdf   (only for PDFs whose visible content is the page image)
import sys, re, pikepdf
pdf = pikepdf.open(sys.argv[1]); nbt = nx = 0
def strip(data):
    global nbt
    out = []; i = 0
    for m in re.finditer(rb'(?<![A-Za-z])BT(?![A-Za-z]).*?(?<![A-Za-z])ET(?![A-Za-z])', data, re.S):
        out.append(data[i:m.start()]); i = m.end(); nbt += 1
    out.append(data[i:]); return b''.join(out)
for pg in pdf.pages:
    res = pg.obj.get('/Resources', {}); xo = res.get('/XObject', {})
    ocr = [k for k, v in xo.items() if str(k).startswith('/OCR-') or (v.get('/Subtype') == '/Form' and b'BT' in v.read_bytes() and b'Do' not in v.read_bytes())]
    c = pg.obj.Contents
    streams = list(c) if isinstance(c, pikepdf.Array) else [c]
    for s in streams:
        d = s.read_bytes(); nd = strip(d)
        for k in ocr: nd = re.sub(re.escape(str(k).encode()) + rb'\s+Do', b'', nd)
        if nd != d: s.write(nd)
    for k in ocr: del xo[k]; nx += 1
pdf.save(sys.argv[2])
print('BT blocks removed', nbt, 'OCR forms removed', nx)
