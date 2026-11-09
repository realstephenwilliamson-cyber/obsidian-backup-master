"""dss_notes.py (9 Nov 2026): notes from dss_parse.py's records.json -> Texts/Qumran/<cave>/DSS <siglum>.md, one per manuscript,
with a block per numbered line (^<col>-<line>, ^f<frag>[c<col>]-<line>), the index note Texts/Qumran/Qumran.md and the catalog note.
Usage: python3 -I dss_notes.py <outdir>"""
import json, re, os, sys, collections
B = sys.argv[1]; R = json.load(open(B + '/records.json')); OUT = B + '/vault/'
TODAY = '2026-11-09'; ROOT = 'Texts/Qumran'
CAT = 'Garcia Martinez, Tigchelaar (eds.) - The Dead Sea Scrolls Study Edition'
PDF = 'Library/Judaica/Garcia Martinez, Tigchelaar (eds.) - The Dead Sea Scrolls Study Edition (1999).pdf'
ED = "F. García Martínez and E. J. C. Tigchelaar (eds.), The Dead Sea Scrolls Study Edition, 2nd ed. (Leiden: Brill, 1999)"
def cave(s):
    m = re.match(r'^(?:pap)?(\d{1,2})Q', s)
    if m: return f'Cave {int(m.group(1))}'
    if s.startswith(('CD', 'CTL')): return 'Cairo Genizah'
    return 'Other'
def name(s): return 'DSS ' + re.sub(r'\s*,\s*', '-', s).replace('/', '-').strip()
def esc(t):
    t = t.replace('<', '\\<').replace('****', '\\*\\*\\*\\*').replace('[[', '[\\[').replace(']]', ']\\]').replace('|', '\\|')
    t = re.sub(r'\x01(\d+)\x01', r'*[p. \1]*', t)
    return re.sub(r'\s+', ' ', t).strip()
def join(lines):
    s = ''
    for l in lines:
        l = l.strip()
        if not l: continue
        if s.endswith('-') and re.match(r'[a-z]', l) and re.search(r'[a-z]-$', s): s = s[:-1] + l
        else: s = (s + ' ' + l) if s else l
    return s
R = [r for r in R if r.get('siglum')]
names = {}; used = collections.Counter()
for r in R:
    n = name(r['siglum']); used[n] += 1
    if used[n] > 1: n += f' ({used[n]})'
    names[id(r)] = n
os.makedirs(OUT + ROOT, exist_ok=True)
paths = {}; stats = collections.Counter()
order = list(R)
for i, r in enumerate(order):
    n = names[id(r)]; cv = cave(r['siglum']); p = f'{ROOT}/{cv}/{n}.md'; paths[id(r)] = p
    os.makedirs(OUT + ROOT + '/' + cv, exist_ok=True)
    pg = r['page']; pr = f'{pg}–{max(r["pages"])}' if r.get('pages') and max(r['pages']) > pg else str(pg)
    al = [r['siglum']] + ([r['short']] if r['short'] and r['short'] != r['siglum'] else []) + ([r['merged']] if r.get('merged') else [])
    fm = ['---', 'type: text', 'work: "Dead Sea Scrolls"', f'manuscript: "{r["siglum"]}"', f'title: "{r["title"].replace(chr(34), "")}"', f'location: "{cv}"',
          f'edition: "{ED}"', f'page_range: "{pr}"', 'aliases:'] + [f'  - "{a}"' for a in al] + ['---']
    prv = names[id(order[i - 1])] if i else None; nxt = names[id(order[i + 1])] if i + 1 < len(order) else None
    nav = (f'[[{prv}|← {order[i-1]["siglum"]}]] · ' if prv else '') + '[[Qumran|index]]' + (f' · [[{nxt}|{order[i+1]["siglum"]} →]]' if nxt else '')
    L = fm + [f'# {r["siglum"]}' + (f' ({r["short"]})' if r['short'] else '') + f' · {r["title"]}', '', nav, '']
    if r.get('merged'): L += [f'*The edition prints {r["siglum"]} and {r["merged"]} under one heading; both are here.*', '']
    bib = join(r.get('even_head', []) + r.get('odd_pre', []))
    if bib: L += ['> [!info]- Edition, photographs, parallels and bibliography', '> ' + esc(bib), '']
    L += [f'*Study Edition, pp. {pr} (the Hebrew or Aramaic on the left-hand pages, in the PDF).*', '']
    if r.get('biblical'):
        L += ['| Fragment | Text |', '|---|---|'] + [f'| {esc(a)} | {esc(b)} |' for a, b in r['biblical']] + ['']; stats['biblical'] += 1
    secs = r.get('sections', [])
    for s in secs:
        L += [f'### {esc(s["label"])}', '']
        if s['pre']: L += [esc(s['pre']), '']
        for (ln, ln2, txt) in s['lines']:
            lab = f'{ln}–{ln2}' if ln2 else str(ln)
            L += [f'**{lab}** {esc(txt)} ^{s["key"]}-{ln}', '']; stats['lines'] += 1
    if not secs and not r.get('biblical'):
        L += [f'> [!note] No English here', f'> The conversion found no translation or list of contents for this manuscript. For biblical manuscripts the edition lists fragments and verses only, and many small or unclassified fragments have no translation; see the Study Edition, p. {pr}.', '']; stats['empty'] += 1
    L += [nav, '']
    open(OUT + p, 'w', encoding='utf-8').write('\n'.join(L))
