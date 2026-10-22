#!/usr/bin/env python3
"""Bundle converted book folders into JSON files of <= 24 MB for p4-create.js.
usage: bundle.py NAME job1 job2 ...  -> /mnt/user-data/outputs/work/p4/bundles/NAME-k.json, plus create-list and check-list"""
import sys, os, json, glob
OUT = '/home/claude/p4/out'
DEST = '/mnt/user-data/outputs/work/p4'
LIMIT = 24 * 1024 * 1024
name, jobs = sys.argv[1], sys.argv[2:]
os.makedirs(DEST + '/bundles', exist_ok=True)
bundles, cur, size, k = [], {}, 0, 0
check = {}
for j in jobs:
    job = json.load(open(os.environ.get('JOBDIR', '/home/claude/p4/jobs') + f'/{j}.json'))
    folder = job['folder']
    rep = json.load(open(os.path.join(job.get('out', OUT), folder, '_report.json')))
    check[rep['written'][0][0] if job.get('single') else folder] = rep['pages']
    for vp, f in rep['written']:
        t = open(f, encoding='utf-8').read()
        b = len(json.dumps(t, ensure_ascii=False).encode())
        if cur and size + b > LIMIT:
            k += 1; fn = f'{name}-{k}.json'; json.dump({'notes': cur}, open(f'{DEST}/bundles/{fn}', 'w'), ensure_ascii=False); bundles.append(fn); cur, size = {}, 0
        cur[vp] = t; size += b
if cur:
    k += 1; fn = f'{name}-{k}.json'; json.dump({'notes': cur}, open(f'{DEST}/bundles/{fn}', 'w'), ensure_ascii=False); bundles.append(fn)
json.dump(bundles, open(f'{DEST}/create-list.json', 'w'))
json.dump(check, open(f'{DEST}/check-list.json', 'w'), ensure_ascii=False)
tot = sum(os.path.getsize(f'{DEST}/bundles/{b}') for b in bundles)
print(json.dumps({'bundles': bundles, 'MB': round(tot / 1e6, 2), 'books': len(check)}))
