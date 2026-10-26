# stats.py (26 Oct 2026, second session): pages, words, junk after the vowel sign i, Devanagari in Latin lines, IAST and look-alike letters of a PDF text layer. Usage: python3 stats.py file.pdf
import re, sys, json
import pymupdf
IAST = re.compile('[āīūṛṝḷṃṁḥṅñṭḍṇśṣĀĪŪṚṂḤṄÑṬḌṆŚṢ]'); LOOK = re.compile('[şņțţıļŗřŞŅȚŢĻŖŘ]')
def bad(c): return not ('ऀ' <= c <= 'ॿ' or c in ' \n.,;:-|।॥()')
def stats(fn):
    doc = pymupdf.open(fn); I = J = inj = dev = words = 0; iast = look = 0
    for pg in doc:
        t = pg.get_text()
        for m in re.finditer('ि(.)', t):
            I += 1; J += bad(m.group(1))
        dev += len(re.findall(r'[ऀ-ॿ]', t))
        for line in t.split('\n'):
            lat = len(re.findall(r'[A-Za-z]', line)); d = len(re.findall(r'[ऀ-ॿ]', line))
            if lat > 15 and lat > 4 * d: inj += d
        words += len(pg.get_text('words')); iast += len(IAST.findall(t)); look += len(LOOK.findall(t))
    return dict(pages=len(doc), words=words, short_i=I, junk_after_i=J, deva_in_latin=inj, deva_total=dev, iast=iast, lookalike=look)
if __name__ == '__main__':
    print(json.dumps(stats(sys.argv[1]), ensure_ascii=False))
