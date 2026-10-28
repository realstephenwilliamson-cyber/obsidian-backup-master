# s_move.py (28 Oct 2026, fifth session): for the CCEL page blocks that still differ from the PDF's footnote list (diff-blocks.json),
# a footnote number that stands as a bare number elsewhere in its page block (inside its own note's text, e.g. 3966 before "οὐκ", or
# after it) is moved to just before its own note's text, where the move is unique: exactly one bare occurrence of the number whose
# removal leaves the note's text (from the PDF, accent-blind) once in the block; both places in the page's footnote zone (from its
# first line that opens with a number of the page's list), the new place at a word boundary and outside any link. Writes moves-new.json [{path, K, N, del, ins}].
# usage: python3 s_move.py pdftext.json notes.json lost.json
import sys, json, re, collections
here = '/home/claude/cc/s'; sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], 'plan', 'out', 'bk']
exec(open(here + '/build_edits.py').read().split('# === ' + 'MAIN ===')[0].replace("exec(open('lost_plan.py')", "exec(open(here + '/lost_plan.py')"))
R = json.load(open('diff-blocks.json'))
def bare(t, a, b, n):
    out = []
    for m in re.finditer(r'(?<![\w\d^#|/.\-–])' + str(n) + r'(?![\w\d])', t[a:b]):
        i = a + m.start()
        pre = t[max(0, i - 400):i]
        if pre.rfind('[[') > pre.rfind(']]') or pre.rfind('<sup>') > pre.rfind('</sup>'): continue
        out.append(i)
    return out
moves, held, cnt = [], [], collections.Counter()
for r in R:
    p, K = r['path'], r['K']; t = NOTES[p]; pdf = AUG if 'Augustine' in p else CHR
    nums, TX = page_text_list(pdf, K)
    for k in r['kinds']:
        if ':' not in k: continue
        n = int(k.split(':')[1]); s0, a, b = block_of(t, K)
        T = TX.get(n, '');
        if len(T) < 4: cnt['short'] += 1; continue
        ok = []
        # the footnote zone: from the first line of the block that opens with a number of the page's footnote list
        zm = None
        for mz in re.finditer(r'(?m)^(\d{1,4}) ', t[a:b]):
            if int(mz.group(1)) in nums: zm = a + mz.start(); break
        if zm is None: cnt['no zone'] += 1; continue
        for i in bare(t, zm, b, n):
            L = len(str(n)); j = i + L
            if j < len(t) and t[j] == ' ': j += 1
            elif i > 0 and t[i - 1] == ' ': i -= 1
            t2 = t[:i] + t[j:]; d = j - i
            BP, BI, BB = plain(t2, a, b - d)
            occ = [o.start() for o in re.finditer(re.escape(T), BP)]
            if len(occ) != 1: continue
            pos = BB[occ[0]]
            if pos == i: continue
            if pos < zm or t2[pos - 1] not in ' \n': continue                     # only in the zone, at a word boundary
            pre = t2[max(0, pos - 400):pos]
            if pre.rfind('[[') > pre.rfind(']]'): continue                       # never inside a link   # the number already stood right before its text (only a space/markup issue)
            t3 = t2[:pos] + f'{n} ' + t2[pos:]
            if plain(str(n) + T)[0] in plain(t3, a, b - d + L + 1)[0]: ok.append({'del': [i, j], 'ins': pos, 'new': t3})
        if len(ok) == 1:
            m = ok[0]; moves.append({'path': p, 'K': K, 'N': n, 'del': m['del'], 'ins': m['ins'], 'kind': k.split(':')[0]}); cnt['move ' + k.split(':')[0]] += 1
            NOTES[p] = m['new']
        else: cnt['no unique move (%d) %s' % (len(ok), k.split(':')[0])] += 1
json.dump(moves, open('moves-new.json', 'w'), ensure_ascii=False, indent=0)
json.dump(NOTES, open('notes_m.json', 'w'), ensure_ascii=False)
print(dict(cnt))
