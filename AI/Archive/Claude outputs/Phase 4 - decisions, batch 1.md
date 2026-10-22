---
type: report
date: 2026-10-07
---
# Phase 4 - decisions, batch 1

Answer in one line if you like, for example: `batch 1: recommended` (every ★), or name the items you want otherwise.

## A. Before I write anything to the vault

1. **One AI.** Please confirm that no other AI tool is working on the vault and that the phase 3 task has stopped.
2. **Computer control of Obsidian.** I will ask for it shortly (a prompt on the computer). I need it for the performance baseline (step 0) and to create the notes. Leave Obsidian open.

Nothing else from your own list is needed to start.

## B. The not-to-convert list (approval point 1)

From the prep in `.work/plan/phase-4-prep/` (690 PDF and DjVu files). Each file is in the vault and stays there; "not convert" means no Markdown copy.

### Proposed NOT to convert: 33 files ★ approve all

| Group | Files | Why |
|---|---|---|
| DjVu: *Kiss of the Yogini* (White); *The Being of the Phenomenon* (Merleau-Ponty) | 2 | no text layer, and Obsidian can't open DjVu. Converting needs a DjVu-to-PDF step and OCR first; say if you want that later |
| Dictionaries: *A Dictionary of Sanskrit Grammar* (463 pp), Apte's *Practical Sanskrit-English Dictionary* (1,184 pp), Macdonell's *Sanskrit-English Dictionary* (404 pp) | 3 | dense multi-column entries; as notes they would be a slow, garbled copy. Look words up in the PDF (and Monier-Williams is already data) |
| `Library/Sanskrit/24 A Vedic Reader for Students.pdf` | 1 | the same book as the born-digital *Macdonell - A Vedic Reader for Students (1992 reprint)*, which is converted instead |
| Practice sheets: Devanagari poster, Devanagari practice A4, Ruppel's Devanagari practice sheet | 3 | handwriting practice, no text to read |
| KSTS *Tantrāloka* vols I–XII | 12 | the root text and Jayaratha's Viveka are already in `Texts/Tantraloka`, repaired against these volumes in phase 2; the PDFs stay for page checks, and the verse-page map already opens them at the page |
| Ruppel extracts: `CIS_Chapter_0`, `_2a`, `_3`, `_4`, `Chapter_1_2…`, `CIS_Appendices` | 6 | pages of the *Cambridge Introduction to Sanskrit*, which is in the vault whole and will be converted whole |
| Bansat-Boudon, *Paramārthasāra* PDF | 1 | already converted (`Library/Trika/Paramarthasara (Bansat-Boudon)/`) |
| `Writing/_Originals/`: AI UOS paper, CyberLevi3, Gospel Differences, SKT 100 Exercise 3, Ruppel errata | 5 | your own originals, outside `Library` |

Fink, the Lombardo/Davis Gita, Olesen, Broo, Matt and Padoux's *Tantric Mantras* have no PDF in the vault, so there is nothing to skip for them. No music files were found.

### Your decision: 9 files

| # | File | Question | ★ Recommended |
|---|---|---|---|
| N1 | Berg (ed.), *The Zohar*, vols 1–23 (3,782 pp, 135 MB web capture) | The vault has Pritzker and Soncino in Markdown. Convert all, only the portions with no English Zohar note in the vault (the nine parashot marked "no English Zohar note" in the concordance in phase 3), or none | ★ only those portions, as one book folder; the rest stays PDF |
| N2–N4 | Ruppel's answer keys: `Chapter_1.pdf`, `Chapter_2_and_2a.pdf`, `Chapter_3.pdf` (1 page each) | convert, or leave | ★ convert (searchable, and ready for the Sanskrit study system you mentioned) |
| N5–N7 | Ruppel's reference sheets: Reference Grammar (14 pp), Sandhi Overview (3 pp), Vocabulary (10 pp) | convert, or leave as printable sheets | ★ convert all three, keeping the PDFs for printing. Where a page is a grid that does not survive as text (likely the sandhi chart), that page gets a line pointing to the PDF page instead of a garbled table |
| N8–N9 | Brunner, Oberhammer, Padoux, *Tāntrikābhidhānakośa* I and II (259 + 306 pp) | convert (searchable entries), or leave as reference PDFs | ★ convert: the entries are short essays in French and English, much more useful searchable |

