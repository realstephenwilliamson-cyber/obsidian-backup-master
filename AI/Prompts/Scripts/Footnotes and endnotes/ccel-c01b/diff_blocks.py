# diff_blocks.py (28 Oct 2026, fifth session): lists every page block of the two CCEL books whose footnotes do not match the PDF's
# footnote list (compared as combine.py does: the run "N text N+1 text ..." from the pdf.js text, accent- and space-blind, inside the
# block's plain text), with a first sorting: lost (a number of held-27.json), inside (a footnote number that stands inside its own
# note's text in the block), greek (the PDF's note holds Greek letters the block lacks), other. Writes diff-blocks.json.
# usage: python3 diff_blocks.py pdftext.json notes.json lost.json (run in the folder that holds the ccel-c01b scripts' copies)
import sys, json, re, collections
here = sys.argv[0].rsplit('/', 1)[0] if '/' in sys.argv[0] else '.'
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], 'plan', 'out', 'bk']
import os; cwd = os.getcwd(); os.chdir(here)
src = open('build_edits.py').read().split('# === ' + 'MAIN ===')[0]
os.chdir(cwd)
src = src.replace("exec(open('lost_plan.py')", "exec(open(here + '/lost_plan.py')")
exec(src)
HELD = {(h['path'], h['N']) for h in LOST}
GR = re.compile(r'[Ͱ-Ͽἀ-῿]')
rows = []; cnt = collections.Counter()
for p, t in NOTES.items():
    pdf = AUG if 'Augustine' in p else CHR
    for m in re.finditer(r'^\*\[[^\]]+\]\* \^pg(\d+)\s*$', t, re.M):
        K = int(m.group(1))
        if str(K) not in P[pdf]: continue
        nums, TX = page_text_list(pdf, K)
        if not nums: continue
        full = ''.join(str(j) + TX.get(j, '') for j in nums)
        s0, a, b = block_of(t, K); blk = plain(t, a, b)[0]
        if full in blk: cnt['match'] += 1; continue
        kinds = []
        if any((p, j) in HELD for j in nums): kinds.append('lost')
        for j in nums:
            pj = plain(str(j) + TX.get(j, ''))[0]
            if pj not in blk and plain(TX.get(j, ''))[0] in blk: kinds.append('number-misplaced:%d' % j)
            elif GR.search(TX.get(j, '')) and plain(TX.get(j, ''))[0] not in blk: kinds.append('greek:%d' % j)
            elif pj not in blk: kinds.append('text-differs:%d' % j)
        cnt['differ'] += 1
        rows.append({'path': p, 'K': K, 'nums': nums, 'kinds': kinds})
json.dump(rows, open('diff-blocks.json', 'w'), ensure_ascii=False, indent=0)
print(dict(cnt))
k1 = collections.Counter(k.split(':')[0] for r in rows for k in set(x.split(':')[0] for x in r['kinds']))
print('blocks by kind', dict(k1))
print('footnotes by kind', dict(collections.Counter(k.split(':')[0] for r in rows for k in r['kinds'])))
