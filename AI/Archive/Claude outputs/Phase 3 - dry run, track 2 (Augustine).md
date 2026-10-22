# Track 2 – Augustine: full change list (batch 2)

For the section *Track 2 – Augustine’s Tractates on John* in “Phase 3 – decisions, batch 2”. Built on 7 Oct 2026 from the notes snapshot of 04:08 UTC. Nothing here is applied yet.

## Counts

- **John line:** 124 notes, 129 links (Tractates 11, 33, 50, 120 and 122 span two chapters). Ops: `drafts/t2-aug/map/ops.json` (124 of its 247 ops).
- **Source callout URL:** 123 notes (Tractate 1 already had its own page). Same file, the other 123 ops.
- **Cleanup of 49–124:** 1,275 ops in 75 notes (all of 49–124 except 87). Every op only deletes. Ops: `drafts/t2-aug/clean-<a>-<b>/ops.json`, 13 files.
  - 975 footnote numbers left in the running text (most glued to the word before): 971 ops, plus 4 numbers (1060, 1097, 1168, 1713) that sit at the head of a pasted block and go with it. The 49–54 draft’s own table says 116; it counts its 1060 and 1097 with the blocks.
  - 304 pasted fragments: 187 are runs of bare scripture references; 54 hold all or the end of a translator’s note (“—Tr.”), usually with references; 63 hold other notes (Latin and Greek words, manuscript readings, cross-references to other tractates and other authors, Migne’s notes), usually with references. Rule used for the split: a fragment with “—Tr.” is a translator’s note; one made only of references is references; the rest is other.
  - 48,132 characters removed in all.
- **Tested together tonight** against the snapshot: the 247 map ops and the 1,275 cleanup ops apply with 0 refused, in either order. All 129 links resolve (unique base name, verse id present). The map ops must go in before track 7’s G19 line.
- **Checker:** every one of the 1,275 cleanup ops was re-read against its CCEL page by a second agent: 0 wrong.

## A1, recommended option: the 22 edits

Not in any ops file yet; built only if you choose this option. The H1 stays as it is in all eight. Index edits are in the table of `Augustine - Tractates on John`; its pipes are escaped, as in the note.

- **18:** `passage: "John 5:19"` → `"John 5:19–20"`; index `[[John 05#^5-19\|John 5:19]]` → `[[John 05#^5-19\|John 5:19–20]]`; callout line `> NPNF heads this tractate John 5:19; §9–11 also expound 5:20a.`
- **25:** `"John 6:15–44"` → `"John 6:15–40"`; index label `John 6:15–44` → `John 6:15–40`; callout line `> NPNF heads this tractate John 6:15–44; the sermon ends at 6:40, and 6:41–44 open Tractate 26.`
- **26:** `"John 6:41–59"` → `"John 6:41–58"`; index label `John 6:41–59` → `John 6:41–58`; callout line `> NPNF heads this tractate John 6:41–59; in the vault's numbering (BSB) the sermon ends at 6:58, and 6:59 is not quoted.`
- **27:** `"John 6:60–72"` → `"John 6:60–71"`; index label `John 6:60–72` → `John 6:60–71`; callout line `> NPNF heads this tractate John 6:60–72; the vault's John 6 (BSB) has 71 verses, and the sermon ends at 6:70–71.`
- **39:** `"John 8:26–27"` → `"John 8:25–26"`; index `[[John 08#^8-26\|John 8:26–27]]` → `[[John 08#^8-25\|John 8:25–26]]`; callout line `> NPNF heads this tractate John 8:26–27; the day's reading begins at 8:25 (§1), and 8:27 is taken up only at the start of Tractate 40 §2.`
- **44:** `"John 9"` → `"John 9:1–41"`; index `John 9` (unlinked) → `[[John 09#^9-1\|John 9:1–41]]`; no callout line (the heading is general, not wrong).
- **50:** `"John 11:55–57; 12"` → `"John 11:55–57; 12:1–11"`; index `; 12` (unlinked) → `; [[John 12#^12-1\|12:1–11]]`; no callout line.
- **64:** `"John 13:31–32"` → `"John 13:31–33"`; index label `John 13:31–32` → `John 13:31–33`; callout line `> NPNF heads this tractate John 13:31–32; the sermon expounds 13:33 as well.`

Each callout line goes after a `>` line at the end of the Source callout, as in Tractate 17. The evidence for each range is in `drafts/t2-aug/map/dryrun.md`.

Each callout line names NPNF’s heading. CCEL’s wording is on record only for 64 (finding E6), so the headings of 18, 25, 26, 27 and 39 are read on CCEL before these lines are written; any that differs from the H1 comes back to you. The index’s *Index by John Chapter* table lists 50 under John 11 only; adding it to the John 12 row is not among these edits.

## Per tractate

“John line” is the label of the new line. Where it differs from the heading, the heading follows in brackets (A1). A2 marks the sermons on a lesson already treated. Numbers and fragments are counted for 49–124 only; for 1–48 the last column gives what the survey found. A3–A6 are the questions in the section.

| Tractate | John line | Numbers removed | Fragments removed | Left alone or unsure |
|---|---|---|---|---|
| 1 | John 1:1–5 | — | — |  |
| 2 | John 1:6–14 | — | — |  |
| 3 | John 1:15–18 | — | — | survey: stray number 47 (A6) |
| 4 | John 1:19–33 | — | — |  |
| 5 | John 1:33 | — | — |  |
| 6 | John 1:32–33 | — | — | survey: stray number 126 (A6) |
| 7 | John 1:34–51 | — | — |  |
| 8 | John 2:1–4 | — | — |  |
| 9 | John 2:1–11 | — | — |  |
| 10 | John 2:12–21 | — | — | survey: stray number 257 (A6) |
| 11 | John 2:23–25; 3:1–5 | — | — | survey: “be1–5. lieved”, a page header inside a word (A6) |
| 12 | John 3:6–21 | — | — |  |
| 13 | John 3:22–29 | — | — |  |
| 14 | John 3:29–36 | — | — |  |
| 15 | John 4:1–42 | — | — |  |
| 16 | John 4:43–54 | — | — |  |
| 17 | John 5:1–18 | — | — | heading corrected to John 5 in phase 1; its Source callout says CCEL prints “Chapter IV. 1–18” |
| 18 | John 5:19–20 (heading: John 5:19; A1) | — | — |  |
| 19 | John 5:19–30 | — | — | survey: stray number 396 (A6) |
| 20 | John 5:19 | — | — | survey: stray number 407 (A6) |
| 21 | John 5:20–23 | — | — |  |
| 22 | John 5:24–30 | — | — |  |
| 23 | John 5:19–40 | — | — |  |
| 24 | John 6:1–14 | — | — |  |
| 25 | John 6:15–40 (heading: John 6:15–44; A1) | — | — |  |
| 26 | John 6:41–58 (heading: John 6:41–59; A1) | — | — | survey: stray number 518 (A6) |
| 27 | John 6:60–71 (heading: John 6:60–72; A1) | — | — |  |
| 28 | John 7:1–13 | — | — |  |
| 29 | John 7:14–18 | — | — |  |
| 30 | John 7:19–24 | — | — |  |
| 31 | John 7:25–36 | — | — |  |
| 32 | John 7:37–39 | — | — |  |
| 33 | John 7:40–53; 8:1–11 | — | — |  |
| 34 | John 8:12 | — | — |  |
| 35 | John 8:13–14 | — | — |  |
| 36 | John 8:15–18 | — | — |  |
| 37 | John 8:19–20 | — | — |  |
| 38 | John 8:21–25 | — | — | survey: 1 number, 3 note pieces (checked on CCEL) (A6) |
| 39 | John 8:25–26 (heading: John 8:26–27; A1) | — | — | survey: none found |
| 40 | John 8:28–32 | — | — | survey: 2 note pieces (estimate) (A6) |
| 41 | John 8:31–36 | — | — | survey: 1 number, 1 note piece (estimate) (A6) |
| 42 | John 8:37–47 | — | — | survey: 1 number, 1 note piece (checked on CCEL) (A6) |
| 43 | John 8:48–59 | — | — | survey: 4 note pieces, one twice (estimate) (A6) |
| 44 | John 9:1–41 (heading: John 9; A1) | — | — | survey: 1 number, 1 note piece (estimate) (A6) |
| 45 | John 10:1–10 | — | — | survey: 1 number, 3 note pieces (estimate) (A6) |
| 46 | John 10:11–13 | — | — | survey: none found |
| 47 | John 10:14–21 | — | — | survey: 5 note pieces (estimate) (A6) |
| 48 | John 10:22–42 | — | — | survey: 1 number, 3 note pieces (checked on CCEL) (A6) |
| 49 | John 11:1–54 | 7 | 6 | footnotes 961–999 were already gone before this cleanup, as in 1–48 |
| 50 | John 11:55–57; 12:1–11 (heading: John 11:55–57; 12; A1) | 20 | 7 | “doorposts”, CCEL “door-posts” (A4) |
| 51 | John 12:12–26 | 23 | 6 | — |
| 52 | John 12:27–36 | 24 | 7 | — |
| 53 | John 12:37–43 | 29 | 6 | false heading §14 (A3) |
| 54 | John 12:44–50 | 15 | 5 | `God “(ver. 43)`, CCEL `God” (ver. 43)` (A4) |
| 55 | John 13:1–5 | 15 | 5 | misplaced heading §4, “4.” in the prose (A3) |
| 56 | John 13:6–10 | 11 | 3 | running head “V. 2, 3.” (A3) |
| 57 | John 13:6–10 (second sermon on the lesson of 56; A2) | 27 | 4 | misplaced heading §3, “3.” in the prose; running head “V. 2, 3.” ×3 (A3) |
| 58 | John 13:10–15 | 13 | 4 | “freeborn”, CCEL “free-born” (A4) |
| 59 | John 13:16–20 | 6 | 2 | — |
| 60 | John 13:21 | 11 | 3 | — |
| 61 | John 13:21–26 | 8 | 3 | “in dicated”: CCEL page break (A4) |
| 62 | John 13:26–31 | 11 | 3 | “trustbetrayer”, CCEL “trust-betrayer” (A4) |
| 63 | John 13:31–32 | 8 | 2 | “it self”: CCEL reading unsettled (A4) |
| 64 | John 13:31–33 (heading: John 13:31–32; A1) | 7 | 4 | misplaced headings §3 (left empty) and §4, “3.” and “4.” in the prose (A3) |
| 65 | John 13:34–35 | 10 | 4 | misplaced heading §3, “3.” in the prose (A3); “blameworthy”, CCEL “blame-worthy” (A4) |
| 66 | John 13:36–38 | 6 | 2 | “Onlybegotten”, CCEL “Only-begotten” (A4) |
| 67 | John 14:1–3 | 9 | 2 | running head “On the Same Passage.” (A3) |
| 68 | John 14:1–3 (second sermon on 14:1–3; A2) | 15 | 3 | false heading §4; running head “On the Same Passage.” ×3 (A3) |
| 69 | John 14:4–6 | 9 | 3 | “lit tle”: CCEL page break (A4) |
| 70 | John 14:7–10 | 3 | 2 | “dis cover”: CCEL page break (A4) |
| 71 | John 14:10–14 (first of three on 14:10–14; A2) | 7 | 2 | running head “On the Same Passage.” (A3) |
| 72 | John 14:10–14 (second of three on 14:10–14; A2) | 10 | 3 | running head ×3 (A3); “justi fication”: CCEL page break (A4) |
| 73 | John 14:10–14 (third of three on 14:10–14; A2) | 10 | 3 | running head “Again on the Same Passage.” ×2, one inside “sal…vation” (A3); “pray ing”: CCEL page break (A4) |
| 74 | John 14:15–17 | 19 | 7 | misplaced headings §3, §4 (left empty), §5; “3.” “4.” “5.” in the prose (A3) |
| 75 | John 14:18–21 | 8 | 2 | — |
| 76 | John 14:22–24 | 7 | 4 | misplaced heading §3, “3.” in the prose (A3) |
| 77 | John 14:25–27 | 12 | 4 | misplaced heading §5, “5.” in the prose (A3) |
| 78 | John 14:27–28 | 5 | 2 | “servantform”, CCEL “servant-form” (A4) |
| 79 | John 14:29–31 | 12 | 3 | — |
| 80 | John 15:1–3 | 11 | 3 | “cornerstone”, CCEL “corner-stone” (A4) |
| 81 | John 15:4–7 | 5 | 4 | false heading §5 (A3) |
| 82 | John 15:8–10 | 12 | 2 | Greek accents stored in another Unicode form (same letters) (A4) |
| 83 | John 15:11–12 | 10 | 3 | Greek accents stored in another Unicode form (same letters) (A4) |
| 84 | John 15:13 | 8 | 3 | — |
| 85 | John 15:14–15 | 11 | 3 | — |
| 86 | John 15:15–16 | 16 | 3 | — |
| 87 | John 15:17–19 | 0 (not cleaned) | 0 (not cleaned) | **not cleaned**: CCEL page not read (HTTP 429). 11 numbers (1451–1461) and 3 pasted pieces remain; §5 holds only footnote text (A5) |
| 88 | John 15:20–21 | 10 | 4 | misplaced heading §3, “3.” in the prose (A3) |
| 89 | John 15:22–23 | 7 | 2 | “judg ments”: CCEL page break (A4) |
| 90 | John 15:23 | 2 | 1 | §3 checked by short quotes only (WebFetch would not copy it) |
| 91 | John 15:24–25 | 23 | 3 | — |
| 92 | John 15:26–27 | 7 | 2 | misplaced heading §2, “2.” in the prose (A3) |
| 93 | John 16:1–4 | 18 | 5 | “He saw”, CCEL “he saw”; “serv ice”: CCEL page break (A4) |
| 94 | John 16:4–7 | 10 | 3 | — |
| 95 | John 16:8–11 | 23 | 5 | “overmuch”, CCEL “over-much”; “inas much”: CCEL page break (A4) |
| 96 | John 16:12–13 | 15 | 5 | misplaced heading §5, “5.” in the prose (A3) |
| 97 | John 16:12–13 (second sermon on 16:12–13; A2) | 14 | 5 | “offhand” (made by the op; CCEL “off-hand”), “onlybegotten”, “everadvancing” (A4) |
| 98 | John 16:12–13 (third sermon on 16:12–13; A2) | 23 | 9 | misplaced heading §4, “4.” in the prose; false heading §9 (A3) |
| 99 | John 16:13 | 37 | 9 | misplaced heading §3, “3.” in the prose (A3); “creatureform” (A4) |
| 100 | John 16:13–15 | 7 | 4 | false heading §5 (A3); Greek accent encoding (A4) |
| 101 | John 16:16–23 | 18 | 5 | misplaced heading §6, “6.” in the prose (A3) |
| 102 | John 16:23–28 | 13 | 4 | misplaced heading §3, “3.” in the prose (A3) |
| 103 | John 16:29–33 | 2 | 1 | — |
| 104 | John 17:1 | 6 | 4 | false heading §4 (A3) |
| 105 | John 17:1–5 | 18 | 5 | — |
| 106 | John 17:6–8 | 10 | 5 | “onlybegotten”, “allpossessing” (A4) |
| 107 | John 17:9–13 | 7 | 3 | — |
| 108 | John 17:14–19 | 9 | 2 | “servantform” (A4) |
| 109 | John 17:20 | 20 | 5 | misplaced heading §4, “4.” in the prose (A3) |
| 110 | John 17:21–23 | 16 | 7 | “Onlybegotten” (A4) |
| 111 | John 17:24–26 | 26 | 7 | misplaced heading §3, “3.” in the prose (A3); “soldierservice” (A4) |
| 112 | John 18:1–12 | 10 | 3 | “ofttimes”, CCEL “oft-times” (A4) |
| 113 | John 18:13–27 | 18 | 5 | “con sider”: CCEL page break (A4) |
| 114 | John 18:28–32 | 7 | 5 | misplaced heading §5 (left empty), “5.” in the prose; false heading §6 (A3); §4–5 checked by short quotes only |
| 115 | John 18:33–40 | 13 | 4 | — |
| 116 | John 19:1–16 | 12 | 3 | — |
| 117 | John 19:17–22 | 19 | 4 | — |
| 118 | John 19:23–24 | 13 | 4 | “perse cuted”: CCEL page break (A4) |
| 119 | John 19:24–30 | 14 | 6 | false headings §7 (left empty) and §8; running head “1-9.” (A3) |
| 120 | John 19:31–42; 20:1–9 | 14 | 3 | misplaced heading §9, “9.” in the prose; running head “1-9.” ×3 (A3); “healthgiving” (A4) |
| 121 | John 20:10–29 | 4 | 4 | misplaced heading §4, “4.” in the prose; running head “1-11.” (A3); “connec tion”: CCEL page break (A4) |
| 122 | John 20:30–31; 21:1–11 | 23 | 8 | running head “1-11.” ×7; ten digits of Augustine’s count missing in §8 (A3); “wellknown” (A4); “re called”: CCEL page break (A4) |
| 123 | John 21:12–19 | 11 | 4 | “with out”: CCEL page break (A4) |
| 124 | John 21:19–25 | 26 | 9 | false heading §9 holding the line “Ten Homilies on the First Epistle of John.” (A3) |
| **Total** | **129 links** | **975** | **304** | |

