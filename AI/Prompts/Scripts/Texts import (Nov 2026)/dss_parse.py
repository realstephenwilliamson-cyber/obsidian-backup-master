"""dss_parse.py (9 Nov 2026): García Martínez & Tigchelaar, The Dead Sea Scrolls Study Edition (Brill 1999 PDF) ->
one record per manuscript of the Index of Manuscripts: header (siglum, short name, title), the edition/bibliography lines,
and the English translation cut into sections (Col./Frag.) and numbered lines; biblical manuscripts get their list of
fragments and verses. Usage: python3 -I dss_parse.py <pdf> <outdir>   (needs <outdir>/index.json from dss_index.py)"""
import fitz, re, json, sys, collections
d = fitz.open(sys.argv[1]); OUT = sys.argv[2]; OFF = 24
E = [e for e in json.load(open(OUT + '/index.json')) if 'siglum' in e and e['siglum'] != 'index']
for e in E: e['siglum'] = e['siglum'].rstrip(',')
HEB = re.compile(r'[֐-׿]')
SIG = r'(?:pap|pap)?\d{0,2}Q[\w.]+|CD-[AB]|CTL(?:evi)?(?: ar)?|Mas\w+|XQ\w+|KhQ\w*|\d{1,2}Q\d+[a-z]*-\d+'
TOK = r'(?:' + SIG + r')(?: title| ar)?(?:\s?\+\s?(?:' + SIG + r'))*'
RUN = re.compile(r'^' + TOK + r'(?:,\s*' + TOK + r')*$')
def page_lines(i):
    t = d[i].get_text(); L = [l.rstrip() for l in t.split('\n')]
    if L and L[0].strip().isdigit(): L = L[1:]
    while L and not L[-1].strip(): L.pop()
    if L and (RUN.match(L[-1].strip()) or L[-1].strip().lower() in ('index of titles', 'index of manuscripts')): L = L[:-1]
    return L
NP = d.page_count
odd = []; even = []   # (printed page, line)
for i in range(OFF + 1, 1310 + OFF):
    pg = i - OFF
    for l in page_lines(i): (odd if pg % 2 else even).append((pg, l))
def is_header(line, e):
    s = line.strip()
    if not re.match(re.escape(e['siglum']) + r'(\s|$)', s): return False
    rest = re.sub(r'\s+', '', s[len(e['siglum']):])
    if e['short'] and rest.startswith(('(' + re.sub(r'\s+', '', e['short']))[:6]): return True
    t = re.sub(r'\s+', '', e['title'])[:8]
    return t and t in rest[:40] or (not rest)
def locate(stream, ents):
    pos = {}; j = 0
    for k, e in enumerate(ents):
        lo = j
        for jj in range(lo, len(stream)):
            pg, l = stream[jj]
            if pg > e['page'] + 4: break
            if pg >= e['page'] - 1 and is_header(l, e): pos[k] = jj; j = jj + 1; break
    return pos
po = locate(odd, E); pe = locate(even, E)
allp = []
for i in range(OFF + 1, 1310 + OFF):
    for l in page_lines(i):
        if not HEB.search(l): allp.append((i - OFF, l))
pa = locate(allp, E)
REF = re.compile(r'^(?:[1-3] )?[A-Z][a-z]+\.? \d+:\d|^\?$|^(?:[1-3] )?[A-Z][a-z]+ \d+$')
HEADRE = re.compile(r'^(Cols?\.\s*[IVXLCivxlc\d]|Frags?\.\s*[\dA-Za-z]|Fragments?\s+\d|Title$|Wads?\s+\d|Col\s[IVXLC]|Frg\.\s*\d)')
def roman(s):
    R = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100}; s = s.lower(); t = 0
    for i, c in enumerate(s):
        v = R[c]; t += -v if i + 1 < len(s) and R[s[i + 1]] > v else v
    return t
def key_of(label):
    lab = label.split('(=')[0].strip().rstrip('.')
    m = re.match(r'^Cols?\.\s*([IVXLCivxlc]+)\b', lab)
    if m: return str(roman(m.group(1)))
    m = re.match(r'^Frags?\.\s*(\d+)[a-z]?(?:\s*[-–+,]\s*\d+[a-z]?)*\s*(?:col\.\s*)?([ivxlc]+)?\b', lab, re.I)
    if m:
        k = 'f' + m.group(1)
        if m.group(2) and re.fullmatch(r'[ivxlc]+', m.group(2), re.I): k += 'c' + str(roman(m.group(2)))
        if re.search(r'\bverso\b', lab): k += 'v'
        return k
    if lab == 'Text': return 't'
    return re.sub(r'[^A-Za-z0-9]+', '', lab)[:12].lower() or 's'
def join(lines):
    s = ''
    for l in lines:
        l = l.strip()
        if not l: continue
        if s.endswith('-') and re.match(r'[a-z]', l) and re.search(r'[a-z]-$', s): s = s[:-1] + l
        else: s = (s + ' ' + l) if s else l
    return re.sub(r'\s+', ' ', s).strip()
