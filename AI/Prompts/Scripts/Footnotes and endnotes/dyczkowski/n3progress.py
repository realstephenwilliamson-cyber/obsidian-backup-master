# n3progress.py (2 Nov 2026, night 3): writes the night's state into progress.json under "night3" (batches applied, notes done
# with their footnote counts, checks, tokens, what is next) and copies it to /mnt/user-data/outputs/dyfn/save-N/progress.json.
import json, os, re, sys, glob
H = '/home/claude/dyfn'; P = json.load(open(f'{H}/progress.json'))
B = json.load(open(f'{H}/n3batches.json'))
done = {}
for b in B['batches']:
    for nid in b['notes']:
        out = open(f'{H}/work/{nid}/out.md', encoding='utf-8').read(); pre = json.load(open(f'{H}/work/{nid}/pre.json'))
        defs = re.findall(r'(?m)^\[\^([0-9A-Za-z]+)\]:', out)
        done[nid] = {'batch': b['batch'], 'defs_after': len(defs), 'real_before': len(pre['real_defs_before']), 'plain_before': pre['plain_found'],
                     'plain_left': len(re.findall(r'(?m)^\d+\S{0,2}\\\. ', out)), 'labels': [defs[0], defs[-1]] if defs else None}
L = json.load(open(f'{H}/ledger.json'))
P['night3'] = {'started': '2026-11-02 18:30 EST', 'lead': 'Opus (chat with Stephen, attended)', 'backup': '.work/backup-dyfn-2026-11-02-n3/',
               'batches': B['batches'], 'checks': B.get('checks', []), 'notes_done': done,
               'summary': {'notes': len(done), 'defs_after': sum(v['defs_after'] for v in done.values()), 'new': sum(v['defs_after'] - v['real_before'] for v in done.values())},
               'tokens': {'all_agents': sum(a['tokens'] for a in L['agents']), 'fable': sum(a['tokens'] for a in L['agents'] if a['model'] == 'fable'), 'agents': L['agents']},
               'next': B.get('next', ''), 'next_job': B.get('next_job')}
json.dump(P, open(f'{H}/progress.json', 'w'), ensure_ascii=False, indent=1)
n = len(glob.glob('/mnt/user-data/outputs/dyfn/save-*')); d = f'/mnt/user-data/outputs/dyfn/save-{n + 1}'; os.makedirs(d)
json.dump(P, open(f'{d}/progress.json', 'w'), ensure_ascii=False, indent=1)
print(d, P['night3']['summary'])