## Every removed fragment, in full

Each fragment is shown between ⟦ ⟧, with the note’s words on each side as they stand at that op’s turn (a number shown nearby is removed by its own op). Joining the words on either side gives the text after the op, which the checkers compared with CCEL’s main text. The tag after the section says what the fragment holds. Line breaks inside a fragment are shown as ¶, and the direction marks the import put around Hebrew words are not shown. Where a removed footnote quotes the divine name, it is shown here as [the divine name, as printed].

Two removed footnotes carry words of Augustine that the translator moved out of the running text: 1845 (Tractate 115) and 1921 (Tractate 120). They are marked below. Nothing of the running text itself is removed.

### Tractate 49

Numbers removed (7): 1000–1006. Fragments removed: 6.

- §3, other note: …but the death is internal, because the evil thought⟦ every one who believeth rises again to life: if we reflect all, and understand, it is by a more horrible death that every sinner dieth.”⟧ had not yet ripened into action. The Lord intimated…
- §4, translator’s note: …so as to take up more thoroughly the necessary points.⟦ and some in more recent times. The time, place, and circumstances make it impossible for the incident here referred to, to be the same as that which took place in Bethany immediately before our Lord’s crucifixion. On that last occasion only was it Lazarus’ sister, Mary, who anointed Jesus. Luke here speaks only of a woman that was a sinner, and there is little evidence to connect her with any of the other Scripture women, even with Mary of Magdala, as is often done, and who is first mentioned by Luke in a different connection in the following chapter (viii. 2).—Tr.⟧ “Now a certain man was sick, [named] Lazarus, of…
- §11, other note: …somewhat obscurely, “He sleepeth;”—therefore He said⟦ Isidorus, and others think the optiones were so called ab optando, as being doubtless chosen as assistants to the decuriones and military adjutants. They were also attached to various offices: and hence there were artisan optiones, and those belonging to official or prison life, in which last signification they are used here; as also in Ambrose’s works (Commentary on the Ephesians, chap. 4) in these words: “Nor did Paul and Silas delay to baptize the jailor (optionem carceris).”⟧ plainly, “Lazarus is dead. And I am glad for your…
- §15, translator’s note: …He is not the God of the dead, but of the living; for⟦ form of spiritual death referred to before.—Tr.⟧ all live unto Him.” Believe then, and though thou…
- §26, other note: …the city of God and the temple against the Romans;⟦ 1000 Institis: Gr. κειρίαις. 1001 Matt. xvi. 19. 1002 Matt. viii. 12.⟧ just because they had a feeling that Christ’s…
- §28, references: …with an example of living, by which He might make it⟦ 1003 Luke i. 8, 9. 1004 Ex. xxx. 7. 1005 Matt. xv. 24. 1006 Chap. x. 16.⟧ manifest that it was no sin in His believing ones,…

### Tractate 50

Numbers removed (20): 1007–1026. Fragments removed: 7.

- §3, references: …for Him, with the intent that neither they nor we⟦ 1007 Isa. liii. 7. 1008 Ex. xii. 22, 23.⟧ should have Him more: but in departing from them, He…
- §6, references: …Jesus, and wiped His feet with her hair; and the house⟦ 1009 Ps. xl. 14. 1010 Ps. cxlii. 4, marg. 1011 Matt. xxviii. 20.⟧ was filled with the odor of the ointment.” Such was…
- §7, translator’s note: …We, indeed, are not so; but He is sufficient, who⟦ 1012 The full expression is nardi pistici pretiosi: Gr. “νάρδου πιστικῆς πολυτίμου:” πιστικός from πίστις, trustworthy, hence, genuine, pure;—though Aug. seems to indicate that it may also have had a geographical reference.—Tr. 1013 Rom. i. 17. 1014 Matt. xxv. 40. 1015 Rom. ii. 24. 1016 Song of Sol. i. 3. 1017 Cor. ii. 14–16.⟧ is pleased to speak by us what it may be for your…
- §9, references: …poor; but because he was a thief, and had the money⟦ 1018 Phil. i. 16, 18.⟧ bag, and bare1019 what was put therein.” Did he bear…
- §11, translator’s note: …unto by angels, save to intimate that His Church was⟦ 1019 “ἐβάσταζεν,” as used by John, may signify here, carried, bore, in a good sense; or carried off as a thief: for the latter sense, see chap. xx. 15.—Tr. 1020 Acts i. 26. 1021 Cor. xi. 29.⟧ destined thereafter to have her repository for money?…
- §12, translator’s note: …shalt thou be with me in paradise.” But if thou⟦ 1022 Augustin’s words, sinite illam, ut in diem sepulturæae meæ servet illud, as rendered above, differ considerably from those of our English version, and are more difficult to understand; but they agree with by far the larger number of Greek mss., which read, ῎Αφες αὐτὴν ἵνα εἰς τὴν ἡμέραν τοῦ ἐνταφιασμοῦ μου τηρήσῃ αὐτό. Our English version, “Let her alone: against the day of my burying hath she kept this,” is taken from mss. which omit ἵνα, and have τετήρηκεν instead of τηρήσῃ.—Tr. 1023 Matt. xvi. 19. 1024 Luke xxiii. 43.⟧ livest wickedly, thou mayest seem to have Christ now,…
- §14, references: …Lord of His power? If you think a dead man one thing,⟦ 1025 Matt. xxviii. 20. 1026 Acts i. 3, 9, 10.⟧ a murdered man another, look you only to this, that…

### Tractate 51

Numbers removed (23): 1027–1049. Fragments removed: 6.

- §2, translator’s note: …to be an interjection, expressive of angry feelings.⟦ 1027 Cor. ii. 15. 1028 Obsecrantis, literally suppliant, which is scarcely suitable to the context. 1029 The “some” here referred to by Augustin could scarcely have had a very extensive knowledge of the Hebrew language, as the word Hosanna, though left untranslated, as a well-known exclamation of the Jews in their religious services, is part of the same quotation from Psalm cxviii. (see vers. 25, 26) with the words that follow in the text. The sacred writers gave the nearest equivalent in Greek letters (῾ωσαννά, Hosanna) of the Hebrew  הֹושִׁיעה נָּאSave now!—Tr. 1030 In text, in lingua latina. 1031 Raca (Syriac ָרָקא, Chaldee רֵיקָא, Hebrew רֵיק, empty) was an insulting epithet of common use from an early period among the Babylonians, and in our Lord’s day among the inhabitants of Syria and Palestine.⟧ ¶ `## §3 ^s3`
- §5, translator’s note: …behold, thy King cometh, sitting on an ass’s colt.”⟦ It exactly answers to our idiot, or numskull, and is of frequent occurrence afterwards in the same sense in rabbinical writings.—Tr. 1032 Gen. xix. 24. 1033 Chap. v. 43. 1034 Phil. ii. 8. 1035 Matt. xxi. 1–16; Mark xi. 1–11; Luke xix. 29–48.⟧ Among that people, then, was the daughter of Zion to…
- §8, other note: …some one supposes here that He spake of Himself as⟦ 1036 Turba turbavit turbam.⟧ glorified, because the Gentiles wished to see Him.…
- §10, references: …with the answer, “Get thee behind me, Satan; for it⟦ 1037 Rom. xi. 25. 1038 Ps. cviii. 5.⟧ is written, Thou shalt not tempt the Lord thy God.”…
- §12, references: …to steal of its contents, yet it was he also⟦ 1039 Matt. iv. 7. 1040 Chap. xxi. 18, 19. 1041 Pet. ii. 21.⟧ who provided what was needful for the meal.1042 And…
- §12, translator’s note: …therefore, is the servant of Christ in the same way⟦ 1042 Chap. xii. 2–6. There is no ground in these verses for Augustin’s notion that the expense of that supper was defrayed out of the funds in Judas’ keeping. The whole account leaves the impression that it was provided by Lazarus and his sisters, although strictly speaking, ἐποίησαν (ver. 2) leaves it undetermined.—Tr. 1043 Chap. xiii. 27, 29. 1044 Phil. ii. 21. 1045 John ii. 6. 1046 Matt. vi. 3. 1047 Matt. xxv. 40. 1048 Rom. x. 4. 1049 Matt. xx. 28.⟧ as Christ also is a servant. And he that serveth…

### Tractate 52

Numbers removed (24): 1050–1073. Fragments removed: 7.

- §2, translator’s note: …saying, Thou shalt follow me the better, because⟦ 1050 The word anima used here, and frequently elsewhere, and corresponding to the Greek ψυχή, denotes “human life,” in reference to its internal principle or substance; and differs from “vita” (Gr. ζωή), as in the words following above, “unto eternal life” (vitam), which expresses rather the general idea of life in its existence, aggregate qualities, and duration. Our English word “soul,” which best corresponds with anima, is, however, more restricted in the idea which it popularly suggests; and hence, as in our English version of the Scriptures, the apparent confusion, which is unavoidable, in translating anima sometimes by “soul” and sometimes by “life.”—Tr. 1051 Chap. xi. 33: literally, as in margin of English Bible, “He troubled Himself.”⟧ it is to aid thy power of endurance that I thus…
- §3, references: …He said concerning him, “Another shall gird thee, and⟦ 1052 Matt. iv. 1–10. 1053 Matt. xxvi. 38, 39.⟧ carry thee whither thou wouldest not,” because He…
- §6, other note: …judgment in the end is reserved, when the living and⟦ 1054 Chap. xxi. 18, 19. 1055 Or, discernment, discretio; see Tract. XLIII. sec. 9. 1056 Ps. xliii. 1. 1057 Ps. xxxvi. 6. 1058 Rom. xi. 33.⟧ the dead shall at last be judged. The devil,…
- §8, references: …widowed Anna knew by the Holy Spirit the infant Lord;⟦1060 1059 Chap. vii. 39. 1060 Luke ii. 25–38.⟧ and that Zacharias and Elisabeth uttered by the Holy…
- §10, references: …prince of this world;” that is, the prince of all the⟦ 1061 Luke i. 41–45, 67–69. 1062 Acts ii. 4–6. 1063 Thess. v. 8. 1064 John ii. 1, 2. 1065 Matt. vi. 12, 13. 1066 Ps. cxxvii. 1.⟧ wicked who inhabit this world. The world is also…
- §12, translator’s note: Rejoins “understanding”. …23). Retaining this, therefore, in their minds, and un⟦1067 Cor. v. 19. 1068 There are here two readings in the Greek mss., πάντας (all men), and πάντα (all things), of which the former seems now the better approved; but the latter is that adopted by Augustin and the Vulgate.—Tr. 1069 Thess. iii. 2. 1070 Luke xxi. 18. 1071 Chap. x. 28. ⟧derstanding what He now said, “When I am lifted up…
- §14, other note: …but derogated not in aught from His own authority.⟦ 1072 Modicum lumen. 1073 Pet. ii. 6–8.⟧¶

### Tractate 53

Numbers removed (29): 1074–1094, 1096–1103. Fragments removed: 6.

- §5, references: …He goes on to say, “Therefore they could not believe,⟦ 1074 Cor. iii. 7.⟧ because that Isaiah said again, He hath blinded their…
- §6, translator’s note: …if the judgments of the saints are righteous, how much⟦ 1075 Rom. xi. 7; Isa. vi. 10; “spirit of remorse,” as in margin of English Bible, where the text has “blindness.”—Tr. 1076 Rom. ix. 14.⟧ more those of the sanctifying and justifying God?…
- §8, references: …the prayer that says, “Lead us not into temptation;”⟦ 1077 Rom. xi. 33. 1078 Ps. xxxvi. 6. 1079 Ecclus. iii. (21). 1080 Matt. x. 26. 1081 Phil. iii. 15, 16. 1082 Col. ii. 3. 1083 Chap. xvi. 12.⟧ and, on the other hand, let no one deny the freedom…
- §10, references: …to the powers of their own will, that they deny⟦ 1084 Matt. vi. 13. 1085 Luke xxii. 32. 1086 Chap. i. 12. 1087 Gal. v. 6. 1088 Rom. xii. 3. 1089 Cor. i. 31. 1090 Rom. x. 3. 1091 Tim. ii. 13.⟧ their need of the divine assistance in order to a…
- §11, references: …submitted themselves unto the righteousness of God.”⟦1097 1092 Rom. iv. 5. 1093 Luke xix. 10. 1094 Chap. xv. 5. 1095 Ps. lxxx. 7. 1096 Luke xxiii. 34. 1097 Rom. x. 2, 3.⟧ ¶ `## §12 ^s12`
- §13, references: …on the foreheads of those who believed on Him, on that⟦ 1098 Ex. xxxiii. 13. 1099 John iii. 2. 1100 Chap. x. 30. 1101 Phil. ii. 7. 1102 Matt. v. 8. 1103 Gal. vi.⟧ ¶ `## §14 ^s14`

