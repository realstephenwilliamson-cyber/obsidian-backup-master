---
type: prompt
updated: 2026-10-13
phase: 7
---
# Reference linker

The script that linked 21,149 scripture, Zohar, Tantrāloka and Avot references inside the converted books on 13 Oct 2026 (phase 6, "B3"), and 21,365 in the texts added on 12–13 Oct (phase 7: Hobbes, the *Summa*, Chrysostom and Origen on John, the JANT). Kept here so the routine prompt [[Map new connections]] and later phases can reuse it instead of writing a new one. The report of that run is [[B3 linking report (13 Oct 2026)]].

## Files

- `b3core.js`: finds references in one line (book names and abbreviations, chapter:verse and chapter.verse, ranges, lists such as "Isa 7:14; 9:6" and "Gen 1:26, 27", chapter-only references for safe full names, "TĀ 3.67" / "T.Ā. III.67" / "Tantrāloka 4.122", "Zohar 2:148b" / "ZḤ 30c", "m. Avot 2:4"), and skips existing links, code, URLs, footnote markers, page markers, glued citation sigla ("Brd.Clr.Cant.27.4.6", "Midr. Rab. Gen. 36.8"), persons ("Daniel H. Ingalls") and page lists.
- `wrapper3.js` (phase 7; `build.py` uses it): `wrapper2.js` plus the options below, a Douay-Rheims index, and an escaped bracket before a reference printed in square brackets. With no options set it behaves as `wrapper2.js`.
- `wrapper2.js`: the phase 6 job body: indexes from the metadata cache (New Testament and Tanakh chapter notes, Torah verses in the parashah notes, the LXX, Zohar folio blocks, Tantrāloka verse notes, Pirkei Avot), the numbering rules, the dry-run report and the apply step.
- `versif-eng.json`: English → Hebrew verse numbers, converted from the Copenhagen Alliance versification specification (`eng.json`, CC BY-SA 4.0, https://github.com/Copenhagen-Alliance/versification-specification).
- `engmax.json`: the last verse of each chapter in English numbering (same source), used to tell English from Hebrew numbering.
- `build.py`: puts the pieces together into one job file for the runner.

## Running it

1. In a cloud workspace with these files: `python3 build.py <tag> <tag>.js` (for example `s70a-links-dry`).
2. Queue `<tag>.js` in `.work/queue/`. It is read-only and writes `.work/out/<tag>.json` (counts, numbering decided per book, undecided references with their lines, missing verses, 50 samples) and `.work/out/<tag>-proposals.json` (every link it would make, with its line).
3. Review the report; have a few hundred samples checked against their lines by agents that did not write the rules.
4. To apply, queue a job whose first line is `// APPLY` and whose body is `(async () => { window.B3APPLY = true; try { return await <the built job>; } finally { window.B3APPLY = false; } })()`. Each changed note is copied first to `window.B3BACKUP` (default `.work/backup-links-<date>/`). The result is `.work/out/<tag>-real.json`.
5. Scope: by default every note in `Library/` with `source_pdf` (the converted books). Set `window.B3SCOPE = ['Texts/Plato/', 'Texts/Hobbes/']` in the job before the built code to run over other folders.
6. Options in `wrapper3.js` (set them in the job before the built code and clear them afterwards: `try { window.B3SCOPE = [...]; window.B3VULG = [...]; return await <the built job>; } finally { window.B3SCOPE = null; window.B3VULG = null; }`):
   - `window.B3NTONLY = ['Texts/Fathers/']`: only New Testament references are linked there;
   - `window.B3VULG = ['Texts/Aquinas/']`: Old Testament and deuterocanonical references follow the Vulgate and link to the Douay-Rheims notes as written; New Testament chapters whose Vulgate numbers differ (Mark 9, 2 Cor 13, 3 John, Rev 12–13, Phil 1, Acts 19) are left undecided;
   - `window.B3OVERRIDE = {'<book path>': 'heb' | 'eng' | 'mixed'}`: sets a book's numbering instead of reading it from the book;
   - `window.B3SKIPNOTES = ['<note path>']`: notes to skip (the JANT's chapter-verse differences table, which made bogus shifts).

## Rules worth knowing before reuse

- **Numbering.** The Tanakh notes use Hebrew numbering and the Torah notes divide the Decalogue as Sefaria does (Exod 20:13 and Deut 5:17 hold four commandments). Books in `Library/Judaica` are taken as Hebrew-numbered; every other book's numbering is read from the book itself (a verse that exists in only one numbering, or a printed "[English 23:3]"). A reference that would move to another verse number is linked only where the book shows English numbering, or for the Decalogue where it is BHS; otherwise it is listed as undecided.
- **Left for a person:** Psalms, Samuel/Kings and Greek Daniel in Church Father translations; Psalm references near Augustine, Jerome, the Vulgate or the Septuagint; references marked Sept./Vulg.; a second numbering in brackets; Avot 5:20 on and chapter 6; Tantrāloka verses within three of a chapter's end (the KSTS count can differ there); books that cite the Tantrāloka by volume and page.
- **Skipped:** headings, index/contents/front-matter notes, lines mostly in Greek, Hebrew or Devanagari, foreign-language quotations, italics and block quotes; a list is held back whole when one member fails.
- **`OVERRIDE` and `EXCLUDE`** in `wrapper2.js` are decisions about particular books from the 13 Oct review. Check them before running over new material.
- **Phase 7 (13 Oct 2026):** the JANT uses both numberings, so it is left "mixed" (moved references undecided); a checker found 3 of 20 such references were already in Hebrew numbering. Plato was left out (its one "reference" was OCR for "ii"). The undecided references from both phases are listed in [[Bible references to decide later]]. The B3 leftovers were settled by 20 per-book rules (job `s77f-a3-apply`, data `.work/plan/p7/a3-items.json`), linking a reference only where its text occurs in the line as often as there are items for it.
- A second run over notes it has already linked finds a few more candidates, because some rules read the neighbouring text and the numbering evidence changes once references are links. Review those by hand rather than applying them blind.
