---
type: prompt
updated: 2026-11-03
---
# SDK 3 - Footnote leftovers in Dyczkowski, Kubjika and Finn (Nov 2026)

For Claude running through the Agent SDK on the laptop (`vault_agent.py`), started with `py vault_agent.py sdk3-footnotes.txt claude-opus-5-5` in `C:\Users\welln\vault-agent\`. Written on 3 Nov 2026 by the audit-corrections session (Opus, cloud) from the project's record docs, which the SDK cannot read: what you need is here or in the files named. The items are the audit's (2–3 Nov 2026) A-03, A-04, A-07, E-02 and E-03; Stephen chose to have them done on 3 Nov.

## Status

- **3 Nov 2026:** written; not started. A session that works on this task updates these lines at its close. The top entries of [[AI log]] are the authority on what has been done since.
- Done before this prompt (3 Nov, pf613): v04 10 n. 173's gap filled with the print's "sādhya-"; Finn 03 and 04's stray colons after calls removed (pf605).

## Before you start

1. Read [[House rules for AI work]] (binding), the *For AIs* section of [[Vault Guide]], the top three entries of [[AI log]], the scripts note *Footnote and endnote scripts* (`AI/Prompts/Scripts/Footnotes and endnotes/`) and, in its `dyczkowski/` folder, the README.
2. Ask Stephen to confirm that no other AI is working on the vault (the cloud chat included). Ask him to start the runner if Obsidian was restarted (the line is in the house rules, *The job runner*); queue a trivial job and read its result before relying on it.
3. The standing rules in short (the house rules govern): never write the divine name (character-class scans, counts only); nothing under `.obsidian`; no zip files; no downloads; Stephen's writing only after an approved diff; renames, moves and deletes only through Obsidian; every full path 240 characters or less; nothing made up.
4. **Never open a PDF view or render pages inside Obsidian** (it hung the runner on 2 Nov 2026). Render on the laptop with Python and PyMuPDF (`fitz`) at 110 dpi (200 dpi for footnote zones that read badly) into `C:\Users\welln\fnwork\fnleft-2026-11\` (outside the vault). Ask before installing anything.
5. **Jobs:** one `(async () => { … })()` expression per file in `.work/queue/`, UTF-8 without a byte-order mark, `// APPLY` as the first line to write; the next free job number (`pfNNN`) is in the top AI log entry. For exact edits use `.work/edits/sdk-templates-2026-11-03/pf591-audfix-apply.js` (a list `[{id, path, old, new}]`, each old once, a divine-name guard, a backup per file) and its check `pf606-finncolon-check.js`; read the `README.txt` there. Footnote checks after every apply: every `[^n]` call has one definition and every definition a call, and Obsidian's cache lists them all (`getFileCache(f).footnotes`; a definition run needs a blank line before it, the cause of the 186 Finn footnotes fixed on 3 Nov); `^pg` blocks and headings unchanged; unresolved links 16 files / 30 links.
6. **Readers:** blind reader subagents (the Task tool, model sonnet) given the page image and the neighbouring words, never the reading you expect; two per page where a word is restored; keep only what they agree on.
7. **Cost:** say the running cost after each part. Stop and report at **$70**, at a part boundary.

## The books

- Dyczkowski's library copy of the Tantrāloka: notes in `Library/Trika/Tantraloka (Dyczkowski)/Tantraloka vol NN (Dyczkowski)/` (`vNN MM` below is volume and note number); PDFs `Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. NN.pdf`. Footnote labels are the printed numbers (with the per-chapter constants of night 3, in the README).
- Dyczkowski's *Kubjikā, Kālī, Tripurā and Trika*: the notes whose path contains `Kubjika, Kali, Tripura and Trika (Dyczkowski)`; scripts `Footnotes and endnotes/kubjika/` (`reader-brief.txt`, `apply_ops.py`).
- Finn, *The Kulacudamani Tantra and The Vamakesvara Tantra*: `Library/Trika/The Kulacudamani Tantra and The Vamakesvara Tantra (Finn)/`; scripts `finn/` and `finn-leftovers/`.

