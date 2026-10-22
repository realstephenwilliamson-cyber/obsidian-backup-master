---
type: note
created: 2026-10-06
---
# Vault analysis (6 Oct 2026) - agent summaries

The closing messages of the seven agents (areas A to G) of the analysis run on 6 Oct 2026 with [[Vault analysis (micro and macro)|Vault analysis (micro and macro)]], as Stephen copied them from that task. The lead was cut off before its checking pass and merged report, so these findings had not yet been checked by a second agent. Phase 1 of the [[AI/Archive/Claude outputs/0 Plan - read me first|October 2026 plan]] does that check and writes *Checked findings*.

The full reports (`A-report.md` to `G-report.md`) and findings (`A-findings.json` to `G-findings.json`) belong in this folder once they are copied from the analysis task. The paths below (`/home/claude/work/...`) are in that task's own workspace, not in the vault. The agents changed nothing in the vault.

---

Area A is finished: all eight checks in the brief were done, and both files are written and the JSON validates (30 findings).

- Report: `/home/claude/work/reports/A-report.md`
- Findings: `/home/claude/work/reports/A-findings.json`
- Scripts: `/home/claude/work/scratch/A/` (libraries installed: rapidfuzz, pyluach)

Findings by kind: wrong 8, gap 6, note 10, improvement 3, broken 1, fragile 1, proposal 1.

The three most important:

1. **The Mūla blocks are not a reliable root text (A1, A2).** In the 19 āhnikas with an independent text (DCS), 53 of 5,444 root half-lines are in no `^mula` block; 46 of them sit in a neighbouring Viveka section. In the same āhnikas, 38 Mūla lines in 37 notes are Jayaratha's prose (e.g. 1.330, 4.10, 15.203). The other 18 āhnikas have no measured rate, but the fault is there too: 37.49, 37.50, 37.58, 37.62 and 37.75 hold only the last quarter of the verse, and they fall on 21–25 Nov 2026 in the practice run. Home's "Today's verses" and the daily note embed only these blocks.
2. **Dyczkowski numbers about a fifth of the verses differently from the vault, and no note says so (A3).** Of 4,813 verses whose printed number could be read, 993 are shifted by half a verse or one verse. The affected āhnikas are 1–6, 8, 11, 13, 15, 16 and 19; none in 28–37. All 5,845 page links are still right, because they were matched by text.
3. **The KSTS edition is not in the vault (A7, A5, A6).** The folder holds two notes and a TSV. The "verse-page map" is 228 anchor rows, 88 of them estimates, with nine internal contradictions, yet the Welcome note says it gives every verse's page. No KSTS page could therefore be tested.

The study plan, the Muktabodha links and the secondary-literature index hold up; the index is 58 of 60 correct on a random sample. One small break affects the plan: "Today's verses" will show no translation link on five days, the first being 17 Nov 2026 (A15).

One web page could not be read: the archive.org item for KSTS vol. IX was refused by the fetch proxy with a rate-limit error, and I did not retry it. Everything else left unchecked is listed in the report's last section, as asked.

Area B is finished: both files are written and the JSON validates with 35 findings.

Report: /home/claude/work/reports/B-report.md
Findings: /home/claude/work/reports/B-findings.json
Scripts and reference data: /home/claude/work/scratch/B/

Findings by kind: wrong 10, note 10, gap 8, improvement 3, proposal 2, broken 1, fragile 1.

Three most important:

