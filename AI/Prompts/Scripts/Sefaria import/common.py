# Shared pieces for the Sefaria imports of 22 Oct 2026 (Kedushat Levi, Likutei Moharan, Mei HaShiloach II).
import csv, html, json, re, urllib.parse

OUT = '/home/claude/sef/out'
VO = '/mnt/user-data/uploads/Obsidian Vault/.work/out/'
TORAH_BOOKS = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']
BOOKS = TORAH_BOOKS + ['Joshua', 'Judges', 'I Samuel', 'II Samuel', 'I Kings', 'II Kings', 'Isaiah', 'Jeremiah', 'Ezekiel',
         'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
         'Psalms', 'Proverbs', 'Job', 'Song of Songs', 'Ruth', 'Lamentations', 'Ecclesiastes', 'Esther', 'Daniel', 'Ezra',
         'Nehemiah', 'I Chronicles', 'II Chronicles']
BORDER = {b: i for i, b in enumerate(BOOKS)}

# ---- the vault's Bible notes (from runner jobs pe17 and pe18) ----
_t = json.load(open(VO + 'pe17-torahmap.json'))
TORAH = {}   # book -> [(note, set(blocks))]
for x in _t['torah']:
    if re.match(r'^Torah \d\d - ', x['b']) and x['fm'] and x['fm'].get('book'):
        TORAH.setdefault(x['fm']['book'], []).append((x['b'], set(x['blocks'])))
PARASHA_NOTE = {x['fm']['parasha']: x['b'] for x in _t['torah'] if re.match(r'^Torah \d\d - ', x['b']) and x['fm']}
BLOCKS = {k: set(v) for k, v in json.load(open(VO + 'pe18-blocks.json')).items()}
WIDTH = {}
for k in BLOCKS:
    m = re.match(r'^(.*) (\d+)$', k)
    if m and m.group(1) in BORDER: WIDTH[m.group(1)] = len(m.group(2))


def target(book, c, v):
    """The vault note holding verse book c:v, or None."""
    bid = f'{c}-{v}'
    if book in TORAH:
        for note, bl in TORAH[book]:
            if bid in bl: return note
        return None
    if book not in WIDTH: return None
    note = f'{book} {c:0{WIDTH[book]}d}'
    return note if bid in BLOCKS.get(note, ()) else None


# ---- Sefaria's links (links*.csv rows that mention the three works) ----
def parse_tanakh(ref):
    """'Psalms 119:1-3' -> (book, c1, v1, c2, v2); v1 None for a chapter."""
    m = re.match(r'^(.+?) (\d+)(?::(\d+))?(?:-(\d+)(?::(\d+))?)?$', ref)
    if not m or m.group(1) not in BORDER: return None
    b, c1, v1, a, b2 = m.group(1), int(m.group(2)), m.group(3), m.group(4), m.group(5)
    v1 = int(v1) if v1 else None
    if a and b2: c2, v2 = int(a), int(b2)
    elif a and v1 is not None: c2, v2 = c1, int(a)
    elif a: c2, v2 = int(a), None
    else: c2, v2 = c1, v1
    return (b, c1, v1, c2, v2)


def load_links(prefix):
    """Rows whose one side starts with prefix and whose other side is Tanakh: [(our ref, tanakh tuple)]."""
    out = []
    for r in csv.reader(open('/home/claude/sef/links/all.csv', encoding='utf-8')):
        if len(r) < 7: continue
        for a, b, cb in ((r[0], r[1], r[6]), (r[1], r[0], r[5])):
            if a.startswith(prefix) and cb == 'Tanakh':
                t = parse_tanakh(b)
                if t: out.append((a, t))
    return out


def verses(t):
    b, c1, v1, c2, v2 = t
    if v1 is None: return {(b, c1, None)}
    if c2 == c1: return {(b, c1, v) for v in range(v1, (v2 or v1) + 1)}
    return {(b, c1, v1), (b, c2, v2)}


