---
type: prompt
updated: 2026-11-09
---
# Texts import (9 Nov 2026): 1 Enoch, Lumpkin's Books of Enoch, the Dead Sea Scrolls

The scripts that made `Texts/Pseudepigrapha/1 Enoch`, the library copy *The Books of Enoch (Lumpkin)* and `Texts/Qumran`, kept so a later session can rerun or extend them. They ran in the cloud workspace (Python 3, PyMuPDF) on copies of the files in Downloads; the notes went into the vault as JSON bundles through the runner (`create-from-bundles.tpl.js`: checks that no path or note name is taken, then `app.vault.create`, in batches of about 270 notes). Run Python with `-I` on downloaded files, from another folder.

| Script | What it does |
|---|---|
| `enoch_build.py <OEBPS> <out>` | Charles, *The Book of Enoch* (SPCK 1917; Project Gutenberg #77935 EPUB): chapters and verses from the HTML (chapter numerals, verse numbers, the parallel Ethiopic and Greek versions marked *E* / *Gg*, sub-verses *a*, *b*, verses printed out of order). Writes `verses.json`, `heads.json`, `report.json` (gaps, merges) |
| `enoch_notes.py <OEBPS> <out>` | The 108 chapter notes (`^C-V` per verse; an *Arrangement* callout where Charles prints verses out of numerical order), the index note with Charles's key to the brackets, Oesterley's introduction with its 22 footnotes, the *Pseudepigrapha* folder note |
| `lumpkin_build.py <epub dir> <out>` | Lumpkin, *The Books of Enoch* (Fifth Estate 2010), a calibre EPUB of the print edition: running heads and page numbers taken out, a page marker per page (printed page = EPUB anchor `pK` − 6), chapter labels made headings (OCR variants such as "35J" and "S" read in sequence; lettered chapters of 3 Enoch kept: 15B, 22B–C, 48A–D) |
| `lumpkin_notes.py <out>` | The 12 part notes, the index note and the catalog note |
| `dss_index.py <pdf> <out>` | García Martínez & Tigchelaar, *Study Edition* (Brill PDF, 1999): the edition's Index of Manuscripts (824 entries) and the English (odd) pages |
| `dss_parse.py <pdf> <out>` | Each manuscript: its header found on the English page (and on the Hebrew page for the edition and bibliography lines), the English cut into sections (*Col.*, *Frag.*) and numbered lines; biblical manuscripts' fragment–verse lists from both sides; running heads (lists of sigla) dropped; 1QM and 1Q33, printed under one heading, made one note |
| `dss_notes.py <out>` | 806 notes `Texts/Qumran/<Cave N>/DSS <siglum>.md` (aliases: the siglum and short name), a block per line: `^<col>-<line>` for a column (arabic: col. iii line 13 → `^3-13`), `^f<frag>-<line>` for a fragment, `^f<frag>c<col>-<line>` for a column of a fragment, `^t-<line>` for a single sheet with no heading (4Q175); the index note *Qumran* with the edition's key to the symbols |

**Known gaps.** 136 Qumran notes say *No English here*: mostly biblical manuscripts whose fragment lists the parser did not pick up (Psalms, Isaiah, Jeremiah …), accounts, cryptic and unclassified fragments, which the edition does not translate, and a few small texts whose header the parser missed (4Q387b, 4Q441, 4Q486 and others; the note gives the page). The Hebrew and Aramaic are not converted: PyMuPDF reads this PDF's right-to-left lines in scrambled order, and the edition's EPUB (2017) stores the letters reversed. In Lumpkin's EPUB the chapter labels 1 Enoch 85, 105, 106 and 2 Enoch 4, 24, 27 are missing and were not supplied.

**Links into these texts** are made by `jantlinks2.py` in `AI/Prompts/Scripts/Reference linker/JANT/` ([[JANT links README (7 Nov 2026)]]).