## Part 1 (A-03): the leading `\[illegible\]` in 847 Dyczkowski definitions

847 definitions in 113 notes open with `\[illegible\] ` right after `[^n]: ` (pattern `^\[\^[^\]]*\]: \\\[illegible\\\]`). In the three cases the audit read (vol. 3 PDF 329 n. 827, vol. 5 PDF 320 n. 859, vol. 6 PDF 58 n. 86) the print has nothing between the number and the text: the placeholder stood for the garbled printed number, which the label now carries.
1. Draw 40 at random (fixed seed, stated) and have two blind readers say what the print has between the footnote number and the first word of the note.
2. If none of the 40 shows a lost word, strip the placeholder in all 847 (one apply, backup, check) and report the 95 % upper bound of the error rate (7.5 % for 0 of 40).
3. If any shows a lost word, stop the bulk strip: read every one of the 847 on the page (two readers), fill the word where both agree, strip where both see nothing, list the rest for Stephen.

## Part 2 (A-04): 8 footnotes left as plain paragraphs

- Call in the previous note (5): v02 06 n. 167, v04 10 n. 165, v06 14 n. 308, v07 10 n. 598 (the line "598?\. Concerning the figure of the sādhaka…", printed n. 329 on vol. 7 PDF 330; its call "(sādhaka)³²⁹" is on PDF 329 = v07 09), v10 03 n. 3. Stephen chose to move each definition into the note that holds its call, made a `[^n]` there with the call placed where the print has it, and taken out of the note that had it (check that the label is not already used in the receiving note).
- Call on a line the OCR dropped (3): v02 08 n. 419 (vol. 2 PDF 258: the subtitle "Visarga⁴¹⁹" is missing between `^pg258` and the verse), v08 10 n. 926 ("Appendix B"), v09 10 n. 493. Add the printed heading or words, read on the page by two readers, with the call, and make the definition a footnote.
- Vol. 10 prints two footnotes numbered 165 (PDF 280); the first has no call and stays plain. Leave it.

## Part 3 (A-07): ten split verse ranges

Still split or garbled after 26 Oct: "(179cd- 18180)" and "(40cd- 4lab)" in v07 02; "(137cd- 14140)" in v10 05; "(40cd- 44270)" in v10 17; "(330cd- 331lab)" in v08 06; "(221cd-" + two newlines + "223ab)" in v05 01; "(80cd-" + two newlines + "8lab)" in v06 04; "(110cd - 3)" in v11 12; "(90cd - 95ab)" and "(15 - 43)" in v09 20. Read each on the page; write the printed range; leave any the page does not settle.

## Part 4 (E-02): about 30 Kubjikā lines with the daṇḍa garble

The audit's check pass found about 30 lines where the printed `|` or `||` came through as two backslashes (`\\`, `|\\`, `\\1`); 35 four-backslash cases were fixed on 3 Nov. Find them with a scan, read each line on its page, and fix only what the page shows.

## Part 5 (E-03): a Finn pass like Kubjikā's

Finn's older garbles: 13 `<sup>` remnants, numbered footnote paragraphs still plain, and junk number lines. Use the Kubjikā method (`kubjika/`: readers write op lists, `apply_ops.py` applies and checks them). Finn's 1,135 footnotes are all in Obsidian's cache since 3 Nov; keep it so.

## Also (A-08)

`prepass.py` in `dyczkowski/` matches numbered paragraphs with `\d`, which in Python also matches Devanagari digits (v04 14 has a line `९\. `). If you use it, change the class to `[0-9]` and note it in the README.

## Close

- An entry at the top of [[AI log]], dated the day, "done with the Agent SDK on the laptop": counts per part, the backups, what is left, the last job number, the total cost.
- Scripts saved in the matching `Footnotes and endnotes/` subfolder (update the READMEs and *Footnote and endnote scripts*); readings and what is left in `.work/edits/fnleft-2026-11/`.
- This session's jobs and results to `.trash/work-fnleft-<YYYY-MM-DD>/` with the adapter; never `.work/plan`, `.work/edits` or the backups.
- The *Status* lines of this note updated.
- A short report to Stephen.