# ---- in-text references ----
ALIAS = {}
for b in BOOKS: ALIAS[b] = b
for a, b in {'Gen': 'Genesis', 'Exod': 'Exodus', 'Ex': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers', 'Deut': 'Deuteronomy',
             'Josh': 'Joshua', 'Judg': 'Judges', 'Isa': 'Isaiah', 'Jer': 'Jeremiah', 'Ezek': 'Ezekiel', 'Hos': 'Hosea',
             'Mic': 'Micah', 'Hab': 'Habakkuk', 'Zeph': 'Zephaniah', 'Hag': 'Haggai', 'Zech': 'Zechariah', 'Mal': 'Malachi',
             'Psalm': 'Psalms', 'Ps': 'Psalms', 'Prov': 'Proverbs', 'Song of Solomon': 'Song of Songs', 'Lam': 'Lamentations',
             'Eccl': 'Ecclesiastes', 'Eccles': 'Ecclesiastes', 'Ecc': 'Ecclesiastes', 'Esth': 'Esther', 'Dan': 'Daniel',
             'Neh': 'Nehemiah', 'Obad': 'Obadiah'}.items(): ALIAS[a] = b
for n, r in (('1', 'I'), ('2', 'II'), ('I', 'I'), ('II', 'II')):
    for base, abbr in (('Samuel', 'Sam'), ('Kings', 'Kgs'), ('Chronicles', 'Chron')):
        ALIAS[f'{n} {base}'] = f'{r} {base}'; ALIAS[f'{n} {abbr}'] = f'{r} {base}'; ALIAS[f'{base} {n}'] = f'{r} {base}'
_names = sorted(ALIAS, key=len, reverse=True)
REF = re.compile(r'(?<![\w|#])(?<!\[\[)(\[)?(' + '|'.join(re.escape(n) for n in _names) + r')\.?(\s+)(\d{1,3})(\s?[:,.]\s?)(\d{1,3})(?:\s?[-–]\s?(\d{1,3}))?(?![\d])(?!\s*(?:Rabbah|Rabba|Rabbati))')


def link_refs(text, confirmed, stats, as_written=False):
    """Link 'Book c:v' (also c,v and c.v) where Sefaria links the same verse to this passage and the verse note exists.
    The text shown stays as written."""
    def rep(m):
        # groups: 1 '[' before the reference (escaped when linked), 2 book, 3 space, 4 chapter, 5 separator, 6 verse, 7 end of range
        br, shown = m.group(1) or '', m.group(0)[len(m.group(1) or ''):]
        book = ALIAS[m.group(2)]; c, v = int(m.group(4)), int(m.group(6))
        if (book, c, v) not in confirmed:
            # as_written (the Talmud, Maimonides): a 'Book c:v' reference whose verse exists is linked as printed (Hebrew numbering, as the Guide says for Jewish texts)
            if not (as_written and ':' in m.group(5) and target(book, c, v)):
                stats['unconfirmed'] = stats.get('unconfirmed', 0) + 1; return m.group(0)
            stats['as_written'] = stats.get('as_written', 0) + 1
        note = target(book, c, v)
        if not note:
            stats['notarget'] = stats.get('notarget', 0) + 1; stats.setdefault('notarget_ex', []).append(shown); return m.group(0)
        stats['linked'] = stats.get('linked', 0) + 1
        return ('\\[' if br else '') + f'[[{note}#^{c}-{v}|{shown}]]'
    # never inside an existing link
    parts = re.split(r'(\[\[[^\]]*\]\])', text)
    return ''.join(p if p.startswith('[[') else REF.sub(rep, p) for p in parts)


