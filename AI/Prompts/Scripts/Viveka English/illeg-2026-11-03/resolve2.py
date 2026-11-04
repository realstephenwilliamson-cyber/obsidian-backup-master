# resolve2.py: the 199 gaps the two readers read differently. Each reading is first reduced to its core: the footnote marks (^N)
# and the ^ of raised ordinals taken out, then the words (and bare punctuation) at either end that already stand next to the gap
# in the note taken off, one by one (a reader copied the neighbours too). Then:
#  same core, with letters, no '?', at most six words  -> fill (both readers agree on the gap itself);
#  both cores the same number, and the gap sits next to that footnote's own label or call -> the placeholder is taken out;
#  otherwise -> a third blind reader. -> tb/rule.json {id: {kind, fill, A, B}}, tb/third.json
import json, glob, re, unicodedata, difflib, collections
def load(d):
    R = {}
    for f in glob.glob(d + '/*.jsonl'):
        for l in open(f, encoding='utf-8'):
            l = l.strip()
            if l:
                try: x = json.loads(l); R[x.get('id')] = x
                except Exception: pass
    return R
A = {**load('read/A'), **load('read2/A')}; B = {**load('read/B'), **load('read2/B')}
N1 = json.load(open('dy-after.json')); pos = json.load(open('tb/pos.json')); ids = json.load(open('tb/ids.json'))
nf = lambda s: unicodedata.normalize('NFC', (s or '').strip()).replace("'", '’').replace('"', '”')
fold = lambda s: ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if c.isascii() and c.isalnum())
marks = lambda s: re.sub(r'\s+', ' ', re.sub(r'\^(?=(st|nd|rd|th)\b)', '', re.sub(r'\^\d+', '', s))).strip()
clean = lambda s: re.sub(r'\[\^[^\]]*\]:?|\\|<[^>]+>', '', s).replace('॥', '||')
def close(x, ctx, lead):
    if x == ctx: return True
    if len(x) < 4 or len(ctx) != len(x): return False
    edge = (x[-4:] == ctx[-4:]) if lead else (x[:4] == ctx[:4])    # the words must meet the gap exactly
    return edge and difflib.SequenceMatcher(None, x, ctx).ratio() >= 0.85
def core(r, before, after):
    w = r.split(); fb, fa = fold(before), fold(after); bs, as_ = before.rstrip(), after.lstrip()
    for k in range(len(w) - 1, 0, -1):          # longest leading run of words found at the end of the before-text
        x = fold(' '.join(w[:k]))
        if (x and close(x, fb[-len(x):], True)) or (not x and bs and not bs[-1].isalnum()): w = w[k:]; break
    for k in range(len(w) - 1, 0, -1):          # longest trailing run found at the start of the after-text
        x = fold(' '.join(w[-k:]))
        if (x and close(x, fa[:len(x)], False)) or (not x and as_ and not as_[0].isalnum()): w = w[:-k]; break
    return ' '.join(w)
caret = lambda s: re.sub(r'\s+', ' ', s.replace('^', ' ^').replace('^', '')).strip()
rule, third, why = {}, [], collections.Counter()
for g in ids:
    p, s, e = pos[g]; t = N1[p]
    before = clean(t[max(0, s - 300):s]); after = clean(t[e:e + 300])
    ma, mb = core(marks(nf(A[g]['printed'])), before, after), core(marks(nf(B[g]['printed'])), before, after)
    xa, xb = core(caret(nf(A[g]['printed'])), before, after), core(caret(nf(B[g]['printed'])), before, after)
    if ma and ma == mb: ca = cb = ma                       # agree with the footnote marks taken out
    elif xa and xa == xb and re.fullmatch(r'\d+', xa): ca = cb = xa   # both read only a footnote number
    else: ca, cb = ma, mb
    if ca == cb and re.fullmatch(r'\d+', ca or ''):
        nx = re.match(r'\s*\[\^(\d+)\]:', t[e:e + 20]); pv = re.search(r'\[\^(\d+)\]:?[ \t]*$', t[max(0, s - 20):s])
        if (nx and nx.group(1) == ca) or (pv and pv.group(1) == ca): rule[g] = {'kind': 'F', 'fill': ''}; continue
        why['number, not by its own label'] += 1; third.append(g); continue
    if ca == cb and ca:
        if '?' in ca: why['?'] += 1; third.append(g); continue
        if not re.search(r'[A-Za-zĀ-ſḀ-ỿ]', ca): why['no letters'] += 1; third.append(g); continue
        if len(ca.split()) > 6: why['over six words'] += 1; third.append(g); continue
        rule[g] = {'kind': 'C' if (ca != marks(nf(A[g]['printed'])) or ca != marks(nf(B[g]['printed']))) else 'N', 'fill': ca}; continue
    why['cores differ'] += 1; third.append(g)
for g in rule: rule[g].update({'A': A[g]['printed'], 'B': B[g]['printed']})
print(collections.Counter(v['kind'] for v in rule.values()), 'third reader:', len(third), dict(why))
json.dump(rule, open('tb/rule.json', 'w'), ensure_ascii=False, indent=0); json.dump(third, open('tb/third.json', 'w'))
