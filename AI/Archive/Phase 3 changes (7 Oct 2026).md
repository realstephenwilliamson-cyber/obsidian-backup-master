---
type: report
date: 2026-10-07
tags:
  - vault-analysis
---

# Phase 3 changes (7 Oct 2026)

Phase 3 of the [[AI/Archive/Claude outputs/0 Plan - read me first|October 2026 plan]], *Links, catalog and structure*, ran from 00:05 to about 10:15 EDT on 7 Oct 2026. It acted only on findings that held in phase 1's checking pass ([[Checked findings]]), and on Stephen's answers to two decision lists. Each track was drafted by agents and read by a separate checking agent before anything was applied. Every change was dry-run in Obsidian first and backed up in `.work/backup-phase3-2026-10-07/`; renames and moves went through Obsidian, so links followed.

**Stephen's decisions:**
- Batch 1 (answered about 01:00): "batch 1: recommended" (Zohar Z1–Z9, Tanya T1–T6, Mei HaShiloach M1–M8, haftarot H1–H6).
- Overnight: apply only the tracks his answers already decided.
- Batch 2 (answered 08:40): "batch 2: recommended", and for the one question without a recommendation, X3 = (b): link the verse meant, keep the printed number as the label, with a marked note.
- The questions and every ★ choice are in `Claude outputs/Phase 3 - decisions, batch 1.md` and `… batch 2.md`; the full change lists are in the eight `Phase 3 - dry run, track N …` files beside them.

**In all:** about 11,300 operations; 3,645 notes changed, 1 note made ([[Haftarot]]), 5 notes renamed or moved; about 15,300 links added or retargeted, and 1,099 embeds added.

## What changed, by track

