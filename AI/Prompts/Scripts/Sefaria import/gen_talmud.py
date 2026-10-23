# The Babylonian Talmud in English (William Davidson edition, Koren-Steinsaltz), one note per daf, from the Sefaria export.
import csv, collections, glob, json, os, re, sys, urllib.parse
sys.path.insert(0, '/home/claude/sef')
from common import to_md, link_refs, verses, parse_tanakh, target, fm, fn_block, checks, TORAH_BOOKS, BORDER, DIVINE

DL = '/home/claude/tal/dl/'; OUT = '/home/claude/tal/out/'
EXPORT = '2026-10-01'
SEDER = {}
for line in open('/home/claude/tal/files.txt'):
    parts = line.strip().split('/')   # json/Talmud/Bavli/Seder X/Tractate/English/...
    SEDER[parts[4]] = parts[3]
TRACT = sorted(SEDER)
SEDER_ORDER = ['Seder Zeraim', 'Seder Moed', 'Seder Nashim', 'Seder Nezikin', 'Seder Kodashim', 'Seder Tahorot']
ONLY = set(sys.argv[1:])     # build only these tractates (samples)

def amud_label(i):            # list index (0-based) -> '2a'
    return f'{i // 2 + 1}{"ab"[i % 2]}'

def parse_tal(ref):
    """'Berakhot 2a:1-3' -> (tractate, daf, 'a', seg or None)."""
    m = re.match(r'^(.+?) (\d+)([ab])(?::(\d+))?', ref)
    if not m or m.group(1) not in SEDER: return None
    return (m.group(1), int(m.group(2)), m.group(3), int(m.group(4)) if m.group(4) else None)

def sefaria_link(ref):
    m = re.match(r'^(.*?) ([\d:ab\-–]+)$', ref)
    path = (m.group(1).replace(' ', '_') + '.' + m.group(2).replace(':', '.')) if m else ref.replace(' ', '_')
    return f'[{ref}](https://www.sefaria.org/{urllib.parse.quote(path, safe="_.,-()\'")})'

# ---- notes of other works in the vault that Sefaria links to a passage ----
TANYA = {'Part I; Likkutei Amarim': ('Tanya - Likkutei Amarim', 2), 'Part II; Shaar HaYichud VehaEmunah': ('Tanya - Shaar HaYichud VehaEmunah', 2),
         'Part III; Iggeret HaTeshuvah': ('Tanya - Iggeret HaTeshuvah', 2), 'Part IV; Iggeret HaKodesh': ('Tanya - Iggeret HaKodesh', 2),
         'Part V; Kuntres Acharon': ('Tanya - Kuntres Acharon', 2)}
VAULT_NAMES = set(json.load(open('/home/claude/tal/vault_names.json'))) if os.path.exists('/home/claude/tal/vault_names.json') else set()
KL_NOTES = {}
for p in glob.glob('/home/claude/sef/out/Texts/Chasidut/Kedushat Levi/*/*.md'):
    t = open(p, encoding='utf-8').read(); al = re.search(r'aliases:\n  - "([^"]+)"', t)
    if al: KL_NOTES[al.group(1)] = (os.path.basename(p)[:-3], set(re.findall(r'^## Teaching (\d+)$', t, re.M)))

def vault_link(ref):
    """A link into the vault for a passage of another work, or None."""
    m = re.match(r'^Likutei Moharan(, Part II)? (\d+)(?::(\d+))?', ref)
    if m:
        n = f"Likutei Moharan {'II' if m.group(1) else 'I'} {int(m.group(2)):03d}"
        return f'[[{n}#{m.group(3)}|LM {"II" if m.group(1) else "I"}:{m.group(2)}' + (f':{m.group(3)}' if m.group(3) else '') + ']]' if m.group(3) else f'[[{n}|LM {"II" if m.group(1) else "I"}:{m.group(2)}]]'
    m = re.match(r'^(Kedushat Levi, .+) (\d+)(?::\d+)?$', ref)
    if m and m.group(1) in KL_NOTES:
        n, teach = KL_NOTES[m.group(1)]
        return f'[[{n}#Teaching {m.group(2)}|{m.group(1)} {m.group(2)}]]' if m.group(2) in teach else None
    m = re.match(r'^Tanya, (Part [IV]+; [^0-9]+?) (\d+)(?::(\d+))?', ref)
    if m and m.group(1) in TANYA:
        base, w = TANYA[m.group(1)]; n = f'{base} {int(m.group(2)):0{w}d}'
        return f'[[{n}|Tanya, {m.group(1).split("; ")[1]} {m.group(2)}]]' if (not VAULT_NAMES or n in VAULT_NAMES) else None
    m = re.match(r'^Pirkei Avot (\d+):(\d+)', ref)
    if m: return f'[[Pirkei Avot {int(m.group(1)):02d}#^{m.group(1)}-{m.group(2)}|Pirkei Avot {m.group(1)}:{m.group(2)}]]'
    return None

