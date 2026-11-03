# mkmap2.py ID RULE [RULE ...] (2 Nov 2026, night 3): the --map for a note whose print numbers its footnotes per chapter
# (or per appendix) while the vault numbers them through the volume. Each RULE is LO-HI:K, for the reader's labels whose
# number part lies in LO..HI: the new label is the printed number + K (one offset per chapter, so the vault's numbering is
# the print's shifted by a constant); or LO-HI:keep. Labels the reader did not list (already real, calls in place) take
# the offset of the nearest listed labels when the two agree. A label that would repeat one already given (a page the scan
# repeats) gets the suffix r. Writes rd/ID/map.json; run review.py ID=0 first.
import json, sys, re, collections
H = '/home/claude/dyfn'; nid = sys.argv[1]
rules = []
for r in sys.argv[2:]:
    rng, k = r.split(':'); lo, hi = map(int, rng.split('-')); rules.append((lo, hi, k))
num = lambda lab: int(re.match(r'\d+', lab).group())
def rule(lab):
    for lo, hi, k in rules:
        if lo <= num(lab) <= hi: return k
    return None
O = json.load(open(f'{H}/rd/{nid}/ops.json', encoding='utf-8')); t = open(f'{H}/work/{nid}/out.md', encoding='utf-8').read()
order = []
for mm in re.finditer(r'\[\^([0-9A-Za-z]+)\](?!:)', t):
    if mm.group(1) not in order: order.append(mm.group(1))
printed = {str(e['n']): int(e['printed']) for e in O['per_note'] if str(e.get('printed', '')).isdigit()}
m, used, amb = {}, set(), []
off = {}
for lab in order:
    k = rule(lab)
    if k is None: amb.append((lab, 'no rule')); continue
    if k == 'keep': new = lab
    elif lab in printed: new = str(printed[lab] + int(k))
    else: new = None
    if new is None:
        # infer from neighbours: same chapter offset k means printed = label - reader's own offset; use neighbours' (new - old)
        prev = next((int(m[x]) - num(x) for x in reversed(order[:order.index(lab)]) if x in m and m[x].isdigit() and rule(x) == k), None)
        nxt = next((printed[x] + int(k) - num(x) for x in order[order.index(lab) + 1:] if x in printed and rule(x) == k and not re.search('[a-z]', x)), None)
        if prev is not None and (nxt is None or nxt == prev): new = str(num(lab) + prev)
        elif nxt is not None and prev is None: new = str(num(lab) + nxt)
        else: amb.append((lab, prev, nxt)); continue
    while new in used: new += 'r'
    used.add(new); m[lab] = new
json.dump(m, open(f'{H}/rd/{nid}/map.json', 'w'), indent=0)
print(nid, 'map', len(m), 'of', len(order), '| ambiguous', amb[:8], '| r-labels', [v for v in m.values() if v.endswith('r')][:8])
