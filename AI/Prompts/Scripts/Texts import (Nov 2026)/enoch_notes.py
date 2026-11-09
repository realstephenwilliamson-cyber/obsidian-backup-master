"""enoch_notes.py (9 Nov 2026): writes the 1 Enoch notes (Charles 1917) from enoch_build.py's verses.json and heads.json,
plus the index note, Oesterley's introduction (with its footnotes) and the Pseudepigrapha folder note.
Usage: python3 -I enoch_notes.py <OEBPS dir> <build outdir>   -> <build outdir>/vault/<vault paths>"""
import json, re, os, sys, html, collections
SRC, B = sys.argv[1], sys.argv[2]
V = json.load(open(B + '/verses.json')); H = json.load(open(B + '/heads.json'))
FOLDER = 'Texts/Pseudepigrapha/1 Enoch'
OUT = B + '/vault/'
TODAY = '2026-11-09'
TR = "R. H. Charles, The Book of Enoch (SPCK, Translations of Early Documents, 1917), the translation of his 2nd ed. (Oxford, 1912)"
LIC = "Public domain (Project Gutenberg #77935)"
SRCURL = "https://www.gutenberg.org/ebooks/77935"
ROMS = [(100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
def roman(n):
    s = ''
    for v, r in ROMS:
        while n >= v: s += r; n -= v
    return s
def nm(c): return f'1 Enoch {c:03d}'
def head_text(t):
    t = t.replace('*', '').strip()
    words = t.split(' ')
    if sum(1 for w in words if w.isupper() and len(w) > 2) >= max(2, len(words) // 2):
        SMALL = {'of', 'and', 'the', 'to', 'in', 'on', 'for', 'a'}
        t = ' '.join(w if re.fullmatch(r'[IVXLC]+[.,]?(-[IVXLC]+\.?)?|\(?[IVXLC]+-[IVXLC]+\.\)?', w) else (w.lower() if i and w.lower() in SMALL else w.capitalize()) for i, w in enumerate(words))
    return t.rstrip()
def pr(pages):
    ps = [p for p in pages if isinstance(p, int)]
    return f'{min(ps)}–{max(ps)}' if len(set(ps)) > 1 else str(ps[0])
# source order of verses, for the arrangement notes
order = sorted(((d['order'], int(c), int(v)) for c, vv in V.items() for v, d in vv.items()), key=lambda x: x[0])
def runs(ch):
    seq = [(c, v) for _, c, v in order if c == ch]
    out = []
    for c, v in seq:
        if out and out[-1][1] == v - 1: out[-1][1] = v
        else: out.append([v, v])
    return [f'{a}' if a == b else f'{a}–{b}' for a, b in out]
os.makedirs(OUT + FOLDER, exist_ok=True)
chap_pages = {}
for c in range(1, 109):
    vv = V[str(c)]
    nums = sorted(int(v) for v in vv)
    pages = sorted({p for v in vv.values() for p in v['pages']})
    chap_pages[c] = pr(pages)
    prev = f'[[{nm(c-1)}|← 1 Enoch {c-1}]]' if c > 1 else '—'
    nxt = f'[[{nm(c+1)}|1 Enoch {c+1} →]]' if c < 108 else '—'
    nav = f'{prev} · [[1 Enoch|index]] · {nxt}'
    L = ['---', 'type: text', 'work: "1 Enoch"', 'book: "1 Enoch"', f'chapter: {c}', f'translation: "{TR}"', f'license: "{LIC}"', f'source: "{SRCURL}"',
         f'page_range: "{chap_pages[c]}"', '---', f'# 1 Enoch {c} (Charles)', '', nav, '']
    r = runs(c)
    notes = []
    if r != ([f'1–{nums[-1]}'] if nums[-1] > 1 else ['1']):
        notes.append(f'Charles prints the verses of this chapter in the order {", ".join(r)}; here they stand in numerical order.')
    if c in (91, 92, 93):
        notes.append('Charles prints chapters 91–93 in the order 92.1–5; 91.1–11, 18–19; 93.1–14; 91.12–17 (93.1–10 and 91.12–17 are the Apocalypse of Weeks); here each chapter is in its own numbering.')
    if c == 90:
        notes.append('Charles prints 90.13–15 and 16–18 side by side as doublets.')
    for v in nums:
        d = vv[str(v)]
        for lvl, t in H.get(f'{c}.{v}', []):
            if lvl == 'n': L += [t, '']
            else: L += [('## ' if lvl in '23' else '### ') + head_text(t), '']
        if v == nums[0] and notes:
            L += ['> [!note] Arrangement', '> ' + '\n> '.join(notes), '']; notes = []
        if d.get('note'): L += [f'*{d["note"]}*', '']
        lines = d['lines']
        body = f'**{c}:{v}** ' + '\n'.join(lines) + f' ^{c}-{v}'
        L += [body, '']
    L += [nav, '']
    open(OUT + FOLDER + f'/{nm(c)}.md', 'w', encoding='utf-8').write('\n'.join(L))
# ---- introduction, preface, abbreviations (HTML -> Markdown)
PFX = [f for f in os.listdir(SRC) if re.search(r'77935-h-\d+\.htm\.xhtml$', f)][0].split('77935-h-')[0]
def part(n): return open(os.path.join(SRC, f'{PFX}77935-h-{n}.htm.xhtml'), encoding='utf8').read()
def md(t):
    t = t[t.find('<body'):]; t = t.split('Printed in Great Britain')[0]
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'<span class="x-ebookmaker-pageno" id="Page_([^"]+)"[^>]*></span>', r' *[p. \1]* ', t)
    t = re.sub(r'<a[^>]*href="[^"]*#f(\d+)"[^>]*>\s*(?:<sup>)?\s*\[?\d+\]?\s*(?:</sup>)?\s*</a>', r'[^\1]', t)
    t = re.sub(r'<sup>\s*(\[\^\d+\])\s*</sup>', r'\1', t); t = re.sub(r'<a id="r\d+"\s*/>', '', t)
    def table(m):
        rows = re.findall(r'<tr>(.*?)</tr>', m.group(0))
        out = []
        for r in rows:
            cells = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip() for x in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r)]
            if any(cells): out.append('| ' + ' | '.join(cells) + ' |')
        if out: out.insert(1, '|' + '---|' * (out[0].count('|') - 1))
        return '\n\n' + '\n'.join(out) + '\n\n'
    t = re.sub(r'<table.*?</table>', table, t)
    def tc(x):
        SM = {'of', 'and', 'the', 'to', 'in', 'on', 'for', 'a', 'its', 'their'}
        w = html.unescape(re.sub(r'<[^>]+>', '', x)).strip().split()
        return ' '.join(v.lower() if i and v.lower() in SM else v.capitalize() for i, v in enumerate(w))
    t = re.sub(r'<h[1-4][^>]*>(.*?)</h[1-4]>', lambda m: '\n\n## ' + tc(m.group(1)) + '\n\n', t)
    t = re.sub(r'<i>(.*?)</i>', lambda m: '*' + m.group(1).strip() + '*' if m.group(1).strip() else '', t)
    t = re.sub(r'<b>(.*?)</b>', r'**\1**', t)
    t = re.sub(r'<div class="line[^"]*">', '\n', t)
    t = re.sub(r'</p>|<p[^>]*>|<div class="linegroup">|<div class="lg-container[^"]*">|<br/>', '\n\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
    t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r' *\n *', '\n', t); t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()
