# offsets.py ID ... (2 Nov 2026, night 3): after review.py, label minus printed number for every footnote in the reader's
# per_note (relabelled as apply_ops did), grouped by offset with the first and last label of each group.
import json, sys
for nid in sys.argv[1:]:
    R = json.load(open(f'/home/claude/dyfn/work/{nid}/rep.json')); O = json.load(open(f'/home/claude/dyfn/rd/{nid}/ops.json')); rl = R['relabelled']
    d = {}
    for e in O.get('per_note', []):
        if str(e.get('printed', '')).isdigit():
            new = rl.get(str(e['n']), str(e['n']))
            if new.isdigit(): d.setdefault(int(new) - int(e['printed']), []).append(int(new))
    print(nid, R['numbers'], {k: (min(v), max(v), len(v)) for k, v in sorted(d.items())})
