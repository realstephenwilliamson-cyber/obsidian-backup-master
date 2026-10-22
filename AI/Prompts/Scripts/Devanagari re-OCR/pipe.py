import sys, json, os, re, subprocess, hashlib, math
import pymupdf as fitz
V = '/mnt/user-data/uploads/Obsidian Vault/'
OUT = '/mnt/user-data/outputs/d09/'
MAN = '/home/claude/d09/rb/manifest.json'
def stats(fn):
    doc = fitz.open(fn); I = J = inj = 0
    for pg in doc:
        t = pg.get_text()
        for m in re.finditer('ि(.)', t):
            I += 1; c = m.group(1)
            if not ('\u0900' <= c <= '\u097f' or c in ' \n.,;:-|।॥()'): J += 1
        for line in t.split('\n'):
            lat = len(re.findall(r'[A-Za-z]', line)); dev = len(re.findall(r'[\u0900-\u097f]', line))
            if lat > 15 and lat > 4 * dev: inj += dev
    return dict(pages=len(doc), short_i=I, junk=J, deva_in_latin=inj)
man = json.load(open(MAN)) if os.path.exists(MAN) else {}
for dev in json.load(open(sys.argv[1])):
    rel = dev.replace('C:\\Vaults\\Obsidian Vault\\', '').replace('\\', '/')
    if rel in man: continue
    src = V + rel
    try: s0 = stats(src)
    except Exception as e: man[rel] = dict(error=str(e)); json.dump(man, open(MAN, 'w'), ensure_ascii=False); continue
    rec = dict(before=s0)
    if s0['junk'] >= 10:
        key = hashlib.md5(rel.encode()).hexdigest()[:10]; out = f'/home/claude/d09/rb/{key}.pdf'
        pg = [str(i + 1) for i, p in enumerate(fitz.open(src)) if any(not ('\u0900' <= m.group(1) <= '\u097f' or m.group(1) in ' \n.,;:-|\u0964\u0965()') for m in re.finditer('\u093f(.)', p.get_text()))]
        rec['ocr_pages'] = len(pg)
        r = subprocess.run(['ocrmypdf', '--redo-ocr', '--pages', ','.join(pg), '--pdf-renderer', 'sandwich', '-l', 'eng+san', '--output-type', 'pdf', '-j', '2', src, out], capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out):
            s1 = stats(out); rec['after'] = s1
            b = open(out, 'rb').read(); parts = []
            for k in range(math.ceil(len(b) / 20_000_000)):
                fn = f'{key}.part{k+1}'; open(OUT + fn, 'wb').write(b[k * 20_000_000:(k + 1) * 20_000_000]); parts.append(fn)
            rec.update(parts=parts, size=len(b), sha256=hashlib.sha256(b).hexdigest()); os.remove(out)
        else: rec['ocr_error'] = r.stderr[-400:]
    man[rel] = rec; json.dump(man, open(MAN, 'w'), ensure_ascii=False, indent=0)
    print(rel, rec.get('before'), rec.get('after'), flush=True)
print('BATCHDONE', sys.argv[1], flush=True)
