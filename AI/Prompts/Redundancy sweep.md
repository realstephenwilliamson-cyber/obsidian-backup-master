---
type: prompt
updated: 2026-10-05
---
# Redundancy sweep

**Use when:** before turning Sync on, after adding a lot of material, or when the vault feels cluttered: to find duplicate files, duplicate catalog notes, leftovers and things that don't belong.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder and give it control of Obsidian. Nothing is deleted without your say-so, and deletions go to the vault's `.trash`.

**Who runs it, model, size:** an AI session with the vault folder and the runner; Opus or Fable, because which of two copies is the better one is a judgment. M: about half a day for the whole vault.

````text
Do a redundancy sweep of my Obsidian vault at C:\Vaults\Obsidian Vault. Find what is duplicated, left over or out of place, and propose what to do. Change nothing until I decide.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md
Confirm with me that no other AI tool is working on the vault.

Look for:
1. Byte-identical files: same size, then the same MD5, anywhere in the vault. Note which copy the catalog links.
2. The same work in different files: two catalog notes for one work, or one work in two files (another edition, a scan plus a text copy, a partial copy, low-resolution spreads, an earlier draft). Compare title pages, page counts and sample text. For each pair, say which copy is better (complete, better scan, text layer, diacritics) and why. The 4 Oct 2026 rule applies: these pairs are LISTED for me, not deleted.
3. Duplicate catalog notes (two notes whose files: overlap or describe the same work): propose a merge. Keep the better note, fold in anything the other has, retarget links to the kept note, and send the other to .trash.
4. Empty notes, empty folders, notes that are only a title, and stray files: AI scratch folders (.work, "Claude outputs"), loose scripts, exports, zip files, "(1)" or " copy" files.
5. Material that doesn't fit the vault's purpose: items unlike the rest of their subject or of the library (out-of-date notices, news clippings, course handouts unrelated to the collection) and items filed under the wrong subject. Say why each stands out. Don't judge the content, only its fit.
6. Space: the biggest files and folders, and what removing or excluding them would save against the 10 GB Sync Plus budget.

Report as tables (identical files; same-work pairs; duplicate notes; leftovers; doesn't fit / misfiled; space), each row with a proposed action and its effect in MB. Then list the yes/no decisions for me at the end of the report and in the AI log entry.

Never trash a file from items 1–2 that belongs to a same-work pair, even if I approve its removal. Take the dropped copy out of its catalog note's files: and list it for me to delete myself; that is the 4 Oct 2026 rule. Byte-identical copies (item 1) may go to .trash once I approve.

When I approve items:
- move or rename them only through Obsidian;
- delete with app.vault.trash(file, false), so they go to the vault .trash;
- for a library file, remove it from its catalog note's files: first;
- retarget links before trashing a note.
Then check that unresolved links did not go up, and report before/after numbers. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** empty `.trash` when you are satisfied. Until then everything removed can be restored.
