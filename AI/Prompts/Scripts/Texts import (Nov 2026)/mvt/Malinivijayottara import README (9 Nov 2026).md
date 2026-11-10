---
type: prompt
updated: 2026-11-09
---
# Mālinīvijayottara import (9 Nov 2026): Dyczkowski's chapters 1–8

The scripts that made `Texts/Malinivijayottara` (473 notes: 456 verse notes, 8 chapter notes, 6 chapter introductions, the general introduction, the index, and the catalog note in `Catalog/Trika`). They ran in the cloud workspace (Python 3, PyMuPDF, Tesseract with the `san` model from tessdata_best) on copies of the PDFs now in `Library/Trika`; the notes went in as two JSON bundles through the runner (jobs pf811 dry, pf812 apply).

Source files, as the scripts name them: `f1` chapters 1–5 article PDF, `f2` chapter 6 article PDF, `f3` chapters 7–8 article PDF, `f4` *Mālinī* January–April 2024 (chapter 6 part 2, PDF pp. 28–35), `f5` *Mālinī* July–September 2022 (chapter 2 introduction and verses 1–24, PDF pp. 23–36). KSTS text: Muktabodha M00160 (`Texts/MUKTABODHA-LIBRARY-IAST_2026_02_20`), copied to `ref/mk_iast.txt`.

| Script | What it does |
|---|---|
| `extract.py f1 …` | Decodes the text layer into `work/<f>.lines.json`. The ScaGoudy fonts are stored as glyph ids (code − 29 for ASCII, a table for the diacritics, different for roman and italic) or as plain Balaram-encoded text; the mode is decided per span, then per line, then per page. Tiny digit spans in any font are footnote calls. Letter-spaced lines are rebuilt from glyph positions. The Devanagari fonts (KrutiDev010, Krishna) are not decoded |
| `order.py` | Reading order of the two-column pages; joins pieces of one printed line; footer zone |
| `mk.py` | The KSTS e-text into chapters, verses and half-lines (`work/mk.json`) |
| `parse.py` | Footnote zone and footnotes, calls put into their lines, each line classed as Devanagari, Sanskrit transliteration (by 5-gram match with the KSTS chapter, or by position after Devanagari lines), English or heading |
| `align.py`, `assemble.py` | Cuts the transliteration into verses by aligning it with the KSTS half-lines; lifts out lines not in the KSTS text; OCRs the printed Devanagari lines and uses the reading to choose between the transliteration and the KSTS text where they differ; groups the English into translation units by their verse references (infers a missing reference from position); headings; splits the chapter introduction from the text at the first Devanagari line |
| `deva.py` | IAST to Devanagari, words joined as in a Devanagari print |
| `render.py`, `prose.py` | Verse notes; running prose (introductions) |
| `ch7.py` | Chapter 7, read from the page images by hand (the print is scanned pages, English only) |
| `build_all.py`, `finish.py` | All chapters, chapter notes, introductions, index, catalog note, checks, bundles. Chapter page ranges are `CH` in `build_all.py` |
| `chk.py 1,2,…` | Diagnostics per chapter |

**Known limits.** The Devanagari is generated, not the print's own. Footnote calls whose note was not found are left as `[n. N]` (2.21, 2.23, 2.29, 2.33, 2.35, 2.40, 4.6–8, 4.40–41, 6.2–3, 8.17–19, 8.83, 8.93). References were supplied at 4.9, 5.30 (no reference in the print) and 8.90 (the print has 91–92). In 4.31–32 the print's transliteration lacks some words. Lists and tables in the introductions are rough. No April–June 2024 issue was at hand; chapter 7's heading says "continued from Previous Issue".
