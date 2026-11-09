"""jantlinks2.py (9 Nov 2026): a second JANT linker, for the texts added on 9 Nov 2026. Reads a dump of the JANT notes
({path: text}) and the block ids of the new notes; writes edits.json [{id, path, old, new}] (one per changed line, for the
pf784-style apply job, which checks every new block link before writing) and proposals.json.
Categories:
  enoch   *1 En.* / *1 Enoch* C.V (lists with "; C.V" and ", V")   -> [[1 Enoch CCC#^C-V|label]]
  qumran  1QS, CD (A/B), 1QM, 1QpHab, 1QSa, 1QSb, 11QTemple/11QSTemple/11Q19, 11QMelch, 4QFlor, 11QPsa, 1QapGen, 4QNNN + col.line
          -> [[DSS <siglum>#^<col>-<line>|label]] when that line exists in the note; CD cols 1-16 -> CD-A, 19-20 -> CD-B.
          1QH/1QHa are left plain: the Study Edition numbers 1QHa's columns in the new way, and the JANT's numbering was not checked.
  rabbah  *Gen./Exod./Lev./Num./Deut. Rab.* C.S -> Sefaria Book.C.S; *Song/Ruth/Lam/Eccl/Esth Rab.* C.S -> Sefaria Book.C
          (the chapter only: Sefaria numbers the Megillot Rabbot by chapter, verse and section)
Usage: python3 -I jantlinks2.py jant.json enoch_ids.json dss_ids.json outdir
  enoch_ids.json: {"1 Enoch 001": ["1-1", ...]};  dss_ids.json: {"DSS 1QS": ["3-13", ...]}"""
import json, re, sys, collections
J = json.load(open(sys.argv[1])); EN = {k: set(v) for k, v in json.load(open(sys.argv[2])).items()}; DS = {k: set(v) for k, v in json.load(open(sys.argv[3])).items()}
OUT = sys.argv[4]
def fm(t):
    m = re.match(r'---\n(.*?)\n---\n', t, re.S); return (m.end() if m else 0)
def segments(line):
    prot = [(m.start(), m.end()) for m in re.finditer(r'\[\[[^\]]*\]\]|`[^`]*`|\[[^\]]*\]\([^)]*\)', line)]
    pos = 0
    for a, b in prot:
        if a > pos: yield pos, a
        pos = b
    if pos < len(line): yield pos, len(line)
ITEM = re.compile(r'(\d{1,3})\.(\d{1,3})([ab]?)((?:[–-]\d{1,3}(?:\.\d{1,3})?[ab]?)?)')
def plist(s, i, allow_chap=False):
    out = []; chap = None
    while True:
        m = ITEM.match(s, i)
        if m and not re.match(r'[\d]', s[m.end():m.end() + 1] or ' ') and not re.match(r'\.\d', s[m.end():m.end() + 2]):
            chap = int(m.group(1)); out.append((m.start(), m.end(), chap, int(m.group(2)))); j = m.end()
        elif allow_chap and chap is None and re.match(r'(\d{1,3})(?![\d.]\d)(?!\s?[A-Za-z])', s[i:]):
            m = re.match(r'(\d{1,3})', s[i:]); out.append((i, i + m.end(), int(m.group(1)), 0)); j = i + m.end(); chap = -1
        else: break
        while chap and chap > 0:
            m2 = re.match(r'(,\s?)(\d{1,3})([ab]?)((?:[–-]\d{1,3}[ab]?)?)(?![\d.]\d)', s[j:])
            if not m2: break
            a = j + len(m2.group(1)); out.append((a, j + m2.end(), chap, int(m2.group(2)))); j = j + m2.end()
        m3 = re.match(r';\s', s[j:])
        if m3 and re.match(r'\d', s[j + m3.end():j + m3.end() + 1]): i = j + m3.end(); continue
        break
    return out
QMAP = {'1QS': 'DSS 1QS', '1QM': 'DSS 1QM', '1QpHab': 'DSS 1QpHab', '1QSa': 'DSS 1Q28a', '1QSb': 'DSS 1Q28b', '11QSTemple': 'DSS 11Q19', '11QTemple': 'DSS 11Q19',
        '11QT': 'DSS 11Q19', '11Q19': 'DSS 11Q19', '11QMelch': 'DSS 11Q13', '4QFlor': 'DSS 4Q174', '11QPsa': 'DSS 11Q5', '1QapGen': 'DSS 1QapGen', '4QTest': 'DSS 4Q175'}
