---
type: prompt
updated: 2026-10-05
---
# Check catalog notes against their files

**Use when:** notes are waiting in *Needs review* (`status: review`), or you suspect catalog details were filled from file names rather than title pages.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder. Control of Obsidian helps for applying the corrections.

**Who runs it, model, size:** an AI session reading title pages; Sonnet is enough. S: under an hour for about twenty notes.

````text
Check catalog notes in my Obsidian vault (C:\Vaults\Obsidian Vault) against the files they describe, and correct what is wrong.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md → The catalog
Confirm with me that no other AI tool is working on the vault.

Scope: every catalog note with status: review, plus any notes I name. If I say "all", sample 30 random catalog notes first and tell me the error rate before doing the rest. Notes with text: print have no file (books I have only on paper): check those against the publisher's page or a library catalog instead, and cite the link.

For each note:
1. Open its files: — the title page, the copyright/imprint page and the PDF metadata. Render the pages as images when the text layer is missing or garbled, and read them. Use the last pages too: some scans carry the volume's title page at the end.
2. Check every bibliographic property against that evidence, using the Guide's forms:
   - title with diacritics as printed. Every catalog note has a subtitle property: if it already holds the subtitle, keep that; otherwise put the subtitle after ": " in title and leave subtitle empty, as the Guide shows;
   - author, editor and translator as plain personal names, one per list item. For a translated classical text, the classical author goes in author and the scholar in translator/editor;
   - year of this edition (a number);
   - publisher "Name, City";
   - series, volume, and container for an article or chapter;
   - type, language, and pages (the PDF's page count for one file).
3. Change a value only when the evidence shows it. Never fill one from memory. If the file doesn't show it, you may settle one missing detail online; cite the exact URL in the note.
4. Leave text, subject, files, aliases and print alone. If the subject looks wrong, say so in the report instead.
5. Empty status (the key stays, with no value) when everything is settled. Leave it as review only if something important can't be settled, and say exactly what in the body.
6. Add one line to the body:
   **Checked against the file** on <date>: <one plain sentence saying what was confirmed or corrected; if still in review, what remains open>.
   Do not delete earlier dated lines.
7. Problems to report rather than fix: the file is a different work, badly incomplete (say which pages), a duplicate of another file, or misfiled by subject.

Work in batches of about 25. For each batch, write the proposed changes as JSON (note, changes, evidence, body line) and show me a summary; apply them through Obsidian (processFrontMatter for properties, vault.process for the body line) only after I approve. Have a second, independent pass re-check a random 10% of the results before applying; report its agreement rate.

Report: notes checked, corrected, still in review (with reasons), and the problems list. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** *Needs review* in *Catalog.base* (or `Catalog/Needs review.base`) should be shorter; what's left there needs your eyes.
