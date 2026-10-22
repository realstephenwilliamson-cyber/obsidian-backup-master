---
type: prompt
updated: 2026-10-05
---
# OCR scripts

The scripts used for the 5 Oct 2026 OCR run (about 150 books), kept here so a later run can reuse them. They are referenced by [[Make scans searchable (OCR)|Make scans searchable (OCR)]]. The Python ones run in a Linux workspace with ocrmypdf, Tesseract 5 (models Latin, san, eng, heb, osd), pikepdf and poppler-utils. The JavaScript ones run in Obsidian's developer console through the `W` helper described in [[House rules for AI work|House rules for AI work]].

## The OCR command

```bash
ocrmypdf --skip-text --output-type pdf --jobs 2 -l Latin+san --tesseract-timeout 300 IN.pdf OUT.pdf   # scans
ocrmypdf --redo-ocr  --output-type pdf --jobs 2 -l Latin+san IN.pdf OUT.pdf                           # replace bad old OCR
python3 overlay.py IN.pdf OUT.pdf Latin+san                                                             # legacy-font or JPEG 2000 pages
python3 fixmap.py OUT.pdf OUT.fixed.pdf                                                                 # then always this
```

Add `--rotate-pages --rotate-pages-threshold 5` only for files known to have upside-down pages. A file whose pages are stored sideways (a `/Rotate` value that leaves the text running vertically) needs its `/Rotate` corrected with pikepdf before the OCR; check by rendering a page and looking at it.

## fixmap.py

```python
#!/usr/bin/env python3
"""Correct systematic letter confusions of Tesseract's Latin-script model in an OCR text layer (invisible text only):
dotless i -> i, and the cedilla/comma/caron look-alikes -> the IAST dot-below letters (s t n l r).
Touches only OCR-layer fonts: ocrmypdf's /OCR-* forms (ToUnicode CMap entries) and Tesseract's GlyphLessFont text (UTF-16 strings).
usage: fixmap.py IN OUT   -> prints JSON {changed: n, by_char: {...}}"""
import sys, re, json, collections
import pikepdf
MAP = {0x0131: 0x0069, 0x015F: 0x1E63, 0x015E: 0x1E62, 0x0146: 0x1E47, 0x0145: 0x1E46, 0x021B: 0x1E6D, 0x021A: 0x1E6C,
       0x0163: 0x1E6D, 0x0162: 0x1E6C, 0x013C: 0x1E37, 0x013B: 0x1E36, 0x0159: 0x1E5B, 0x0158: 0x1E5A}
cnt = collections.Counter()
def fix_cmap(stream):
    data = stream.read_bytes().decode('latin-1')
    def rep(m):
        u = int(m.group(2), 16)
        if u in MAP: cnt['cmap:' + chr(u)] += 1; return f'<{m.group(1)}> <{MAP[u]:04X}>'
        return m.group(0)
    # bfchar entries: <CID> <UNICODE>
    new = re.sub(r'<([0-9A-Fa-f]{4})>\s*<([0-9A-Fa-f]{4})>', rep, data)
    if new != data: stream.write(new.encode('latin-1'))
def fix_glyphless(form):
    ops = pikepdf.parse_content_stream(form); changed = False; out = []
    def fs(s):
        nonlocal changed
        b = bytes(s)
        if len(b) % 2: return s
        a = bytearray(b)
        for i in range(0, len(a), 2):
            u = (a[i] << 8) | a[i + 1]
            if u in MAP:
                v = MAP[u]; a[i] = v >> 8; a[i + 1] = v & 255; cnt['text:' + chr(u)] += 1; changed = True
        return pikepdf.String(bytes(a))
    for operands, op in ops:
        o = str(op)
        if o in ('Tj', "'", '"') and operands and isinstance(operands[-1], pikepdf.String):
            operands = list(operands[:-1]) + [fs(operands[-1])]
        elif o == 'TJ' and operands and isinstance(operands[0], pikepdf.Array):
            operands = [pikepdf.Array([fs(x) if isinstance(x, pikepdf.String) else x for x in operands[0]])]
        out.append((operands, op))
    if changed: form.write(pikepdf.unparse_content_stream(out))
seen_fonts, seen_forms = set(), set()
def visit(res, inside_ocr):
    for name, xo in (res.get('/XObject') or {}).items():
        if xo.get('/Subtype') != '/Form': continue
        og = xo.objgen
        if og in seen_forms and og != (0, 0): continue
        seen_forms.add(og)
        fonts = (xo.get('/Resources') or {}).get('/Font') or {}
        is_ocr = inside_ocr or str(name).startswith('/OCR-') or any(str(f.get('/BaseFont')) == '/GlyphLessFont' for f in fonts.values())
        if is_ocr:
            for f in fonts.values():
                if str(f.get('/BaseFont')) == '/GlyphLessFont':
                    fix_glyphless(xo)
                elif f.get('/Subtype') == '/Type0' and f.get('/ToUnicode') is not None and f.objgen not in seen_fonts:
                    seen_fonts.add(f.objgen); fix_cmap(f.ToUnicode)
        visit(xo.get('/Resources') or {}, is_ocr)
src, dst = sys.argv[1:3]
pdf = pikepdf.open(src)
for pg in pdf.pages: visit(pg.obj.get('/Resources') or {}, False)
pdf.save(dst, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.preserve)
print(json.dumps({'changed': sum(cnt.values()), 'by': dict(cnt)}, ensure_ascii=False))
```

