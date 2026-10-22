# Törzsök, round 2: the notes not yet converted, from readings of the page images (vres*.json): each note's number,
# first and last words, and the words before its call. Works on the notes as they are after round 1.
# Strict: certain readings; notes not running across pages; the note's first and last words found once, in order, in
# the page's text below the call; the call's words found once; nothing that already holds a footnote is touched.
import sys, os, re, json, glob, difflib, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = r'C:\Vaults\Obsidian Vault'
ORIG = os.path.join(VAULT, r".work\backup-footnotes-2026-10-18\Torzsok-round2\Library\Trika\The Doctrine of Magic Female Spirits' (Torzsok)")
QUOTES = set('\'’”"‘“')
def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)
def norm2(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]', '', w)
def words(s): return [norm2(w) for w in (s or '').split() if norm2(w)]
def matches(toks, want, lo, hi, thr=0.8):
    """all end positions e in [lo,hi) where want matches toks ending at e with ratio >= thr"""
    out = []
    if not want: return out
    W = ''.join(want)
    for e in range(lo, hi):
        s = max(lo, e - len(want) + 1)
        r = difflib.SequenceMatcher(None, ''.join(t[3] for t in toks[s:e + 1]), W).ratio()
        if r >= thr and difflib.SequenceMatcher(None, toks[e][3], want[-1]).ratio() >= 0.85: out.append((r, s, e))
    # keep local maxima only (a match and its neighbour are the same place)
    best = []
    for m in sorted(out, key=lambda x: -x[0]):
        if all(abs(m[2] - b[2]) > len(want) for b in best): best.append(m)
    return best
