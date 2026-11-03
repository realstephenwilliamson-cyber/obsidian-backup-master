---
type: prompt
updated: 2026-11-03
---
# SDK 2 - Page labels, held and misread (Nov 2026)

For Claude running through the Agent SDK on the laptop (`vault_agent.py`), started with `py vault_agent.py sdk2-pagelabels.txt claude-opus-5-5` in `C:\Users\welln\vault-agent\`. Written on 3 Nov 2026 by the audit-corrections session (Opus, cloud) from the project's record docs, which the SDK cannot read: what you need is here or in the files named.

## Status

- **3 Nov 2026, cloud session (pf620–pf630):** most of part 2 done; parts 1 and 3 not started.
  - Read blind by two Fable readers each (194 page images in two rounds; data and README in `.work/edits/audcorr-2026-11-03/`): **92 markers corrected in 28 notes** (the misreads, 13 blank opening pages filled by the run where printed pages on both sides fix them exactly, and neighbours that print a number other than their marker).
  - *The Apostolic Fathers* (Roberts), a born-digital PDF printing PDF − 40: **all 235 markers off that run settled from the PDF's text layer** (checked first against 31 pages the readers had read), with 14 `page_range` values and 14 index labels (pf628–pf630; `textlayer_fix.py`).
  - Left for part 2: `.work/edits/audcorr-2026-11-03/descents-left.json` (51: Śivādvaita Nirṇaya 21, which with `held-sivadvaita.json` needs the whole book looked at, since its pages print Devanagari numerals, the readers confused ४ and ५ and it seems to have two numberings; 14 restarts to 1–3, most of them legitimate; 16 others, several known repeats: *Speak Truth to Power* pp. 51–52, *Acting Out* 64–65, Malini 06 112–113, a Dyczkowski repeated scan page) and `left-in-changed-notes.json` (offset shifts in *Society Must Be Defended* 05, Rastogi's *Introduction* 07, Dupuche 10 and *Krama* Part 4 02, whose `page_range` "738–75" is still broken). False alarms, leave: Dhvanyāloka 26 PDF 837–839 and Abhinavabhāratī 05 PDF 130–132 print what their markers say.
- Done before this prompt (3 Nov, pf610–pf611): Malini Vijayottara Tantra 01's front matter ("1–5; 1–2; i–iii; 1–28") and Russell VSI 02–06 (PDF 9–13 = viii–xii from the contents page; PDF 7, 8, 14 = `[PDF n]`). Do not redo them. Stephen on Malini: the scan is poor; mark it as best as can be read and move on.
- A session that works on this task updates these lines at its close.

## Before you start

1. Read [[House rules for AI work]] (binding), the *For AIs* section of [[Vault Guide]] (and its page-marker rule), the top three entries of [[AI log]], and the scripts note *Page labels* (`AI/Prompts/Scripts/Library conversion/Page labels/`).
2. Ask Stephen to confirm that no other AI is working on the vault (the cloud chat included). Ask him to start the runner if Obsidian was restarted (the line is in the house rules, *The job runner*); queue a trivial job and read its result before relying on it.
3. The standing rules in short (the house rules govern): never write the divine name (character-class scans, counts only); nothing under `.obsidian`; no zip files; no downloads; Stephen's writing only after an approved diff; renames, moves and deletes only through Obsidian; every full path 240 characters or less; nothing made up.
4. **Never open a PDF view or render pages inside Obsidian** (a runner job that did so hung the runner on 2 Nov 2026; `render-strips.js` and `render-strips-pack.js` in the scripts folder do exactly that, so do not queue them). Render on the laptop with Python and PyMuPDF (`fitz`) at 110 dpi, full pages, into `C:\Users\welln\fnwork\pagelabels-2026-11\` (outside the vault). Ask before `py -m pip install pymupdf` if it is missing.
5. **Jobs:** one `(async () => { … })()` expression per file in `.work/queue/`, UTF-8 without a byte-order mark, `// APPLY` as the first line to write. The next free job number (`pfNNN`) is in the top AI log entry. Edits through `.work/edits/edits-job2.tpl.js` with `.work/edits/mkjob.py` (whole marker lines or frontmatter lines, each occurring once); the check job after an apply from `.work/edits/sdk-templates-2026-11-03/pf538-pl28j-check.js` (new name, your backup folder).
6. **Cost:** say the running cost after each part. Stop and report at **$50**, at a part boundary.

