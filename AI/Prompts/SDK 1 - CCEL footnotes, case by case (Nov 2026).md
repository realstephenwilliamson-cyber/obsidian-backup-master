---
type: prompt
updated: 2026-11-03
---
# SDK 1 - CCEL footnotes, case by case (Nov 2026)

For Claude running through the Agent SDK on the laptop (`vault_agent.py`), started with `py vault_agent.py sdk1-ccel.txt claude-opus-5-5` in `C:\Users\welln\vault-agent\`. Written on 3 Nov 2026 by the audit-corrections session (Opus, cloud) from the project's record docs, which the SDK cannot read: what you need is here or in the files named.

## Status

- **3 Nov 2026:** written; not started. A session that works on this task updates these lines at its close. The top entries of [[AI log]] are the authority on what has been done since.
- **3 Nov 2026, 14:25–15:45 (Claude Code on the laptop): done.** All 123 blocks read; 102 put right in 35 notes (pf635–pf649, pf655–pf657); blocks matching the PDF's list 1,761 → 1,857 of 1,884; the other 27 read right against the print except Augustine 07 p. 15. **Left:** three deletions for Stephen in `.work/edits/ccel-2026-11/for-stephen.jsonl`. Scripts in `AI/Prompts/Scripts/Footnotes and endnotes/ccel-c01b/sdk1-2026-11/`.
- **3 Nov 2026, 16:37–17:30 (cloud chat): checked blind and closed.** 30 of the 98 changed page blocks, two readers each: no footnote text SDK 1 wrote differs from the print; the older converter leftovers the readers noticed are listed in `.work/edits/ccel-2026-11/blind-check-2026-11-03/README.txt`. The SDK plan is dropped (no API credit).
- Done before this prompt: Chrysostom on Matthew 05, note 48 restored ("\[πολιτεα.\]") and page block `^pg32` (nn. 55–62) put in the "N text" form (pf613, 3 Nov; audit items C-03 and C-06).

## Before you start

1. Read [[House rules for AI work]] (binding), the *For AIs* section of [[Vault Guide]], and the top three entries of [[AI log]].
2. Ask Stephen to confirm that no other AI is working on the vault (the cloud chat included). Ask him to start the runner if Obsidian was restarted (the line is in the house rules, *The job runner*); queue a trivial job and read its result before relying on it.
3. The standing rules in short (the house rules govern):
   - never write the divine name; scan with character-class patterns and report counts only;
   - nothing under `.obsidian`; no zip files; no downloads;
   - Stephen's own writing (`Projects/`, `Journal/`, concept and hub notes) only after he approves a diff;
   - renames, moves and deletes only through Obsidian; every full path 240 characters or less;
   - nothing made up: every count from a script you ran, every reading from the page.
4. **Never open a PDF view or render pages inside Obsidian.** A runner job that did so hung the runner on 2 Nov 2026. On the laptop, use Python with PyMuPDF (`fitz`): page images at 110 dpi and the PDF's text, into `C:\Users\welln\fnwork\ccel-2026-11\` (outside the vault). Ask before `py -m pip install pymupdf` if it is missing. Read the notes straight from disk; the runner is for writing.
5. **Jobs:** one `(async () => { … })()` expression per file in `.work/queue/`, UTF-8 without a byte-order mark, first line `// APPLY` to write (otherwise a dry run). Take the next free job number (`pfNNN`) from the top AI log entry. More than a handful of notes → through the runner (house rules, *Working on the laptop*). Templates: `.work/edits/edits-job2.tpl.js` with `.work/edits/mkjob.py`, and the finished jobs in `.work/edits/sdk-templates-2026-11-03/` (read its `README.txt`).
6. **Cost:** say the running cost after each group of blocks. Stop and report at **$70**, at a group boundary, with what is left.

## The task

Two CCEL books converted on 7–9 Oct 2026, whose footnotes the 28 Oct sessions moved and restored (scripts note: *CCEL footnote runs*, in `AI/Prompts/Scripts/Footnotes and endnotes/ccel-c01b/`):

