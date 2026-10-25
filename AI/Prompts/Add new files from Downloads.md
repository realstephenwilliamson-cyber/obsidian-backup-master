---
type: prompt
updated: 2026-10-09
---
# Add new files from Downloads

**Use when:** new books, articles or chapters (PDF, DjVu, EPUB) have collected in Downloads, or in any folder you name, and should go into the library with catalog notes and a Markdown copy.

**Before you start:**

- Close other AI tools.
- In a new Cowork task, connect the vault folder and the folder the files are in. On this laptop that has been `C:\Users\welln\OneDrive\Documents\Downloads`.
- Give it control of Obsidian if you want it to check things in the app.
- **Who runs it, model, size:** an AI session; Sonnet for a batch of plain PDFs, Opus or Fable when the batch has scans to OCR or hard title pages. S for up to ten files, M for twenty to forty: the time goes on OCR and conversion, not on tokens. Collect new files in the Downloads folder *Add to Obsidian* and file them in one session rather than one at a time.

**Copy everything in the box into the task.** Edit the first line if you only want some of the files.

````text
Add the new library files from my Downloads folder (or the folder I connected) to my Obsidian vault at C:\Vaults\Obsidian Vault.

FIRST read these two notes in the vault and follow them; they override anything below:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md (sections "The catalog" and "Adding things, step by step")
Then confirm with me that no other AI tool is working on the vault.

1. Inventory. List the candidate files: name, size, type and date. Leave out installers, images, audio, spreadsheets and anything that is clearly not a book, article, chapter or thesis; list those separately and ask what I want. Ask before going on if the list is long or anything is unclear.
   EPUBs are not copied into the vault, because Obsidian can't open them. Identify them, check them for duplicates (step 3), and list them for AI/Prompts/Convert an e-book to notes.md.

2. Identify each work from the file itself, never from the file name alone.
   - For a PDF: the title page and copyright page (render them as images if the text layer is poor), PDF metadata and page count.
   - For an EPUB: its package metadata and title page.
   - Note the title with diacritics as printed, authors, editors, translators, year of this edition, publisher with city, series and volume, the container for an article or chapter, language(s) and page count.
   - If a detail is not in the file and you look it up online, cite the URL in the catalog note. If you can't settle it, leave it empty and set status: review.