## overlay.py

```python
#!/usr/bin/env python3
"""Add an invisible OCR text layer on top of every page of a born-digital PDF whose own text is unreadable
(legacy or broken fonts), WITHOUT rasterizing the page: the original vector page stays as it is.
usage: overlay.py SRC OUT LANGS"""
import sys, os, subprocess, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
import pikepdf

src, out, langs = sys.argv[1:4]
tmp = tempfile.mkdtemp()
env = dict(os.environ, OMP_THREAD_LIMIT='1')
try:
    pdf = pikepdf.open(src)
    n = len(pdf.pages)

    def dpi_for(i):
        # scanned pages: render at twice the scan resolution (200-300 dpi); vector pages: 300 dpi
        try:
            out = subprocess.run(['pdfimages', '-list', '-f', str(i + 1), '-l', str(i + 1), src], capture_output=True, text=True, timeout=30).stdout.splitlines()[2:]
            ppi = [int(l.split()[12]) for l in out if len(l.split()) > 12 and l.split()[12].isdigit() and int(l.split()[3]) > 600]
            if ppi: return max(200, min(300, 2 * min(ppi)))
        except Exception:
            pass
        return 300

    def do(i):
        base = f'{tmp}/p{i:05d}'
        subprocess.run(['pdftoppm', '-f', str(i + 1), '-l', str(i + 1), '-r', str(dpi_for(i)), '-gray', '-png', '-singlefile', src, base],
                       check=True, capture_output=True, timeout=600)
        subprocess.run(['tesseract', base + '.png', base, '-l', langs, '-c', 'textonly_pdf=1', 'pdf'],
                       check=True, capture_output=True, timeout=900, env=env)
        os.remove(base + '.png')
        return base + '.pdf'

    with ThreadPoolExecutor(2) as ex:
        files = list(ex.map(do, range(n)))
    keep, skipped = [], 0
    for i, f in enumerate(files):
        pg = pdf.pages[i]
        if int(pg.obj.get('/Rotate', 0)) % 360:
            skipped += 1; continue
        t = pikepdf.open(f); keep.append(t)
        pg.add_overlay(t.pages[0])
    pdf.save(out)
    print(f'overlay ok: {n} pages, {skipped} rotated pages left without overlay')
finally:
    shutil.rmtree(tmp, ignore_errors=True)
```

## Quality check (qcheck.py)

Written for the 5 Oct run's job files (`jobs.json`, `status.json`, `parts/`); the paths at the top have to be adapted, but the measure is the useful part. Samples 12 pages per output. `fw` is the share of common function words among Latin-script words (ordinary English prose is about 0.4; under 0.15 needs a look). `odd` counts characters typical of upside-down text; accented Vedic transliteration also raises it.

