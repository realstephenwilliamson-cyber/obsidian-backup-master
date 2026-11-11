---
type: prompt
updated: 2026-11-10
---
# Audit of the work since 3 Nov 2026

**Use when:** you want an independent check of what the AI sessions of 3–10 Nov 2026 did, without repeating the whole-vault audit. It is read-only and ends in a report; nothing is fixed. It builds on [[Complete vault audit]] (read it first: its rules for every agent, its checking pass and its report layout are used here unchanged) and replaces that prompt's SETTING and its agent list with the ones below, which cover only what is new. The whole-vault audit stays the prompt for a season's end.

**Why not the old prompt as it stands:** its SETTING is blank, its figures date from 14 Oct, and several parts name things that have since changed (*Home (mobile)*, *Library/Other*, the four old Bases). The old prompt was rated a day or more; this one covers less, and its cost is an estimate until it has run once.

**Before you start:**

- Close other AI tools; the runner line from the house rules ready to paste.
- Check the meters first. Page-image readers are the expensive part (a Fable reader about 120,000 tokens; four at once plus the lead fills most of a 5-hour window). Run the cheap wave first, read the meters, then decide on the Fable wave. If the container is above about 40 % used, wait for its reset.
- **Who runs it, model, size:** Sonnet or Opus as lead; Sonnet for areas B to E; Fable only for the page-image readers in area A. two waves (an estimate: a few hours; read the meters between them).

````text
Run an independent audit of the work AI sessions did in my Obsidian vault (C:\Vaults\Obsidian Vault) from 3 Nov 2026 (evening) to the present, and write a report. Read the prompt AI/Prompts/Complete vault audit.md first: its rules (read-only, no fixes, evidence for every finding, samples with numbers, the divine name left as the sources write it, download nothing), its CHECK pass and its REPORT layout apply here as if written out. Where it names areas A to K, use the areas below instead. You are the lead; I opt in to multi-agent work.

SETTING. The vault went into maintenance mode on 3 Nov 2026 after the build (6 Oct to 3 Nov). The last whole-vault check was the health report of 21 Oct 2026 (AI/Health reports/); anything before 3 Nov is outside this audit except as the baseline. What changed since is in AI/AI log.md (the entries from "3 Nov 2026 (evening, from 17:35)" to the newest; its Open work list says what was left). Earlier versions of every note are in Git; each session's backups are in .work/backup-*/ or .trash/work-*/. Files and measurements: as in the old prompt (stage files into your workspace, read-only jobs through the runner, scripts in AI/Prompts/Scripts/Health checks/). The vault changed on 10 Nov in ways the Guide may not yet describe: "Other" became Religious-Studies (Catalog/Religious-Studies/, Library/Religious-Studies/), Homer, Borges, Chan, Russell and the Larry May books are Philosophy; four Bases became Catalog/Library checks.base; Home (mobile) was deleted and its four buttons are in Home.md's Capture section; the homily page view gained a Glosses drawer (Templates/Views/homily-page/, 10 Nov 2026).

FIRST (lead): read AI/Prompts/House rules for AI work.md; Vault Guide.md; AI/AI log.md in full; Notes/Open items.md; Notes/Discuss next session.md; if attached, the project docs 07 and "State - read first". Run health-counts.js, health-settings.js and guide-numbers.js and compare with the 21 Oct figures. From Git, list every note added or changed since 3 Nov (evening), by top folder; the agents sample from that list. Ask me to confirm that no other AI works on the vault and that the runner is started, and give me your plan in ten lines before anything starts.

Known and accepted (not findings unless changed): unresolved links, 24 in all on 10 Nov (week notes not yet written, a future daily note, template code); catalog notes in status: review; the two DjVu books with no Markdown copy; Smart Connections exclusions needing my update in the plugin's settings (AI/Smart Connections exclusions.md says which); the Markdown copy of May's Genocide not made (my choice); Dyczkowski's Tantraloka library copy with 547 [illegible]; the page-label leftovers listed under Open work.

WAVE 1 (cheap; Sonnet agents, in parallel)

B. Structure and catalog. For all catalog notes (use a script, not a sample): subject equals the folder in Catalog/ and Library/; every files: link resolves; no catalog note without a file unless text: print; subject values against the Guide's list; the 14 notes in Catalog/Religious-Studies and the moved Philosophy ones; Catalog.base, Catalog/Library checks.base (its three views) and every other Base: open each (render-check.js), counts, errors. The Scholars pages (Knepper, Mohanty, May). Whether anything still says Other as a subject, Needs review.base, Physical Library.base, Shelf check.base, To delete.base. The CIS answer keys: the nine catalog notes (Chapters 4 to 12) and their MD copies in Study/Sanskrit against the pattern of Chapters 1 to 3: links, properties, pages.