| Track | When (EDT) | What |
|---|---|---|
| 5 LXX verse ids (G37) | 01:11 | A blank line after each verse in the 1,116 LXX notes (27,573 lines), so Obsidian registers every verse id. Links and embeds into LXX verses that resolve: 3 before, 114 of 114 after. |
| 2 Tanya, Mei HaShiloach | 01:15 | 1,653 links in 151 notes: 622 Tanya and Mei HaShiloach citations of the Zohar and Tikkunei Zohar; 1,031 Mei HaShiloach scripture citations to Tanakh and Torah. Each citation's text kept, the link wrapped round it. |
| 1 Zohar | 01:36–01:39, 07:37, 09:26 | 1,062 footnote links retargeted (B8, B10); the [[Zohar folio index]] extended to volumes 10 and 12 (404 ids, with "not marked" lists); 12 B6 folio ids placed (6 overnight, 6 in batch 2) and their links; "Pritzker translation" lines on Soncino notes (24 first lines, 80 second lines, and the lines for 1.109b, 1.121a, 3.151a, 3.283a); `Zohar 8.03` renamed *Parashat Qedoshim* and `8.04` *Parashat Emor*, with the links meant by name fixed; the concordance's Zohar cells (Z9); two main-text ids (`^z1-109b`, `^z1-121a`) and the six footnote links to them; the Sample Homily's "Emor" link (Z14). |
| 2 Tikkunei Zohar, BCP | 08:35 | 372 Tikkunei Zohar citations linked to Tanakh and Torah (E10); 26 BCP Apocrypha lessons to the LXX (E11); 529 psalm numbers in the BCP Sunday lectionary tables to the BCP Psalm notes (L7); the Judith footnote and Ecclesiastes 2 items (L6); Mei HaShiloach Emor → 8.04 (L2); 7 Tanya "Introduction" citations to *Patach Eliyahu* (L3); `Song. 1:6` in 060b (L5, tested first: the italics stay intact). |
| 2 Augustine | 08:35, 09:26 | Each of the 124 tractates opens with a **John:** line (129 links); 123 Source callouts link the tractate's own CCEL page; tractates 49–124 (87 aside) cleaned of pasted footnote matter (1,275 deletions, every one read against CCEL); A1: the `passage` property and the index row follow the text in 8 tractates, with a callout line for the 6 whose range differs; A3: 32 false § headings removed or moved to where CCEL's sections begin, 27 printed running heads removed, 10 digits of 122 §8 restored from CCEL. |
| 3 Crosswalks, numbering | 08:35, 09:26 | 35 BCP psalm-verse links point at the BCP Psalm notes (E2); the numbering rule in the Guide, the *Map new connections* prompt and the concordance (X2); the two source slips (E8, X3 b); the alphabet crosswalk's statements reworded where the vault's Tantrāloka contradicts them (X4–X7); the Parātrīśikā crosswalk (X10–X15; the 1992 Muller-Ortega chapter is in the vault's Goudriaan volume, ch. 8); two KSTS editions linked. |
| 4 Lectionary | 08:35, 09:27 | The second (complementary) Old Testament track and the "or" readings in the 78 Propers 4–29 (1,060 embeds); the C9 repair of Proper 28B and Reign of Christ C; Proper 22C's Lamentations (R4); the [[Haftarot]] note (Ashkenazi, Sephardi differences noted, special Shabbatot with the plan dates) and a `## Haftarah` section and header links (Mei HaShiloach, Zohar, Haftarah) in the 54 parashah notes, with a Haftarah column in the concordance; 128 collect ids renamed after their occasion, 6 split collects joined, 2 Easter Vigil ids; `collect` (221 notes, Contemporary) and `psalm_bcp` (217 notes) properties; both homily templates show the collect of the day and the psalm as the Prayer Book prints it; 8 plan rows mark the Presentation, Annunciation and Visitation in Years 1–2 (R7). |
| 6 Catalog, Philosophy | 08:36, 09:37 | The 113 catalog notes without a check line checked against their files (344 property changes, a dated line each); `physical_copy: false` on 572 notes; Muktabodha years as numbers (478) and "Pre-1900" emptied (21); 236 stale sentences and lists; Bennett's *Leviathan* labelled as his adaptation; TT2 marked as an uncorrected proof; the Grant PDF filed under its author and linked from *The Cybernetic Leviathan*; the Technics hub's feed lists the 12 core works first; Phaedrus and Pirkei Avot made plain text "(not in the vault yet)"; C2, C6, C9, C10; the daily note's list property renamed `verses_read` (C7); the Monier-Williams note now describes the file it holds, Macdonell's dictionary (K7). |
| 7 Dashboards, G findings | 09:42 | Home's Today block in a fixed order, with a red line where a part fails (F3); the date box, lookup boxes, quick capture, review buttons, homily and hub templates (F4, F5, F19, F29); *Setting up a new device* in the Guide (F23, F24); NT references open the JPS verse (G21, 94 links); a space after italic labels in LXX footnotes (G26, 2,544 places, and 75 more beyond the checked count); previous/next lines in 1,701 notes (G19); Zohar vols 10 and 12 footnotes and titles (G51); Mei HaShiloach teaching headings show the verse cited (D8); BCP collect headings (D9); B14, B34, C20, D31, A12; the JPS, LXX and BCP psalms link one another (E25, 907 links) and each John chapter links its tractates (129). |

## Checks

- **Before applying:** a checking agent read every op (or, for the largest sets, every op by script and a sample by reading) against its source: the Zohar notes, Sefaria, CCEL, Vanderbilt, the BCP and JPS texts, the catalog files' title pages. Its corrections were made, or the item was held.
- **After each batch, in Obsidian:**
  - every new or changed link resolves (1,653; 1,669; 2,330; 856; 6,121);
  - 20 random changed links per batch opened with Obsidian's own link opening, each on the right note and verse;
  - unresolved links: 107 before the phase, 96 after (74 pairs in 21 notes; the Hub template's 11 placeholder links are gone);
  - Home and Home (mobile) render with no Dataview errors.
- **Track 7, in Obsidian, before and after:** before, the Today block drew the Office first, a forced read error made parts vanish with no message, and a refresh while drawing doubled parts. After: study lines, *Today's verses*, *Translation*, *Daily Office* in that order on both Homes; forced errors give red lines (`today-study failed: …`, `today-verses failed: …`, `Could not build today's Daily Office: …`); a refresh while drawing shows each part once. The date box is unchanged today and gives the expected lines on three test dates in late 2029 and 2030; Dataview's `index.touch()` redraws it (the midnight redraw's dependency); the review buttons show "These buttons work only in Vault review - actions" outside that note; the lookup and Devanagari boxes keep their text across a redraw.
- **Z11:** the 19 "Pritzker translation" lines added in batch 2 open the paragraph at the folio id, which sits at the print page's head (B5), so each opens 0–4 paragraphs before the cited side's text, across a passage boundary. For 1.098b it is a third line.

## Held or left for later

- **Batch 3 (answered "recommended"; applied 10:30 EDT):** Tractate 87 and 1–48 cleaned the same way as 49–124 (60 deletions: footnote numbers, pasted note text and printed running heads; a checker re-read 30 against CCEL and 30 against the saved copies, 0 wrong); the Home follow-ups ("Not yet written in the last 14 days", open sections stay open, buttons take the date when pressed, the plan's last week and end, a time-zone line, red lines for the date box, Sanskrit card and quick capture, a nav line in new daily notes, Polyphonic homily fixes, a *Scratch* view in Library.base); 022's subtitle and languages; Pentecost A–C `psalm_bcp` 37a. Tested in Obsidian: the new label, sections kept open on a redraw, the Advent 1B button and the plan-ended line on fake dates, red lines for forced errors in the panchang, the flashcard register and quick capture, and no doubling on a refresh while drawing. Quick capture's kept form was tested only in the harness.
- **Held:** C34 (the CCT notice in 225 RCL notes): commontexts.org's permissions page was refused (rate limit), so the wording CCT asks for is not confirmed. 9 second Pritzker lines (Z11) wait for B5's id pass; Tsav and Qedoshim (Z15) for a matching pass; G19's Pritzker volume 1 lines for a rebuild under the title.
- **Left, as answered:** 5 Tanya links (L1), the *Raaya Mehemna* links (L4), A2, A4, X8, X9, R1, R6, C11 (Wiener and Lessig on the phase 7 list), K1–K9 as in the list.
- **Listed, not changed:** BCP transcription slips (Monday in Holy Week "none other that", Vigil "only- begotten", Epiphany "Peoples"), which need a printed copy; six Tikkunei citations that do not fit their verses; the *Mātṛkā* concept note's "earth element (*kṣa*)" (Stephen's writing).
- **Phase 4 preparation:** `.work/plan/phase-4-prep/` classifies the 690 PDF and DjVu files and proposes 33 not to convert, with 9 for Stephen's decision.