```python
#!/usr/bin/env python3
"""Quality check of finished OCR outputs: sample pages, measure how much of the Latin text is real words.
usage: qcheck.py [idx ...]  (default: every done job)"""
import json, os, re, subprocess, sys, random, tempfile
J = json.load(open('/mnt/user-data/outputs/ocr/jobs.json')); S = json.load(open('/opt/ocr/work/status.json'))
PARTS = '/mnt/user-data/outputs/ocr/parts/'
FW = set('''the of and to in a is that for it as was with be by on not he i this are or his from at which but have an they you were
her she there been one all we their has would when if so no will what can more about into than them its only other some could
these then also may such our those very do had any same him who between through being both each after where should because
without must way under first upon itself must thus here how even most himself own whose shall made does yet well therefore
le la les de des et un une est du en dans que qui pour par sur au aux ne pas il elle se sont plus ce cette der die und das ist
nicht mit sich des den dem zu von auf ein eine'''.split())
def text(pdf, pages):
    out = []
    for p in pages:
        r = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'], capture_output=True, text=True, timeout=120)
        out.append(r.stdout)
    return '\n'.join(out)
def metrics(t):
    toks = re.findall(r"[A-Za-zÀ-ɏḀ-ỿ]{2,}", t)
    low = [x.lower() for x in toks]
    fw = sum(1 for x in low if x in FW)
    deva = len(re.findall(r'[ऀ-ॿ]', t))
    upside = sum(t.count(c) for c in 'ƏəÁá' ) # common in upside-down Latin
    return dict(tok=len(toks), fw=round(fw / max(1, len(toks)), 3), deva=deva, odd=upside)
ids = sys.argv[1:] or [k for k, v in S.items() if v.get('state') == 'done' and k.isdigit()]
res = {}
for k in sorted(ids, key=int):
    v = S[k]; parts = v.get('parts') or []
    if not parts: continue
    with tempfile.NamedTemporaryFile(suffix='.pdf', dir='/opt/qc') as f:
        for p in parts: f.write(open(PARTS + k + '/' + p, 'rb').read())
        f.flush()
        n = v.get('pages') or 1
        random.seed(int(k)); pages = sorted(set([min(n, max(1, x)) for x in random.sample(range(1, n + 1), min(n, 12))]))
        m = metrics(text(f.name, pages))
    m.update(idx=k, pages=n, langs=v.get('langs'), mode=v.get('mode'), name=J[int(k)]['path'].split('/')[-1][:60])
    res[k] = m
    print(json.dumps(m, ensure_ascii=False), flush=True)
json.dump(res, open('/opt/qc/qc.json', 'w'), ensure_ascii=False, indent=1)
```

## Splitting a large output and writing the manifest

Files over about 25 MB can't be written to the vault in one piece by the file bridge. Split them, copy the parts to `.work/ocr/<id>/`, and write `.work/ocr/manifest.json` (a list with one entry per file).

```python
import hashlib, json, os
PART = 25 * 1024 * 1024
def split(out_pdf, idx, vault_path, orig_size, dest):        # dest: local folder mirrored to .work/ocr/
    os.makedirs(f'{dest}/{idx}', exist_ok=True); parts = []
    with open(out_pdf, 'rb') as f:
        for k, b in enumerate(iter(lambda: f.read(PART), b'')):
            open(f'{dest}/{idx}/p{k:03d}', 'wb').write(b); parts.append(f'p{k:03d}')
    md5 = hashlib.md5(open(out_pdf, 'rb').read()).hexdigest()
    return {'idx': str(idx), 'path': vault_path, 'orig_size': orig_size, 'out_size': os.path.getsize(out_pdf), 'md5': md5, 'parts': parts}
# manifest = [split(...), split(...)]; json.dump(manifest, open(f'{dest}/manifest.json', 'w'), ensure_ascii=False, indent=1)
```

`orig_size` is the size of the vault file now; ocr-apply refuses to replace a file that has changed since. For a second pass on a file whose first original is already in `.trash`, add `bak_size` (the size of that backup).

## ocr-apply.js (Obsidian console)

Joins the parts in `.work/ocr/<id>/` listed in `.work/ocr/manifest.json`. Each manifest entry is `{idx, path, orig_size, out_size, md5, parts[], bak_size?}`. The script checks the MD5 and that the vault file is still `orig_size`, copies the original to `.trash/ocr-originals-<DATE>/` (set `DATE` at the top for a new run), then writes the new file.

```javascript
(async () => {
  // Swap in the OCR'd PDFs listed in .work/ocr/manifest.json. Each original is copied to .trash/ocr-originals-2026-10-05 first;
  // (for a second pass the backup already holds the first original: bak_size). A file is replaced only if its parts reassemble to the expected md5 and the original is still the size it was when staged.
  const A = app.vault.adapter, fs = require('fs'), path = require('path'), crypto = require('crypto');
  const base = A.getBasePath();
  const DATE = '2026-10-05';  // set to the date of the new run: originals go to .trash/ocr-originals-<DATE>
  const M = JSON.parse(await A.read('.work/ocr/manifest.json'));
  const log = []; let ok = 0;
  for (const m of M) {
    try {
      const dir = path.join(base, '.work', 'ocr', String(m.idx));
      if (!fs.existsSync(dir)) { log.push(`${m.idx} SKIP no parts`); continue; }
      const buf = Buffer.concat(m.parts.map(p => fs.readFileSync(path.join(dir, p))));
      const h = crypto.createHash('md5').update(buf).digest('hex');
      if (h !== m.md5 || buf.length !== m.out_size) { log.push(`${m.idx} SKIP md5/size mismatch`); continue; }
      const tgt = path.join(base, m.path);
      const size = fs.statSync(tgt).size;
      if (size !== m.orig_size) { log.push(`${m.idx} SKIP original is ${size} bytes, expected ${m.orig_size}`); continue; }
      const bak = path.join(base, '.trash', 'ocr-originals-' + DATE, m.path);
      fs.mkdirSync(path.dirname(bak), { recursive: true });
      if (!fs.existsSync(bak)) fs.copyFileSync(tgt, bak);
      if (fs.statSync(bak).size !== (m.bak_size || m.orig_size)) { log.push(`${m.idx} SKIP backup copy missing or wrong size`); continue; }
      fs.writeFileSync(tgt, buf);
      if (fs.statSync(tgt).size !== m.out_size) { log.push(`${m.idx} ERR written size differs`); continue; }
      fs.rmSync(dir, { recursive: true, force: true });
      ok++; log.push(`${m.idx} OK ${m.path}`);
    } catch (e) { log.push(`${m.idx} ERR ${e.message}`); }
  }
  await A.write(`.work/out/ocr-apply-${Date.now()}.txt`, log.join('\n'));
  return `ocr applied ${ok} of ${M.length}; ` + log.filter(l => !/ OK /.test(l)).join(' | ');
})()
```

