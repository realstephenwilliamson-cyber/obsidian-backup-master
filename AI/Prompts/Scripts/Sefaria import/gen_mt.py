# Maimonides (Mishneh Torah, Guide, Eight Chapters, Introduction to the Mishnah) and the Kitzur Shulchan Arukh, from the Sefaria export (22 Oct 2026).
import csv, collections, glob, json, os, re, sys, urllib.parse
sys.path.insert(0, '/home/claude/sef')
from common import to_md, link_refs, link_talmud, verses, parse_tanakh, target, fm, fn_block, checks, BORDER, TAL_SIDES, TAL_BLOCKS

OUT = '/home/claude/ram/out/'; DL = '/home/claude/ram/dl/'; EXPORT = '2026-10-01'
NOTES = {}; STATS = collections.Counter(); REPORT = collections.defaultdict(list)

def nav(prev, index, nxt):
    return (f'← [[{prev}]] · ' if prev else '') + f'[[{index}]]' + (f' · [[{nxt}]] →' if nxt else '')

# ---- Sefaria links for these works ----
TAN = collections.defaultdict(list); TALM = collections.defaultdict(list)
def tal_parse(ref):
    m = re.match(r'^(.+?) (\d+)([ab])(?::(\d+))?', ref)
    return (m.group(1), int(m.group(2)), m.group(3), int(m.group(4)) if m.group(4) else None) if m else None
for f in sorted(glob.glob('/home/claude/ram/links/l*.csv')):
    for r in csv.reader(open(f, encoding='utf-8')):
        if len(r) < 7: continue
        for a, b, cb in ((r[0], r[1], r[6]), (r[1], r[0], r[5])):
            if not re.match(r'^(Mishneh Torah, |Guide for the Perplexed|Kitzur Shulchan Arukh|Eight Chapters|Rambam Introduction to the Mishnah)', a): continue
            if cb == 'Tanakh':
                t = parse_tanakh(b)
                if t: TAN[a].append(t)
            elif cb == 'Talmud':
                k = tal_parse(b)
                if k and (k[0], f'{k[1]}{k[2]}') in TAL_SIDES: TALM[a].append((b, k))

def refs_for(prefix):
    """Tanakh refs linked to any ref that starts with prefix (a unit)."""
    out = []
    for a, ts in TAN.items():
        if a == prefix or a.startswith(prefix + ':') or a.startswith(prefix + ' '): out += ts
    return out

def conf_of(ts):
    s = set()
    for t in ts: s |= verses(t)
    return s

def linkify(txt, ts, st, as_written=True):
    return link_talmud(link_refs(txt, conf_of(ts), st, as_written=as_written), st)

def talmud_item(b, k):
    tr, d, s, seg = k
    # to the line when it has English, else to the side (22 Oct 2026: 3 links pointed at empty segments)
    return f'[[{tr} {d}#^{d}{s}-{seg}|{b}]]' if seg and (tr, f'{d}{s}-{seg}') in TAL_BLOCKS else f'[[{tr} {d}#{d}{s}|{b}]]'

def verse_item(t):
    b, c1, v1, c2, v2 = t
    note = target(b, c1, v1 or 1)
    lab = f'{b} {c1}' + (f':{v1}' if v1 else '') + (f'–{v2}' if v2 and c2 == c1 and v2 != v1 else (f'–{c2}:{v2}' if c2 != c1 and v2 else ''))
    return f'[[{note}#^{c1}-{v1 or 1}|{lab}]]' if note else lab

def margin(unit_refs, label_unit):
    """Margins of a chapter: the Talmud passages and the verses Sefaria links to its halakhot."""
    tal = collections.OrderedDict(); tan = collections.OrderedDict()
    for ref, n in unit_refs:
        for b, k in TALM.get(ref, []): tal.setdefault((b, k), set()).add(n)
        for t in TAN.get(ref, []): tan.setdefault(t, set()).add(n)
    out = []
    def ns(x): x = sorted(i for i in x if i); return (f' ({label_unit[0] if len(x) == 1 else label_unit[1]} ' + ', '.join(map(str, x)) + ')') if x else ''
    if tal: out.append('> [!xref]- In the Talmud\n' + '\n'.join(f'> - {talmud_item(b, k)}{ns(v)}' for (b, k), v in sorted(tal.items(), key=lambda x: (x[0][1][0], x[0][1][1], x[0][1][2], x[0][1][3] or 0))))
    if tan: out.append('> [!torah]- Verses\n' + '\n'.join(f'> - {verse_item(t)}{ns(v)}' for t, v in sorted(tan.items(), key=lambda x: (BORDER[x[0][0]], x[0][1], x[0][2] or 0))))
    return out

