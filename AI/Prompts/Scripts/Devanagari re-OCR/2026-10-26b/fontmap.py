# Keep a Word/Distiller PDF's pages and its existing OCR layer; only give the legacy MSTT fonts a ToUnicode CMap mapping every code
# to a space, so search and copy find the OCR text and not the font's gibberish. Usage: python3 fontmap.py in.pdf out.pdf
import sys, pikepdf
i, o = sys.argv[1:3]; p = pikepdf.open(i)
cmap = ("/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
        "/CMapName /Adobe-Identity-UCS def\n/CMapType 2 def\n1 begincodespacerange\n<00> <FF>\nendcodespacerange\n"
        "1 beginbfrange\n<00> <FF> [" + ' '.join('<0020>' for _ in range(256)) + "]\nendbfrange\nendcmap\nCMapName currentdict /CIDFont defineresource pop\nend\nend\n")
tu = pikepdf.Stream(p, cmap.encode()); fixed = set()
for pg in p.pages:
    for k, f in pg.obj.Resources.get('/Font', {}).items():
        if 'MSTT' in str(f.get('/BaseFont')) and f.objgen not in fixed: f.ToUnicode = tu; fixed.add(f.objgen)
p.save(o); print('fonts given a space map', len(fixed))
