# packet_ch2.py (28 Oct 2026): a page reader's folder for part of a Chapter Two note: packet.py's note.txt and pages.txt,
# restricted to a range of PDF pages, plus every page of the range (also those with no definition: carried-over text),
# and what the Chapter Two pre-pass did on each page (ch2-map.json).
# Usage: packet_ch2.py ID PDF FIRST LAST OUTDIR
import sys, os, json, subprocess, re
from PIL import Image, ImageOps
nid, pdf, a, b, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
H = '/home/claude/dyfn'; os.makedirs(out, exist_ok=True)
subprocess.run(['python3', f'{H}/scripts/packet.py', f'{H}/work/{nid}', pdf, out + '/_full'], check=True, capture_output=True)
pt = open(out + '/_full/pages.txt', encoding='utf-8').read().split('\n')
R = json.load(open(f'{H}/work/{nid}/pre.json', encoding='utf-8'))
M = json.load(open(f'{H}/ch2/num/ch2-map.json', encoding='utf-8'))
keep, cur = [], None
for l in pt:
    m = re.match(r'^PDF (\d+) ', l)
    if m: cur = int(m.group(1))
    if cur is not None and a <= cur <= b: keep.append(l)
have = {int(re.match(r'^PDF (\d+) ', l).group(1)) for l in keep if l.startswith('PDF ')}
for pg, lab, ml in R['pages_all']:
    if a <= pg <= b and pg not in have: keep.append('PDF %d (printed p. %s), marker line %d: no footnote defined here by the script (look for carried-over footnote text, or a footnote start the script missed)' % (pg, lab, ml))
def pdfnum(l): m = re.match(r'^PDF (\d+) ', l); return int(m.group(1)) if m else None
# keep the blocks in page order
blocks, cb = {}, None
for l in keep:
    if pdfnum(l) is not None: cb = pdfnum(l); blocks.setdefault(cb, [])
    blocks[cb].append(l)
lines = []
for pg in sorted(blocks):
    lines += blocks[pg]
    for r in M:
        if r['pdf'] != pg: continue
        what = ('real before tonight' if r.get('real') else ('made definition %d (%s)' % (r['n'], r.get('how')) if r.get('how') in ('paragraph start', 'split from line') else ('NOT MADE' if r.get('n') else 'taken as no footnote')))
        lines.append('  pre-pass: image start «%s» -> %s%s' % (r['ocr'][:50], what, ('; ' + '; '.join(r['flags'])) if r['flags'] else ''))
head = [l for l in pt if l and not l.startswith('PDF ') and not l.startswith('  ')]
open(out + '/pages.txt', 'w', encoding='utf-8').write('\n'.join(head + ['', 'Your pages: PDF %d-%d.' % (a, b), ''] + lines) + '\n')
os.replace(out + '/_full/note.txt', out + '/note.txt')
for k in range(a, b + 1):
    dst = os.path.join(out, 'p-%03d.png' % k)
    src = out + '/_full/p-%03d.png' % k
    if os.path.exists(src): os.replace(src, dst); continue
    tmp = os.path.join(out, '_t')
    subprocess.run(['pdftoppm', '-f', str(k), '-l', str(k), '-r', '200', '-gray', '-png', '-singlefile', pdf, tmp], check=True)
    im = Image.open(tmp + '.png').convert('L'); bb = ImageOps.invert(im).point(lambda v: 255 if v > 60 else 0).getbbox()
    if bb: im = im.crop((max(0, bb[0] - 12), max(0, bb[1] - 12), min(im.width, bb[2] + 12), min(im.height, bb[3] + 12)))
    im.save(dst, optimize=True); os.remove(tmp + '.png')
subprocess.run(['rm', '-rf', out + '/_full'])
print(out, len([f for f in os.listdir(out) if f.endswith('.png')]), 'images')