NUMRE = re.compile(r'(?:(?<=\s)|^)(\d{1,2})(?:-(\d{1,2}))?(?=\s|\[|\(|‹|\{|«|$)')
def split_lines(text):
    """numbered lines in sequence: returns (pre, [(n, n2, text)])"""
    out = []; pre = ''; cur = None; last = None; i = 0
    for m in NUMRE.finditer(text):
        n = int(m.group(1)); n2 = int(m.group(2)) if m.group(2) else None
        ok = (last is None and n <= 40 and (m.start() == 0 or not text[:m.start()].strip() or len(out) == 0)) or (last is not None and (n == last + 1 or (n2 is None and last < n <= last + 2)))
        if last is None and m.start() > 0 and text[:m.start()].strip(): ok = ok and n <= 3  # a first number after some text
        if not ok: continue
        seg = text[i:m.start()].strip()
        if cur is None: pre = seg
        else: out.append((cur[0], cur[1], seg))
        cur = (n, n2); last = n2 or n; i = m.end()
    if cur is None: return text.strip(), []
    out.append((cur[0], cur[1], text[i:].strip()))
    return pre, out
recs = []
for k, e in enumerate(E):
    r = dict(e); r['pages'] = []
    # even-page header block (edition, PAM, parallels, bibliography start): Latin lines up to the first section or Hebrew line
    if k in pe:
        j = pe[k] + 1; nxt = min([v for kk, v in pe.items() if kk > k] or [len(even)])
        blk = []; bib = []
        while j < nxt:
            pg, l = even[j]
            if HEB.search(l) or HEADRE.match(l.strip()): break
            blk.append(l); j += 1
        r['even_head'] = blk
        # biblical lists: Frag. N + reference pairs anywhere in the even span
        pairs = []; L = [l.strip() for _, l in even[pe[k] + 1:nxt]]
        for a, b in zip(L, L[1:]):
            if re.match(r'^Frags?\.?,?\s*[\dA-Za-z]', a) and re.match(r'^(?:[1-3] )?[A-Z][a-z]+\.? \d+:\d|^\?$|^(?:[1-3] )?[A-Z][a-z]+ \d+$', b): pairs.append((a, b))
        if pairs: r['biblical'] = pairs
    if k in po:
        j = po[k] + 1; nxt = min([v for kk, v in po.items() if kk > k] or [len(odd)])
        span = odd[j:nxt]
        secs = []; cur = {'label': None, 'raw': [], 'pages': []}
        for pg, l in span:
            s = l.strip()
            if HEADRE.match(s) and len(s) < 120 and not re.match(r'^Frags?\.?\s*\d+\s*$', s) or re.match(r'^(Cols?\.|Frags?\.)\s*[\dIVXLCivxlc]', s) and len(s) < 120:
                secs.append(cur); cur = {'label': s, 'raw': [], 'pages': [pg]}; continue
            if pg not in cur['pages']: cur['pages'].append(pg); cur['raw'].append(f'\x01{pg}\x01')
            cur['raw'].append(l)
        secs.append(cur)
        # no section heading before the numbered lines (a single sheet): split the first part at its line 1
        raw0 = secs[0]['raw']
        i1 = next((ix for ix, x in enumerate(raw0) if re.match(r'^\s*1\s+\S', x)), None)
        if i1 is not None:
            secs.insert(1, {'label': 'Text', 'raw': raw0[i1:], 'pages': secs[0]['pages']}); secs[0] = dict(secs[0], raw=raw0[:i1])
        r['odd_pre'] = [x for x in secs[0]['raw'] if not x.startswith('\x01')]
        out = []; seen = collections.Counter()
        for sct in secs[1:]:
            text = join(sct['raw'])
            pre, lines = split_lines(text)
            key = key_of(sct['label']); seen[key] += 1
            if seen[key] > 1: key += 'abcdefghij'[seen[key] - 2]
            out.append({'label': sct['label'], 'key': key, 'pre': pre, 'lines': lines})
        r['sections'] = out
        r['pages'] = sorted({pg for pg, _ in span})
    if k in pa and not any(sx['lines'] for sx in r.get('sections', [])):
        j = pa[k] + 1; nxt = min([v for kk, v in pa.items() if kk > k] or [len(allp)])
        L = [l.strip() for _, l in allp[j:nxt]]; pairs = []
        for a, b in zip(L, L[1:]):
            if re.match(r'^Frags?\.?,?\s*[\dA-Za-z]', a) and REF.match(b): pairs.append((a, b))
        if pairs: r['biblical'] = pairs; r.pop('sections', None)
    recs.append(r)
for a, b in zip(recs, recs[1:]):
    if a.get('short') and a['short'] == b.get('short') and a['page'] == b['page'] and not any(x['lines'] for x in a.get('sections', [])) and b.get('sections'):
        a['sections'] = b.pop('sections'); a['pages'] = b.get('pages', []); a['merged'] = b['siglum']; b['merged_into'] = a['siglum']
recs = [r for r in recs if 'merged_into' not in r]
json.dump(recs, open(OUT + '/records.json', 'w'), ensure_ascii=False)
st = collections.Counter(('odd' if 'sections' in r else '') + ('+bib' if 'biblical' in r else '') + ('+even' if 'even_head' in r else '') for r in recs)
print(len(recs), st, sum(len(r.get('sections', [])) for r in recs), sum(len(s['lines']) for r in recs for s in r.get('sections', [])))
