---
type: prompt
updated: 2026-10-15
---
# Devanagari re-OCR scripts

Used on 15 Oct 2026 (decision D09 a/b) for the library PDFs whose OCR text layer had been written with OCRmyPDF's default fpdf2 renderer, which puts a junk character after the Devanagari vowel sign ि. Paths inside are those of the Claude cloud workspace and must be adapted.

- `pre.py` measures a PDF without changing it: pages, ि count, junk characters after ि.
- `pipe.py <batch.json>` takes a list of vault paths (staged into the workspace), measures each, and for files with 10 or more junk characters re-reads **only the pages that have the fault** (`ocrmypdf --redo-ocr --pages … --pdf-renderer sandwich -l eng+san`), measures again, and splits the new file into 20 MB parts with its size and SHA-256 in `manifest.json`. It skips files already in the manifest, so it can be restarted.
- `mkrep.py` writes `pdfrep.json` (target, parts, size, SHA-256, and the dated line for the catalog note) for the files not yet replaced; `pdfrep-apply.js` is the runner job that joins the parts, checks size and SHA-256, backs up the old PDF, writes the new one with `modifyBinary` and adds the line to every catalog note that links the PDF; `record.py` marks a replaced file as done; `watch.sh` waits for the next finished file.

**Lessons.** The cloud workspace is suspended when the AI's turn ends, and background processes die with it: stay in the turn (poll with waits of up to ten minutes) and check that the process is still running before saying so. With `--pages`, a 400-page book with the fault on every page takes about twelve minutes on two cores. Result on 15 Oct: 23 of 48 PDFs had the fault; junk characters 77,255 before, 98 after.