# ---- Maimonides and the Kitzur (built in /home/claude/ram/out) ----
RAM = {}
for _p in glob.glob('/home/claude/ram/out/Texts/**/*.md', recursive=True):
    _t = open(_p, encoding='utf-8').read(); _a = re.search(r'aliases:\n  - "([^"]+)"', _t)
    if _a: RAM[_a.group(1)] = (os.path.basename(_p)[:-3], set(re.findall(r' \^([\w-]+)$', _t, re.M)))

def ram_link(ref):
    """'Mishneh Torah, Reading the Shema 1:9' -> the chapter note's block; Kitzur and Guide likewise."""
    m = re.match(r'^(Mishneh Torah, .+? \d+|Kitzur Shulchan Arukh \d+):(\d+)', ref)
    if m and m.group(1) in RAM:
        n, bl = RAM[m.group(1)]; c = m.group(1).rsplit(' ', 1)[1]
        return f'[[{n}#^{c}-{m.group(2)}|{ref}]]' if f'{c}-{m.group(2)}' in bl else f'[[{n}|{ref}]]'
    m = re.match(r'^(Guide for the Perplexed, Part \d+ \d+)', ref)
    if m and m.group(1) in RAM: return f'[[{RAM[m.group(1)][0]}|{ref}]]'
    m = re.match(r'^(Mishneh Torah, .+? \d+|Kitzur Shulchan Arukh \d+|Eight Chapters \d+)$', ref)
    if m and m.group(1) in RAM: return f'[[{RAM[m.group(1)][0]}|{ref}]]'
    return None

# ---- Sefaria's links, by amud ----
TORAH_OR = collections.defaultdict(list); MESORET = collections.defaultdict(list); EIN = collections.defaultdict(list); VAULT = collections.defaultdict(list)
SEGREFS = collections.defaultdict(list)   # (tractate, daf, side, seg) -> tanakh tuples, for in-text links
for f in sorted(glob.glob('/home/claude/tal/links/l*.csv')):
    for r in csv.reader(open(f, encoding='utf-8')):
        if len(r) < 7: continue
        for a, b, ta, tb, ca, cb in ((r[0], r[1], r[3], r[4], r[5], r[6]), (r[1], r[0], r[4], r[3], r[6], r[5])):
            if ca != 'Talmud' or ta not in SEDER: continue
            k = parse_tal(a)
            if not k or (ONLY and k[0] not in ONLY): continue
            amud = k[:3]; typ = r[2]
            if cb == 'Tanakh':
                t = parse_tanakh(b)
                if t: TORAH_OR[amud].append((t, k[3])); SEGREFS[k].append(t)
            elif typ in ('mesorat hashas', 'related passage'):
                MESORET[amud].append((b, cb, k[3]))
            elif typ == 'ein mishpat / ner mitsvah':
                EIN[amud].append((b, k[3]))
            elif cb in ('Chasidut', 'Mishnah', 'Halakhah', 'Jewish Thought'):
                vl = vault_link(b) or (ram_link(b) if not b.startswith('Mishneh Torah') else None)
                if vl: VAULT[amud].append((vl, k[3]))

