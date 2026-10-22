---
type: report
date: 2026-10-07
---
# Phase 4 - pilot (decisions, batch 2)

The 8 pilot books are converted in the cloud workspace, not yet in the vault. **Phase 4 - pilot review (8 books).html** shows 3 pages of each beside the page image, and the folder of each book. A separate checking agent (Fable) read all 24 pages against the images; I fixed what it found that a script can fix (a doubled text layer in Rastogi, soft hyphens, an English line overwritten by Devanagari OCR, Hebrew vowel-point order, more anusvāra forms) and rebuilt the books.

Answer `batch 2: recommended`, or name the items you want otherwise.

## Performance baseline (step 0, measured in Obsidian at 12:33)

| Measure | Now |
|---|---|
| Omnisearch indexes the PDFs? | **Yes** (*PDF indexing* on, through Text Extractor). Its index cache is off, so it rebuilds at every start-up. |
| Omnisearch search | 30–175 ms; PDFs fill 13–16 of the top 20 results for common words |
| Obsidian's own search, "consciousness" / "spanda" | 7.5 s / 3.9 s until the results stop changing (it does not read PDFs) |
| Open Library.base | 1.8 s |
| Open Home | 3.8 s first time, 1.5 s again |

What this already shows: the PDFs slow Omnisearch only at start-up and crowd its results; they don't touch Obsidian's own search. The converted text **will** slow Obsidian's own search, because it searches every note. I'll measure after the pilot is in the vault and after every few batches. If it lags, the settings to weigh are in section F.

## The pilot: what came out

| Book | Route | Result |
|---|---|---|
| Bryan, *Jesus and Israel's Traditions* | born-digital | **Good.** Chapters from the bookmarks, headings, 570 linked footnotes, printed page numbers from the PDF's own page labels, Greek read by OCR where the font had no character map |
| Bisschop, *Invoking the Powers that Be* (two columns) | born-digital | **Good** body and IAST; the end-notes list at the back is untidy |
| Basi LeGani (Hebrew and English) | born-digital | **Usable.** Text complete, footnotes linked. Hebrew words are in order inside each phrase, but the first words of some mixed lines are displaced, and the side-by-side layout becomes Hebrew phrases first, then the English |
| Dyczkowski, *Tantrāloka* vol. I | the existing OCR layer, Devanagari read again with Tesseract `san` | **English about 90–95% clean.** The Devanagari verses are now real Devanagari (they were glyph junk). Sanskrit in roman letters about 50% exact. Footnote references don't survive |
| *Bahurūpagarbha Stotra* | the GlyphLessFont layer only | **Poor for the Sanskrit** (about 55–60% of words exact, `Siva`, `namah`), English fine. That layer is from 5 Oct, with the Latin model's limits |
| Dyczkowski, *Canon of the Śaivāgama* | **fresh OCR** (Latin) | English readable; IAST 40–65% exact; superscripts come out as `!`, `®` |
| Padoux, *Vāc* | **fresh OCR** (Latin) | English readable; IAST about 50–85% |
| Rastogi, *Introduction to the Tantrāloka* | ClearScan layer (one copy) + OCR of the Devanagari footnotes | English good; footnotes linked (392); Devanagari footnotes partly garbled |

**A finding that changes the plan:** the inventory counted Padoux's *Vāc* and Dyczkowski's *Canon* as "born-digital text". They are old scans whose text layer turns diacritics into other letters (`kuriçlalinl` for *kuṇḍalinī*, `pifha` for *pīṭha*). Many Indology books listed as born-digital are probably the same. So more books than planned need fresh OCR, and the batches will classify every file by looking at its pages, not by the inventory.

## Decisions

| # | Question | ★ Recommended |
|---|---|---|
| P1 | **Format.** Folder `Library/<Subject>/<Short title (Author)>/`; an index note (`type: book`, contents with page ranges); chapter notes named `<short title> NN - <chapter>` with *previous · contents · next* at the top; every note's properties: `type`, `work` (the catalog note), `book`, `order`, `source_pdf` (plain text, so the PDF keeps a single link, from its catalog note), `pages`, `pdf_pages`, `text_source`, `converted`; `*[p. N]* ^pgK` at the start of every PDF page; footnotes as `[^n]` where the reference was found | ★ approve |
| P2 | **Sanskrit in OCR'd scans.** Tesseract's Latin model cannot write ṃ ḥ ṛ ḍ ṅ ṭ ṇ and drops Ś before capitals; about half of the IAST words in old Indology scans come out exactly right. (a) Accept: the English and most Sanskrit become searchable (Omnisearch ignores diacritics), the PDF stays for exact reading, and each note's `text_source` says "OCR". (b) Later, test a dictionary pass that restores diacritics only where an OCR word matches exactly one form in the vault's Monier-Williams or DCS data, marked as restored, on one book first, for your approval. (c) Leave those books unconverted until a better OCR model is available | ★ (a) now, and (b) as a later test, asked separately |
| P3 | **Notes in OCR'd and end-note books.** References come out as plain numbers or OCR marks, so the notes stay as visible numbered paragraphs where they are printed (never as hidden footnote definitions) | ★ accept |
| P4 | **Short works without chapters** (articles, stotras, up to about 40 pages): one note holding the text, instead of an index note plus one text note | ★ one note |
| P5 | **Page numbers not printed** (chapter openings): taken from the neighbouring pages when the pages before and after agree; otherwise the PDF page number, as the plan says | ★ approve |
| P6 | **Books without bookmarks** are split into 40-page parts, as the plan says. For Dyczkowski's *Tantrāloka* volumes, which phase 5 reuses, I'd also split at the start of each chapter (āhnika) where it can be read on the page | ★ approve |
| P7 | **Put the 8 pilot books in the vault now,** so you can look at them in Obsidian (computer and, later, phone) and I can measure the search speed with them. They are new folders only; if you want the format changed, they go to `.trash` and are made again | ★ yes |

## Usage and time

- I can't see your usage meter. Please tell me the % now (it was 73% at the start), so I can estimate what the 640 books will take.
- **OCR is the slow part, not the usage.** This workspace has 2 processors and reads about 1,800 pages an hour; born-digital books take seconds. When the batches are classified I'll give you the OCR hours. Long OCR runs in the background while the agents check finished books.

## F. Settings to weigh later (yours to change; nothing to do yet)

- **Omnisearch → PDF indexing:** off once a batch is in Markdown (the text is then in the notes, and PDFs stop crowding the results).
- **Omnisearch → cache:** on, so it doesn't rebuild the whole index at every start.
- **Settings → Files and links → Excluded files:** a pattern for PDFs keeps them out of search, the graph and the quick switcher; links still open them.
- **Smart Connections:** exclude the PDFs, and the converted books if you don't want them in its suggestions.