3. Check for duplicates. Search the catalog (Catalog/**) by title, author and aliases, and compare page counts and MD5 hashes.
   - The same file already present: skip it and tell me.
   - The same work in a different file (another edition, a scan versus a text copy, a partial copy): tell me which looks better and why, and wait for my decision. If I keep both, they share one catalog note.
   - A catalog note with text: print for the same work (a book I had only on paper): add the file to that note's files: and set text, keeping its status and print. Don't make a second note.
   - A volume of a set the library already has: it joins that set's catalog note.

4. Subject and folder. The subject is one of Trika | Judaica | Christianity | Philosophy | Sanskrit-Study | Hinduism | Biblical-Studies | Other.
   - The file goes in Library/<Subject>/; Sanskrit-Study files go in Library/Sanskrit/.
   - The catalog note goes in Catalog/<Subject>/.
   - Choose by content, not by the shelf a bookseller used. Kashmir Śaivism, Krama and Kaula material is Trika; other Śaiva, Śākta, Purāṇic and Vedic material is Hinduism; Sanskrit grammars, readers and dictionaries are Sanskrit-Study. "Other" is for what fits none of these.
   - If unsure, say so and suggest one.

5. Name the file in ASCII: "Author - Short title (year).pdf", under about 100 characters, with no diacritics and none of [ ] # ^ | : * ? " < > \ /. For an edited volume, use "Editor (ed.) - Title (year)". COPY the file into the subject folder; leave the original in Downloads for me to delete.

6. Text layer. Extract text from about 12 pages spread through the file.
   - Fewer than about 150 characters a page means it is a scan: set text: scan and list it for OCR (AI/Prompts/Make scans searchable (OCR).md). Its Markdown copy (step 7) is made from a fresh OCR.
   - Text that comes out as gibberish (old Indic fonts, broken font maps) also goes on the OCR list, noted as needing an overlay.
   - Otherwise set text: searchable.

7. Convert it to Markdown (since 9 Oct 2026 the library keeps a Markdown copy of each book beside the PDF; Vault Guide → Layout). Skip this only for files I say to leave as PDFs, and ask first for very large files (over about 1,000 pages) or ones that are mostly pictures.
   - Use the scripts in AI/Prompts/Scripts/Library conversion/ (read its note first): the converter (conv.py) takes a small job file per book and writes the notes; the runner jobs put them into the vault through Obsidian and check them.
   - Text source: the PDF's own text layer when it is good; a fresh OCR (AI/Prompts/Make scans searchable (OCR).md → step 3 for languages) when it is a scan, gibberish, or someone else's poor OCR; or the layer with its junk words replaced from a fresh OCR. Sample a few pages of the result against the page images before deciding.
   - Format: a folder Library/<Subject>/<Short title (Author)>/ with an index note (named like the folder) and one note per chapter, from the printed contents or the PDF's bookmarks, otherwise parts of 40 pages. Chapter notes are named "<Short title> NN - <Chapter>" with previous · contents · next links. An article of a few pages is one note, Library/<Subject>/<Short title (Author)>.md.
   - Every PDF page starts with a marker *[p. N]* ^pgK, where N is the printed page number and K the PDF page, so links can point at a page. Footnotes become Markdown footnotes where their reference can be found. Devanagari, IAST and Hebrew are kept.
   - Frontmatter of each note: type (book or book-chapter), work (a link to the catalog note), book (a link to the index note), order, source_pdf (the PDF's vault path as plain text, not a link), page_range (the printed page range, as text; the index note keeps pages, the page count), pdf_pages, text_source (where the text came from), converted (the date).
   - If the text has known weaknesses (a fresh OCR of transliterated Sanskrit, a poor scan), say so in a short callout at the top of each note.
   - Names in ASCII, and no note name used twice anywhere in Library/ (a bare [[name]] link would open the wrong one).

8. Catalog note: one per work, named "Author - Short title.md" without the year (Catalog/<Subject>/Torzsok - Yogini and Goddess Possession.md, as in the Guide). Use the exact property block from Vault Guide → The catalog (Templates/Catalog Item.md has it too), keeping the value forms:
   - year and pages as numbers;
   - lists as lists, with plain personal names;
   - files: with full vault paths, like - "[[Library/Trika/Author - Short title (1990).pdf]]", followed by the Markdown index note, like - "[[Library/Trika/Short title (Author)/Short title (Author)]]";
   - status: empty, or review with the reason in the body.
   Body:
   - a "# Title" line, followed by the Open the PDF button (a dataviewjs block: await dv.view("Templates/Views/open-pdf"));
   - one sentence starting "**Checked against the file** on <date>:" that says where the details came from;
   - a "**Text layer**" line if it is a scan or has a broken text layer;
   - "See also" links to closely related catalog notes (same text in another translation, the same series, a commentary on it). Add a matching link back.

9. Related notes.
   - If the file fills a gap listed in Texts/Crosswalks/Incomplete Sets and Scholar Research Guide.md, update that note.
   - If the author has a page in Catalog/Scholars/, nothing to do: the page lists their works from the catalog. If they now have two or more works in the library and no page, add their name under "To profile" in Catalog/Scholars/Scholars.md.

10. Check your work:
   - every new files: link resolves;
   - every converted book has all its page markers: Obsidian finds a ^pgK block for every PDF page;
   - no note name is used twice in Library/;
   - each work shows in Catalog/<Subject>.md and in Catalog/Catalog.base;
   - the number of unresolved links has not gone up;
   - every new file name is ASCII.
   Also add up the new files' size against the Sync budget. The vault is about 8.9 GB and Obsidian Sync Plus allows 10 GB including version history. Warn me if the total gets within 0.5 GB of the limit.

11. Report back in a short table: file → catalog note, subject, pages, text (searchable/scan). Then list:
    - duplicates or same-work pairs waiting for my decision;
    - notes left in review, and why;
    - files that need OCR;
    - books converted, with notes and pages, and any left as PDFs;
    - the originals in Downloads that I can now delete.
    Clean up your scratch in .work as the house rules describe when you are done (never .work/plan or the backups).
````

**Afterwards:** delete the copied originals from Downloads when you are satisfied. Scans can go straight on to [[Make scans searchable (OCR)|Make scans searchable (OCR)]].