The texts are sound; the Zohar links are where the faults are. Torah and Tanakh are complete: 5,846 + 17,360 verses, and all 929 chapters match Sefaria's verse counts. Rashi, the Tanya and the Pritzker Zohar notes are complete and clean. But at least 619 references the edition tags "(MhN)" open the main-Zohar note instead of the Midrash ha-Ne'lam text in volume 10. A further 129 links open the 1933 Soncino note although a Pritzker note has that folio, 9 open a different folio from the one they name, and the folio index omits volumes 10 and 12. All are mechanical fixes (B7–B10).
The Hasidic texts are not joined to the rest. The Tanya's 382 Zohar citations ("Zohar II:85a") and about 850 scripture citations in Mei HaShiloach (Hebrew book names such as "Mishlei, 23:26") are plain text. In the concordance, 4 range links and 10 Zohar cells are wrong or weak, and the Homily (Polyphonic) template's four parashah links cannot resolve for any value of parashah (B18, B19, B21–B23).
Gaps for the weekly reading. Haftarot are not mapped to parashiot anywhere. Pritzker volume 11 is absent, with 933 references pointing into its range. Mei HaShiloach is volume I only. Parashah notes link forward only to Rashi (B25, B11, B27, B31).

Not settled, and listed in the report: Rashi comment counts were compared with Sefaria in full for Deuteronomy but on only 16 sample chapters for the other four books. Stanford University Press and Project MUSE refused the fetch, so volume 11's details and one book recommendation rest on search listings. Nothing was run in Obsidian, so the template finding and one duplicate-id finding rest on reading the files.

Area C is finished: both files are written and the JSON validates with 35 findings.

- Report: `/home/claude/work/reports/C-report.md`
- Findings: `/home/claude/work/reports/C-findings.json`
- Scripts: `/home/claude/work/scratch/C/` (`build_report.py` with `report_data.py` regenerates both files)

**Findings by kind (C1–C35):** wrong 11, gap 9, note 6, broken 3, fragile 3, improvement 2, proposal 1. 33 are verified and 2 unverified (C22, C34); 19 fixes are safe and 16 need Stephen.

**Three most important:**
1. **Augustine is cut off from John and partly corrupted (C1, C2).** None of the 124 tractate notes contains a link, so no tractate is reachable from the John verse it treats, though the Vault Guide says New Testament references in the Fathers are linked. Tractates 49–124 also carry 962 stray footnote numbers and about 710 pieces of footnote text inside sentences.
2. **The homily workflow picks the wrong occasion on feasts (C11, C12, C13).** It works for an ordinary Sunday (traced for 11 Oct, 22 Nov and 29 Nov 2026). On Sunday 1 Nov 2026 the button will offer Proper 26A rather than All Saints. A dated note on a weekday feast such as 25 Dec silently takes the coming Sunday's readings. `Templates/Homily (Polyphonic).md` cannot produce one working link.
3. **The lectionary notes are accurate but incomplete (C9, C10, C14, C15, C16).** All 8,471 verse embeds resolve and every renumbering checked is right. But each Proper holds only one of the two Old Testament tracks and the "or" alternatives are dropped. The "Fixed" All Saints and Thanksgiving notes hold Year A readings yet are used in 2027 and 2028. The collect and the Prayer Book psalm never reach the homily note.

**Not settled:** Obsidian's own behaviour could not be tested from the mirror, chiefly whether the LXX verse anchors are addressable (C22). About 160 RCL notes were checked for internal consistency only, not against Vanderbilt. Three Daily Office differences from Wikisource remain open against a printed Prayer Book (C29).

**For the main session to save:** Stephen emptied `.trash` himself before the analysis, and Sync being paused is intended; neither is reported as a fault.

The area D report and findings are written and the JSON validates (35 findings).

- **Report:** `/home/claude/work/reports/D-report.md`
- **Findings:** `/home/claude/work/reports/D-findings.json`
- **Scripts:** `/home/claude/work/scratch/D/` (`build_report.py` regenerates both files)

**Findings by kind:** 9 wrong, 3 broken, 8 gap, 1 fragile, 9 improvement, 4 note, 1 proposal.