### Tractate 54

Numbers removed (15): 1104–1118. Fragments removed: 5.

- §2, other note: …on Him as the Father, must believe that He has⟦ 1104 Jas. iv. 6. 1105 Chap. viii. 28. 1106 Chap. vii. 16. 1107 Tract. XXIX., haberet a quo esset.⟧ a Son; and in this way, he that believeth on the…
- §3, references: …apostle might say, He that receiveth me, receiveth Him⟦ 1108 Chap. i. 12. 1109 Chap. x. 34; Ps. lxxxii. 6. 1110 Rom. iv. 5.⟧ that sent me; or, He that heareth me, heareth Him…
- §5, references: Rejoins “understand”. …unto the Son;” namely, that thereby we are to under⟦1111 Matt. x. 40. 1112 Chap. xiv. 1. 1113 Matt. v. 14–16. 1114 Chap. v. 22. ⟧stand, It is not now that I judge him. And why not…
- §7, references: …separating the Son from the Father as to admit of any⟦ 1115 Ps. ci. 1. 1116 Rom. ii. 12.⟧ intervening air, to give effect, by its percussion,…
- §8, other note: …begat the Truth. What, then, could He now say to the⟦ 1117 Chap. v. 26. 1118 Verax.⟧ Truth? For the Truth had no imperfection to be…

### Tractate 55

Numbers removed (15): 1119–1133. Fragments removed: 5.

- §1, translator’s note: …from the world, and another to pass away with it; one⟦ 1119 Transitus, transit, pass over.—Tr. 1120 Ex. xiv. 29. A curious mistake of Augustin’s to derive the name of the feast from Israel’s passing over the Red Sea, instead of [the divine name, as printed]’s passing over the houses of the Israelites, when He smote the firstborn of Egypt! Compare Ex. xii. 11, 13, 23, 27.—Tr. 1121 Isa. liii. 7. 1122 Ex. xii. 23. 1123 Col. i. 13.⟧ thing to pass to the Father, another to pass to the…
- §3, references: …certainly that the supper was not yet over, or, in⟦ 1124 Rom. x.⟧ ¶ `## §4 ^s4`
- §4, translator’s note: `## §4 ^s4` ¶ ⟦1125 Cor. v. 7. 1126 That is, “applies to Christ’s humanity, not His divinity.”—Tr. 1127 Luke xvi. 27, 28. 1128 Chap. xv. 13. 1129 Cœna facta; δείπνου γενομένου. See Augustin’s explanation below.—Tr. ⟧other words, that there was still bread on the table.…
- §6, references: …mark the meaning of the evangelist; because that, when⟦ 1130 Eph. vi. 12.⟧ about to speak of the pre-eminent humility of the…
- §7, translator’s note: …him now, when found, imitate the Redeemer’s humility.⟦ 1131 Literally, “emptied Himself,” as in the Greek.—Tr. 1132 Phil. ii. 6, 7. 1133 Luke xix. 10.⟧¶

### Tractate 56

Numbers removed (11): 1134–1144. Fragments removed: 3.

- §2, translator’s note: …withhold the lowest, but I lay the foremost also at⟦ 1134 It is curious to notice how Augustin here contradicts his previous and natural explanation of the passage, in order to uphold the primacy of Peter. It looks as if here he suddenly felt that his former words were rather adverse to the notion.—Tr.⟧ Thy disposal. Deny me not having a part with Thee,…
- §4, translator’s note: …is, even to our feet wherewith we walk on the earth.⟦ 1135 Of course, it is a mere elegance in the Latinity to which Augustin here refers, as between præter pedes and nisi pedes, when qualifying the expression, “Mundus est totus” (he is all clean).—Tr. 1136 Of course, it is a mere elegance in the Latinity to which Augustin here refers, as between præter pedes and nisi pedes, when qualifying the expression, “Mundus est totus” (he is all clean).—Tr. 1137 Of course, it is a mere elegance in the Latinity to which Augustin here refers, as between præter pedes and nisi pedes, when qualifying the expression, “Mundus est totus” (he is all clean).—Tr. 1138 John i. 8. 1139 Rom. viii. 34. 1140 Matt. vi. 12. 1141 John i. 9.⟧ ¶ `## §5 ^s5`
- §5, references: …will be present to enable us also to pay our debts.⟦ 1142 Eph. v. 26, 27. 1143 Song of Sol. v. 3. 1144 Col. iii. 1, 2.⟧ V. 2, 3.

### Tractate 57

Numbers removed (27): 1145–1171. Fragments removed: 4.

- §2, other note: …He also says: “Open to me, my sister, my nearest, my⟦ 1145 Rom. xiii. 8. 1146 Col. iii. 1, 2. 1147 Acts ix. 4. 1148 Matt. vi. 12. 1149 Chap. xiii. 5. 1150 Rom. viii. 34. 1151 Ps. xlv. 2. 1152 Patruelis, literally cousin (by the father’s side).⟧ V. 2,
- §3, references: …instrument, those who do so may fear to defile their⟦ 1153 Song of Sol. v. 2, 3. 1154 Matt. xxviii. 20. 1155 Chap. i. 51. 1156 Phil. i. 23, 24. 1157 Eph. iii. 17. 1158 Cor. ix. 27. 1159 Jas. i. 19. 1160 Ps. li. 8. 1161 Chap. iii. 29.⟧ V. 2, 3. feet, when they aim at pleasing men with the…
- §4, other note: …to open? and how shall they hear without a preacher?⟦1168 1162 Ps. xlvi. 10. 1163 Ecclus. xxxviii. 24. 1164 Two readings, affectibus or affatibus. 1165 Matt. x. 27. 1166 Matt. xxiv. 12. 1167 Cor. xi. 3. 1168 Rom. x. 14.⟧ V. 2, 3.
- §6, references: …washed, and may your prayers find acceptance with God.⟦ 1169 Jas. iii. 1, 2. 1170 Matt. vi. 12. 1171 Ps. li. 8.⟧¶

### Tractate 58

Numbers removed (13): 1172–1184. Fragments removed: 4.

- §3, references: …profit is ours to be the subjects of such loftiness,⟦ 1172 Prov. xxvii. 2.⟧ the servants of the truth. That He calls Himself Lord…
- §4, other note: …we have here of humility: and brethren do this to one⟦ 1173 Sæcularis. 1174 Cicero, in Q. Cæcilium. 1175 Cicero, de Oratore. 1176 Cor. xii. 6. 1177 Cor. i. 31. 1178 Ps. xxxiv. 2.⟧ another in turn, even in the visible act itself, when…
- §5, translator’s note: …if He forgives us, whom we have nothing to forgive;⟦ 1179 Tim. v. 10. 1180 Dan. iii. 88; that is, in the apocryphal piece called “The Song of the Three Children,” and which, as it has no place in the Hebrew Scriptures, is also omitted in our English version. Its place would fall between the 23d and 24th verses of chap. iii.—Tr. 1181 Matt. vi. 12. 1182 Rom. viii. 34. 1183 Jas. v. 16.⟧ how much more ought we, who are unable to live here…
- §5, references: …that is, loose on earth, may be loosed in heaven.⟦ 1184 Col. iii. 13.⟧¶

### Tractate 59

Numbers removed (6): 1185–1190. Fragments removed: 2.

- §2, translator’s note: …may God forbid!) we shall be adopting, in the Arian⟦ 1185 Chap. vi. 70. 1186 Cor. xi. 29. 1187 A modo; Greek, ’Απ’ ἄρτι; margin of English Bible, “From henceforth.”—Tr.⟧ fashion. For they, when they hear or read these words…
- §3, references: …he may give heed to Him who sent Him. If, then, thou⟦ 1188 Chap. x. 30. 1189 Ps. xix. 5. 1190 Chap. i. 14.⟧ lookest for Christ in Peter, thou wilt find the…

### Tractate 60

Numbers removed (11): 1191–1201. Fragments removed: 3.

- §2, translator’s note: …yet transform the body of our humility into similarity⟦ 1191 Chap. xiii. 18, 10, 11. 1192 Chap. vi. 71. 1193 Chap. xii. 27. 1194 Chap. x. 18. 1195 Phil. iii. 21. The text has transfiguravit (pret.), “hath transformed,” in this as well as in the next clause, “hath transferred,” but here it is evidently a misprint for transfigurabit (fut.).—Tr.⟧ of form with the body of His glory, hath also…
- §4, other note: …Him; lest His own words should convince us of⟦ 1196 Cor. i. 20. 1197 Ps. xciv. 11. 1198 Phil. i. 23. 1199 Gaudium, non lætitia.⟧ the contrary when He says, “My soul is sorrowful,…
- §5, references: …our human feelings whenever He judged it becoming.⟦ 1200 Matt. xxvi. 38. 1201 Chap. xi. 33, margin.⟧¶

### Tractate 61

Numbers removed (8): 1202–1209. Fragments removed: 3.

- §3, references: …towards each other. Each one’s own conscience was⟦ 1202 John ii. 19.⟧ known to himself; but as he was ignorant of his…
- §5, references: …underlying these words, and having reference to the⟦ 1203 Chap. xxi. 20–24. 1204 Matt. ix. 9. 1205 Ex. vi. 1. 1206 Cor. xii. 2.⟧ bosom on which the narrator was leaning. For what…
- §6, translator’s note: …than remains to us now at the close of this discourse.⟦ 1207 The original mss. give different readings of this verse. That followed by our English version is supported by the Codd. Alex. and Cantabr., which read, Νεύει οὖν τούτῳ Σίμων Πέτρος πυθέσθαι τίς ἂν εἴη περὶ οὗ λέγει. The Latin version used by Augustin reads, Innuit ergo Simon Petrus, et dicit ei, Quis est de quo dicit, and approaches nearly to that found in the Codd. Vat. and Ephr., which read, Νεύει οὗν τούτῳ Σ. Π., καὶ λέγει αὐτῷ, Εἰπὲ τίς ἐστιν περὶ οὗ λέγει—“Simon Peter therefore beckons to this one, and says to him, Say [ask], who is it of whom He speaks?” Of the early versions, the Syriac adopts the former, while the Vulgate resembles the latter. The Sinaitic gives a fuller reading, compounded of both the others. There is thus some doubt as to the original text; but the latter has some special arguments of an internal kind in its favor: such as the consideration that, from its peculiar and somewhat redundant form, it could hardly have been substituted in place of the former, which is smoother and more elegant, while the converse is perfectly supposable; and also the weighty fact that John nowhere else makes use of the optative mood, as he would here (τίς ἂν εἴη), if the former reading—that followed by our English version—were the true one.—Tr. 1208 Wisd. of Sol. ii. 1. 1209 Pectoris sinus; the hollow, the inmost part of the breast.⟧¶

### Tractate 62

Numbers removed (11): 1210–1220. Fragments removed: 3.

- §1, references: …evidence of the grace he had treated with ingratitude?⟦ 1210 Rom. vii. 13. 1211 Cor. xii. 7–9. 1212 Cor. xi. 27.⟧ ¶ `## §2 ^s2`
- §4, references: …loved the Church, and gave Himself for it. And as the⟦ 1213 Luke xxii. 3, 4. 1214 Luke xxii. 19–21. 1215 Rom. iv. 25. 1216 Eph. v. 25.⟧ apostle also says of himself: “Who loved me, and gave…
- §6, references: …them now, to defer them till a future occasion.⟦ 1217 Gal. ii. 20. 1218 Matt. vi. 34. 1219 Tim. v. 16. 1220 Ps. xix. 2.⟧¶

### Tractate 63

Numbers removed (8): 1221–1228. Fragments removed: 2.

- §2, references: …the Lord? What says the day when the night had gone⟦ 1221 Ps. lxix. 32. 1222 Ps. cv. 4. 1223 Tim. iii. 7. 1224 Ecclus. xviii. 7.⟧ out? What says the Redeemer when the seller had…
- §2, references: …if they were the things signified, the Lord makes use⟦ 1225 Chap. vii. 39. 1226 Matt. xiii. 43. 1227 Cor. x. 4. 1228 Matt. xiii. 38.⟧ of the words, “Now is the Son of man glorified;”…

### Tractate 64

Numbers removed (7): 1229–1235. Fragments removed: 4.

- §2, references: …not be able to come? And where, then, is the place of⟦ 1229 Acts i.⟧ ¶ `## §3 ^s3`
- §3, references: `## §3 ^s3` ¶ ⟦1230 Matt. xxviii. 20. 1231 Ps. xc.¶⟧`## §4 ^s4`
- §4, translator’s note: …at that time less able to follow the Lord to death,⟦ 1232 Chap. xvii. 24. 1233 Luke xxiv. 44. 1234 Scarcely an admissible use of the “now” (ἄρτι), which manifestly refers to the time of Jesus saying so to the disciples, and not to the period of their inability to come.—Tr.⟧ but they were less able to follow Him to the life…
- §4, references: …thereon must be put off till another opportunity.⟦ 1235 Rom. vi. 9.⟧¶

### Tractate 65

Numbers removed (10): 1236–1245. Fragments removed: 4.

- §1, translator’s note: …wherewith He loved them, when about to lead them on to⟦ 1236 Lev. xix. 18. 1237 Song of Sol. viii. 5, where Augustin, in dealbata, follows the Septuagint in their misreading and alteration of the original םִן־הַמִּדְבָּר, “from the wilderness” (as in chap. iii. 6), into  מִחְבָּרֶרֶח,מִחְלַבֶּנֶח, or some such participle. The Vulgate differs from Augustin, and reads correctly, de deserto, but interposes between this and the next clause another participial expression, deliciis affuens, abounding in delights. Our English version follows the original.—Tr. 1238 Cor. xii. 25, 26.⟧ the goal where all sufficiency should be theirs, and…
- §2, references: …did He love us, that we also should love one another;⟦ 1239 Ps. ciii. 5. 1240 Cor. xv. 28. 1241 Col. iii.⟧ ¶ `## §3 ^s3`
- §3, references: `## §3 ^s3` ¶ ⟦1242 Song of Sol. viii. 6. 1243 Matt. xxii. 37–40. ⟧bestowing this on us by His own love to us, that we…
- §3, translator’s note: …commencement in dealing with the words that follow.⟦ 1244 Cor. xiii. 1–3. 1245 Song of Sol. vii. 6, according to the Septuagint. It is very doubtful, however, whether the LXX. themselves held the meaning drawn from their version by Augustin. It seems all to depend on where they inserted the point of interrogation (;); and the mss. vary. The Vatican, that in common use, places it after ἀγάπη (love), which could hardly have been Augustin’s reading. Other mss. place it at the end of the verse, making the whole a single sentence, as in our English version. Augustin must have found the point immediately after ἡδύνθης (“thou art pleasant”), thus disjoining ἀγάπη from what precedes, and making it, with ἐν τρυφαῖς σου, a clause by itself. The Masoretic punctuation of the Hebrew gives some grounds for Augustin’s reading: for there is a larger disjunctive accent over “( נעמהthou art pleasant”), indicating the central pause of the verse; while the minor disjunctive under  אהבהmay only be intended to make up by emphasis for the abruptness of the language.—Tr.⟧¶

