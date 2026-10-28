# filter_spec.py (28 Oct 2026, item 6): from pf418's spec (pagefill-spec re-run with per-note offsets) keep only the edits of
# chapter notes whose printed markers agree (one offset per numbering, none descending) and whose book passed the blind page
# reading (every read page shows the expected number, or no number on a fill page); write an edits-job2 spec and a list of the rest.
# usage: python3 filter_spec.py SPEC.json KEY.json READINGS.jsonl[,…] OUT_SPEC.json OUT_LEFT.json
import sys, json, re, os, collections
spec, keyf, reads, outs, outl = sys.argv[1:6]
S = json.load(open(spec)); K = json.load(open(keyf))
R = {}
for f in reads.split(','):
    for l in open(f):
        if l.strip(): j = json.loads(l); R[j['id']] = j
cons = lambda n: len(n['offs']['a']) <= 1 and len(n['offs']['r']) <= 1 and n['desc'] == 0
NC = {n['path']: n for n in S['notes']}
norm = lambda s: str(s).strip().lower()
bookbad = collections.defaultdict(list); bookread = collections.Counter()
HOLD = [h for h in (sys.argv[6].split('|') if len(sys.argv) > 6 else []) if h]
for i, k in K.items():
    r = R.get(i)
    if not r: bookbad[k['book']].append([i, 'not read']); continue
    p = norm(r['printed']); bookread[k['book']] += 1
    if p == norm(k['expect']): continue
    if p in ('none', 'unclear', 'noimage'): continue   # no number seen: no contradiction (a fill page may print none; an anchor may be a chapter opening)
    bookbad[k['book']].append([i, k['kind'], 'expected ' + k['expect'], 'read ' + r['printed'], r.get('note', '')])
byBase = collections.defaultdict(list)
for n in S['notes']: byBase[os.path.basename(n['path'])[:-3]].append(n)
out = {}; left = collections.defaultdict(list); cnt = collections.Counter()
for p, pairs in S['edits'].items():
    for o, nw in pairs:
        if p in NC: n = NC[p]; kind = 'marker' if o.startswith('*[PDF') else 'range'
        else:
            m = re.match(r'- \[\[([^\]|#]+)', o); c = [x for x in byBase.get(m.group(1).split('/')[-1], []) if x['book'] == p] if m else []
            n = c[0] if c else None; kind = 'label'
        why = None
        if n is None: why = 'chapter note not found'
        elif not cons(n): why = 'markers disagree in the note'
        elif bookbad.get(n['book']): why = 'book failed the page reading'
        elif any(h in n['book'] for h in HOLD): why = 'held by the lead'
        elif kind != 'label' or True:
            # printed values need a book reading unless the edit only names PDF pages
            needs = kind == 'marker' or (kind == 'range' and re.search(r'"[^"]+"', nw)) or (kind == 'label' and '(pp.' in nw)
            if needs and not bookread.get(n['book']): why = 'book not read'
        if why: left[why].append([p, o.strip()[:160], nw.strip()[:160]]); cnt[(kind, 'left')] += 1; continue
        out.setdefault(p, []).append([o, nw]); cnt[(kind, 'kept')] += 1
json.dump({'backup': '.work/backup-pagelabels-2026-10-28', 'edits': out}, open(outs, 'w'), ensure_ascii=False)
json.dump({'counts': {str(k): v for k, v in cnt.items()}, 'bookbad': bookbad, 'left': left}, open(outl, 'w'), ensure_ascii=False, indent=1)
print(dict(cnt)); print('books failing:', len(bookbad), '; notes in spec:', len(out))
