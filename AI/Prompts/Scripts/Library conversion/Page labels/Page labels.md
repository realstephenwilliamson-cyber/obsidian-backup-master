---
type: prompt
updated: 2026-10-26
---
# Page labels

Read-only runner jobs that measure the page markers and the index labels of the converted books, written on 26 Oct 2026 (third session of the corrections week) and kept under the house rule *Keep what a later session will use*. None of them changes a note.

## Files

| file | what it does |
|---|---|
| `index-label-scan.js` | (pf270) for every book's index note, compares each contents line `[[note\|label]] (pp. a–b)` with the chapter note's `page_range` and its first and last page markers; flags labels that differ, mix numberings (roman and arabic, `p.` and `PDF`) or run backwards. 26 Oct: 523 lines flagged. |
| `pagefill-scan.js` | (pf275) finds `*[PDF K]*` markers inside a numbered run (both neighbours printed in the same numbering, numbers differing by exactly their PDF distance) and the `page_range` values and index labels that would follow from numbering them. 26 Oct: 255 markers, 634 page_range changes, 611 index labels. |
| `pagefill-spec.js` | (pf276) the same, written as an `edits-job2` spec to `.work/edits/pagefill27.json`. **Not applied**: the automatic recompute is unsafe where a book's ranges descend or its printed page labels came from OCR (258 odd cases), so on 26 Oct only Chan, Farrer and *Cybernetics* were done, by reading the pages. |
| `pagefill-spec2.js` | (pf418, 28 Oct 2026) pf276 re-run on the vault as it is, plus, for each chapter note, the printed-marker offsets (printed number minus PDF page) per numbering, and the fills with their neighbours; writes `.work/out/pf418-spec.json`. |
| `render-strips.js` | (pf421) renders the top and bottom strips of chosen PDF pages with Obsidian's pdf.js to PNGs in `.work/xfer/pl28/`, for blind readers (list `[{id, pdf, K}]`). |
| `page-number-brief.txt` | the readers' brief: the page's own printed number, or none / unclear / noimage. |
| `filter_spec.py` | keeps only the edits of chapter notes whose markers agree (one offset per numbering, none descending) and whose book no reading contradicts, minus a hold list; writes an `edits-job2` spec and the list of the rest. |
| `pagelabels-check.js` | (pf431) read-only check after an apply: frontmatter readable, every marker's `^pg` block registered, divine-name count against the backup, line count unchanged. |

The results of 26 Oct are in `.work/edits/pagelabels-2026-10-26/` (`pf270-rangescan.json`, `pf275-pagefill.json`), with the spec `.work/edits/pagefill27.json`. The rule for unnumbered pages is in the Vault Guide (page markers: a page that prints no number takes its number from the pages around it inside a numbered run, or at either end of one where the contents or the page count fixes it).

## Use

**28 Oct 2026:** applied where safe (pf427–pf431): 124 markers filled, 455 `page_range` values and 326 index labels in 591 notes of 137 books, after 284 page strips were read blind (fill pages and their run's ends, one page per book with printed-range changes; 199 of 202 fill-run readings agree, the rest unclear or in two held books). Also Chan's 14 `[p. i]` markers in notes 18–19 (the running head "CH'ENG I" read as a page number; pages 545–571, read on the page) with note 19's range and label, Farrer's line break, Wiener's text_source. Left (`.work/edits/pagelabels-2026-10-28/left.json`): 243 edits in 118 notes of 54 books whose markers disagree (Prabuddha Bharata 56, Vasudeva, Törzsök, Rastogi, Shastri, Grimes …), Vasudeva and Hirschi held, Cyclonopedia and the Dyczkowski draft of chapter 1 contradicted by the reading; and the 258 notes with labels that are not plain numbers. Earlier: A later pass can start from `pagefill27.json`: take the books whose cases are all inside a clean run, check a sample of pages per book on the images, and apply book by book with a dry run first.
