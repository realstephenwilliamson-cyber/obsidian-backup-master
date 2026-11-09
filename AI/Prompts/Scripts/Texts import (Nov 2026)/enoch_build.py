"""enoch_build.py (9 Nov 2026): 1 Enoch from Charles's translation (SPCK 1917; Project Gutenberg #77935, EPUB) into
one note per chapter with a block per verse (^C-V), an index note with Oesterley's introduction kept as its own note.
Usage: python3 -I enoch_build.py <unzipped epub OEBPS dir> <outdir>
Writes <outdir>/notes/*.md and <outdir>/report.json (verse counts, gaps, duplicates)."""
import re, html, json, sys, os, collections
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT + '/notes', exist_ok=True)
PFX = [f for f in os.listdir(SRC) if re.search(r'77935-h-\d+\.htm\.xhtml$', f)][0].split('77935-h-')[0]
def part(n): return open(os.path.join(SRC, f'{PFX}77935-h-{n}.htm.xhtml'), encoding='utf8').read()
ROM = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
def rom(s):
    s = s.upper().strip('. '); t = 0
    for i, ch in enumerate(s):
        v = ROM[ch]; t += -v if i + 1 < len(s) and ROM[s[i + 1]] > v else v
    return t
def inline(s):
    s = re.sub(r'<i>(.*?)</i>', lambda m: '*' + m.group(1).strip() + '*' if m.group(1).strip() else '', s, flags=re.S)
    s = re.sub(r'<b>(.*?)</b>', lambda m: '**' + m.group(1).strip() + '**', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s)
def prep(t):
    t = t[t.find('<body'):]
    t = t.split('Printed in Great Britain')[0]
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'(\d{1,3}) ?<i>([a-e])\.</i>', r'\1. <i>\2.</i>', t)  # 6a. -> 6. *a.*
    t = re.sub(r'<abbr title="[^"]*">([IVXLC]+)</abbr>\.', r'<abbr title="x">\1.</abbr>', t)  # LVII</abbr>.
    t = re.sub(r'<span class="x-ebookmaker-pageno" id="Page_(\d+)"[^>]*></span>', '\x01\\1\x01', t)
    t = re.sub(r'<h([234])[^>]*>(.*?)</h\1>', lambda m: '\n\x02' + m.group(1) + re.sub(r'\s+', ' ', inline(m.group(2).replace('<br/>', ' '))).strip() + '\n', t, flags=re.S)
    t = re.sub(r'<abbr title="[^"]*">([IVXLC]+)\.</abbr>', '\x06\\1\x06', t)  # chapter numbers (abbr without class)
    t = re.sub(r'<p class="c01[89]">(\x01\d+\x01)?(?:<abbr class="spell">E</abbr>|<abbr class="spell"/>E)</p>', '\\1\n\x07E\n', t)
    t = re.sub(r'<p class="c01[89]">(\x01\d+\x01)?<abbr class="spell">G<sup>g</sup></abbr></p>', '\\1\n\x07Gg\n', t)
    t = re.sub(r'<p[^>]*>(\[[^<\]]*—<span class="sc">Edd\.</span>\])</p>', lambda m: '\n\x08' + inline(m.group(1)) + '\n', t)
    t = re.sub(r'<div class="group">', '\n\x04', t)
    t = re.sub(r'<div class="line[^"]*">', '\n\x03', t)
    t = re.sub(r'<p[^>]*>', '\n\x05', t)
    t = re.sub(r'</(?:p|div)>', '\n', t)
    return inline(t)
stream = ''.join(prep(part(n)) for n in range(4, 12))
# ---- walk
V = collections.OrderedDict()   # (c, v) -> {'lines': [str], 'pages': [], 'order': k}
heads = collections.defaultdict(list)  # (c, v) -> headings placed before this verse
pending = []; label = ''; vpara = ''; vnext = ''; vstart = None; ch = 0; vs = 0; page = 31; mode = 'p'; order = 0; after_chap = False; log = []
cur = None
def start(c, v):
    global cur, order, pending
    key = (c, v)
    if key in V:
        log.append(('merge', c, v)); cur = V[key]; cur['lines'].append('')
        if pending: heads[key].extend(pending); pending = []
        return
    order += 1
    V[key] = {'lines': [''], 'pages': [page], 'order': order}
    if pending: heads[key[:2]].extend(pending); pending = []
    cur = V[key]
def add(text, newline=False):
    global label
    if cur is None: return
    if newline and cur['lines'][-1].strip(): cur['lines'].append('')
    if label and not cur['lines'][-1].strip():
        text = f'*{label}:* ' + text.lstrip(); label = ''
    cur['lines'][-1] += text