## Stephen's rule (28 Oct 2026)

A page that prints no number takes the run's number only where printed pages on both sides fix it exactly; anything less certain stays `[PDF K]`. A `page_range` or an index label is changed only when both its ends are fixed. A page that does print a number gets the number it prints (a misread is corrected to what is on the page, read by two readers).

## The reading method (28 Oct, sixth session)

Render the pages an entry rests on and their neighbours, shuffle them with a fixed seed, and give them to **two reader subagents** (the Task tool, model sonnet) **blind**: each gets only the images and `page-number-fullpage-brief.txt` from the scripts folder (full pages: the strips of 28 Oct missed running heads), never the number the note has or the number you expect. Keep only what both readers agree on; list the rest for Stephen with both readings. `run_pinned.py` sorts entries by the rule above.

## Part 1: the 80 held entries

`.work/edits/pagelabels-2026-10-28j/held-after-28j.json` (read the `README.txt` beside it): 79 page ranges and index labels whose first or last page is not yet fixed, and Vasudeva 02's PDF 41, each with `why_still_held`. Read the pages each rests on; apply what the readings and the rule settle; list the rest.

## Part 2: misread printed page numbers (audit D-06)

Mostly done on 3 Nov (see *Status*). What is left is in `.work/edits/audcorr-2026-11-03/descents-left.json` and `left-in-changed-notes.json`. The scripts of 3 Nov are in the scripts folder: `descent-survey.js` and `run-break-survey.js` (read-only runner jobs that make such lists), `read_compare.py` (render, shuffle, compare two readers, write an `edits-job2` spec; it uses `pdftoppm`: on the laptop use PyMuPDF for the rendering part) and `textlayer_fix.py` (only for born-digital PDFs with a constant offset). For each case: read the page(s) blind as above; correct a marker where both readers read the printed number; fill a page that prints nothing only by the rule; then fix the `page_range` and index label that depend on it, only when both ends are fixed. A repeated scan page keeps its repeated number, as on 28 Oct (*Speak Truth to Power*, *Acting Out*), or an `r`-label in Dyczkowski's copy (night 3's practice). Śivādvaita Nirṇaya: look at the whole book first (its contents page, how the Sanskrit and English pages are numbered) and propose a plan to Stephen before changing anything there.

## Part 3: placeholder markers (audit D-05)

`.work/edits/audcorr-2026-11-03/placeholder-suspects.json` (pf620; made before the 3 Nov corrections, so skip any marker they changed): 58 markers in 48 notes of the form `*[p. K]* ^pgK` (printed number = PDF number, the old converter's stand-in for an unnumbered page) whose neighbours do not continue that number. The audit found 15 such notes besides the three it fixed; this list is wider and includes single-page notes and legitimate cases. Read each page blind; a page that prints its number keeps or gets it; a blank, half-title or part-title page follows Stephen's rule (the run's number only where both sides fix it exactly, else `[PDF K]`); then the ranges and labels as above.

## Close

- An entry at the top of [[AI log]], dated the day, "done with the Agent SDK on the laptop": counts per part, the backups, what is left (with page numbers and both readings), the last job number, the total cost.
- New scripts in `AI/Prompts/Scripts/Library conversion/Page labels/` (a row each in *Page labels*); the readings and what is left in `.work/edits/pagelabels-2026-11/`.
- This session's jobs and results to `.trash/work-pagelabels-<YYYY-MM-DD>/` with the adapter; never `.work/plan`, `.work/edits` or the backups.
- The *Status* lines of this note updated.
- A short report to Stephen.
