---
type: prompt
updated: 2026-10-09
---
# Make scans searchable (OCR)

**Use when:** catalog notes show `text: scan` (*Catalog.base* → *Scans without text*), or a PDF's text comes out as gibberish when you search or copy it.

Since 9 Oct 2026 most library books also have a Markdown copy (Vault Guide → Layout), and search uses that, so a text layer in the PDF matters mainly for copying from the PDF and for PDF++ links. A new scan is converted to Markdown when it is filed ([[Add new files from Downloads|Add new files from Downloads]]); the same OCR settings apply. The fixes below come from that conversion (7–9 Oct 2026).

**Before you start:**

- Close other AI tools.
- Use a Cowork task, which has a Linux workspace that can run OCR. Connect the vault folder and give it control of Obsidian, because files over about 25 MB have to be put in place from the Obsidian console.
- OCR is slow: about 2–3 seconds a page, so a 400-page book takes 15–20 minutes. Large batches run for hours; the task can keep going while you do other things.
- **Who runs it, model, size:** an AI session; Sonnet is enough, the work is scripted ([[OCR scripts]]). S in usage; the hours go on the OCR itself.

````text
Make the scanned PDFs in my Obsidian vault (C:\Vaults\Obsidian Vault) searchable by adding an OCR text layer, without changing how the pages look.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md (The catalog; Adding things → step 6 Scans)
- AI/Prompts/Scripts/OCR scripts.md (the tested scripts from the 5 Oct 2026 run; reuse them)
Confirm with me that no other AI tool is working on the vault.

1. Find the work.
   - Every catalog note with text: scan, plus any PDF I name.
   - For each file, extract text from about 12 sampled pages and count characters per page; also detect Devanagari, Hebrew and IAST characters.
   - Classify each file:
     (a) no text layer → OCR in "skip" mode (ocrmypdf --skip-text);
     (b) old OCR that dropped diacritics or is garbled → "redo" (--redo-ocr);
     (c) born-digital text in a legacy or unmapped font that extracts as gibberish → "overlay": render each page, OCR it, and lay an invisible text layer over the unchanged vector page (overlay.py);
     (d) JPEG 2000 page images → overlay too, because ocrmypdf re-encodes them much larger;
     (e) pages stored sideways or upside down → fix the page rotation first. Check with Tesseract OSD on two or three pages and look at a rendered page yourself.
   Show me the list with page counts and estimated hours before starting.

2. Set up in your Linux workspace: ocrmypdf with Tesseract 5 and the language models Latin, san, eng, heb and osd, plus pikepdf and poppler-utils. Packages often install the Latin model as tessdata/script/Latin.traineddata; copy or link it to tessdata/Latin.traineddata so that "-l Latin" works, and check with tesseract --list-langs.

3. Languages.
   - Indology (Trika, Hinduism, Sanskrit-Study): "Latin" (the script model keeps IAST diacritics), plus "+san" if sample pages contain Devanagari (more than about 0.5% of characters). If only some pages have Devanagari, OCR those pages with Latin+san and the rest with Latin alone: Latin+san turns italic English into Devanagari digits.
   - Judaica: eng, plus +heb if there is Hebrew.
   - Everything else: eng for English; Latin for books in other Latin-script languages (French, German, Latin), whose accents eng would drop. The catalog's language property tells you which.
   - Greek: eng+grc (install the grc model, Ancient Greek; used for Parmenides in the Markdown conversion).
   - Never use plain eng for Indology: it drops diacritics.

4. Run ocrmypdf --output-type pdf --jobs <cores> -l <langs> with the mode flag.
   - Yellowed or grey scans inside a white margin (Google Books scans) can come out with no text at all: add --tesseract-thresholding sauvola.
   - Typescripts and dense pages where whole lines or the first letters of lines are missing: try --tesseract-pagesegmode 6 on a few pages and keep it if it reads more real words (not for two-column pages).
   Then run fixmap.py on every output. It corrects the Latin model's look-alike letters in the invisible text only: ı→i, ş→ṣ, ņ→ṇ, ț/ţ→ṭ, ļ→ḷ, ř→ṛ (and their capitals). In Indology books it may also apply the word rules that worked in the Markdown conversion (`AI/Prompts/Scripts/Library conversion/`: `afix.py` and the converter's `postfix`):
   - ä or å → ā (the Latin model reads ā that way), except in German words (Universität, Bäumer: check a German word list) and in books that print Vedic accents (Lanman, Whitney, Macdonell), where å can stand for an accented vowel; a typescript's "anå", "shoulä" are "and", "should";
   - rh, ħ or ń → ṁ, but only inside words that already carry other IAST letters;
   - ñň or ňñ → ñ, jň → jñ, ň before c or j → ñ.