def torah_line(refs):
    """The '**Torah:**' line of a teaching from Sefaria's links to the Torah (as in the Mei HaShiloach notes)."""
    items = []
    for t in sorted(set(refs), key=lambda t: (BORDER[t[0]], t[1], t[2] or 0, t[3], t[4] or 0)):
        b, c1, v1, c2, v2 = t
        if b not in TORAH: continue
        note = target(b, c1, v1 or 1)
        if not note: continue
        if v1 is None: lab = f'{b} {c1}' + (f'–{c2}' if c2 != c1 else '')
        elif c2 == c1 and v2 == v1: lab = f'{b} {c1}:{v1}'
        elif c2 == c1: lab = f'{b} {c1}:{v1}–{v2}'
        else: lab = f'{b} {c1}:{v1}–{c2}:{v2}' if v2 else f'{b} {c1}:{v1}–{c2}'
        items.append(f'[[{note}#^{c1}-{v1 or 1}|{lab}]]')
    seen = []; [seen.append(i) for i in items if i not in seen]
    return ('**Torah:** ' + ', '.join(seen)) if seen else ''


# ---- HTML to Markdown ----
def _marks(s, tag, mk):
    # move spaces out of the emphasis markers so Markdown reads them
    s = re.sub(rf'<{tag}>(\s*)(.*?)(\s*)</{tag}>', lambda m: (m.group(1) + mk + m.group(2) + mk + m.group(3)) if m.group(2).strip() else m.group(0).replace(f'<{tag}>', '').replace(f'</{tag}>', ''), s, flags=re.S)
    return s


def _footnotes(s, fns):
    """<sup class="footnote-marker">n</sup><i class="footnote">… nested <i> …</i> -> [^k]; the note's own italics kept."""
    out = []; pos = 0
    pat = re.compile(r'<sup class="footnote-marker">[^<]*</sup>\s*<i class="footnote">')
    while True:
        m = pat.search(s, pos)
        if not m: out.append(s[pos:]); break
        out.append(s[pos:m.start()]); i = m.end(); depth = 1
        tok = re.compile(r'<i(?:\s[^>]*)?>|</i>')
        while depth:
            t = tok.search(s, i)
            if not t: break
            depth += 1 if t.group(0) != '</i>' else -1; i = t.end()
        body = s[m.end():i - 4] if depth == 0 else s[m.end():]
        fns.append(to_md(body, [])); out.append(f'[^{len(fns)}]'); pos = i if depth == 0 else len(s)
    s = ''.join(out)
    # a footnote with no marker in front of it
    return re.sub(r'<i class="footnote">(.*?)</i>', lambda m: (fns.append(to_md(m.group(1), [])) or f'[^{len(fns)}]'), s, flags=re.S)


