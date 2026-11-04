---
type: scripts
---
# Finn's footnotes, book-wide (3 Nov 2026, night)

What was done: every page of *The Kulacudamani Tantra and The Vamakesvara Tantra* (Finn) compared with the PDF's own text layer (the old Courier / Courier-Oblique OCR, read by `pdfside.py` from `../finn/`), and each page that differed settled from the layer, or from the page image where the layer was unclear. The AI log entry of 3 Nov 2026 (night) has the counts.

Run in the cloud workspace with PyMuPDF on a staged copy of the PDF and of the ten notes (paths in the scripts are the workspace's: `/home/claude/finn/`, with `md/` the notes as staged, `layer.json` from `../finn/layer.py`).

| Script | What it does |
|---|---|
| `survey.py` | per page: the layer's note labels and first words, matched to the page block's definitions, plain `N\.` paragraphs or other paragraphs; flags pages that differ |
| `survey2.py` | per page: definition numbers against the layer's, the text of each definition against the layer note of the same number, and each `[^X]` call's preceding word against the layer's raised call |
| (inline in the session) | the number-run check: in book order, the definitions' numbers in each run (Introduction, Part II introduction, KCT, VT chapters) and the numbers missing from each run; this found the 183 gaps |
| `view.py K ...` | compact view of a page for settling it: layer notes, layer calls, the block's foot and the snippets around the calls |
| `blk.py K[:from]` | the page block in full, lines numbered |
| `img.py K[:y0-y1]` | renders a page or a band of it (130 dpi) |
| `fnlib.py` | builds exact `{id, path, old, new}` edits from edits on page blocks (`sub`, `para` to turn a paragraph into a definition, `L` to give a label `N` or `N-pP` when `N` is taken in the note), simulates them as `pf591` does and checks calls and definitions paired, a blank line before every definition run and no text line directly after a definition |
| `spec01.py` … `spec10.py` | the decisions, note by note, with a comment per page; they write `.work/edits/finn-2026-11-03n/finnNN-spec.json` |
| `spec-restore.py` | the second pass on notes 01 and 02: footnote text the OCR had dropped, restored where two blind readers agreed (`reader-brief.txt`, `readings.json`) → `finnR-spec.json` |
| `mkjobs.py NNN dry|apply|check spec [backup]` | runner jobs from the kept templates `pf591-audfix-apply.js` and `pf680-footnote-check.js` |

Conventions kept: a footnote whose number is already taken in the note is `[^N-pP]` (P = printed page); a footnote that is only a drawing is `*(a drawing in the print)*`; a footnote with no call in the print stays a plain `N\.` paragraph (18 and 89 in the Introduction, the second 272 on p. 138, which the print numbers twice); the print's own duplicate (157 and 158 on p. 354 say the same) is kept. Verse numbers standing alone and misplaced verse numbers were left where they are.
