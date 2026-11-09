"""lumpkin_build.py (9 Nov 2026): Lumpkin, The Books of Enoch (Fifth Estate, 2009), EPUB (calibre) -> a Markdown copy:
an index note and ten part notes, page markers *[p. N]* ^pgN (N the printed page = EPUB anchor pK - 6), running heads and
page numbers removed, paragraphs split by a page break joined, chapter labels made headings.
Usage: python3 -I lumpkin_build.py <unzipped epub dir> <outdir>"""
import re, html, os, sys, json, collections
SRC, OUT = sys.argv[1], sys.argv[2]
FOLDER = 'Library/Biblical-Studies/The Books of Enoch (Lumpkin)'
IDX = 'The Books of Enoch (Lumpkin)'
CAT = 'Lumpkin - The Books of Enoch'
OFF = 6
tot = ''.join(open(os.path.join(SRC, f'index_split_00{i}.html'), encoding='utf8', errors='ignore').read() for i in range(5))
raw = re.findall(r'<p[^>]*>(.*?)</p>', tot, re.S)
def clean(p):
    p = re.sub(r'<(i|em)>(.*?)</\1>', lambda m: '*' + m.group(2).strip() + '*' if m.group(2).strip() else '', p, flags=re.S)
    p = re.sub(r'<(b|strong)>(.*?)</\1>', lambda m: '**' + m.group(2).strip() + '**' if m.group(2).strip() else '', p, flags=re.S)
    p = html.unescape(re.sub(r'<[^>]+>', '', p))
    return re.sub(r'\s+', ' ', p).strip()
HEAD = re.compile(r'^(Joseph\s*[B8]\.?\s*Lumpkin|The\s+Books\s+of\s+Enoch|J|•|-|—)$', re.I)
items = []   # ('page', K) | ('p', text)
for p in raw:
    for k in re.findall(r'<a id="p(\d+)"', p): items.append(('page', int(k)))
    t = clean(p)
    if t: items.append(('p', t))
# remove running heads and page numbers around page breaks
pages = [i for i, x in enumerate(items) if x[0] == 'page']
drop = set(); trail = {}
for i in pages:
    K = items[i][1]; prevnum = str(K - 1 - OFF)
    # before the break: up to 3 paragraphs that are a head or the page number, or a paragraph ending in the number
    j = i - 1; n = 0
    while j >= 0 and n < 3 and items[j][0] == 'p':
        t = items[j][1]; tn = t.replace(' ', '')
        if tn == prevnum or HEAD.match(t): drop.add(j); j -= 1; n += 1; continue
        m = re.search(r'\s(\d[\d ]{0,4})$', t)
        if m and m.group(1).replace(' ', '') == prevnum: trail[j] = t[:m.start()].rstrip()
        break
    # after the break: a running head
    j = i + 1; n = 0
    while j < len(items) and n < 2 and items[j][0] == 'p' and HEAD.match(items[j][1]): drop.add(j); j += 1; n += 1
# last page's number
out = []
for i, x in enumerate(items):
    if i in drop: continue
    if i in trail: x = ('p', trail[i])
    out.append(x)
# join paragraphs split by a page break
merged = []; joined = 0
for i, x in enumerate(out):
    if x[0] == 'p' and len(merged) >= 2 and merged[-1][0] == 'page' and merged[-2][0] == 'p':
        prev = merged[-2][1]
        if False:  # no joining: the page marker keeps its own paragraph and block id, as in the other library copies
            pg = merged.pop(); merged[-1] = ('p', prev + ' ' + f'*[p. {pg[1] - OFF}]* ' + x[1]); merged.append(('mid', pg[1])); joined += 1; continue
    merged.append(x)
# chapter labels
CH = re.compile(r'^\[?\(?\s*(?:Chapter|CHAPTER)\s+([0-9IVXLCSJl]+)\s*[\]\}J]?\)?\s*(.*)$')
R = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
def rom(s):
    t = 0
    for i, c in enumerate(s):
        v = R[c]; t += -v if i + 1 < len(s) and R[s[i + 1]] > v else v
    return t
# split points: by printed page of known starts (from the EPUB's own table of contents) and 1 Enoch chapter numbers
TOC = [(9, 'Introduction'), (27, '1 Enoch'), (225, '2 Enoch, introduction'), (233, '2 Enoch'), (299, '3 Enoch, introduction'), (306, '3 Enoch')]
book = None; chap = collections.defaultdict(int); parts = []; cur = None; K = 1; rep = collections.Counter(); flagged = []
def newpart(title):
    global cur
    cur = {'title': title, 'lines': [], 'k0': K}; parts.append(cur)
newpart('Front matter')
for x in merged:
    if x[0] == 'page':
        K = x[1]
        for k, t in TOC:
            if K == k:
                book = {'1 Enoch': '1E', '2 Enoch': '2E', '3 Enoch': '3E'}.get(t, book if 'introduction' not in t else None)
                if t == '1 Enoch': newpart('1 Enoch 1–36')
                elif t != '1 Enoch': newpart(t if t != 'Introduction' else 'Introduction')
        mk = f'*[p. {K - OFF}]* ^pg{K - OFF}' if K - OFF >= 1 else f'*[front matter, EPUB page {K}]*'
        cur['lines'].append(mk); cur.setdefault('pages', []).append(K - OFF)
        continue
    if x[0] == 'mid':
        cur.setdefault('pages', []).append(x[1] - OFF); continue
    t = x[1]
    m = CH.match(t)
    if m and book and len(t) < 160:
        tok = m.group(1); exp = chap[book] + 1; n = None
        rest0 = m.group(2).strip(); ms = re.match(r'^-?\s*([A-D])\b\s*(.*)$', rest0)
        suf = ms.group(1) if ms else ''
        if suf: exp = chap[book]  # a lettered part (15B, 22C, 48A-D) may repeat the chapter number
        cands = []
        if tok.isdigit(): cands.append(int(tok))
        if re.fullmatch(r'[IVXLC]+', tok): cands.append(rom(tok))
        for v in (tok.replace('S', '5').replace('l', '1').replace('J', ''), tok.replace('S', '8').replace('l', '1').replace('J', '')):
            if v.isdigit(): cands += [int(v), int(v[:-1]) if len(v) > 1 else -1]
        for c in cands:
            if exp <= c <= exp + 3: n = c; break
        if n is None: flagged.append((book, tok, cands, exp, t[:60])); n = exp
        elif n != exp: flagged.append((book, tok, 'gap', exp, n))
        chap[book] = n; rep[book] += 1
        if book == '1E' and n in (37, 72, 83, 91):
            newpart({37: '1 Enoch 37–71', 72: '1 Enoch 72–82', 83: '1 Enoch 83–90', 91: '1 Enoch 91–108'}[n])
            cur['pages'] = [K - OFF]
        rest = (ms.group(2) if ms else rest0).strip(' -–—')
        cur['lines'].append(f'### Chapter {n}{suf}' + (f'\n\n{rest}' if rest else ''))
        continue
    cur['lines'].append(t)
# split long 3 Enoch into two at chapter 24 if present
res = {'parts': [(p['title'], len('\n\n'.join(p['lines']))) for p in parts], 'chapters': dict(rep), 'flagged': flagged, 'joined': joined, 'dropped': len(drop), 'trail': len(trail)}
json.dump(parts, open(OUT + '/lumpkin-parts.json', 'w'), ensure_ascii=False)
print(json.dumps(res, ensure_ascii=False, indent=0)[:3000])