pref = md(part(1)); intro = md(part(2)); abbr = md(part(3))
# drop the duplicated title line the source repeats
def dehead(t, h):
    m = re.match(r'(\*\[p\. [^\]]+\]\*)?\s*' + h + r'\s*', t)
    return ((m.group(1) + ' ') if m and m.group(1) else '') + t[m.end():] if m else t
pref = dehead(pref, '## Editors’ Preface'); intro = dehead(intro, '## Introduction').replace('\n## ', '\n### ')
abbr = re.sub(r'\*\[p\. [^\]]+\]\*', '', abbr); abbr = re.sub(r'## Abbreviations, Brackets,[^\n]*\n+', '', abbr).strip()
fn = part(11); fn = fn[fn.find('Footnotes'):]
fns = []
for m in re.finditer(r'<div class="footnote" id="f(\d+)">(.*?)</div>', fn, re.S):
    body = re.sub(r'<span class="label">.*?</span>', '', m.group(2), flags=re.S)
    body = re.sub(r'<i>(.*?)</i>', r'*\1*', body); body = html.unescape(re.sub(r'<[^>]+>', '', body)); body = re.sub(r'\s+', ' ', body).strip()
    fns.append(f'[^{m.group(1)}]: {body}')
used = set(re.findall(r'\[\^(\d+)\]', intro))
INTRO = '1 Enoch - Introduction (Oesterley)'
IL = ['---', 'type: text', 'work: "1 Enoch"', 'book: "1 Enoch"', 'part: introduction', f'translation: "{TR}"', f'license: "{LIC}"', f'source: "{SRCURL}"', '---',
      '# The Book of Enoch: Introduction (W. O. E. Oesterley)', '', '[[1 Enoch|index]] · [[1 Enoch 001|1 Enoch 1 →]]', '', '## Editors’ Preface', '', pref, '', '## Introduction', '', intro, '', *fns, '']
