# Decision 7 (26 Oct 2026): after the Latin+san re-OCR, the Latin model writes look-alike letters for IAST ones (ş for ṣ, ņ for ṇ, ț/ţ for ṭ,
# ı for i, ļ for ḷ, ŗ and ř for ṛ). In OCRmyPDF's sandwich layer the text is a GlyphLessFont (Identity-H, CID = Unicode), so the letters are
# replaced in the hex strings of the OCR text XObjects only. Usage: python3 fixlayer.py in.pdf out.pdf
import sys, re, pikepdf, collections
MAP = {0x015F: 0x1E63, 0x015E: 0x1E62, 0x0146: 0x1E47, 0x0145: 0x1E46, 0x021B: 0x1E6D, 0x021A: 0x1E6C, 0x0163: 0x1E6D, 0x0162: 0x1E6C,
       0x0131: 0x0069, 0x013C: 0x1E37, 0x013B: 0x1E36, 0x0157: 0x1E5B, 0x0156: 0x1E5A,
       0x0159: 0x1E5B, 0x0158: 0x1E5A}  # ř Ř for ṛ Ṛ (added 26 Oct after the whole-volume comparison)
cnt = collections.Counter()
def fixhex(m):
    h = m.group(1)
    if len(h) % 4: return m.group(0)
    u = [int(h[i:i + 4], 16) for i in range(0, len(h), 4)]
    v = [MAP.get(c, c) for c in u]
    for a, b in zip(u, v):
        if a != b: cnt[chr(a)] += 1
    return b'<' + ''.join('%04X' % c for c in v).encode() + b'>'
pdf = pikepdf.open(sys.argv[1]); pages = 0
for pg in pdf.pages:
    xo = pg.obj.get('/Resources', {}).get('/XObject', {})
    for k, v in list(xo.items()):
        if not str(k).startswith('/OCR-') or v.get('/Subtype') != '/Form': continue
        f = list(v.Resources.Font.values())[0] if '/Resources' in v and '/Font' in v.Resources else None
        if not f or str(f.get('/BaseFont')) != '/GlyphLessFont': continue
        b = v.read_bytes(); nb = re.sub(rb'<([0-9A-Fa-f]+)>', fixhex, b)
        if nb != b: v.write(nb); pages += 1
pdf.save(sys.argv[2])
print('pages', pages, dict(cnt))
