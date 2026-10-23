"""Conservative clean-up of the OCR letter damage in the library copy of Dyczkowski's Tantraloka (22 Oct 2026).
Only patterns whose reading is fixed: stand-in letters (ã ă ŝ ș ñ+k/g ù ň ž and the escaped \$ for Ś), ṁ read as rh / rn,
and the footnote-call junk (TM ® ™ °). Headings, page markers, links and code are not touched. lib3/ -> lib4/."""
import re, glob, os, json, collections, sys
SRC, DST = sys.argv[1] if len(sys.argv) > 1 else 'lib3', sys.argv[2] if len(sys.argv) > 2 else 'lib4'
ENGL = set()
for f in ('/usr/share/dict/american-english-large', '/usr/share/dict/british-english-large'):
    ENGL |= {w.strip().lower() for w in open(f, encoding='utf-8', errors='ignore')}
P5 = '/mnt/user-data/uploads/Obsidian Vault/.work/plan/phase-5-work/'
uf = json.load(open(P5 + '12oct/units-final.json'))['units']
LET = r"A-Za-zāīūṛṝḷḹṅñṭḍṇśṣṁḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṀḤ"
STAND = "ãÃăŝŜșȘùňžŽ"
TOK = re.compile(rf"(?:\\\$)?[{LET}{STAND}]+")
OK_TOK = re.compile(rf"(?:\\\$)?[{LET}{STAND}]+$")
# attested spellings: Dyczkowski's own (the cleaned verse translations, and the library text's undamaged words)
ATT = collections.Counter()
for v in uf.values(): ATT.update(w.lower() for w in re.findall(rf"[{LET}]+", v if isinstance(v, str) else ''))
V = "aāiīuūeo"
STATS = collections.Counter(); SAMPLES = collections.defaultdict(list)
def note(cls, a, b):
    STATS[cls] += 1
    if len(SAMPLES[cls]) < 400: SAMPLES[cls].append((a, b))
def english(w): return w.lower() in ENGL
def fix_token(w):
    o = w
    if w.startswith('\\$') and len(w) > 2 and w[2].islower():
        w = 'Ś' + w[2:]; note('\\$ → Ś', o, w)
    if not OK_TOK.match(w) or '\\$' in w: return w
    a = w
    # an English word with a stand-in letter in it ("conŝidered", "soùnd")
    # (only ù and ŝ: the dictionary also holds Sanskrit loanwords such as atman, nyaya, mudra)
    plain = w.replace('ù', 'u').replace('ŝ', 's')
    if plain != w and w.islower() and not re.search(f'[{STAND}āīūṛṅñṭḍṇśṣṁḥ]', plain) and len(plain) >= (5 if 'ù' in w else 7) and english(plain):
        note('English word', w, plain); return plain
    # ã / ă (a doubled vowel keeps one ā)
    w = re.sub(r'āã|ãā|ãa|aã|āă|ăā', 'ā', w); w = re.sub(r'Āã|ÃĀ|ĀÃ|Ãā', 'Ā', w)
    w = w.replace('ã', 'ā').replace('Ã', 'Ā').replace('ă', 'ā')
    if w != a: note('ã ă → ā', a, w); a = w
    w = re.sub(r'śŝ|ŝś|ŝŝ|sŝ|ŝs', 'ś', w); w = re.sub(r'Śŝ|Ŝś', 'Ś', w); w = w.replace('ŝ', 'ś').replace('Ŝ', 'Ś')
    if w != a: note('ŝ → ś', a, w); a = w
    w = re.sub(r'ṣș|șṣ|șș', 'ṣ', w); w = re.sub(r'Ṣș|ȘṢ|Șș', 'Ṣ', w); w = w.replace('ș', 'ṣ').replace('Ș', 'Ṣ')
    if w != a: note('ș → ṣ', a, w); a = w
    # ù: a ṅ (or ṁ, ñ) whose dot the OCR misread
    if 'ù' in w:
        if True:
            w = re.sub(rf'(?<=[{V}])rù(?:ń|h(?=kh))?', 'ṁ', w)
            w = re.sub(r'ñù(?=[kg])', 'ṅ', w)
            def mu(m):
                c1, c2 = w[:m.start()] + 'ṅ' + w[m.end():], w[:m.start()] + 'ṁ' + w[m.end():]
                return 'ṁ' if ATT[c2.lower()] > ATT[c1.lower()] else 'ṅ'
            if re.search(r'ṁù(?:ń|h(?=kh))?(?=[kg])', w): w = re.sub(r'ṁù(?:ń|h(?=kh))?(?=[kg])', mu, w, count=1)
            w = re.sub(r'ṁù', 'ṁ', w)
            w = re.sub(rf'(?<=[{V}])ù(?=[kg])', 'ṅ', w)
            w = re.sub(r'(?<=j)ù(?=[{V}])'.replace('{V}', V), 'ñ', w)
        if w != a: note('ù → ṅ/ṁ/ñ', a, w); a = w
    # ñ before k/g is ṅ
    def mn(m):
        c1, c2 = w[:m.start()] + 'ṅ' + w[m.end():], w[:m.start()] + 'ṁ' + w[m.end():]
        return 'ṁ' if ATT[c2.lower()] > ATT[c1.lower()] else 'ṅ'
    if re.search(r'[ṁñ]*(?:ṁñ|ñṁ)[ṁñ]*(?=[kgKG])', w): w = re.sub(r'[ṁñ]*(?:ṁñ|ñṁ)[ṁñ]*(?=[kgKG])', mn, w)
    w = re.sub(r'ñ(?=[kgKG])', 'ṅ', w)
    if w != a: note('ñ → ṅ before k/g', a, w); a = w
    # ň: an ṁ (with the m, r or ṁ the OCR put before it)
    w = re.sub(r'(?:[mr]|ṁ+)?ňṁ?', 'ṁ', w)
    if w != a: note('ň → ṁ', a, w); a = w
    # ž / Ž in the few words where the reading is plain
    w = re.sub(r'^Žś', 'Īś', w); w = re.sub(r'^ž(?=rdhv|ha)', 'ū', w)
    if w != a: note('ž → ū/Ī', a, w); a = w
    # ṁ read as rh / rn (after a vowel, before a consonant; rn only in words that are not English)
    if 'rh' in w or 'rn' in w:
        w2 = re.sub(rf'(?<=[{V}])rhn?$', 'ṁ', w) if len(w) >= 3 and not english(w) else w
        w2 = re.sub(rf'(?<=[{V}])rh(?=[kgcjṭḍtdpbmnyrlvśṣsh])', 'ṁ', w2)
        if not english(w):
            w2 = re.sub(rf'(?<=[{V}])rn(?=[kgcjṭḍtdpbyrlvśṣsh])', 'ṁ', w2)
        if w2 != w and not english(w): w = w2
        if w != a: note('rh rn → ṁ', a, w); a = w
    return w
