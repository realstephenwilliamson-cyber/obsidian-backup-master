# Devanagari re-OCR scripts, 26 Oct 2026 (second session)

The scripts used for decision 8 (the poor text layers) in the second session of the corrections week. They change only a PDF's invisible text layer; the page images stay byte-identical (checked with `verify.py`). The record is the AI log entry *26 Oct 2026 (second session)* and the Claude project doc *Corrections week, second session (26 Oct 2026) - record*. The first session's scripts are in `../2026-10-26/`.

| File | What it does |
|---|---|
| `strip.py` | removes every text layer from a scanned PDF (BT..ET blocks and OCR form XObjects) before a fresh OCR |
| `spread2.py` | two-page spreads (Gonda, Abbinnett): splits each page image at the gutter, deskews (and upscales if asked) each half, reads it with Tesseract, and places the text back on the original page with the exact affine map; `--keep-others` strips only the pages it reads |
| `fixlayer2.py` | maps the Latin model's look-alike letters (ş ņ ț ţ ı ļ ŗ ř) to IAST in the OCR layer; `--indic` also maps Š š → Ś ś and ã ä → ā, for English books on Indian subjects |
| `vecgraft.py` | Word/Distiller PDFs (Durga700): keeps the original vector pages, grafts a new OCR layer from a `--force-ocr` copy, and gives the old MSTT fonts a text map to spaces so their gibberish is no longer found in search or copy |
| `fontmap.py` | the font map of `vecgraft.py` alone, keeping the existing OCR layer |
| `stats.py` | pages, words, junk after ि, Devanagari in Latin lines, IAST and look-alike letters of a layer (the catalog lines' before/after figures) |
| `verify.py` | page count, page sizes, every image stream byte-identical, and a low-dpi render equal on every page |
| `pagecmp.py`, `dictscore.py` | per-page and whole-book share of English words in a layer, to find pages where a new layer is worse |

Lessons: a re-OCR with the same model on the same image gives the same reading; change the model (English only where no Devanagari is printed), the image (split, deskew, upscale) or force the OCR. Tesseract's best models gave no gain on Lanman or Singh. A second reader on the page images decides.
