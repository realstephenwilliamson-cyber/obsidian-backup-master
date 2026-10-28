# C-01(b) detector (28 Oct 2026): page blocks of the CCEL NPNF notes whose footnote zone holds numbers whose calls are in the next page block.
import json, re, sys
D = json.load(open(sys.argv[1]))
PG = re.compile(r'^\*\[p\. [^\]]+\]\* \^pg(\d+)\s*$')
CALL = re.compile(r'<sup>(\d+)</sup>|\[\^(\d+)\](?!:)')
def order(p): return int(re.search(r' (\d\d) - ', p).group(1))
books = {}
for p in D: books.setdefault('A' if 'Augustine' in p else 'C', []).append(p)
out = []
for b, ps in books.items():
    blocks = []  # (path, K, start_line, end_line, lines)
    for p in sorted(ps, key=order):
        L = D[p].split('\n'); cur = None
        for i, s in enumerate(L):
            m = PG.match(s)
            if m:
                if cur: cur[3] = i; blocks.append(cur)
                cur = [p, int(m.group(1)), i, None]
        if cur: cur[3] = len(L); blocks.append(cur)
    def info(bl):
        p, K, a, e = bl; L = D[p].split('\n')[a:e]
        calls = set(); zone = []
        for j, s in enumerate(L):
            for m in CALL.finditer(s): calls.add(int(m.group(1) or m.group(2)))
            if re.match(r'^(\d{1,4} |\[\^\d+\]:)', s) or (zone and s.strip() and not re.match(r'^(\d+\\\.|\*|“|[A-Z])', s)): zone.append((a + j + 1, s))
        return calls, zone
    I = [info(bl) for bl in blocks]
    for k in range(len(blocks) - 1):
        calls, zone = I[k]; ncalls, _ = I[k + 1]
        hits = []
        for ln, s in zone:
            nums = [int(x) for x in re.findall(r'(?<![\d.:^\-])\b(\d{2,4})\b(?![\d\]])', re.sub(r'\[\[[^\]]*\]\]', ' ', s))]
            h = [n for n in nums if n in ncalls and n not in calls and n > 9]
            if h: hits.append((ln, h))
        if hits:
            out.append({'book': b, 'path': blocks[k][0], 'K': blocks[k][1], 'nextpath': blocks[k + 1][0], 'nextK': blocks[k + 1][1], 'hits': hits,
                        'missing_in_next': sorted(n for n in ncalls if not any(n in h for _, h in hits) and not any(re.search(r'(?<!\d)%d(?!\d)' % n, s) for _, s in I[k + 1][1]))[:20]})
json.dump(out, open('cands.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'blocks with forward-displaced numbers')
for o in out: print(o['book'], o['path'].split('/')[-1][:30], o['K'], '->', o['nextK'], 'same' if o['path']==o['nextpath'] else 'NEXT NOTE', [h for _, h in o['hits']])
