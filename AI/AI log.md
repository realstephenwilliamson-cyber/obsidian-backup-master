---
type: log
---
# AI log

What each AI session changed in the vault, newest first, in a few lines: the date, what changed (with counts), where its backup is, what it left. The [[House rules for AI work|house rules]] ask for an entry after every session. What the vault holds and how it works is in [[Vault Guide]].

On 3 Nov 2026, at Stephen's word, the records of the build (6 Oct – 3 Nov 2026) were cut to what a later session will use: this log's earlier entries and the build's reports, decisions and finished prompts went to `.trash`. Their last versions stay in the vault's Git history (for this note: `git log -p -- "AI/AI log.md"`).

**Next free job number: pf688.**

## Open work

Left unfinished on purpose, with where its data is. Each item is a session of its own; none is urgent. Delete an item when it is done.

- **Dyczkowski's Tantrāloka translation** (the library copy, `Library/Trika/Tantraloka (Dyczkowski)/`):
    - 741 `\[illegible\]` placeholders in 706 places: about 206 that the PDF's text layer could not place on a page, about 500 where the two blind readers did not agree or flagged the spot. The list: `.work/edits/fnleft-2026-11/gaps-left.json`; the method and scripts: [[Illegible gaps README (3 Nov 2026)]] in `AI/Prompts/Scripts/Viveka English/illeg-2026-11-03/`.
    - 8 footnotes left as plain paragraphs (5 whose call is in the note before, 3 whose call is on a line the OCR dropped): `.work/edits/fnleft-2026-11/README.txt`, part 2.
    - 56 numbered paragraphs left plain in 13 notes (footnotes with no call in the print or with the call in another note, and numbered lists); footnotes the print numbers but the note lacks (Chapter Nine 76, 235, 374; Twenty-Eight 124, 236, 347; Twenty-Nine 195, 196, 312, 470; Chapter Five 84–86, in a heading); vol. 10 prints two footnotes numbered 165 (the first, with no call, stays plain). Data: `.work/edits/dyfn/`; scripts: `AI/Prompts/Scripts/Footnotes and endnotes/dyczkowski/`.
- **Finn's footnotes:** 13 `<sup>` remnants and some junk lines that need the page read: part 5 of [[SDK 3 - Footnote leftovers in Dyczkowski, Kubjika and Finn (Nov 2026)]].
- **Page labels:** the held and misread page labels (ranges and index labels whose end pages are not fixed; the misread page numbers the audit's D-06 left; Śivādvaita Nirṇaya, whose Devanagari page numbers need a plan for the whole book): the *Status* of [[SDK 2 - Page labels, held and misread (Nov 2026)]]; data `.work/edits/pagelabels-2026-10-28j/held-after-28j.json` and `.work/edits/audcorr-2026-11-03/`.
- The two SDK prompts were written for the Agent SDK on the laptop; a chat session can follow their scope and method and skip the launch steps.
- **Stephen's own:** [[Open items]]; the Bible references left plain: [[Bible references to decide later]].

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
