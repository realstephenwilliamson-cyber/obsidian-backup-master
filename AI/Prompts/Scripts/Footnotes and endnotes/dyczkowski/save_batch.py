# save_batch.py BATCH JOBS "BLIND" "CHECK" ID[=title] ...: records a batch in progress.json (night 2) and stages the op files and checks
import sys, json, os, shutil, re
H = '/home/claude/dyfn'; OUT = '/mnt/user-data/outputs/dyfn/save'
B, jobs, blind, check = sys.argv[1:5]; ids = sys.argv[5:]
P = json.load(open(f'{H}/progress.json')) if os.path.exists(f'{H}/progress.json') else json.load(open(f'{H}/progress-n1.json'))
NIGHT = os.environ.get('NIGHT', 'night3')   # the progress key of this run (night 2: night2; 2 Nov 2026: night3)
n2 = P.setdefault(NIGHT, {'started': os.environ.get('STARTED', '2026-11-02 18:30 EST'), 'backup': os.environ.get('BKDIR', '.work/backup-dyfn-2026-11-02-n3/'), 'batches': [], 'notes_done': {}})
n2['batches'] = [b for b in n2['batches'] if b['batch'] != B] + [{'batch': B, 'notes': ids, 'jobs': jobs, 'blind_check': blind, 'after_apply': check}]
os.makedirs(f'{OUT}/ops', exist_ok=True); os.makedirs(f'{OUT}/checks', exist_ok=True)
for nid in ids:
    pre = json.load(open(f'{H}/work/{nid}/pre.json')); out = open(f'{H}/work/{nid}/out.md', encoding='utf-8').read()
    defs = len(re.findall(r'(?m)^\[\^\d+\]:', out)); title = re.sub(r'^Tantraloka Dyczkowski v\d\d \d\d - ', '', [l for l in open(f'{H}/paths.txt') if l.startswith(nid + '=')][0].strip().split('/')[-1][:-3])
    n2['notes_done'][nid] = {'title': title, 'calls_defs': defs, 'new': defs - len(pre['real_defs_before']), 'plain_before': pre['plain_found'], 'plain_left': len(re.findall(r'(?m)^\d+\S{0,2}\\\. ', out)), 'batch': B}
    shutil.copy(f'{H}/rd/{nid}/ops.json', f'{OUT}/ops/ops-{nid}.json')
    if os.path.exists(f'{H}/rd/{nid}/map.json'): shutil.copy(f'{H}/rd/{nid}/map.json', f'{OUT}/ops/map-{nid}.json')
for f in os.listdir(f'{H}/checks'):
    if f.startswith(B + '-') and f.endswith('.json'): shutil.copy(f'{H}/checks/{f}', f'{OUT}/checks/{f}')
for f in ('tasks.json', 'answers.json'):
    if os.path.exists(f'{H}/checks/{B}/{f}'): shutil.copy(f'{H}/checks/{B}/{f}', f'{OUT}/checks/{B}-{f}')
L = json.load(open(f'{H}/ledger.json')); n2['tokens'] = {'all_agents': sum(a['tokens'] for a in L['agents']), 'fable': sum(a['tokens'] for a in L['agents'] if a['model'] == 'fable'), 'caps': json.loads(os.environ.get('CAPS', '{}')), 'agents': L['agents']}
n2['summary'] = {'notes': len(n2['notes_done']), 'footnotes_new': sum(v['new'] for v in n2['notes_done'].values())}
json.dump(P, open(f'{H}/progress.json', 'w'), ensure_ascii=False, indent=1)
print(n2['summary'], sorted(os.listdir(f'{OUT}/ops'))[-3:], len(os.listdir(f'{OUT}/checks')))