### Tractate 66

Numbers removed (6): 1246–1251. Fragments removed: 2.

- §2, other note: …Christ; and so denies Him in respect of what He became⟦ 1246 See Ambrose, on Luke xxii.⟧ on our account, that the nature He had given us might…
- §2, references: …home the lesson to ourselves, that no man should place⟦ 1247 Tim. ii. 5. 1248 Rom. v. 19. 1249 Cor. xv. 21, 22. 1250 Chap. xx. 27, 28. 1251 Matt. xxvi. 34, 69–74, and Luke xxii. 55–60.⟧ his confidence in human strength. For what else had…

### Tractate 67

Numbers removed (9): 1252–1260. Fragments removed: 2.

- §2, other note: …glory; and so also the resurrection of the dead. The⟦ 1252 A few of the mss. have “ye believe,” after the Vulgate: the Greek verb also, πιστεύετε which occurs twice in this clause, is doubtful, signifying, ye believe, or, believe (imperative).—Migne. 1253 Phil. ii. 6, 7. 1254 Chap. xiii. 38. 1255 Matt. xx. 9.⟧ saints, like the stars in the sky, obtain in the…
- §4, references: Rejoins “receivest”. …Thy people shall dwell with Thyself? Or if Thou re⟦1256 Cor. xv. 41, 42, 28. 1257 John iv. 8. 1258 Cor. v. 1. 1259 Ps. lxxxiv. 4. 1260 Matt. vi. 9. ⟧ceivest them unto Thyself, how wilt Thou come again,…

### Tractate 68

Numbers removed (15): 1261–1275. Fragments removed: 3.

- §1, translator’s note: …what is yet to be.” Therefore He has both made such⟦ 1261 The apparent contrariety that Augustin here deals with, partly arises from a mistaken interpretation of the second half of verse 2, as given above. His Latin version read, si quo minus, dixissem vobis quia vado, etc., and is a close verbal rendering of the original text, as found in several mss.,—εἰ δὲ μὴ, εἶπον ἂν ὑμῖν, ὅτι πορεύομαι,—although some others omit the ὅτι. But while verbally exact, grammatical accuracy and a fair exegesis will admit of a pause after ὑμῖν (vobis), as the general sense of the passage requires. ῞Οτι might thus be used in the sense of “because;” or, as it often is, as a particle introducing a direct statement.—Tr. 1262 Isa. xlv. 11, according to the Septuagint, whose reading, as usual, is followed by Augustin, although here a very manifest mistranslation of the Hebrew. The words are, “Thus saith [the divine name, as printed], the Holy One of Israel (ויצּרו  )האיתות שאלוניand his Maker, Ask me of things to come,” etc. This is the rendering really in accordance with the usual Hebrew idiom, with the sense of the passage itself, and with the frequent use of Yotser (Maker) by Isaiah. It is that also approved by the Masoretic pointing, and followed generally by the other translations, including the Vulgate, which has: plastes ejus: ventura interrogate me, etc. The LXX., however, make ha’othiyyoth dependent on yots’ro (notwithstanding its own suffix), instead of the verb that follows, and reads, ὁ ποιήσας (αὐτὸν in some copies) τὰ ἐπερχόμενα, which Augustin renders in the text: qui fecit quæ futura sunt.—Tr.⟧ On the Same Passage. things and is yet to make them.…
- §2, references: …just as we now pray when we say, “Thy kingdom come.”⟦ 1263 Luke vi. 13. 1264 Eph. i. 4. 1265 Rom. viii. 30. 1266 Cor. iii. 17. 1267 Cor. xv. 23, 24. 1268 Matt. xiii. 24, 38–43. 1269 Matt. vi. 10.⟧ On the Same Passage. Even now, therefore, already is…
- §3, references: …a partaker of Thee, some less, some more, such will⟦ 1270 Matt. xxv. 34. 1271 Rom. i. 17. 1272 Cor. v. 6–8. 1273 Matt. v. 8. 1274 Acts xv. 9. 1275 Chap. xv.⟧ ¶ `## §4 ^s4`

### Tractate 69

Numbers removed (9): 1276–1284. Fragments removed: 3.

- §3, translator’s note: …and didst place Thyself not only before the carnal⟦ 1276 Chap. xvi. 10. 1277 Wisd. ix. 15. 1278 Ps. cxxiii. 1. 1279 Isa. vii. 9, according to LXX., which reads, ἐὰν μὴ πιστεύσητε, οὐδὲ μὴ συνῆτε. ּתֵאָמֵנז, however, will scarcely admit the meaning of “understand” (συνῆτε). There is a play in the Hebrew upon the verb אָמֵי, which is the one used in both clauses, first in the Hiphil, where it means to cleave fast to, to show a firm trust in; and secondly, in the Niphal, to be held fast, to be confirmed in one’s trust. Hence the rendering of our English Bible is more correct: “If ye will not believe, surely ye shall not be established.”—Tr. 1280 Phil. ii. 7.⟧ eyes, but even in the very hands of men. And how…
- §4, references: …of the Gospel; but your souls ought not to be burdened⟦ 1281 Rom. x. 10. 1282 Rom. iii. 4. 1283 Rom. vi. 9.⟧ with spiritual food, however pleasant, especially as…
- §4, references: …as the spirit is willing, but the flesh is weak.⟦ 1284 Matt. xxvi. 41.⟧¶

### Tractate 70

Numbers removed (3): 1285–1287. Fragments removed: 2.

- §2, references: …said, “Lord, show us the Father, and it sufficeth⟦ 1285 Chap. v. 26. 1286 Ps. xlii. 6.⟧ us.” And the Lord replied to him, “Have I been so…
- §2, translator’s note: …have known me, ye have known my Father also;” because⟦ 1287 That is, those who ascribed suffering to the Father; because the Sabellians, denying the distinct personality of the Son, and regarding Him as only a special revelation of God the Father, were chargeable, therefore, with holding that it was God the Father who really suffered and died on the cross.—Tr.⟧ it is I, who am the only way to the Father, that will…

### Tractate 71

Numbers removed (7): 1288–1294. Fragments removed: 2.

- §3, references: …and yet it was He that did both. Nevertheless, when He⟦ 1288 Chap. x. 30. 1289 Chap. v. 21, 19. 1290 Chap. xiii. 16. 1291 Ps. xviii. 1. 1292 Acts v. 15. 1293 Matt. xiv. 36.⟧ so spake, He was commending the efficacious power1294…
- §3, other note: …we are obliged to defer their further consideration.⟦ 1294 Opera.⟧ On the Same Passage.

### Tractate 72

Numbers removed (10): 1295–1304. Fragments removed: 3.

- §1, translator’s note: …rich man go away sad from His presence, when seeking⟦ 1295 Chap. xv. 5. 1296 That is, here, “without any self-originating aid of his,” as if he had any independent and meritorious share in the work. Augustin plays on the prepositions, per (eum), and præter (eum).—Tr. 1297 Ps. cxvi. 12.⟧ On the Same Passage. counsel about eternal life? He…
- §3, references: …Christ is certainly working in him, but not without⟦ 1298 Chap. xiv. 21. 1299 Matt. vii. 24. 1300 Chap. xi. 25. 1301 Rom. iv. 5. 1302 Phil. ii. 12.⟧ On the Same Passage. him; and one which I might,…
- §3, translator’s note: …a little delay for its consideration and discussion.⟦ 1303 Matt. xxiv. 35. 1304 Tim. iii. 16. On account of the well-known textual controversy among Biblicists, this passage, as quoted by Augustin, is so far valuable, as it shows us how he read and understood the point in dispute, namely, whether it is “God was manifested” (as in our English version), or, “Who [which] was manifested,” as here by Augustin; in other words, whether the original text read Θεός or ὅς before ἐφανερώθη. The evidence is almost equally divided between the two; and the difficulty is chiefly caused by the circumstance, that in the earliest mss., the Uncial, ΘΕΟΣ (God) is usually written in a contracted form, consisting of the first and last letters, ΘΣ, which differs from the pronoun ὅς (who), written ΟΣ, merely by the little line inside the Θ, and another line over the contraction; both of which may have been unintentionally omitted at the time of copying, or purposely inserted at an after date. To us now, the question is of less importance, as, if the true reading be ὅς (who), its antecedent can only be Χριστός (Christ). [The R.V., in accordance with the oldest mss. and the best critical edition, reads: “He who (ὅς) was manifested”—Tr.]⟧ Again on the Same Passage.

### Tractate 73

Numbers removed (10): 1305–1314. Fragments removed: 3.

- §1, references: …for a dish of pottage, that Esau lost his birthright.⟦ 1305 Jas. iv. 3. 1306 Num. xi. 32. 1307 Tim. iv. 4. 1308 Rom. xiv. 20. 1309 Gen. iii. 6. 1310 Gen. xxv. 34.⟧ Again on the Same Passage.
- §3, references: Leaves “salAgain on the Same Passage. vation” (A3). …through ignorance that is injurious to his sal⟦1311 Cor. xv. 10. 1312 Cor. xii. 8. ⟧Again on the Same Passage. vation, he asketh it not in…
- §4, references: …in the Son; for the Father and the Son are one.⟦ 1313 Gal. vi. 9. 1314 Matt. vi. 9–13.⟧¶

### Tractate 74

Numbers removed (19): 1315–1333. Fragments removed: 7.

- §1, translator’s note: …loveth not the Son, but some figment of his own⟦ 1315 Augustin has cognoscetis for the second “know,” and scit for that immediately preceding. The Greek text, however, has γινώσκω in both places, and in the present tense. He has also manebit et in vobis erit. The tense of μενει, whether present or future, depends simply on the place of the accent, μένει, or μενεῖ: while, as between the two readings ἐστὶν and žσται, the preponderance of ms. authority seems in favor of the latter, although the present γινώσκετε in the principal clause would be more naturally followed by an equally proleptic present in those which follow.—Tr. 1316 Rom. v. 5.⟧ imagination. And besides, this is the apostolic…
- §2, translator’s note: …Spirit], did He on that account fail in afterwards⟦ 1317 Or, “Jesus is Lord.” The weight of authority is clearly in favor of the reading followed by Augustin—λέγει, Κύριος ’Ιησοῦς, giving the direct utterance of the speaker; and not the indirect accusative, Κύριον ’Ιησοῦν, followed by our English version.—Tr. 1318 Cor. xii.⟧ ¶ `## §3 ^s3`
- §3, references: `## §3 ^s3` ¶ ⟦1319 Tit. i. 16. 1320 Cor. ii. 12. 1321 Chap. xx. 22. ⟧sending Him according to His promise? Or was it not…
- §3, references: …as God hath dealt to every man the measure of⟦ 1322 Acts ii.⟧ ¶ `## §4 ^s4`
- §4, references: `## §4 ^s4` ¶ ⟦1323 Kings ii. 9. 1324 Chap. iii. 34. 1325 Col. ii. 9. 1326 Tim. ii.¶⟧`## §5 ^s5`
- §5, references: `## §5 ^s5` ¶ ⟦1327 Luke iv. 18–21. 1328 Luke ii. 40. ⟧faith.”1329 Nor is it the Spirit Himself that is…
- §5, references: …in which He may be seen and known, unless He be in us.⟦ 1329 Rom. xii. 3. 1330 Cor. xii. 4. 1331 John ii. 1. 1332 Rom. viii. 7, marg. 1333 John ii. 16.⟧¶

### Tractate 75

Numbers removed (8): 1334–1341. Fragments removed: 2.

- §3, references: …as by man is death, by man also is the resurrection⟦ 1334 Ps. x. 14. 1335 Matt. ix. 15.⟧ of the dead. For as in Adam all die, even so in…
- §5, other note: …which follows, “and I will manifest myself to him.”⟦ 1336 Cor. xv. 21, 22. 1337 Cor. v. 7. 1338 John iii. 2. 1339 Rom. viii. 10. 1340 Chap. xv. 5. 1341 Separabiliter.⟧ “I will love, and will manifest;” that is, I will…

### Tractate 76

Numbers removed (7): 1342–1348. Fragments removed: 4.

- §2, references: …the one-minded to dwell [together] in a house. In this⟦ 1342 Ps. xliii. 1. 1343 Cor. xiii. 1–⟧ ¶ `## §3 ^s3`
- §3, translator’s note: `## §3 ^s3` ¶ ⟦1344 Unanimes. 1345 Ps. lxviii. 6: according to Augustin’s translation and adaptation of the words מֹושִׁיב יְחִירִים בַּיְתָה, and which the Vulgate has also rendered somewhat similarly, qui inhabitare facit unius moris in domo. The English version is rather more accordant with the context, “who setteth the solitary in families,” or rather, “who maketh the solitary [lit. those standing alone] to dwell in a house,” marg.; that is, if  יָחִירmight not even here retain its proper meaning of “only one,” and, hence “beloved one.” At all events, the word thus used, and its place in the context (see especially the preceding verse), may warrant the combination of both meanings,—that those who are “ones standing alone,” friendless, cast off from others, in a human sense, are יְחִירִים, “only ones,” “beloved ones” in the heavenly Father’s sight, to whom He extends a special protection, and provideth a home.—Tr. ⟧house Father and Son make their abode, and impart that…
- §4, references: …The Son doth not manifest Himself in such a way as⟦ 1346 Acts i. 11. 1347 John ii. 18.⟧ this to the world: for the world is spoken of in the…
- §5, references: …prerogative, that He is in all respects His equal.⟦ 1348 Chap. i. 1.⟧¶

### Tractate 77

Numbers removed (12): 1349–1360. Fragments removed: 4.

