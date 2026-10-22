# Dhvanyaloka round 2: notes not yet converted, from readings of the page images (r2res*.json). Works on the vault's
# notes as they are now (after round 1 and the quote fix). Same strict rules as Törzsök round 2, plus: a note may run
# over pages within one note file (page markers and running heads stay after the definition); a call is looked for
# only outside note paragraphs and definitions.
import sys, os, re, json, glob, difflib, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = r'C:\Vaults\Obsidian Vault'
ORIG = os.path.join(VAULT, r'.work\backup-footnotes-2026-10-18\Dhvanyaloka-round2\Library\Trika\The Dhvanyaloka of Anandavardhana with the Locana (Anandavardhana)')
MARK = re.compile(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg\d+$')
RH = re.compile(r'^\s*\\?\[?\s*[§S]\s*\d+[.\-]\d+|^\s*\d{1,3}\s*\\?\[?\s*[§S]\s*\d')
QUOTES = set('\'’”"‘“')
def norm2(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]', '', w)
def words(s): return [norm2(w) for w in (s or '').split() if norm2(w)]
def matches(toks, want, lo, hi, thr=0.8):
    out = []
    if not want: return out
    W = ''.join(want)
    for e in range(lo, hi):
        s = max(lo, e - len(want) + 1)
        r = difflib.SequenceMatcher(None, ''.join(t[3] for t in toks[s:e + 1]), W).ratio()
        if r >= thr and difflib.SequenceMatcher(None, toks[e][3], want[-1]).ratio() >= 0.85: out.append((r, s, e))
    best = []
    for m in sorted(out, key=lambda x: -x[0]):
        if all(abs(m[2] - b[2]) > len(want) for b in best): best.append(m)
    return best
def run():
    rd = []
    for f in sorted(glob.glob(os.path.join(HERE, 'r2res*.json'))): rd += json.load(open(f, encoding='utf-8'))
    rep = collections.Counter()
    files = {os.path.basename(f): open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(glob.escape(ORIG), '*Translation and Notes*.md'))}
    # token streams per file, with page and kind (note paragraph / definition / text)
    T = {}; pagefile = {}
    for fn, t in files.items():
        toks = []; K = None; kind = 'text'; prev_blank = True
        pos = 0
        for line in t.split('\n'):
            m = re.search(r'\^pg(\d+)$', line)
            if MARK.match(line): K = int(m.group(1)); pagefile.setdefault(K, fn)
            elif line.strip() and K:
                if prev_blank: kind = 'def' if line.startswith('[^') else ('note' if re.match(r'^\s*\d{1,2}\\?\.\s', line) else 'text')
                if not RH.match(line):
                    for mm in re.finditer(r'\S+', line):
                        n = norm2(mm.group(0))
                        if n: toks.append((pos + mm.start(), pos + mm.end(), mm.group(0), n, K, kind))
            prev_blank = not line.strip()
            pos += len(line) + 1
        T[fn] = toks
    used = {fn: set(re.findall(r'\[\^([^\]\s]+)\]', t)) for fn, t in files.items()}
    edits = collections.defaultdict(list)
    for c in rd:
        try: N = int(c['number'])
        except (TypeError, ValueError): rep['number not usable'] += 1; continue
        if c.get('certain') is False: rep['uncertain reading'] += 1; continue
        if not c.get('first') or not c.get('call_before'): rep['note or call not read'] += 1; continue
        try: Kn, Kl, Kc = int(c['note_page']), int(c['last_page']), int(c['call_page'])
        except (TypeError, ValueError, KeyError): rep['pages not given'] += 1; continue
        fn = pagefile.get(Kn)
        if not fn or pagefile.get(Kl) != fn or pagefile.get(Kc) != fn: rep['call or note in another file'] += 1; continue
        idl = '%s-%d' % (c['block'], N)
        if idl in used[fn]: rep['already converted'] += 1; continue
        toks = T[fn]; t = files[fn]
        first, last = words(c['first']), words(c['last'])
        if len(first) < 3 or len(last) < 3: rep['too few words read'] += 1; continue
        lo = next((i for i, x in enumerate(toks) if x[4] >= Kn), len(toks)); hi = next((i for i, x in enumerate(toks) if x[4] > Kn), len(toks))
        fm = matches(toks, first[:5], lo, hi)
        if len(fm) != 1: rep['note start not found once'] += 1; continue
        s1 = fm[0][1]
        # the match may begin one word late (the note's first word sits before a line break or after its label)
        for back in (1, 2):
            if s1 - back >= 0 and toks[s1 - back][3] == first[0] and toks[s1][3] != first[0]:
                s1 -= back; break
        if toks[s1][5] == 'def': rep['note start inside a definition'] += 1; continue
        hi2 = next((i for i, x in enumerate(toks) if x[4] > Kl), len(toks))
        lm = matches(toks, last[-5:], s1, hi2)
        if not lm: rep['note end not found'] += 1; continue
        if len(lm) > 1: rep['note end ambiguous'] += 1; continue
        e2 = lm[0][2]
        ns, ne = toks[s1][0], toks[e2][1]
        span = t[ns:ne]
        if '[^' in span or re.search(r'(?m)^#', span): rep['span holds a footnote or heading'] += 1; continue
        sp_w = ''.join(norm2(x) for x in span.split()[3:])
        others = [words(o['first'])[:4] for o in rd if o.get('block') == c['block'] and o is not c and o.get('first')]
        if any(len(o) >= 3 and ''.join(o) in sp_w for o in others): rep['another note inside the span'] += 1; continue
        pre = re.search(r'(\S+)\s*$', t[:ns])
        if pre and re.fullmatch(r'[\dIlOS|!?%°*]{1,3}\\?[.,]?', pre.group(1)) and re.search(r'\d', pre.group(1)):
            ns = pre.start(1)
        # the call: outside note paragraphs and definitions, on its page
        clo = next((i for i, x in enumerate(toks) if x[4] >= Kc), len(toks)); chi = next((i for i, x in enumerate(toks) if x[4] > Kc), len(toks))
        cand = [x for x in matches(toks, words(c['call_before'])[-5:], clo, chi) if toks[x[2]][5] == 'text']
        if len(cand) != 1: rep['call words not found once'] += 1; continue
        cs, ce, w = toks[cand[0][2]][:3]
        if '[^' in w or t[ce:ce + 2] == '[^': rep['call word already has a footnote'] += 1; continue
        pw = c['call_before'].split()[-1]
        ptail = re.sub(r'^.*[^\W\d_]', '', pw); mtail = re.sub(r'^.*[^\W\d_]', '', w)
        let = w[:len(w) - len(mtail)] if mtail else w
        if not mtail.startswith(ptail): rep['call word differs'] += 1; continue
        rest = mtail[len(ptail):]
        if re.search(r'[^\W\d_]', rest): rep['call word differs'] += 1; continue
        keep = ''.join(m_.group(0) for m_ in re.finditer(r'\\[\[\]]|.', rest) if m_.group(0) in QUOTES or m_.group(0) in '.,;:)]}|' or m_.group(0) in ('\\]', '\\['))
        # the definition: the note's lines joined; page markers and running heads that fell inside stay after it
        lines = t[ns:ne].split('\n')
        keep_lines = [l for l in lines if MARK.match(l) or RH.match(l)]
        body = ' '.join(l.strip() for l in lines if l.strip() and not MARK.match(l) and not RH.match(l))
        ml = re.match(r'^\s*([\dIlOS|!?%°*]{1,3})\\?[.,]?\s*', body)
        if ml and re.search(r'\d', ml.group(1)): body = body[ml.end():]
        grp = [(ns, ne, ('[^%s]: %s' % (idl, body.strip()), keep_lines), 'def'), (cs, ce, let + ptail + '[^%s]' % idl + keep, 'call')]
        if any(not (e1_ <= s2_ or e2_ <= s1_) for (s1_, e1_, _, _) in grp for (s2_, e2_, _, _) in edits[fn]):
            rep['overlaps another footnote'] += 1; continue
        used[fn].add(idl); edits[fn] += grp; rep['footnotes'] += 1
    out = {}
    for fn, es in edits.items():
        t = files[fn]
        for s, e, r_, kind in sorted(es, key=lambda x: -x[0]):
            if kind == 'def':
                d_, kl = r_
                before, after = t[:s], t[e:]
                pre = '' if before.endswith('\n\n') or before == '' else ('\n' if before.endswith('\n') else '\n\n')
                post = ''.join('\n\n' + l for l in kl)
                after = re.sub(r'^(\s*\d{1,3})\.(\s)', r'\1\\.\2', after.lstrip(' '), count=1)
                sep = '' if after.startswith('\n\n') else ('\n' if after.startswith('\n') else '\n\n')
                t = before.rstrip(' ') + pre + d_ + post + sep + after
            else: t = t[:s] + r_ + t[e:]
        SUF = '; more notes made footnotes from readings of the page images 18 Oct 2026'
        t = re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1) + (m.group(2)[:-1] + SUF + '"' if m.group(2).endswith('"') else m.group(2) + SUF), t, count=1, flags=re.M)
        out[fn] = t
    return out, rep
if __name__ == '__main__':
    out, rep = run(); print(dict(rep))
    os.makedirs(os.path.join(HERE, 'r2out'), exist_ok=True)
    for fn, t in out.items(): open(os.path.join(HERE, 'r2out', fn), 'w', encoding='utf-8', newline='\n').write(t)
