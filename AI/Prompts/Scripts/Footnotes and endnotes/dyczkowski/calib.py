# calib.py (27 Oct 2026): compares a reader's converted note with the reference conversion of the same note (vol. 5 part 8, made
# 26 Oct by an Opus reader and checked), call by call: a call agrees when the last three words before it agree.
# Usage: calib.py READER_OUT REFERENCE PRE_JSON
import sys, json, re
a, b, pj = sys.argv[1:4]
W = lambda s: re.findall(r'[^\W\d_]+', s.lower())
def ctx(t):
    t = re.sub(r'(?m)^\[\^\d+\]:.*$', '', t)
    out = {}
    for m in re.finditer(r'\[\^(\d+)\](?!:)', t):
        before = re.sub(r'\[\^\d+\]', '', t[max(0, m.start() - 200):m.start()])
        out[int(m.group(1))] = W(before)[-3:]
    return out
A, B = ctx(open(a, encoding='utf-8').read()), ctx(open(b, encoding='utf-8').read())
pre = json.load(open(pj, encoding='utf-8')); real = set(pre['real_defs_before'])
plain_defs = set(pre['numbers']) - real
cands = sorted(n for n in B if n not in real)
agree = [n for n in cands if A.get(n) == B[n]]
dis = [(n, ' '.join(A.get(n, ['—'])), ' '.join(B[n])) for n in cands if A.get(n) != B[n]]
print('reference calls not real before: %d; reader agrees on %d (%.1f%%)' % (len(cands), len(agree), 100 * len(agree) / len(cands)))
print('of these, defs present in the old text (by the old numbering): %d' % len(plain_defs))
for d in dis: print(d)
