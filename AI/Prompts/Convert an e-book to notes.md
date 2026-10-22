---
type: prompt
updated: 2026-10-05
---
# Convert an e-book to notes

**Use when:** you have an EPUB (or a clean born-digital PDF) of a book you want to read, quote and link inside Obsidian rather than as a separate file, like the Fink, Lombardo/Davis, Olesen, Broo and Zohar conversions. Obsidian can't open EPUBs itself, so the vault keeps converted notes rather than the EPUB.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder and the folder holding the e-book.

**Who runs it, model, size:** an AI session; Sonnet, the conversion is scripted ([[Library conversion scripts]]). S per book.

````text
Convert an e-book into notes in my Obsidian vault (C:\Vaults\Obsidian Vault), following the vault's existing conversions.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md → "An e-book converted to Markdown", The catalog, Links, Callouts
- One existing conversion as the model. Look at its index note and two chapter notes:
  Library/Philosophy/Play as Symbol of the World (Fink)/
  or Texts/Zohar/Zohar 12 - Zoharic Compositions/ for a text with folio markers.
Confirm with me that no other AI tool is working on the vault.

The book: <file name>. Ask me the subject if it's not obvious.

1. Identify the work from the e-book's metadata and title/copyright pages, then check the library for an existing catalog note or file (if there is one, the conversion is added to that note).
2. Folder: Library/<Subject>/<Short title (Author)>/ (Sanskrit-Study → Library/Sanskrit/; a primary text that is read unit by unit may belong in Texts/ instead, so ask). Images go in _images/ inside it, with ASCII names.
3. Notes:
   - an index note with type: book and the table of contents as links;
   - one note per chapter (or per natural unit), named "<Short title> NN - <Chapter title>" in ASCII, zero-padded so they sort.
   Keep:
   - headings as in the book;
   - italics and Greek, Hebrew and Devanagari text exactly;
   - page numbers as [p. N] markers where the e-book has page-list anchors;
   - notes as Markdown footnotes ([^n]), with every reference having its definition;
   - tables as Markdown tables, with pipes inside links escaped as \|.
   Front and back matter go in their own notes. Don't summarise or modernise anything.
4. Catalog note in Catalog/<Subject>/ (properties per the Guide; files: links the index note). Body: where the details came from, and "Converted to notes on <date> from <EPUB name>".
5. Checks:
   - every footnote reference has a definition, and no definition is orphaned;
   - no duplicate block IDs;
   - every internal link resolves;
   - the chapter count matches the e-book's table of contents;
   - a spot check of three passages against the e-book, word for word;
   - all images present.
6. If the book cites scripture, the Zohar or the Tantrāloka, offer to run AI/Prompts/Map new connections.md over the new notes.

Report the folder, the number of notes, the checks, and anything odd. Leave the original e-book where it was; don't copy the EPUB into the vault. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** open the index note and a couple of chapters; the catalog note should now point to them.