def put(path, text):
    NOTES[path] = text

# =========================== Mishneh Torah ===========================
def mishneh_torah():
    order = [t for t in json.load(open('/home/claude/ram/mt_order.json'))]
    order = list(dict.fromkeys(order))
    files = {os.path.basename(p)[:-5]: p for p in glob.glob('/home/claude/ram/mt/*.json')}
    books = {}
    for line in open('/home/claude/ram/mt_files.txt'):
        parts = line.strip().split('/'); books[parts[4]] = parts[3]
    BOOKORDER = ['Introduction', 'Sefer Madda', 'Sefer Ahavah', 'Sefer Zemanim', 'Sefer Nashim', 'Sefer Kedushah', 'Sefer Haflaah', 'Sefer Zeraim', 'Sefer Avodah',
                 'Sefer Korbanot', 'Sefer Taharah', 'Sefer Nezikim', 'Sefer Kinyan', 'Sefer Mishpatim', 'Sefer Shoftim']
    secs = [t for t in order if t in files] + [t for t in files if t not in order]
    secs.sort(key=lambda t: BOOKORDER.index(books[t]))   # stable: Sefaria's order inside each book
    REPORT['mt_not_in_touger'] = [t for t in order if t not in files]
    index = collections.OrderedDict(); allnotes = []
    ver = None
    plan = []
    for title in secs:
        J = json.load(open(files[title])); ver = J['versionTitle']; short = title.replace('Mishneh Torah, ', '')
        t = J['text']; book = books[title]; bi = BOOKORDER.index(book)
        folder = f'Texts/Maimonides/Mishneh Torah/{bi:02d} {book}/Mishneh Torah - {short}/'
        chapters = t if (t and isinstance(t[0], list)) else [t]
        for ci, ch in enumerate(chapters, 1):
            hal = [(hi, h) for hi, h in enumerate(ch, 1) if isinstance(h, str) and h.strip()]
            if not hal: continue
            plan.append((title, short, book, folder, ci, hal, len(chapters), J))
    names = [f'Mishneh Torah - {p[1]} {p[4]:02d}' for p in plan]
    for k, (title, short, book, folder, ci, hal, nch, J) in enumerate(plan):
        name = names[k]; prev = names[k - 1] if k else None; nxt = names[k + 1] if k + 1 < len(names) else None
        fns = []; st = {}; paras = []; unit_refs = []
        for hi, h in hal:
            ref = f'{title} {ci}:{hi}'; unit_refs.append((ref, hi))
            paras.append(f'**{hi}.** ' + linkify(to_md(h, fns), TAN.get(ref, []), st) + f' ^{ci}-{hi}'); STATS['mt_halakhot'] += 1
        fns = [linkify(x, [], st) for x in fns]
        for kk, vv in st.items():
            if isinstance(vv, int): STATS['mt_' + kk] += vv
        d = {'type': 'text', 'work': 'Mishneh Torah', 'author': ['Moses Maimonides'], 'translation': J['versionTitle'], 'translator': ['Eliyahu Touger'],
             'license': J['license'], 'source': f"https://www.sefaria.org/{title.replace(' ', '_')}.{ci}?ven={urllib.parse.quote(J['versionTitle'].replace(' ', '_'))}&lang=en",
             'aliases': [f'{title} {ci}', f'MT {short} {ci}'], 'book': book, 'section': short, 'chapter': ci}
        head = [fm(d), f'# {name}', '', nav(prev, f'Mishneh Torah - {short}', nxt), '', f'*{book} · {short} · Chapter {ci}* · [[Mishneh Torah - {short}]] · [[Mishneh Torah]]']
        mg = margin(unit_refs, ('halakhah', 'halakhot'))
        put(folder + name + '.md', '\n'.join(head) + '\n\n' + ('\n\n'.join(mg) + '\n\n' if mg else '') + '\n\n'.join(paras) + fn_block(fns) + '\n')
        index.setdefault((book, title, short, folder), []).append((name, ci))
        STATS['mt_notes'] += 1
    # section notes and the index
    L = [fm({'type': 'index', 'work': 'Mishneh Torah', 'author': ['Moses Maimonides'], 'translation': ver, 'translator': ['Eliyahu Touger'], 'license': 'CC-BY-NC',
             'source': 'https://www.sefaria.org/texts/Halakhah/Mishneh%20Torah', 'aliases': ['Mishneh Torah index', 'Mishneh Torah (Touger)', 'Yad HaChazakah']}),
         '# Mishneh Torah (Touger)', '',
         f'The *Mishneh Torah* in Rabbi Eliyahu Touger\'s translation (Moznaim), one note per chapter ({STATS["mt_notes"]:,} notes, {STATS["mt_halakhot"]:,} halakhot), following Sefaria\'s structure. Sefaria describes it as a "Legal code written by Maimonides in the 12th century, groundbreaking in its organization and scope." Each halakhah is a block (`^3-9` is chapter 3, halakhah 9), so a link can point to it; Touger\'s notes are the footnotes. At the top of each chapter, collapsed boxes list the Talmud passages and the verses Sefaria links to its halakhot; verse and Talmud references in the text are links.',
         '', '## License and attribution', '', f'- **Translation:** {ver}', '- **Translator:** Eliyahu Touger', '- **License:** CC-BY-NC ("© Published and Copyright by Moznaim Publications. Must obtain written permission from Moznaim Publications for any commercial use. Any use must cite Copyright by Moznaim Publications. Released into the commons with a CC-BY-NC license.", Sefaria\'s version notes)',
         '- **Print edition:** https://moznaim.com/products/mishneh-torah-rambam', f'- **Digital text:** [Sefaria](https://www.sefaria.org/), via the [Sefaria-Export](https://github.com/Sefaria/Sefaria-Export) dataset (export of {EXPORT}).']
    cur = None
    for (book, title, short, folder), items in index.items():
        if book != cur: L += ['', f'## {book}', '']; cur = book
        L.append(f'- [[Mishneh Torah - {short}]] ({len(items)} chapters)')
        rows = [' · '.join(f'[[{n}|{c}]]' for n, c in items[j:j + 10]) for j in range(0, len(items), 10)]
        put(folder + f'Mishneh Torah - {short}.md', '\n'.join([fm({'type': 'index', 'work': 'Mishneh Torah', 'book': book, 'section': short, 'aliases': [title, f'Hilchot {short}', f'Laws of {short}']}),
            f'# Mishneh Torah - {short}', '', f'*{book}* · [[Mishneh Torah]]', '', '## Chapters', ''] + [r + '  ' for r in rows[:-1]] + rows[-1:]) + '\n')
    put('Texts/Maimonides/Mishneh Torah/Mishneh Torah.md', '\n'.join(L) + '\n')

