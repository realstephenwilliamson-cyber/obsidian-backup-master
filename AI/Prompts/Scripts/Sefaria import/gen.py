# Builds the vault notes for Kedushat Levi, Likutei Moharan and Mei HaShiloach vol. II from the Sefaria export (22 Oct 2026).
import glob, json, os, re, sys, collections
sys.path.insert(0, '/home/claude/sef')
from common import *

DL = '/home/claude/sef/dl/'
EXPORT = '2026-10-01'
NOTES = {}     # vault path -> text
STATS = collections.Counter(); LSTATS = {}; REPORT = collections.defaultdict(list)
def J(name): return json.load(open(DL + name))
def put(path, text): NOTES[path] = text

def nav(prev, index, nxt):
    if prev and nxt: return f'← [[{prev}]] · [[{index}]] · [[{nxt}]] →'
    if nxt: return f'[[{index}]] · [[{nxt}]] →'
    if prev: return f'← [[{prev}]] · [[{index}]]'
    return f'[[{index}]]'

def footer(fns):
    return ('\n\n' + '\n'.join(f'[^{i}]: {t}' for i, t in enumerate(fns, 1))) if fns else ''

def unit_links(links, keyf):
    U = collections.defaultdict(list)
    for ref, t in links:
        k = keyf(ref)
        if k is not None:
            for kk in (k if isinstance(k, list) else [k]): U[kk].append(t)
    return U

def confirmed(ts):
    s = set()
    for t in ts: s |= verses(t)
    return s

