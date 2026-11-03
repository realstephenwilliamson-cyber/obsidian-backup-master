# mkmap.py ID [MIN] [APPENDIX_OFFSET] (2 Nov 2026, night 3): the --map for apply_ops.py from the reader's per_note: every label
# whose printed number is MIN or more (default 1) gets the printed number; a smaller printed number (an appendix whose print
# starts again) gets printed + APPENDIX_OFFSET if given, else keeps the note's label. Writes rd/ID/map.json and lists the labels
# in the reader's output that the map does not cover (run review.py ID=0 first) and any label given twice.
import json, sys, re, collections
H = '/home/claude/dyfn'; nid = sys.argv[1]; MIN = int(sys.argv[2]) if len(sys.argv) > 2 else 1; AOFF = int(sys.argv[3]) if len(sys.argv) > 3 else None
O = json.load(open(f'{H}/rd/{nid}/ops.json', encoding='utf-8')); m = {}
for e in O['per_note']:
    if not str(e.get('printed', '')).isdigit(): continue
    p = int(e['printed']); n = str(e['n'])
    m[n] = str(p) if p >= MIN else (str(p + AOFF) if AOFF is not None else n)
t = open(f'{H}/work/{nid}/out.md', encoding='utf-8').read()
labs = set(re.findall(r'\[\^([0-9A-Za-z]+)\]', t))
# labels the reader did not list (footnotes already real, whose calls were in place): the offset of the nearest listed labels
# before and after (in call order), when the two agree
order = []
for mm in re.finditer(r'\[\^([0-9A-Za-z]+)\](?!:)', t):
    if mm.group(1) not in order: order.append(mm.group(1))
off = lambda k: int(m[k]) - int(k) if k.isdigit() and m[k].isdigit() else None
amb = []
for i, k in enumerate(order):
    if k in m or not k.isdigit(): continue
    b = next((off(x) for x in reversed(order[:i]) if x in m and off(x) is not None), None)
    a = next((off(x) for x in order[i + 1:] if x in m and off(x) is not None), None)
    if b is not None and (a is None or a == b): m[k] = str(int(k) + b)
    elif a is not None and b is None: m[k] = str(int(k) + a)
    else: amb.append((k, b, a))
if amb: print('AMBIGUOUS (offsets before/after differ):', amb)
dup = [v for v, c in collections.Counter(m.values()).items() if c > 1]
json.dump(m, open(f'{H}/rd/{nid}/map.json', 'w'), indent=0)
print(nid, 'map', len(m), '| labels in text', len(labs), '| not in map', sorted(labs - set(m))[:20], '| given twice', dup[:10])
