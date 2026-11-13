---
type: prompt
updated: 2026-11-13
---
# Library conversion scripts

The tested scripts from phase 4 of the October 2026 plan (7–9 Oct 2026), which made the Markdown copies of the library's books. They are in the folder `AI/Prompts/Scripts/Library conversion/` (hidden in the file explorer, like the other non-note files). [[Add new files from Downloads|Add new files from Downloads]] uses them for each new book; the record of how they were built and what each option fixed is the progress doc "08 Phase 4 - progress" in the Claude project.

They were written for a Cowork task's Linux workspace with the vault folder staged at `/mnt/user-data/uploads/Obsidian Vault/` and the work in `/home/claude/p4/` (`jobs/`, `out/`, `cache/`). Copy them there, or change the paths at the top of each script.

## Setting up

- Python 3 with `pymupdf`, `numpy`, `pillow`, `pyyaml` and `wordfreq` (`pip install … --break-system-packages`).
- Tesseract 5 with the models `Latin`, `san`, `eng`, and `heb`, `grc` if needed. If the package puts the Latin model in `tessdata/script/`, link it to `tessdata/Latin.traineddata`.
- `en_words.txt` beside `conv.py`: the English word list, one word per line, lowercased, from `/usr/share/dict/american-english-large` and `british-english-large` (packages `wamerican-large`, `wbritish-large`). It is not stored here because of its size (1.7 MB).

## The scripts

| File | What it does |
|---|---|
| `classify.py` | Samples each PDF's pages (text per page, IAST, Devanagari, Hebrew, garbled fonts, scans) and proposes a route: the text layer (`pymupdf`), an OCR layer of glyphless text (`glyphless`), or fresh OCR (`ocr`), with languages |
| `mkjob.py` | Writes a job file for a book (title, authors, byline, folder and note names, catalog link) from its catalog note |
| `conv.py` | The converter: `python3 conv.py jobs/<job>.json` writes the index note and chapter notes to `out/` with a `_report.json`. Options are keys in the job file (below) |
| `glyphfix.py` | Used by `conv.py`: repairs text layers whose fonts have no Unicode map (Sanskrit transliteration fonts, TeX ligatures) by matching glyph shapes |
| `afix.py` | Used by `conv.py`: ä/å read for ā in OCR'd Indology text, word by word (German words kept, "anå" → "and") |
| `ocr_worker.py` | Fills the OCR cache for whole books in the background: `python3 ocr_worker.py queue.json 0 1` (worker 0 of 1); a queue item is `{pdf, langs, san_pages, psm, ocr_prep, reverse}` |
| `spreads.py` | For scans with two book pages on one PDF page: reads the printed page numbers in the corners and writes `<job>.spreads.json` |
| `bundle.py` | Packs converted books into JSON bundles (under 24 MB) plus `create-list.json` and `check-list.json` for the runner |
| `underdot.py` | (22 Oct 2026) For a text layer that draws the dot below a letter as a separate mark (PyMuPDF reads it as `\_`, as in Lutgendorf's *Hanuman's Tale*): puts the dot back on its letter in the converted notes. `python3 underdot.py <folder> [write]`; without `write` it only counts |

### Runner jobs (`runner/`)

They run inside Obsidian through the vault's runner (`.work/plan/phase-3-tools/runner.js`; jobs go in `.work/queue/`, results in `.work/out/`). A job is a dry run unless its first line is `// APPLY` (the runner sets `window.DRY`). Every job that changes notes backs them up first under `.work/backup-phase4-…/`.