open(OUT + FOLDER + f'/{INTRO}.md', 'w', encoding='utf-8').write('\n'.join(IL))
# ---- index
secs = []  # (level, heading, first chapter)
for c in range(1, 109):
    for v in sorted(int(x) for x in V[str(c)]):
        for lvl, t in H.get(f'{c}.{v}', []):
            if lvl in '23': secs.append((lvl, head_text(t), c, v))
X = ['---', 'type: text-index', 'work: "1 Enoch"', f'translation: "{TR}"', f'license: "{LIC}"', f'source: "{SRCURL}"', f'converted: {TODAY}', 'aliases:', '  - "Book of Enoch"', '  - "Ethiopic Enoch"', '---',
     '# 1 Enoch', '',
     '**Translation:** R. H. Charles, *The Book of Enoch*, with an introduction by W. O. E. Oesterley (London: SPCK, 1917; Translations of Early Documents, Series I: Palestinian Jewish Texts (Pre-Rabbinic)). The Gutenberg text was made from the tenth impression (1962). The editors\' note on the title page says the translation is reprinted from Charles\'s second edition of *The Book of Enoch* (Oxford University Press, 1912).  ',
     f'**Source:** Project Gutenberg eBook #77935 (released 14 February 2026; produced from images at the Internet Archive), {SRCURL}. Public domain in the USA.  ',
     '**Catalog:** [[Charles (tr.) - The Book of Enoch]] · **Introduction:** [[' + INTRO + '|Oesterley\'s introduction and the editors\' preface]]', '',
     f'One note per chapter (108), with a block per verse, so `[[1 Enoch 001#^1-9]]` opens 1 Enoch 1.9. Chapter and verse numbers are Charles\'s, the standard ones. Where Charles prints verses out of their numerical order (91–93, 60.25, a few others) or gives the Ethiopic (*E*) and the Greek of the Gizeh fragment (*Gg*) side by side, the note says so.', '',
     '## Abbreviations, brackets and symbols (Charles)', '', abbr, '', '## Contents', '']
for lvl, t, c, v in secs:
    ind = '' if lvl == '2' else '    '
    X.append(f'{ind}- [[{nm(c)}#^{c}-{v}|{t}]]' if lvl == '3' else f'- **[[{nm(c)}|{t}]]**')
X += ['', '## Chapters', '']
row = []
for c in range(1, 109):
    row.append(f'[[{nm(c)}|{c}]]')
    if c % 12 == 0: X.append(' · '.join(row)); X.append(''); row = []
if row: X.append(' · '.join(row))
open(OUT + FOLDER + '/1 Enoch.md', 'w', encoding='utf-8').write('\n'.join(X) + '\n')
# ---- Pseudepigrapha folder note
P = ['---', 'type: index', '---', '# Pseudepigrapha', '', 'Jewish writings of the Second Temple period outside the Hebrew Bible and the Apocrypha, one folder per work.', '',
     '- [[1 Enoch]]: Charles\'s translation (1917), one note per chapter', '']
open(OUT + 'Texts/Pseudepigrapha/Pseudepigrapha.md', 'w', encoding='utf-8').write('\n'.join(P))
print('notes', len(os.listdir(OUT + FOLDER)), 'footnotes', len(fns), 'used', len(used), 'sections', len(secs))
