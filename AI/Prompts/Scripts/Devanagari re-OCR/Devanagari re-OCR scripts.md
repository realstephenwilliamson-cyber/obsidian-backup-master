---
type: prompt
updated: 2026-10-26
---
# Devanagari re-OCR scripts

Used on 15 Oct 2026 (decision D09 a/b) for the library PDFs whose OCR text layer had been written with OCRmyPDF's default fpdf2 renderer, which puts a junk character after the Devanagari vowel sign ि. Paths inside are those of the Claude cloud workspace and must be adapted.

- `pre.py` measures a PDF without changing it: pages, ि count, junk characters after ि.
- `pipe.py <batch.json>` takes a list of vault paths (staged into the workspace), measures each, and for files with 10 or more junk characters re-reads **only the pages that have the fault** (`ocrmypdf --redo-ocr --pages … --pdf-renderer sandwich -l eng+san`), measures again, and splits the new file into 20 MB parts with its size and SHA-256 in `manifest.json`. It skips files already in the manifest, so it can be restarted.
- `mkrep.py` writes `pdfrep.json` (target, parts, size, SHA-256, and the dated line for the catalog note) for the files not yet replaced; `pdfrep-apply.js` is the runner job that joins the parts, checks size and SHA-256, backs up the old PDF, writes the new one with `modifyBinary` and adds the line to every catalog note that links the PDF; `record.py` marks a replaced file as done; `watch.sh` waits for the next finished file.

**Lessons.** The cloud workspace is suspended when the AI's turn ends, and background processes die with it: stay in the turn (poll with waits of up to ten minutes) and check that the process is still running before saying so. With `--pages`, a 400-page book with the fault on every page takes about twelve minutes on two cores. Result on 15 Oct: 23 of 48 PDFs had the fault; junk characters 77,255 before, 98 after.

## 26 Oct 2026: Dyczkowski's Tantrāloka (decision 7), folder `2026-10-26/`

- `pipe-latin-san.py`: as `pipe.py`, for every PDF in its folder, with `-l Latin+san` (the 5 Oct language set; `eng+san` stripped every IAST mark from the English lines). Tesseract's `Latin.traineddata` (a script model) is not installed in the workspace and raw downloads are blocked: attach the GitHub repository `tesseract-ocr/tessdata_fast` and check out `script/Latin.traineddata` sparsely.
- `fixlayer.py in.pdf out.pdf`: the Latin model writes look-alike letters (ş ņ ț ţ ı ļ ŗ ř for ṣ ṇ ṭ ṭ i ḷ ṛ ṛ). In the sandwich layer the text is a GlyphLessFont (Identity-H, CID = Unicode), so they are replaced in the hex strings of the OCR text XObjects (pikepdf). Compare the whole volume old against new before replacing: ř turned up only there.
- `post.py` runs `fixlayer.py` on each finished volume and writes size, SHA-256, 20 MB parts and the IAST and look-alike counts to `post.json`. `mkcheck2.py` picks three pages per volume for a second reader. `mkrep2.py` writes `dzrep.json`; `mkrep3.py` does the same for a volume already replaced once. `cmp.py NN` compares the old and new layers of a whole volume (whitespace ignored) and lists what was deleted and inserted. `dzrep-apply.js.tpl` is the runner job: it checks the old file's size and SHA-256, joins the parts, checks them, backs up the old PDF, writes with `modifyBinary`, reads back and deletes the parts; the catalog line is written separately.
- `loop.sh`, `postloop.sh`, `succ.sh`: a background shell in the workspace ends after two hours; `succ.sh <pid> <script>` starts the next loop when the old one ends.

**Lesson.** Tesseract with the same models on the same page images reads the same text. The new layer was the 5 Oct reading letter for letter, without the junk glyphs the old renderer had written after ि (and after र्म, ो and the like), and with more line breaks. So a re-OCR with the same languages cannot serve as a second witness for misread words: change the model or the image for that.
