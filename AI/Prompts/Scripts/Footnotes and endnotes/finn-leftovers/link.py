# Finn leftovers: turn the notes still standing as 'N\.' paragraphs into footnotes, from calls and note ends read
# from the page images (calls_*.json). Strict: certain readings only; the note's first words must match its paragraph,
# its last words must be found (the definition ends there); the call's words must be found once in the body.
import sys, os, re, json, glob, difflib, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = r'C:\Vaults\Obsidian Vault'
ORIG = os.path.join(VAULT, r'.work\backup-footnotes-2026-10-18\Finn-leftovers\Library\Trika\The Kulacudamani Tantra and The Vamakesvara Tantra (Finn)')
MARK = re.compile(r'^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$')
QUOTES = set('\'’”"‘“')

def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)

def words(s): return [norm(w) for w in (s or '').split() if norm(w)]

def find_seq(toks, want, lo=0, hi=None):
    """best place (end token index) where the token sequence want occurs in toks[lo:hi]; returns (ratio, end)"""
    hi = len(toks) if hi is None else hi; best = (0, None)
    if not want: return best
    W = ''.join(want)
    for e in range(lo, hi):
        s = max(lo, e - len(want) + 1)
        r = difflib.SequenceMatcher(None, ''.join(t[3] for t in toks[s:e + 1]), W).ratio()
        last = difflib.SequenceMatcher(None, toks[e][3], want[-1]).ratio()
        if r + 0.5 * last > best[0] + 0.5 * (1 if best[1] is not None else 0) and last >= 0.6:
            if r > best[0]: best = (r, e)
    return best

