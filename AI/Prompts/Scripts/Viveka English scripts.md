---
type: prompt
updated: 2026-10-23
---
# Viveka English scripts

The scripts that, on 22 Oct 2026, made Dyczkowski's English of Jayaratha's *Viveka* readable from every Tantrāloka verse note. The English stays where it is, in the library copy of his eleven volumes (`Library/Trika/Tantraloka (Dyczkowski)/`); each of his verse units there has two headings (`### TĀ 1.1` before the verse, `#### Viveka on 1.1` before the commentary), and each verse note's *Viveka* section opens with a folded `[!viveka]` box that embeds those sections. [[Tantraloka page]] shows the same text beside the Sanskrit. The record is the AI log, 22 Oct 2026 (evening).

They are in `AI/Prompts/Scripts/Viveka English/`. They were written for a cloud workspace with the work in `/home/claude/viv/`: `lib/` held copies of the 123 library notes as they were before the headings; the phase 5 data are read from the vault's `.work/plan/phase-5-work/` (`units-matched.json`, `12oct/units-final.json`, `12oct/verses-final.json`, and `dz_units2.py`, which the scripts load). Copy them there, or change the paths at the top of each script.

## The scripts

| File | What it does |
|---|---|
| `seg.py` | Splits each library note into paragraphs with their kind (verse, prose, footnote, page marker) and finds each phase 5 unit's translation in them (`found.json`) |
| `seg2.py` | Each unit's place: the verse block, the translation, and the commentary that runs to the next unit's verse block (`units-pos.json`) |
| `gen.py` | The first pass: the headings (`lib-inserts.json`, offsets checked against the text) and the verse-note boxes (`verse-callouts.json`). Where a verse has no commentary of its own, the box shows the next unit's and says the commentary is given together |
| `gen2.py` | The second pass, which replaced the first: units that are not Tantrāloka verses (quotations Jayaratha gives with their own verse numbers, the labels of a figure, numbers the OCR garbled) are folded back into the commentary of the verse before them, but only inside a chapter (at a chapter's start or end they may be Jayaratha's own verses or an appendix); headings in a fixed order; a commentary that runs on over later notes gets a "(continued)" heading in each |
| `gen3.py` | The third pass, which is what the vault now has: `gen2.py` plus two corrections found by the page check. Where a unit's verse block was not found right before its translation (a translation in several paragraphs, or footnotes between verse and translation), the heading goes before the Devanagari found further back; a verse block broken by a page's footnotes is followed back over them; the book's subheading just before a verse block goes with that verse. A section that holds only a subheading is not counted as commentary. The box line for a verse with no commentary of its own reads "No commentary follows this verse directly; shown here is the next, after TĀ …" |
| `clean.py` | The letter clean-up (run as `python3 clean.py <in> <out>` on the folders of notes) of the library copy: stand-in letters (ã ă → ā, ŝ → ś, ș → ṣ, ñ before k/g → ṅ, ù → ṅ/ṁ/ñ by position, ň → ṁ, \$ → Ś, a few ž), ṁ read as "rh"/"rn" (after a vowel and before a consonant, or at the end of a Sanskrit word; never in an English word), and the TM ® ™ ° the OCR left for footnote numbers. Headings, page markers, links and code are left alone. It prints counts and keeps samples |
| `proof.py` | The proofreading pass of 22 Oct 2026 (night): restores the Ś the OCR dropped from Śiva, Śakti, Śaiva and their compounds ("Lord iva", "Kula (akti)", "Kashmiri aiva authors"), in English lines only, never in a Sanskrit line, where *iva* is the particle "like"; lowercase ś in a gloss after a lowercase word ("energies (śakti)"), as printed. Writes the patch for `viveka-patch.js` and a list of the changes with their pages (`python3 proof.py <lib-in> <lib-out> <patch.json> <samples.json>`) |
| `viveka-headings.js.tpl` | Runner job of the first pass (`__DRY__`, `__TAG__`): checks every offset, backs up, inserts the headings, adds the boxes |
| `viveka-patch.js` | Runner job of the second and third passes: applies a patch (`lib-patch.json`: per note the length and hash of the text it was made from, the edits, and the length and hash after) only to a note that is exactly that text, checks the result, backs up first; replaces, adds or takes out the boxes (`callouts.json`). Without the first line `// APPLY` it is a dry run |
| `viveka-check.js` | Read-only runner job: every embed in the boxes reaches a heading that exists; the vault's unresolved-link count |
| `cands.py` | The second proofreading pass (23 Oct 2026): finds the candidates (words that lost their Ś; ṁ read as "ri"/"r"; bracketed terms whose diacritic spelling is far commoner in the library copy) in the 123 chapter notes, and in the other 43 notes after `clean.py` and `proof.py` |
| `crops.py` | Places each candidate on its PDF page through the OCR text layer (the word and its neighbours), crops the line, boxes the word, and stacks the strips into numbered sheets |
| `reading-brief.txt` | The brief the reading agents followed: transcribe the boxed word exactly as printed, without being shown the vault's reading or the fix |
| `build_patch.py` | Builds the patch from the readings: Ś and bracketed diacritics only where the reading is confident and the placement checks; ṁ by rule; whole-line hunks with length and hash before and after |
| `proof2-patch.js` | Runner job of the second pass (as `viveka-patch.js`, without the boxes) |
| `dots.py` | The dots-below pass (23 Oct 2026, evening): candidates for ṛ (an r between consonants) and ḥ (a final h after a vowel), with ṇ ḍ ṭ ṣ from spellings in the copy, by tier (Sanskrit line; English line with other marks; unmarked word in an English line; matched spelling only) |
| `build_dots.py` | Scores the page-read sample per tier and builds the patch for the tiers given (applied: the three rule tiers) |