# =========================== Kedushat Levi ===========================
def kedushat_levi():
    munk_f = 'Early Works__Kedushat Levi__English__Kedushat Levi translated by Rb. Eliyahu Munk.json'
    M = J(munk_f); C = J('Early Works__Kedushat Levi__English__Sefaria Community Translation.json')
    YU = J('Early Works__Kedushat Levi__English__YU Torah miTzion Beit Midrash.json'); FE = J('Early Works__Kedushat Levi__English__Rabbi Mike Feuer, Jerusalem Anthology.json')
    MV, CV = M['versionTitle'], C['versionTitle']
    links = load_links('Kedushat Levi, ')
    def key(ref):
        m = re.match(r'^Kedushat Levi, (.+) (\d+)(?:[-:](\d+))?$', ref)
        if not m: return None
        parts = tuple(m.group(1).split(', ')); a = int(m.group(2))
        return parts + (a,)
    U = unit_links(links, key)
    base = 'Texts/Chasidut/Kedushat Levi/'
    order = []   # (folder, book, section, note name, segments)
    folders = {'Genesis': '1 Genesis', 'Exodus': '2 Exodus', 'Leviticus': '3 Leviticus', 'Numbers': '4 Numbers', 'Deuteronomy': '5 Deuteronomy'}
    def collect(mt, ct, path):
        mt = mt if isinstance(mt, list) else []; ct = ct if isinstance(ct, list) else []
        segs = []
        for i in range(max(len(mt), len(ct))):
            ms = mt[i] if i < len(mt) and isinstance(mt[i], str) else ''
            cs = ct[i] if i < len(ct) and isinstance(ct[i], str) else ''
            if ms.strip(): segs.append((i + 1, ms, 'munk')); STATS['kl_munk'] += 1; STATS['kl_both'] += bool(cs.strip())
            elif cs.strip(): segs.append((i + 1, cs, 'comm')); STATS['kl_comm'] += 1
        return segs
    for book in TORAH_BOOKS:
        names = list(dict.fromkeys(list(M['text'].get(book, {}).keys()) + list(C['text'].get(book, {}).keys())))
        for sec in names:
            segs = collect(M['text'][book].get(sec), C['text'][book].get(sec), (book, sec))
            if not segs: REPORT['kl_no_english'].append(f'{book}, {sec}'); continue
            pn = PARASHA_NOTE.get(sec)
            name = f'Kedushat Levi {pn[6:8]} - {sec}' if pn else f'Kedushat Levi - {sec}'
            order.append((folders[book], book, sec, name, segs, pn))
    for top, v in C['text'].items():
        if top in TORAH_BOOKS or top == 'Letters of Approbation': continue
        if isinstance(v, dict):
            for sec, t in v.items():
                segs = collect(M['text'].get(top, {}).get(sec) if isinstance(M['text'].get(top), dict) else None, t, (top, sec))
                if segs: order.append(('6 Other', top, sec, f'Kedushat Levi - {top} - {sec}', segs, None))
                else: REPORT['kl_no_english'].append(f'{top}, {sec}')
        else:
            segs = collect(M['text'].get(top) if isinstance(M['text'].get(top), list) else None, v, (top,))
            if segs: order.append(('6 Other', top, None, f'Kedushat Levi - {top}', segs, None))
            else: REPORT['kl_no_english'].append(top)
    # YU / Feuer: texts with no licence in the export; counted, not imported
    def nonempty(x, p=()):
        if isinstance(x, dict):
            for k, v in x.items(): yield from nonempty(v, p + (k,))
        elif isinstance(x, list):
            for i, v in enumerate(x): yield from nonempty(v, p + (i + 1,))
        elif isinstance(x, str) and x.strip(): yield p
    for nm, V in (('YU Torah miTzion', YU), ('Feuer', FE)): REPORT['kl_skipped_versions'].append(f"{nm}: {len(list(nonempty(V['text'])))} passages, licence {V.get('license', 'not stated')}")
    index_lines = collections.OrderedDict()
    for k, (folder, book, sec, name, segs, pn) in enumerate(order):
        prev = order[k - 1][3] if k else None; nxt = order[k + 1][3] if k + 1 < len(order) else None
        all_comm = all(s[2] == 'comm' for s in segs)
        title = f'Kedushat Levi, {book}, {sec}' if sec else f'Kedushat Levi, {book}'
        d = {'type': 'text', 'work': 'Kedushat Levi',
             'author': ['Levi Yitzchak of Berditchev'], 'translation': CV if all_comm else MV, 'translator': None if all_comm else ['Eliyahu Munk'],
             'license': 'CC0' if all_comm else 'CC-BY', 'source': sefaria_url(title, CV if all_comm else MV),
             'aliases': [title] + ([f'Kedushat Levi on {sec}', f'Kedushat Levi, Parashat {sec}'] if pn else []),
             'book': book if book in TORAH_BOOKS else None, 'parasha': sec if pn else None, 'section': None if pn else (sec or book)}
        if not pn and book in TORAH_BOOKS: d['section'] = sec
        fns = []; body = []; st = {}
        for i, s, src in segs:
            u = U.get((book, sec, i) if sec else (book, i), [])
            txt = link_refs(to_md(s, fns), confirmed(u), st)
            block = [f'## Teaching {i}', '']
            if src == 'comm' and not all_comm: block += ['*Sefaria Community Translation (CC0).*', '']
            block.append(txt)
            tl = torah_line(u)
            if tl: block += ['', tl]
            body.append('\n'.join(block))
        for kk, vv in st.items():
            if isinstance(vv, int): STATS['kl_' + kk] += vv
            else: REPORT['kl_' + kk] += vv
        where = f'*{book} · {sec}*' if sec else f'*{book}*'
        head = [fm(d), f'# {name}', '', nav(prev, 'Kedushat Levi', nxt), '',
                where + (f' · Torah: [[{pn}]]' if pn else '') + ' · [[Kedushat Levi]]']
        if all_comm: head += ['', '> [!note] Sefaria Community Translation\n> Munk\'s translation does not cover this section; the English here is the Sefaria Community Translation (CC0), and only the passages it translates are here.']
        text = '\n'.join(head) + '\n\n' + '\n\n'.join(body) + footer(fns) + '\n'
        put(base + folder + '/' + name + '.md', text)
        index_lines.setdefault(folder, []).append((name, sec or book, len(segs), all_comm))
    # index note
    cats = {'1 Genesis': 'Genesis', '2 Exodus': 'Exodus', '3 Leviticus': 'Leviticus', '4 Numbers': 'Numbers', '5 Deuteronomy': 'Deuteronomy', '6 Other': 'Other sections'}
    d = {'type': 'index', 'work': 'Kedushat Levi', 'author': ['Levi Yitzchak of Berditchev'], 'translation': MV, 'translator': ['Eliyahu Munk'], 'license': 'CC-BY',
         'source': 'https://www.sefaria.org/Kedushat_Levi', 'aliases': ['Kedushat Levi index', 'Kedushat Levi (Munk)']}
    L = [fm(d), '# Kedushat Levi (Munk)', '',
         '*Kedushat Levi*, in Rabbi Eliyahu Munk\'s translation, following Sefaria\'s structure: one note per parasha, and one note for each section that is not on a parasha. Sefaria describes it as the "Seminal work of Rabbi Levi Yitzchak of Berditchev arranged according to the weekly Torah portion." Teachings are numbered as on Sefaria; where Sefaria links a teaching to a Torah verse, the verse is linked under the teaching, and scripture references in the text are linked where Sefaria links the same verse to that teaching.',
         '', f'Munk\'s translation covers the five books of the Torah ({STATS["kl_munk"]} teachings). {STATS["kl_comm"]} more passages, mostly in sections Munk did not translate (the Chanukah and Purim homilies, *Likutim*, *The Rules of Miracles*), are in the Sefaria Community Translation (CC0) and are marked where they appear. Sections with no English on Sefaria: ' + '; '.join(REPORT['kl_no_english']) + '.',
         '', '## License and attribution', '',
         f'- **Translation:** {MV}', '- **Translator:** Eliyahu Munk', '- **License:** CC-BY',
         f'- **Version source:** {M.get("versionSource")}', f'- **Version notes:** {M.get("versionNotes")}', f'- **Print edition:** {M.get("purchaseInformationURL")}',
         '- **Other passages:** Sefaria Community Translation, CC0.',
         f'- **Digital text:** [Sefaria](https://www.sefaria.org/), via the [Sefaria-Export](https://github.com/Sefaria/Sefaria-Export) dataset (export of {EXPORT}).']
    for folder, items in index_lines.items():
        L += ['', f'## {cats[folder]}', ''] + [f'- [[{n}]]' + (' (community translation)' if ac else '') for n, s, c, ac in items]
    put(base + 'Kedushat Levi.md', '\n'.join(L) + '\n')