| Job | What it does |
|---|---|
| `p4-replace.js` | Creates the notes of the bundles in `.work/p4/bundles/` listed in `.work/p4/create-list.json`; replaces a note only if it was made by this conversion (has `source_pdf` and `converted`) |
| `p4-check.js` | For each book in `check-list.json`: every page block `^pgK` registered by Obsidian; note count; unresolved links |
| `p4-catalog.js` | Adds the Markdown index note to the catalog note's `files:` and the *Open the PDF* button |
| `p4-links.js` | Makes the study plans' PDF page links open the Markdown page first, with the PDF beside it |
| `p4-dupnames.js` | Lists note names used twice in `Library/` |
| `p4-rename.js`, `p4-trash.js` | Renames (with Obsidian's link updates) and moves to `.trash`, from a list |
| `p4-afix-collect.js`, `p4-afix-apply.js.tpl` | The 9 Oct ä/å repair of notes already in the vault: collect the words, make the map with `afix.py`, apply |

Work in bundles of at most about 300 notes and wait a minute or two after an apply before the checks: larger applies froze Obsidian twice on 7 Oct while Omnisearch and Smart Connections indexed the new notes.

## Added 22 Oct 2026 (the PDF-only works: 21 books)

`conv.py` gained five options; the old behaviour is unchanged when they are absent. The 22 job files of that day are in `example jobs/2026-10-22/` and show each option in use.

| Option | What it fixes | Example job |
|---|---|---|
| `split_halves` | Scans with two book pages on one PDF page, read by fresh OCR: each half is read on its own, so the gutter does not garble the lines beside it | Graham |
| `ncols_landscape` | With `ncols`: apply the column split only to landscape pages (the two-page spreads), not to single pages in the same file | Graham |
| `baseline_sort` | Lines ordered by their baseline, not their top, so a raised note letter does not lift its line out of order (an apparatus of lettered notes) | Davila |
| `bidi_runs` | Lines that mix Hebrew and English (notes quoting Hebrew): Hebrew runs read right to left, English runs keep their order | Berman |
| `san_sort` | With `san_pages`: one-column verse pages keep their Devanagari and transliteration lines in page order | Olivelle, the *Durgā Saptaśatī* hymns |

Options that already existed, used in new ways that day:
- `ocr_ranges` with the Hebrew model on Hebrew pages (`heb`, or `heb+eng` on mixed pages), the rest from the text layer (Verman).
- `charmap` for a born-digital PDF whose font puts diacritics at its own letter codes (Å for ā, ç for ī, æ for ṇ …), read off the PDF's pages (*Seeking Mahadevi*).
- `force_bad_fonts` for a book whose TimesNewRoman fonts lack a Unicode map (*Woman and Goddess in Hinduism*). It made Lutgendorf worse; `underdot.py` fixed that book instead.

**Lesson:** choose each book's route and languages after looking at a few page images, not only from `classify.py`'s text-layer statistics. Olivelle's edition prints the Upanisads in Devanagari, and the first route (Latin only) would have lost it. The record is the AI log, 22 Oct 2026 (afternoon), and the project doc *PDF-only works - record (22 Oct 2026)*.

## Job options used most

`route` (`pymupdf` or `ocr`); `langs` (`Latin`, `eng`, `Latin+san` …); `san_pages` (a second OCR with `+san` only on pages that need it); `psm` (`3`, `6` or `best`); `ocr_prep: 'norm-sauvola'` (yellowed scans); `merge_ocr` (keep a text layer, replace its junk words from a fresh OCR); `latin_fix` (English lines that the `san` model spoiled read again with `eng`); `fixmap`, `anusvara`, `charmap` (letter repairs); `accents` (a book with Vedic accents: no ä/å repair); `use_toc`, `toc`, `big_heads`, `contents_heads`, `fuzzy_heads` (where the chapters come from); `pnum_override`, `labels` (printed page numbers); `ncols`, `gutter_bands`, `columns`, `col_segments` (column layouts); `fn_runin`, `fn_max_size` (footnotes); `callout` (a warning at the top of each note); `single` (an article in one note). The three files in `example jobs/` show a plain OCR job, a layer-and-OCR merge with a callout, and a two-column OCR job; `example jobs/2026-10-22/` has the 22 jobs of 22 Oct 2026.

## Added 26 Oct 2026

- `Soft hyphens/` ([[Soft hyphens]]): born-digital PDFs that store every hyphen as U+00AD, which the converter drops; the scan, the classifier and the page-by-page patch used for Sen Sharma and Brown.
- `Page labels/` ([[Page labels]]): read-only scans of the index labels and of the `[PDF K]` markers inside numbered runs, with their results of 26 Oct (not applied).
- `example jobs/2026-10-26/`: the four re-split jobs of 26 Oct (second session).
- `example jobs/2026-10-29/`: the two Levinas jobs of 29 Oct (*Totality and Infinity*, 19 notes; *The Levinas Reader*, 24 notes; `legacy_fonts: false` for the Reader).

## Added 13 Nov 2026 (Pelikan, *The Christian Tradition*, vol. 1)

`conv.py` gained six options for a fresh OCR of a book that prints its references in a left margin column and has Greek words in English pages; without them it behaves as before. The job, the post-fix script and the OCR prefill are in `example jobs/2026-11-13/`.

| Option | What it does |
|---|---|
| `grc_words` | The page read again with the given languages (`eng+grc`); a Greek word from that reading replaces the English reading's non-word in the same place when it is bracketed, or has five or more Greek letters at confidence 50 or more, or stands in a line with such a word. `grc_pages` [first, last] limits it (covers and endpapers gave junk) |
| `margin_col` | A line read across the margin and the text is split; margin lines go first on the page, as separate paragraphs, and are never taken for running heads; the text's edges are measured without them. Old-style 1 read as i, t, I or l before a book abbreviation or a colon is made 1 |
| `no_sup` | Figures are never raised as note calls (old-style 0, 1, 2 are x-high) |
| `no_headlike` | No headings guessed from type size (OCR sizes are word heights, so lines with many ascenders came out as headings); headings come from `toc` |
| `psm_ranges` | [first, last, psm] for some pages, or [first, last, psm, "halves"] to read each half of the page on its own (a two-column table: the biblical index) |
| `entry_ranges` | [first, last, ncols(, indent)]: list pages (abbreviations, bibliography, indexes): a line at its column's edge, measured near the line so a skewed scan does not count, starts an entry; `indent` (default 0.6 body sizes) widens the allowance where sub-entries are indented |

`prefill.py pdf langs first last` fills the OCR cache ahead of `conv.py` (two in parallel: one per language set). `postfix_ct1.py` holds the vol. 1 corrections made after conversion (two section headings, covers and endpapers, three misreads of t and i as #).

Vols. 2 and 3 of the same set followed the same afternoon: `The Christian Tradition 2 (Pelikan).json`, `The Christian Tradition 3 (Pelikan).json` and `postfix_ct23.py` in the same folder (section headings, the spines, a Greek title, and margin abbreviations whose italic letters the OCR read as # or ::, read off the page images). `prefill.py` makes the PDF's path absolute itself: the OCR cache is keyed on the path, so a relative path there and an absolute one in the job meant every page was read again.
