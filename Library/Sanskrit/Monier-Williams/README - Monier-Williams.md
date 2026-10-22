---
type: "data"
work: "Monier-Williams Sanskrit-English Dictionary (1899)"
license: "CC BY-NC-SA 3.0 (data header); repository LICENSE CC BY-SA 4.0"
source: "https://github.com/sanskrit-lexicon/csl-orig/blob/55e8addbd96e8d9001b8789026b026763f4049c1/v02/mw/mw.txt"
aliases:
  - "Monier-Williams"
  - "MW dictionary"
---
# Monier-Williams Sanskrit-English Dictionary (data)

Monier Monier-Williams, *A Sanskrit-English Dictionary*, new edition (Oxford: Clarendon Press, 1899), as digitized by the Cologne Digital Sanskrit Dictionaries. No notes are generated from it; the whole dictionary is one tab-separated file beside this note.

## Source

- [sanskrit-lexicon/csl-orig](https://github.com/sanskrit-lexicon/csl-orig), file `v02/mw/mw.txt`, commit `55e8addbd96e8d9001b8789026b026763f4049c1`.
- 286525 entries (one row per Cologne record; nominal entries are split into the sub-records the digitization uses).

## License

The data's own header (`v02/mw/mwheader.xml`) says:

> Copyright © 2014 The Sanskrit Library and Thomas Malten
> All rights reserved other than those granted under the Creative Commons Attribution Non-Commercial Share Alike license available in full at //creativecommons.org/licenses/by-nc-sa/3.0/legalcode, and summarized at //creativecommons.org/licenses/by-nc-sa/3.0/. Permission is granted to build upon this work non-commercially, as long as credit is explicitly acknowledged exactly as described herein, and derivative work is distributed under the same license.

The repository's LICENSE file gives CC BY-SA 4.0. This file follows the stricter terms above (Attribution–NonCommercial–ShareAlike 3.0): it is for non-commercial use, and anything derived from it must carry this credit and the same license.

Credits, as listed in the header: Monier Monier-Williams, with Ernst Leumann and Carl Cappeller, *A Sanskrit-English Dictionary* (Oxford, The Clarendon Press, 1899); first digital edition by Thomas Malten (Köln Universität, 1997); XML edition (30 June 2014) by Jim Funderburk, Thomas Malten and Peter M. Scharf, The Sanskrit Library (Providence, RI) and the Institut für Südasien- und Südostasienstudien (Köln); supported by the United States National Science Foundation, the United States National Endowment for the Humanities and the Deutsche Forschungsgemeinschaft. Further contributors:

- supplement integration: Sharon Ben-Dor
- supplement integration, accent revision, homophony regularization, hierarchical display revision, linking of Sanskrit words within entries to headwords: Pawan Goyal
- markup analysis: Malcolm D. Hyman
- tagging of the list of works and authors, and association of abbreviations actually used with those in the list: Susan J. Moore
- lexical categorization of nominals, and feminine stem analysis: Ramaswamy Chandrashekar
- Greek data entry: Wendy Teo
- Error correction, parenthetical headword hierarchical placement: Dr. Sampada Savardekar Thomas
- Insertion of Arabic text: Jason Lyle Reeder
- edited by: Peter M. Scharf

## Format

`monier-williams.tsv`: UTF-8, tab-separated, one header row, LF line endings. Columns:

| Column | Content |
|---|---|
| id | Cologne record number (`L`), e.g. 4 or 4.1 for a sub-record |
| page_col | page and column of the 1899 print, e.g. 1,1 |
| headword | headword in IAST (from SLP1 `k1`) |
| headword_print | headword as printed, with compound divisions (from `k2`), in IAST |
| homonym | homonym number, where the dictionary has one |
| line | Monier-Williams' “line” of the headword (1–4; A/B for continuations) |
| text | the entry, markup removed; Sanskrit in IAST |

All text is NFC-normalized.

Conversion details:

- Sanskrit (SLP1) becomes IAST; Vedic accents become combining marks: udātta as acute (á), anudātta as grave (à), svarita as circumflex (â).
- Characters the dictionary uses inside Sanskrit (— for compound joins, ˚ for an abbreviated repetition, √ for a root) are kept as they are.
- Where the digitization records a correction (its chg markup), only the corrected reading is kept.
- The srs mark inside Sanskrit words is dropped (37041 times); its printed form is not documented in the data.
- Tags such as ab (abbreviation), ls (literary source) and lex (grammatical category) are removed and their text kept; info and page-break tags are removed.