# =========================== Likutei Moharan ===========================
def likutei_moharan():
    A = J([os.path.basename(f) for f in glob.glob(DL + '*Volumes 1-11*')][0]); B = J([os.path.basename(f) for f in glob.glob(DL + '*Volumes 12-15*')][0])
    AV, BV = A['versionTitle'], B['versionTitle']
    links = load_links('Likutei Moharan')
    def key(ref):
        m = re.match(r'^Likutei Moharan(, Part II)? (\d+)(?::(\d+))?', ref)
        if m: return (2 if m.group(1) else 1, int(m.group(2)), int(m.group(3)) if m.group(3) else None)
        m = re.match(r'^Likutei Moharan, (Introduction|Go See)(?: (\d+))?', ref)
        if m: return (m.group(1), None, None)
        return None
    U = unit_links(links, key)
    base = 'Texts/Chasidut/Likutei Moharan/'
    notes = []
    for part, V, ver in ((1, A['text'][''], AV), (2, B['text']['Part II'], BV)):
        for li, lesson in enumerate(V, 1):
            secs = [(si, [g for g in sec if isinstance(g, str) and g.strip()]) for si, sec in enumerate(lesson, 1)]
            secs = [(si, g) for si, g in secs if g]
            if not secs: REPORT['lm_empty'].append(f'{part}:{li}'); continue
            notes.append((part, li, secs, ver))
    names = [f"Likutei Moharan {'I' if p == 1 else 'II'} {li:03d}" for p, li, s, v in notes]
    for k, (part, li, secs, ver) in enumerate(notes):
        name = names[k]; P = 'I' if part == 1 else 'II'
        prev = names[k - 1] if k else None; nxt = names[k + 1] if k + 1 < len(names) else None
        sref = f'Likutei Moharan {li}' if part == 1 else f'Likutei Moharan, Part II {li}'
        d = {'type': 'text', 'work': 'Likutei Moharan', 'author': ['Nachman of Breslov'], 'translation': ver, 'translator': ['Moshe Mykoff'], 'license': 'CC-BY-NC',
             'source': sefaria_url(('Likutei_Moharan.' if part == 1 else 'Likutei_Moharan,_Part_II.') + str(li), ver).replace('Likutei_Moharan.', 'Likutei_Moharan.', 1),
             'aliases': [sref, f'LM {P}:{li}', f'Likutei Moharan {P} {li}'], 'part': P, 'lesson': li}
        fns = []; body = []; st = {}
        lesson_refs = U.get((part, li, None), [])
        for si, segs in secs:
            u = U.get((part, li, si), []) + lesson_refs
            conf = confirmed(u)
            paras = [link_refs(to_md(g, fns), conf, st) for g in segs]
            if paras and paras[0].startswith(f'**{si}.** '): paras[0] = paras[0][len(f'**{si}.** '):]; STATS['lm_numbers_dropped'] += 1   # the number is the heading
            body.append(f'## {si}\n\n' + '\n\n'.join(paras))
        for kk, vv in st.items():
            if isinstance(vv, int): STATS['lm_' + kk] += vv
            else: REPORT['lm_' + kk] += vv
        head = [fm(d), f'# {name}', '', nav(prev, 'Likutei Moharan', nxt), '', f'*Part {P} · Lesson {li}* · [[Likutei Moharan]]']
        put(base + f'Part {P}/' + name + '.md', '\n'.join(head) + '\n\n' + '\n\n'.join(body) + footer(fns) + '\n')
        STATS['lm_notes'] += 1; STATS['lm_sections'] += len(secs)
    # front matter notes
    for sec, nm in (('Introduction', 'Likutei Moharan - Introduction'), ('Go See', 'Likutei Moharan - Go See')):
        segs = [g for g in A['text'][sec] if isinstance(g, str) and g.strip()]
        fns = []; st = {}
        conf = confirmed(U.get((sec, None, None), []))
        paras = [link_refs(to_md(g, fns), conf, st) for g in segs]
        for kk, vv in st.items():
            if isinstance(vv, int): STATS['lm_' + kk] += vv
        d = {'type': 'text', 'work': 'Likutei Moharan', 'author': ['Nachman of Breslov'], 'translation': AV, 'translator': ['Moshe Mykoff'], 'license': 'CC-BY-NC',
             'source': sefaria_url(f'Likutei Moharan, {sec}', AV), 'aliases': [f'Likutei Moharan, {sec}'], 'section': sec}
        put(base + nm + '.md', '\n'.join([fm(d), f'# {nm}', '', nav(None, 'Likutei Moharan', None), '', f'*{sec}* · [[Likutei Moharan]]', '']) + '\n' + '\n\n'.join(paras) + footer(fns) + '\n')
    d = {'type': 'index', 'work': 'Likutei Moharan', 'author': ['Nachman of Breslov'], 'translation': AV, 'translator': ['Moshe Mykoff'], 'license': 'CC-BY-NC',
         'source': 'https://www.sefaria.org/Likutei_Moharan', 'aliases': ['Likutei Moharan index', 'Likutey Moharan', 'Likutei Moharan (Mykoff)']}
    L = [fm(d), '# Likutei Moharan (Mykoff)', '',
         f'*Likutei Moharan* in Moshe Mykoff\'s translation (Breslov Research Institute), following Sefaria\'s structure: one note per lesson, Part I (lessons 1–{max(l for p, l, s, v in notes if p == 1)}) and Part II (lessons 1–{max(l for p, l, s, v in notes if p == 2)}), with the lesson\'s numbered sections as headings. Sefaria describes it as "Rebbe Nachman of Breslov’s magnum opus, containing interpretations of talmudic stories and of parts of the Zohar, among other sermons." Scripture references in the text are linked where Sefaria links the same verse to that lesson. Sefaria\'s English has the translation only, not the Breslov Research Institute\'s notes; *A Pleasant Song* and *Additions from Manuscript* have no English on Sefaria.',
         '', '## License and attribution', '',
         f'- **Translation:** {AV}; {BV}', '- **Translator:** Moshe Mykoff', '- **License:** CC-BY-NC',
         f'- **Print edition:** {A.get("purchaseInformationURL")}',
         f'- **Digital text:** [Sefaria](https://www.sefaria.org/), via the [Sefaria-Export](https://github.com/Sefaria/Sefaria-Export) dataset (export of {EXPORT}).',
         '', '## Front matter', '', '- [[Likutei Moharan - Introduction]]', '- [[Likutei Moharan - Go See]]']
    for P in ('I', 'II'):
        L += ['', f'## Part {P}', '']
        ns = [n for n in names if n.startswith(f'Likutei Moharan {P} ')]
        # ten lessons to a line keeps the index short
        rows = [' · '.join(f'[[{n}|{int(n[-3:])}]]' for n in ns[j:j + 10]) for j in range(0, len(ns), 10)]
        L += [r + '  ' for r in rows[:-1]] + rows[-1:]
    put(base + 'Likutei Moharan.md', '\n'.join(L) + '\n')