- §2, other note: …also speaking, where thou readest in the Acts of the⟦ 1349 Eam [Trinitatem] distincte audire, inseparabiliter intelligere. 1350 Ps. ii. 7. 1351 Chap. vi. 45. 1352 Matt. xxiii. 10.⟧ Apostles, that the Holy Spirit said to the blessed…
- §4, references: …that what is expressed once may have a reference⟦ 1353 Acts x. 20. 1354 Cor. iv.⟧ ¶ `## §5 ^s5`
- §5, references: `## §5 ^s5` ¶ ⟦1355 Eph. ii. 14. 1356 John iii. 2. 1357 Cor. v. 6, 7. ⟧to both? Or may it not be that here also we have some…
- §5, other note: …that we should be of one heart with Himself, having⟦ 1358 Matt. vi. 12. 1359 Rom. vii. 22, 23. 1360 Consors dicitur, qui sortem jungit—concors dicendus, qui corda jungit.⟧ our hearts run into one, that this one heart, set on…

### Tractate 78

Numbers removed (5): 1361–1365. Fragments removed: 2.

- §2, references: …For it is the servant-form which is that wherein⟦ 1361 Phil. ii. 6, 7. 1362 Chap. x. 30.⟧ the Son of God is less, not only than the Father, but…
- §3, translator’s note: …and thus Christ is God, a rational soul, and a body.⟦ 1363 Chap. i. 1, 14. 1364 The Eunomians were a branch of the Arians, only slightly differing in some of their tenets regarding the essential inferiority to God, and the creaturehood of the Son and the Holy Spirit. As a sect, they belong to the fourth century, and derived their name from Eunomius, bishop of Cyzicus.—Tr. 1365 Luke ii. 51.⟧ In all of these we confess Him to be Christ, we…

### Tractate 79

Numbers removed (12): 1366–1377. Fragments removed: 3.

- §1, other note: …it, and also could predict it before He did it: and⟦ 1366 Chap. xx. 29. 1367 Text, sperantium, although many mss. have sperandorum, or sperandarum, “things hoped for.” 1368 Convictio. 1369 Heb. xi. 1.⟧ this they should then believe, not with a new, but…
- §2, other note: …us into the kingdom of the Son of His love.”⟦ 1370 Defecta—refecta. 1371 Defecta—refecta. 1372 Jas. iv. 4. 1373 Chap. i. 10. 1374 Eph. vi. 12: Augustin, rectores mundi tenebrarum harum; original, τοὺς κοσμοκράτορας τοῦ σκότους τούτου. 1375 Eph. v. 8. 1376 Col. i. 12, 13.⟧ And in Him the prince of this world, that is, of this…
- §2, references: …Son of God was endowed by nature, and not by robbery.⟦ 1377 Ps. lxix. 4.⟧¶

### Tractate 80

Numbers removed (11): 1378–1388. Fragments removed: 3.

- §2, translator’s note: …says, “Now ye are clean through the word which I have⟦ 1378 Tim. ii. 5. 1379 Hebrew סוּרֵי, pass. part. of רוּס, to depart [from God], and so, perhaps, “stragglers,” i.e. “straggling branches of [a strange vine];” or, as in English version, “degenerate branches,” rather than as in text, where Augustin gives, in amaritudinem, vitis aliena, following the LXX., which reads, “εἰς πικρίας ἡ ἄμπελος ἡ ἀλλοτρία.” The Vulgate is better: in pravum, vinea aliena.—Tr. 1380 Jer. ii. 21. 1381 Isa. v. 4. 1382 Chap. xiv. 28.⟧ spoken unto you.” Here, you see, He is also the…
- §3, references: …and, says the blessed Peter in his epistle, “Even⟦ 1383 Cor. iii. 5–7. 1384 Chap. xiii. 10. 1385 Rom. x. 10. 1386 Acts xv. 9.⟧ as baptism doth also now save us, not the putting…
- §3, other note: …clean through the word which I have spoken unto you.”⟦ 1387 Literally, “questioning,” interrogatio, Pet. iii. 21. 1388 Eph. v. 25, 26.⟧¶

### Tractate 81

Numbers removed (5): 1389–1393. Fragments removed: 4.

- §3, references: …abideth in me, and I in him, the same bringeth forth⟦ 1389 Rom. x. 3. 1390 Tim. iii. 8.⟧ much fruit; for without me ye can do nothing.” For…
- §4, references: …it draws not its life from the root. It is to this⟦ 1391 Ezek. xv.⟧ ¶ `## §5 ^s5`
- §5, references: `## §5 ^s5` ¶ ⟦1392 Matt. vi. 9. ⟧distinction that the word of Scripture has respect,…
- §5, references: …purpose of being judged according to them at last.⟦ 1393 Ps. ciii. 18.⟧¶

### Tractate 82

Numbers removed (12): 1394–1405. Fragments removed: 2.

- §2, other note: Rejoins “Father”. …He is pointed out as Mediator when He says, “The Fath⟦1394 Clarificatus, literally, “clarified,” or made bright, clear, to men’s eyes. See immediately afterwards in text. 1395 Rom. iv. 2. 1396 Tract. LXXXI. sec. 2. 1397 Matt. v. 16. 1398 Eph. ii. 10. 1399 Gal. v. 6. 1400 John iv. 19. 1401 Tim. ii. 5. ⟧er—me, and I—you.” For the Father, indeed, also loveth…
- §4, other note: …the Word was made flesh, and dwelt among us.⟦ 1402 Non in quantum Deus, sed in quantum homo est. 1403 Luke ii. 52. 1404 Ps. iii. 3. 1405 Chap. i. 1, 14.⟧¶

### Tractate 83

Numbers removed (10): 1406–1415. Fragments removed: 3.

- §2, other note: …or commandment, both are the rendering of the same⟦ 1406 Chap. xiii. 8. 1407 Eph. i. 4. 1408 Præceptum, sive mandatum.⟧ Greek word, entolé (ἐντολή). But He had already made…
- §3, translator’s note: …but hateth his own soul. Let us, therefore, be holding⟦ 1409 See Tract. LXV. 1410 Chap. xiii. 34. 1411 Cor. xiii. 13. 1412 Rom. xiii. 10. 1413 Jas. ii. 19. 1414 Ps. xi. 5. Augustin here, as usual, along with the Vulgate, follows the Septuagint in what is clearly a mistranslation of the Hebrew text, which is correctly rendered grammatically in our English version, though not exactly according to the Masoretic punctuation. ( שָֽׂנְאָהfem.) shows that “his soul” is the subject, and not the object of the hatred.—Tr.⟧ fast to this precept of the Lord, to love one…
- §3, references: …their love one to another, that God may be all in all.⟦ 1415 Cor. xv. 28.⟧¶

### Tractate 84

Numbers removed (8): 1416–1423. Fragments removed: 3.

- §2, other note: …and die we must, however unwilling: He, by dying,⟦ 1416 John iii. 16. 1417 Prov. xxiii. 1, 2: see below, and also Tract. XLVII. sec. 2, note 4. 1418 Pet. ii. 21. 1419 Chap. x. 18.⟧ straightway slew death in Himself; we, by His death,…
- §2, translator’s note: …which is human; “if thou turn it upon Him, He will⟦ 1420 Acts ii. 31. 1421 This parenthesized sentence is found, according to Migne, inserted here in six mss. In three others it occurs immediately before the second following sentence, beginning, “But if any one,” etc. In other mss. it is wanting; and Migne omits it from the text.—Tr.⟧ nowhere be visible,” because He cannot be seen with…
- §2, translator’s note: …to presume on a comparison between Him and ourselves.⟦ 1422 The whole of this passage, taken from Proverbs xxiii. 3–5, as well as verses and 2, quoted in sec. of this Lecture, and in Tract. XLVII. sec. (where see note 4), departs so widely from the Hebrew text, and even from the Septuagint (which is itself considerably astray), that it is hardly possible to account for the differences; and we refrain from attempting it. The text had evidently been felt to be obscure from very early times, especially for those who were unacquainted with the Hebrew; and hence transformations, omissions, and interpolations of words, and even of sentences, on the part of copyists and commentators, had resulted in the very various readings of different versions. The passage as given by Augustin is a good example of his ingenuity in spiritualizing the statements of Scripture.—Tr. 1423 Gal. ii. 20.⟧¶

### Tractate 85

Numbers removed (11): 1424–1434. Fragments removed: 3.

- §2, references: …then, in my very service, I am no longer a servant.⟦ 1424 Luke vi. 46. 1425 Matt. xxv. 21.⟧ ¶ `## §3 ^s3`
- §3, references: …of God, that we might know the things that are freely⟦ 1426 John iv. 18. 1427 Ps. xix. 9. 1428 Rom. viii. 15. 1429 Rom. xi. 20. 1430 Chap. viii. 35. 1431 Chap. i. 12. 1432 Cor. iv. 7.⟧ given to us of God.”1433 Whatever good there is, is…
- §3, references: …present discourse, but leave them over till another.⟦ 1433 Cor. ii. 12. 1434 Cor. i. 31.⟧¶

### Tractate 86

Numbers removed (16): 1435–1450. Fragments removed: 3.

- §1, references: …an end, and at its close the reward be received; not⟦ 1435 Chap. xvi. 12. 1436 Isa. xlv. 11. 1437 Ps. xxii. 16. 1438 Cor. xiii. 10, 12. 1439 Tit. iii. 5. 1440 Rom. viii. 24, 25. 1441 Pet. i. 8, 9. 1442 Gal. v. 6.⟧ only the redemption of our body, whereof the Apostle…
- §2, references: …one, listen: “Ye have not chosen me, but I have chosen⟦ 1443 Rom. viii. 23. 1444 Cor. iv. 16. 1445 Ps. lxxxiv. 10. 1446 Ps. lix. 10. 1447 Eph. i. 4. 1448 Rom. xi. 5, 6.⟧ you.” Not that thou mayest say, I am chosen because I…
- §3, references: …that which really belongs to the way of salvation.⟦ 1449 Rom. xiv. 23. 1450 Chap. xv. 5.⟧¶

### Tractate 87

Not cleaned: its CCEL page could not be read (HTTP 429). See A5.

### Tractate 88

Numbers removed (10): 1462–1471. Fragments removed: 4.

- §2, other note: …miserable, therefore, are those who do such things on⟦ 1462 Pet. ii. 21. 1463 Chap. xv. 15, xiii. 16. 1464 See above, Tract. LXXXV. sec.⟧ ¶ `## §3 ^s3`
- §3, references: `## §3 ^s3` ¶ ⟦1465 Chap. viii. 35. 1466 John iv. 18. 1467 Ps. xix. 9. 1468 Matt. xxv. 21. ⟧account of that name, as those are blessed who suffer…
- §4, references: …of the godly, certainly also punished murderers⟦ 1469 Matt. v. 10. 1470 Cor. i. 30, 31.⟧ and adulterers, and all classes of evil-doers whom…
- §4, references: …are being gathered by Christ along with the others.⟦ 1471 Wisd. vi. 16.⟧¶

### Tractate 89

Numbers removed (7): 1472–1478. Fragments removed: 2.

- §2, references: …sin of not believing on Christ, inasmuch as He came⟦ 1472 Cor. ii. 16.⟧ not and spake not to them. But it is not in the…
- §4, references: …Saviour who came to seek that which was lost, shall⟦ 1473 Matt. x. 40. 1474 Luke x. 16. 1475 Cor. xiii. 3. 1476 Rom. ii. 12. 1477 Rom. vii. 12. 1478 Luke xix. 10.⟧ doubtless become the prey of perdition; although it…

### Tractate 90

Numbers removed (2): 1479–1480. Fragments removed: 1.

- §3, references: …if they loved God, what other answer would they have⟦ 1479 Cor. x. 13. 1480 Cor. iv. 5.⟧ given but that they did love Him, and that not with…

### Tractate 91

Numbers removed (23): 1481–1503. Fragments removed: 3.

- §2, references: …manna for them from heaven in their hunger, and water⟦ 1481 Kings xvii. 21, 22. 1482 Kings iv. 35. 1483 Kings xiii. 21. 1484 Matt. xiv. 15–21, and xv. 32–38. 1485 Matt. xiv. 25–29. 1486 John ii. 9. 1487 John ix. 7. 1488 Ex. vii.-xii. 1489 Ex. xiv. 21–29. 1490 Ex. xvi.⟧ from the rock in their thirst?1491 Who else save…
- §3, other note: …were made whole.” None other man did such things in⟦ 1491 Ex. xvii. 6. 1492 “Jesus Nave”: ᾽Ιησοῦς (υἱὸς) Ναυῆ, Sept., Josh. i. 1. 1493 Josh. iii. 1494 Josh. x. 12–14. 1495 Judg. xv. 19. 1496 Kings ii. 11. 1497 Dan. vi. 22. 1498 Dan. iii. 23–27. 1499 Mark. i. 32–34. 1500 Matt. viii. 17. 1501 Mark vi. 56.⟧ them. For so are we to understand the words in them,…
- §4, references: …He Himself did them without any doing on their part.⟦ 1502 Matt. vi. 11. 1503 Ps. lxxii. 18.⟧¶

### Tractate 92

Numbers removed (7): 1504–1510. Fragments removed: 2.

- §1, references: …blood which they had shed. For the blood of Christ⟦ 1504 Gal. v. 6. 1505 Acts ii.⟧ ¶ `## §2 ^s2`
- §2, references: …bear when lapsing himself into denial. And what shall⟦ 1506 Rom. v. 5. 1507 Matt. xxvi. 69–74. 1508 John iv. 18. 1509 John xxi. 15. 1510 Acts ii.–v.⟧ I say more? In him there shone forth such an…

### Tractate 93

Numbers removed (18): 1511–1528. Fragments removed: 5.

- §2, references: …themselves therefrom, although no one expelled⟦ 1511 Ps. xix. 4. 1512 Chap. xv. 20. 1513 Ps. cxix. 165. 1514 Rom. v. 5.⟧ them? Doubtless He meant to announce with…
- §3, references: …known the Father, nor me.” That is to say, they have⟦ 1515 Rom. xi. 17. 1516 Chap. xii. 42, 43. 1517 Chap. v. 44. 1518 Rom. x. 3. 1519 Ps. lxxxix. 15–17. 1520 Rom. x. 2, 3.⟧ not known the Father, nor His Son, to whom they think…
- §3, other note: …have also been put on record. “Ye perceive that the⟦ 1521 Indicativo modo.⟧ whole world is gone after him:1522 “If we let him…
- §4, references: …blessing. For that such was the cause of His⟦ 1522 Chap. xii. 19. 1523 Chap. xi. 48, 50. 1524 Chap. xv. 20. 1525 Rom. x. 2. 1526 Rom. xi. 25, 17. 1527 Acts ii.–iv.⟧ making these announcements to them beforehand, is…
- §4, references: …slay the flesh had no power to darken their faith.⟦ 1528 Ps. xlii. 8.⟧¶

### Tractate 94

Numbers removed (10): 1529–1538. Fragments removed: 3.