**Three most important:**
1. **No Plato in the vault, and two hub links are wrong.** The Second Domestication hub's "Plato — Phaedrus (Thamus & Theuth)" opens Graham's Presocratics Part 2 (no mention of Theuth or Thamus in the file). Its "Pirkei Avot" opens the Rashi index; the vault has no Avot. Free, legal Phaedrus texts were confirmed on Perseus and Gutenberg (D1, D2, D3, D30).
2. **The only "Leviathan" is Jonathan Bennett's modernised adaptation of Parts 1–2**, catalogued as the primary text, labelled "(1651)" in a concept note and listed as "Complete" in the Incomplete Sets guide. Parts 3–4 are not in the vault. Husserl's time lectures, Being and Time, Derrida's Dissemination and Time and Narrative are also not held (D4, D5, D19, D28).
3. **Catalog and feeds are unreliable for this project.** Ten catalog notes have a wrong author, editor, year or identity. The Grant article that seeded the Cybernetic Leviathan is filed under "Glendinning" and linked from nothing. The Technics and Time 2 file is an uncorrected proof. The Technics hub's literature feed shows 10 of 53 matches chosen by file-creation time, with none of the core works. Per Obsidian's documentation, `Stiegler.base` misses two of his books. Only 18 of 120 Philosophy catalog notes are linked from his notes (D6–D10, D14, D15, D21).

Nothing was run inside Obsidian, so the feed and base results are computed from the queries and the catalog. A few bibliographic details (Ricoeur *Writings and Lectures* vol. 5, the Husserl translation, open access for *Bifurcate*) could not be confirmed online and are marked in the findings. The lead's three instructions are followed: checkpoints were written, `.trash` appears only as stale sentences in notes (D23), and Sync is not reported.

**Area E is finished. Both files are written and the JSON validates (43 findings).**

- Report: `/home/claude/work/reports/E-report.md`
- Findings: `/home/claude/work/reports/E-findings.json`
- Scripts, for re-running: `/home/claude/work/scratch/E/`

**Findings by kind:** wrong 12, gap 7, broken 2, fragile 1, improvement 2, note 4, proposal 15 (E29–E43, each read on both sides).

**The three most important:**

1. **The Tantrāloka is an island in the link graph (E20).** There are no links between a Tantrāloka passage and any Jewish or Christian text, in either direction. Only 40 of 5,845 verse notes are linked from outside the Tantrāloka area, and Stephen's Writing folder links none. Seven of the proposals anchor a Trika passage (E29–E35).
2. **The scripted links are mechanically sound, but 29 are wrong and about 1,100 references were never linked.** All 226,221 anchored links resolve and no Bible link names one book and opens another. The wrong ones are:
   - 10 Zohar folios mis-split ("149a" read as 1:49a) (E1);
   - 7 Prayer Book psalm verses, because the BCP numbers verses its own way (E2);
   - 4 parashah ranges (E3) and 5 other references (E7) shifted that were not in English numbering;
   - Tractate 17, whose heading says John 4 but whose text is John 5 — the slip is in the source page (E6);
   - 2 misprints carried from the sources (E8).

   The unlinked ones are in Mei HaShiloach, the Tanya's Zohar citations, Tikkunei Zohar and the BCP (E9, E10, E11, E19). The 124 Augustine tractate texts carry no links at all (E12).
3. **The crosswalks are the weakest part.**
   - The RCL concordance has 4 wrong range links, 6 Zohar cells pointing at other parashiyot and 5 wrong tractate ranges (E3–E5).
   - The two Kabbalah/Trika crosswalks contain statements that the vault's own Tantrāloka text contradicts, and link only the tops of two notes (E16, E17).
   - The Second Domestication hub's "Phaedrus" link opens a Presocratics volume, and the dialogue is not in the library (E21).

Not checked, and listed in the report: the Pritzker print volumes (not in the vault), the 122 other tractate headings against their text, and the factual content of the two research-guide crosswalks.

Area F is finished: both files are written and the JSON validates (32 findings).

