# compose.py (28 Oct 2026, fifth session): the vault's notes (notes.json) -> s_move.py's moves (notes_m.json) -> lost_plan.py's plan on
# notes_m.json (PLANDIR/plan.json; entries whose number already stands bare in the page's footnote zone are dropped, so no number is
# doubled) -> one edits-job2 spec of whole page blocks taken from the vault's notes. Checks: <sup> calls and ^pg lines unchanged,
# no non-space character lost except the moved numbers' (re-inserted), text outside the blocks identical; page blocks matching the
# PDF's footnote list before and after.  usage: python3 compose.py pdftext.json notes.json lost2.json PLANDIR OUTSPEC BACKUP
import sys, json, re, collections
here = '/home/claude/cc/s'; A = list(sys.argv); sys.argv = [A[0], A[1], 'notes_m.json', A[3], A[4], A[5], A[6]]
exec(open(here + '/build_edits.py').read().split('# === ' + 'MAIN ===')[0].replace("exec(open('lost_plan.py')", "exec(open(here + '/lost_plan.py')"))
ORIG = json.load(open(A[2])); NM = NOTES; MOVES = json.load(open('moves-new.json')); plan = json.load(open(PLANDIR + '/plan.json'))
def zone_bare(t, K, n):
    s0, a, b = block_of(t, K); pdf = AUG if 'Augustine' in t[:0] else None
    return [m.start() for m in re.finditer(r'(?<![\w\d^#|/.\-–])' + str(n) + r'(?![\w\d])', t[a:b]) if not (t[a:a + m.start()].rfind('<sup>') > t[a:a + m.start()].rfind('</sup>')) and not (t[a:a + m.start()].rfind('[[') > t[a:a + m.start()].rfind(']]'))]
keep, dropped = [], []
for r in plan:
    t = NM[r['path']]; s0, a, b = block_of(t, r['K'])
    # the footnote zone of the block: from its first line opening with a number of the page's list
    pdf = AUG if 'Augustine' in r['path'] else CHR; nums, TX = page_text_list(pdf, r['K'])
    zm = next((a + m.start() for m in re.finditer(r'(?m)^(\d{1,4}) ', t[a:b]) if int(m.group(1)) in nums), a)
    bare = [m for m in re.finditer(r'(?<![\w\d^#|/.\-–])' + str(r['N']) + r'(?![\w\d])', t[zm:b]) if not (t[zm:zm + m.start()].rfind('[[') > t[zm:zm + m.start()].rfind(']]'))]
    (dropped if bare else keep).append(r)
ops = collections.defaultdict(list); cls = collections.Counter()
for r in keep:
    p = r['path']; n = r['N']; cls[r['cls']] += 1
    if r['cls'] in ('A', 'A1'): ops[p].append((r['pos'], f'{n} ', r['K']))
    elif r['cls'] == 'B': ops[p].append((r['pos'], f' {n} {restored(r["T"])}', r['K']))
    elif r['cls'] == 'B1': ops[p].append((r['pos'], f'\n\n{n} {restored(r["T"])}', r['K']))
FINAL = dict(NM)
for p, L in ops.items():
    new = NM[p]
    for pos, pay, K in sorted(L, key=lambda x: -x[0]): new = new[:pos] + pay + new[pos:]
    FINAL[p] = new
blocks = collections.defaultdict(set)
for m in MOVES: blocks[m['path']].add(m['K'])
for r in keep: blocks[r['path']].add(r['K'])
spec = {'backup': A[6], 'edits': {}}; bad = []
mk = lambda s: re.findall(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', s, re.M)
nw = lambda s: collections.Counter(c for c in s if not c.isspace())
for p, Ks in blocks.items():
    o, f = ORIG[p], FINAL[p]
    if o.count('<sup>') != f.count('<sup>') or mk(o) != mk(f): bad.append((p, 'sup/pg'))
    if nw(o) - nw(f): bad.append((p, 'removed', dict(nw(o) - nw(f))))
    spec['edits'][p] = []
    for K in sorted(Ks):
        so, ao, bo = block_of(o, K); sf, af, bf = block_of(f, K)
        assert o.count(o[so:bo]) == 1
        spec['edits'][p].append([o[so:bo], f[sf:bf]])
    oo = o
    for old, new in spec['edits'][p]: oo = oo.replace(old, new)
    if oo != f: bad.append((p, 'outside blocks differs'))
json.dump(spec, open(A[5], 'w'), ensure_ascii=False)
json.dump(FINAL, open('notes_final.json', 'w'), ensure_ascii=False)
json.dump({'kept': keep, 'dropped_number_present': dropped}, open('plan-kept.json', 'w'), ensure_ascii=False, indent=0)
cnt = collections.Counter()
for p in ORIG:
    pdf = AUG if 'Augustine' in p else CHR
    for m in re.finditer(r'^\*\[[^\]]+\]\* \^pg(\d+)\s*$', ORIG[p], re.M):
        K = int(m.group(1))
        if str(K) not in P[pdf]: continue
        nums, TX = page_text_list(pdf, K)
        if not nums: continue
        full = ''.join(str(j) + TX.get(j, '') for j in nums)
        for lab, t in (('before', ORIG[p]), ('after', FINAL[p])):
            s0, a, b = block_of(t, K); cnt[lab + (' match' if full in plain(t, a, b)[0] else ' differ')] += 1
print('moves', len(MOVES), 'plan kept', dict(cls), 'dropped (number already in the zone)', len(dropped))
print('notes', len(spec['edits']), 'block edits', sum(len(v) for v in spec['edits'].values()), 'problems', bad[:5], len(bad))
print(dict(cnt))
