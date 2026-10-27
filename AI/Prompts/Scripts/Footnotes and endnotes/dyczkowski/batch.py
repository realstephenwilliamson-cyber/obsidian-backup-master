# batch.py (27 Oct 2026, Dyczkowski footnotes night 1): prepares one apply batch for the runner.
# Usage: batch.py BATCH FIRSTJOB ID=VAULTPATH [ID=VAULTPATH ...]
#   ID is the work id (e.g. v11-06): src/ID.md is the text the reader worked from, work/ID/out.md the converted text,
#   and /mnt/user-data/uploads/Obsidian Vault/VAULTPATH the note as freshly re-staged from the vault.
# Refuses a note whose fresh copy differs from src/ID.md. Writes to /mnt/user-data/outputs/dyfn/BATCH/:
#   edits/dyfn-BATCH/part01.json (the textpatch spec) and three jobs: pfN dry run, pfN+1 apply (backup in
#   .work/backup-dyfn-2026-10-27), pfN+2 the read-only check (dyfn-check.tpl.js).
import sys, os, json, subprocess
B, first = sys.argv[1], int(sys.argv[2]); pairs = [a.split('=', 1) for a in sys.argv[3:]]
H = '/home/claude/dyfn'; UP = '/mnt/user-data/uploads/Obsidian Vault/'; OUT = '/mnt/user-data/outputs/dyfn/' + B
BK = '.work/backup-dyfn-2026-10-27'
os.makedirs(OUT + '/edits/dyfn-' + B, exist_ok=True); os.makedirs(OUT + '/queue', exist_ok=True)
args, lst = [], []
for nid, vp in pairs:
    fresh = open(UP + vp, encoding='utf-8', newline='').read(); src = open(f'{H}/src/{nid}.md', encoding='utf-8', newline='').read()
    if fresh != src: sys.exit('CHANGED since read: ' + vp)
    args += [vp, UP + vp, f'{H}/work/{nid}/out.md']
    pre = json.load(open(f'{H}/work/{nid}/pre.json', encoding='utf-8'))
    lst.append({'p': vp, 'old': pre['real_defs_before']})
subprocess.run(['python3', f'{H}/scripts/mkspec.py', OUT + '/edits/dyfn-' + B + '/part01.json'] + args, check=True)
tpl = '/mnt/user-data/uploads/Obsidian Vault/.work/edits/textpatch.tpl.js'
t = open(tpl, encoding='utf-8').read()
def job(n, tag, apply, body):
    open(f'{OUT}/queue/pf{n}-{tag}.js', 'w', encoding='utf-8').write(('// APPLY\n' if apply else '') + body)
mk = lambda tag: t.replace('__NAME__', 'dyfn-' + B).replace('__TAG__', tag).replace('__BACKUP__', BK)
job(first, f'dyfn-{B}-dry', False, mk(f'pf{first}-dyfn-{B}-dry'))
job(first + 1, f'dyfn-{B}-apply', True, mk(f'pf{first + 1}-dyfn-{B}-apply'))
c = open(f'{H}/scripts/dyfn-check.tpl.js', encoding='utf-8').read()
c = c.replace('__TAG__', f'pf{first + 2}-dyfn-{B}-check').replace('__BACKUP__', BK).replace('__LIST__', json.dumps(lst, ensure_ascii=False)).replace('__UNRES__', '16/30')
job(first + 2, f'dyfn-{B}-check', False, c)
print(sorted(os.listdir(OUT + '/queue')))