NUM = re.compile(r'(?:(?<=^)|(?<=[\s\x06(“‘"\[]))(\d{1,3})\.\s+')
for raw in stream.split('\n'):
    if not raw.strip(): continue
    if raw.startswith('\x07'):
        vnext = raw[1:].strip()
        if vnext == 'E': vstart = (ch, vs)
        continue
    if raw.startswith('\x08'): pending.append(('n', raw[1:].strip())); continue
    if raw.startswith('\x02'):
        lvl, txt = raw[1], raw[2:].strip()
        if txt: pending.append((lvl, txt))
        mh = re.match(r'([IVXLC]+)\.\s(\d{1,3})(?=[-–,.\s])', txt)
        if mh and lvl in '34':
            ch = rom(mh.group(1)); vs = int(mh.group(2)) - 1; after_chap = False
        elif lvl in '34' and re.match(r'([IVXLC]+)\.\s(?![\d])', txt):
            ch = rom(re.match(r'([IVXLC]+)', txt).group(1)); vs = 0; after_chap = True
        continue
    lead = raw[0] if raw[0] in '\x03\x04\x05' else ''
    s = raw[1:] if lead else raw
    if lead == '\x04': continue
    newline = lead in ('\x03', '\x05')
    if lead == '\x05':
        mode = 'p'; vpara = vnext; vnext = ''
        if vpara:
            label = vpara
            if vpara != 'E' and vstart in V and not NUM.match(re.sub(r'^\x01\d+\x01', '', s).lstrip()):
                cur = V[vstart]; cur['lines'].append(''); newline = False
    if lead == '\x03': mode = 'l'
    # tokens: page markers, chapter markers, verse numbers
    pos = 0; first = True
    toks = re.split(r'(\x01\d+\x01|\x06[IVXLC]+\x06)', s)
    for tk in toks:
        if not tk: continue
        if tk.startswith('\x01'):
            page = int(tk.strip('\x01'))
            if cur is not None and page not in cur['pages']: cur['pages'].append(page)
            continue
        if tk.startswith('\x06'):
            ch = rom(tk.strip('\x06')); vs = 0; after_chap = True; continue
        # split by verse numbers
        i = 0
        for m in NUM.finditer(tk):
            n = int(m.group(1))
            before = tk[i:m.start()]
            at_start = not before.strip() and (newline or after_chap) and not (cur and cur['lines'][-1].strip() and not newline)
            prevtxt = (cur['lines'][-1] if cur else '') + before
            back = n < vs and (ch, n) not in V and (at_start or re.search(r'[.;:!?’”)\]]\s*$', prevtxt))
            sub = n <= vs and (ch, n) in V and re.match(r'\*[a-e]\.\*', tk[m.end():])
            ver = bool(vpara) and (ch, n) in V and n <= vs + 1
            ok = back or sub or ver or (after_chap and n == 1) or n == vs + 1 or (vs < n <= vs + 12 and (at_start or re.search(r'[.;:!?’”)\]—]\s*$', (cur['lines'][-1] if cur else '') + before)))
            if not ok: continue
            carry = ''
            if before.strip() in ('[', '(', '‘', '“', '[(', '(['):
                carry = before.strip(); before = ''
            if before.strip():
                if after_chap: start(ch, 1); vs = 1; after_chap = False
                add(before.strip() if not (cur and cur['lines'][-1]) else before, newline and not cur['lines'][-1].strip() == '')
            vs = n; start(ch, vs); after_chap = False; newline = False
            if vpara: label = vpara
            if carry: add(carry)
            i = m.end()
        rest = tk[i:]
        if rest.strip():
            if after_chap: start(ch, 1); vs = 1; after_chap = False; add(rest.lstrip())
            else: add(rest if (cur and cur['lines'][-1]) else rest.lstrip(), newline)
            newline = False
# ---- clean lines
def joinopen(lines):
    out = []
    for x in lines:
        if out and re.fullmatch(r'[\[(‘“]+', out[-1].strip()): out[-1] = out[-1].strip() + x.lstrip()
        else: out.append(x)
    return out
def tidy(s):
    s = re.sub(r'[ \t\r]+', ' ', s).strip()
    s = s.replace(' ,', ',').replace(' .', '.')
    return s
chapters = collections.defaultdict(dict)
for key, d in V.items():
    c, v = key[0], key[1]
    lines = joinopen([tidy(x) for x in d['lines'] if tidy(x)])
    if len(key) == 3: v = f'{v}-dup{key[2]}'
    chapters[c][v] = {'lines': lines, 'pages': d['pages'], 'order': d['order']}
l6 = chapters[60][6]['lines']
if len(l6) == 2 and l6[1].startswith('5. When the punishment'):
    chapters[60][25] = {'lines': [l6[1][3:]], 'pages': chapters[60][6]['pages'], 'order': chapters[60][6]['order'], 'note': 'Charles prints this verse after 60.6 (numbered 5 in the Gutenberg text).'}
    chapters[60][6]['lines'] = l6[:1]
rep = {'chapters': len(chapters), 'verses': sum(len(x) for x in chapters.values()), 'log': log, 'gaps': {}, 'empty': [], 'maxv': {}}
for c, vv in sorted(chapters.items()):
    nums = sorted(int(v) for v in vv if isinstance(v, int))
    rep['maxv'][c] = nums[-1] if nums else 0
    miss = [n for n in range(1, (nums[-1] if nums else 0) + 1) if n not in nums]
    if miss: rep['gaps'][c] = miss
    for v, d in vv.items():
        if not d['lines']: rep['empty'].append((c, v))
json.dump({str(c): {str(v): d for v, d in vv.items()} for c, vv in chapters.items()}, open(OUT + '/verses.json', 'w'), ensure_ascii=False, indent=0)
json.dump({str(k[0]) + '.' + str(k[1]): [h for h in hs] for k, hs in heads.items()}, open(OUT + '/heads.json', 'w'), ensure_ascii=False, indent=0)
json.dump(rep, open(OUT + '/report.json', 'w'), ensure_ascii=False, indent=1)
print('chapters', rep['chapters'], 'verses', rep['verses'], 'dups', len(log), 'gaps', rep['gaps'], 'empty', rep['empty'][:10])
