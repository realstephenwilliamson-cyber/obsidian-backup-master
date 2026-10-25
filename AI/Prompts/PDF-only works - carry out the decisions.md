---
type: prompt
updated: 2026-10-22
---
# PDF-only works - carry out the decisions

**Use when:** Stephen has marked the rows of *PDF-only works - decisions* (carried out and trashed 22 Oct 2026) (`Notes/`; C convert, K keep as PDF, D delete). The prompt turns the marks into work: conversions by the library's own method, deletions through Obsidian, the catalog and the Guide's counts brought up to date. Written 22 Oct 2026 at the close of the orientation chat, so that the thinking is done on the note, at no cost, and the carrying out goes to a cheap model.

**Before you start:** close other AI tools; copy the vault folder, or let the task back up what it touches; Obsidian open with the runner line pasted (house rules → *The job runner*).

**Who runs it, model, size:** an AI session; Sonnet for the K and D rows and for conversions of born-digital PDFs; Opus or Fable when a C row is a scan or a garbled layer (OCR and a sample check). S for a dozen rows, M for the whole list; the OCR time is hours, not tokens.

````text
Carry out the marks on Notes/PDF-only works - decisions.md in my Obsidian vault at C:\Vaults\Obsidian Vault.

FIRST read AI/Prompts/House rules for AI work.md and Vault Guide.md (The catalog; Adding things; Plugins → What not to change or do) and follow them; then confirm with me that no other AI tool is on the vault and that the runner is running (queue a probe job and read its result).

1. Read the decisions note. List the rows by mark (C, K, D, blank) and the counts; ask about anything ambiguous before changing a thing. Blank rows stay as they are.

2. K rows: nothing to change. If a K row's catalog note says `status: review` or `text: scan`, leave it on the queues; do not clear them here.

3. D rows, one dry run for the whole set first:
   - For each work, from its catalog note's files: list the library files, and from app.metadataCache.resolvedLinks the notes that link the catalog note or those files (hubs, concepts, Stephen's writing, the Scholars pages, Incomplete Sets, the Tantraloka secondary-literature note, Smart Connections exclusions). Show me that list before anything is trashed; links in Projects/, Journal/ and the concept and hub notes change only after I approve a diff, the rest you re-point or unlink as the dry run proposes.
   - Apply: back the catalog note up to .work/backup-pdfonly-<date>/, then app.vault.trash(file, false) for the library file(s) and the catalog note, in a runner job. Never a shell or Explorer delete. A work whose catalog note has an About section or `print: true`: ask before trashing.
   - A scholar page lists its works live from the catalog; if a scholar is left with no work in the library, say so.

4. C rows: convert each work with the method of AI/Prompts/Add new files from Downloads.md, step 6 onward (the PDF is already filed): the text layer when it is good, a fresh OCR when it is a scan or a garbled font (AI/Prompts/Make scans searchable (OCR).md, step 3 for languages); the converter in AI/Prompts/Scripts/Library conversion/ (read Library conversion scripts.md first; the workspace mirrors the vault path so the OCR cache keys match); chapters from the PDF's bookmarks or the printed contents, each start page verified; a callout at the top of every note when the text came from OCR. Add the index note to the catalog note's files:, keep the PDF link. Sample at least three pages of every converted book against the page images before writing it in. Check: every page block ^pgK registered, no note name used twice in Library/, the files: links resolve, unresolved links not up.

5. Afterwards: count again (catalog notes with a Markdown copy; PDF only) and correct the Guide's Layout row for Library/ (the sentence "442 catalog notes (22 Oct 2026 …)" and "217 catalogued works (22 Oct 2026)"); update the Catalog subject indexes if they are not live; a dated entry at the top of AI/AI log.md with the counts and the backup folder; move the decisions note's done rows into a "Done" section at its foot with the date; clean your .work scratch as the house rules say (never .work/plan or the backups).

Report: a table of what was converted (notes, pages, text source), what was deleted (files, catalog notes, links re-pointed), what waits on me, and the new counts.
````

**Afterwards:** empty `.trash` when the deletions are settled; the Sync budget is unaffected (PDFs do not sync).
