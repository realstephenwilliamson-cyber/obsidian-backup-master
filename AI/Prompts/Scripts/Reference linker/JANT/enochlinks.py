"""enochlinks.py (12 Nov 2026): links plain references to 1 Enoch anywhere in the vault outside the Enoch notes (the JANT's italic
*1 En.* C.V form is jantlinks2.py's; this one takes the other forms too, and chapter-only references).
Forms: 1 Enoch / 1 En. / 1 En / I Enoch / I En. (italic or not, e.g. *1 Enoch*, *1 En*.) + C:V or C.V (ranges, ", V" and "; C:V" lists),
or a chapter or chapter range alone (-> the chapter note). 2 and 3 Enoch are left plain (Lumpkin's numbering not checked against the
authors'). Skipped: headings, frontmatter, text inside links or code, index notes ("Index" in the name: page numbers follow the
references), Stephen's own folders (Projects, Journal, Study/Concepts, Study/Hubs). In a table row the link's bar is escaped.
Usage: python3 -I enochlinks.py dump.json enoch_ids.json outdir   (dump: {path: text}; ids: {"1 Enoch 038": ["38-2", ...]})
Writes outdir/proposals.json and outdir/new.json ({path: new text})."""
import json, re, sys, collections
D = json.load(open(sys.argv[1], encoding='utf-8')); IDS = {k: set(v) for k, v in json.load(open(sys.argv[2], encoding='utf-8')).items()}; OUT = sys.argv[3]
OWN = ('Projects/', 'Journal/', 'Study/Concepts/', 'Study/Hubs/')
PRE = re.compile(r'(?<![\w\[|#/^.\\])(?:\*(?:1|I) En(?:och)?\.?\*\.?|(?:1|I) En(?:och|\.)?)\s?(?=\d)')
ITEM = re.compile(r'(\d{1,3})[.:](\d{1,3})([a-d]?)((?:\s?[–-]\s?\d{1,3}(?:[.:]\d{1,3})?[a-d]?)?)')
CHAP = re.compile(r'(\d{1,3})((?:[–-]\d{1,3})?)(?![\d]|[.:,]\d)')
def segments(line):
    prot = [(m.start(), m.end()) for m in re.finditer(r'\[\[[^\]]*\]\]|`[^`]*`|\[[^\]]*\]\([^)]*\)|\^\[[^\]]*\]', line)]
    pos = 0
    for a, b in prot:
        if a > pos: yield pos, a
        pos = b
    if pos < len(line): yield pos, len(line)
def plist(s, i):
    out = []
    while True:
        m = ITEM.match(s, i)
        if m and not re.match(r'\d|[.:]\d', s[m.end():m.end() + 2] or ' '):
            c = int(m.group(1)); out.append((m.start(), m.end(), c, int(m.group(2)))); j = m.end()
            while True:
                m2 = re.match(r'(,\s?)(\d{1,3})([a-d]?)((?:[–-]\d{1,3}[a-d]?)?)(?![\d]|[.:]\d)', s[j:])
                if not m2: break
                a = j + len(m2.group(1)); out.append((a, j + m2.end(), c, int(m2.group(2)))); j = j + m2.end()
        else:
            m = CHAP.match(s, i)
            if not m: break
            if out and not re.match(r'\s?[;,)\]]|\.?\s*$|\.\s', s[m.end():]): break   # a chapter after "; " only when the list goes on or ends there
            out.append((m.start(), m.end(), int(m.group(1)), 0)); j = m.end()
        m3 = re.match(r';\s?(?=\d)', s[j:])
        if m3: i = j + m3.end(); continue
        break
    return out
props, new, skipped = [], {}, collections.Counter()
for p, t in D.items():
    if p.startswith(OWN) or 'Index' in p.rsplit('/', 1)[-1]: skipped['own or index'] += 1; continue
    m0 = re.match(r'---\n.*?\n---\n', t, re.S); b0 = m0.end() if m0 else 0
    lines = t[b0:].split('\n'); changed = False; fence = False
    for k, line in enumerate(lines):
        if line.lstrip().startswith('```'): fence = not fence
        if fence or line.startswith('#') or not line.strip(): continue
        reps = []
        for a, b in segments(line):
            seg = line[a:b]
            for m in PRE.finditer(seg):
                for (x, y, c, v) in plist(seg, m.end()):
                    nm = f'1 Enoch {c:03d}'
                    if nm not in IDS: skipped['no chapter ' + str(c)] += 1; continue
                    lab = seg[x:y]
                    if v and f'{c}-{v}' not in IDS[nm]: skipped['no verse'] += 1; continue
                    tgt = f'{nm}#^{c}-{v}' if v else nm
                    bar = '\\|' if line.lstrip().startswith('|') else '|'
                    reps.append((a + x, a + y, lab, f'[[{tgt}{bar}{lab}]]'))
        if not reps: continue
        nl = line
        for s0, e0, lab, link in sorted(reps, key=lambda r: -r[0]):
            nl = nl[:s0] + link + nl[e0:]
            props.append({'path': p, 'label': lab, 'link': link, 'ctx': line[max(0, s0 - 60):e0 + 15]})
        lines[k] = nl; changed = True
    if changed: new[p] = t[:b0] + '\n'.join(lines)
json.dump(props, open(OUT + '/proposals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump(new, open(OUT + '/new.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('notes', len(new), 'links', len(props), 'skipped', dict(skipped))
