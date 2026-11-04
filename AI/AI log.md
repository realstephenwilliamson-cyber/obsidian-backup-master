---
type: log
---
# AI log

What each AI session changed in the vault, newest first, in a few lines: the date, what changed (with counts), where its backup is, what it left. The [[House rules for AI work|house rules]] ask for an entry after every session. What the vault holds and how it works is in [[Vault Guide]].

On 3 Nov 2026, at Stephen's word, the records of the build (6 Oct – 3 Nov 2026) were cut to what a later session will use: this log's earlier entries and the build's reports, decisions and finished prompts went to `.trash`. Their last versions stay in the vault's Git history (for this note: `git log -p -- "AI/AI log.md"`).

**Next free job number: pf707.**

## Open work

Left unfinished on purpose, with where its data is. Each item is a session of its own; none is urgent. Delete an item when it is done.

- **Dyczkowski's Tantrāloka translation** (the library copy, `Library/Trika/Tantraloka (Dyczkowski)/`):
    - 547 `\[illegible\]` placeholders in 517 places: 206 that the PDF's text layer could not place on a page, about 300 where a reader marked the reading low or flagged the spot, 10 where three readers did not agree. The list: `.work/edits/fnleft-2026-11/gaps-left.json`; the method and scripts: [[Illegible gaps README (3 Nov 2026)]] in `AI/Prompts/Scripts/Viveka English/illeg-2026-11-03/`.
    - 6 footnotes left as plain paragraphs: 167 in v02 06 and 165 in v04 10, which run over several pages mixed with the body text; 3 in v10 03 (footnotes 1–3 of Chapter Twenty-Eight have no calls); 3 whose call is on a line the OCR dropped. `.work/edits/fnleft-2026-11/README.txt`, part 2.
    - 56 numbered paragraphs left plain in 13 notes (footnotes with no call in the print or with the call in another note, and numbered lists); footnotes the print numbers but the note lacks (Chapter Nine 76, 235, 374; Twenty-Eight 124, 236, 347; Twenty-Nine 195, 196, 312, 470; Chapter Five 84–86, in a heading); vol. 10 prints two footnotes numbered 165 (the first, with no call, stays plain). Data: `.work/edits/dyfn/`; scripts: `AI/Prompts/Scripts/Footnotes and endnotes/dyczkowski/`.