JUNK = [('® ™', re.compile(r'[®™]+')),
        ('TM', re.compile(r"(?<=[a-zāīūṛṅñṭḍṇśṣṁḥ.,;:)’”'\"!?*])TM(?:TM)*(?![a-z])")),
        ('°', re.compile(r"(?<=[A-Za-zāīūṛṅñṭḍṇśṣṁḥ.,;:)’”'\"!?*])°(?!\d)"))]
PROT = re.compile(r'\[\[[^\]]*\]\]|`[^`]*`|https?://\S+|<[^>]+>')
def fix_line(line):
    if line.startswith('#') or line.startswith('*[p.') or line.startswith('*[PDF') or line.startswith('^'): return line
    line = re.sub(r'ŝ\\\$', 'ś', line); line = re.sub(r'Ŝ\\\$', 'Ś', line)
    line = re.sub(r'(?<=-)(\s*)\\\$(?=[a-zāīū])', r'\1ś', line)
    # \$ inside a word: Ś / ś, after K the Ṣ of kṣa, T\$ for Īś
    line = re.sub(r'(?<![^\W\d_])T\\\$(?=[a-zāīū])', 'Īś', line); line = re.sub(r'Ī[śŝ]?\\\$', 'Īś', line)
    line = re.sub(r'[śs]\\\$(?=[a-zāīūṛ])', 'ś', line); line = re.sub(r'Ś\\\$', 'Ś', line)
    line = re.sub(r'(?<=[a-zāīūṛ])\\\$(?=[a-zāīūṛ])', 'ś', line)
    line = re.sub(r'[ṢȘ]\\\$', 'Ṣ', line); line = re.sub(r'K\\\$Ṣ', 'KṢ', line); line = re.sub(r'K\\\$', 'KṢ', line)
    out, last = [], 0
    for m in list(PROT.finditer(line)) + [None]:
        seg = line[last:m.start()] if m else line[last:]
        for cls, rx in JUNK:
            seg2 = rx.sub('', seg)
            if seg2 != seg: STATS[cls] += len(rx.findall(seg)); seg = seg2
        seg = TOK.sub(lambda t: fix_token(t.group(0)), seg)
        out.append(seg)
        if m: out.append(m.group(0)); last = m.end()
    return ''.join(out)
changed = 0
for f in sorted(glob.glob(SRC + '/*/*.md')):
    raw = open(f, encoding='utf-8').read()
    m = re.match(r'^---\n.*?\n---\n', raw, flags=re.S); off = m.end() if m else 0
    body = '\n'.join(fix_line(l) for l in raw[off:].split('\n'))
    new = raw[:off] + body
    d = DST + f[len(SRC):]; os.makedirs(os.path.dirname(d), exist_ok=True)
    open(d, 'w', encoding='utf-8').write(new); changed += new != raw
print('notes changed', changed); print(dict(STATS))
json.dump({k: v for k, v in SAMPLES.items()}, open('clean-samples.json', 'w'), ensure_ascii=False, indent=0)