- Augustine, NPNF1 6: notes in `Library/Christianity/Sermon on the Mount, Harmony of the Gospels, Homilies (Augustine)/`; PDF `Library/Christianity/Augustine - Sermon on the Mount, Harmony of the Gospels, Homilies (NPNF1 6).pdf`.
- Chrysostom, *Homilies on Matthew* (NPNF1 10): notes in `Library/Christianity/Homilies on Matthew (Chrysostom)/`; PDF `Library/Christianity/Chrysostom - Homilies on Matthew (NPNF1 10, 1888).pdf`.

What is left (about 3–7 % of the page blocks):

- **127 page blocks** whose footnotes still differ from the PDF's footnote list: `.work/edits/c01d-2026-10-28/differ-127.json` (27 Augustine, 100 Chrysostom). Kinds: 76 with Greek the converter damaged or a note split across pages, 28 numbers that could not be moved uniquely, 23 lost calls, 38 other. Chrysostom 05 `K32` was done on 3 Nov.
- **135 held cases** with the reason each was held: `.work/edits/c01d-2026-10-28/held-135.json`. Four are already closed (audit C-04): Chrysostom 10 N815 K244; Augustine 26 N2887 and N2889 K823–824; Chrysostom 20 N2215 K618. Chrysostom 05 N48 was done on 3 Nov. Most of the rest sit in the 127 blocks.

## Method (28 Oct sessions, adapted to the laptop)

1. **Fresh text.** With PyMuPDF, write the PDF text of every page of both PDFs and the current text of every note of both books into `C:\Users\welln\fnwork\ccel-2026-11\` (`pdftext.json` as `{pdf path: {K: text}}`, `notes.json` as `{note path: text}`, the format of the 28 Oct dump; `pf525-ccel-dump-DO-NOT-QUEUE.js` in the templates folder shows it, but do not queue it). The scripts were built on pdf.js text, so first run `diff_blocks.py` (with `PYTHONPATH` set to the ccel-c01b folder) on three blocks you know and compare with `differ-127.json` before trusting it on all.
2. **Readers.** One reader subagent per page (the Task tool, model sonnet): the page image, the block's footnote text from the note, and the PDF's text for that page, with `reader-brief.txt` from the ccel-c01b folder. The reader writes exact old/new edits.
3. **Your check** of every proposed edit against the PDF text: characters only added or moved, never dropped; `<sup>` calls and `^pg` lines unchanged; Greek kept in the form of the PDF's own text (this edition's text layer drops some accented letters, e.g. `πολιτεα`, `φιλοσοφαν`; the notes follow it).
4. **Blind check** by a different subagent with `footnote-check-brief.txt`: it gets the page image and the edited block, never the reader's edits. Watch notes whose texts are identical (Chrysostom 05's 42 and 43 caught a pass out on 28 Oct).
5. **Apply** in groups of about 20 blocks: an `edits-job2` spec (whole page blocks or exact strings, each occurring once), a dry run, the apply with backup `.work/backup-ccel-2026-11-<DD>/`, then a check made from `pf528-c01d-check.js` (new name, your backup folder). After each apply: unresolved links 16 files / 30 links (the baseline since 26 Oct); the divine-name count of each changed note equal to its backup's.
6. A case the readers disagree on, or the page cannot settle, is listed for Stephen with the page number and both readings; it is not guessed.

## Close

- An entry at the top of [[AI log]], dated the day, "done with the Agent SDK on the laptop": what changed with counts, the backups, what is left, the last job number used, the total cost.
- New or changed scripts saved in the ccel-c01b folder (update *CCEL footnote runs*); data for what is left in `.work/edits/ccel-2026-11/`.
- This session's jobs and results moved to `.trash/work-ccel-<YYYY-MM-DD>/` with the adapter (house rules, *When you finish*); never `.work/plan`, `.work/edits` or the backups.
- The *Status* lines of this note updated.
- A short report to Stephen.
