# shypatch.py (26 Oct 2026, third session): patch a converted book's notes for the soft-hyphen fault, page by page.
# usage: shypatch.py BOOK.pdf NOTESDIR DECISIONS.json MODE OUT.json   MODE = "joined" (the notes have every split joined: Sen Sharma)
#        or "hyphened" (every split already a hyphen: Brown after 26 Oct). DECISIONS: {"a|b|c": "HJ", ...} (H keep hyphen, J join, S space).
# For each U+00AD token on PDF page K the decided form replaces the note's current form inside that page's block (marker ^pgK to the next
# marker), only where the note holds exactly as many whole-word occurrences as the page has tokens of that kind and the page prints the
# current form nowhere else; everything else is listed. Writes {path: {oldText, newText}} plus a report.
import sys, re, json, glob, collections
import pymupdf as fitz
pdf, ndir, decf, mode, outf = sys.argv[1:6]
dec = json.load(open(decf, encoding='utf-8'))
d = fitz.open(pdf)
page_toks = collections.defaultdict(collections.Counter); page_plain = {}
for k, pg in enumerate(d, 1):
    txt = pg.get_text().replace('\xa0', ' ')
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            s = ''.join(sp['text'] for sp in l['spans']).replace('\xa0', ' ')
            for m in re.finditer(r"[\w’']+(?:­[\w’']+)+", s): page_toks[k][m.group(0).replace('­', '|')] += 1
    page_plain[k] = re.sub(r"[\w’']+(?:­[\w’']+)+", ' ', txt).replace('­', '')
notes = {p: open(p, encoding='utf-8').read() for p in glob.glob(ndir + '/*.md')}
MK = re.compile(r'^\*\[(?:p\.|PDF) [^\]]+\]\* \^pg(\d+)\s*$', re.M)
blocks = {}   # K -> (path, start, end) character offsets
for p, t in notes.items():
    ms = list(MK.finditer(t))
    for i, m in enumerate(ms): blocks[int(m.group(1))] = (p, m.end(), ms[i + 1].start() if i + 1 < len(ms) else len(t))
new = dict(notes); rep = collections.Counter(); listed = []
def form(tok, code):
    parts = tok.split('|'); s = parts[0]
    for c, b in zip(code, parts[1:]): s += {'H': '-', 'J': '', 'S': ' '}[c] + b
    return s
edits = collections.defaultdict(list)   # path -> [(start, end, old, newstr)]
for k, toks in sorted(page_toks.items()):
    if k not in blocks: listed.append((k, 'no block', list(toks))); continue
    p, s0, s1 = blocks[k]; seg = notes[p][s0:s1]
    groups = collections.defaultdict(list)
    for tok, n in toks.items():
        code = dec.get(tok)
        if code is None: listed.append((k, 'no decision', tok)); continue
        cur = form(tok, ('J' if mode == 'joined' else 'H') * (tok.count('|')))
        tgt = form(tok, code)
        if cur == tgt: rep['unchanged'] += n; continue
        groups[cur].append((tok, n, tgt))
    for cur, g in groups.items():
        tgts = {t for _, _, t in g}; n = sum(x[1] for x in g)
        if len(tgts) > 1: listed.append((k, 'different targets', cur, sorted(tgts))); rep['listed'] += n; continue
        tgt = tgts.pop()
        pat = re.compile(r"(?<![\w’'\-])" + re.escape(cur) + r"(?![\w’'\-])")
        hits = [m for m in pat.finditer(seg)]
        genuine = len(pat.findall(page_plain[k]))
        if genuine or len(hits) != n: listed.append((k, f'note {len(hits)} vs page {n} (+{genuine} plain)', [x[0] for x in g], cur, tgt)); rep['listed'] += n; continue
        for m in hits: edits[p].append((s0 + m.start(), s0 + m.end(), cur, tgt))
        rep['changed'] += n
out = {}
for p, es in edits.items():
    t = notes[p]
    for a, b, o, nw in sorted(es, reverse=True):
        assert t[a:b] == o; t = t[:a] + nw + t[b:]
    out[p] = {'oldText': notes[p], 'newText': t}
json.dump({'notes': out, 'report': dict(rep), 'listed': listed}, open(outf, 'w', encoding='utf-8'), ensure_ascii=False)
print(dict(rep), 'notes changed', len(out), 'listed items', len(listed))
