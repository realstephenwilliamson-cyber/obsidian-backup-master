---
type: prompt
updated: 2026-10-06
---
# 2 Repair the Tantraloka root text

**Use when:** after phase 1.

**What it does:**
- checks the Mūla block of every Tantrāloka verse note against two independent witnesses: the Digital Corpus of Sanskrit (DCS) and the Kashmir Series (KSTS) edition;
- repairs the Mūla blocks after showing you examples;
- rebuilds the verse-page map so that every verse has its KSTS page.

**Expect:** one or two sessions. You approve 30 examples and a short list of uncertain readings.

````text
Phase 2 of my October 2026 plan for my Obsidian vault (C:\Vaults\Obsidian Vault): make the Tantrāloka's root text (the Mūla blocks in the verse notes) match the edition, and rebuild the KSTS verse-page map.

FIRST read Prompts/October 2026 plan/0 Plan - read me first.md and follow its rules. Then read:
- the progress doc;
- in Notes/Vault analysis (6 Oct 2026)/: A-report.md, G-report.md (G36) and Checked findings.md;
- the area A scripts in .work/analysis-2026-10-06/ (the DCS comparison);
- .work/plan/phase-2-prep/, if it exists;
- six verse notes from different āhnikas, to see how the Mūla, IAST, translation and Viveka sections are laid out.

What the analysis found (checked in phase 1):
- In the 19 āhnikas that DCS covers, 53 of 5,444 root half-lines are in no ^mula block. 46 of them sit in a neighbouring Viveka section.
- In the same āhnikas, 38 Mūla lines are Jayaratha's prose.
- 84 of the verses that have word-analysis notes have a wrong Mūla: commentary run in, a half-verse missing, or different text.
- The other 18 āhnikas are unmeasured.
- The "verse-page map" is 228 anchor rows, 88 of them estimates, with nine contradictions.
- The KSTS edition isn't in the vault.

1. Reference texts.
   - DCS, for the āhnikas it covers.
   - The KSTS edition (archive.org, public domain; download approved), for all 37 āhnikas:
     - OCR the Devanagari verses (Tesseract san) and transliterate them to IAST;
     - use it as the witness for the āhnikas DCS lacks, and as a second witness where DCS has them;
     - record each volume's archive.org identifier and the printed and PDF page of every verse. This becomes the new page map (step 5).
   - A third witness where it helps: the Muktabodha e-text in Texts/MUKTABODHA-LIBRARY-IAST_2026_02_20, if it has the Tantrāloka.
2. Align every verse note's Mūla with the witnesses.
   - Work at the half-line level, with fuzzy matching (rapidfuzz).
   - Classify each verse: correct; half-line missing (and where it is now); commentary in the Mūla; partial; different text; unclear.
   - Use one workflow, with an agent per āhnika or pair of āhnikas. Each agent returns its table and the proposed new Mūla for each verse, with the witnesses' lines.
3. Check every proposed change.
   - Use checking agents separate from the aligners.
   - Each one looks at the KSTS page image and either confirms the change or sends it back.
   - Where the witnesses disagree, don't guess: put both readings and the page on a list for me.
4. Show me, and wait for my approval:
   - the counts by class and āhnika;
   - 30 before/after examples from at least 10 āhnikas;
   - the open list.
   Then apply:
   - change only the Mūla block (Devanagari and IAST), and, where a half-line moved out of a Viveka section, that Viveka section;
   - keep the ^mula block ids and everything else in the note.
   For each verse whose Mūla changed and that has a word-analysis note in Library/Sanskrit/Tantraloka words/, say whether the analysis still matches.
5. The page map.
   - Rebuild "Tantraloka verse-page map.md" and tantraloka-pages.tsv in Library/Sanskrit/KSTS/Trika/KSTS - Tantraloka Sanskrit (vols I-XII)/ so that every verse has its KSTS volume, printed page and PDF page, from step 1.
   - Back up the old files first.
   - Ask me whether to add the KSTS volumes themselves to the vault, with their sizes. Files over 25 MB go through Downloads.
     - If yes, the map's links open the local PDF at the page.
     - If no, they open archive.org at the page.
6. Checks:
   - every verse note still has exactly one ^mula block;
   - a script check that no Mūla line matches Viveka prose better than root text;
   - a checking agent reads 100 random verses against the page image;
   - Home's Today's verses works on 10 dates across the plan;
   - the unresolved-link count is unchanged.
7. Update the Tantrāloka sections of the Guide and the Welcome note, and the KSTS volumes note, to say what is now true. Add a History line.

Approval points: the open list from step 3; the 30 examples; adding the KSTS volumes.

If the window still has room, prepare phase 3 (read-only) and save it in .work/plan/phase-3-prep/: the Sefaria reference data and the link tables for the Zohar, Tanya and Mei HaShiloach fixes.
````

**Afterwards:** check *Today's verses* on a few dates and skim the list of repaired verses. Then start [[AI/Archive/Claude outputs/3 Links, catalog and structure]].