- Report: `/home/claude/work/reports/F-report.md`
- Findings: `/home/claude/work/reports/F-findings.json`
- Scripts, Node harness and outputs: `/home/claude/work/scratch/F/` (re-run instructions are in the report's last section)

**Findings by kind:** 8 fragile, 7 wrong, 3 broken, 1 gap, 4 improvement, 1 proposal, 8 note.

**Three most important:**
1. **Home's note buttons can make blank notes (F1, F2).** Templater's "Trigger on new file creation" is stored per device in the installed 2.25.1 and does not sync, so the buttons can make a blank note that then counts as written. This already happened to the 4 Oct homily note, and the Guide's remedy ("Replace templates in the active file") does not fill a blank note.
2. **Home on a second device depends on switches nobody has written down (F23, F24).** The eleven `view.js` scripts are "other file types", which Obsidian Sync leaves out by default and which is set per device; the Guide's Standard-plan advice is to leave that switch off. At least six such per-device settings decide whether Home works on the phone.
3. **Three Bases list all 10,162 files under Library instead of the 640 catalog notes (F17).** `By author`, `By subject` and `Library.base` filter only on the `Library` folder; `Stiegler.base` also pulls in 16 PDFs and misses two of Stiegler's works. This comes from my own evaluation against Obsidian's documented rules, not from opening the Bases.

Dataview does not wait for the views (F3), so their order in the Today block is not guaranteed and their errors are silent. This is read from the plugin code; nothing was run in Obsidian.

The tables under Home tested clean:
- **Study plan:** 1,156 rows, every one of the 5,845 verses covered once.
- **Daily Office:** 53 of 53 dates match the lectionary notes.
- **Shabbat table:** 40 of 42 values identical to hebcal, the other two off by one minute.
- **Panchang:** agrees with Drik Panchang on four dates.

Per your three changes: I checkpointed after each check, treated the emptied `.trash` only as stale statements (F27), and did not report the Sync pause itself. What I could not check is listed in the report, chiefly whether the Templater and Sync switches are on on either device, and the phone.

Nothing in the vault, `.obsidian` or `.work` was changed. I staged six plugin `main.js` files read-only to see how the installed versions behave.


Area G is finished: both files are written and the JSON validates (52 findings).

- Report: `/home/claude/work/reports/G-report.md`
- Findings: `/home/claude/work/reports/G-findings.json`
- Findings by kind: wrong 22, broken 6, gap 3, fragile 5, improvement 8, note 8.
- Coverage: all 20,352 notes and 22,410 file names were checked by script. Of the 132 sampled notes, 113 were read in full and the 19 longest in part. The 25 catalog notes were compared with their PDFs (20 agree, 5 differ), and the print-only Ruiz note agrees with the publisher's page.

The three most important findings:
1. **G37 (broken, unverified in his app):** in the 1,116 Septuagint notes, 27,573 verse ids sit mid-paragraph, where Obsidian does not register them. Single verses cannot be linked or embedded, and 16 lectionary embeds depend on them. The fix is one scripted pass adding a blank line after each verse; opening `Texts/RCL/Lectionary/RCL/Year C/Epiphany-8C.md` confirms it first.
2. **G36 (wrong):** 84 Tantraloka verse notes have a mula that is not the verse — commentary run in (36), a half-verse missing (44), or different text (4). Only the 2,726 verses with word-analysis notes could be compared; the other 3,119 are unchecked.
3. **G32 with G27–G30:** catalog errors cluster in the 123 of 640 notes with no "Checked against the file" line. All 4 such notes in the sample were wrong or incomplete, against 1 of 21 checked ones.

Next in value are G1/G2: the `Library/Library.base` "All" view is filtered to one author, and three tables take in 9,247 notes instead of the 640 catalog notes.

Nothing was run in Obsidian, so Bases, Dataview and Templater behaviour, and the block-id and line-break findings (G37, G41, G48), rest on reading and documentation. All limits are listed under "Things I could not check".
