"""lumpkin_notes.py (9 Nov 2026): writes the Markdown copy of Lumpkin, The Books of Enoch, from lumpkin_build.py's parts,
and its catalog note. Usage: python3 -I lumpkin_notes.py <build outdir>  -> <outdir>/vault/..."""
import json, re, os, sys
B = sys.argv[1]
P = json.load(open(B + '/lumpkin-parts.json'))
FOLDER = 'Library/Biblical-Studies/The Books of Enoch (Lumpkin)'
IDX = 'The Books of Enoch (Lumpkin)'; CAT = 'Lumpkin - The Books of Enoch'; TODAY = '2026-11-09'
OUT = B + '/vault/'; os.makedirs(OUT + FOLDER, exist_ok=True); os.makedirs(OUT + 'Catalog/Biblical-Studies', exist_ok=True)
# split 3 Enoch at its chapter 23
parts = []
for p in P:
    if p['title'] == '3 Enoch':
        i = next(i for i, l in enumerate(p['lines']) if l.startswith('### Chapter 23'))
        # keep the page marker that precedes the heading with the second half
        j = i
        while j > 0 and not p['lines'][j - 1].startswith('*[p.') and j > i - 3: j -= 1
        a = dict(p, title='3 Enoch 1–22C', lines=p['lines'][:i]); b = dict(p, title='3 Enoch 23–48D', lines=p['lines'][i:])
        parts += [a, b]
    else: parts.append(p)
def ascii(s): return s.replace('–', '-')
names = [f'The Books of Enoch {i:02d} - {ascii(p["title"])}' for i, p in enumerate(parts, 1)]
CALL = ('> [!warning] Text from the e-book\n'
        '> The e-book (calibre) carries the print edition\'s running heads and page numbers, removed here, and misreadings of the printed text '
        'such as "IUD 1:14" for "JUD 1:14" and "Joseph 8. Lumpkin". Page markers *[p. N]* give the printed page. Chapter labels missing from the e-book '
        '(1 Enoch 85, 105, 106; 2 Enoch 4, 24, 27) are not supplied.')
def pages_of(lines):
    ps = [int(m.group(1)) for l in lines for m in re.finditer(r'\*\[p\. (\d+)\]\*', l)]
    return ps
prev_last = None
for i, (p, nm) in enumerate(zip(parts, names)):
    lines = [l for l in p['lines'] if not l.startswith('*[front matter')]
    ps = pages_of(lines)
    first = ps[0] if ps else None
    # a part that starts mid-page begins on the previous part's last page
    if lines and not lines[0].startswith('*[p.') and prev_last: first = prev_last
    last = ps[-1] if ps else first
    prev_last = last
    pr = '' if first is None else (f'{first}–{last}' if last != first else str(first))
    nav = (f'[[{names[i-1]}|← previous]] · ' if i else '') + f'[[{IDX}|contents]]' + (f' · [[{names[i+1]}|next →]]' if i + 1 < len(names) else '')
    fm = ['---', 'type: book-chapter', f'work: "[[{CAT}]]"', f'book: "[[{IDX}]]"', f'order: {i+1}', f'page_range: "{pr}"',
          'text_source: "EPUB (Fifth Estate; calibre 5.15), not kept in the vault; running heads and page numbers removed"', f'converted: {TODAY}', '---']
    body = [nav, '', CALL, '', f'# {p["title"]}', ''] + [l + '\n' for l in lines] + [nav, '']
    open(OUT + FOLDER + f'/{nm}.md', 'w', encoding='utf-8').write('\n'.join(fm + body))
X = ['---', 'type: book', f'work: "[[{CAT}]]"', 'title: "The Books of Enoch: A Complete Volume Containing 1 Enoch (The Ethiopic Book of Enoch), 2 Enoch (The Slavonic Secrets of Enoch), 3 Enoch (The Hebrew Book of Enoch)"',
     'author:', '  - Joseph B. Lumpkin', 'pages: 432', 'text_source: "EPUB (Fifth Estate; calibre 5.15), not kept in the vault"', f'converted: {TODAY}', '---',
     f'# The Books of Enoch (Lumpkin)', '', f'Joseph B. Lumpkin, *The Books of Enoch: A Complete Volume Containing 1 Enoch, 2 Enoch, 3 Enoch* (Blountsville, AL: Fifth Estate, 2010; first printing March 2009). Catalog: [[{CAT}]].', '',
     CALL, '', '## Contents', '']
for p, nm in zip(parts, names): X.append(f'- [[{nm}|{p["title"]}]]')
X += ['', 'For 1 Enoch cited by chapter and verse, the vault\'s text is Charles\'s translation: [[1 Enoch]].', '']
open(OUT + FOLDER + f'/{IDX}.md', 'w', encoding='utf-8').write('\n'.join(X))
C = f'''---
title: "The Books of Enoch: A Complete Volume Containing 1 Enoch (The Ethiopic Book of Enoch), 2 Enoch (The Slavonic Secrets of Enoch), 3 Enoch (The Hebrew Book of Enoch)"
subtitle: ""
author:
  - Joseph B. Lumpkin
editor: []
translator: []
year: 2010
publisher: Fifth Estate
series: ""
volume: ""
container: ""
subject:
  - Biblical-Studies
  - Judaica
type: book
language:
  - English
pages: 432
text: searchable
status:
print: false
files:
  - "[[{FOLDER}/{IDX}]]"
aliases:
  - The Books of Enoch (Lumpkin)
---
# The Books of Enoch: A Complete Volume Containing 1 Enoch, 2 Enoch, 3 Enoch

```dataviewjs
await dv.view("Templates/Views/open-pdf")
```

**Checked against the file** on 9 November 2026: the title and copyright pages of the EPUB (Copyright © 2010 Joseph B. Lumpkin; first printing March 2009; Fifth Estate, Blountsville, Alabama; ISBN 9781933580807; Library of Congress Control No. 2009942338). The book's contents give the Introduction from p. 3, 1 Enoch from p. 21, 2 Enoch from p. 219 and 3 Enoch from p. 293; the last printed page is 432.

Kept as notes: [[{IDX}]] in `{FOLDER}`, {len(parts)} notes with the printed page numbers. The EPUB is not in the vault, since Obsidian can't open it; it is in Downloads (*Add to Obsidian*). Its text was taken from the printed book and keeps some misreadings (each note says so).

Lumpkin's 1 Enoch is his own rendering with commentary between the verses; the vault's 1 Enoch for references by chapter and verse is Charles's translation (1917).

**See also:** [[Charles (tr.) - The Book of Enoch]] · [[Davila - Hekhalot Literature in Translation]] (3 Enoch among the Hekhalot texts)
'''
open(OUT + f'Catalog/Biblical-Studies/{CAT}.md', 'w', encoding='utf-8').write(C)
print(names); print([(n, os.path.getsize(OUT + FOLDER + f'/{n}.md')) for n in names])