# =========================== Guide for the Perplexed ===========================
def guide():
    f = glob.glob(DL + '*Guide for the Perplexed, English Translation, Friedlander 1903.json')[0]; J = json.load(open(f)); t = J['text']; ver = J['versionTitle']
    base = 'Texts/Maimonides/Guide for the Perplexed/'
    units = []
    for k in ('Letter to R Joseph son of Judah', 'Prefatory Remarks'):
        if t.get(k): units.append((f'Guide for the Perplexed - {k.replace("Letter to R Joseph son of Judah", "Letter to Rabbi Joseph")}', f'Guide for the Perplexed, {k}', t[k], k))
    for p in (1, 2, 3):
        P = t[f'Part {p}']
        if P.get('Introduction'): units.append((f'Guide for the Perplexed {p}.00 - Introduction', f'Guide for the Perplexed, Part {p}, Introduction', P['Introduction'], f'Part {p}, Introduction'))
        for ci, ch in enumerate(P[''], 1):
            if ch and any(isinstance(x, str) and x.strip() for x in ch): units.append((f'Guide for the Perplexed {p}.{ci:02d}', f'Guide for the Perplexed, Part {p} {ci}', ch, f'Part {p}, Chapter {ci}'))
    names = [u[0] for u in units]
    for k, (name, ref, segs, label) in enumerate(units):
        fns = []; st = {}
        ts = refs_for(ref)
        paras = [linkify(to_md(s, fns), ts, st, as_written=False) for s in segs if isinstance(s, str) and s.strip()]
        for kk, vv in st.items():
            if isinstance(vv, int): STATS['guide_' + kk] += vv
        d = {'type': 'text', 'work': 'Guide for the Perplexed', 'author': ['Moses Maimonides'], 'translation': ver, 'translator': ['Michael Friedländer'],
             'license': J['license'], 'source': 'https://www.sefaria.org/' + ref.replace(' ', '_').replace(',_Part_', ',_Part_') + '?ven=' + urllib.parse.quote(ver.replace(' ', '_')) + '&lang=en', 'aliases': [ref]}
        head = [fm(d), f'# {name}', '', nav(names[k - 1] if k else None, 'Guide for the Perplexed', names[k + 1] if k + 1 < len(names) else None), '', f'*{label}* · [[Guide for the Perplexed]]']
        put(base + name + '.md', '\n'.join(head) + '\n\n' + '\n\n'.join(paras) + fn_block(fns) + '\n'); STATS['guide_notes'] += 1
    L = [fm({'type': 'index', 'work': 'Guide for the Perplexed', 'author': ['Moses Maimonides'], 'translation': ver, 'translator': ['Michael Friedländer'], 'license': J['license'],
             'source': 'https://www.sefaria.org/Guide_for_the_Perplexed', 'aliases': ['Guide for the Perplexed index', 'Moreh Nevukhim', 'The Guide']}),
         '# Guide for the Perplexed (Friedländer)', '', f'Maimonides\' *Guide for the Perplexed* in Michael Friedländer\'s translation (1903, public domain), one note per chapter ({len(units)} notes). Sefaria describes it as "Maimonides’ 12th-century philosophical masterwork, written as a letter to his student demonstrating the compatibility of Judaism and philosophy." Verse references are linked where Sefaria links the same verse to that chapter.',
         '', '## License and attribution', '', f'- **Translation:** {ver}', f'- **License:** {J["license"]}', f'- **Version source:** {J.get("versionSource")}', f'- **Digital text:** [Sefaria](https://www.sefaria.org/), via the Sefaria-Export dataset (export of {EXPORT}).', '']
    cur = None
    for name, ref, segs, label in units:
        part = label.split(',')[0]
        if part != cur: L += ['', f'## {part}', '']; cur = part
        L.append(f'- [[{name}]]' + ('' if 'Chapter' not in label else ''))
    put(base + 'Guide for the Perplexed.md', '\n'.join(L) + '\n')

