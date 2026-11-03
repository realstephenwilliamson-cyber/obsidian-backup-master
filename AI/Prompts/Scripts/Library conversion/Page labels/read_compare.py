# read_compare.py (3 Nov 2026, audit corrections, D-06): render, shuffle and compare page-number readings for markers that break their run.
#   python3 read_compare.py render ITEMS.json PDFMAP.json OUTDIR [SEED]
#       ITEMS.json: [{path, K, label, expected}, ...] (from run-break-survey.js or descent-survey.js); PDFMAP.json: {note path: source_pdf}.
#       Renders each target page and its PDF neighbours (K-1, K+1) at 110 dpi with pdftoppm into OUTDIR/img/imgNNN.jpg, shuffled with SEED,
#       and writes OUTDIR/key.json. Never render inside Obsidian (rule of 2 Nov 2026).
#   python3 read_compare.py compare OUTDIR A.json B.json VAULT
#       A.json, B.json: the two blind readers' arrays [{img, printed}, ...] (brief: page-number-fullpage-brief.txt).
#       For every rendered page whose two readings agree on a plain number (Devanagari digits normalised) that differs from the note's
#       marker, writes an edits-job2 spec to OUTDIR/spec.json; pages the readers disagree on or call unclear go to OUTDIR/held.json.
import json, random, re, subprocess, sys
DEV = str.maketrans('०१२३४५६७८९', '0123456789')
MRE = re.compile(r'^\*\[(?:p\. ([^\]]+)|PDF (\d+))\]\* \^pg(\d+)\s*$', re.M)
def render(items, pdfmap, out, seed):
    items = json.load(open(items)); pdfs = json.load(open(pdfmap)); seen = {}; pages = []
    for i, r in enumerate(items):
        r['pdf'] = pdfs[r['path']]
        for role, k in (('target', r['K']), ('prev', r['K'] - 1), ('next', r['K'] + 1)):
            key = (r['pdf'], k)
            if key in seen: seen[key]['roles'].append([i, role]); continue
            q = {'pdf': r['pdf'], 'K': k, 'roles': [[i, role]]}; seen[key] = q; pages.append(q)
    random.Random(seed).shuffle(pages)
    for n, q in enumerate(pages, 1):
        q['img'] = f'img{n:03d}'
        subprocess.run(['pdftoppm', '-r', '110', '-f', str(q['K']), '-l', str(q['K']), '-jpeg', '-singlefile', VAULT + q['pdf'], f"{out}/img/{q['img']}"], check=True)
    json.dump({'items': items, 'pages': pages}, open(f'{out}/key.json', 'w'), ensure_ascii=False, indent=1)
def compare(out, a, b, vault):
    K = json.load(open(f'{out}/key.json')); A = {e['img']: e['printed'] for e in json.load(open(a))}; B = {e['img']: e['printed'] for e in json.load(open(b))}
    paths = {}; spec = {}; held = []
    for q in K['pages']:
        notes = {K['items'][i]['path'] for i, _ in q['roles']}
        ra, rb = A[q['img']].translate(DEV), B[q['img']].translate(DEV)
        for p in notes:
            t = paths.setdefault(p, open(vault + p, encoding='utf-8').read())
            m = next((m for m in MRE.finditer(t) if int(m.group(3)) == q['K']), None)
            if not m: continue
            lab = m.group(1) or 'PDF'
            if ra == rb and ra.isdigit():
                if ra != lab: spec.setdefault(p, []).append([m.group(0).rstrip() + '\n', f"*[p. {ra}]* ^pg{q['K']}\n"])
            elif lab != ra or lab != rb: held.append({'path': p, 'K': q['K'], 'marker': lab, 'readA': A[q['img']], 'readB': B[q['img']]})
    json.dump({'backup': '.work/backup-<task>-<date>', 'edits': spec}, open(f'{out}/spec.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(held, open(f'{out}/held.json', 'w'), ensure_ascii=False, indent=1)
    print(sum(len(v) for v in spec.values()), 'edits in', len(spec), 'notes;', len(held), 'held')
if __name__ == '__main__':
    VAULT = '/mnt/user-data/uploads/Obsidian Vault/'
    if sys.argv[1] == 'render': render(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 20261103)
    else: VAULT = sys.argv[5]; compare(sys.argv[2], sys.argv[3], sys.argv[4], VAULT)
