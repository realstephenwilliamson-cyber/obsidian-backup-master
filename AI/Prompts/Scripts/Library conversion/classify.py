#!/usr/bin/env python3
"""Decide the text route for each staged PDF from a sample of its pages.
usage: classify.py LIST.json OUT.json   (LIST: [{path, subject, src}] vault paths; files under /mnt/user-data/uploads/Obsidian Vault/)
Route: pymupdf | glyphless | ocr ; plus langs and flags."""
import sys, json, re, os, collections
import pymupdf as fitz
V = '/mnt/user-data/uploads/Obsidian Vault/'
INDO = {'Trika', 'Hinduism', 'Sanskrit'}
IAST = re.compile(r'[āīūṛṝḷṃṁḥṅñṭḍṇśṣĀĪŪṚṆŚṢ]')
GARB = re.compile(r'[çïÿ¬µßå†®©¤¦]|[�-]')
FW = set('the of and to in a is that for it as was with be by on not he this are or his from at which but have an they'.split())


def probe(path):
    d = fitz.open(V + path)
    n = len(d)
    idx = sorted(set([min(n - 1, max(0, int(n * f))) for f in (0.15, 0.3, 0.45, 0.6, 0.75, 0.9)]))
    r = collections.Counter()
    fonts = collections.Counter()
    for i in idx:
        p = d[i]; t = p.get_text()
        r['chars'] += len(t); r['iast'] += len(IAST.findall(t)); r['garb'] += len(GARB.findall(t))
        r['deva'] += len(re.findall(r'[ऀ-ॿ]', t)); r['heb'] += len(re.findall(r'[֐-׿]', t))
        r['grk'] += len(re.findall(r'[Ͱ-Ͽἀ-῿]', t))
        w = re.findall(r'[A-Za-z]{2,}', t); r['words'] += len(w); r['fw'] += sum(1 for x in w if x.lower() in FW)
        area = p.rect.width * p.rect.height
        for img in p.get_image_info():
            bb = fitz.Rect(img['bbox'])
            if bb.width * bb.height > 0.6 * area: r['fullimg'] += 1; break
        for f in p.get_fonts(): fonts[f[3]] += 1
    k = len(idx)
    return dict(pages=n, toc=len(d.get_toc()), cpp=r['chars'] // k, iast_per_k=round(1000 * r['iast'] / max(1, r['chars']), 1),
                garb_per_k=round(1000 * r['garb'] / max(1, r['chars']), 1), deva=r['deva'], heb=r['heb'], grk=r['grk'],
                fw=round(r['fw'] / max(1, r['words']), 2), scan=round(r['fullimg'] / k, 2), glyphless='GlyphLessFont' in fonts,
                fonts=len(fonts))


def test_ocr(path):
    import subprocess, tempfile
    d = fitz.open(V + path); n = len(d); tot = 0; ia = 0
    for i in sorted(set([min(n - 1, int(n * 0.4)), min(n - 1, int(n * 0.7))])):
        pix = d[i].get_pixmap(dpi=300, colorspace=fitz.csGRAY)
        with tempfile.TemporaryDirectory() as td:
            pix.save(td + '/p.png')
            t = subprocess.run(['tesseract', td + '/p.png', '-', '-l', 'Latin'], capture_output=True, text=True, timeout=300).stdout
        tot += len(t); ia += len(IAST.findall(t))
    return round(1000 * ia / max(1, tot), 1)


def decide(row, pr):
    subj = row['path'].split('/')[1]
    indo = subj in INDO
    src = row.get('src', '')
    if pr['glyphless'] and src == 'ocr-overlay':
        return 'glyphless', 'Latin', 'OCR layer (GlyphLessFont) only'
    if pr['cpp'] < 200:
        return 'ocr', ('Latin' if indo else 'eng'), 'little or no text layer: fresh OCR'
    if pr['garb_per_k'] > 3:
        return 'ocr', ('Latin' if indo else 'eng'), f'garbled characters in the text layer ({pr["garb_per_k"]}/1000): fresh OCR'
    if indo and pr['scan'] >= 0.8 and pr['iast_per_k'] < 2:
        k = test_ocr(row['path'])
        pr['ocr_iast_per_k'] = k
        if k >= 3:
            return 'ocr', 'Latin', f'scan: the text layer has {pr["iast_per_k"]} IAST letters per 1000, a fresh OCR of two pages {k}: fresh OCR with the Latin model'
        return 'pymupdf', '', f'scan, but a fresh OCR finds no more diacritics ({k}/1000): the text layer'
    if pr['fw'] < 0.15 and pr['deva'] < 100 and pr['heb'] < 100 and pr['grk'] < 100:
        return 'check', '', f'few English function words ({pr["fw"]}): look before choosing'
    return 'pymupdf', '', 'text layer'


if __name__ == '__main__':
    rows = json.load(open(sys.argv[1]))
    out = []
    for row in rows:
        try:
            pr = probe(row['path'])
            route, langs, why = decide(row, pr)
            out.append(dict(row, **pr, route=route, langs=langs, why=why))
        except Exception as e:
            out.append(dict(row, route='error', why=str(e)))
        print(json.dumps({k: out[-1].get(k) for k in ('path', 'route', 'why', 'scan', 'iast_per_k', 'garb_per_k', 'fw')}, ensure_ascii=False)[:300], flush=True)
    json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