# index
by = collections.defaultdict(list)
for r in order: by[cave(r['siglum'])].append(r)
def ck(c): return (0, int(c.split()[1])) if c.startswith('Cave') else (1, c)
X = ['---', 'type: text-index', 'work: "Dead Sea Scrolls"', f'edition: "{ED}"', f'converted: {TODAY}', 'aliases:', '  - "Dead Sea Scrolls"', '  - "DSS"', '---', '# Qumran',
     '', f'The Dead Sea Scrolls in the English of García Martínez and Tigchelaar, *The Dead Sea Scrolls Study Edition* (2nd ed., Brill, 1999): one note per manuscript, in the order of the edition, by cave. Catalog: [[{CAT}]].', '',
     'Each numbered line of the translation has its own block: a column as `^<column>-<line>` (`[[DSS 1QS#^3-13]]` is 1QS col. iii 13; `[[DSS CD-A#^6-19]]` is CD vi 19), a fragment as `^f<fragment>-<line>`, with `c<column>` for a column of a fragment (`[[DSS 4Q521#^f2c2-12]]` is 4Q521 frag. 2 col. ii 12). Only the English is here; the Hebrew and Aramaic stand on the left-hand pages of the edition, in the PDF. Biblical manuscripts, which the edition does not translate, list their fragments and verses.', '',
     '## Key to symbols in the translation (the edition, p. xxiii)', '',
     '- `] XXX [` legible text of varying degrees of certainty, preserved in the manuscript', '- `[XXX]` text restoration, sometimes minimally preserved in the manuscript',
     '- `] … [` one or more illegible traces or untranslatable readings in the manuscript', '- `[…]` lacuna of unspecified length in the manuscript',
     '- `{XXX}` or `{…}` legible or illegible text erased or corrected by the copyist', '- `<XXX>` text written in the manuscript which should be deleted according to the editors',
     '- `‹XXX›` translation of corrected text', '- *Blank* space left blank in the manuscript', '- `****` four dots in the manuscript to represent the tetragrammaton',
     '- `(XXX)` explanation required for the meaning of the English text', '- `/XXX/` or `/…/` legible or illegible text inserted between the lines by the copyist', '']
for c in sorted(by, key=ck):
    X += [f'## {c}', '']
    X += [f'- [[{names[id(r)]}|{r["siglum"]}]] {r["title"]}' for r in by[c]] + ['']
open(OUT + ROOT + '/Qumran.md', 'w', encoding='utf-8').write('\n'.join(X))
print(len(order), dict(stats), len(by))
