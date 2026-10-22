# Dhvanyaloka round 2: blocks that still have notes not converted (in the vault now), with their page ranges;
# task files for image readers and the page images (whole pages: they are small).
import sys, os, re, json, glob, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import blocks as BL
VAULT = r'C:\Vaults\Obsidian Vault'
FOLDER = os.path.join(VAULT, r'Library\Trika\The Dhvanyaloka of Anandavardhana with the Locana (Anandavardhana)')
PDF = os.path.join(VAULT, r'Library\Trika\Anandavardhana - The Dhvanyaloka, with the Locana of Abhinavagupta (1990).pdf')
ids = set()
for f in glob.glob(os.path.join(glob.escape(FOLDER), '*Translation and Notes*.md')):
    ids |= set(re.findall(r'(?m)^\[\^([^\]]+)\]:', open(f, encoding='utf-8').read()))
S = BL.stream(56, 745); blks = BL.blocks(S)
tasks = []
for b in blks:
    if b['letter'] == '?' or not b['frags']: continue
    text, notes = BL.split_block(b)
    m = len(BL.label_chain(notes)) if notes else 0
    calls = {c[2] for c in BL.calls_in(text)}
    have = {int(x.split('-')[-1]) for x in ids if re.match(r'^%s%d[a-z]?-\d+$' % (b['letter'], b['K']), x)}
    want = max([m] + [c for c in calls if c <= 40])
    missing = [n for n in range(1, want + 1) if n not in have]
    if not missing: continue
    pages = sorted({f['K'] for f in b['frags']})
    tasks.append(dict(block='%s%d' % (b['letter'], b['K']), letter=b['letter'], first_page=pages[0], last_page=pages[-1],
                      text_first_words=' '.join(text[0]['toks'][:6]) if text else '', missing=missing, converted=sorted(have)))
allpages = sorted({k for t in tasks for k in range(t['first_page'], t['last_page'] + 1)})
print('blocks', len(tasks), 'notes missing', sum(len(t['missing']) for t in tasks), 'pages', len(allpages))
d = pymupdf.open(PDF); OUT = os.path.join(HERE, 'pages'); os.makedirs(OUT, exist_ok=True)
for K in allpages:
    p = d[K - 1]; z = min(1300 / p.rect.width, 1500 / p.rect.height)
    p.get_pixmap(matrix=pymupdf.Matrix(z, z), colorspace=pymupdf.csGRAY).save(os.path.join(OUT, 'p%03d.jpg' % K), jpg_quality=75)
n = len(tasks); k = 8
for i in range(k):
    part = tasks[i * n // k:(i + 1) * n // k]
    json.dump(part, open(os.path.join(HERE, 'r2task%d.json' % (i + 1)), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('task', i + 1, len(part), 'blocks', sum(len(t['missing']) for t in part), 'notes', len({kk for t in part for kk in range(t['first_page'], t['last_page'] + 1)}), 'pages')