5. Check every output before it goes near the vault:
   - same page count;
   - text on the sampled pages;
   - Latin-script text should be real words. For English prose, about 40% of the words should be common function words; under 15% usually means sideways pages or the wrong model;
   - look at one rendered page.
   Any file that fails gets looked at, not applied.

6. Apply each output.
   - First copy the original to .trash/ocr-originals-<YYYY-MM-DD>/<same vault path> (only if no copy is there yet).
   - Then write the new file in place, but only if the vault file is still exactly the size you OCR'd (and, for a direct write, has the same modification time).
   - Files up to about 25 MB can be written directly. Bigger ones go as parts to .work/ocr/<id>/ with a manifest.json; ocr-apply.js joins them in the Obsidian console, checks the MD5 and the original's size, and makes the backup.

7. Catalog notes (by script, dry run first):
   - set text: searchable once every PDF of the note has text;
   - add or replace one dated line in the body, for example:
     **Text layer** (<date>): OCR text added (Latin-script and Devanagari models, so diacritics and Devanagari come through); the page images are unchanged. The scan without text is in `.trash/ocr-originals-<date>`.
   - Use the matching wording for redo, overlay and rotation. For a note with several files, write one line for all of them when they had the same treatment, otherwise one "**Text layer of `<file>`**" line each.
   - Replace any older "**Text layer** (PDF audit, 1 Oct 2026): …" line rather than adding a second one.

8. Size: OCR'd files grow about 5% on average. Report the total growth, and warn me if the vault gets within 0.5 GB of the 10 GB Sync Plus limit.

9. Report:
   - files done, with pages and languages;
   - files skipped, and why;
   - the quality-check results;
   - growth in MB;
   - where the originals are. They stay in .trash until I empty it, so I can check a few files first.
   Then remind me that, once Sync is on, each OCR'd file uploads as a new version. Sync keeps old versions of attachments for two weeks, so the extra storage is temporary.
````

**Afterwards:** open two or three of the files, search for a word you know is on a page, and empty `.trash/ocr-originals-…` when satisfied. If you want PDFs searched from Omnisearch, keep Text Extractor on and PDF indexing on in Omnisearch's settings.

## Known issues from the 6 Oct 2026 spot-check

An independent check of 15 OCR'd books (3 pages each, page image beside the text) found these; a new run should deal with them. Those marked *(fixed in the Markdown copies)* were dealt with in the 7–9 Oct conversion; the PDFs' own text layers still have them.

- *(fixed in the Markdown copies)* **ṁ/ṃ never comes out:** Tesseract's Latin model writes `rh`, `ħ` or `ń` for the anusvāra (Dyczkowski vol. I: 206× "sarh", no "saṁ"), so *saṁsāra*, *saṁvit* are not findable. A conservative post-map (`rh`/`ħ` → `ṁ` only inside words that already carry other IAST letters), tested on one volume, would help.
- **Devanagari split at ि:** in the hOCR text layer (the default renderer) almost every Devanagari word with the i-vowel sign is split in two, so searching for it fails. The GlyphLessFont overlay is much better (25%). Re-rendering with `--pdf-renderer sandwich` or patching the i-mātrā glyph mapping fixes it.
- *(fixed in the Markdown copies)* **Latin+san on italics:** italic or bold Latin words can turn into Devanagari digit strings (*Bhaṭṭa* → "2108118"). Use `Latin` alone for books with little Devanagari.
- **No deskew:** about 11% of Husserl's pages and 7% of Singh's *Vijñāna Bhairava* are skewed and read as fragments; `--deskew` changes the page images, so ask first.
- **Overlays keep the old gibberish:** text extraction interleaves the old and new layers; search for single words works. Neutralising the old fonts' ToUnicode would leave only the OCR text.
- **`--redo-ocr` on a good ClearScan file** (Rastogi, *Introduction to the Tantrāloka*) doubled the English text; it did add searchable Devanagari footnotes, and the Tantrāloka index finds many more references in it. Check for good visible text before choosing redo.
- **Low-resolution and typescript scans:** the *Philosophies of Religion* excerpt and the 1956 *Mālinīvijayottara* typescript read poorly; re-OCR at 300 dpi with `eng` and `--deskew --clean`.
- *(grc used for Parmenides in the Markdown copies)* **Greek:** no Greek model was installed, so the Greek pages of Graham's *Early Greek Philosophy* are noise; install `grc` and rerun with `eng+grc`.