Not checked in the prep, and checked as each batch runs instead: books that are mostly plates, plans or diagrams. Any book whose pages are mostly images is held out of its batch and listed for you.

## C. How the work is done, given your usage (★ approve)

You have about 27% of this week's usage left until Monday, and 74% of Fable's. The phase as written uses an agent per book to convert and a second agent per book to check: about 1,300 agent runs. That would take far more than the week's remainder. I propose the same checks at a fraction of the cost:

1. **Conversion by script, not by agent.** For a born-digital or OCR'd PDF, an agent would only run the extraction script and read its output; the script does the same work identically every time and uses no usage. One tested script per text route (PyMuPDF, the OCR layer, a fresh Tesseract pass). An agent is called in only for a book the script's own checks flag.
2. **Checks on every book, by script:** every `^pgK` present and in order; page count; each footnote reference has its note and the reverse; diacritics and Devanagari counted against the source page; running headers removed (repeated lines); `[illegible]` counted; no empty notes.
3. **Visual checks by agents, as you asked:** 3 random pages of every book read against the page image. One checking agent takes about 6 books (18 pages) rather than one book, and the checking agents run on **Fable**, so that work draws on Fable's allowance and the main allowance carries the lead. Same pages checked; far fewer agent start-ups.
4. **The pilot first,** with its usage measured, so I can tell you what a batch of 80 costs before going on.

## D. The cloud credit and the two GitHub repositories

I read `Texts/Cloud build reports.md`. Those repositories built texts from open sources (Sefaria, SBLGNT, Brenton, Monier-Williams, DCS) in Claude Code cloud sessions, and the results were imported into the vault.

- **For phase 4: not worth it.** A cloud session can only work on what is in a GitHub repository, and this phase's input is your PDFs, which are only on this computer. They would have to be pushed to GitHub with git from your computer (about 7.9 GB; GitHub refuses single files over 100 MB, and four are over; the repository would have to stay private, since most of the books are copyrighted). This task cannot do that for you: its GitHub access is refused.
- **Where the credit would pay: phase 7.** Plato's *Phaedrus*, Pirkei Avot and the complete *Leviathan* (downloads you approved on 6 Oct) are exactly the kind of job those repositories did. A Claude Code cloud session could build them in one of the repositories now, on the credit, without touching the vault; phase 7 then imports and links them. ★ If you want that, say so and I will write the prompt (short) for you to paste into a cloud session. It works only in GitHub, so it doesn't break the one-AI rule.

## E. The pilot (for information; change any)

1. Born-digital English: Bryan, *Jesus and Israel's Traditions of Judgement and Restoration* (CUP 2002), 296 pp.
2. Born-digital, IAST-heavy: Dyczkowski, *The Canon of the Śaivāgama and the Kubjikā Tantras* (SUNY 1988), 243 pp.
3. Dyczkowski, *Tantrāloka* translation, vol. 1 (514 pp, the OCR layer with the anusvāra fix; reused in phase 5).
4. Overlay stotra: *Bahurūpagarbha Stotra* (14 pp, GlyphLessFont layer only).
5. Judaica with Hebrew: a book with real Hebrew text (I'm checking which of *Daily Prayers*, *Basi Legani* or the Koren Talmud has Hebrew in its text layer; the Talmud's page layout may itself be a not-to-convert candidate).
6. Two-column journal article: the first article in the library the script finds laid out in two columns.
7. Heavy footnotes: Padoux, *Vāc* (SUNY 1990), 464 pp.
8. Redo book: Rastogi, *Introduction to the Tantrāloka* (job 158, text twice: one copy kept).

For each: 3 pages beside the page image, and the folder layout.