# =========================== Eight Chapters ===========================
def eight_chapters():
    f = glob.glob(DL + '*Eight Chapters__English__The Eight Chapters*')[0]; J = json.load(open(f)); t = J['text']; ver = J['versionTitle']
    base = 'Texts/Maimonides/Eight Chapters/'
    units = [('Eight Chapters - Introduction', 'Eight Chapters, Introduction', t['Introduction'], 'Introduction')] + \
            [(f'Eight Chapters {i}', f'Eight Chapters {i}', ch, f'Chapter {i}') for i, ch in enumerate(t[''], 1) if ch]
    names = [u[0] for u in units]
    for k, (name, ref, segs, label) in enumerate(units):
        fns = []; st = {}
        paras = [linkify(to_md(s, fns), refs_for(ref), st, as_written=False) for s in (segs if isinstance(segs, list) else [segs]) if isinstance(s, str) and s.strip()]
        d = {'type': 'text', 'work': 'Eight Chapters', 'author': ['Moses Maimonides'], 'translation': ver, 'translator': ['Joseph I. Gorfinkle'], 'license': J['license'],
             'source': 'https://www.sefaria.org/' + ref.replace(' ', '_') + '?ven=' + urllib.parse.quote(ver.replace(' ', '_')) + '&lang=en', 'aliases': [ref]}
        put(base + name + '.md', '\n'.join([fm(d), f'# {name}', '', nav(names[k - 1] if k else None, 'Eight Chapters', names[k + 1] if k + 1 < len(names) else None), '', f'*{label}* · [[Eight Chapters]]']) + '\n\n' + '\n\n'.join(paras) + fn_block(fns) + '\n')
        STATS['eight_notes'] += 1
    put(base + 'Eight Chapters.md', '\n'.join([fm({'type': 'index', 'work': 'Eight Chapters', 'author': ['Moses Maimonides'], 'translation': ver, 'translator': ['Joseph I. Gorfinkle'], 'license': J['license'], 'source': 'https://www.sefaria.org/Eight_Chapters', 'aliases': ['Shemonah Perakim', 'Eight Chapters index']}),
        '# Eight Chapters (Gorfinkle)', '', 'Maimonides\' *Eight Chapters* (*Shemonah Perakim*) in Joseph I. Gorfinkle\'s translation, public domain. Sefaria describes it as "Maimonides’ 12th-century philosophical introduction to Pirkei Avot, analyzing the soul, human purpose, and free will." See also [[Pirkei Avot]].', '',
        f'- **Translation:** {ver}; **License:** {J["license"]}; **Version source:** {J.get("versionSource")}; digital text from Sefaria (export of {EXPORT}).', '', '## Chapters', ''] + [f'- [[{n}]]' for n in names]) + '\n')