def verse_link(t):
    b, c1, v1, c2, v2 = t
    note = target(b, c1, v1 or 1)
    if v1 is None: lab = f'{b} {c1}' + (f'–{c2}' if c2 != c1 else '')
    elif c2 == c1 and (v2 in (None, v1)): lab = f'{b} {c1}:{v1}'
    elif c2 == c1: lab = f'{b} {c1}:{v1}–{v2}'
    else: lab = f'{b} {c1}:{v1}–{c2}:{v2}' if v2 else f'{b} {c1}:{v1}–{c2}'
    return f'[[{note}#^{c1}-{v1 or 1}|{lab}]]' if note else lab

_SEGTEXT = {}
def seg_ok(tr, d, s, seg):
    """True when that line of the daf has English (Sefaria leaves some segments empty; they get no block)."""
    if tr not in _SEGTEXT:
        try: _SEGTEXT[tr] = json.load(open(DL + tr + '.json'))['text']
        except Exception: _SEGTEXT[tr] = None
    t = _SEGTEXT[tr]
    if t is None: return False
    try: x = t[(d - 1) * 2 + (0 if s == 'a' else 1)][seg - 1]
    except (IndexError, TypeError): return False
    return isinstance(x, str) and bool(x.strip())

def tal_link(ref):
    k = parse_tal(ref)
    if not k: return None
    tr, d, s, seg = k
    if seg and not seg_ok(tr, d, s, seg): seg = None   # 22 Oct 2026: 8 Mesoret links pointed at empty segments; now to the side
    lab = ref[len(tr) + 1:]   # 22 Oct 2026: was the text after the first word, which doubled two-word names (Bava Kamma Kamma)
    return f'[[{tr} {d}#^{d}{s}-{seg}|{tr} {lab}]]' if seg else f'[[{tr} {d}#{d}{s}|{tr} {lab}]]'

def seglist(xs):
    segs = sorted({s for s in xs if s})
    return '' if not segs else ' (line ' + ', '.join(map(str, segs)) + ')' if len(segs) == 1 else ' (lines ' + ', '.join(map(str, segs)) + ')'

def margins(amud):
    out = []
    lab = f'{amud[1]}{amud[2]}'
    if TORAH_OR.get(amud):
        g = collections.OrderedDict()
        for t, s in sorted(TORAH_OR[amud], key=lambda x: (BORDER[x[0][0]], x[0][1], x[0][2] or 0)): g.setdefault(t, []).append(s)
        out.append(f'> [!torah]- Torah Or ({lab})\n' + '\n'.join(f'> - {verse_link(t)}{seglist(ss)}' for t, ss in g.items()))
    if MESORET.get(amud):
        g = collections.OrderedDict()
        for b, cb, s in MESORET[amud]: g.setdefault((b, cb), []).append(s)
        items = []
        for (b, cb), ss in g.items():
            items.append((tal_link(b) if cb == 'Talmud' and parse_tal(b) else (vault_link(b) or sefaria_link(b))) + seglist(ss))
        out.append(f'> [!xref]- Mesoret HaShas ({lab})\n' + '\n'.join(f'> - {x}' for x in items))
    if EIN.get(amud):
        g = collections.OrderedDict()
        for b, s in EIN[amud]: g.setdefault(b, []).append(s)
        out.append(f'> [!xref]- Ein Mishpat ({lab})\n' + '\n'.join(f'> - {ram_link(b) or sefaria_link(b)}{seglist(ss)}' for b, ss in g.items()))
    if VAULT.get(amud):
        g = collections.OrderedDict()
        for vl, s in VAULT[amud]: g.setdefault(vl, []).append(s)
        out.append(f'> [!links]- In this vault ({lab})\n' + '\n'.join(f'> - {vl}{seglist(ss)}' for vl, ss in g.items()))
    return out

