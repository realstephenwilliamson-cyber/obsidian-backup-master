# Container paths (/home/claude/dz/...) are those of the 26 Oct 2026 session; adjust before reuse.
# After pipe.py: fix the look-alike letters (fixlayer.py) in each finished volume, then recompute size, SHA-256, parts and the stats
# (with IAST letters and look-alikes, old and new). Marks the manifest entry 'fixed'. Run repeatedly; skips volumes already fixed.
import json, os, re, subprocess, hashlib, math, fcntl
import pymupdf
MAN = '/home/claude/dz/rb/manifest.json'; OUT = '/mnt/user-data/outputs/dz/'; POST = '/home/claude/dz/rb/post.json'
IAST = re.compile('[āīūṛṝḷṃṁḥṅñṭḍṇśṣĀĪŪṚṂḤṄÑṬḌṆŚṢ]'); LOOK = re.compile('[şņțţıļŗřŞŅȚŢĻŖŘ]')
def cnt(fn):
    t = ''.join(p.get_text() for p in pymupdf.open(fn)); return dict(iast=len(IAST.findall(t)), lookalike=len(LOOK.findall(t)))
man = json.load(open(MAN)); post = json.load(open(POST)) if os.path.exists(POST) else {}
for name, r in man.items():
    if 'after' not in r or name in post: continue
    key = name.replace('Dyczkowski - Tantraloka, vol. ', 'v').replace('.pdf', ''); rb = f'/home/claude/dz/rb/{key}.pdf'; fx = f'/home/claude/dz/rb/{key}.fixed.pdf'
    if not os.path.exists(rb): continue
    res = subprocess.run(['python3', '/home/claude/dz/fix/fixlayer.py', rb, fx], capture_output=True, text=True)
    if res.returncode: print(name, 'fix failed', res.stderr[-300:]); continue
    b = open(fx, 'rb').read(); parts = []
    for p in [f for f in os.listdir(OUT) if f.startswith(key + '.new.part')]: os.remove(OUT + p)
    for k in range(math.ceil(len(b) / 20_000_000)):
        fn = f'{key}.new.part{k+1}'; open(OUT + fn, 'wb').write(b[k * 20_000_000:(k + 1) * 20_000_000]); parts.append(fn)
    post[name] = dict(fix=res.stdout.strip(), parts=parts, size=len(b), sha256=hashlib.sha256(b).hexdigest(), old=cnt('/home/claude/dz/pdf/' + name), new=cnt(fx), after=r['after'], before=r['before'], ocr_pages=r['ocr_pages'], old_size=r['old_size'], old_sha256=r['old_sha256'])
    json.dump(post, open(POST, 'w'), ensure_ascii=False, indent=1); print(name, post[name]['old'], post[name]['new'], flush=True)
