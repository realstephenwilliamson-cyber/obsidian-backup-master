# Track 3 – crosswalks and scripture numbering: full change list (batch 2)

For the section *Track 3 – crosswalks and scripture numbering* in "Phase 3 – decisions, batch 2". Built on 7 Oct 2026 from the notes snapshot of 04:08 UTC. Nothing here is applied yet.

## Counts and checks

- **Ready to apply: 3 links in 2 notes** (`/home/claude/p3/batch2/t3-ready-ops.json`, 3 replace ops). Visible text unchanged.
- **Ops that wait for an answer:** `/home/claude/p3/batch2/t3-question-ops.json`, keyed by question and option: X1 34, X2 4 (or 1), X3 2 per option, X4–X7 1 each, X10–X11 1 each, X12 2, X13 3, X15 2. X8, X9 and X14 have no op yet (X8 and X9 are recommended "leave"; X14's two lines are built after your answer). Any other option that changes text and has no op in the file (for example X10's full rewording, X13's separate Laghuvṛtti line, X15's replacement of Singh) is built and checked only after an answer.
- **Overnight changes:** of the notes these ops touch, two changed overnight. *Tanya – Iggeret HaTeshuvah 01* (X3): track 2 linked `II:135b` in footnote 27, line 75; the E8 ops are on footnote 21 (line 69). *RCL to Jewish and Patristic Concordance* (X2, op 2): track 1 changed the Kedoshim and Emor cells, and the 8.03/8.04 renames rewrote its links to those notes; op 2's find is the `## 1.` heading line. Re-checked by applying last night's changes to the snapshot copies of these two notes (the renames' link rewrites and the `t1c-emor` ops on the concordance; the track 2 op on the Tanya note): every X2 and X3 find still occurs once. The 3 ready ops touch neither note. No op in this track reads or writes a link to Zohar 8.03 or 8.04.
- **Script checks** (each option alone; then the ready ops and every ★ option chained; then that chain with each E8 option): every `find` occurs once at its turn; the link-only ops (ready, X1) leave the visible text unchanged; every new link target has a unique base name and its `^id` or heading exists; every table row keeps its cell count; nothing written contains the divine name. **0 problems.**

## Ready to apply (3)

| Note | Line | Change | Before → after | Checked by |
|---|---|---|---|---|
| BCP - Ministration to the Sick | 64 | link repointed to the BCP Psalter (E2's doubtful 8th link) | `[[Psalms 145#^145-14\|Psalm 145:14-22]]` → `[[BCP Psalm 145#^145-14\|Psalm 145:14-22]]` | t3/verify checker: BCP 145 has 22 verses, JPS 21; the cue "(The eyes of all wait upon you, O Lord)" is BCP 145:16 word for word; BCP 145:14 "faithful in all his words" has no JPS verse; the current link opens JPS 145:14, which is BCP 145:15 |
| Paratrisika-vivarana and the Alphabet of Creation | 25 | held e-text linked (E17) | `KSTS Vol. 32 (printed as 31)` → `[[Texts/Muktabodha/mAlinIvijayavArtika-M00158\|KSTS Vol. 32 (printed as 31)]]` | t3/e17 checker: M00158 "Photographed from volume 32 … incorrectly printed as volume 31"; *mālinīvijayavārtika*, Srinagar 1921 |
| Paratrisika-vivarana and the Alphabet of Creation | 26 | held e-text linked (E17) | `KSTS Vol. 1` → `[[Texts/Muktabodha/zivasUtravimarzinI text version-M00349\|KSTS Vol. 1]]` | t3/e17 checker: M00349 *śivasūtravimarśinī*, Kṣemarāja, ed. Chatterji 1911, "transcribed from volume 1 of the KSTS" |

## Done in phase 1, re-checked on the 04:08 snapshot (no change)

Checked by the t3/verify drafter and again by its checker (scripts re-run, not copied).

| Item | Verdict | What the vault has now |
|---|---|---|
| Concordance range links (B21 = E3 = G42) | done, right | Rows 8, 25, 42, 51 open `Torah 08 - Vayishlach#^32-4`, `Torah 25 - Tzav#^6-1`, `Torah 42 - Matot#^30-2`, `Torah 51 - Nitzavim#^29-9`. All 54 rows: each range link opens its parashah's first verse, and each label's end is the note's last verse. All 55 block links resolve. The "mark the table Hebrew-numbered" half is X2 (op 2). |
| Zohar cells (E4) | done | Masei, Eikev, Re'eh, Shoftim, Nitzavim and V'Zot HaBerachah read "—". Your Z9 answer (Ki Teitzei → Zohar 10.11; the other nine "— (no Zohar section in the vault)") is decided but not yet in the concordance; no op for it was found among the drafts (t1, t4) at 02:50. Kedoshim and Emor cells were retargeted overnight with the 8.03/8.04 renames (track 1). |
| Tractate ranges (C4 = E5) | done, right | All 21 John rows equal the ranges recomputed from the 124 `passage` properties (13: 55–66; 14: 067, 67–79; 15: 80–92; 16: 093, 93–103; 17: 104, 104–111; 20: 120, 120–122; 21: 122, 122–124). |
| 7 BCP psalm-verse links (E2) | done, right | 74:15 (×2), 139:10 (×2), 139:10-11, 93:4 and 123:3 open the BCP Psalm note at the verse quoted, in Evening Prayer Rite One (48, 56), Rite Two (47, 55), An Order of Worship for the Evening (59) and Concerning the Psalter (38, two links). Each id ends its paragraph, so Obsidian registers it. The 8th (145:14-22) is the ready op above. |
| Shifted references (E7, E26/E27) | done, right | Ehrman `Psalms 022#^22-2`, `Psalms 069#^69-22`; Cloud build reports line 69 `Joel 3#^3-1` (was line 67); the Biblical Greek chat, now under `Writing/The Gospel of Recognition/AI/`, lines 31 and 114 `LXX Psalms 81#^81-6` (resolves since track 5's blank lines). None of E26's 9 wrong links is still wrong. The other 19 shifted links outside RCL and BCP were read in context: all right (the writer used English numbers). 28 more are quoted as evidence in the analysis reports and Claude outputs; left alone. |
| Psalter list and Psalm 151 row (E18) | done | "Psalms 117–146: MT = LXX + 1" is in the list; the line reads "The RCL notes embed the JPS psalm only"; all 155 table lines in *Psalms numbering* have 6 cells. |
| Vault-wide Bible-link check | clean | 0 links name one book and open another; 0 open a verse neither numbering gives; 606 shifted English → Hebrew; 2,222 in shift zones linked as written; 3 flagged chapter-only (Obadiah 15-21, Jude 17-25 ×2) are right, because those books have one chapter. |

## X1 – the other 34 Prayer Book psalm-verse links (option a)

Each link keeps its label; only the target note changes, from the JPS psalm to the BCP Psalm note with the printed number. The checker read all 34: the BCP verse at the printed number is the verse quoted, and it is the same verse the current JPS link opens.

| Note | Line | Label | Before (target) | After (target) |
|---|---|---|---|---|
| Concerning the Psalter | 38 | Psalm 1:6 | `Psalms 001#^1-6` | `BCP Psalm 001#^1-6` |
| Concerning the Psalter | 52 | Psalm 68:4 | `Psalms 068#^68-5` | `BCP Psalm 068#^68-4` |
| Concerning the Psalter | 52 | Psalm 83:18 | `Psalms 083#^83-19` | `BCP Psalm 083#^83-18` |
| Offertory Sentences - HE II | 26 | Psalm 50:14 | `Psalms 050#^50-14` | `BCP Psalm 050#^50-14` |
| Offertory Sentences - HE II | 28 | Psalm 96:8 | `Psalms 096#^96-8` | `BCP Psalm 096#^96-8` |
| Offertory Sentence - HE 1 | 26 | Psalm 50:14 | `Psalms 050#^50-14` | `BCP Psalm 050#^50-14` |
| Offertory Sentence - HE 1 | 28 | Psalm 96:8 | `Psalms 096#^96-8` | `BCP Psalm 096#^96-8` |
| The Sunday of the Passion - Palm Sunday | 71 | Psalm 118:19-29 | `Psalms 118#^118-19` | `BCP Psalm 118#^118-19` |
| The Great Vigil of Easter | 120 | Psalm 33:1-11 | `Psalms 033#^33-1` | `BCP Psalm 033#^33-1` |
| The Great Vigil of Easter | 120 | Psalm 36:5-10 | `Psalms 036#^36-6` | `BCP Psalm 036#^36-5` |
| The Great Vigil of Easter | 138 | Psalm 33:12-22 | `Psalms 033#^33-12` | `BCP Psalm 033#^33-12` |
| The Great Vigil of Easter | 164 | Psalm 42:1-7 | `Psalms 042#^42-2` | `BCP Psalm 042#^42-1` |
| The Great Vigil of Easter | 164 | Psalm 42:1-7 | `Psalms 042#^42-2` | `BCP Psalm 042#^42-1` |
| Morning Prayer - Rite Two | 99 | Psalm 118:24 | `Psalms 118#^118-24` | `BCP Psalm 118#^118-24` |
| Morning Prayer - Rite Two | 121 | Psalm 19:4 | `Psalms 019#^19-5` | `BCP Psalm 019#^19-4` |
| Morning Prayer - Rite Two | 125 | Psalm 105:1 | `Psalms 105#^105-1` | `BCP Psalm 105#^105-1` |
| Morning Prayer - Rite Two | 131 | Psalm 122:1 | `Psalms 122#^122-1` | `BCP Psalm 122#^122-1` |
| Morning Prayer - Rite Two | 133 | Psalm 19:14 | `Psalms 019#^19-15` | `BCP Psalm 019#^19-14` |
| Morning Prayer - Rite Two | 135 | Psalm 43:3 | `Psalms 043#^43-3` | `BCP Psalm 043#^43-3` |
| Morning Prayer - Rite Two | 247 | Psalm 95:1-7 | `Psalms 095#^95-1` | `BCP Psalm 095#^95-1` |
| Morning Prayer - Rite One | 97 | Psalm 118:24 | `Psalms 118#^118-24` | `BCP Psalm 118#^118-24` |
| Morning Prayer - Rite One | 119 | Psalm 19:4 | `Psalms 019#^19-5` | `BCP Psalm 019#^19-4` |
| Morning Prayer - Rite One | 123 | Psalm 105:1 | `Psalms 105#^105-1` | `BCP Psalm 105#^105-1` |
| Morning Prayer - Rite One | 129 | Psalm 122:1 | `Psalms 122#^122-1` | `BCP Psalm 122#^122-1` |
| Morning Prayer - Rite One | 131 | Psalm 19:14 | `Psalms 019#^19-15` | `BCP Psalm 019#^19-14` |
| Morning Prayer - Rite One | 133 | Psalm 43:3 | `Psalms 043#^43-3` | `BCP Psalm 043#^43-3` |
| Morning Prayer - Rite One | 244 | Psalm 95:1-7 | `Psalms 095#^95-1` | `BCP Psalm 095#^95-1` |
| Evening Prayer - Rite Two | 41 | Psalm 141:2 | `Psalms 141#^141-2` | `BCP Psalm 141#^141-2` |
| Evening Prayer - Rite Two | 45 | Psalm 96:9 | `Psalms 096#^96-9` | `BCP Psalm 096#^96-9` |
| Evening Prayer - Rite Two | 49 | Psalm 16:7 | `Psalms 016#^16-7` | `BCP Psalm 016#^16-7` |
| Evening Prayer - Rite One | 42 | Psalm 141:2 | `Psalms 141#^141-2` | `BCP Psalm 141#^141-2` |
| Evening Prayer - Rite One | 46 | Psalm 96:9 | `Psalms 096#^96-9` | `BCP Psalm 096#^96-9` |
| Evening Prayer - Rite One | 50 | Psalm 16:7 | `Psalms 016#^16-7` | `BCP Psalm 016#^16-7` |
| Concerning the Service - An Order of Worship for the Evening | 32 | Psalm 36:5-9 | `Psalms 036#^36-6` | `BCP Psalm 036#^36-5` |

## X2 – the numbering rule (ops 2–4, with the checker's two fixes)

**Op 2, the concordance (under "## 1. The 54 Parashiot Concordance Table").** Source: B-findings.json B21 fix; E-findings.json E3 fix; the four rows now open Torah 08 ^32-4, Torah 25 ^6-1, Torah 42 ^30-2, Torah 51 ^29-9 (all 54 range links checked against the Torah notes' first and last verse ids)

Before:
```text
## 1. The 54 Parashiot Concordance Table
```
After:
```text
## 1. The 54 Parashiot Concordance Table

The *Biblical Range* column gives each parashah's boundaries in Hebrew (JPS) verse numbers, so its links go to the verse as written, with no English-to-Hebrew shift.
```

**Op 3, *Prompts/Map new connections*, Part A rule 1 (a new bullet).** Source: E-findings.json E26 fix (1)-(4); Phase 1 changes (6 Oct 2026).md (E2, E7, B21 items); BCP Psalm 074 ^74-15 'Yours is the day' = Psalms 074 ^74-16 'the day is Yours'

Before:
```text
   - Zohar, Hasidic texts, Rashi and the Judaica already use Hebrew numbering: link as written.
```
After:
```text
   - Zohar, Hasidic texts, Rashi and the Judaica already use Hebrew numbering: link as written.
   - The folder does not decide every case. A reference marked LXX, Septuagint or Vulgate ("LXX Ps 81:6") links to its Texts/LXX note as written; this is the one case where a canonical book goes to the LXX. Psalm verses cited in the BCP link to the BCP Psalm notes (Library/BCP 1979/09 The Psalter/), which keep the BCP's own verse numbers (BCP Psalm 74:15 is JPS 74:16). The parashah ranges in the crosswalk tables are in Hebrew numbering: link as written. In the dry run, list every shifted link outside Texts/RCL/ and Library/BCP 1979/ with its sentence, so I can catch a writer who used the Hebrew numbers.
```

**New op, the same prompt, rule 5 (checker's fix: no contradiction with op 3).** Source: drafts/t3/verify/check.md, problem 4

Before:
```text
never send canonical references to the LXX.
```
After:
```text
never send canonical references to the LXX, except a reference marked LXX, Septuagint or Vulgate (rule 1).
```

**Op 4, Vault Guide, "Two numberings" (line 73), as drafted: use if X1 = a and L7 = ★.** Source: E-findings.json E2, E3, E26 fixes; Phase 1 changes (6 Oct 2026).md

Before:
```text
The Zohar, Hasidic texts, Rashi and the Judaica already use the Hebrew numbering and are linked as written.
```
After:
```text
The Zohar, Hasidic texts, Rashi and the Judaica already use the Hebrew numbering and are linked as written. The folder does not decide every case: a reference marked LXX, Septuagint or Vulgate links to its `Texts/LXX` note as written (`LXX Ps 81:6`); a psalm verse the Prayer Book cites links to its BCP Psalm note, because the BCP Psalter numbers verses its own way (BCP Psalm 74:15 is JPS 74:16); the parashah ranges in the crosswalk tables are in Hebrew numbering and are linked as written; and where an author cites the Hebrew numbers (Ehrman's `Ps 22:2`), the link follows the author. A linking pass lists every shifted link outside `Texts/RCL/` and `Library/BCP 1979/` for a human look.
```

**Op 4, variant for X1 = b or L7 not ★** (checker's fix: the clause holds for new links only). After:
```text
The Zohar, Hasidic texts, Rashi and the Judaica already use the Hebrew numbering and are linked as written. The folder does not decide every case: a reference marked LXX, Septuagint or Vulgate links to its `Texts/LXX` note as written (`LXX Ps 81:6`); new links to a psalm verse the Prayer Book cites go to its BCP Psalm note, because the BCP Psalter numbers verses its own way (BCP Psalm 74:15 is JPS 74:16); the parashah ranges in the crosswalk tables are in Hebrew numbering and are linked as written; and where an author cites the Hebrew numbers (Ehrman's `Ps 22:2`), the link follows the author. A linking pass lists every shifted link outside `Texts/RCL/` and `Library/BCP 1979/` for a human look.
```

## X3 – E8, the two links that follow a slip in the source

Current lines (the Tanya note as it is after last night's track-2 link at line 75):

- *Tanya – Iggeret HaTeshuvah 01*, line 69:
```text
[^21]: [[Psalms 089#^89-23|Psalms 89:23]].
```
- *Essential Kabbalah 15 – Notes*, line 943 (full line):
```text
**garments: the stories of this world** Several of the Torah’s commandments are clothed and conveyed in story; see [[Torah 08 - Vayishlach#^32-24|Genesis 32:24–32]]; [[Torah 36 - Beha'alotcha#^9-6|Numbers 9:6–14]]; [[Torah 37 - Sh'lach#^15-32|15:32–36]]; [[Torah 41 - Pinchas#^27-1|27:1–11]]. Furthermore, biblical narrative often transmits moral teaching.
```
**(a) keep the printed link, add a marked note that links the verse meant**

- Tanya - Iggeret HaTeshuvah 01: `[^21]: [[Psalms 089#^89-23|Psalms 89:23]].` →
```text
[^21]: [[Psalms 089#^89-23|Psalms 89:23]] [vault: the words quoted are at [[Psalms 089#^89-33|89:33]]].
```
- Essential Kabbalah 15 - Notes: `see [[Torah 08 - Vayishlach#^32-24|Genesis 32:24–32]];` →
```text
see [[Torah 08 - Vayishlach#^32-24|Genesis 32:24–32]] [vault: = [[Torah 08 - Vayishlach#^32-25|32:25–33]] in JPS numbering];
```

**(b) link the verse meant, keep the printed number as the label, say so**

- Tanya - Iggeret HaTeshuvah 01: `[^21]: [[Psalms 089#^89-23|Psalms 89:23]].` →
```text
[^21]: [[Psalms 089#^89-33|Psalms 89:23]] [vault: so printed; the words quoted are at 89:33, which the link opens].
```
- Essential Kabbalah 15 - Notes: `see [[Torah 08 - Vayishlach#^32-24|Genesis 32:24–32]];` →
```text
see [[Torah 08 - Vayishlach#^32-25|Genesis 32:24–32]] [vault: so printed; = 32:25–33 in JPS numbering, which the link opens];
```

**(d) remove the link, keep the text, list it in the phase 3 record**

- Tanya - Iggeret HaTeshuvah 01: `[^21]: [[Psalms 089#^89-23|Psalms 89:23]].` →
```text
[^21]: Psalms 89:23.
```
- Essential Kabbalah 15 - Notes: `see [[Torah 08 - Vayishlach#^32-24|Genesis 32:24–32]];` →
```text
see Genesis 32:24–32;
```

**(c) leave both lines as they are**, and add this line to the phase 3 record:
```text
- Two citations left as the source prints them (E8). Tanya, Iggeret HaTeshuvah 1, n. 21 prints "Psalms 89:23" for words that are at 89:33; the link opens 89:23. Matt, The Essential Kabbalah, notes p. 208, prints "Genesis 32:24–32" for the wrestling and the sinew rule, which are 32:25–33 in the vault (JPS) numbering; the link opens 32:24.
```

Notes: in (a) and (b) the inserted bracket begins `vault:` because both sources use square brackets for their own insertions (Kehot about 750 pairs in the Tanya notes; Matt 26 in this file, written escaped as `\[…\]`). The inserted brackets are not escaped; both forms render the same. Option (a) puts a link inside a bracket (`]]]` in the Tanya line): look at it once in Reading view after it is applied. Backlinks are the same in every option, because both verses sit in the same note.

## X4–X9 – E16, *Linguistic Creation in Kabbalah and Trika*

Exact-verse links: the drafts propose none. The note's one Tantrāloka link (`Tantrāloka 3.1ff`) already opens the verse its label names, it links no chapter note, and it names no verse in plain text. Verse links come only with the rewordings below. Not taken up by the drafts (reviewer's note): the note's Zohar link, `[[Texts/Zohar/Zohar 1 - Genesis/Zohar 1.06 - Haqdamat Sefer ha-Zohar|Haqdamat Sefer ha-Zohar (Matt tr.)]]` (line 36), opens the top of Zohar 1.06; the letters passage it describes is on 1:2b–3b (the letters enter from line 66 of that note). `^z1-2b` exists and ends the paragraph at line 58, where the 1:2b marker stands. No op drafted; listed under *Not done* in the section.

**X4 (E16 Q1, T27): kṣa as earth** – line 40. Source: TA 3.142, 3.153 [Viveka], 3.157, 3.180 [Viveka], 3.181; 11.49, 11.53 [Viveka]; drafts/t3/e16 Q1 with its checker's corrections

Before:
```text
which then crystallizes into the consonants down to the earth element *kṣa*.
```
After:
```text
which then crystallizes into the consonants ([[Tantraloka 03.142|TĀ 3.142]]): the stops *ka* to *ma* stand for the principles from earth up to *puruṣa* ([[Tantraloka 03.149|TĀ 3.149–153]], with Jayaratha), then come the semivowels and the four *ūṣman*s, and last the fiftieth letter ([[Tantraloka 03.181|TĀ 3.181]]), which Jayaratha names as *kṣa*, *ka* joined to *sa* (on [[Tantraloka 03.180|3.180]]). In the path of letters of Āhnika 11, *kṣa* is the letter of earth ([[Tantraloka 11.049|TĀ 11.49–53]], with Jayaratha).
```

**X4, the "add see" option** – line 40. Source: TA 11.49-53

Before:
```text
down to the earth element *kṣa*.
```
After:
```text
down to the earth element *kṣa* (see [[Tantraloka 11.049|TĀ 11.49–53]]).
```

**X5 (E16 Q2, T14): the 34 consonants** – line 26. Source: TA 3.153, 3.158, 3.179 [Viveka: hakarena saha], 3.180-181; drafts/t3/e16 Q2

Before:
```text
34 *Vyañjanas* (5 vargas of 5 stops + 4 semivowels + 4 sibilants)
```
After:
```text
34 *Vyañjanas* (5 vargas of 5 stops + 4 semivowels + 4 *ūṣman*s, *śa ṣa sa ha*, + *kṣa*)
```

**X6 (E16, the finding's third claim): "12 Elementals"** – line 26. Source: Zohar 2.02 - Parashat Lekh Lekha, n. 20 (SY 2:1); Zohar 7.08 - Parashat Aharei Mot, n. 552 (SY 5:1); E16 checker

Before:
```text
12 Elementals)
```
After:
```text
12 Simples)
```

**X7 (E16 Q3, T7): the bindu as "Initial Vibration"** – line 24. Source: TA 3.104, 3.110-111, 3.133b-134a; [Viveka] on 3.111; E16 checker

Before:
```text
| *Nāda* / *Bindu* (ं) |
```
After:
```text
| *Nāda* / *Bindu* (ं); in TĀ 3 the bindu is the fifteenth phoneme, after *au*, the fourteenth ([[Tantraloka 03.104\|3.104]], [[Tantraloka 03.110\|3.110–111]]), and Śiva's own point, *śivabindu* ([[Tantraloka 03.133\|3.133–134]]) |
```

**X8 (E16 Q4, T3), optional wording only** (recommended: leave). Line 15, abstract. Instead of "Both traditions reject the idea of language as arbitrary social convention, viewing speech as …":
```text
Both traditions deny that language is mere convention. For Abhinavagupta ordinary words do live by convention (TĀ 11.70), but every convention rests on an awareness of the letters that does not depend on it (TĀ 11.66–73). Speech in that sense is the primordial, divine energy …
```

**X9 (E16 Q5, T6/T17/T32), optional qualifier only** (recommended: leave). Line 23, row 1, after "beyond speech.":
```text
beyond differentiated speech; in the TĀ anuttara is itself the first phoneme a (3.227) and supreme speech (parā vāk, Jayaratha on 3.236).
```

## X10–X15 – E17, *Paratrisika-vivarana and the Alphabet of Creation*

Exact-verse links: the note names no Tantrāloka, MŚV or Zohar verse by number. It names one Śivasūtra verse, "Sūtra 1.4" (line 26), but the vault has the Śivasūtra only as PDFs and Muktabodha e-texts (M00349, M00083, M00667), with no verse notes, so there is nothing to link at a verse. Its 2 ready links (above) are to held editions.

**X10 (E17 Q1, statement 41): Mātṛkā "descent", Mālinī "return"** – line 42. Source: TA 15.124 [Viveka], 15.128cd-129ab, 15.132, 29.201-202 [Viveka], 29.243 [Viveka in 29.247]; E17 checker

Before:
```text
into the supreme non-dual state.
```
After:
```text
into the supreme non-dual state.

*In the vault's Tantrāloka:* Mālinī is tied to withdrawal ([[Tantraloka 15.132|TĀ 15.132]]) and to *samāveśa* ([[Tantraloka 29.201|29.201–202]], with Jayaratha), and Jayaratha notes that other scriptures set her out both ways, by emission and by withdrawal (on [[Tantraloka 15.124#Viveka|15.124]]). He also reads the *na*-to-*pha* order as emission (on 29.243; his comment is in [[Tantraloka 29.247#Viveka|29.247]]), while uttering from *pha* back to *na* withdraws the circle of the paths ([[Tantraloka 15.128|15.128–129]]).
```

**X11 (E17 Q2, statement 16): "na-pha-ḍha"** – line 24. Source: TA 15.121-125, 15.128ab; Padoux, Tantric Mantras 05

Before:
```text
(*na-pha-ḍha*...)
```
After:
```text
(*na* … *pha*)
```

**X12 (E17 Q3): spellings**

| Line | Before | After |
|---|---|---|
| 51 | `*Varpoddhāra* & *Pratyāhāra*` | `*Varṇoddhāra* & *Pratyāhāra*` |
| 52 | `The silent gutter breath` | `The silent guttural breath` |

**X13 (E17 Q4), option a**

| Line | Before | After |
|---|---|---|
| 23 | `**Paul Muller-Ortega** (1992)` | `**Paul Muller-Ortega** (undated typescript, on the *Parātrīśikā-laghuvṛtti*, PTLV)` |
| 23 | `[[Library/Catalog/Trika/Born of the Yogini's Heart` | `[[Texts/Muktabodha/parAtrIzikAlaghuvRtti-M00042\|PTLV (Muktabodha)]]<br>[[Library/Catalog/Trika/Born of the Yogini's Heart` |
| 15 | `*Parātrīśikā-vivaraṇa* (PTV / PTLV)` | `*Parātrīśikā-vivaraṇa* (PTV)` |

**X15 (E17 Q6): "(not in the vault)"**

| Line | Before | After |
|---|---|---|
| 26 | `**Jaideva Singh** (*Siva Sutras: The Yoga of Supreme Identity*)` | `**Jaideva Singh** (*Siva Sutras: The Yoga of Supreme Identity*) (not in the vault)` |
| 27 | `**Subrahmanya Sastri** (English translation & commentary)` | `**Subrahmanya Sastri** (English translation & commentary) (not in the vault)` |

**X12, the second option (also reword the gloss)**, line 51. Instead of "recombining phonemic roots to dissolve mental conditioning (*vikalpa-saṃskāra*)":
```text
extracting letters, and gathering the whole alphabet, a to ha, which then dissolves into anuttara (TĀ 3.204–205, with Jayaratha; 6.238)
```

**X14 (E17 Q5): the two source lines, corrected by the checker (built and checked after your answer).**

After the SAUḤ list (line 38):
```text
*In the vault:* Jayaratha reads TĀ 4.186–4.189 as the extraction of SAUḤ (sa, au and the visarga), citing Parātrīśikā 10 (tṛtīyaṃ brahma suśroṇi) for the letter sa (on 4.187).
```
After the matrix (line 53):
```text
*Sources in the vault for parts of this table:* letters as Śakti and her body (TĀ 3.198; 15.117–126); a as anuttara (TĀ 3.204, with Jayaratha); stones that build houses (Tanya, Iggeret HaKodesh 05, citing Sefer Yetzirah 4:12); permutation and number-play (Matt, Essential Kabbalah 08: Sefer Yetsirah 2:4–5, Abulafia); the heart where SAUḤ pulsates (TĀ 4.182–4.188, with Jayaratha); lev = 32 = the paths of Wisdom (Zohar 9.05, n. 37); alef as Keter (Zohar 1:3b, n. 110); the fifty gates of Binah (Zohar 3:262a, n. 58); the thirty-two paths (Sefer Yetsirah 1:1, in Matt). No vault source was found for the other glosses.
```

Draft text replaced by these: op 6 said "the Tantrāloka takes SAUḤ apart … at TĀ 4.186–4.191" (wrong range; the Mūla never names SAUḤ, Jayaratha does; 4.189cd–4.191ab treat the piṇḍanātha), and op 7 ended "The other glosses have no source yet" (false for five glosses).

