"""jantlinks.py (7 Nov 2026): links in the JANT notes the references whose targets are in the vault but that the
13 Oct linker left plain. Reads jant.json ({path: text}, from a runner dump); writes edits.json [{id, path, old, new}]
(one edit per changed line, for the pf591 edit template) and proposals.json (one entry per link, with its category).
Categories:
  ezra   *4 Ezra*, *5 Ezra*, *6 Ezra*, 2 Esd  -> NRSVue 2 Esdras (4 Ezra = 2 Esd 3-14, same numbering)
  one    Jude, Philem, 2 Jn, 3 Jn with a verse only -> New Testament (BSB/SBLGNT) note, as the linker links NT refs
  avot   *m. Avot* C.V -> Pirkei Avot (ch. 1-4 and 5.1-19 only; 5.20 on and ch. 6 differ between editions)
  note   C.Vn. / v Nn. (the JANT's own notes) -> the JANT annotation whose key covers the verse
  see    see/cf. C.V with no book (the same book) -> New Testament note
Skips: headings, frontmatter, text inside existing links or code, a list after any other siglum.
Usage: python3 jantlinks.py jant.json outdir"""
import json, re, sys, collections
J = json.load(open(sys.argv[1])); OUT = sys.argv[2]
NT = {'Mt': 'Matthew', 'Mk': 'Mark', 'Lk': 'Luke', 'Jn': 'John', 'Acts': 'Acts', 'Rom': 'Romans', '1 Cor': '1 Corinthians',
      '2 Cor': '2 Corinthians', 'Gal': 'Galatians', 'Eph': 'Ephesians', 'Phil': 'Philippians', 'Col': 'Colossians',
      '1 Thess': '1 Thessalonians', '2 Thess': '2 Thessalonians', '1 Tim': '1 Timothy', '2 Tim': '2 Timothy', 'Titus': 'Titus',
      'Philem': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James', '1 Pet': '1 Peter', '2 Pet': '2 Peter', '1 Jn': '1 John',
      '2 Jn': '2 John', '3 Jn': '3 John', 'Jude': 'Jude', 'Rev': 'Revelation'}
ONE = {'Jude': 'Jude', 'Philem': 'Philemon', '2 Jn': '2 John', '3 Jn': '3 John', '2 John': '2 John', '3 John': '3 John'}
DASH = '–'
def fm(t):
    m = re.match(r'---\n(.*?)\n---\n', t, re.S); d = {}
    if m:
        for l in m.group(1).split('\n'):
            k, _, v = l.partition(':'); d[k.strip()] = v.strip().strip('"')
    return d, (m.end() if m else 0)
# ---- index of JANT annotation keys: (book, chap) -> [(start, end, block)]
KEYS = collections.defaultdict(list)
for p, t in J.items():
    if '/Annotations/' not in p: continue
    d, _ = fm(t); b, c = d.get('book'), int(d.get('chapter', 0) or 0)
    for l in t.split('\n'):
        m = re.match(r'\*\*\[\[NRSVue [^\]|]+\|([^\]]+)\]\]:\*\*.*\s\^([\w-]+)\s*$', l)
        if not m: continue
        nums = [int(x) for x in re.findall(r'\d+', m.group(1))]
        if not nums: continue
        KEYS[(b, c)].append((nums[0], nums[-1], m.group(2)))
def note_target(book, c, v):
    ks = KEYS.get((book, c))
    if not ks: return None
    ex = [k for k in ks if k[0] == v]
    cov = ex or [k for k in ks if k[0] <= v <= k[1]]
    return f'JANT {book} {c:02d}#^{cov[0][2]}' if cov else None
def nt_target(book, c, v): return f'{book} {c:02d}#^{c}-{v}'
# ---- protect existing links, code, inline html
def segments(line):
    """yield (start, end) of stretches outside [[...]], `...`, and markdown links"""
    prot = [(m.start(), m.end()) for m in re.finditer(r'\[\[[^\]]*\]\]|`[^`]*`|\[[^\]]*\]\([^)]*\)', line)]
    pos = 0
    for a, b in prot:
        if a > pos: yield pos, a
        pos = b
    if pos < len(line): yield pos, len(line)