## Checks used

- Every embed resolves, and the unresolved-link count is unchanged (13/27) — `viveka-check.js` after each pass.
- The letter fixes: 40 changes drawn at random and read on the page images; the 33 that could be found on the page were all right, one with a capital Ś where the print has ś after a line-break hyphen.
- The sections: 50 verses drawn at random, each section's start, end and first 100 words read against the page images by agents that had not seen the work. After the second pass: start right in 48, end right in 43 (7 ran on into the next verse — fixed by the third pass and rechecked); 1.2% of the words read differ from the print.

## What is still imperfect

- Other OCR slips stay: dots below that the 23 Oct rules did not cover (ṇ ḍ ṭ ṣ found only by spellings in the copy, where the print has typos of its own; ṛ before y or v; ḥ in words of three letters; abbreviations), ṁ that the OCR read as a final h, Devanagari read as Latin junk, and what the second pass left (11 Ś candidates and 79 bracketed terms it could not place, or where the print has another word). The Ś the OCR dropped from Śiva, Śakti and Śaiva was put back in the English lines on 22 Oct 2026, night (`proof.py`, 803 words; 31 of them read on the page images, all as printed), and on 23 Oct where the page shows it in Sanskrit lines and mantra lists (33). On 23 Oct ṁ read as "ri"/"r" was mended (506, by rule; 58 of 58 sampled as printed), 130 bracketed terms were given the print's diacritics (240 more are printed without them), and the 43 notes outside the verse chapters had the letter clean-up. The record is the AI log, 23 Oct 2026 (15:04–15:45). Later the same day ṛ and ḥ were restored by rule (22,089 words; 175 of 178 sampled words as printed; AI log, 23 Oct 2026, 15:58–16:20).
- Where a range is printed inside one of Dyczkowski's long translations (8.438–445), the phase 5 map split it, so part of the translation shows as commentary. A lead-in sentence occasionally sits under the next verse's heading (6.39).
- Where Dyczkowski quotes a passage at the very start or end of a chapter, the quotation may still have headings of its own ("Dyczkowski's verse N").
- 25 verse notes have no unit placed (new or renamed units) and 113 have no commentary within reach; they have no box.
