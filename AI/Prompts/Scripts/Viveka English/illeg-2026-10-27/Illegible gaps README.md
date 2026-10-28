---
type: prompt
updated: 2026-10-28
---
# Illegible gaps README

The scripts of the `[illegible]` pass of 27–28 Oct 2026 over the library copy of Dyczkowski's Tantrāloka (`Library/Trika/Tantraloka (Dyczkowski)/`). The record is the AI log, 27 Oct 2026 (late evening), and the project doc *Illegible gaps by OCR and reading (27 Oct 2026) - record*. They follow the 23 Oct night pass (`night_illeg.py` … in the folder above), which filled 758 gaps; this pass reached the gaps that one could not place or read.

Written for a cloud workspace (`/home/claude/ill/`) with the library copy staged under `notes/lib/<vol folder>/`, the eleven PDFs linked as `pdfs/`, and the Monier-Williams data file. Needs `tesseract-ocr-script-latn` (Tesseract's Latin-script model), `pymupdf`, `rapidfuzz` and the `wamerican-large`/`wbritish-large` word lists.

## The method

1. `extract.py` lists every `\[illegible\]` run with its note, offsets and PDF page (`items.json`).
2. `ocr_pages.py` OCRs every page that holds a run, whole, with the Latin-script model at 400 dpi (TSV with word boxes; about 2 hours of workspace time for 2,368 pages, no model usage).
3. `align.py` places each run in its page's OCR by the note's neighbouring words (near matches allowed) and takes the OCR words between them (witness 1).
4. `w2p.py` reads each placed gap again from crops of its word boxes: 600 dpi without the dictionary, 450 dpi with it (witnesses 2 and 3).
5. `accept3.py` proposes a fill where two of the three readings agree on the letters and the macrons; the spelling is checked against `mw-heads.json` (Monier-Williams headwords, `mw_heads.py`), which supplies the dots the OCR loses (*sṛṣṭi*, *ṭīkā*); the copy's own counts are only a last resort, since it still holds many uncorrected OCR forms. Garbled footnote numbers, digits, capitals (mantras), odd punctuation and gaps over a line end are left out.
6. `sheets.py` makes the reading sheets (one printed line per gap, the gap boxed; the item list gives the note's words around the gap, never the fill); `reading-brief.txt` is the readers' brief (Sonnet agents).
7. `confirm.py` keeps a fill only where the blind reading, with high confidence, has the same letters as the OCR fill, or is one letter from it (the OCR loses a final ṁ or a first ū); what goes in is the reading's text, marks and punctuation as printed, without raised footnote numbers and without repeating a bracket or stop the note already has beside the gap.
8. `build_patch.py` writes the line patch (per note the length and FNV-1a hash before and after); `illeg-patch.tpl.js` applies it through the runner (backups first; a note is changed only if it is exactly the text the patch was made from); `illeg-check.tpl.js` checks the result (notes as intended; divine-name counts, footnote calls and definitions, `^pg` blocks and headings equal to the backups'; Viveka embeds; unresolved links).
9. `compare.py` scores a set of fills against a set of readings (used for the test of 50 and the audit sample).

## Result (27 Oct 2026)

4,352 placeholders in 4,199 runs before. 2,872 runs placed on their page; 896 fills proposed by the OCR rule; 882 confirmed by the blind readings and applied (113 notes, 837 lines): 667 as the OCR proposed, 158 with the reading's marks or punctuation, 57 where the reading was one letter from the OCR. The test of 50 before the readings: letters right in 49. The audit of 59 applied fills by a fresh reader: 59 right. 3,458 placeholders are left (3,317 runs).

## The data

In `.work/edits/illeg-2026-10-27/`: `items.json` (every run), `placed.json` (the page placement), `crop-readings.json` (the scripts call it `w2.json`), `accepted.json` (the proposed fills), `reads.json` (every blind reading, by set), `confirmed.json`, `edits.json` (what was written), `lib-patch.json` (the patch applied), `mw-heads.json`, `leftovers.json`.

## What is left

`.work/edits/illeg-2026-10-27/leftovers.json` lists every gap not filled, with the reason, and for the placed ones their page, box and the three OCR readings, so a later reading pass needs no OCR. See the record for the counts.
