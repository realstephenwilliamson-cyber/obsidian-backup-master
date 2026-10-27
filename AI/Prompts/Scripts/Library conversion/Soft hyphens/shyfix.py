# shyfix.py (26 Oct 2026, third session): soft hyphens (U+00AD) in born-digital PDFs whose text layer stores every hyphen as U+00AD.
# The vault's converter drops U+00AD, so hard hyphens are lost ("selfmanifestation"); the same layer also keeps leftover line-break
# hyphens from the print inside reflowed lines ("Ku-mar", "manifes-tation"), which are soft. For each U+00AD inside a line:
#   hard if both sides are numbers or roman numerals, if the second part is capitalised, or if both parts are very common words (zipf >= 6);
#   otherwise soft (left joined, as the note has it) when the joined word is English (zipf >= 2) or occurs joined elsewhere in the book,
#   unless the hyphenated form occurs 3+ times and the joined word is rare (zipf < 3); everything else hard. Doubt leaves the note as it is.
# Output per PDF page: [(joined, hyphenated, decision)], used to patch the note's page block (only where the counts agree).
import sys, re, json, collections
import pymupdf as fitz
from wordfreq import zipf_frequency as zf
NUM = re.compile(r'^(\d+[a-z]?|[ivxlcdm]+|[IVXLCDM]+)$')
def tokens(pdf):
    d = fitz.open(pdf); pages = []
    for pg in d:
        toks = []
        for b in pg.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                s = ''.join(sp['text'] for sp in l['spans']).replace('\xa0', ' ')
                for m in re.finditer(r"[\w’']+(?:­[\w’']+)+", s): toks.append(m.group(0))
        pages.append((toks, pg.get_text().replace('\xa0', ' ')))
    return pages
def decide(pages):
    plain = collections.Counter(); shycount = collections.Counter()
    for toks, txt in pages:
        for w in re.findall(r"[\w’']+", re.sub(r"[\w’']+(?:­[\w’']+)+", ' ', txt)): plain[w.lower()] += 1
        for t in toks: shycount[t.replace('­', '-').lower()] += 1
    def word(w): return zf(w.lower(), 'en') >= 3 and len(w) >= 3
    out = []
    for toks, txt in pages:
        res = []
        for t in toks:
            parts = t.split('­'); cur = parts[0]; seps = []
            for i, b in enumerate(parts[1:]):
                a = cur.split('-')[-1]; rest = ''.join(parts[i + 1:])
                if NUM.match(a) and NUM.match(b): seps.append('-'); cur += '-' + b; continue
                J = a + b
                if b[:1].isupper(): soft = False
                elif zf(a.lower(), 'en') >= 6 and zf(b.lower(), 'en') >= 6: soft = False
                elif zf(J.lower(), 'en') >= 2.0 or plain[J.lower()] > 0: soft = shycount[(a + '-' + b).lower()] < 3 or zf(J.lower(), 'en') >= 3
                else: soft = False
                seps.append('' if soft else '-'); cur += ('' if soft else '-') + b
            res.append((''.join(parts), cur, t))
        out.append(res)
    return out
if __name__ == '__main__':
    pages = tokens(sys.argv[1]); dec = decide(pages)
    json.dump(dec, open(sys.argv[2], 'w'), ensure_ascii=False)
    c = collections.Counter('hard' if '-' in h else 'soft' for p in dec for (j, h, t) in p)
    print(sys.argv[1].split('/')[-1], dict(c))