V = r'\d{1,3}[ab]?'
ITEM_CV = re.compile(r'(\d{1,2})\.(\d{1,3})([ab]?)((?:[–-]\d{1,3}(?:\.\d{1,3})?[ab]?)?)(n\.)?')
def parse_list(s, i, allow_chap=False):
    """parse a reference list at s[i:]; returns [(start, end, chap, verse, isnote)] using chapter carry for ',V' items"""
    out = []; chap = None
    while True:
        m = ITEM_CV.match(s, i)
        if m and not re.match(r'[\d.]', s[m.end():m.end()+1] or ' ') :
            chap = int(m.group(1)); out.append((m.start(), m.end(), chap, int(m.group(2)), bool(m.group(5)))); j = m.end()
        elif allow_chap and re.match(r'(\d{1,2})((?:[–-]\d{1,2})?)(?![\d.*])(?!\s?[A-Za-z])', s[i:]) and chap is None:
            m = re.match(r'(\d{1,2})((?:[–-]\d{1,2})?)(?![\d.*])(?!\s?[A-Za-z])', s[i:]); out.append((i, i + m.end(), int(m.group(1)), 0, False)); j = i + m.end(); chap = -1
        else: break
        # comma-continued verses of the same chapter: ",17" ", 44–54"
        while chap and chap > 0:
            m2 = re.match(r'(,\s?)(\d{1,3})([ab]?)((?:[–-]\d{1,3}[ab]?)?)(n\.)?(?![\d.]\d)', s[j:])
            if not m2: break
            a = j + len(m2.group(1)); out.append((a, j + m2.end(), chap, int(m2.group(2)), bool(m2.group(5)))); j = j + m2.end()
        m3 = re.match(r';\s', s[j:])
        if m3 and re.match(r'\d', s[j + m3.end():j + m3.end() + 1]): i = j + m3.end(); continue
        break
    return out
