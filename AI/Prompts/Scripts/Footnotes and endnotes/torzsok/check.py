# Compare rewritten notes with the originals: structure, words, footnote pairing.
# usage: python check.py ORIG_FOLDER OUT_FOLDER   (only files present in OUT_FOLDER are compared)
import sys, os, re, glob, collections, unicodedata, difflib
MARK = re.compile(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg\d+$')
def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)
def split_fm(t):
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    return (m.group(1), t[m.end():]) if m else ('', t)
def strip_fn(t):
    t = re.sub(r'(?m)^\[\^[^\]\s]+\]:', ' ', t)      # definition labels (line start only)
    return re.sub(r'\[\^[^\]\s]+\]', '', t)          # references
def check(orig, new, name):
    probs = []
    fo, bo = split_fm(orig); fn, bn = split_fm(new)
    lo = [l for l in fo.split('\n') if not l.startswith('text_source:')]
    ln = [l for l in fn.split('\n') if not l.startswith('text_source:')]
    if lo != ln: probs.append('frontmatter differs')
    if '[[' in fn and fn.count('[[') != fo.count('[['): probs.append('link count in frontmatter changed')
    Lo, Ln = bo.split('\n'), bn.split('\n')
    mo = [l for l in Lo if MARK.match(l)]; mn = [l for l in Ln if MARK.match(l)]
    if mo != mn: probs.append('page markers differ')
    for i, l in enumerate(Ln):
        if MARK.match(l) and i + 1 < len(Ln) and Ln[i + 1].strip(): probs.append('marker not followed by blank: ' + l)
    ho = [l for l in Lo if re.match(r'^#{1,6} ', l)]; hn = [l for l in Ln if re.match(r'^#{1,6} ', l)]
    if ho != hn: probs.append('headings differ')
    # words (letters only), per file
    wo = collections.Counter(norm(w) for w in re.findall(r'\S+', strip_fn(bo)) if norm(w))
    wn = collections.Counter(norm(w) for w in re.findall(r'\S+', strip_fn(bn)) if norm(w))
    if wo != wn: probs.append('words differ: -%s +%s' % (dict(list((wo - wn).items())[:8]), dict(list((wn - wo).items())[:8])))
    # removed characters (non-space): only digits and junk marks may go
    co = collections.Counter(c for c in strip_fn(bo) if not c.isspace()); cn = collections.Counter(c for c in strip_fn(bn) if not c.isspace())
    removed = co - cn; added = cn - co
    bad_removed = {c: v for c, v in removed.items() if c.isalpha()}
    if bad_removed: probs.append('letters removed: %s' % bad_removed)
    if added: probs.append('characters added: %s' % dict(added))
    # footnote pairing
    refs = collections.Counter(m.group(1) for m in re.finditer(r'\[\^([^\]\s]+)\]', bn)
                               if not (m.end() < len(bn) and bn[m.end()] == ':' and (m.start() == 0 or bn[m.start() - 1] == '\n')))
    defs = collections.Counter(re.findall(r'^\[\^([^\]\s]+)\]:', bn, flags=re.M))
    bad = sorted(k for k in set(refs) | set(defs) if refs[k] != 1 or defs[k] != 1)
    if bad: probs.append('unpaired footnotes: %s' % bad[:12])
    return dict(name=name, refs=sum(refs.values()), defs=sum(defs.values()), removed=dict(removed), problems=probs)
if __name__ == '__main__':
    od, nd = sys.argv[1], sys.argv[2]
    tot = collections.Counter(); allrem = collections.Counter()
    for f in sorted(glob.glob(os.path.join(glob.escape(nd), '*.md'))):
        n = os.path.basename(f)
        r = check(open(os.path.join(od, n), encoding='utf-8').read(), open(f, encoding='utf-8').read(), n)
        tot['refs'] += r['refs']; tot['defs'] += r['defs']; allrem.update(r['removed'])
        print(n, '| refs', r['refs'], 'defs', r['defs'], '|', 'OK' if not r['problems'] else r['problems'])
    print('TOTAL', dict(tot), 'removed chars', dict(allrem))
