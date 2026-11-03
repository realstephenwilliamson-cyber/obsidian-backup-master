# setup_vol.py VOL N1 N2 ... (2 Nov 2026, night 3): copies the freshly staged notes of one volume to src/, records their vault
# paths in paths.txt, runs prepass.py on each and builds each reader's packet (packet.py) in rd/ID. Prints the range of each note.
import os, sys, shutil, subprocess, re, json
UP = '/mnt/user-data/uploads/Obsidian Vault/'; H = '/home/claude/dyfn'
vol = sys.argv[1]; ids = {int(x) for x in sys.argv[2:]}
base = f'Library/Trika/Tantraloka (Dyczkowski)/Tantraloka vol {vol} (Dyczkowski)/'
paths = {}
for f in sorted(os.listdir(UP + base)):
    m = re.match(r'Tantraloka Dyczkowski v(\d\d) (\d\d) - ', f)
    if m and int(m.group(2)) in ids: paths[f'v{vol}-{m.group(2)}'] = base + f
old = dict(l.strip().split('=', 1) for l in open(H + '/paths.txt') if '=' in l) if os.path.exists(H + '/paths.txt') else {}
old.update(paths); open(H + '/paths.txt', 'w').write(''.join(f'{k}={v}\n' for k, v in sorted(old.items())))
pdf = UP + f'Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. {vol}.pdf'
procs = []
for nid, vp in paths.items():
    shutil.copy(UP + vp, f'{H}/src/{nid}.md')
    subprocess.run(['python3', f'{H}/scripts/prepass.py', f'{H}/src/{nid}.md', f'{H}/work/{nid}'], check=True, capture_output=True)
    procs.append(subprocess.Popen(['python3', f'{H}/scripts/packet.py', f'{H}/work/{nid}', pdf, f'{H}/rd/{nid}'], stdout=subprocess.DEVNULL))
for p in procs: p.wait()
for nid in paths:
    p = json.load(open(f'{H}/work/{nid}/pre.json')); nums = sorted(d['n'] for pg in p['pages'] for d in pg['defs'])
    rng = set(range(nums[0], nums[-1] + 1)) if nums else set()
    print(nid, paths[nid].split(' - ')[-1][:-3], '| plain', p['plain_found'], '| range', (nums[0], nums[-1]) if nums else None, '| real before', len(p['real_defs_before']),
          '| pages', len(p['pages']), (p['pages'][0]['pdf'], p['pages'][-1]['pdf']) if p['pages'] else '', '| gaps', sorted(rng - set(nums))[:8], '| flags', [(f['line'], f['number']) for f in p['flags']])