SEF = {'Gen': 'Bereshit_Rabbah', 'Exod': 'Shemot_Rabbah', 'Lev': 'Vayikra_Rabbah', 'Num': 'Bamidbar_Rabbah', 'Deut': 'Devarim_Rabbah',
       'Song': 'Shir_HaShirim_Rabbah', 'Ruth': 'Ruth_Rabbah', 'Lam': 'Eichah_Rabbah', 'Eccl': 'Kohelet_Rabbah', 'Esth': 'Esther_Rabbah'}
MEG = {'Song', 'Ruth', 'Lam', 'Eccl', 'Esth'}
props = []; edits = []; miss = collections.Counter()
for p, t in J.items():
    b0 = fm(t); lines = t[b0:].split('\n')
    for line in lines:
        if line.startswith('#') or not line.strip(): continue
        reps = []
        for a, b in segments(line):
            seg = line[a:b]
            for m in re.finditer(r'\*1 En(?:och|\.)?\*\.?\s?|\*1 En\.\*\s?', seg):
                for (x, y, c, v) in plist(seg, m.end()):
                    nm = f'1 Enoch {c:03d}'
                    if nm in EN and f'{c}-{v}' in EN[nm]: reps.append((a + x, a + y, 'enoch', seg[x:y], f'[[{nm}#^{c}-{v}|{seg[x:y]}]]'))
                    else: miss['enoch'] += 1
            for m in re.finditer(r'(?<![\w\[/])(1QS|1QM|1QpHab|1QSa|1QSb|11QSTemple|11QTemple|11QT|11Q19|11QMelch|4QFlor|11QPsa|1QapGen|4QTest|CD(?: [AB])?|4Q\d{2,3}[a-z]?)\*?\s(?=\d)', seg):
                sig = m.group(1)
                for (x, y, c, v) in plist(seg, m.end()):
                    if v == 0: continue
                    if sig.startswith('CD'):
                        nm = 'DSS CD-B' if (sig == 'CD B' or c in (19, 20)) else 'DSS CD-A'
                    else: nm = QMAP.get(sig, 'DSS ' + sig)
                    if nm in DS and f'{c}-{v}' in DS[nm]: reps.append((a + x, a + y, 'qumran', seg[x:y], f'[[{nm}#^{c}-{v}|{seg[x:y]}]]'))
                    else: miss['qumran ' + sig] += 1
            for m in re.finditer(r'\*(Gen|Exod|Lev|Num|Deut|Song|Ruth|Lam|Eccl|Esth)\.? Rab\.?\*\.?\s?', seg):
                bk = m.group(1)
                for (x, y, c, v) in plist(seg, m.end(), allow_chap=True):
                    ref = f'{SEF[bk]}.{c}' + (f'.{v}' if v and bk not in MEG else '')
                    reps.append((a + x, a + y, 'rabbah', seg[x:y], f'[{seg[x:y]}](https://www.sefaria.org/{ref})'))
        if not reps: continue
        reps.sort(key=lambda r: (r[0], -(r[1] - r[0]))); keep = []; last = -1
        for r in reps:
            if r[0] >= last: keep.append(r); last = r[1]
        new = line
        for s0, e0, cat, lab, link in sorted(keep, key=lambda r: -r[0]):
            new = new[:s0] + link + new[e0:]
            props.append({'path': p, 'cat': cat, 'label': lab, 'link': link, 'ctx': line[max(0, s0 - 50):e0 + 10]})
        edits.append({'id': f'e{len(edits)+1}', 'path': p, 'old': line, 'new': new})
json.dump(edits, open(OUT + '/edits.json', 'w'), ensure_ascii=False, indent=0)
json.dump(props, open(OUT + '/proposals.json', 'w'), ensure_ascii=False, indent=0)
print('edits (lines)', len(edits), 'links', len(props), dict(collections.Counter(x['cat'] for x in props)), 'not linked', dict(miss))
