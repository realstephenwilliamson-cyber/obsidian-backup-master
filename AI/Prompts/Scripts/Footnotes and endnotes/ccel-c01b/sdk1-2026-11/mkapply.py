# mkapply.py (SDK 1): from edits-<tag>.json, the edits-job2 spec .work/edits/ccel-2026-11/<tag>.json (backup
# .work/backup-ccel-2026-11-<DD>/<tag>) and three queue jobs: dry run, apply, check (from pf528, new names, this backup).
# usage: py mkapply.py TAG DD N   (N = first job number; writes pfN dry, pfN+1 apply, pfN+2 check into OUTDIR jobs/)
import json, sys, os
tag, DD, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
V = 'C:/Vaults/Obsidian Vault/'
spec = json.load(open(f'edits-{tag}.json', encoding='utf-8')); bk = f'.work/backup-ccel-2026-11-{DD}/{tag}'
spec['backup'] = bk
open(V + f'.work/edits/ccel-2026-11/{tag}.json', 'w', encoding='utf-8').write(json.dumps(spec, ensure_ascii=False))
tpl = open(V + '.work/edits/edits-job2.tpl.js', encoding='utf-8').read().replace("NAME = 'NAME'", f"NAME = 'ccel-2026-11/{tag}'")
chk = open(V + '.work/edits/sdk-templates-2026-11-03/pf528-c01d-check.js', encoding='utf-8').read()
chk = chk.replace("BK = '.work/backup-c01d-2026-10-28'", f"BK = '{bk}'").replace('pf528-c01d-check', f'pf{N+2}-ccel-{tag}-check')
chk = chk.replace("// pf528 (28 Oct 2026, fifth session): read-only check after pf527 (CCEL: 67 numbers moved, 13 restored, 6 whole notes).", f"// pf{N+2} (SDK 1, {DD} Nov 2026): read-only check after pf{N+1} (CCEL footnotes, group {tag}); made from pf528.")
os.makedirs('jobs', exist_ok=True)
for name, body in ((f'pf{N}-ccel-{tag}-dry.js', tpl), (f'pf{N+1}-ccel-{tag}-apply.js', '// APPLY\n' + tpl), (f'pf{N+2}-ccel-{tag}-check.js', chk)):
    open('jobs/' + name, 'w', encoding='utf-8', newline='\n').write(body)   # UTF-8, no BOM
print('spec', sum(len(v) for v in spec['edits'].values()), 'blocks in', len(spec['edits']), 'notes; jobs pf%d-pf%d' % (N, N + 2))