- **Finn's translation:** the 13 `<sup>` remnants were settled on 3 Nov 2026 (entry below). The pages they sat on also had footnotes left plain or under the wrong label (pp. 116–117, 350–352, 372, 394); other pages may hold the same, and no full survey has been made. Lines of bare verse numbers that the OCR moved away from their verses (e.g. p. 117) are left.
- **Page labels:** the held and misread page labels (ranges and index labels whose end pages are not fixed; the misread page numbers the audit's D-06 left; Śivādvaita Nirṇaya, whose Devanagari page numbers need a plan for the whole book): the *Status* of [[SDK 2 - Page labels, held and misread (Nov 2026)]]; data `.work/edits/pagelabels-2026-10-28j/held-after-28j.json` and `.work/edits/audcorr-2026-11-03/`.
- The two SDK prompts were written for the Agent SDK on the laptop; a chat session can follow their scope and method and skip the launch steps.
- **Stephen's own:** [[Open items]]; the Bible references left plain: [[Bible references to decide later]].

## 3 Nov 2026 (evening, 19:22–19:40): Finn's 13 `<sup>` remnants and the footnotes of their pages (Opus lead in the cloud)

- **Stephen (19:22):** 73 % of the week; do Finn.
- **Done (pf701–pf703, 49 edits in 5 notes):** each `<sup>` call made a Markdown footnote call, with its definition, from the PDF's text layer (page images for p. 117 and the drawings): note 02 p. 65, the Introduction's notes 38–42 (all five were plain; labelled `-p65`, as the note does for repeated numbers); note 03 pp. 116–117, calls 183–188 (the converter had 185 under 183, 186 under 184-p117, 188 under 186, and 183 and 187 plain); note 05 p. 187 (156) and pp. 197–198 (188, 191, 193: drawings in the print, so the definitions say so); note 09 p. 345 (120), pp. 350–352 (134–138, 143–148; 145 and 146 had been one call off); note 10 p. 372 (221, which had 222's label, and 222), p. 394 (73), the plate on p. 399 (two tags taken off its junk text) and the bibliography on p. 413 (a stray 7; three entries run together). `<sup>` left in the book: 0.
- **Check (pf703):** calls and definitions paired in all five notes, every definition in Obsidian's footnote cache, `^pg` blocks, headings and divine-name counts equal to the backups; unresolved links 16 / 30.
- **Backup:** `.work/backup-finn-2026-11-03/` (to `.trash` after the Git commit, pf706). **Saved:** `.work/edits/fnleft-2026-11/finn-spec.json`; the script that wrote it, `AI/Prompts/Scripts/Footnotes and endnotes/finn-leftovers/finn-sup-2026-11-03.py`.

## 3 Nov 2026 (evening, 19:04–19:35): a third round of gap fills (189 settled); footnotes 308 and 598 made real footnotes (Opus lead in the cloud; one Sonnet reader)

- **Stephen (19:04):** Fable used up, 73 % of the week; use the remainder.
- **Gaps (pf688–pf690):** the 199 gaps whose two readings differed with both readers confident. 155 settled without a new reading: the two readings agree once footnote marks are taken out and the words a reader copied from either side of the gap (already in the note) are set aside; 27 of them were a footnote number standing alone next to its own label or call, so the placeholder was taken out. The other 44 read by a third blind reader; 34 filled where two of the three agree. 221 edits in 83 notes; placeholders 741 → 547. The brackets of 33 earlier fills escaped (`\[`, `\]`) as the converter writes them. Check: calls and definitions paired, all 6,217 definitions in the cache, `^pg` blocks, headings and divine-name counts equal to the backups.
- **Three calls kept from reading as links (pf695–pf697):** a fill in brackets right after a call (`[^34](Now,)`) made a Markdown link; the parenthesis is now escaped (v02 04, v08 09, v09 08).
- **Footnotes 308 and 598 (pf695–pf697):** the call read on the page (vol. 6 p. 456, after "enduringly the same)."; vol. 7 p. 307, after "(sādhaka)"), the call put there in v06 13 and v07 09, the definition moved there from v06 14 and v07 10.
- **Unresolved links** 16 / 30 again after the link fix (18 / 32 in between). This log, *Viveka English scripts* and the README updated by pf698–pf699.
- **Backups:** `.work/backup-gaps3-2026-11-03/`, `.work/backup-fn2-2026-11-03/` (to `.trash` after the Git commit, pf700). **Saved:** `.work/edits/fnleft-2026-11/` `gaps3-spec.json`, `gaps3-decisions.json`, `fn2-spec.json`, `gaps-left.json` (now 517 places); the scripts of the round in `AI/Prompts/Scripts/Viveka English/illeg-2026-11-03/` (*round 3* in its README).

## 3 Nov 2026 (evening, from 17:35): the inner `[illegible]` gaps in Dyczkowski's copy (1,764 filled); the build's records trimmed (Opus lead in the cloud; Fable and Sonnet readers)

- **Stephen (17:35):** get as much done as possible; the logs, states and histories of the build may be trimmed or purged as long as a later maintainer is not hindered (no records for history's sake). He approved deleting all but ten of the project's docs.
- **Gaps (pf676, pf678–pf680):** every `\[illegible\]` run in the 128 notes of the library copy read on the page images: pass 1 the 1,566 runs placed on 27 Oct (the gap boxed on a 200 dpi strip), pass 2 the others, located by the PDF's text layer (698 of 904); two blind readers each; filled only where both wrote the same. 1,691 edits in 113 notes, 1,764 gaps; placeholders 2,607 → 741. Check: calls and definitions paired, all 8,065 definitions in Obsidian's footnote cache, `^pg` blocks and divine-name counts equal to the backups; one heading changed, as planned (a verse line that the OCR turned into a heading, v06 04, TĀ 9.43: the fill *kāmaṁ*); unresolved links 16 / 30. Against the OCR witnesses of 27 Oct, 1,233 of the 1,288 pass-1 fills score 0.5 or more.
- **Trim (pf681–pf686):** 52 notes to `.trash` (all of `AI/Archive/` but two lists, the session checklist, the orientation and audit-decision notes, *Vault Guide history*, three finished prompts); the links to them in the 10 staying notes that had any made plain or taken out; this log cut to this page; *AI*, the house rules, *Prompts - read me*, *Open items*, *Discuss next session*, the *Complete vault audit* prompt and *Viveka English scripts* brought up to date. In `.work`, everything but the runner, the edit templates, the data of the open work and the template backup that the templates' comments name went to `.trash/work-trim-2026-11-03/`, the `backup-*` folders with it (the notes' earlier versions are in Git and in Sync's version history). In the project, 125 docs deleted and 10 kept.
- **Backups:** `backup-gaps-2026-11-03/` and `backup-trim-2026-11-03/`, both in `.trash/work-trim-2026-11-03/` since the Git commit.
- **Saved:** `AI/Prompts/Scripts/Viveka English/illeg-2026-11-03/` (scripts, briefs, [[Illegible gaps README (3 Nov 2026)]]); the footnote check as a job template, `.work/edits/sdk-templates-2026-11-03/pf680-footnote-check.js`; in `.work/edits/fnleft-2026-11/`, `gaps-spec.json`, `gaps-decisions.json` and `gaps-left.json`.
- **Git (pf687):** committed and pushed.
- Meter at 17:35: 62 % of the week, 82 % of Fable. Fable's allowance ran out during the reading; Sonnet readers did the rest.

## Up to 3 Nov 2026: the build, in brief

Between 6 Oct and 3 Nov 2026 Claude sessions with Stephen rebuilt and completed the vault: the library catalogued and converted to Markdown (page markers, footnotes, links into the texts), the primary texts added (the Tantrāloka with Jayaratha's Viveka, Torah and Tanakh, the Zohar, the Talmud, the Bible, the Fathers), the calendar, the daily, weekly and homily notes, the page views, the health checks and the job runner. [[Vault Guide]] describes what exists; the tools are in `AI/Prompts/Scripts/` (start at [[Prompts - read me]]).