# =========================== Introduction to the Mishnah ===========================
def intro_mishnah():
    f = glob.glob(DL + '*Rambam Introduction to the Mishnah, translation by Rabbi Francis Nataf*')[0]; J = json.load(open(f)); t = J['text']; ver = J['versionTitle']
    base = 'Texts/Maimonides/Rambam Introduction to the Mishnah/'
    units = [(f'Rambam Introduction to the Mishnah {i:02d}', i, ch) for i, ch in enumerate(t, 1) if ch and any(isinstance(x, str) and x.strip() for x in ch)]
    names = [u[0] for u in units]
    for k, (name, i, segs) in enumerate(units):
        fns = []; st = {}; ref = f'Rambam Introduction to the Mishnah {i}'
        paras = [linkify(to_md(s, fns), refs_for(ref), st) + f' ^{i}-{j}' for j, s in enumerate(segs, 1) if isinstance(s, str) and s.strip()]
        d = {'type': 'text', 'work': 'Rambam Introduction to the Mishnah', 'author': ['Moses Maimonides'], 'translation': ver, 'translator': ['Francis Nataf'], 'license': J['license'],
             'source': 'https://www.sefaria.org/Rambam_Introduction_to_the_Mishnah.' + str(i) + '?ven=' + urllib.parse.quote(ver.replace(' ', '_')) + '&lang=en', 'aliases': [ref], 'chapter': i}
        put(base + name + '.md', '\n'.join([fm(d), f'# {name}', '', nav(names[k - 1] if k else None, 'Rambam Introduction to the Mishnah', names[k + 1] if k + 1 < len(names) else None), '', f'*Section {i}* · [[Rambam Introduction to the Mishnah]]']) + '\n\n' + '\n\n'.join(paras) + fn_block(fns) + '\n')
        STATS['intro_notes'] += 1
    put(base + 'Rambam Introduction to the Mishnah.md', '\n'.join([fm({'type': 'index', 'work': 'Rambam Introduction to the Mishnah', 'author': ['Moses Maimonides'], 'translation': ver, 'translator': ['Francis Nataf'], 'license': J['license'], 'source': 'https://www.sefaria.org/Rambam_Introduction_to_the_Mishnah', 'aliases': ['Introduction to the Mishnah (Maimonides)']}),
        '# Rambam Introduction to the Mishnah (Nataf)', '', 'Maimonides\' introduction to his Commentary on the Mishnah, in Rabbi Francis Nataf\'s translation (2017, CC0), one note per section as Sefaria divides it.', '',
        f'- **Translation:** {ver}; **License:** {J["license"]}; digital text from Sefaria (export of {EXPORT}).', '', '## Sections', ''] + [f'- [[{n}]]' for n in names]) + '\n')

