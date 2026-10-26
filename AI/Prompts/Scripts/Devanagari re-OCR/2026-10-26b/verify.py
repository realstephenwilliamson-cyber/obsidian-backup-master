# verify.py SRC NEW: page count, page sizes, every image stream byte-identical (sorted per page), and a low-dpi render equal on every page
import sys, hashlib, pymupdf
a = pymupdf.open(sys.argv[1]); b = pymupdf.open(sys.argv[2]); bad = []
assert a.page_count == b.page_count, ('pages', a.page_count, b.page_count)
for i in range(a.page_count):
    if a[i].rect != b[i].rect: bad.append((i + 1, 'rect'))
    ia = sorted(hashlib.md5(a.xref_stream_raw(x[0])).hexdigest() for x in a[i].get_images())
    ib = sorted(hashlib.md5(b.xref_stream_raw(x[0])).hexdigest() for x in b[i].get_images())
    if ia != ib: bad.append((i + 1, 'images'))
    if a[i].get_pixmap(dpi=30).samples != b[i].get_pixmap(dpi=30).samples: bad.append((i + 1, 'render'))
print(sys.argv[2].split('/')[-1], 'pages', a.page_count, 'problems', len(bad), bad[:8])
