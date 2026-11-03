# mkcheck.py (SDK 1): blind-check files for the edited cases of a group: chk/<tag>/vNN.jpg (the page) and vNN.txt (the block as edited,
# from notes-<tag>.json), in a shuffled order; the key (vNN -> case) in chk/<tag>-key.json, which the checkers never see.
# usage: py mkcheck.py TAG c001 c002 ...
import json, re, sys, os, shutil, random
tag = sys.argv[1]; ids = sys.argv[2:]
idx = {c['id']: c for c in json.load(open('cases.json', encoding='utf-8'))}
N = json.load(open(f'notes-{tag}.json', encoding='utf-8'))
d = f'chk/{tag}'; os.makedirs(d, exist_ok=True)
random.seed(tag); random.shuffle(ids); key = {}
for i, cid in enumerate(ids):
    c = idx[cid]; t = N[c['path']]
    m = re.search(r'^\*\[[^\]]+\]\* \^pg%d\s*$' % c['K'], t, re.M); m2 = re.search(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', t[m.end():], re.M)
    b = t[m.end(): m.end() + m2.start() if m2 else len(t)].strip()
    v = 'v%02d' % (i + 1); key[v] = cid
    open(f'{d}/{v}.txt', 'w', encoding='utf-8').write(b); shutil.copy(f'cases/{cid}.jpg', f'{d}/{v}.jpg')
json.dump(key, open(f'chk/{tag}-key.json', 'w'), indent=0)
print(len(key), 'cases in', d)