props = []; edits = []
for p, t in J.items():
    if '/Annotations/' not in p and '/Introductions/' not in p: continue
    d, body0 = fm(t); book = d.get('book'); chap0 = int(d.get('chapter', 0) or 0)
    if not book: continue
    lines = t[body0:].split('\n'); changed = False
    for li, line in enumerate(lines):
        if line.startswith('#') or not line.strip(): continue
        reps = []  # (start, end, newtext, cat, label, target)
        for a, b in segments(line):
            seg = line[a:b]
            # ezra
            for m in re.finditer(r'(\*?[456] Ezra\*?|2 Esd\b\.?)(\s?\\\[=?(?:2 Esd(?: \d+–\d+)?|\*4 Ezra\*)\\\])?(\s?\(?\s?)', seg):
                if re.match(r'\*?[456] Ezra', m.group(1)) and not m.group(1).endswith('*') and '*' in m.group(1)[:1]:
                    pass
                for (x, y, c, v, isn) in parse_list(seg, m.end(), allow_chap=True):
                    if not (1 <= c <= 16) or isn: continue
                    tgt = f'NRSVue 2 Esdras {c:02d}#^{c}-{v if v else 1}'
                    reps.append((a + x, a + y, None, 'ezra', seg[x:y], tgt))
            # single-chapter books
            for m in re.finditer(r'(?<![\w⟧])(Jude|Philem|2 Jn|3 Jn|2 John|3 John) (?=\d)', seg):
                j = m.end(); bk = ONE[m.group(1)]; first = True
                while True:
                    m2 = re.match(r'(\d{1,2})([ab]?)((?:[–-]\d{1,2}[ab]?)?)(?![\d.:]\d|\d)', seg[j:])
                    if not m2: break
                    lab_s = j if not first else m.start(); lab_e = j + m2.end()
                    reps.append((a + lab_s, a + lab_e, None, 'one', seg[lab_s:lab_e], f'{bk} 01#^1-{int(m2.group(1))}'))
                    j = lab_e; first = False
                    m3 = re.match(r',\s?(?=\d)', seg[j:])
                    if not m3: break
                    j += m3.end()
            # m. Avot
            for m in re.finditer(r'\*?m\. ?Avot\*?\.?\s?', seg):
                for (x, y, c, v, isn) in parse_list(seg, m.end()):
                    if isn or c > 5 or c < 1 or (c == 5 and v >= 20) or (c, v) == (3, 12) or seg[x:y].endswith(('a', 'b')): continue  # JANT's 3.12 is Danby's numbering (Kehati 3.11)
                    reps.append((a + x, a + y, None, 'avot', seg[x:y], f'Pirkei Avot {c:02d}#^{c}-{v}'))
            # note refs and see/cf. same-book verse refs
            for m in re.finditer(r'(?<![\w⟧\]\.–\-\*/])(\d{1,2})\.(\d{1,3})(?:[–-]\d{1,3})?n\.', seg):
                pre = seg[:m.start()]
                w = re.search(r'((?:[123] )?[A-Z][a-z]+)\.?\s$', pre)
                bk = book
                if w and w.group(1) in NT: bk = NT[w.group(1)]
                elif w and re.search(r'[A-Z][a-z]+\.?\s$', pre) and not re.search(r'(See|Cf)\.?\s$', pre): continue
                if re.search(r'\*[^*]+\*\.?\s$', pre): continue
                c, v = int(m.group(1)), int(m.group(2)); tg = note_target(bk, c, v)
                if tg: reps.append((a + m.start(), a + m.end(), None, 'note', m.group(0), tg))
            for m in re.finditer(r'\bvv?\.? (\d{1,3})(?:[–-]\d{1,3})?n\.', seg):
                if '/Annotations/' not in p: continue
                tg = note_target(book, chap0, int(m.group(1)))
                if tg: reps.append((a + m.start(), a + m.end(), None, 'note', m.group(0), tg))
            for m in re.finditer(r'\b(?:see|See|cf\.|Cf\.)(?: also| esp\.)?\s(?=\d)', seg):
                if re.search(r'(\]\]|\\\])\S{0,3}[;,]?\s*(\(\s*)?$', line[:a + m.start()]): continue  # right after a link to another book
                if re.search(r'\b(?:[123] )?[A-Z][a-z]{1,6}\.? \d{1,3}(?:[.:]\d{1,3})?[^.()]{0,25}$', line[:a + m.start()]): continue  # after a plain book reference
                # the sentence so far (from the key, a lemma or a full stop) names another work: a link to another book, a siglum with numbers,
                # a plain book abbreviation, Josephus or Philo -> the reference may belong to it; leave it
                sent = re.split(r'\*\*:|\.\s(?=[A-Z*“"])|\.\)\s', line[:a + m.start()])[-1]
                own = re.escape(book)
                if re.search(r'\[\[(?!NRSVue %s |%s \d|JANT %s )[^\]]+\]\]' % (own, own, own), sent) or re.search(r'\*[^*]{1,30}\*\.?\s?\d', sent) \
                   or re.search(r'\b(Josephus|Philo|Ant\.|J\.W\.|Gen|Exod?|Lev|Num|Deut|Isa|Jer|Ezek|Dan|Ps|Pss|Lk|Mk|Mt|Jn|Rom|Acts|Heb)\b(?!\s?[A-Z])', sent): continue
                for (x, y, c, v, isn) in parse_list(seg, m.end()):
                    if isn: continue  # handled above
                    reps.append((a + x, a + y, None, 'see', seg[x:y], nt_target(book, c, v)))
        if not reps: continue
        # de-duplicate overlaps (keep earliest, longest)
        reps.sort(key=lambda r: (r[0], -(r[1] - r[0]))); keep = []; last = -1
        for r in reps:
            if r[0] >= last: keep.append(r); last = r[1]
        new = line
        for s0, e0, _, cat, lab, tgt in sorted(keep, key=lambda r: -r[0]):
            new = new[:s0] + f'[[{tgt}|{lab}]]' + new[e0:]
            props.append({'path': p, 'cat': cat, 'label': lab, 'target': tgt, 'ctx': line[max(0, s0 - 50):e0 + 10]})
        edits.append({'id': f'e{len(edits)+1}', 'path': p, 'old': line, 'new': new})
json.dump(edits, open(OUT + '/edits.json', 'w'), ensure_ascii=False, indent=0)
json.dump(props, open(OUT + '/proposals.json', 'w'), ensure_ascii=False, indent=0)
print('edits (lines)', len(edits), 'links', len(props), dict(collections.Counter(x['cat'] for x in props)))