- §2, references: …make them His martyrs, that is, His witnesses through⟦ 1529 Matt. xxiv. 9; Mark xiii. 9–13; and Luke xxi. 12–17. 1530 Matt. x. 17. 1531 Cor. xiii. 7. 1532 Rom. v. 5.⟧ the Holy Spirit; so that by His effectual working…
- §4, references: …continue to love me carnally, and, content with such⟦ 1533 Chap. xiii. 36. 1534 Acts i. 9–11.⟧ milk, desire to remain infants always. “It is…
- §5, references: …no diversity of essence, yet the personal distinction⟦ 1535 Chap. i. 32. 1536 Cor. v. 16. 1537 Matt. xxviii. 20. 1538 Chap. xiv. 23.⟧ of each one separately should be presented to notice;…

### Tractate 95

Numbers removed (23): 1539–1561. Fragments removed: 5.

- §1, references: …love in your hearts, and, having your fear thereby⟦ 1539 Chap. xv. 22, 19. 1540 Chap. xvii. 25. 1541 Matt. xxv. 41. 1542 Acts i. 7, 8. 1543 Cor. xiii. 3. 1544 Rom. v. 5. 1545 John iv. 18.⟧ expelled, ye shall have freedom to reprove. We have…
- §2, other note: …and said, “because I go to the Father, and ye⟦ 1546 Tract. XX. 1547 Eccles. vii. 20, 16.⟧ shall see me no more.” Wherefore it is of its own…
- §3, other note: …that is, Christ in such a condition, they were no more⟦ 1548 Eph. v. 13. 1549 Chap. xx. 29. 1550 Rom. i. 17; Hab. ii. 4; and Heb. xi. 1. 1551 Sperantium substantia. 1552 Cor. xv. 8. 1553 Acts vii. 56. 1554 Rom. viii. 3.⟧ to see after He had passed from this world to the…
- §4, references: Rejoins “reserved”. …of infernal darkness, and gave them up to be re⟦1555 Cor. v. 16. 1556 Chap. xiv. 30. 1557 Chap. i. 10. 1558 Chap. iii. 17. 1559 Eph. v. 8. 1560 Chap. xii. 31. ⟧served for punishment in the judgment,”1561 how is the…
- §4, references: …of the punishment that overtook the pride of angels.⟦ 1561 Pet. ii. 4.⟧¶

### Tractate 96

Numbers removed (15): 1562–1576. Fragments removed: 5.

- §1, references: …so are ye: although it may be that many now can bear⟦ 1562 Chap. xv. 15. 1563 Isa. xlv. 11, Septuagint. 1564 Chap. xiii. 36–38.⟧ what Peter then could not, in the same way as many…
- §4, references: …the nature of God, as incorporeal, and unconfined by⟦ 1565 Rom. v.⟧ ¶ `## §5 ^s5`
- §5, other note: `## §5 ^s5` ¶ ⟦1566 ῾Οδηγήσει ὑμᾶς εἰς τὴν ἀλήθειαν πᾶσαν, or ἐν τῇ ἀληθείᾳ πάσῃ 1567 Ps. lxxxvi. 11. 1568 Chap. vi. 45. ⟧limits, and yet not rolled out as a mass of matter…
- §5, references: …is the will of God, which is good, and acceptable, and⟦ 1569 Matt. xviii. 10. 1570 Wisd. ix. 15. 1571 Cor. i. 22. 1572 Cor. xiii. 9, 12. 1573 Eph. v. 12. 1574 Eph. iv. 23.⟧ perfect;”1575 that, “rooted and grounded in love, ye…
- §5, references: …that love ever more and more largely in your hearts.⟦ 1575 Rom. xii. 2. 1576 Eph. iii. 17–19.⟧¶

### Tractate 97

Numbers removed (14): 1577–1590. Fragments removed: 5.

- §1, references: Rejoins “offhand”. …therefore, that are incessantly being uttered off⟦1577 Cor. i. 22. 1578 Cor. ii. 9. ⟧hand and openly about the eternity, the truth, the…
- §2, other note: …waters.” For the woman thus spoken of is the vanity⟦ 1579 Cor. iii. 6. 1580 Prov. ix. 13–17, according to the Septuagint, where, in verse 13,  פתיותis rendered ἐνδεὴς ψωμοῦ, “in want of a morsel of bread,” as if from  פתor פתות, a morsel. The form of the word, however, as well as the Masoretic pointing, shows its connection with  פתיin the sense of “simplicity” or “folly” personified. And again in verse 17, the LXX. have partly inverted the Hebrew order of the words, and translate “( ימתקוare sweet”) in its active sense of “taste with relish” (or pleasure), as if it were מתקו, Imperative; and read “( ינעםis sweet”)⟧ of the impious, who, utterly senseless as they are,…
- §4, translator’s note: …unto fables.” For that mentioning of secrecy and⟦ in the last clause, as if it were  נעיםor נעם, “sweet,” or “sweetness:” hence Augustin’s rendering above. The Vulgate corresponds more nearly with the Hebrew and our English version.—Tr. 1581 Tim. iv. 3, 4.⟧ theft, whereof it is said, “Partake with pleasure of…
- §5, translator’s note: …met with the words of the Apostle Paul in his⟦ 1582 Tim. ii. 16, 17. Augustin translates κενοφωνίας (“babblings,” “empty utterances,” vaniloquia, Vulgate) as if it read καινοφωνίας, “novelties of words.”—Tr. 1583 Acts xi. 26. 1584 Xenodochia, houses of entertainment for strangers. 1585 “Of the same essence (or substance) with the Father,” as applied to Christ. 1586 Chap. x. 30. 1587 Chap. xiii. 34. 1588 Tim. vi. 20, 21.⟧ Epistle to the Corinthians: “I could not speak unto…
- §5, references: …that for the time we may bring the present to a close.⟦ 1589 Cor. iii. 1, 2. 1590 Cor. ii. 6, 13, 14.⟧¶

### Tractate 98

Numbers removed (23): 1591–1613. Fragments removed: 9.

- §2, references: …the passion of His Only-begotten, that no one should⟦ 1591 Cor. iii. 1, 2. 1592 Cor. i. 23, 24.⟧ glory in man, what understanding had they of Christ…
- §3, references: …you as unto spiritual, but as unto carnal,” as if he⟦ 1593 Cor. i. 12. 1594 Gal. vi. 14. 1595 Cor. xiv. 37, 38. 1596 Gal. iv. 9. 1597 Eph. i.⟧ ¶ `## §4 ^s4`
- §4, references: `## §4 ^s4` ¶ ⟦1598 Cor. ii. 2. ⟧said, What I did speak, ye could not receive as…
- §4, references: …who, while accounting evil to be a substance uncreated⟦ 1599 Cor. ii. 14. 1600 Cor. i. 30, 31. 1601 Cor. i. 12. 1602 Heb. v. 12–14. 1603 Cor. ii. 6.⟧ by God, make God Himself a mutable substance, as is…
- §6, other note: …of that which existed. For even in the very food that⟦ 1604 In place of τὸ στερεὼμα, solidity, steadfastness, Augustin reads τὸ ὑστερῆμα, that which is lacking. So also in his epistle to Paulinus, which is marked (in Migne’s edition of Augustin). 1605 Col. ii. 5. 1606 Thess. iii. 10. 1607 Heb. vi. 1, 2.⟧ we take, so far is there from being any contrariety…
- §7, references: …thou hast come to some understanding of what is not⟦ 1608 Chap. i. 1, 14. 1609 Phil. iii. 15, 16.⟧ at variance with the rule of the Catholic faith,…
- §8, references: …others; so that one of them attained even to things⟦ 1610 Rom. i. 21. 1611 Gal. i.⟧ ¶ `## §9 ^s9`
- §9, references: `## §9 ^s9` ¶ ⟦1612 Chap. vi. 45. ⟧of which it is not lawful for a man to speak. Taking…
- §9, references: …which is good, but untainted by that which is evil.⟦ 1613 Cor. xii. 2, 4.⟧¶

### Tractate 99

Numbers removed (37): 1614–1650. Fragments removed: 9.

- §1, other note: …the Holy Spirit, “For He shall not speak of Himself;⟦ 1614 Chap. v. 30. 1615 Tracts. XIX.–XXII. 1616 Phil. ii. 8. 1617 Chap. v. 22, 27. 1618 Literally, “when He emptied Himself.” 1619 Phil. ii. 6, 7. 1620 Rom. v. 19.⟧ but whatsoever He shall hear, that shall He speak,”…
- §2, references: …their own order to the birth, and succeed those which⟦ 1621 Chap. x. 30. 1622 Chap. xiv. 28. 1623 Matt. iii. 16. 1624 Acts ii.⟧ ¶ `## §3 ^s3`
- §3, references: `## §3 ^s3` ¶ ⟦1625 Luke ix. 35. ⟧are dying away, so that all that we have to say is…
- §3, other note: …years, they are the thoughts only of a childish mind.⟦ 1626 Eph. v. 2. 1627 Rev. iii. 16. 1628 Deus Christus. 1629 Chap. iv. 34. 1630 Song of Sol. ii. 6.⟧ ¶ `## §4 ^s4`
- §4, references: …from, another. And yet surely there should not⟦ 1631 Chap. i. 9, 1. 1632 Song of Sol. i. 4, Septuagint. 1633 Ps. xxxvi. 9. 1634 Ps. lxxiii. 28. 1635 Chap. v. 26.⟧ on that account occur to human thought any idea of…
- §5, references: …whom He is; and of Him He is, from whom He proceeds.⟦ 1636 Ex. iii. 14.⟧ ¶ `## §6 ^s6`
- §7, references: …and said, “Receive ye the Holy Spirit.” For what else⟦ 1637 Matt. x. 20. 1638 Gal. iv. 6. 1639 Eph. iv. 4–6. 1640 Rom. viii. 11, 9. 1641 Chap. iv. 24. 1642 Chap. xx. 22.⟧ was signified by such a breathing upon them, but that…
- §9, references: …the mother, it is not then that he proceedeth from⟦ 1643 Luke viii. 46. 1644 Luke i. 34, 35. 1645 Luke xxiv. 49. 1646 Acts i. 8, marg. 1647 Luke vi. 19. 1648 Chap. xv. 26. 1649 Chap. vii. 16.⟧ the mother; and when he cometh forth from the mother…
- §9, other note: …to some length, they must be left over for another.⟦ 1650 This passage from sec. 8, Augustin has transferred into Book XV. “On the Trinity,” chap. 27.⟧¶

### Tractate 100

Numbers removed (7): 1651–1657. Fragments removed: 4.

- §2, other note: …evil; and in regard to persons, when they think one to⟦ 1651 Clarificabit: see below. 1652 Matt. x. 20.⟧ be good who is evil; and in regard to both, when what…
- §3, translator’s note: …what Christ is not. For to say that the only-begotten⟦ 1653 Histrionibus, literally, play-actors. 1654 Ps. x. 3. Augustin here, as usual, follows the Septuagint. ( הִלֵּלpraise), however, is not passive, but, instead of its usual accusative, takes  עַלwith the subject of praise, and is rendered with sufficient accuracy in the English version. ְבֵּרֵך, also, must be translated actively, with “the covetous,” or “the defrauder,” as its nominative: and the verse should thus read, “The wicked boasteth of his soul’s desire, and the defrauder blesseth [and] blasphemeth [the divine name, as printed].” It would be natural enough in the defrauder to do both.—Tr.⟧ Son is not equal to Him that begat, is not good: to…
- §4, references: …is that the only-begotten Son said, “All things that⟦ 1655 Ps. cviii.⟧ ¶ `## §5 ^s5`
- §5, references: …require a different opening for their discussion.⟦ 1656 Luke xv. 31. 1657 Chap. xvii. 10.⟧¶

### Tractate 101

Numbers removed (18): 1658–1675. Fragments removed: 5.

- §2, translator’s note: …will be a friend of this world, is become the enemy of⟦ 1658 Chap. xvi. 10. 1659 The English version has here, “Ye shall not see me,” reading οὐ in the original, with the Alexandrine Codex. Several of the others, however (including the Sinaitic), have οὐκέτι (“no more”), rendered by Augustin jam non, which has thus the greater weight of authority on its side.—Tr. 1660 Above, Tract. XCV.⟧ God;”1661 for the effect of that enmity to God was,…
- §5, other note: …to be looked at and handled; but rather to that of⟦ 1661 Jas. iv. 4. 1662 Rom. vi. 9. 1663 Greek, ἐρωτήσετε. 1664 Acts i.⟧ ¶ `## §6 ^s6`
- §6, references: `## §6 ^s6` ¶ ⟦1665 Acts vii. 59. 1666 Chap. xx. 27. ⟧which He had already said, “He that loveth me, shall…
- §6, references: …where He saith, “A little while, and ye shall no more⟦ 1667 Chap. xiv. 21. 1668 John iii. 2. 1669 Chap. xvii. 3. 1670 Cor. xiii. 12. 1671 Chap. xiv. 8, 10. 1672 John ii. 18.⟧ see me;” and not to the subsequent, where He saith,…
- §6, references: …if the Lord will, obtain a more befitting explanation.⟦ 1673 Acts i. 3, 9. 1674 Matt. xxviii. 20. 1675 Rom. xii. 12.⟧¶

### Tractate 102

Numbers removed (13): 1676–1688. Fragments removed: 4.

