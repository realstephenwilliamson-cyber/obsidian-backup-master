---
type: prompt
updated: 2026-10-06
---
# 3 Links, catalog and structure

**Use when:** after phase 2.

**What it does:** the rest of the analysis's fixes, in seven parallel tracks:
1. Zohar links;
2. missing links (Augustine → John, Tanya → Zohar, Mei HaShiloach → Tanakh, the BCP);
3. crosswalks;
4. the lectionary's second track and the haftarot;
5. the LXX verse ids;
6. the catalog;
7. dashboards and scripts.

**Expect:** about two sessions. You approve one dry-run list per track.

````text
Phase 3 of my October 2026 plan for my Obsidian vault (C:\Vaults\Obsidian Vault): the link, lectionary, catalog and structure fixes from the 6 Oct analysis.

FIRST read Prompts/October 2026 plan/0 Plan - read me first.md and follow its rules. Then read:
- the progress doc (including the decisions I made in phase 1);
- in Notes/Vault analysis (6 Oct 2026)/: Checked findings.md and the B, C, D, E, F and G reports;
- the scripts in .work/analysis-2026-10-06/;
- .work/plan/phase-3-prep/, if it exists.

How to work:
- Act only on findings that held in the checking pass, and on decisions only as I answered them.
- Each track is its own workflow of agents. Run the tracks in parallel where they don't touch the same notes.
- For each track: one dry-run list for my approval, then apply in batches, with backups.

Track 1. Zohar (B7–B10, E1)
- The ~619 references tagged (MhN) → the Midrash ha-Ne'lam notes in volume 10.
- The ~129 links to the 1933 Soncino note where a Pritzker note has that folio → the Pritzker note.
- The 9 links that open a different folio from the one they name.
- The ~10 folios split wrongly ("149a" read as 1:49a).
- The folio index: add volumes 10 and 12.

Track 2. Missing links (C1, C2, E6, E9–E12, E19, B18, B19)
- Augustine's 124 tractates:
  - link each one to the John verses it treats, taken from its heading and checked against its text. Tractate 17's heading says John 4 but its text is John 5 (E6): link John 5 and add a note.
  - In tractates 49–124, remove the ~962 stray footnote numbers and ~710 footnote fragments. Compare against the source text named in the tractate notes (download approved), so that nothing of Augustine's is lost. List anything unsure.
- The Tanya's ~382 Zohar citations ("Zohar II:85a") → the Pritzker folio notes, by the Guide's Zohar rule.
- Mei HaShiloach's ~850 scripture citations, which use Hebrew book names ("Mishlei, 23:26") → the Tanakh and Torah verse notes.
- The Tikkunei Zohar and BCP references the reports list.
- Keep each citation's text as it is and wrap it in the link. Never link inside quoted Hebrew or inside headings.

Track 3. Crosswalks and scripture numbering (B21–B23, E2–E5, E7, E8, E16, E17)
- The RCL concordance: the 4 wrong range links, the wrong Zohar cells and the 5 wrong tractate ranges.
- The 7 Prayer Book psalm-verse links: use the Psalms numbering crosswalk.
- The 4 shifted parashah ranges and the 5 other shifted references.
- The 2 misprints carried over from the sources (E8): mark them, don't silently correct them. This is a decision for me.
- The Kabbalah/Trika crosswalks (E16, E17):
  - list each statement that the vault's own Tantrāloka text contradicts, with the verse, for me to decide;
  - where a crosswalk links only the top of a note, link the exact verse.

Track 4. Lectionary and the Jewish year (C9, C10, C14–C16, B11, B25, B27, B31)
- Each Proper: add the second Old Testament track and the "or" alternatives.
  - Citations from the RCL tables, verse text from the vault.
  - Same format as the existing readings, so the embeds keep working.
- The collect and the Prayer Book psalm in the homily note (C's proposal): show me the template change first.
- A haftarah table: each parashah → its haftarah, from Sefaria, Ashkenazi custom by default, with Sephardi differences noted.
  - As one table note, and as a section in each parashah note.
  - The parashah notes should link forward to Mei HaShiloach and the Zohar, not only to Rashi (B31).
- Mei HaShiloach volume II (B27) and Pritzker volume 11 (B11) aren't free: list them for phase 7.

Track 5. LXX verse ids (G37)
- Obsidian doesn't register a block id that sits in the middle of a paragraph.
- Test first with Texts/RCL/Lectionary/RCL/Year C/Epiphany-8C.md and one LXX note.
- Then, in the 1,116 LXX notes, put each verse in its own paragraph (a blank line after each verse), keeping the text and the ids.
- Check:
  - the 16 lectionary embeds that depend on these ids now show their verse;
  - 50 random verse links open the right verse.

Track 6. Catalog and Philosophy (D4–D10, D14, D15, D19, D21, G27–G32)
- The 10 catalog notes with a wrong author, editor, year or identity.
- Bennett's Leviathan: label it as his adaptation of Parts 1–2, not the 1651 text. The complete text comes in phase 7.
- The Grant article: file it under its author, and link it from the Cybernetic Leviathan note.
- The Technics and Time 2 file: mark it as an uncorrected proof.
- The Technics hub's literature feed shows 10 of 53 works, chosen by file-creation time. Make it show the core works first, by a property or an explicit list; show me before applying.
- The 123 catalog notes without a "Checked against the file" line:
  - follow Prompts/Check catalog notes against their files.md for all of them (agents, about 5 notes each, title and copyright pages);
  - put the corrections in one approval list.
- Hub links to texts that aren't in the vault (Phaedrus and Pirkei Avot; D1–D3, E21): make them plain text marked "(not in the vault yet)". Phase 7 relinks them.

Track 7. Dashboards and scripts (F3, the other F findings, G41, G48, the remaining G findings)
- The Today block on Home:
  - make the order of today-study, today-verses and daily-office fixed;
  - make their errors visible instead of silent (F3).
- Every other F finding that held: fix the safe ones.
- List the per-device switches Home depends on (F23, F24): syncing "other file types" so the view.js scripts reach the phone, the Templater trigger, Homepage, and so on. These become a "Setting up a new device" checklist in the Guide.
- The G findings that are left (properties, empty sections, stale instructions): fix the safe ones. Duplicates are listed, not deleted.

Checks for each track:
- counts;
- unresolved links unchanged or fewer;
- 20 random changed links opened by script in Obsidian (the target exists, and its heading or block resolves);
- a checking agent reads 30 changed notes against the source.

Approval points: one dry-run list per track; the decisions; the template change.

At the end: fix any Guide or Welcome sentence this phase made untrue, and add a History line.

If the window still has room, prepare phase 4 (read-only) and save it in .work/plan/phase-4-prep/: from Prompts/Scripts/PDF inventory (6 Oct 2026).csv, the classification of every PDF and the proposed not-to-convert list.
````

**Afterwards:** check what [[AI/Archive/Claude outputs/0 Plan - read me first]] lists under *After 3*, then start [[AI/Archive/Claude outputs/4 Convert the library PDFs to Markdown]].
