# Deshpande: checks for linked endnote calls. usage: checklinks.py ORIG_FOLDER OUT_FOLDER
import sys, os, re, glob, collections, unicodedata
O, N = sys.argv[1], sys.argv[2]
MARK = re.compile(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg\d+$')
LINK = re.compile(r'\[\[Abhinavagupta 12 - Appendix - Notes and References#\^(n-\d+-\d+[a-z]?)\|[⁰¹²³⁴⁵⁶⁷⁸⁹ᴬᵃ]+\]\]')
BID = re.compile(r' \^(n-\d+-\d+[a-z]?)$', re.M)
def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)
def fm(t):
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S); return (m.group(1), t[m.end():]) if m else ('', t)
links = collections.Counter(); ids = collections.Counter(); removed = collections.Counter()
for f in sorted(glob.glob(os.path.join(glob.escape(N), '*.md'))):
    n = os.path.basename(f)
    a = open(os.path.join(O, n), encoding='utf-8').read(); b = open(f, encoding='utf-8').read()
    fa, ba = fm(a); fb, bb = fm(b)
    probs = []
    if [l for l in fa.split('\n') if not l.startswith('text_source:')] != [l for l in fb.split('\n') if not l.startswith('text_source:')]: probs.append('frontmatter')
    la, lb = ba.split('\n'), bb.split('\n')
    if [l for l in la if MARK.match(l)] != [l for l in lb if MARK.match(l)]: probs.append('markers')
    for i, l in enumerate(lb):
        if MARK.match(l) and i + 1 < len(lb) and lb[i + 1].strip(): probs.append('marker without blank line')
    if [l for l in la if l.startswith('#')] != [l for l in lb if l.startswith('#')]: probs.append('headings')
    for m in LINK.finditer(bb): links[m.group(1)] += 1
    for m in BID.finditer(bb): ids[m.group(1)] += 1
    sb = BID.sub('', LINK.sub('', bb))
    wa = collections.Counter(norm(w) for w in ba.split() if norm(w)); wb = collections.Counter(norm(w) for w in sb.split() if norm(w))
    if wa != wb: probs.append('words: -%s +%s' % (dict(wa - wb), dict(wb - wa)))
    ca = collections.Counter(c for c in ba if not c.isspace()); cb = collections.Counter(c for c in sb if not c.isspace())
    removed.update(ca - cb)
    if cb - ca: probs.append('added chars %s' % dict(cb - ca))
    print(n[:40], '| links', sum(1 for _ in LINK.finditer(bb)), '| ids', sum(1 for _ in BID.finditer(bb)), '|', probs or 'OK')
bad = [k for k in links if ids[k] != 1] + [k for k in ids if ids[k] != 1]
print('links', sum(links.values()), 'distinct targets', len(links), 'ids', sum(ids.values()), 'targets without exactly one id', bad,
      'ids without a link', [k for k in ids if not links[k]], 'removed chars', dict(removed))
