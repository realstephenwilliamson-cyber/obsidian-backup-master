# s_star.py (28 Oct 2026, third session after 28 Oct): in the CCEL books, footnote numbers printed by the converter AFTER their own
# note's text ("ταπεινν, LXX. 588 Isa. lxvi. 2" where the PDF has "588 ταπεινν, LXX." and "589 Isa. lxvi. 2"), mostly where a
# note begins with Greek. For every page block and every footnote j of that PDF page: if "j"+T_j is not in the block (compared
# without whitespace/markup) but T_j+"j" is, exactly once, and T_j occurs once, and the digits are a token of their own, the
# number moves to before its text (the number and the whitespace after it are cut; "j " goes before the text).
# usage: python3 s_star.py pdftext.json notes.json lost.json OUTDIR   -> OUTDIR/notes_s.json, OUTDIR/sstar.json
import json, re, sys, collections
argv0 = list(sys.argv)
exec(open('build_edits.py').read().split('# === ' + 'MAIN ===')[0])
OUT = argv0[4]
def cut_span(t, ds, de):
    # the number and the space after it; at a line end, the space before it; alone on a line, the line break after it
    if t[de:de + 1] == ' ':
        e = de
        while t[e:e + 1] == ' ': e += 1
        return ds, e
    if t[ds - 1:ds] == ' ': return ds - 1, de
    if t[ds - 1:ds] == '\n' and t[de:de + 2] == '\n\n' and not t[de + 2:].lstrip('\n').startswith('*['): return ds, de + 2
    return ds, de
NS = {}; moves = []; bad = []
for p, t0 in NOTES.items():
    t = t0; pdf = AUG if 'Augustine' in p else CHR
    for m in list(re.finditer(r'^\*\[[^\]]+\]\* \^pg(\d+)\s*$', t0, re.M)):
        K = int(m.group(1))
        if str(K) not in P[pdf]: continue
        nums, LIDX, body = page_fns(pdf, K)
        for j in nums:
            done = False
            for MODE in ('base', 'skel'):
                Tj = fn_text(pdf, K, j); TXj = norm(Tj) if Tj else ''
                if len(TXj) < (4 if MODE == 'base' else 6): continue
                s0, a, b = block_of(t, K); BP, BI, BB = plain(t, a, b)
                if (str(j) + TXj) in BP: break
                if BP.count(TXj) != 1 or BP.count(TXj + str(j)) != 1: continue
                o = BP.index(TXj + str(j)); q = o + len(TXj)
                ds, de = BI[q], BI[q + len(str(j)) - 1] + 1
                if t[ds:de] != str(j) or t[ds - 1].isdigit() or (de < len(t) and t[de].isdigit()): continue
                ins = BB[o]
                ds, e = cut_span(t, ds, de)
                t = t[:ins] + f'{j} ' + t[ins:ds] + t[e:]
                done = True; break
            MODE = 'base'
            if not done: continue
            moves.append({'path': p, 'K': K, 'j': j})
    nw = lambda s: collections.Counter(c for c in s if not c.isspace())
    if nw(t) != nw(t0) or t.count('<sup>') != t0.count('<sup>'): bad.append(p)
    NS[p] = t
json.dump(NS, open(OUT + '/notes_s.json', 'w'), ensure_ascii=False)
json.dump(moves, open(OUT + '/sstar.json', 'w'), ensure_ascii=False, indent=0)
print('numbers moved', len(moves), 'notes', len(set(m['path'] for m in moves)), 'blocks', len(set((m['path'], m['K']) for m in moves)), 'problems', bad)
