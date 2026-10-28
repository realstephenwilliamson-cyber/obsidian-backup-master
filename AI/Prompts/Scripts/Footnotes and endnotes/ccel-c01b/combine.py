# combine.py (28 Oct 2026, third session after 28 Oct): original notes -> s_star.py's moves (notes_s.json, sstar.json) -> lost_plan.py and
# build_edits.py run on notes_s.json (PLANDIR/plan.json, PLANDIR/spec_s.json) -> one edits-job2 spec of whole page blocks taken from the ORIGINAL
# notes (c01c-edits3.json). Checks: <sup> calls and ^pg lines unchanged, no non-space character lost, text outside the blocks identical;
# and how many page blocks match the PDF's footnote list before and after.
# usage (in the folder holding the scripts and notes_s.json, sstar.json, PLANDIR/): python3 combine.py pdftext.json notes_s.json lost.json PLANDIR x y notes.json
import json, re, sys, collections
argv0 = list(sys.argv)
exec(open('build_edits.py').read().split('# === ' + 'MAIN ===')[0])
ORIG = json.load(open(argv0[7]))   # the original notes.json (pf495)
NS = json.load(open('notes_s.json')); spec_s = json.load(open(argv0[4] + '/spec_s.json')); moves = json.load(open('sstar.json'))
plan = json.load(open(argv0[4] + '/plan.json'))
FINAL = {}
for p, t in NS.items():
    for old, new in spec_s['edits'].get(p, []): assert t.count(old) == 1; t = t.replace(old, new)
    FINAL[p] = t
blocks = collections.defaultdict(set)
# pass P: a number that is right before its own note's text but ends the previous paragraph ("…—R.\] 1993\n\n\[R.V. …") starts its note's paragraph instead
paramoves = []
for p in list(FINAL):
    t = FINAL[p]; pdf = AUG if 'Augustine' in p else CHR
    for m in list(re.finditer(r'^\*\[[^\]]+\]\* \^pg(\d+)\s*$', t, re.M)):
        K = int(m.group(1))
        if str(K) not in P[pdf]: continue
        nums, LIDX, body = page_fns(pdf, K)
        for j in nums:
            Tj = fn_text(pdf, K, j); TXj = norm(Tj) if Tj else ''
            if len(TXj) < 3: continue
            s0, a, b = block_of(t, K); BP, BI, BB = plain(t, a, b)
            if BP.count(str(j) + TXj) != 1 or BP.count(TXj) != 1: continue   # a text printed twice on the page (Chrysostom p. 266, 891/892) is left alone
            k = BP.find(str(j) + TXj); ds = BI[k]; de = BI[k + len(str(j)) - 1] + 1; ins = BB[k + len(str(j))]
            if t[ds:de] != str(j) or t[ds - 1:ds] != ' ' or '\n' not in t[de:ins] or t[de:ins].strip(): continue
            t = t[:ds - 1] + t[de:ins] + f'{j} ' + t[ins:]
            paramoves.append({'path': p, 'K': K, 'j': j}); blocks[p].add(K)
    FINAL[p] = t
json.dump(paramoves, open('paramoves.json', 'w'), ensure_ascii=False, indent=0)
print('numbers moved to the start of their paragraph', len(paramoves))
for m in moves: blocks[m['path']].add(m['K'])
for r in plan: blocks[r['path']].add(r['K'])
spec = {'backup': '.work/backup-c01c-2026-10-28', 'edits': {}}; bad = []
mk = lambda s: re.findall(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', s, re.M)
nw = lambda s: collections.Counter(c for c in s if not c.isspace())
for p, Ks in blocks.items():
    o, f = ORIG[p], FINAL[p]
    if o.count('<sup>') != f.count('<sup>') or mk(o) != mk(f): bad.append((p, 'sup/pg'))
    added = nw(f) - nw(o); removed = nw(o) - nw(f)
    if removed: bad.append((p, 'removed', dict(removed)))
    spec['edits'][p] = []
    for K in sorted(Ks):
        so, ao, bo = block_of(o, K); sf, af, bf = block_of(f, K)
        assert o.count(o[so:bo]) == 1
        spec['edits'][p].append([o[so:bo], f[sf:bf]])
    # all text outside the changed blocks identical
    oo, ff = o, f
    for old, new in spec['edits'][p]: oo = oo.replace(old, new)
    if oo != f: bad.append((p, 'outside blocks differs'))
json.dump(spec, open('c01c-edits3.json', 'w'), ensure_ascii=False)
# whole-book comparison with the PDF lists, before and after
cnt = collections.Counter()
for p in ORIG:
    pdf = AUG if 'Augustine' in p else CHR
    for m in re.finditer(r'^\*\[[^\]]+\]\* \^pg(\d+)\s*$', ORIG[p], re.M):
        K = int(m.group(1))
        if str(K) not in P[pdf]: continue
        nums, TX = page_text_list(pdf, K)
        if not nums: continue
        full = ''.join(str(j) + TX.get(j, '') for j in nums)
        for lab, t in (('before', ORIG[p]), ('after', FINAL.get(p, ORIG[p]))):
            s0, a, b = block_of(t, K); cnt[lab + (' match' if full in plain(t, a, b)[0] else ' differ')] += 1
print('notes', len(spec['edits']), 'block edits', sum(len(v) for v in spec['edits'].values()), 'problems', bad[:5], len(bad))
print(dict(cnt))
