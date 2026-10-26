# fixlayer.py (26 Oct 2026) with an optional second map (26 Oct 2026, second session): --indic also maps the Latin model's Š š Ŝ ŝ to Ś ś
# and ã ä Ã Ä to ā Ā, for English books on Indian subjects where those letters cannot be meant (checked per book before use).
# Usage: python3 fixlayer2.py in.pdf out.pdf [--indic]
import sys, re, pikepdf, collections
MAP = {0x015F: 0x1E63, 0x015E: 0x1E62, 0x0146: 0x1E47, 0x0145: 0x1E46, 0x021B: 0x1E6D, 0x021A: 0x1E6C, 0x0163: 0x1E6D, 0x0162: 0x1E6C,
       0x0131: 0x0069, 0x013C: 0x1E37, 0x013B: 0x1E36, 0x0157: 0x1E5B, 0x0156: 0x1E5A, 0x0159: 0x1E5B, 0x0158: 0x1E5A}
if '--indic' in sys.argv:
    MAP.update({0x0160: 0x015A, 0x0161: 0x015B, 0x015C: 0x015A, 0x015D: 0x015B, 0x00E3: 0x0101, 0x00E4: 0x0101, 0x00C3: 0x0100, 0x00C4: 0x0100})
cnt = collections.Counter()
def fixhex(m):
    h = m.group(1)
    if len(h) % 4: return m.group(0)
    u = [int(h[i:i + 4], 16) for i in range(0, len(h), 4)]
    v = [MAP.get(c, c) for c in u]
    for x, y in zip(u, v):
        if x != y: cnt[chr(x)] += 1
    return b'<' + ''.join('%04X' % c for c in v).encode() + b'>'
args = [x for x in sys.argv[1:] if not x.startswith('--')]
pdf = pikepdf.open(args[0]); pages = 0
for pg in pdf.pages:
    xo = pg.obj.get('/Resources', {}).get('/XObject', {})
    for k, v in list(xo.items()):
        if not str(k).startswith('/OCR-') or v.get('/Subtype') != '/Form': continue
        f = list(v.Resources.Font.values())[0] if '/Resources' in v and '/Font' in v.Resources else None
        if not f or str(f.get('/BaseFont')) != '/GlyphLessFont': continue
        b = v.read_bytes(); nb = re.sub(rb'<([0-9A-Fa-f]+)>', fixhex, b)
        if nb != b: v.write(nb); pages += 1
pdf.save(args[1])
print('pages', pages, dict(cnt))
