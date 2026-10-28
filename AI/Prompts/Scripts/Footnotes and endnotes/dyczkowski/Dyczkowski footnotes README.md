---
type: prompt
updated: 2026-10-27
---
# Dyczkowski footnotes - README

Scripts for turning the plain footnotes of the library copy of Dyczkowski's Tantrāloka (`Library/Trika/Tantraloka (Dyczkowski)/`, 177 notes) into Markdown footnotes, written on the night of 27 Oct 2026 from the Kubjika method (`../kubjika/`) and improved on the second night (27 Oct, evening). They run in a Claude cloud workspace (paths such as `/home/claude/dyfn/` must be adapted); the vault is changed only by runner jobs. The state of the work is in `.work/edits/dyfn/progress.json`; the record of each night is a project doc in `claude/completion-2026-10/`.

| File | What it does |
|---|---|
| `prepass.py` | One note: numbered plain paragraphs (`971\. text`, `500?\. text`) → `[^n]: text`; a number that breaks the sequence is fixed from its neighbours or flagged; a clash with a real footnote is flagged and left plain; same-page continuation paragraphs indented; a page map (definitions, body lines, hints) in `pre.json`. |
| `packet.py` | The reader's folder for one note: the pre-pass text with line numbers, `pages.txt`, and the page images of every page with footnotes (200 dpi, greyscale, margins trimmed). |
| `reader-brief.txt` | The page reader's brief: place each call on the image; fix definition numbers, splits, carry-overs, strays; move already-real calls that stand in the wrong place; asterisk notes become paragraphs of their footnote; report what can't be decided. |
| `reader-task.txt` | The task text given to each reader (night 2), with the practical points (save as you go, `printed` = the printed footnote number, say how the numbers relate to the print). |
| `apply_ops.py` | Applies a reader's op list to the pre-pass text and checks it against the original note: each number once as a call and once as a definition, calls in order, frontmatter, page markers, headings and block ids unchanged, the word-level differences listed for the lead to read. `--renumber` relabels by call order (for letter labels such as `232b`); `--start=N` makes the first label N (night 2: where the note's numbers ran behind the print); `--map=FILE` relabels by an explicit map instead. A call glued to `(` gets a space (Obsidian reads `[^n](x)` as a link), and since night 2 every definition gets a blank line before it (a definition right after a non-blank line is not listed by Obsidian as a footnote). |
| `mkspec.py` | The whole-note spec for `.work/edits/textpatch.tpl.js` (oldLen/oldHash guard). |
| `batch.py` | One apply batch: refuses a note changed since it was read, writes the spec and three jobs (dry run, apply with backup, `dyfn-check`). Set `BK` to the night's backup folder. |
| `sample.py`, `checker-brief.txt`, `compare.py` | The blind check: 8 footnotes per note (moved calls and carry-overs first), the page image and the paragraph with the calls removed given to a checker that has not seen the note; its answers compared with the note. Automatic mismatches are expected where a call stands on the page before or after its definition's page, where two definitions on a page begin alike, and where carried-over text was already joined; the lead reads each one. |
| `fixblank.py` | Night 2: for notes already applied, puts a blank line before every definition that follows a non-blank line, with the three jobs (it found 18 notes; afterwards Obsidian listed 1,786 of 1,786 footnotes, including seven that were real before and had not been listed). |
| `calib.py` | The calibration: a reader's result on vol. 5 part 8 (from its backup) against the converted note. |
| `dyfn-check.tpl.js` | The read-only check after each apply (a copy is in `.work/edits/`): divine-name counts against the backups, Obsidian's footnote cache by id, every `^pg` block still registered, every heading link into the notes resolves, unresolved links. |
| `review.py`, `crop.py`, `cmpshow.py`, `save_batch.py`, `ledger.py` | The lead's helpers (night 2): `review.py ID[=START|=0|=map:FILE]` runs `apply_ops.py` and prints a summary (label minus printed number, word differences, the reader's problems); `crop.py VOL PDFPAGE "words" OUT.png` crops the line of a page that holds the words (for reading a call on the image); `cmpshow.py` lists a blind check's mismatches; `save_batch.py` records a batch in `progress.json` and stages its op files and checks; `ledger.py` adds up the agents' tokens against the caps. |

**Data kept:** the readers' op lists (`ops-*.json`, with the lead's edits marked `"by": "lead"` and explained under `lead`; `map-*.json` where labels were mapped) and the blind checks' tasks, keys, answers and reports are in `.work/edits/dyfn/`.

**Order per note:** stage the note → `prepass.py` → `packet.py` → a reader agent with `reader-brief.txt` and `reader-task.txt` → `review.py` (read the word differences and the reader's problems; give `=START` or a map where the numbers drift from the print) → blind check per batch of up to five notes → re-stage, `batch.py`, dry run, apply → `dyfn-check`.

**Facts about the book** (for the next reader):
- The vault numbers the footnotes through each chapter or volume, as the print does in vols. 1–3 (vol. 1 through the volume; vol. 2's Chapter Two 1–151 and Chapter Three 1–885; vol. 3's Chapter Four 1–999); vol. 11's print starts again in each chapter, and the appendices of vol. 3 start again at 1 in each appendix. In those cases the vault keeps its own through-numbering.
- The converter's numbers drift from the print where two footnotes ran together or one was split in two; readers split, join and renumber so that every call meets its own text, and the lead gives the printed numbers (`--start`, `--map`). A number may therefore occur at the end of one note and the start of the next.
- The text layer has no call digits (Tesseract read the superscripts as quote marks, `?`, `TM` or stray letters), so the calls are read on the page images. Already-real calls that an earlier pass left inside Devanagari verse lines are moved to where the print has them; the English words that pass left there stay.
- Carried-over footnote text is usually already joined to its footnote; a definition split off from another often stays in the earlier page's footnote zone (harmless: Obsidian collects footnotes at the end).
- Vol. 2's Chapter Two (notes 02 and 03): most footnotes stand as plain paragraphs whose numbers the OCR lost, so the pre-pass does not see them; only 146–151 were made footnotes. They need a pre-pass that takes a paragraph without a number.
