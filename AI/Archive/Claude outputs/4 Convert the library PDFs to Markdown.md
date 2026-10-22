---
type: prompt
updated: 2026-10-06
---
# 4 Convert the library PDFs to Markdown

**Use when:** after phase 3.

**What it does:**
- turns every book and article in `Library/` into notes, with a page anchor at each page, so the library reads, searches and links on every device;
- folds the OCR fixes from the 6 Oct spot-check into the conversion;
- keeps the PDFs in the vault on this computer, for page numbers and layout. Sync will leave them off the phone and tablet.
- On the computer, each catalog note gets an *Open the PDF* button.

**Expect:** the largest phase, several sessions. It starts with a pilot of 8 books for your approval, then works through batches of about 80 books on its own. Each new task picks up from the progress doc.

````text
Phase 4 of my October 2026 plan for my Obsidian vault (C:\Vaults\Obsidian Vault): convert the PDFs in Library to Markdown notes, so the library reads, searches and links on every device.
The PDFs stay in the vault on this computer (decided 6 Oct 2026), and Obsidian Sync will leave them off the phone and tablet.

FIRST read Prompts/October 2026 plan/0 Plan - read me first.md and follow its rules. Then read the progress doc. If this phase has already started, resume from the progress doc and .work/plan/phase-4-state.json, and don't redo finished books.
Then read:
- Vault Guide.md → The catalog; Adding things → "An e-book converted to Markdown";
- Prompts/Make scans searchable (OCR).md → "Known issues from the 6 Oct 2026 spot-check", and Prompts/Scripts/OCR scripts.md;
- Prompts/Scripts/PDF inventory (6 Oct 2026).csv (678 PDFs, 167,436 pages, and where each one's text comes from);
- Notes/Vault analysis (6 Oct 2026)/Checked findings.md (the OCR and catalog findings);
- .work/plan/phase-4-prep/, if it exists;
- one existing conversion as the model: Library/Philosophy/Play as Symbol of the World (Fink)/ (an index note, one note per chapter, footnotes, [p. N] markers).

0. Performance first. My condition for keeping the PDFs in the vault is no lag in searches or views.
   - Before converting, measure on the computer:
     - whether Omnisearch indexes the PDFs (through Text Extractor), and how long a search takes;
     - how long Library.base and Home take to open;
     - Obsidian's own search for a common word.
   - Measure again after the pilot and after every few batches.
   - What can cause lag, and the setting to tell me (settings are mine to change):
     - Omnisearch indexing PDF text: turn PDF indexing off once a book is in Markdown, since its text is then in the notes;
     - Obsidian's Settings → Files and links → Excluded files: a pattern for PDFs keeps them out of search, the graph and the quick switcher, while links still open them;
     - Smart Connections: exclude the PDFs, and the converted-book folders if I want;
     - Bases that take in whole folders (fixed in phase 1).
   - If searches or views still lag after these, stop and tell me. Moving the PDFs out of the vault is then reconsidered.
1. Classify every PDF, and list the ones you propose NOT to convert, with the reason, for my decision. Likely candidates:
   - the 2 DjVu files;
   - books that are mostly plates, plans or diagrams;
   - dictionaries already in the vault as data (Monier-Williams has a TSV), and dense multi-column dictionaries;
   - the KSTS Sanskrit volumes, whose text is in Texts/Tantraloka;
   - books already converted: Fink, the Lombardo/Davis Gita, Olesen, Broo, Matt, Padoux's Tantric Mantras, Bansat-Boudon's Paramarthasara;
   - worksheets and music.
2. The format of each converted book:
   - Folders and notes:
     - Library/<Subject>/<Short title (Author)>/, with an index note (type: book, the table of contents as links) and one note per chapter;
     - chapters come from the PDF's bookmarks; without bookmarks, use parts of about 40 pages.
   - Page anchors:
     - at the start of each PDF page, a line `*[p. N]* ^pgK`;
     - N is the printed page number when it can be read, otherwise the PDF page number; K is always the PDF page number;
     - so any `#page=K` link can become `[[Chapter note#^pgK]]`.
   - Frontmatter on every note: type, work (a link to the catalog note), source_pdf (path), pages, text_source, converted (date).
   - Text:
     - footnotes as Markdown footnotes;
     - running headers and footers removed;
     - hyphenated line ends joined, but real hyphens kept, including those in Sanskrit compounds;
     - paragraphs reflowed;
     - unreadable spans marked `[illegible]`;
     - never invent text.
3. Where the text comes from, by class, with the OCR fixes from the spot-check folded in:
   - Born-digital with good text: PyMuPDF.
   - Private-use glyphs or garbled diacritics: the OCR text.
     - For 'ocr-overlay' files, use only the GlyphLessFont OCR layer, not the old font layer.
     - Otherwise OCR the pages: Latin, plus san where there is Devanagari, plus heb or grc where needed. The Greek model wasn't used in October; use it for Greek now.
   - ocr-skip and ocr-redo files: the OCR layer. Rastogi's Introduction (job 158) has its text twice; use one copy.
   - Devanagari-heavy books: a Tesseract plain-text pass, because the PDF text layer splits words at ि. Test on one book first.
   - Post-fixes, each tested on one book first:
     - the anusvāra: `rh`, `ħ` or `ń` → ṁ, only inside words with other IAST letters;
     - italic words turned into strings of digits in the Latin+san layer: re-OCR those pages with Latin alone and compare;
     - deskew skewed pages before OCR.
   - Hebrew: keep the right-to-left text in order, and check one page by eye.
4. A pilot of 8 books:
   - a born-digital English book;
   - a born-digital IAST-heavy book;
   - one Dyczkowski Tantrāloka volume (its extraction is reused in phase 5);
   - an overlay stotra;
   - a Hebrew or Judaica book;
   - a two-column journal article;
   - a book with heavy footnotes;
   - one redo book.
   For each, show me 3 pages beside the page image, and the folder layout. Wait for my approval.
5. Batches, after approval: about 80 books each, lowest risk first.
   - One workflow per batch:
     - an agent per book: stage the PDF, convert it, check its own work;
     - a separate checking agent per book: 3 random pages against the page image, diacritics present where the source has them, every ^pgK present, footnotes attached.
   - The lead bundles the notes into JSON files of 25 MB or less in .work/, and creates the notes in Obsidian's console with app.vault.create. Never thousands of single commits.
   - After each batch:
     - the note count;
     - the unresolved-link count unchanged;
     - Home opens;
     - the performance check;
     - update the progress doc and the state file.
6. Catalog notes (back them up first):
   - add the Markdown index note to files:, keeping the PDF;
   - add an "Open the PDF" button: a small view, Templates/Views/open-pdf, that calls app.openWithDefaultApp for the PDF. On a phone it says the PDF is on the computer.
7. Links, each as its own dry run for my approval:
   (a) Tantraloka - secondary literature (about 4,700 citations): add the Markdown page link beside each PDF link.
   (b) The KSTS verse-page map: only if phase 2 didn't make it local already.
   (c) The 23 PDF links in my writing: list them only.
   The verse notes' Dyczkowski links are phase 5; links inside the converted books are phase 6.
8. When all batches are done, update:
   - Prompts/Make scans searchable (OCR).md, with the fixes that worked (it stays a routine prompt);
   - Prompts/Add new files from Downloads.md: a new PDF is now converted as part of filing it;
   - the Guide (layout, the catalog, adding things, the Omnisearch row), with a History line.

Approval points: the not-to-convert list; the pilot; each link dry run.

This phase takes several sessions. Keep going batch after batch without waiting for me, except at the approval points. When a usage limit stops you, I'll say "Continue".
````

**Afterwards:**
- Open a converted book on the phone, and follow a citation from the Tantrāloka index to its page.
- On the computer, try the *Open the PDF* button.
- Notice whether search feels as fast as before.
- Then start [[AI/Archive/Claude outputs/5 Dyczkowski into the verse notes]].
