# merge_ops.py (28 Oct 2026): joins the op lists of two page readers who shared one note (each did a range of its pages)
# into rd/ID/ops.json, after checking that each reader's ops lie on its own pages (a move's `after` may point earlier).
# Usage: merge_ops.py ID PART:FIRSTPDF:LASTPDF [PART:FIRSTPDF:LASTPDF ...]
import sys, json, os, re
H = '/home/claude/dyfn'; nid = sys.argv[1]
pre = json.load(open(f'{H}/work/{nid}/pre.json', encoding='utf-8'))
marks = sorted((ml, pg) for pg, lab, ml in pre['pages_all'])
def page_of(line):
    pg = None
    for ml, p in marks:
        if ml <= line: pg = p
    return pg
out = {'note': nid, 'ops': [], 'problems': [], 'per_note': [], 'parts': []}
for spec in sys.argv[2:]:
    part, a, b = spec.split(':'); a, b = int(a), int(b)
    D = json.load(open(f'{H}/rd/{part}/ops.json', encoding='utf-8'))
    bad = [o for o in D['ops'] if not (a <= (page_of(o['line']) or 0) <= b)]
    out['parts'].append({'part': part, 'pages': [a, b], 'ops': len(D['ops']), 'outside_range': len(bad)})
    for o in bad: print('OUTSIDE', part, o.get('line'), page_of(o.get('line')), str(o)[:120])
    out['ops'] += D['ops']; out['problems'] += ['[%s] %s' % (part, p) for p in D.get('problems', [])]; out['per_note'] += D.get('per_note', [])
os.makedirs(f'{H}/rd/{nid}', exist_ok=True)
json.dump(out, open(f'{H}/rd/{nid}/ops.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out['parts']), 'ops', len(out['ops']), 'problems', len(out['problems']), 'per_note', len(out['per_note']))