# =========================== Mei HaShiloach II ===========================
def mei_hashiloach_2():
    C = J('Izhbitz__Mei HaShiloach__English__Sefaria Community Translation.json'); CV = C['versionTitle']
    links = load_links('Mei HaShiloach, Volume II')
    def key(ref):
        m = re.match(r'^Mei HaShiloach, Volume II, ([^,]+), (.+?) (\d+)(?::(\d+))?', ref)
        return (m.group(1), m.group(2), int(m.group(3))) if m else None
    U = unit_links(links, key)
    base = 'Texts/Chasidut/Mei HaShiloach/Volume II/'
    order = []
    for sect, v in C['text']['Volume II'].items():
        if not isinstance(v, dict): continue
        for sec, t in v.items():
            if not isinstance(t, list) or not json.dumps(t).strip('[]", '): continue
            items = []
            for i, x in enumerate(t, 1):
                if isinstance(x, str) and x.strip(): items.append((i, [x], None))
                elif isinstance(x, list) and any(isinstance(y, str) and y.strip() for y in x):
                    items.append((i, [y for y in x if isinstance(y, str) and y.strip()], i))
            if items: order.append((sect, sec, items))
    def label(sect, sec, i):
        if sect == 'Talmud': return f'{sec} {(i + 1) // 2}{"a" if i % 2 else "b"}'
        return f'{sec} {i}'
    for k, (sect, sec, items) in enumerate(order):
        name = f'Mei HaShiloach II - {sec}'; pn = PARASHA_NOTE.get(sec) if sect in TORAH_BOOKS else None
        prev = f'Mei HaShiloach II - {order[k - 1][1]}' if k else None
        nxt = f'Mei HaShiloach II - {order[k + 1][1]}' if k + 1 < len(order) else None
        title = f'Mei HaShiloach, Volume II, {sect}, {sec}'
        d = {'type': 'text', 'work': 'Mei HaShiloach', 'author': ['Mordechai Yosef Leiner of Izhbitz'], 'translation': CV, 'license': 'CC0', 'source': sefaria_url(title, CV),
             'aliases': [title] + ([f'Mei HaShiloach II on {sec}'] if pn else []), 'volume': 2, 'section': sect, 'parasha': sec if pn else None}
        fns = []; body = []; st = {}
        for n, (i, segs, chap) in enumerate(items, 1):
            u = U.get((sect, sec, i), [])
            paras = [link_refs(to_md(g, fns), confirmed(u), st) for g in segs]
            h = f'## Teaching {i}' if chap is None else f'## Teaching {n} ({label(sect, sec, i)})'
            tl = torah_line(u)
            body.append(h + '\n\n' + '  \n'.join(paras) + (('\n\n' + tl) if tl else ''))
        for kk, vv in st.items():
            if isinstance(vv, int): STATS['mh_' + kk] += vv
        head = [fm(d), f'# {name}', '', nav(prev, 'Mei HaShiloach', nxt), '',
                f'*Volume II · {sect} · {sec}*' + (f' · Torah: [[{pn}]]' if pn else '') + ' · [[Mei HaShiloach]]', '',
                '> [!note] Sefaria Community Translation (partial)\n> Volume II has no published English translation on Sefaria. These are the passages the Sefaria Community Translation (CC0) has translated so far; the other teachings of this section are in Hebrew only.']
        put(base + name + '.md', '\n'.join(head) + '\n\n' + '\n\n'.join(body) + footer(fns) + '\n')
        STATS['mh_notes'] += 1; STATS['mh_teachings'] += len(items)
    REPORT['mh_order'] = [(s, sec) for s, sec, it in order]

if __name__ == '__main__':
    kedushat_levi(); likutei_moharan(); mei_hashiloach_2()
    import shutil; shutil.rmtree(OUT, ignore_errors=True)
    for p, t in NOTES.items():
        os.makedirs(os.path.dirname(OUT + '/' + p), exist_ok=True); open(OUT + '/' + p, 'w', encoding='utf-8').write(t)
    allc = collections.Counter()
    for p, t in NOTES.items():
        for k, v in checks(t).items(): allc[k] += v
    print(dict(STATS)); print(dict(allc)); print(len(NOTES), 'notes', sum(len(t.encode()) for t in NOTES.values()) / 1e6, 'MB')
    for k, v in REPORT.items(): print(k, v[:12] if isinstance(v, list) else v, len(v) if isinstance(v, list) else '')