def run():
    calls = []
    for f in sorted(glob.glob(os.path.join(HERE, 'calls_*.json'))): calls += json.load(open(f, encoding='utf-8'))
    rep = collections.Counter(); log = []
    files = {os.path.basename(f): open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(glob.escape(ORIG), '*.md'))}
    J = json.load(open(os.path.join(HERE, 'leftovers.json')))
    edits = collections.defaultdict(list)
    used = {fn: set(re.findall(r'\[\^([^\]\s]+)\]', t)) for fn, t in files.items()}
    for c in calls:
        K, N = int(c['pdf']), int(c['number'])
        if not c.get('call_before'): rep['call not found in image'] += 1; continue
        if c.get('certain') is False: rep['uncertain reading'] += 1; continue
        if re.search(r'(?i)continu|next page|previous page|onto', c.get('note') or ''): rep['note crosses a page'] += 1; continue
        fn = J[str(K)]['f']; t = files[fn]
        # the page section
        ms = [(m.start(), int(m.group(2)), m.group(1)) for m in re.finditer(r'(?m)^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$', t)]
        idx = [i for i, x in enumerate(ms) if x[1] == K]
        if not idx: rep['page not found'] += 1; continue
        a = ms[idx[0]][0]; b = ms[idx[0] + 1][0] if idx[0] + 1 < len(ms) else len(t)
        sec = t[a:b]; plabel = ms[idx[0]][2]
        toks = [(a + m.start(), a + m.end(), m.group(0), norm(m.group(0))) for m in re.finditer(r'\S+', sec)]
        toks = [x for x in toks if x[3] or re.search(r'\d', x[2])]
        # the note's paragraph
        lab = [m for m in re.finditer(r'(?m)^\s*%d\\\.\s' % N, sec)]
        if len(lab) != 1: rep['note paragraph not found once'] += 1; continue
        ns = a + lab[0].start()
        first = words(c.get('note_first')); last = words(c.get('note_last'))
        ti = next(i for i, x in enumerate(toks) if x[0] >= a + lab[0].end())
        r1 = difflib.SequenceMatcher(None, ''.join(x[3] for x in toks[ti:ti + len(first)]), ''.join(first)).ratio() if first else 0
        if r1 < 0.75: rep['note first words do not match'] += 1; log.append((K, N, 'first', r1)); continue
        # the next numbered paragraph or page end limits the search for the last words
        nxt = re.search(r'(?m)^\s*\d{1,4}\\\.\s', sec[lab[0].end():])
        lim = a + lab[0].end() + nxt.start() if nxt else b
        hi = next((i for i, x in enumerate(toks) if x[0] >= lim), len(toks))
        rl, el = find_seq(toks, last, ti, hi)
        if el is None or rl < 0.8: rep['note last words not found'] += 1; log.append((K, N, 'last', rl)); continue
        ne = toks[el][1]
        # the call: in the body, before the notes (the text above the first note paragraph on the page)
        first_note = re.search(r'(?m)^\s*\d{2,4}\\\.\s', sec)
        body_hi = next((i for i, x in enumerate(toks) if x[0] >= ns), len(toks))
        bw = words(c['call_before'])
        rc, ec = find_seq(toks, bw, 0, body_hi)
        if ec is None or rc < 0.8: rep['call words not found'] += 1; log.append((K, N, 'call', rc)); continue
        # unique? another place nearly as good -> skip
        rc2, ec2 = find_seq(toks, bw, 0, max(0, ec - len(bw)))
        rc3, ec3 = find_seq(toks, bw, ec + 1, body_hi)
        if max(rc2, rc3) >= rc - 0.05: rep['call words ambiguous'] += 1; continue
        cs, ce, w, _ = toks[ec]
        if '[^' in w or (ec + 1 < len(toks) and toks[ec + 1][2].startswith('[^')):
            rep['call word already has a footnote'] += 1; continue
        # printed punctuation at the end of the word stays; digits and junk after it go (quote marks stay)
        pw = c['call_before'].split()[-1]
        ptail = re.sub(r'^.*[^\W\d_]', '', pw)
        mtail = re.sub(r'^.*[^\W\d_]', '', w)
        let = w[:len(w) - len(mtail)] if mtail else w
        if mtail.startswith(ptail): rest = mtail[len(ptail):]
        else: rest = None
        if rest is None or re.search(r'[^\W\d_]', rest): rep['call word differs'] += 1; log.append((K, N, 'word', w, pw)); continue
        keepq = ''.join(ch for ch in rest if ch in QUOTES or ch in '.,;:)')
        new_w = let + ptail + '[^@]' + keepq
        # a separate junk token right after (' 61') holding the number
        nt = toks[ec + 1] if ec + 1 < len(toks) else None
        extra = None
        if nt and not nt[3] and re.fullmatch(r'[\d?!*°]{1,4}[.,;:]?', nt[2]) and nt[0] < ns:
            extra = (nt[0], nt[1], re.sub(r'[^.,;:]', '', nt[2]))
        idl = str(N) if str(N) not in used[fn] else '%d-p%s' % (N, re.sub(r'[^\w]', '', plabel))
        used[fn].add(idl)
        body = t[ns:ne]
        body = re.sub(r'^\s*%d\\\.\s+' % N, '', body).replace('\n', ' ').strip()
        grp = [(ns, ne, '[^%s]: %s' % (idl, body), 'def'), (cs, ce, new_w.replace('[^@]', '[^%s]' % idl), 'call')]
        if extra: grp.append((extra[0], extra[1], extra[2], 'junk'))
        # a footnote goes in whole or not at all: none of its edits may overlap an edit already taken
        taken = edits[fn]
        if any(not (e1 <= s2 or e2 <= s1) for (s1, e1, _, _) in grp for (s2, e2, _, _) in taken):
            rep['overlaps another footnote'] += 1; used[fn].discard(idl); continue
        edits[fn] += grp
        rep['footnotes'] += 1
    out = {}
    for fn, es in edits.items():
        t = files[fn]; last_s = len(t) + 1
        for s, e, r_, kind in sorted(es, key=lambda x: -x[0]):
            if e > last_s: raise SystemExit('overlap left in %s at %d' % (fn, s))
            if kind == 'def':
                after = t[e:]
                sep = '' if after.startswith('\n') else '\n\n'
                t = t[:s] + r_ + sep + after.lstrip(' ')
            else:
                t = t[:s] + r_ + t[e:]
            last_s = s
        SUF = '; remaining notes linked from the page images 18 Oct 2026'
        t = re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1) + (m.group(2)[:-1] + SUF + '"' if m.group(2).endswith('"') else m.group(2) + SUF), t, count=1, flags=re.M)
        out[fn] = t
    return out, rep, log

if __name__ == '__main__':
    out, rep, log = run()
    print(dict(rep))
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    for fn, t in out.items(): open(os.path.join(HERE, 'out', fn), 'w', encoding='utf-8', newline='\n').write(t)
    json.dump(log, open(os.path.join(HERE, 'linklog.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
