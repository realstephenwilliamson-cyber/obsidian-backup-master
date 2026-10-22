---
type: prompt
updated: 2026-10-07
---
# Vault health assessment

> **Retired 21 Oct 2026**, kept in `AI/Archive/` for its checklist. The [[Monthly check-up]]'s report (`health-report.js`, no AI) and its follow-up prompt took its place; `health-counts.js` and `health-settings.js` ([[Health check scripts]]) still measure everything listed here.

**Use when:** about once a month, after a big change, before turning Sync back on, or whenever something on Home or in a Base looks wrong.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder and give it control of Obsidian, because most checks run in Obsidian's console. The assessment itself changes nothing. Fixes come afterwards, only the ones you approve.

````text
Run a health assessment of my Obsidian vault at C:\Vaults\Obsidian Vault. This is read-only until I approve fixes.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md
Confirm with me that no other AI tool is working on the vault.

Measure the following with scripts in the Obsidian console (the W helper and .work/ folder from the house rules); write the full results to .work/out/health-<date>.json.

1. Counts: files, Markdown notes and folders, compared with the last recorded figures (5 Oct 2026: 22,436 files, 20,342 notes, 51 unresolved links in 16 notes, catalog files: links 702 of 702).

2. Links:
   - unresolved links (app.metadataCache.unresolvedLinks), grouped by note and by target, separating new ones from the known remainder;
   - links to missing headings or block IDs (#^…), checked against each target's cached blocks and headings;
   - ambiguous names: two notes with the same base name, which makes [[Name]] ambiguous;
   - embeds of missing images or files.

3. Catalog (Catalog/**):
   - every file in Library/<Subject>/ (PDF, DjVu, e-book folder) has exactly one catalog note linking it in files:;
   - every files: link resolves (notes with text: print are books I have only on paper; their files: is empty on purpose);
   - property types are right (year and pages numbers, lists as lists, subject from the allowed list, text and status values from the Guide);
   - notes in status: review and their reasons;
   - text: scan notes;
   - catalog notes whose subject doesn't match their folder.

4. Names: non-ASCII file or folder names outside the places the Guide allows them (the Greek lexicon); forbidden characters; " (1)" or " copy" endings; double spaces.

5. Properties across the vault: names that differ only in case (Title vs title), and values whose type conflicts with the vault-wide type of that property.

6. Empty notes, empty folders, and orphans: non-note files nothing links to (excluding Library files, which are reached through the catalog). Leave Journal and Writing out of the orphan list.

7. Scripts and dashboards:
   - Home renders without errors (open it and check the console);
   - the calendar tables in Calendar cover today and at least the next 12 months; they currently end on 31 Dec 2029;
   - the study-plan tables have a row for today;
   - Templates/Views scripts load.

8. Size and Sync:
   - the vault's total size, split by PDFs, .txt e-texts, audio, images and notes;
   - the largest 20 files;
   - the size of .trash and of any .work or scratch folders;
   - the result against the Sync Plus limit (10 GB, version history included), and the 200 MB per-file limit.

9. Stray material:
   - files at the top level other than Home.md and Vault Guide.md;
   - folders not listed in the Guide's Layout table (ignore Attachments/ and _images/ folders, and dot-folders such as .obsidian, .trash and .smart-env, which are expected);
   - scripts or exports left by AI sessions (for example a "Claude outputs" folder, .work, leftover .js files outside Templates/Views).

10. Bloat assessment (the short form of area I in AI/Prompts/Vault analysis (micro and macro).md):
   - growth since the last run, by kind and by top folder; anything new over 50 MB;
   - the 20 largest notes, and folders of many small generated notes with how much they are used;
   - material held twice (a PDF and its Markdown conversion, one work in two files, superseded drafts, old approval and dry-run files);
   - plugin caches (.smart-env and the like), .trash, .work and Claude outputs;
   - properties, tags, templates, Bases views and scripts that nothing uses.
   For each: size or count, what it costs (Sync storage, speed, search noise, upkeep), and a recommendation (keep, slim, exclude from Sync, move out of the vault, or delete: listed, never deleted). Size alone is not bloat.

Report as one short table per area, with: what is fine, what is wrong (with exact paths), and for each problem a proposed fix marked safe (mechanical, reversible) or decision (needs my judgement). Do not fix anything until I say which fixes to make. Then make the approved fixes through Obsidian (dry run first, backups in .work/backup-health-<date>/), measure again, and report before/after numbers. List the decisions I haven't made in the AI log entry. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** compare the numbers with the last run (the report gives both). [[Vault Health & Phantom Link Manager|Vault Health]] shows the unresolved links live between runs.
