# pagecmp.py OLD NEW: per page, English-word-list hits in each layer; lists pages where NEW has clearly fewer
import sys, re, unicodedata, pymupdf, json
W = set()
for fn in ['/usr/share/dict/american-english-large', '/usr/share/dict/british-english-large']:
    W |= {w.strip().lower() for w in open(fn, encoding='utf-8', errors='ignore')}
def norm(w): return ''.join(c for c in unicodedata.normalize('NFD', w) if not unicodedata.combining(c)).lower()
def hits(t): return sum(1 for w in re.findall(r"[A-Za-zÀ-ɏḀ-ỿ]{3,}", t) if norm(w) in W)
a = pymupdf.open(sys.argv[1]); b = pymupdf.open(sys.argv[2]); worse = []
for i in range(a.page_count):
    ha, hb = hits(a[i].get_text()), hits(b[i].get_text())
    if hb < 0.9 * ha and ha - hb >= 15: worse.append((i + 1, ha, hb))
print(sys.argv[2].split('/')[-1], 'pages where NEW has clearly fewer list words:', len(worse), worse)
json.dump([w[0] for w in worse], open(sys.argv[2] + '.worse.json', 'w'))