def to_md(s, fns):
    """One Sefaria string -> Markdown. Footnotes are appended to fns and marked [^n]."""
    s = re.sub('(?<=[A-Za-z.,;:])\u200e(?=[\u0590-\u05ff])', ' ', s)   # a mark that stood for a space before Hebrew
    s = re.sub('[\u200e\u200f\u202a\u202b\u202c]', '', s)
    s = _footnotes(s, fns)
    s = re.sub(r'<sup>(\d+)</sup>', r'\1', s)
    s = s.replace('*', '\\*')                          # a literal asterisk in the source (section dividers) is not emphasis
    s = re.sub(r'</(b|i|strong|em)>(\s*)<\1>', r'\2', s)   # adjacent runs of the same emphasis are one run
    s = re.sub(r'<br\s*/?>\s*<br\s*/?>', '\n\n', s)
    s = re.sub(r'<br\s*/?>', '  \n', s)
    s = re.sub(r'</?(strong)>', lambda m: m.group(0).replace('strong', 'b'), s)
    s = re.sub(r'</?(em)>', lambda m: m.group(0).replace('em', 'i'), s)
    s = re.sub(r'<(b|i)\s[^>]*>', r'<\1>', s)
    for _ in range(2):
        s = _marks(s, 'b', '**'); s = _marks(s, 'i', '*')
    s = re.sub(r'</?(small|span|big|u|sup|sub|a)(\s[^>]*)?>', '', s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    s = html.unescape(s)
    s = s.replace('\xa0', ' ').replace('<', '\\<')   # editorial <insertions> stay visible (Obsidian would read them as tags)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s).replace('\n', '  \n').replace('    \n', '  \n')
    s = re.sub(r'(  \n){2,}', '\n\n', s)
    s = s.strip()
    # a paragraph that would start a list, heading or quote
    s = '\n\n'.join(re.sub(r'^(#|>|[-+*] |\d+\. )', lambda m: '\\' + m.group(1), p) for p in s.split('\n\n'))
    return s


def fn_block(fns):
    """Footnote definitions; a note's later lines are indented so they stay inside it."""
    return ('\n\n' + '\n'.join(f'[^{i}]: ' + t.replace('\n\n', '\n\n    ').replace('  \n', '  \n    ') for i, t in enumerate(fns, 1))) if fns else ''


def fm(d):
    out = ['---']
    for k, v in d.items():
        if v is None: continue
        if isinstance(v, list):
            out.append(f'{k}:'); out += [f'  - {json.dumps(x, ensure_ascii=False)}' for x in v]
        elif isinstance(v, (int, float)): out.append(f'{k}: {v}')
        else: out.append(f'{k}: {json.dumps(v, ensure_ascii=False)}')
    out.append('---'); return '\n'.join(out)


def sefaria_url(title, ven):
    return 'https://www.sefaria.org/' + title.replace(' ', '_') + '?ven=' + urllib.parse.quote(ven.replace(' ', '_'), safe='._-') + '&lang=en'


_Y, _H, _W = chr(0x5d9), chr(0x5d4), chr(0x5d5); _N = '[\u0591-\u05c7]*'
DIVINE = re.compile(r'\b[Y]\.?[-\s]?[Hh]\.?[-\s]?[VvWw]\.?[-\s]?[Hh]\b|[Y]ah[wv]eh|[J]ehovah|[Y]ud[-\s]+[Hh]e[hi]?[-\s]+[Vv]av[-\s]+[Hh]e[hi]?|' + _Y + _N + _H + _N + _W + _N + _H)   # counted only, never written


def checks(text):
    return {'divine': len(DIVINE.findall(text)), 'dollar': text.count('$'), 'pct': text.count('%%'), 'eq': text.count('=='),
            'tag': len(re.findall(r'(?<![\w&/])#[A-Za-z]', text)), 'heb_chars': len(re.findall(r'[֐-׿]', text)),
            'leftover_tags': len(re.findall(r'</?[a-z]+[ >]', text))}


# ---- Talmud references ('Berakhot 2a', 'Berachot 3a', 'Shabbos 31a') -> the daf notes (22 Oct 2026) ----
TAL_SIDES = set(); TAL_BLOCKS = set()
try:
    import glob as _g, os as _o
    for _p in _g.glob('/home/claude/tal/out/Texts/Talmud/*/*/*.md'):
        _b = _o.path.basename(_p)[:-3]; _m = re.match(r'^(.+) (\d+)$', _b)
        if _m:
            _t = open(_p, encoding='utf-8').read()
            for _s in re.findall(r'^## (\d+[ab])$', _t, re.M): TAL_SIDES.add((_m.group(1), _s))
            # the lines that have English (a segment Sefaria leaves empty has no block): links to a line check this
            for _s in re.findall(r' \^(\d+[ab]-\d+)$', _t, re.M): TAL_BLOCKS.add((_m.group(1), _s))
except Exception: pass
TAL_ALIAS = {}
for _t in ['Arakhin', 'Avodah Zarah', 'Bava Batra', 'Bava Kamma', 'Bava Metzia', 'Beitzah', 'Bekhorot', 'Berakhot', 'Chagigah', 'Chullin', 'Eruvin', 'Gittin',
           'Horayot', 'Keritot', 'Ketubot', 'Kiddushin', 'Makkot', 'Megillah', 'Meilah', 'Menachot', 'Moed Katan', 'Nazir', 'Nedarim', 'Niddah', 'Pesachim',
           'Rosh Hashanah', 'Sanhedrin', 'Shabbat', 'Shevuot', 'Sotah', 'Sukkah', 'Taanit', 'Tamid', 'Temurah', 'Yevamot', 'Yoma', 'Zevachim']: TAL_ALIAS[_t] = _t
for _a, _t in {'Berachot': 'Berakhot', 'Brachot': 'Berakhot', 'Shabbos': 'Shabbat', 'Eiruvin': 'Eruvin', 'Pesahim': 'Pesachim', 'Betzah': 'Beitzah', 'Beitza': 'Beitzah',
               'Rosh HaShanah': 'Rosh Hashanah', "Ta'anit": 'Taanit', 'Taanis': 'Taanit', "Mo'ed Katan": 'Moed Katan', 'Chaggigah': 'Chagigah', 'Hagigah': 'Chagigah',
               'Yevamos': 'Yevamot', 'Ketubbot': 'Ketubot', 'Kesubos': 'Ketubot', 'Kiddushin': 'Kiddushin', 'Kidushin': 'Kiddushin', 'Bava Kama': 'Bava Kamma',
               'Baba Kamma': 'Bava Kamma', 'Baba Metzia': 'Bava Metzia', 'Bava Metsia': 'Bava Metzia', 'Baba Batra': 'Bava Batra', 'Bava Basra': 'Bava Batra',
               'Makot': 'Makkot', 'Shevuos': 'Shevuot', "Avodah Zara": 'Avodah Zarah', "Avoda Zara": 'Avodah Zarah', 'Horiyot': 'Horayot', 'Zevahim': 'Zevachim',
               'Menahot': 'Menachot', 'Menachos': 'Menachot', 'Hullin': 'Chullin', 'Chulin': 'Chullin', 'Bechorot': 'Bekhorot', 'Bechoros': 'Bekhorot',
               'Arachin': 'Arakhin', 'Temura': 'Temurah', 'Kritot': 'Keritot', 'Kerisos': 'Keritot', "Me'ilah": 'Meilah', 'Nidah': 'Niddah', 'Sukka': 'Sukkah',
               'Megilla': 'Megillah', 'Yevamoth': 'Yevamot', 'Sota': 'Sotah', 'Nedarim': 'Nedarim', "Sh'vuot": 'Shevuot', "Shevu'ot": 'Shevuot', "Bava Metzi'a": 'Bava Metzia', 'Megilah': 'Megillah', "Mo'ed Kattan": 'Moed Katan', 'Moed Kattan': 'Moed Katan', "Avodah Zorah": 'Avodah Zarah', 'Keritut': 'Keritot', "Ta'anis": 'Taanit', "Yevamot": 'Yevamot'}.items(): TAL_ALIAS[_a] = _t
TREF = re.compile(r'(?<![\w|#\[*])(\*?)(' + '|'.join(re.escape(n) for n in sorted(TAL_ALIAS, key=len, reverse=True)) + r')(\*?)(,?\s+)(\d{1,3})([ab])\b(?![\]])')


def link_talmud(text, stats):
    """'Berachot 3a' -> [[Berakhot 3#3a|Berachot 3a]] when that side of the daf has a note."""
    def rep(m):
        if bool(m.group(1)) != bool(m.group(3)): return m.group(0)   # half an italic marker: leave it
        tr = TAL_ALIAS[m.group(2)]; d, s = int(m.group(5)), m.group(6)
        if (tr, f'{d}{s}') not in TAL_SIDES:
            stats['tal_notarget'] = stats.get('tal_notarget', 0) + 1; return m.group(0)
        stats['tal_linked'] = stats.get('tal_linked', 0) + 1
        return f'[[{tr} {d}#{d}{s}|{m.group(0)}]]'
    parts = re.split(r'(\[\[[^\]]*\]\])', text)
    return ''.join(p if p.startswith('[[') else TREF.sub(rep, p) for p in parts)
