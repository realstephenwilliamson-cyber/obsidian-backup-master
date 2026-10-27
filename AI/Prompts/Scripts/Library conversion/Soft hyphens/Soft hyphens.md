---
type: prompt
updated: 2026-10-26
---
# Soft hyphens

Scripts for one fault of born-digital PDFs, written on 26 Oct 2026 (third session of the corrections week) and kept under the house rule *Keep what a later session will use*. Some e-texts (SUNY Press, for example) store **every** hyphen as a soft hyphen (U+00AD), and they also keep the print's leftover line-break hyphens inside reflowed lines. The vault's converter drops U+00AD, so real hyphens are lost ("selfmanifestation" for "self-manifestation"). Obsidian's pdf.js strips U+00AD, so it cannot see the fault; PyMuPDF can.

## Files

| file | what it does |
|---|---|
| `softhyph-scan.js` | runner job (pf269, read-only): samples up to 14 pages of every born-digital book with pdf.js and counts hyphens, soft hyphens, en and em dashes. Because pdf.js hides U+00AD, the useful signal is **no ASCII hyphens at all** in a sizeable sample; its result of 26 Oct is `.work/edits/pagelabels-2026-10-26/softhyph-scan-2026-10-26.json`. |
| `shyfix.py` | first-pass classifier (wordfreq + the book's own spellings) for each split point: H keep a hyphen, J join. Superseded on 26 Oct by readers' decisions, but useful as a first sort. Needs `pip install pymupdf wordfreq`. |
| `shypatch.py` | the patch: for each U+00AD token on PDF page K it puts the decided form into the note's page block (`^pgK` to the next marker), only where the counts agree and the page prints the current form nowhere else; everything else is listed. Writes `{path: {oldText, newText}}` for a `textpatch` job (`.work/edits/textpatch.tpl.js`). |
| `sen_decisions.json`, `brown_decisions.json` | the decisions used on 26 Oct: `{"a|b": "H"/"J"/"S"}` (S = a space). |
| `decisions-report.txt` | the readers' report: counts, the joins, the unsure cases and how the book's own habit decided them. |

## Done

- 26 Oct 2026: Sen Sharma, *The Philosophy of Sadhana* (6 notes) and Brown, *The Triumph of the Goddess* (11 notes), pf279 dry, pf280 apply. 11 Sen cases and one Brown case were left as they were and listed in the session record.
- The scan of 203 born-digital books found no other book with zero hyphens in its sample (the next lowest have 2–19 hyphens in 16,000–48,000 characters, which a text with few compounds can have). A book converted later from a born-digital PDF should be checked the same way.
