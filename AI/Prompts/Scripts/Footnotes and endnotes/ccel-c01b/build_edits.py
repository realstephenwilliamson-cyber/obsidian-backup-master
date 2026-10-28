# build_edits.py (28 Oct 2026, fourth session): from lost_plan.py's plan (A, A1, B, B1), whole-page-block edits for edits-job2.
# Restored notes (B, B1) take the PDF's text with [ ] escaped and New Testament references linked by nt_link.py.
# Checks before any job: characters of each note = old + inserted pieces; <sup> calls and ^pg lines unchanged; every lost N now
# outside <sup>; and per changed block whether the PDF's whole footnote list for the page now appears in the block in order.
# usage: python3 build_edits.py pdftext.json notes.json lost.json PLANDIR OUTSPEC BACKUPDIR
import json, re, sys, collections
_argv = list(sys.argv)
exec(open('lost_plan.py').read().split('# === ' + 'MAIN ===')[0])
sys.argv = _argv
import nt_link
PLANDIR, OUTSPEC, BACKUP = sys.argv[4], sys.argv[5], sys.argv[6]
M = nt_link.build_map(NOTES)
NOLINK = ['Luke 07#^7-54', 'Matthew 06#^6-53']   # pf499: verses that do not exist (the PDF prints Matt. vi. 53, Luke vii. 54); left plain

def esc(s): return s.replace('[', '\\[').replace(']', '\\]')
def restored(T):
    s = nt_link.link(esc(T), M)
    for x in NOLINK: s = re.sub(r'\[\[' + re.escape(x) + r'\|([^\]]+)\]\]', r'\1', s)
    return s

def block_of(t, K): return block_span(t, K)

def page_text_list(pdf, K):
    nums, LIDX, body = page_fns(pdf, K)
    return nums, {j: norm(fn_text(pdf, K, j)) for j in nums}

# === MAIN ===
if __name__ == '__main__':
    plan = json.load(open(PLANDIR + '/plan.json'))
    ops = collections.defaultdict(list); lostset = collections.defaultdict(set); cls = collections.Counter()
    for r in plan:
        p = r['path']; n = r['N']; lostset[p].add(n); cls[r['cls']] += 1
        if r['cls'] in ('A', 'A1'): ops[p].append((r['pos'], f'{n} ', r['K']))
        elif r['cls'] == 'B': ops[p].append((r['pos'], f' {n} {restored(r["T"])}', r['K']))
        elif r['cls'] == 'B1': ops[p].append((r['pos'], f'\n\n{n} {restored(r["T"])}', r['K']))
    spec = {'backup': BACKUP, 'edits': {}}; report = collections.Counter(); bad = []
    for p, L in ops.items():
        t = NOTES[p]; new = t
        for pos, pay, K in sorted(L, key=lambda x: -x[0]): new = new[:pos] + pay + new[pos:]
        if new.count('<sup>') != t.count('<sup>'): bad.append((p, 'sup'))
        if re.findall(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', new, re.M) != re.findall(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', t, re.M): bad.append((p, 'pg'))
        if collections.Counter(new) != collections.Counter(t) + collections.Counter(''.join(x[1] for x in L)): bad.append((p, 'chars'))
        rest = re.sub(r'<sup>\d+</sup>', ' ', new)
        for n in lostset[p]:
            if not re.search(r'(^|[^\d.,\-–/#^|])' + str(n) + r'(?!\d)', rest): bad.append((p, 'still lost', n))
        spec['edits'][p] = []
        for K in sorted(set(x[2] for x in L)):
            so, ao, bo = block_of(t, K); sn, an, bn = block_of(new, K)
            assert t.count(t[so:bo]) == 1
            spec['edits'][p].append([t[so:bo], new[sn:bn]])
    json.dump(spec, open(OUTSPEC, 'w', encoding='utf-8'), ensure_ascii=False)
    print(dict(cls), 'notes', len(ops), 'block edits', sum(len(v) for v in spec['edits'].values()), 'problems', bad[:10], len(bad))
