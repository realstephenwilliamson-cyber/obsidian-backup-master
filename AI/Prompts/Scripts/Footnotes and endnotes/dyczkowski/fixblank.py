# fixblank.py TAG FIRSTJOB ID... : for notes already applied, put a blank line before every definition that follows a non-blank
# line (Obsidian otherwise does not list it as a footnote); writes the spec and three jobs (dry, apply, check).
import sys, re, json, subprocess, os
H = '/home/claude/dyfn'; UP = '/mnt/user-data/uploads/Obsidian Vault/'; tag, first = sys.argv[1], int(sys.argv[2]); ids = sys.argv[3:]
P = dict(l.strip().split('=', 1) for l in open(f'{H}/paths.txt'))
OUT = f'/mnt/user-data/outputs/dyfn/{tag}'; os.makedirs(OUT + f'/edits/dyfn-{tag}', exist_ok=True); os.makedirs(OUT + '/queue', exist_ok=True)
args, lst, n = [], [], 0
for nid in ids:
    vp = P[nid]; fresh = open(UP + vp, encoding='utf-8', newline='').read(); ours = open(f'{H}/work/{nid}/out.md', encoding='utf-8', newline='').read()
    new0 = re.sub(r"(?m)^([^\n]*\S[^\n]*)\n(?=\[\^[0-9A-Za-z]+\]:)", r"\1\n\n", fresh); same = fresh == ours or new0 == ours
    new = re.sub(r'(?m)^([^\n]*\S[^\n]*)\n(?=\[\^[0-9A-Za-z]+\]:)', r'\1\n\n', fresh)
    k = len(re.findall(r'(?m)^(?:[^\n]*\S[^\n]*)\n(?=\[\^[0-9A-Za-z]+\]:)', fresh))
    print(nid, 'vault==ours' if same else 'VAULT DIFFERS', 'blank lines to add:', k)
    if not same or not k: continue
    open(f'{H}/work/{nid}/fix.md', 'w', encoding='utf-8', newline='').write(new)
    args += [vp, UP + vp, f'{H}/work/{nid}/fix.md']; lst.append({'p': vp, 'old': json.load(open(f'{H}/work/{nid}/pre.json'))['real_defs_before']}); n += 1
if not n: sys.exit('nothing to do')
subprocess.run(['python3', f'{H}/scripts/mkspec.py', OUT + f'/edits/dyfn-{tag}/part01.json'] + args, check=True)
t = open(UP + '.work/edits/textpatch.tpl.js', encoding='utf-8').read(); BK = '.work/backup-dyfn-2026-10-27-n2'
mk = lambda jt: t.replace('__NAME__', 'dyfn-' + tag).replace('__TAG__', jt).replace('__BACKUP__', BK)
open(f'{OUT}/queue/pf{first}-dyfn-{tag}-dry.js', 'w', encoding='utf-8').write(mk(f'pf{first}-dyfn-{tag}-dry'))
open(f'{OUT}/queue/pf{first+1}-dyfn-{tag}-apply.js', 'w', encoding='utf-8').write('// APPLY\n' + mk(f'pf{first+1}-dyfn-{tag}-apply'))
c = open(f'{H}/scripts/dyfn-check.tpl.js', encoding='utf-8').read().replace('__TAG__', f'pf{first+2}-dyfn-{tag}-check').replace('__BACKUP__', BK).replace('__LIST__', json.dumps(lst, ensure_ascii=False)).replace('__UNRES__', '16/30')
open(f'{OUT}/queue/pf{first+2}-dyfn-{tag}-check.js', 'w', encoding='utf-8').write(c)
print(n, 'notes;', sorted(os.listdir(OUT + '/queue')))