- §2, other note: …you;” that by the words, “if anything,” should not be⟦ 1676 Above, Tract. LXXIII. 1677 Exaudiuntur, heard and answered. 1678 Gal. vi.⟧ ¶ `## §3 ^s3`
- §3, translator’s note: …have no place there where such abundance shall reign.⟦ 1679 Cor. xiii. 12. 1680 Matt. xi. 27. 1681 John iii. 2. 1682 Ps. ciii. 5. 1683 Ps. xvii. 15. So the Septuagint translate ָ אֶשְׂבְּעָה בְהָקִיץ תְּמוּנָתֶך. The Hiphil intransitive form  הֵקִיץis used, however, only of “awaking” out of sleep, not of “appearing,” or “being manifested;” and תְּמוּנָה properly means, appearance, form, likeness, although “glory” may in the present connection be implied: so that while the rendering of the Septuagint may be grammatically defensible, “I shall be satisfied when Thy glory is manifested,” yet the strict meaning of the words, the context, and the accentuation, favor that of the English version, “I shall be satisfied, on awaking, with Thy likeness.”—Tr.⟧ ¶ `## §4 ^s4`
- §4, other note: …His manhood, as addressing the Father on our behalf;⟦ 1684 Cor. ii. 6. 1685 Cor. iii. 1. 1686 Animalis.⟧ but in respect to His Godhead, as hearing [and…
- §6, references: …not the world in the ruling activity of His presence.⟦ 1687 John iv. 19. 1688 Rom. v. 5.⟧¶

### Tractate 103

Numbers removed (2): 1689–1690. Fragments removed: 1.

- §3, references: …own, “Be of good cheer, I have overcome the world.”⟦ 1689 Luke xxiv. 21. 1690 Cor. xv. 57.⟧¶

### Tractate 104

Numbers removed (6): 1691–1696. Fragments removed: 4.

- §2, references: …while having distress in the world, and had exhorted⟦ 1691 Chap. xiv. 25, 26.⟧ them to be of good cheer, because He had overcome the…
- §3, references: …His humility than to His glory, in accordance with the⟦ 1692 Gal. iv.⟧ ¶ `## §4 ^s4`
- §4, references: `## §4 ^s4` ¶ ⟦1693 Isa. xlix. 8. 1694 Cor. vi. 2. 1695 Rom. viii. 32. ⟧testimony of the apostle, who says, “He humbled…
- §4, translator’s note: …the latter out to greater length by such a discussion.⟦ 1696 Phil. ii. 7–11. So Augustin, with a few others of the early fathers, incorrectly renders the last clause instead of that given by our English version, which is alone grammatically and textually correct: “That Jesus Christ is Lord, to the glory (εἰς δόξαν) of God the Father.”—Tr.⟧¶

### Tractate 105

Numbers removed (18): 1697–1714. Fragments removed: 5.

- §2, translator’s note: …give eternal life to all that Thou hast given Him.”⟦ 1697 Ps. lxxvi. 1. 1698 Ps. cxiii. 3, 1: pueri, from the LXX. παῖδες. The Hebrew is עַבְדֵי, “servants.”—Tr. 1699 Ps. cxiii. 3, 1: pueri, from the LXX. παῖδες. The Hebrew is עַבְדֵי, “servants.”—Tr. 1700 Rom. xiii. 1. 1701 Col. i. 16.⟧ ¶ `## §3 ^s3`
- §4, references: …Him to do, when there still remains the trial of the⟦ 1702 Ps. lxxxiv. 4.⟧ passion wherein He especially furnished His martyrs…
- §5, translator’s note: …He had so spoken as if He had done what He was still⟦ 1703 Pet. ii. 21. 1704 Ps. xxii. 16, 17. Dinumeraverunt (they counted), in accordance with a reading of the Septuagint—that found in the printed text—ἐξηρίθμησαν. A better reading, however, is also found in mss., ἐξήρίθμησα, conforming in person, though not in tense, to the Hebrew ( אֲכַפֵּרI may count).—Tr. 1705 Ps. xxii. 16, 17. Dinumeraverunt (they counted), in accordance with a reading of the Septuagint—that found in the printed text—ἐξηρίθμησαν. A better reading, however, is also found in mss., ἐξήρίθμησα, conforming in person, though not in tense, to the Hebrew ( אֲכַפֵּרI may count).—Tr. 1706 Chap. xv. 15. 1707 Chap. xvi. 12. 1708 Isa. xlv. 11, according to the Septuagint. See note, Tract. LXVIII. sec. 1.⟧ to do; but that here He demanded of the Father to do…
- §8, translator’s note: …of David according to the flesh, who was predestinated⟦1713 1709 Eph. i. 4. 1710 Tim. ii. 5. 1711 Rom. iv. 17. 1712 Rom. viii. 28–30. 1713 Rom. i. 1–4: ὁρισθέντος, determined, declared, not “predestinated,” which is a mistake of the Latin version used by Augustin.—Tr.⟧ the Son of God in power, according to the Spirit of…
- §8, translator’s note: …must be taken into consideration in another discourse.⟦ 1714 Rom. i. 1–4: ὁρισθέντος, determined, declared, not “predestinated,” which is a mistake of the Latin version used by Augustin.—Tr.⟧¶

### Tractate 106

Numbers removed (10): 1715–1724. Fragments removed: 5.

- §2, references: …bodily presence that He said, “While I was with them,⟦ 1715 Ps. xxxv. 18.⟧ I kept them,” as if already that presence were no…
- §4, references: …His name is great in Israel”? Therefore, “I have⟦ 1716 Matt. xxviii. 20. 1717 Ps. lxxvi. 1.⟧ manifested Thy name unto these men whom Thou gavest…
- §5, references: …by God the Son, apart from whom there was nothing ever⟦ 1718 Chap. xvi. 25. 1719 Chap. xv. 15.⟧ possessed by the Father; but it is His custom to…
- §6, other note: …the mind. “And they have known truly,” He adds, “that⟦ 1720 Omnitenens. 1721 Chap. xv. 19.⟧ I came out from Thee, and they have believed that…
- §7, references: …otherwise would He give any words to the Word, wherein⟦ 1722 Chap. xvi. 31, 32. 1723 Matt. xxvi. 69–74. 1724 Matt. x. 33.⟧ in an ineffable way He hath spoken all things? But…

### Tractate 107

Numbers removed (7): 1725–1731. Fragments removed: 3.

- §2, references: …Son, that the Holy Spirit was to receive that whereof⟦ 1725 Luke xv. 31. 1726 Luke xx. 36. 1727 Chap. xvi. 15.⟧ He said, “He shall receive of mine;” but most…
- §7, references: …that the Scripture might be fulfilled.” The betrayer⟦ 1728 Chap. x. 30. 1729 Chap. xiv. 28. 1730 Chap. xvi. 23.⟧ of Christ was called the son of perdition, as…
- §8, other note: …and righteously, and godly in the present.⟦ 1731 Augustin: “108th” (Vulg.).⟧¶

### Tractate 108

Numbers removed (9): 1732–1740. Fragments removed: 2.

- §2, references: …them in the truth,” but, Sanctify them in me?⟦ 1732 Chap. xv. 19. 1733 Phil. i. 6. 1734 Chap. xiv. 6. 1735 Chap. viii. 32–36.⟧ ¶ `## §3 ^s3`
- §5, other note: …let us understand that He thereby meant that He would⟦ 1736 Chap. i. 1, 14. 1737 Rom. viii. 3. 1738 Cum et ipsi sint ego. 1739 Gal. iii. 29, 16. 1740 Col. i. 24.⟧ sanctify them in Himself, He immediately added, “That…

### Tractate 109

Numbers removed (20): 1741–1760. Fragments removed: 5.

- §2, translator’s note: …says, “Many believed on Him”? For whence came the⟦ 1741 Chap. xv. 27. 1742 The interrogative particle, numquid, beginning this and the following sentences, implies a negative answer. If Nathanael be identified with Bartholomew, the answer would be affirmative.—Tr. 1743 Chap. xix. 38. 1744 Chap. ii. 23, iv. 39, vii. 31, viii. 30, x. 42.⟧ multitude of those who, with branches of trees,…
- §3, references: …by the same of Satan. Those, accordingly, are found⟦ 1745 Matt. xxi. 9; Ps. viii. 2. 1746 I Cor. xv. 6. 1747 Acts i. 15, and ii.⟧ ¶ `## §4 ^s4`
- §4, references: `## §4 ^s4` ¶ ⟦1748 Luke ii. 25–38. 1749 Luke i. 41–45, 67–79. 1750 Chap. i. 19–36, and iii. 26–36. 1751 Matt. xvi. 16, 23. ⟧to be the greater in faith who were long since…
- §5, other note: …word of the resurrection of Christ, it is said by the⟦ 1752 Gal. i. 1, 12. 1753 Luke xxiii. 42. 1754 Job vii. 1: Tentatio super terram, ע ָ ב ָ עא ַ ראָ־ל ֶ  ;ץEnglish version, “An appointed time (marg., warfare) upon earth.” Rev. Ver. puts “warfare” into the text, and “time of service” on the margin. 1755 Gal. ii. 2, 9.⟧ same apostle, “Whether it were I, or they, so we…
- §5, references: …must be reserved for discussion in another discourse.⟦ 1756 Cor. xv. 11. 1757 Rom. x. 8, 9. 1758 Acts xvii. 31. 1759 Thess. ii. 13. 1760 Acts vi. 1–4.⟧¶

### Tractate 110

Numbers removed (16): 1761–1776. Fragments removed: 7.

- §2, references: …be one are not of one class, and the world that is⟦ 1761 Chap. x. 30. 1762 Gal. iii. 28.⟧ thereafter to believe on this very ground that these…
- §3, references: …“And the glory which Thou gavest me, I have given⟦ 1763 Cor. xi. 32. 1764 Chap. iii. 17. 1765 Cor. v. 19. 1766 Eph. v. 8.⟧ them.” And what was that glory but immortality, which…
- §3, references: …added, “That they may be one, as we also are one.”⟦ 1767 Chap. v. 21, 19. 1768 Chap. ii. 19.⟧ ¶ `## §4 ^s4`
- §4, references: …reconciling the world unto Himself.” Therefore said⟦ 1769 Chap. xiv. 23. 1770 Cor. iii. 23.⟧ He, “I in them, and Thou in me;” as if He had said, I…
- §6, references: …love toward us, in that, while we were yet sinners,⟦ 1771 Eph. i. 4.⟧ Christ died for us.”1772 He, therefore, had love…
- §7, references: …ourselves to the angels on this account, that, while⟦ 1772 Rom. v. 8, 9. 1773 Ps. v. 5. 1774 Wisd. xi. 25. 1775 Rom. v. 6.⟧ there are angels also who have sinned, there has been…
- §7, references: …that we should be in some sort their associates.⟦ 1776 Luke xx. 36.⟧¶

### Tractate 111

Numbers removed (26): 1777–1802. Fragments removed: 7.

- §1, references: …this reward, that where He is, there also we shall⟦ 1777 Rom. xii. 12. 1778 Ps. cxvi. 11. 1779 Chap. xiv. 6. 1780 Chap. vi. 44.⟧ be with Him; nor can that be otherwise which the…
- §2, references: …what he is certain will yet be done. But if it is in⟦ 1781 Matt. xxvi. 39. 1782 Rom. i.⟧ ¶ `## §3 ^s3`
- §3, references: `## §3 ^s3` ¶ ⟦1783 Chap. iii. 13. 1784 Eph. ii. 4–6. ⟧respect of the form of God, wherein He is equal to the…
- §3, other note: …is against me.” But when He said to God the Father, “I⟦ 1785 Luke xxiii. 43. 1786 In inferno. 1787 Ps. cxxxix. 8. 1788 Wisd. vii. 24. 1789 Chap. i. 5. 1790 Matt. xii. 30.⟧ will that they also whom Thou hast given me be with…
- §3, other note: …Father, art in me, and I in Thee:” and they are our⟦ 1791 John iii. 2. 1792 Merces. 1793 Heb. xi. 1. 1794 Isa. xxvi. 10. 1795 Matt. v. 8. 1796 Matt. xxv. 46. 1797 Chap. xiv. 10.⟧ place, because there follows, “That they also may be…
- §5, translator’s note: …it hath not known Him; while the world which He hath⟦ 1798 Ps. lxxvi. 2: in pace, ְ ;םל”שָבrather as in English version, “in Salem” (Jerusalem).—Tr. 1799 Ps. lxxvi. 2: in pace, ְ ;םל”שָבrather as in English version, “in Salem” (Jerusalem).—Tr. 1800 Col. iii. 1–4.⟧ reconciled unto Himself through Christ hath known Him…
- §6, translator’s note: …passion, as He granteth us grace, in others to follow.⟦ 1801 Quam dilexisti me. The part which follows, which we have enclosed within parentheses, may be omitted by the English reader, as it only deals with the Latin idiom.—Tr. 1802 Tim. iv. 7.⟧¶

### Tractate 112

Numbers removed (10): 1803–1812. Fragments removed: 3.

- §2, translator’s note: …profound counsel of the Father of the family, learned⟦ 1803 Augustin refers to his books “On the Harmony of the Evangelists.” 1804 The text runs thus: Sciebat, inquit, et Judas, qui tradebat eum, locum. Ordo verborum est, Sciebat locum, qui tradebat eum; which could not be intelligibly translated into English.—Tr.⟧ where he might opportunely scatter the slender flock,…
- §6, other note: …they had never found access: for He continued the day,⟦ 1805 Thomas Aquinas in the Casena reads here, He commands his enemies, and not altogether unsuitably.—Migne. 1806 Luke xxii. 51. 1807 Rom. vii. 6. 1808 Gal. iv. 24. 1809 Rom. viii. 31, 32. 1810 Eph. v. 2.⟧ while they remained as darkness; neither had they…
- §6, references: …God willing, with what follows in another discourse.⟦ 1811 Ps. xxxiv. 5. 1812 Ps. cxvi. 16.⟧¶

### Tractate 113

Numbers removed (18): 1813–1830. Fragments removed: 5.

- §2, references: …to Peter, Thou shalt deny that thou art my disciple;⟦ 1813 Eph. v. 2. 1814 Rom. viii. 32. 1815 Matt. xxvi. 57. 1816 Chap. xiii. 23, and xix. 26. 1817 Chap. xiii. 37.⟧ but, “Thou shalt deny me.”1818 Him, therefore, he…
- §3, references: …on the authority of the other evangelists, to those⟦ 1818 Matt. xxvi. 34. 1819 Acts xi. 26. 1820 Matt. xvi. 19. 1821 Chap. xvi. 25.⟧ who were truly His own, in comparison with others who…
- §4, references: …(literally, take aim), and advance prosperously and⟦ 1822 Deut. xix. 15. 1823 Matt. x. 27. 1824 Mark. iv. 12.⟧ reign, because of truth, and meekness, and…
- §5, translator’s note: …Zacharias, in the wilderness,” etc. Accordingly these⟦ 1825 Ps. xlv. 4. In the Hebrew text, at the close of verse and beginning of verse (Eng. Ver. verses and 4), there is a repetition of the word והדרך, which in both cases is rendered in our English Version, “and [in] Thy majesty.” By the Septuagint, however, and the Vulgate, and here by Augustin, the latter of the two has been differently read as a verb, as if pointed ְוְהַדְרֵך, in the sense of “Bend thy bow,” “Take aim,” with the acc. omitted. Our English Version combines the next two verbs צְלַח רְכַב, “ride prosperously” while in the above the distinction is preserved, “advance prosperously, ride (as a king, reign).”—Tr. 1826 Matt. v. 39. 1827 Ps. lvii. 7. 1828 Here probably we should read Silas, according to Acts xvi. 25.—Migne. 1829 Luke iii. 2.⟧ two pontiffs fulfilled their years in turn: and it…
- §6, references: …the Lord before Pontius Pilate the governor.⟦ 1830 Chap. xiii. 38.⟧¶

### Tractate 114

Numbers removed (7): 1831–1837. Fragments removed: 5.

- §3, other note: …to life, and, above all, the foolish who were become⟦ 1831 This reading of the text is also found in “The Harmony of the Evangelists,” Book iii. chap. 7; but the true biblical reading is now ascertained to be, ἀπὸ τοῦ Καἴάφα, “from Caiaphas.”—Migne.⟧ wise, whether Jesus were a malefactor. But these…
- §4, references: …captains of the temple, and elders, Be ye come out,⟦ 1832 Ps. xxxv. 12. 1833 Deut. xiii.⟧ ¶ `## §5 ^s5`
- §5, translator’s note: `## §5 ^s5` ¶ ⟦Augustin evidently attaches a wrong meaning to the words, Nobis non licet interficere quenquam; as if these Jews thereby insinuated that they did not themselves wish Christ’s death: unaware, seemingly, of the fact, that, on their subjugation by the Romans, their own rulers were still allowed to try minor offenses, but were deprived of the power of inflicting capital punishment; and that, consequently, it was because they were actually bent on putting Him to death, and no less penalty would satisfy them, that they thus brought Him before the Roman governor.—Tr. 1834 Chap. xix.⟧ ¶ `## §6 ^s6`
- §6, references: `## §6 ^s6` ¶ ⟦1835 Ps. lvii. 4. ⟧as against a thief,” etc?1836 As therefore the chief…
- §6, references: …innocence, but their madness might be made manifest.⟦ 1836 Luke xxii. 52. 1837 Mark x. 33, 34.⟧¶

### Tractate 115

Numbers removed (13): 1838–1850. Fragments removed: 4.

- §1, references: …wonder that one should be delivered up to a judge for⟦ 1838 Ps. xciv. 11.⟧ punishment, who proclaimed himself a king; but if no…
- §2, references: …of this world;” or, “My kingdom is not from hence.”⟦ 1839 Matt. ii. 3, 16. 1840 Ps. ii. 6. 1841 Chap. xvii. 16, 15. 1842 Matt. xiii. 38–41. 1843 Chap. xv. 19. 1844 Col. i. 13.⟧ ¶ `## §3 ^s3`
- §4, translator’s note: **Holds 1845: Augustine’s words, in the translator’s English, on “in hoc”.** …calling, not according to our works, but according to⟦ 1845 The verse quoted reads in Latin, “Ego in hoc natus sum, et ad hoc veni,” etc.; and in reference to the words, in hoc, Augustin goes on to say, in the passage marked * * . “We are not to lengthen the syllable [vowel] of this pronoun when He says, In hoc natus sum, as if He meant to say, In this thing was I born; but to shorten it, as if He had said, Ad hanc rem natus sum, vel ad hoc natus sum (for this thing was I born), just as He says, Ad hoc veni in mundum (for this came I into the world). For in the Greek Gospel there is no ambiguity in this expression,” the Greek having εἰς τοῦτο. This passage is interesting only to Latin scholars, as showing that in ordinary parlance they marked, in Augustin’s time, the distinction between hoc of the abl. and hoc of the nom. or acc.—Tr. 1846 Thess. iii. 2. 1847 Chap. xiv. 6. 1848 Chap. viii. 18. 1849 Rom. viii. 28.⟧ His own purpose and grace.”1850 For if our thoughts…
- §5, references: …but this must be taken up in another discourse.⟦ 1850 Tim. i. 8, 9.⟧¶

### Tractate 116

Numbers removed (12): 1851–1862. Fragments removed: 3.

- §5, references: …indeed, delivered me to thy power at the bidding of⟦ 1851 Matt. xxvi. 63, xxvii. 14; Mark xiv. 61, xv. 5; Luke xxiii. 7–9; John xix. 9. 1852 Isa. liii. 7. 1853 Rom. xiii. 1.⟧ envy, whilst thou art to exercise thy power upon me…
- §8, translator’s note: …is recorded. When Pilate, therefore, had sat⟦ 1854 Exinde: Greek, ἐκτούτου; literally. “therefrom.”—Tr. 1855 Exinde: Greek, ἐκτούτου; literally. “therefrom.”—Tr. 1856 Exinde: Greek, ἐκτούτου; literally. “therefrom.”—Tr. 1857 Lithostrotos. 1858 Parasceve; Greek, παρασκευή. 1859 Mark xv. 25. 1860 See below, Tract. CXVII. secs. 1, 2.⟧ down before the tribunal, “he saith unto the Jews,…
- §9, references: …the subject of consideration in another discourse.⟦ 1861 Chap. xviii. 31. 1862 Chap. xix. 23.⟧¶

### Tractate 117

Numbers removed (19): 1863–1881. Fragments removed: 4.

- §2, other note: …that therewith began the preparation of the true⟦ 1863 Mark xv. 25. 1864 Quasi. 1865 Matt. xxvii. 45; Mark xv. 33; and Luke xxiii. 44. 1866 Cor. v. 7. 1867 Matt. xxvi. 66.⟧ passover, whose shadow was the passover of the Jews,…
- §3, other note: …of the other evangelists, were thieves with whom⟦ 1868 “On the Harmony of the Evangelists,” Book iii. chap. xiii. secs. 40–50. 1869 Gal. vi. 14. 1870 Matt. v. 15.⟧ He was crucified, and between whom He was fixed,1871…
- §5, other note: …king also of the Gentiles? For this reason, because it⟦ 1871 Matt. xxvii. 38; Mark xv. 27; and Luke xxiii. 33. 1872 Isa. liii. 12. 1873 Ps. lvii., lviii. 1874 Ps. ii. 6–8. 1875 Chap. x. 16. 1876 Sacramentum.⟧ was the wild olive tree that was made partaker of the…
- §5, references: …wrote he wrote, because what the Lord said He said.⟦ 1877 Rom. xi. 17. 1878 Rom. ix. 7, 8. 1879 Gal. iii. 29. 1880 Rom. ii. 29. 1881 Gal. iv. 22–31.⟧¶

### Tractate 118

Numbers removed (13): 1882–1894. Fragments removed: 4.

- §2, references: …account given by this evangelist is also in harmony⟦ 1882 Matt. xxvii. 35. 1883 Mark xv. 24. 1884 Luke xxiii. 34.⟧ with the testimony of prophecy, which he likewise…
- §3, other note: …over in addition to their equal shares of the rest.⟦ 1885 As it now is in the Greek [Textus receptus], κλῆρον.—Migne.⟧ ¶ `## §4 ^s4`
- §4, other note: …of each individual, but by the secret judgment of God.⟦ 1886 Matt. xxiv. 31. 1887 Cor. xii. 31. 1888 Eph. iii. 19. 1889 Col. iii. 14. 1890 Desuper. 1891 Matt. xvi. 15, 16, 19. 1892 Per totum.⟧ ¶ `## §5 ^s5`
- §5, references: …of dissertation, as God shall grant us assistance.⟦ 1893 Eph. iii. 18. 1894 Gal. v. 24.⟧¶

### Tractate 119

Numbers removed (14): 1895–1908. Fragments removed: 6.

- §2, other note: …and with a closer familiarity, so that He even made⟦ 1895 Chap. ii. 4. 1896 See Tract. VIII. 1897 Tim. v. 8.⟧ him lean upon His bosom at supper;1898 in order, I…
- §4, references: …them all. He saw, therefore, that all was accomplished⟦ 1898 Chap. xiii. 23. 1899 Matt. xix. 27, 29. 1900 Cor. vi. 10. 1901 Acts iv. 32–35.⟧ that required to be done before He received the…
- §6, references: …that thus puts off his garment when he pleases, as He⟦ 1902 Ps. lxix. 21. 1903 Ps. li.⟧ ¶ `## §7 ^s7`
- §7, references: `## §7 ^s7` ¶ ⟦1904 Phil. ii.¶⟧`## §8 ^s8`
- §8, references: `## §8 ^s8` ¶ ⟦1905 Matt. xxvii. 48, and Mark xv. 36. 1906 Chap. x. 18. ⟧put off His flesh at His pleasure? Who is there that…
- §8, other note: …if such was the power He exhibited as a dying man!⟦ 1907 Abit…obiit. 1908 Abit…obiit.⟧ 1-9.

### Tractate 120

Numbers removed (14): 1909–1922. Fragments removed: 3.

- §2, other note: …such blood? What more healthgiving than such a wound?⟦ 1909 Aperuit. 1910 Vigilans. 1911 Aperuit. 1912 Gen. vi. 16. 1913 Gen. ii. 22. 1914 Gen. iii. 20. 1915 This last clause is found only in three of the Augustinian mss.⟧ 1-9.
- §4, other note: …bury;” for in this way, unless I am mistaken, he has⟦ 1916 Cor. v. 7. 1917 Isa. liii. 7. 1918 Chap. iii. 1, 2. 1919 This revelation, whereby the body of Nicodemus was discovered, is referred to the close of the year 415, by those who trust in the authority of the Presbyter Lucian, in a small book written on the subject.—Migne.⟧ 1-9. admonished us that, in duties of this kind,…
- §8, other note: **Holds 1921: words of Augustine’s Latin that the translator left out of his English.** …hasten on to other points, on which we are compelled⟦ 1920 Una Sabbati. 1921 Augustin here adds, quem Matthæus solus in Evangelistis primam Sabbati nominavit (Matt. xxviii. 1) contrasting primam with una. 1922 Some editions here insert into the text, More sanctæ Scripturæ, “after the manner of Holy Scripture.” Others enclose it within brackets.—Migne.⟧ 1-

### Tractate 121

Numbers removed (4): 1923–1926. Fragments removed: 4.

- §3, references: …to the Father, but refused it in the case of women⟦ 1923 Ps. lxviii.⟧ ¶ `## §4 ^s4`
- §4, references: `## §4 ^s4` ¶ ⟦1924 Luke xxiv. 39. ⟧till after His ascension? But no one, even had any the…
- §4, references: …remained inviolate, “Then were the disciples glad⟦ 1925 Matt. xxviii. 9.⟧ when they saw the Lord. Then said He unto them again,…
- §5, references: …the faith of the Gentiles: “Blessed are they that have⟦ 1926 Isa. xxvi. 3, margin.⟧ not seen, and yet have believed.” He made use of…

### Tractate 122

Numbers removed (23): 1927–1949. Fragments removed: 8.

- §2, references: …to work at all; and on the third day the Lord rose⟦ 1927 Matt. iv. 19. 1928 Matt. xix. 21, 22, 27. 1929 Luke ix. 62.⟧ 1-11. again, and re called them to the hope which…
- §3, references: …support, and, as the soldiers of Christ, to receive⟦ 1930 Thess. iii. 8. 1931 Cor. xv. 10.⟧ 1-11. the wages due to them, as from the inhabitants…
- §5, other note: …fish which ye have now caught. Simon Peter went up,⟦ 1932 Sicut a provincialibus Christi. 1933 Cor. ix. 11–15, 7. 1934 Matt. vi. 33.⟧ 1-11. and drew the net to land full of great fishes,…
- §7, references: …to signify those who stood on the right hand, the good⟦ 1935 Matt. xiii. 48, 49.⟧ 1-11. alone. There the net was broken on account of…
- §8, references: …“The letter killeth, but the spirit giveth life.” Let⟦ 1936 Luke v. 3–7. 1937 Ps. xl. 5. 1938 Deut. ix. 10. 1939 Cor. iii. 6.⟧ 1-11. the spirit then be added to the letter, lest…
- §8, references: …7, and you have 28; to this add 8, and 9, and 10, and⟦ 1940 Chap. iv. 24. 1941 Gen. i., ii. 3. 1942 Isa. xi. 2, 3. 1943 Rev. iii. 1. 1944 Cor. xii. 11.⟧ 1-11. you get 55; to this add and 12, and 13, and you…
- §9, references: …and Pharisees, ye shall not enter into the kingdom of⟦ 1945 Acts i. 4; ii. 2–4. 1946 Matt. xiii. 47.⟧ 1-11. heaven.”1947 Such, doubtless—these scribes and…
- §9, references: …topics that cannot be included in the present lecture.⟦ 1947 Matt. v. 17–20. 1948 Matt. xxiii. 2, 3. 1949 Matt. xi. 11.⟧¶

### Tractate 123

Numbers removed (11): 1950–1960. Fragments removed: 4.

- §2, references: …caught,” that all of us who cherish this hope may know⟦ 1950 Chap. vi. 41.⟧ that we ourselves, through that septenary number of…
- §5, references: …wicked, irreligious, without affection, false⟦ 1951 Chap. xiii. 37. 1952 Matt. xvi. 21, 22. 1953 Phil. ii. 21.⟧ accusers, incontinent, implacable, with out kindness,…
- §5, other note: …not the things that are Jesus Christ’s, and be turning⟦ 1954 Cœcati. 1955 Tim. iii. 1–5. 1956 Tim. i. 7.⟧ those to the use of their own lusts for whom the…
- §5, references: …who can fail to see that the shepherds ought all the⟦ 1957 Phil. i. 23. 1958 Cor. v. 4. 1959 Matt. xxvi. 39. 1960 Chap. x. 18, 11.⟧ more to set themselves closely to imitate the…

### Tractate 124

Numbers removed (26): 1961, 1963–1987. Fragments removed: 9.

- §2, other note: …that that disciple dieth not, and yet that this is the⟦ 1961 Sic eum volo manere donec veniam. 1962 Acts xii. 2.⟧ meaning of such words as He is here recorded to have…
- §3, references: …the living body lies so long asleep beneath the⟦ 1963 Deut. xxxiv. 6. 1964 Matt. xvii. 3. 1965 Kings ii. 11. 1966 Matt. xxvii. 52, 53.⟧ ground, till the coming of the end of the world? Nay,…
- §4, references: …of all that the Lord asked what He asked. The Lord⟦ 1967 Phil. i. 23.⟧ therefore knew, not only that Peter loved Him, but…
- §5, references: …that man is kept through time in the penalty,⟦ 1968 Wisd. ix. 15. 1969 Rom. viii. 24, 25. 1970 Job vii. 1. 1971 Matt. vi. 13.⟧ even when he is no longer held by his sin as liable…
- §5, references: …this very account the Lord said, “On this rock will I⟦ 1972 Job xiv. 1. 1973 Ps. lxxvii. 9. 1974 Gal. iv. 4. 1975 Tim. ii. 5. 1976 Matt. vi. 12.⟧ build my Church,” because Peter had said, “Thou art…
- §5, other note: …without any temptation to pride, it may cleave to that⟦ 1977 Matt. xvi. 16–19. 1978 Cor. x. 4. 1979 Cor. iii. 11. 1980 Universitati. 1981 Pet. ii. 21. 1982 Cor. xiii. 12.⟧ which is supremely good; the one discerneth both good…
- §7, references: …gospel through the whole world, that every one of His⟦ 1983 John iii. 2. 1984 Ps. xxv. 10.⟧ own may drink thereat according to his own individual…
- §8, other note: …I am also compelled to bring my discourse to a close.⟦ 1985 Jerome, Book I., Against Jovinian. 1986 Ps. lxxiii.⟧ ¶ `## §9 ^s9`
- §9, references: `## §9 ^s9` ¶ ⟦1987 Ps. lxviii. 21. ⟧Ten Homilies on the First Epistle of John.