C. Dashboards, views and templates. Home.md (Capture section above Tasks, buttons work, no link to a deleted page); Templates/Views/homily-page/view.js and view.css read as code: fragile assumptions, edge cases (a reading with no JANT note, a Holy Day with propers both, a Track 1 Sunday, a homily made before 5 Nov that embeds its texts, the polyphonic template, a verse note in two chapters), hard-coded paths, speed; the Homily templates against the view; Templates/Views changed since 3 Nov (git diff); the Health check scripts against what the vault now is. Render-check every dashboard, hub, plan, the Guide and every Base; report every error box or console error. I turned on Obsidian's core Slides plugin on 10 Nov; note it, change nothing.

D. The Guide, the prompts and the rules. Every path, number, plugin state and procedure in Vault Guide.md that the 3 to 10 Nov work touched, tested against the vault. Search every note outside AI/Archive, .trash and the dated reports for names that no longer exist ("Home (mobile)", "Phone page", "Library/Other", "Needs review", the four old Base names, "Other" as a subject) and list each hit with its path and line. AI/Prompts: each prompt's paths, property vocabularies and scripts against the vault; Prompts - read me's table; the house rules against how work is done now. AI/AI log.md's Open work, Notes/Open items.md, Notes/Discuss next session.md: complete and still true? The project doc "State - read first", if attached: does it agree with the vault?

E. Size, Sync, Git and hygiene. Figures against the 21 Oct health report: notes, files, size by top folder, the 30 largest files; .trash and .work (what is there, what could go); Git (last commit, anything uncommitted, size of .git); the remote vault as the Guide's Sync section describes it. A stratified random sample of 100 notes from the "changed since 3 Nov" list: properties against the Guide's vocabularies, broken links, placeholders, duplicates, names against the ASCII rule.

Read the meters with me, then:

WAVE 2 (page images; Fable readers, at most four at once, each saves its findings to a file before ending)

A1. Malinivijayottara (Texts/Malinivijayottara, 473 notes). Eight readers compared every text page with the notes on 10 Nov (72 notes corrected, pf818, after 151 on 9 Nov, pf813). NOT yet read by anyone: the introductions and the generated Devanagari. Read all introduction notes against the page images; 30 generated Devanagari verses against their IAST (the Devanagari is built from IAST: look for lost conjuncts and misplaced vowel signs); 20 random verse notes against the pages (^mula, ^iast, translation, footnote pairing); the five PDFs in Library/Trika, the catalog note and the line in Texts/Texts.md. Check that none of pf818's corrections was undone (compare with the backup).

A2. 1 Enoch, Lumpkin's Books of Enoch, the Dead Sea Scrolls (Texts/Qumran) and the JANT links made to them (9 Nov). Structure and 20 notes each against the sources; the count of Qumran notes without English (136 on 9 Nov) and that each says so; catalog notes and files; the 98 references to 1 Enoch elsewhere still plain (Open work).

A3. The JANT links: 1,832 (7 Nov) and 551 (9 Nov), plus the Sefaria links for Midrash Rabbah. From the diffs against Git or the backups (.work/edits/jant-links-2026-11-07/), draw 60 changed links at random; for each, read the JANT sentence and the verse the link opens and say right / wrong / doubtful; every link's target resolves (a script, all of them); the form of the Sefaria links.

A4. Dyczkowski's Tantraloka library copy and its footnotes, Finn's footnotes (1,100) and the page labels (3 Nov). 40 filled [illegible] gaps against the page images (zoomed strips at 250 dpi), 30 Finn footnotes against their pages, 30 page labels read from the printed page; the leftovers in Open work (are the numbers right?).

CLAIMS (the lead, after both waves). Take each AI log entry from 3 Nov (evening) to now as a list of claims. For each, say holds / holds in part / does not hold, with the numbers from the agents' samples and your own checks (counts through the runner, ten things the log says exist or work, looked at).

CHECK and REPORT as in the old prompt, with these areas (A1 to A4, B, C, D, E, Claims). The report goes to the project as claude/audit-<date>/Audit of the work since 3 Nov 2026.md; I say whether to save a copy in Notes/. Nothing is changed. When I choose actions, they go through the house rules in a new task (dry run, backups, one AI on the vault).
````

**Afterwards:** choose the actions; small safe ones can go through the [[Monthly check-up]]'s rules, big ones start from the matching prompt in AI/Prompts/.