def run():
    rd = []
    for f in sorted(glob.glob(os.path.join(HERE, 'vres*.json'))): rd += json.load(open(f, encoding='utf-8'))
    rep = collections.Counter()
    files = {os.path.basename(f): open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(glob.escape(ORIG), '*.md'))}
    pagefile = {}
    for fn, t in files.items():
        for m in re.finditer(r'(?m)^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$', t): pagefile[int(m.group(2))] = fn
    used = {fn: set(re.findall(r'\[\^([^\]\s]+)\]', t)) for fn, t in files.items()}
    edits = collections.defaultdict(list)
    for c in rd:
        if c.get('number') in (None, '') : rep['run-on part'] += 1; continue
        try: N = int(str(c['number']).strip())
        except ValueError: rep['number not usable'] += 1; continue
        K = int(c['pdf'])
        if c.get('certain') is False: rep['uncertain reading'] += 1; continue
        if c.get('continues'): rep['note crosses a page'] += 1; continue
        if not c.get('call_before'): rep['call not on the page'] += 1; continue
        fn = pagefile.get(K)
        if not fn: rep['page not found'] += 1; continue
        t = files[fn]
        ms = [(m.start(), m.end(), int(m.group(2)), m.group(1)) for m in re.finditer(r'(?m)^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$', t)]
        i = [k for k, x in enumerate(ms) if x[2] == K][0]
        a = ms[i][1]; b = ms[i + 1][0] if i + 1 < len(ms) else len(t); plabel = ms[i][3]
        toks = [(a + m.start(), a + m.end(), m.group(0), norm2(m.group(0))) for m in re.finditer(r'\S+', t[a:b])]
        toks = [x for x in toks if x[3]]
        first, last = words(c.get('first')), words(c.get('last'))
        if len(first) < 3 or len(last) < 3: rep['too few words read'] += 1; continue
        fm = matches(toks, first[:5], 0, len(toks), 0.8)
        if len(fm) != 1: rep['note start not found once'] += 1; continue
        r1, s1, e1 = fm[0]
        lm = matches(toks, last[-5:], s1, min(len(toks), s1 + 400), 0.8)
        if len(lm) < 1: rep['note end not found'] += 1; continue
        r2, s2, e2 = lm[0] if len(lm) == 1 else min(lm, key=lambda x: x[2])
        if len(lm) > 1 and lm[1][0] >= lm[0][0] - 0.02: rep['note end ambiguous'] += 1; continue
        ns, ne = toks[s1][0], toks[e2][1]
        span = t[ns:ne]
        if '[^' in span or '*[' in span: rep['note span holds a footnote or marker'] += 1; continue
        others = [words(o.get('first'))[:4] for o in rd if int(o['pdf']) == K and o is not c and o.get('first')]
        sp_w = ''.join(norm2(x) for x in span.split()[3:])
        if any(len(o) >= 3 and ''.join(o) in sp_w for o in others): rep['another note inside the span'] += 1; continue
        # the note's own number just before its first word (digits or junk only): goes with the definition's label
        pre = re.search(r'(\S+)\s*$', t[a:ns])
        if pre and re.fullmatch(r'[\dIl|!?%°*]{1,4}', pre.group(1)) and re.search(r'\d', pre.group(1)):
            ns = a + pre.start(1)
        # the call, above the note
        # the call lies in the body: before the first of the page's notes (as the reader saw them)
        zone = s1
        for o in rd:
            if int(o['pdf']) != K or not o.get('first'): continue
            om = matches(toks, words(o['first'])[:5], 0, len(toks), 0.8)
            if len(om) == 1: zone = min(zone, om[0][1] - 1)
        cm = matches(toks, words(c['call_before'])[-5:], 0, max(0, zone), 0.8)
        if len(cm) != 1: rep['call words not found once'] += 1; continue
        cs, ce, w, _ = toks[cm[0][2]]
        if '[^' in w or t[ce:ce + 2] == '[^': rep['call word already has a footnote'] += 1; continue
        pw = c['call_before'].split()[-1]
        ptail = re.sub(r'^.*[^\W\d_]', '', pw); mtail = re.sub(r'^.*[^\W\d_]', '', w)
        let = w[:len(w) - len(mtail)] if mtail else w
        if not mtail.startswith(ptail): rep['call word differs'] += 1; continue
        rest = mtail[len(ptail):]
        if re.search(r'[^\W\d_]', rest): rep['call word differs'] += 1; continue
        keep = ''.join(m_.group(0) for m_ in re.finditer(r'\\[\[\]]|.', rest) if m_.group(0) in QUOTES or m_.group(0) in '.,;:)]}' or m_.group(0) in ('\\]', '\\['))
        idl = str(N) if str(N) not in used[fn] else '%d-p%s' % (N, re.sub(r'[^\w]', '', plabel))
        if idl in used[fn]: idl = '%d-pdf%d' % (N, K)
        body = t[toks[s1][0]:ne].replace('\n', ' ').strip()
        gl = re.match(r'^([\dIl|!?%°*]{1,3})(?=[A-Z‘"\'(])', body)          # the note's number glued to its first word
        if gl and re.search(r'\d', gl.group(1)) and (''.join({'I': '1', 'l': '1'}.get(x, x) for x in gl.group(1)) == str(N) or not re.search(r'[A-Za-z]', gl.group(1))):
            body = body[gl.end():]
        grp = [(ns, ne, '[^%s]: %s' % (idl, body), 'def'), (cs, ce, let + ptail + '[^%s]' % idl + keep, 'call')]
        if any(not (e1_ <= s2_ or e2_ <= s1_) for (s1_, e1_, _, _) in grp for (s2_, e2_, _, _) in edits[fn]):
            rep['overlaps another footnote'] += 1; continue
        used[fn].add(idl); edits[fn] += grp; rep['footnotes'] += 1
    out = {}
    for fn, es in edits.items():
        t = files[fn]
        for s, e, r_, kind in sorted(es, key=lambda x: -x[0]):
            if kind == 'def':
                before, after = t[:s], t[e:]
                pre = '' if before.endswith('\n\n') or before == '' else ('\n' if before.endswith('\n') else '\n\n')
                post = '' if after.startswith('\n') else '\n\n'
                t = before.rstrip(' ') + pre + r_ + post + after.lstrip(' ')
            else: t = t[:s] + r_ + t[e:]
        SUF = '; more footnotes from readings of the page images 18 Oct 2026'
        t = re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1) + (m.group(2)[:-1] + SUF + '"' if m.group(2).endswith('"') else m.group(2) + SUF), t, count=1, flags=re.M)
        out[fn] = t
    return out, rep
if __name__ == '__main__':
    out, rep = run(); print(dict(rep))
    os.makedirs(os.path.join(HERE, 'vout'), exist_ok=True)
    for fn, t in out.items(): open(os.path.join(HERE, 'vout', fn), 'w', encoding='utf-8', newline='\n').write(t)
