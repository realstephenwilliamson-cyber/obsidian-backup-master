# For Word/Distiller PDFs whose own fonts extract as junk (Durga700): keep the original vector pages, remove the old OCR layer,
# graft the new OCR layer from a --force-ocr copy (same page size), and give the legacy MSTT fonts a ToUnicode CMap that maps every
# code to a space, so only the OCR text is found when searching or copying. Usage: python3 vecgraft.py orig.pdf ocr.pdf out.pdf
import sys, re, pikepdf
orig, ocr, out = sys.argv[1:4]
o = pikepdf.open(orig); n = pikepdf.open(ocr)
cmap = ("/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
        "/CMapName /Adobe-Identity-UCS def\n/CMapType 2 def\n1 begincodespacerange\n<00> <FF>\nendcodespacerange\n"
        "1 beginbfrange\n<00> <FF> [" + ' '.join('<0020>' for _ in range(256)) + "]\nendbfrange\nendcmap\nCMapName currentdict /CIDFont defineresource pop\nend\nend\n")
tu = pikepdf.Stream(o, cmap.encode()); fixed = set(); removed = grafted = 0
for i, (pg, pn) in enumerate(zip(o.pages, n.pages)):
    res = pg.obj.Resources; xo = res.get('/XObject', {})
    old = [k for k, v in xo.items() if v.get('/Subtype') == '/Form' and '/Resources' in v and '/Font' in v.Resources and
           any(str(f.get('/BaseFont')) in ('/GlyphLessFont',) or 'NotoSans' in str(f.get('/BaseFont')) for f in v.Resources.Font.values())]
    c = pg.obj.Contents; streams = list(c) if isinstance(c, pikepdf.Array) else [c]
    for s in streams:
        d = s.read_bytes(); nd = d
        for k in old: nd = re.sub(re.escape(str(k).encode()) + rb'\s+Do', b'', nd)
        if nd != d: s.write(nd)
    for k in old: del xo[k]; removed += 1
    for k, f in res.get('/Font', {}).items():
        if 'MSTT' in str(f.get('/BaseFont')) and f.objgen not in fixed: f.ToUnicode = tu; fixed.add(f.objgen)
    for k, v in pn.obj.Resources.XObject.items():
        if str(k).startswith('/OCR-'):
            name = pikepdf.Page(pg).add_resource(o.copy_foreign(v), pikepdf.Name.XObject, prefix='OCR-')
            pikepdf.Page(pg).contents_add(pikepdf.Stream(o, f'q {name} Do Q\n'.encode()), prepend=False); grafted += 1
o.save(out); print('old OCR forms removed', removed, 'fonts given a space map', len(fixed), 'OCR forms grafted', grafted)
