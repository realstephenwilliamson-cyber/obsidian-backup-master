# Share of Latin-script tokens (lowercased, diacritics stripped) found in the English word lists; a rough OCR-quality measure for English prose.
import sys, re, unicodedata, pymupdf
W = set()
for fn in ['/usr/share/dict/american-english-large', '/usr/share/dict/british-english-large']:
    try: W |= {w.strip().lower() for w in open(fn, encoding='utf-8', errors='ignore')}
    except FileNotFoundError: pass
def norm(w): return ''.join(c for c in unicodedata.normalize('NFD', w) if not unicodedata.combining(c)).lower()
def score(fn, pages=None):
    d = pymupdf.open(fn); tot = ok = 0
    for i, pg in enumerate(d):
        if pages and i + 1 not in pages: continue
        for w in re.findall(r"[A-Za-zÀ-ɏḀ-ỿ]{3,}", pg.get_text()):
            tot += 1; ok += norm(w) in W
    return tot, ok, round(100 * ok / max(tot, 1), 1)
if __name__ == '__main__':
    for f in sys.argv[1:]: print(f.split('/')[-1], score(f))
