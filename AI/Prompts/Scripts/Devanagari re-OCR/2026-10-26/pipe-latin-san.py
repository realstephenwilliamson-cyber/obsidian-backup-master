# Container paths (/home/claude/dz/...) are those of the 26 Oct 2026 session; adjust before reuse.
# Decision 7 (26 Oct 2026; Latin+san, the 5 Oct language set, after eng+san lost every IAST diacritic): re-OCR the pages of Dyczkowski's Tantraloka volumes whose text layer has a junk glyph after ि.
# Adapted from AI/Prompts/Scripts/Devanagari re-OCR/pipe.py (15 Oct). Usage: python3 pipe.py  (processes every PDF in /home/claude/dz/pdf not yet in the manifest)
import sys, json, os, re, subprocess, hashlib, math, glob
import pymupdf as fitz
SRC = '/home/claude/dz/pdf/'; OUT = '/mnt/user-data/outputs/dz/'; MAN = '/home/claude/dz/rb/manifest.json'
def bad(c): return not ('ऀ' <= c <= 'ॿ' or c in ' \n.,;:-|।॥()')
def stats(fn):
    doc = fitz.open(fn); I = J = inj = dev = 0
    for pg in doc:
        t = pg.get_text()
        for m in re.finditer('ि(.)', t):
            I += 1; J += bad(m.group(1))
        dev += len(re.findall(r'[ऀ-ॿ]', t))
        for line in t.split('\n'):
            lat = len(re.findall(r'[A-Za-z]', line)); d = len(re.findall(r'[ऀ-ॿ]', line))
            if lat > 15 and lat > 4 * d: inj += d
    return dict(pages=len(doc), short_i=I, junk=J, deva_in_latin=inj, deva_total=dev, words=sum(len(p.get_text('words')) for p in doc))
man = json.load(open(MAN)) if os.path.exists(MAN) else {}
for src in sorted(glob.glob(SRC + '*.pdf')):
    name = os.path.basename(src)
    if name in man and 'after' in man[name]: continue
    s0 = stats(src); rec = dict(before=s0)
    doc = fitz.open(src)
    pg = [str(i + 1) for i, p in enumerate(doc) if any(bad(m.group(1)) for m in re.finditer('ि(.)', p.get_text()))]
    rec['ocr_pages'] = len(pg)
    key = name.replace('Dyczkowski - Tantraloka, vol. ', 'v').replace('.pdf', ''); out = f'/home/claude/dz/rb/{key}.pdf'
    print(name, s0, 'pages to OCR', len(pg), flush=True)
    r = subprocess.run(['ocrmypdf', '--redo-ocr', '--pages', ','.join(pg), '--pdf-renderer', 'sandwich', '-l', 'Latin+san', '--output-type', 'pdf', '-j', '2', src, out], capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(out):
        s1 = stats(out); rec['after'] = s1
        b = open(out, 'rb').read(); parts = []
        for k in range(math.ceil(len(b) / 20_000_000)):
            fn = f'{key}.new.part{k+1}'; open(OUT + fn, 'wb').write(b[k * 20_000_000:(k + 1) * 20_000_000]); parts.append(fn)
        rec.update(parts=parts, size=len(b), sha256=hashlib.sha256(b).hexdigest(), old_size=os.path.getsize(src), old_sha256=hashlib.sha256(open(src,'rb').read()).hexdigest())
    else: rec['ocr_error'] = r.stderr[-800:]
    man[name] = rec; json.dump(man, open(MAN, 'w'), ensure_ascii=False, indent=1)
    print(name, 'after', rec.get('after'), rec.get('ocr_error', ''), flush=True)
print('ALLDONE', flush=True)
