# Finn: notes still standing as paragraphs. The PDF's old OCR layer sets notes in Courier-Oblique with the number in
# the margin; a leftover is such a note number with no definition on its page but a 'N\.' paragraph in the md.
import pymupdf, re, glob, os, json, collections
PDF = glob.glob(r'C:\Vaults\Obsidian Vault\Library\Trika\*Finn*.pdf') + glob.glob(r'C:\Vaults\Obsidian Vault\Library\Trika\KULACUDAMANI*.pdf')
MD = r'C:\Vaults\Obsidian Vault\Library\Trika\The Kulacudamani Tantra and The Vamakesvara Tantra (Finn)'
print('pdf', PDF)
d = pymupdf.open(PDF[0])
pages = {}
for f in sorted(glob.glob(os.path.join(glob.escape(MD), '*.md'))):
    L = open(f, encoding='utf-8').read().split('\n'); K = None
    for i, l in enumerate(L):
        m = re.match(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg(\d+)$', l)
        if m: K = int(m.group(1)); pages[K] = dict(f=os.path.basename(f), lines=[]); continue
        if K: pages[K]['lines'].append(l)
out = {}; tot = collections.Counter()
for K, pg in pages.items():
    if K > d.page_count: continue
    notes = []
    spans = [s for b in d[K - 1].get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans'] if s['text'].strip()]
    rows = []
    for s in sorted(spans, key=lambda s: (round(s['origin'][1]), s['bbox'][0])):
        if rows and abs(s['origin'][1] - rows[-1][0]) < 3: rows[-1][1].append(s)
        else: rows.append([s['origin'][1], [s]])
    for y, sp in rows:
        sp.sort(key=lambda s: s['bbox'][0])
        m = re.fullmatch(r'(\d{1,4})\.?', sp[0]['text'].strip())
        if not m or len(sp) < 2: continue
        rest = sp[1:]; tl = sum(len(s['text']) for s in rest)
        obl = sum(len(s['text']) for s in rest if 'Oblique' in s['font'] or 'Italic' in s['font'])
        if tl and obl > 0.6 * tl and sp[1]['bbox'][0] - sp[0]['bbox'][2] > 4: notes.append(int(m.group(1)))
    text = '\n'.join(pg['lines'])
    defs = set(int(x) for x in re.findall(r'(?m)^\[\^(\d+)', text))
    left = [n for n in notes if n not in defs and re.search(r'(?m)^\s*%d\\\.\s' % n, text)]
    tot['italic notes'] += len(notes); tot['leftover'] += len(left)
    if left: out[K] = dict(f=pg['f'], notes=left)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leftovers.json'), 'w'), indent=0)
print(dict(tot), 'pages', len(out))
