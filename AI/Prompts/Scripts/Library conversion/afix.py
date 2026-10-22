"""ä/å (and Ä/Å) that Tesseract's Latin model reads for ā (Ā) in OCR'd Indological text.
Per word:  äā/āä/åā/āå -> ā (the letter read twice);  a word that becomes a common English
word with d (anä -> and, shoulä -> should: typescript d read as ä) takes d;  a German word
(5+ letters, wordfreq zipf >= 2.0: Universität, Beiträge, Bäumer) keeps ä;  otherwise ä/å -> ā, Ä/Å -> Ā.
Books whose text marks Vedic accents (å may be ā́ or á there) are left alone by the caller."""
import re
from functools import lru_cache
from wordfreq import zipf_frequency as _z

WORD = re.compile(r'[^\W\d_]*[äåÄÅ][^\W\d_]*')
NOT_D = {'dna'}
DOUBLE = re.compile(r'[äå]ā|ā[äå]|[ÄÅ]Ā|Ā[ÄÅ]')


@lru_cache(maxsize=None)
def fix_word(w):
    w2 = DOUBLE.sub(lambda m: 'Ā' if m.group().isupper() else 'ā', w)
    if not re.search('[äåÄÅ]', w2): return w2
    if 'ä' in w2 and len(w2) >= 5 and (_z(w2, 'de') >= 2.0 or _z(w2.lower(), 'de') >= 2.0): return w2
    d = re.sub('[äå]', 'd', w2)
    if len(d) >= 3 and d.lower() not in NOT_D and not re.search('[āīūṛṭḍṇśṣṃḥñ]', d) and _z(d.lower(), 'en') >= 3.5: return d
    return w2.translate(str.maketrans({'ä': 'ā', 'å': 'ā', 'Ä': 'Ā', 'Å': 'Ā'}))


def fix_text(t):
    n = [0]
    def rep(m):
        w = m.group(); r = fix_word(w)
        if r != w: n[0] += 1
        return r
    return WORD.sub(rep, t), n[0]
