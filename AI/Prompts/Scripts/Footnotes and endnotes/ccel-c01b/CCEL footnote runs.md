---
type: prompt
updated: 2026-10-28
---
# CCEL footnote runs (C-01b)

Scripts of 28 Oct 2026 for the audit finding C-01(b): in the two CCEL books (Augustine NPNF1 6, Chrysostom on Matthew), the converter put the footnotes of some PDF pages at the end of the page block before, so the footnote text sat one page early (often after the 1888 print-page number that opens them). Run in the workspace, on a dump of the notes (a runner job that writes every note of the two books to JSON) and the pdf.js text of the pages (a job like pf442).

| file | what it does |
|---|---|
| `detect.py` | lists page blocks whose footnote zone holds numbers whose calls are in the next block (`cands.json`). 28 Oct: 269 blocks. |
| `plan2.py` | for each, the start of the run: the first such number, extended back over the pieces (a print-page number, Greek text that precedes its number) that the next PDF page has and this one lacks; the run ends at the block's end. |
| `strict.py` | keeps a cut only where it falls on a clean item boundary, checked against both PDF pages (`ok.json`, `hold.json`). 28 Oct: 204 kept, 65 held. |
| `build_spec.py` | moves each kept run to the next page block (before its own footnotes, or at its end) and writes whole-block edits for `edits-job2`; it checks that the non-space characters and the `^pg` blocks are unchanged. |
| `reader-brief.txt` | the readers' brief for the held cases: the block's footnote text and the two page images; the reader gives the words where the next page's footnotes begin ("move"), or "mixed", "none", "unclear". |
| `apply_read.py` | applies the readers' cut points where the quote occurs once, the words after it are on the next page and the text before it on this one; the same whole-block edits and checks as `build_spec.py`. |

**28 Oct 2026:** 204 runs moved in 43 notes (pf444 dry, pf445, check pf446), then 62 of the 65 held ones from the readers' cut points (pf466 dry, pf467, check pf468): 266 runs in all. Both checks: every `^pg` block registered, `[^N]:` and divine-name counts unchanged, the characters the same as the backups'. Blind readers given a moved run and the two page images in random order put 10 of 10 and 8 of 8 on the page they were moved to. **Left:** 3 (`.work/edits/c01b-2026-10-28/hold.json`): two where the text before the reader's cut is not on the page, and one where the reader found nothing to move. The pdf.js page text is kept in `pf442-c01b-text.json` there.

**28 Oct 2026, third session (pf472–pf475):** the 3 held cases closed on the pdf.js text: two runs moved to their own page (Augustine 26 part 7, PDF 824; Chrysostom on Matthew 20 part 16, PDF 618), with what the converter had dropped there restored from the PDF text (the number 2887, note 2889, note 2212, the number 2215); in Augustine 07 part 1 notes 15–16 are on PDF 44, as the note has them. **Found:** `lost-number-scan.js` (the pf472 probe) lists, in the 68 notes of the two books, 1,604 of 7,474 calls whose number appears nowhere else in the note: the converter often dropped the last footnote of a PDF page, usually only its number, sometimes the whole note (list: `.work/edits/c01b-2026-10-28/lost-numbers-pf472.json`). A later pass can restore them from the pdf.js text of every page (a job like pf442 over all pages), with readers for what the text does not settle.
