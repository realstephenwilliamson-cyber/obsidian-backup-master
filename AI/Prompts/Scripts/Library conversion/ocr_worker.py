#!/usr/bin/env python3
"""Fill the OCR cache for whole books (format-independent), so conversion later reads from cache.
usage: ocr_worker.py QUEUE.json WORKER_ID NWORKERS   QUEUE: [{pdf, langs}]"""
import sys, json, os, re, time
sys.path.insert(0, os.path.dirname(__file__))
import conv, pymupdf as fitz
q = json.load(open(sys.argv[1])); wid, nw = int(sys.argv[2]), int(sys.argv[3])
V = '/mnt/user-data/uploads/Obsidian Vault/'
for k, item in enumerate(q):
    if k % nw != wid: continue
    d = fitz.open(V + item['pdf']); n = len(d); t0 = time.time(); conv.OCR_PREP = item.get('ocr_prep')
    for i in (range(n - 1, -1, -1) if item.get('reverse') else range(n)):   # reverse: a second worker on the same book from the end
        if item.get('psm') == 'best':
            la = conv.ocr_page(d, i, item['langs'], dpi=300, psm=3); lb = conv.ocr_page(d, i, item['langs'], dpi=300, psm=6)
            ls = lb if len(''.join(x.text for x in lb)) > len(''.join(x.text for x in la)) else la
        else:
            ls = conv.ocr_page(d, i, item['langs'], dpi=300, psm=item.get('psm', 3))
        if item.get('san_pages') and conv.wants_san(d[i], ls):
            conv.ocr_page(d, i, item['langs'] + '+san', dpi=300)
    print(json.dumps({'done': item['pdf'], 'pages': n, 'sec': round(time.time() - t0)}), flush=True)