NOTES = {}; STATS = collections.Counter(); IDX = collections.defaultdict(list)
for tr in TRACT:
    if ONLY and tr not in ONLY: continue
    J = json.load(open(DL + tr + '.json')); ver = J['versionTitle']
    edition = re.sub(r'<[^>]+>', '', J.get('versionNotes', '')).strip()
    amudim = J['text']; seder = SEDER[tr]
    dafs = collections.OrderedDict()
    for i, segs in enumerate(amudim):
        if segs and any(isinstance(s, str) and s.strip() for s in segs): dafs.setdefault(i // 2 + 1, []).append(i)
    dl = list(dafs)
    folder = f'Texts/Talmud/{seder}/{tr}/'
    for k, d in enumerate(dl):
        name = f'{tr} {d}'; prev = f'{tr} {dl[k - 1]}' if k else None; nxt = f'{tr} {dl[k + 1]}' if k + 1 < len(dl) else None
        sides = [amud_label(i) for i in dafs[d]]
        meta = {'type': 'text', 'work': 'Talmud Bavli', 'masekhet': tr, 'seder': seder.replace('Seder ', ''), 'daf': d,
                'translation': ver, 'edition': edition, 'license': J.get('license'),
                'source': f'https://www.sefaria.org/{tr.replace(" ", "_")}.{d}a?ven={urllib.parse.quote(ver.replace(" ", "_"))}&lang=en',
                'aliases': [f'{tr} {s}' for s in sides] + [f'BT {tr} {d}']}
        body = []; st = {}
        for i in dafs[d]:
            s = amud_label(i); side = s[-1]; fns = []
            paras = []
            for j, seg in enumerate(amudim[i], 1):
                if not (isinstance(seg, str) and seg.strip()): continue
                conf = set()
                for t in SEGREFS.get((tr, d, side, j), []): conf |= verses(t)
                txt = link_refs(to_md(seg, fns), conf, st, as_written=True)
                paras.append(txt + f' ^{s}-{j}'); STATS['segments'] += 1
            body.append(f'## {s}\n\n' + '\n\n'.join(margins((tr, d, side))) + ('\n\n' if margins((tr, d, side)) else '') + '\n\n'.join(paras)
                        + fn_block(fns))
            STATS['amudim'] += 1
        for kk, vv in st.items():
            if isinstance(vv, int): STATS[kk] += vv
        nav = (f'← [[{prev}]] · ' if prev else '') + f'[[{tr}]]' + (f' · [[{nxt}]] →' if nxt else '')
        head = [fm(meta), f'# {name}', '', nav, '', f'*{seder} · {tr} · Daf {d}* · [[{tr}]] · [[Talmud]]']
        NOTES[folder + name + '.md'] = '\n'.join(head) + '\n\n' + '\n\n'.join(body) + '\n'
        STATS['notes'] += 1
        IDX[(seder, tr)].append(d)
    # tractate index note
    ns = [f'{tr} {d}' for d in dl]
    rows = [' · '.join(f'[[{n}|{n.split(" ")[-1]}]]' for n in ns[j:j + 10]) for j in range(0, len(ns), 10)]
    meta = {'type': 'index', 'work': 'Talmud Bavli', 'masekhet': tr, 'seder': seder.replace('Seder ', ''), 'translation': ver, 'license': J.get('license'),
            'source': f'https://www.sefaria.org/{tr.replace(" ", "_")}', 'aliases': [f'Masekhet {tr}', f'Tractate {tr}', f'BT {tr}']}
    NOTES[folder + tr + '.md'] = '\n'.join([fm(meta), f'# {tr}', '', f'*{seder}* · [[Talmud]]', '',
        f'Tractate {tr} of the Babylonian Talmud in the William Davidson edition (Koren–Steinsaltz English), one note per daf, dapim {dl[0]}–{dl[-1]} ({len(dl)} notes). In each note the bold words translate the Talmud\'s text and the rest is Rabbi Steinsaltz\'s explanation, as on Sefaria.', '',
        '## Dapim', ''] + [r + '  ' for r in rows[:-1]] + rows[-1:]) + '\n'

if __name__ == '__main__':
    import shutil
    if not ONLY: shutil.rmtree(OUT, ignore_errors=True)
    for p, t in NOTES.items():
        os.makedirs(os.path.dirname(OUT + p), exist_ok=True); open(OUT + p, 'w', encoding='utf-8').write(t)
    allc = collections.Counter()
    for t in NOTES.values():
        for k, v in checks(t).items(): allc[k] += v
    print(dict(STATS)); print(dict(allc)); print(len(NOTES), 'notes', round(sum(len(t.encode()) for t in NOTES.values()) / 1e6, 1), 'MB')
    json.dump({f'{s}|{t}': v for (s, t), v in IDX.items()}, open('/home/claude/tal/idx.json', 'w'))