## textprops.js (Obsidian console)

Sets the catalog `text` property and the dated **Text layer** lines from `.work/ocr/textprops.json` (`{notes: {notePath: {text, lines: [{file, line, replace[], remove[]}]}}}`). Dry run unless `window.DRY = false`; it backs up each changed note to `.work/backup-textprops/`.

```javascript
(async () => {
  // Set the catalog `text` property and the dated **Text layer** lines from .work/ocr/textprops.json
  // ({ notes: { notePath: { text: 'searchable'|'scan'|null, lines: [{ file: basename|null, line: '...' , replace: [regex strings] }] } } }).
  // window.DRY !== false -> report only. Backups of changed notes in .work/backup-textprops/.
  const DRY = window.DRY !== false;
  const A = app.vault.adapter, V = app.vault, FM = app.fileManager;
  const J = JSON.parse(await A.read('.work/ocr/textprops.json'));
  const log = []; let nProp = 0, nLine = 0, nNotes = 0;
  for (const [p, d] of Object.entries(J.notes)) {
    const f = V.getAbstractFileByPath(p);
    if (!f) { log.push('MISSING ' + p); continue; }
    const t0 = await V.read(f);
    const curText = app.metadataCache.getFileCache(f)?.frontmatter?.text ?? null;
    const wantProp = d.text !== undefined && d.text !== null && d.text !== curText;
    // body edits
    let t = t0; const ch = [];
    for (const L of d.lines || []) {
      let done = false;
      for (const rs of L.replace || []) {
        const re = new RegExp(rs, 'm');
        if (re.test(t)) { t = t.replace(re, L.line); done = true; ch.push('~ ' + L.line.slice(0, 90)); break; }
      }
      if (L.remove && L.remove.length) {  // drop the per-file lines that a combined line replaces
        const rm = L.remove.map(rs => new RegExp(rs)), a = t.split('\n'), out = [];
        for (let i = 0; i < a.length; i++) {
          if (a[i] !== L.line && rm.some(r => r.test(a[i]))) {
            ch.push('- ' + a[i].slice(0, 90));
            if (out.length && out[out.length - 1].trim() === '' && i + 1 < a.length && a[i + 1].trim() === '') i++;
            continue;
          }
          out.push(a[i]);
        }
        t = out.join('\n');
      }
      if (!done) {
        if (t.includes(L.line)) continue;
        const i = t.indexOf('\n---\n\n## Also in your library');
        t = i > 0 ? t.slice(0, i).replace(/\s*$/, '') + '\n\n' + L.line + '\n' + t.slice(i) : t.replace(/\s*$/, '') + '\n\n' + L.line + '\n';
        ch.push('+ ' + L.line.slice(0, 90));
      }
    }
    if (!wantProp && t === t0) continue;
    nNotes++;
    log.push(`${p}: ${wantProp ? `text ${curText} -> ${d.text}; ` : ''}${ch.length} line(s)`); ch.forEach(c => log.push('    ' + c));
    if (DRY) continue;
    const b = '.work/backup-textprops/' + p; const bd = b.split('/').slice(0, -1).join('/');
    if (!(await A.exists(bd))) await A.mkdir(bd);
    if (!(await A.exists(b))) await A.write(b, t0);
    if (t !== t0) { await V.modify(f, t); nLine += ch.length; }
    if (wantProp) { await FM.processFrontMatter(f, fm => { fm.text = d.text; }); nProp++; }
  }
  await A.write('.work/out/textprops-' + (DRY ? 'dry' : 'applied') + '.txt', log.join('\n'));
  return `${DRY ? 'DRY' : 'APPLIED'}: ${nNotes} notes; property changes ${DRY ? '(dry)' : nProp}; lines ${DRY ? '(dry)' : nLine}`;
})()
```
