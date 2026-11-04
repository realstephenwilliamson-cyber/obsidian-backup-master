---
type: prompt
updated: 2026-11-03
---
# Illegible gaps README (3 Nov 2026)

The inner `[illegible]` gaps in Dyczkowski's library copy.

The second reading pass over the `\[illegible\]` placeholders in the library copy of Dyczkowski's Tantrāloka translation
(`Library/Trika/Tantraloka (Dyczkowski)/`), after the OCR pass of 27 Oct (`../illeg-2026-10-27/`). No OCR: each gap was read on
the page by two blind readers, and filled only where both wrote exactly the same.

Result: 2,607 placeholders in 2,470 runs → **741 in 706 runs**; 1,764 gaps filled by 1,691 edits in 113 notes (jobs pf678 dry
run, pf679 apply, pf680 check). The 706 runs left: about 206 the PDF's text layer could not place on a page; about 500 whose readings
were dropped (a reader low, a reader's note of trouble, the two readings apart, or a fill that failed a rule in `build2.py`).
Validation: 1,233 of 1,288 pass-1 fills score 0.5 or more against the old OCR witnesses of 27 Oct.

## Files

- `pf676-dy-dump.js`: runner job, read-only; writes `.work/xfer/dy-notes.json` (path → text of every note in the folder).
- `match.py`: ties the placed gaps of 27 Oct (`.work/edits/illeg-2026-10-27/leftovers.json`, items with `box400`) to the
  placeholder runs as they are now, by the words on each side → `matched.json`.
- `mk.py`: pass 1 sheets: the printed line at 200 dpi with the gap boxed in red, 12 strips to a sheet → `sheets2/`, `tasks2.json`.
- `pass2.py`: pass 2: the runs the boxes do not cover, located by the text layer (the words before or after the gap); a strip of
  that line and its neighbours, 10 to a sheet → `sheets3/`, `runs2.json`, `tasks3.json`.
- `brief.txt` (pass 1, boxed) and `brief2.txt` (pass 2, unboxed): the reader briefs. Output per sheet: one JSON line per ID,
  `{"id","printed","conf","note"}`. Reader A read the sheets in order, reader B in reverse order; neither saw the other.
- `build2.py`: both passes → fills where the readers agree exactly and neither is low or flags the spot; drops fills with `?`, no
  letters, a word repeated from the neighbour, or more than six words; strips footnote marks `^N`; `||` → `॥` on lines that use ॥;
  clusters edits within 80 characters so each `old` string occurs once → `gaps-spec.json` and `gaps-decisions.json`.
- The apply and check used the job templates in `.work/edits/sdk-templates-2026-11-03/`: `pf591-audfix-apply.js` (exact edits, each
  old text once) and `pf680-footnote-check.js` (calls and definitions paired, the footnote cache, `^pg` blocks, headings and
  divine-name counts against the backups).

The scripts ran in the cloud workspace under `/home/claude/ill/` with the vault's files staged under
`/mnt/user-data/uploads/Obsidian Vault/`; change those paths to rerun them.

## Data

In `.work/edits/fnleft-2026-11/`: `gaps-spec.json` (the edits applied), `gaps-decisions.json` (ID → fill and note),
`gaps-left.json` (the 706 runs left: note, number of placeholders, the line they sit on). A further pass would start from
`gaps-left.json`: locate each on the page by hand or with a better text-layer search, then the same two-reader method.

## Round 3 (3 Nov 2026, evening)

The 199 gaps whose two readings differed, both readers confident (jobs pf688–pf690; data `gaps3-spec.json`, `gaps3-decisions.json`):

- `align.py`: the place of every unfilled gap in the notes as pf679 left them.
- `resolve2.py`: each reading reduced to its core: footnote marks (`^N`) and the `^` of raised ordinals taken out, then the words
  at either end that already stand next to the gap in the note set aside (a reader often copied the neighbours too; the words must
  meet the gap exactly). Same core → filled (128); both cores the same footnote number, next to that footnote's own label or call
  → the placeholder taken out (27). The rest (44) to a third reader.
- `brief3.txt`: the third reader's brief (the strips cut from the first sheets, the words before and after from the current text).
- `third_decide.py`: filled where the third reading's core equals one of the first two (34).
- `build3.py`: the edits, with the brackets of fills escaped (and those of 33 earlier fills), and a placeholder that stood alone on
  its line taken out with the line.

Result: 547 placeholders in 517 places left (`gaps-left.json`, rebuilt). A fill in brackets right after a call made a Markdown link
(`[^34](Now,)`) in three notes; the parenthesis was escaped afterwards (`fn2-spec.json`). Check the joins of any later fill the same way.
