# Build the runner job and its data for one book. usage: makejob.py BOOK ORIG_FOLDER(vault-relative, with /) OUT_DIR [apply]
import sys, os, json, glob, hashlib
VAULT = r'C:\Vaults\Obsidian Vault'
book, folder, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
apply = len(sys.argv) > 4 and sys.argv[4] == 'apply'
files = {}
for f in sorted(glob.glob(os.path.join(glob.escape(outdir), '*.md'))):
    n = os.path.basename(f)
    cur = open(os.path.join(VAULT, folder, n), encoding='utf-8', newline='').read()
    new = open(f, encoding='utf-8', newline='').read()
    files[n] = dict(sha=hashlib.sha256(cur.encode('utf-8')).hexdigest(), new=new)
data = dict(folder=folder, backup='.work/backup-footnotes-2026-10-18/%s/' % book, files=files)
os.makedirs(os.path.join(VAULT, '.work', 'footnotes-2026-10-18'), exist_ok=True)
with open(os.path.join(VAULT, '.work', 'footnotes-2026-10-18', book + '.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(data, fh, ensure_ascii=False)
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fnjob.js'), encoding='utf-8').read().replace('__BOOK__', book)
if apply: js = '// APPLY\n' + js
name = 'fn-%s-%s.js' % (book, 'apply' if apply else 'dry')
with open(os.path.join(VAULT, '.work', 'queue', name), 'wb') as fh:
    fh.write(js.encode('utf-8'))          # UTF-8 without a byte-order mark
raw = open(os.path.join(VAULT, '.work', 'queue', name), 'rb').read(12)
print('queued', name, 'first bytes', raw, 'files', len(files))
