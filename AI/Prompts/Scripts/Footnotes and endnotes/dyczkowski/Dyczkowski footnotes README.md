---
type: prompt
updated: 2026-10-27
---
# Dyczkowski footnotes - README

Scripts for turning the plain footnotes of the library copy of Dyczkowski's Tantrāloka (`Library/Trika/Tantraloka (Dyczkowski)/`, 177 notes) into Markdown footnotes, written on the night of 27 Oct 2026 from the Kubjika method (`../kubjika/`). They run in a Claude cloud workspace (paths such as `/home/claude/dyfn/` must be adapted); the vault is changed only by runner jobs. The state of the work is in `.work/edits/dyfn/progress.json`; the record of each night is a project doc in `claude/completion-2026-10/`.

| File | What it does |
|---|---|
| `prepass.py` | One note: numbered plain paragraphs (`971\. text`, `500?\. text`) → `[^n]: text`; a number that breaks the sequence is fixed from its neighbours or flagged; a clash with a real footnote is flagged and left plain; same-page continuation paragraphs indented; a page map (definitions, body lines, hints) in `pre.json`. |
| `packet.py` | The reader's folder for one note: the pre-pass text with line numbers, `pages.txt`, and the page images of every page with footnotes (200 dpi, greyscale, margins trimmed). |
| `reader-brief.txt` | The page reader's brief: place each call on the image; fix definition numbers, splits, carry-overs, strays; report what can't be decided. |
| `apply_ops.py` | Applies a reader's op list to the pre-pass text (with `--renumber`, relabels every footnote by the order of its calls, for readers who split run-together notes with letter labels; a call glued to `(` gets a space, since Obsidian reads `[^n](x)` as a link) and checks it against the original note: each number once as a call and once as a definition, calls in order, frontmatter, page markers, headings and block ids unchanged, the word-level differences listed for the lead to read. |
| `mkspec.py` | The whole-note spec for `.work/edits/textpatch.tpl.js` (oldLen/oldHash guard). |
| `batch.py` | One apply batch: refuses a note changed since it was read, writes the spec and three jobs (dry run, apply with backup, `dyfn-check`). |
| `sample.py`, `checker-brief.txt`, `compare.py` | The blind check: 8 footnotes per note (inserted calls and carry-overs first), the page image and the paragraph with the calls removed given to a checker that has not seen the note; its answers compared with the note. |
| `calib.py` | The calibration: a reader's result on vol. 5 part 8 (from its backup) against the converted note. |
| `dyfn-check.tpl.js` | The read-only check after each apply (a copy is in `.work/edits/`): divine-name counts against the backups, Obsidian's footnote cache by id, every `^pg` block still registered, every heading link into the notes resolves, unresolved links. |

**Data kept:** the readers' op lists (`ops-*.json`, with the lead's edits where there were any) and the blind checks' tasks, keys and answers are in `.work/edits/dyfn/`.

**Order per note:** stage the note → `prepass.py` → `packet.py` → a reader agent with `reader-brief.txt` → `apply_ops.py` (read the word differences) → blind check per batch → re-stage, `mkspec.py`, dry run, apply → `dyfn-check`.

**Facts about the book** (for the next reader): the vault numbers the footnotes through each volume (vol. 11 Chapter Thirty-Two starts at 364) while vol. 11's print starts again at 1 in each chapter (vol. 1 prints them through the volume, as the vault does); readers renumber where the converter's numbers had drifted from the print (two notes run together, a continuation numbered as a note), so a number may occur at the end of one note and the start of the next; the text layer has no call digits (Tesseract read the superscripts as quote marks or `?`), so the calls are read on the page images; in vol. 11 the converter had already joined most notes carried over a page break.
