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

The results of 26 Oct are in `.work/edits/pagelabels-2026-10-26/` (`pf270-rangescan.json`, `pf275-pagefill.json`), with the spec `.work/edits/pagefill27.json`. The rule for unnumbered pages is in the Vault Guide (page markers: a page that prints no number takes its number from the pages around it inside a numbered run, or at either end of one where the contents or the page count fixes it).

## Use

A later pass can start from `pagefill27.json`: take the books whose cases are all inside a clean run, check a sample of pages per book on the images, and apply book by book with a dry run first.