# =========================== Kitzur Shulchan Arukh ===========================
def kitzur():
    f = glob.glob(DL + '*Kitzur Shulchan Aruch, trans. Rabbi Avrohom Davis*')[0]; J = json.load(open(f)); t = J['text']; ver = J['versionTitle']
    base = 'Texts/Kitzur Shulchan Arukh/'
    units = [(f'Kitzur Shulchan Arukh {i:03d}', i, ch) for i, ch in enumerate(t, 1) if ch and any(isinstance(x, str) and x.strip() for x in ch)]
    names = [u[0] for u in units]
    for k, (name, i, segs) in enumerate(units):
        fns = []; st = {}; paras = []
        for j, s in enumerate(segs, 1):
            if not (isinstance(s, str) and s.strip()): continue
            ref = f'Kitzur Shulchan Arukh {i}:{j}'
            paras.append(f'**{j}.** ' + linkify(to_md(s, fns), TAN.get(ref, []), st) + f' ^{i}-{j}'); STATS['kitzur_seifim'] += 1
        fns = [linkify(x, [], st) for x in fns]
        for kk, vv in st.items():
            if isinstance(vv, int): STATS['kitzur_' + kk] += vv
        d = {'type': 'text', 'work': 'Kitzur Shulchan Arukh', 'translation': ver, 'translator': ['Avrohom Davis'], 'license': J['license'],
             'source': f'https://www.sefaria.org/Kitzur_Shulchan_Arukh.{i}?ven=' + urllib.parse.quote(ver.replace(' ', '_')) + '&lang=en', 'aliases': [f'Kitzur Shulchan Arukh {i}', f'Kitzur Shulchan Aruch {i}', f'KSA {i}'], 'chapter': i}
        put(base + name + '.md', '\n'.join([fm(d), f'# {name}', '', nav(names[k - 1] if k else None, 'Kitzur Shulchan Arukh', names[k + 1] if k + 1 < len(names) else None), '', f'*Chapter {i}* · [[Kitzur Shulchan Arukh]]']) + '\n\n' + '\n\n'.join(paras) + fn_block(fns) + '\n')
        STATS['kitzur_notes'] += 1
    rows = [' · '.join(f'[[{n}|{int(n[-3:])}]]' for n in names[j:j + 10]) for j in range(0, len(names), 10)]
    put(base + 'Kitzur Shulchan Arukh.md', '\n'.join([fm({'type': 'index', 'work': 'Kitzur Shulchan Arukh', 'translation': ver, 'translator': ['Avrohom Davis'], 'license': J['license'], 'source': 'https://www.sefaria.org/Kitzur_Shulchan_Arukh', 'aliases': ['Kitzur Shulchan Aruch', 'Kitzur Shulchan Arukh index']}),
        '# Kitzur Shulchan Arukh (Davis)', '', f'The *Kitzur Shulchan Arukh* in Rabbi Avrohom Davis\'s translation (Metsudah, 1996), one note per chapter ({len(names)} notes), each se\'if a block (`^72-4` is chapter 72, se\'if 4); Davis\'s notes are the footnotes. Sefaria describes it as a "Popular handbook with simplified summaries of laws relevant to daily life, published in 1864." The author\'s name is not in Sefaria\'s export, so it is not given here. Chapter 32 has no English in this translation on Sefaria, so it has no note.', '',
        f'- **Translation:** {ver}', f'- **License:** {J["license"]}', f'- **Version source:** {J.get("versionSource")}', f'- **Digital text:** [Sefaria](https://www.sefaria.org/), via the Sefaria-Export dataset (export of {EXPORT}).', '', '## Chapters', ''] + [r + '  ' for r in rows[:-1]] + rows[-1:]) + '\n')

if __name__ == '__main__':
    import shutil; shutil.rmtree(OUT, ignore_errors=True)
    mishneh_torah(); guide(); eight_chapters(); intro_mishnah(); kitzur()
    put('Texts/Maimonides/Maimonides.md', '\n'.join([fm({'type': 'index', 'aliases': ['Rambam', 'Moses Maimonides']}), '# Maimonides', '', 'Works of Maimonides in the vault (English, from Sefaria, imported 22 Oct 2026):', '',
        '- [[Mishneh Torah]] (Touger)', '- [[Guide for the Perplexed]] (Friedländer)', '- [[Eight Chapters]] (Gorfinkle)', '- [[Rambam Introduction to the Mishnah]] (Nataf)']) + '\n')
    for p, t in NOTES.items():
        os.makedirs(os.path.dirname(OUT + p), exist_ok=True); open(OUT + p, 'w', encoding='utf-8').write(t)
    allc = collections.Counter()
    for t in NOTES.values():
        for k, v in checks(t).items(): allc[k] += v
    print(dict(STATS)); print(dict(allc)); print(len(NOTES), 'notes', round(sum(len(t.encode()) for t in NOTES.values()) / 1e6, 1), 'MB')
    for k, v in REPORT.items(): print(k, v)
