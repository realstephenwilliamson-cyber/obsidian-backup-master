# (13 Nov 2026) Fill conv.py's OCR cache for a page range ahead of the conversion: prefill.py pdf langs first last.
# Run two at once (one per language set, e.g. eng and eng+grc); pages already cached are skipped. The cache is keyed on the PDF's
# path as the converter opens it, so the path is made absolute here: give the job's "pdf" the same absolute path.
import sys, time, os
sys.path.insert(0, '/home/claude/p4/scripts')
import conv, pymupdf as fitz
doc = fitz.open(os.path.abspath(sys.argv[1])); langs = sys.argv[2]; a, b = int(sys.argv[3]), int(sys.argv[4])
t0 = time.time()
for i in range(a - 1, min(b, doc.page_count)):
    conv.ocr_page(doc, i, langs, dpi=300, psm=3)
    print(i + 1, round(time.time() - t0), flush=True)
