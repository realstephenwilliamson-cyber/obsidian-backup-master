---
type: report
date: 2026-10-06
tags:
  - vault-analysis
---
# Checked findings (analysis of 6 Oct 2026)

Phase 1 of the [[AI/Archive/Claude outputs/0 Plan - read me first|October plan]] checked the findings of the vault analysis ([[Agent summaries]] and the A–H reports in this folder) before anything else was changed.

**How they were checked.** 221 of the 263 findings were checked: every finding of kind *wrong*, *broken*, *gap* or *fragile*, and every proposed fix marked safe. One checking agent per batch of about ten tried to disprove each finding against the vault (a text snapshot taken by Obsidian at 16:06) or against the source it cites. Every finding the first checker did not fully confirm got a second, independent look (74 second looks). Seven were also tested in Obsidian itself (F3, F17, G1, G2, G37, G41, G48). The other 42 findings are proposals and notes whose fix is a decision; they were not checked and are listed with the phase that will take them up.

**Result:** 148 hold, 67 hold in part (the count or scope is corrected in the table), 6 are disproved, 42 were not checked. *Phase* is the phase of the plan that takes the finding up; *Now* says what phase 1 did.


## The ten most valuable improvements

| # | Improvement | Findings | Area | Effort | Safe or decision | Phase |
|---|---|---|---|---|---|---|
| 1 | **Repair the Tantrāloka root text.** In the 18 āhnikas the DCS covers, 53 of 5,444 root half-lines are outside the Mūla blocks and 38 lines of Jayaratha's prose are inside them; āhnika 37 had 28 short verses. | A1, A2, G36 | A, G | large | decision | 2 (āhnika 37 done in phase 1) |
| 2 | **Make the homily take the right feast.** On Sunday 1 Nov 2026 the button offered Proper 26A, weekday feasts took the coming Sunday, the 2027–28 feasts had Year A readings, and the Polyphonic template could not resolve a link. | C11–C14, F10, F13, F14, B23, G44 | C, F | medium | decision | 1 (done) |
| 3 | **Stop blank notes on a second device.** Templater's create trigger is kept per device and off by default; the Home buttons now fill the note themselves. Still to do: Templater's excluded folders and the switch on the phone (your settings), and a new-device checklist in the Guide. | F1, F2, F24, F25 | F | small | safe; settings yours | 1 (done in part), 8 |
| 4 | **Link the Daily Office lessons.** 121 lessons are plain text (all the Apocrypha and Ecclesiastes, and about 30 other forms); 21 of the 24 days from 16 Oct to 8 Nov have one. | C30, E11 | C, E | small | safe | 1 (done: 120 of 121) |
| 5 | **Let LXX verses be linked.** 28,690 verse ids sit mid-paragraph; Obsidian registers 1,117 of them (tested), so single verses cannot be linked or embedded, and the verses run together in Reading view. One scripted pass (a blank line after each verse) fixes both. | C22, G37, G48 | C, G | medium | safe | 3 |
| 6 | **Rebuild Augustine's Tractates.** No tractate links to John; footnotes are spliced into the prose in 49–124 and lost in 1–48. | C1, C2, E12, G20 | C, E, G | large | decision | 3 |
| 7 | **Correct the Zohar links.** About 630 Midrash ha-Ne'lam and 200 Piqqudin links open main-text or Soncino notes, and 128 go to Soncino where a Pritzker note has the folio. | B5–B10, B22, E1 | B, E | medium | safe | 3 (E1 in phase 1) |
| 8 | **Record Dyczkowski's numbering.** About a fifth of the verses he prints are numbered differently from the vault, and no note says so. | A3, A21 | A | large | decision | 5 |
| 9 | **Connect the traditions.** No Tantrāloka passage links to or from a Jewish or Christian text; parashah notes link only Rashi. Fifteen anchored proposals are ready. | E20, E25, B31, E29–E43 | E, B | large | decision | 6 |
| 10 | **Check the catalog against the files.** Catalog errors cluster in the 123 notes with no "Checked against" line; ten notes have a wrong author, editor, year or identity. | G32, D6–D9, D22, A22, B33, C32, G27–G29 | D, G, A, B, C | medium | safe | 3 (40 notes in phase 1) |

Also done in phase 1: the Bases list the 640 catalog notes, not all 10,162 files under Library (F17, G1, G2, D15, D33).


## A. Trika and the Tantrāloka

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| A1 (= G36) | 53 of 5,444 DCS half-lines are outside the Mula blocks in DCS's 18 ahnikas (not 19); ahnika 37 has 28 damaged notes, not 5, and 34.3 is damaged too. | partly | decision | 2 | āhnika 37 and 34.3 done (b3, b3b, B6); the rest phase 2 |
| A2 (= G36) | 38 lines of Jayaratha's prose or quotation sit inside the Mula blocks of 37 verse notes in the DCS ahnikas, plus 15.203. | holds | safe | 2 | āhnika 37 and 34.3 done (b3, b3b, B6); the rest phase 2 |
| A3 | About a fifth of readable verses carry a different number in Dyczkowski (shifted or split) in ahnikas 1-6, 8, 11, 13, 15, 16, 19; no note says so. | holds | decision | 5 |  |
| A4 | All 5,845 Dyczkowski page links resolve to the right volume and printed page; 16 are deliberate page ranges. | holds | safe | 5 |  |
| A5 | Already fixed: Welcome now says the map gives 228 anchor verses (88 estimated); no note claims every verse any more. | **disproved** | safe | – | already fixed |
| A6 | The KSTS anchor table contradicts itself in at least nine places; which value is right needs the scans. | holds | decision | 2 |  |
| A7 | The KSTS edition is not in the vault; Guide and Welcome now say so; the Hub label and four download URLs still mislead. | partly | decision | 2 |  |
| A8 | 5,845 verse notes and 37 chapter notes are consistent in numbering, properties, sections and navigation. | holds | safe | 8 |  |
| A9 | Devanagari and IAST agree in all 5,845 verses because the IAST is a mechanical transliteration | not checked (proposal) | decision | - |  |
| A10 | The Tantraloka index note has two stale sentences, and chapter notes 24 and 33 point to a Closing section they lack. | holds | safe | 1 | done (B6) |
| A11 | Quotation marks lost and first letters changed in Jayaratha's text (an artefact of the Muktabodha files) | not checked (proposal) | decision | 2 |  |
| A12 | Secondary-literature index: 130 sources, 4,711 page links, 2,134 verses, all consistent; I could not re-read the sampled errors. | holds | safe | 1 | two entries to move: with A20 (phase 3) |
| A13 | Dyczkowski volume files keep download-site names that break the naming rule | not checked (proposal) | decision | 3 |  |
| A14 | The study plan covers every verse once, in order, in 1,099 correct days; parashah, lectionary, Dyczkowski and milestone columns all check out. | holds | safe | 8 |  |
| A15 | Already fixed: Today's verses now matches 'pp.' links; the translation fold-out shows on all five days. | **disproved** | safe | – | already fixed |
| A16 | Today's verses loop silently drops verses after a missing note; today only 1.76 is missing and no portion spans it. | holds | safe | 1 | done (B6) |
| A17 | All 499 Muktabodha notes link one DEV and one IAST e-text; all 998 resolve (one differs only in case) and no e-text is orphaned. | holds | safe | 8 |  |
| A18 | Obsidian cannot open the 998 Muktabodha .txt e-texts, and neither core search nor Omnisearch (as set) searches their contents. | holds | decision | 4 |  |
| A19 | All 499 Muktabodha `year` values are quoted text: 245 four-digit years, 233 "", 21 "Pre-1900". Catalog notes hold numbers or empty. | partly | safe | 3 |  |
| A20 | TAK II's 202 Tantraloka references (177 existing verses) are missing from the secondary-literature index because its legacy font reads TĀ as 'TÛ'. | holds | safe | 3 |  |
| A21 | The 37 chapter notes hold only Sanskrit (opening, first lines, closing); Dyczkowski's held contents file offers about 1,100 section headings to outline them. | holds | decision | 5 |  |
| A22 | The Dyczkowski catalog note calls the translation 'unpublished', but all eleven volumes carry '© 2023' and their own ISBN; two sentences are stale. | holds | safe | 1 | done (B6) |
| A23 (= G7, B26, D23 (part)) | 112 catalog notes (36 in Trika) and Guide l.110 still say OCR originals are in .trash/ocr-originals-2026-10-05; the trash was emptied. | partly | safe | 3 | the Guide sentence (b5) and 6 notes (B6); the rest phase 3 |
| A24 | 68 of the 151 Trika catalog notes are not named "Author - Short title" | not checked (proposal) | decision | 3 |  |
| A25 (= G43) | The Incomplete Sets note recommends acquiring Vasudeva's Yoga of the Malinivijayottaratantra, which is held and is the index's third-largest source. | holds | safe | 1 | done (B6) |
| A26 | The KSTS volumes note's verse-count table puts ahnikas 5 and 7 in the wrong volumes, differs from the vault in eight ahnikas and dates vol. X ~1927 (record: 1933). | holds | safe | 2 |  |
| A27 | Word analysis covers 19 of 37 ahnikas and none of the practice run | not checked (proposal) | decision | 7 |  |
| A28 | Index of the scriptures Jayaratha cites, verse by verse | not checked (proposal) | decision | 6 |  |
| A29 | Held: none of Sanderson's five Trika papers (free PDFs), Gnoli, Silburn/Padoux, TAK III, Goudriaan-Gupta or Padoux Contributions III; GRETIL coverage is likely complete but unconfirmed. | holds | decision | 7 |  |
| A30 (= E15 (part)) | The Matrix's Tantraloka row names three catalog notes, as code text, that do not exist under those names; this is a subset of E15. | holds | safe | 3 | done (B6) |

## B. Torah, Rashi, Zohar and Hasidut

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| B1 | Torah notes are complete: 54 parashiot with standard boundaries and 5,846 verses; every chapter count matches Sefaria. | holds | safe | 8 |  |
| B2 | Prophets and Writings are complete: 742 chapter notes, 17,360 verses, all chapter counts equal Sefaria's, English only. | holds | safe | 8 |  |
| B3 | In Ezekiel 24 the anchors ^24-22/23/24 hold verses 24, 22 and 23, with leftover {24}/{22}/{23} labels. | holds | safe | 1 | done (B6) |
| B4 | Rashi notes: Hebrew words are left untransliterated in 1,619 of 7,787 comment paragraphs; lemmas and names follow Metsudah, not JPS | not checked (proposal) | decision | 3 |  |
| B5 | Zohar folio ids sit at the print-page head; the folio turn is usually 1-3 paragraphs later, contrary to two index sentences. | holds | safe | 3 | done (B6) |
| B6 | Twelve part-3 folio sides have Pritzker text but no block id; 16 links to 3:33b and 3:151a go to Soncino. | holds | safe | 3 |  |
| B7 | Zohar folio index covers volumes 1-9 only: 404 ids from volumes 10 and 12 are missing, and its 'not marked' lists are stale. | holds | safe | 3 |  |
| B8 | About 630 (MhN)-tagged and 200 (Piq)-tagged Zohar links open main-text or Soncino notes although volume 10 or 12.06 has the folio. | holds | safe | 3 |  |
| B9 (= E1 (overlaps)) | Nine Zohar links in six notes open the wrong folio because a leading 1 was read as the volume (112a opens 1:12a). | holds | safe | 3 | done with E1 (B6) |
| B10 | 128 Zohar links go to Soncino notes although a Pritzker note has the folio, 124 of them for volumes 10 and 12; 27 Soncino notes lack the Pritzker line. | holds | safe | 3 |  |
| B11 | Pritzker vol. 11 is absent; about 1,526 plain ZH 60-93 citations and about 880 (ST)/(Mat)/(Tos) links in 76 notes lack its text. | partly | decision | 7 |  |
| B12 | Welcome calls the ~1,400 Sefaria notes 'folios the Pritzker volumes don't' have; 1,208 of the 1,274 Soncino notes duplicate Pritzker folios. | holds | safe | 1 | done (B6) |
| B13 | Zohar Chadash notes are 98.6% Aramaic: 64 of 4,421 paragraphs have any English | not checked (proposal) | decision | 3 |  |
| B14 | Sifra di-Tsni'uta defines six folio ids twice (plain and annotated copy); a link can reach only one copy. | holds | safe | 3 |  |
| B15 (= G38) | Pritzker volume 1's three text notes lack 219 of 452 print-page markers; no other Zohar note has gaps. | holds | decision | 4 |  |
| B16 (= G17) | In 12 Mei HaShiloach non-parashah notes, 57 of 68 comparable teaching headings give Sefaria's chapter:running-number, not the cited verse. | partly | safe | 3 |  |
| B17 (= G19 (part)) | Tanya is complete (122 notes, Kehot, CC-BY-NC) but has no paragraph ids and no previous/next links. | holds | safe | 3 |  |
| B18 (= E19) | No Zohar citation in Tanya (382, plus ~106 Tikkunei) or Mei HaShiloach (~59-64 by book or parashah name) is a link. | partly | safe | 3 |  |
| B19 (= G18, E9) | About 1,000 scripture citations in Mei HaShiloach's text and footnotes are plain text; about 400 are Prophets/Writings with no link anywhere. | partly | safe | 3 |  |
| B20 | Of Mei HaShiloach's 487 parashah teachings, 455 have Torah links: the opening verse is among them in 408, first in 322. | holds | safe | 3 |  |
| B21 (= E3, G42) | Four Biblical Range links in the RCL concordance are shifted as if English-numbered; two open the previous parashah's note. | holds | safe | 1 | done (B6) |
| B22 | Concordance Zohar column: 6 cells point at another parashah, 3 at mostly-Aramaic Zohar Chadash notes, Devarim empty; 12.11 has English for 3. | holds | decision | 3 |  |
| B23 (= C13, F13, G44) | Homily (Polyphonic) template's four parashah links join a folder and `parashah`. No value can resolve more than one of them, and the default resolves none. | holds | decision | 1 | done (b2: homily) |
| B24 | The study plan's parashah column is right on every Saturday checked: all 166 against a Diaspora calendar library, and all 51 of 5788 against Hebcal. | holds | safe | 8 |  |
| B25 | No haftarah table exists. No parashah note, plan row or concordance row names the week's prophetic reading. | holds | decision | 3 |  |
| B26 (= A23, G7) | Four Judaica catalog notes say the pre-OCR scan is in .trash/ocr-originals-2026-10-05. It is not; .trash was emptied. | holds | safe | 3 | the Guide sentence (b5) and 6 notes (B6); the rest phase 3 |
| B27 | The vault has only Mei HaShiloach volume I. On Sefaria, only 3% of volume II has any English (community translation). | holds | decision | 7 |  |
| B28 | Commentaries and Hasidic texts that Sefaria offers in English under open licences and that would sit beside Rashi verse by verse | not checked (proposal) | decision | 7 |  |
| B29 | The Judaica library has almost no secondary studies of the Zohar, Izbica or Tanya: no Scholem, Tishby, Green, Liebes, Wolfson or Magid. | holds | decision | 7 |  |
| B30 | The Kabbalah Centre Zohar PDF holds English text for the portions the Pritzker and Soncino notes lack; its catalog note does not say what the file is | not checked (proposal) | decision | 3 |  |
| B31 | All 54 parashah notes link only to Rashi. Nothing leads from the Torah text to that week's Mei HaShiloach, Zohar or haftarah. | partly | safe | 3 |  |
| B32 | The 11 Pritzker glossaries (about 1,000 entries, 148 distinct headwords) overlap heavily, are unlinked from the Hasidic texts, and spellings differ by translation. | holds | decision | 6 |  |
| B33 | Pritzker Zohar catalog note: year 2019 matches no volume, the body says 'Zohar 1 through Zohar 9', and the subjects include Kabbalah and Zohar. | holds | safe | 1 | done (B6) |
| B34 | 301 span tags in 77 Pritzker notes (vols 1-9, mostly body text); build scripts in tools/ are absent; Rashi 'translator: Avrohom Davis' is unsourced. | partly | safe | 3 |  |
| B35 | Judaica file and catalog-note names mostly do not follow the Guide's naming rule | not checked (proposal) | decision | 3 |  |

## C. Bible and Christian sources

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| C1 (= E12, G20) | Augustine tractates 49-124 have glued footnote numbers and footnote text in sentences; 38-48 carry spliced translator's notes; 1-37 lost all footnotes; no definitions. | partly | decision | 3 |  |
| C2 (= E25 (part)) | None of the 124 tractate notes has a link, so John chapters show no tractate backlinks; the Guide wrongly says NT references are linked. | partly | safe | 3 | Guide sentence corrected (b5); Tractate 17 and the concordance ranges (B6); links phase 3 |
| C3 (= E6, G35) | Tractate 17 is labelled John 4:1-18 (an NPNF/CCEL misprint) but treats the healing at the pool, John 5:1-18. | holds | safe | 1 | done (B6) |
| C4 (= E5) | The concordance's tractate ranges for John 13-17 are wrong and disagree with the index note; four other rows omit chapter-spanning tractates. | holds | safe | 1 | done (B6) |
| C5 | Catena page map: John 1 should open PDF page 7 (not 8) and John 18 page 549 (not 556); the other 19 rows are right. | holds | safe | 1 | done (B6) |
| C6 | The Catena map is chapter-level only; a verse-to-page table can be built from the scan's 'VER.' running heads after OCR cleanup. | partly | safe | 3 |  |
| C7 | Texts/Fathers holds only Augustine; no work or study of Gregory of Nyssa exists; Maximus's Ambigua to John and Ad Thalassium are absent. | partly | decision | 7 |  |
| C8 | For an ordinary Sunday the Home button and Homily template produce the right note and readings; only Homilies.md's example name is wrong. | holds | safe | 1 | done (B6) |
| C9 | Proper notes hold only the semi-continuous track; two notes mix in the complementary psalm (Proper-28B and Reign-of-ChristC). | partly | decision | 3 |  |
| C10 | Where the RCL offers 'or' alternatives, the RCL notes keep only the first; only PresentationA records one. | holds | safe | 3 |  |
| C11 (= F14) | A homily note named with a weekday feast's date silently takes the coming Sunday's readings (e.g. Christmas Day 2026 gives Christmas 1B). | holds | safe | 1 | done (b2: homily) |
| C12 | On Sunday 1 Nov 2026 both Home's button and the Homily template take Proper 26A, although All Saints' Day is a Principal Feast. | holds | decision | 1 | done (b2); 6 Aug 2028 Transfiguration: phase 3 |
| C13 (= F13, G44, B23) | The Polyphonic template's lectionary link, four reading embeds and four parashah links cannot resolve. Its six fixed links do. Welcome line 59 overstates it. | partly | decision | 1 | done (b2: homily) |
| C14 (= F10) | The Fixed All Saints, Thanksgiving and Vigil notes hold Year A readings yet serve the 2027 and 2028 rows; Easter Evening is absent. | holds | safe | 1 | done (b2: homily) |
| C15 | Nothing links to a collect, and in each seasonal collect note 34 of 82 block IDs are named after 'Preface' headings, not the occasion. | holds | decision | 3 |  |
| C16 | RCL notes embed the psalm only from the JPS Tanakh; none links to the BCP Psalter or the LXX psalm, contrary to the concordance. | holds | decision | 3 |  |
| C17 | The earlier-homily lists match by note name. 22 groups (52 notes) share readings under different names, so the first misses come on 1–2 Jan 2028. | partly | decision | 3 |  |
| C18 | The hub links '2026-11-22 Christ the King' while Home's button makes '2026-11-22 Reign of Christ (A)'. The two names can produce duplicate homilies. | partly | safe | 1 | done (b4: hub link) |
| C19 | No NT Greek word links to its lexicon note, and lexicon notes are 200 of John 1's 240 backlinks. Searching the printed word often finds the lemma anyway. | partly | decision | 3 |  |
| C20 | 541 of 5,461 Greek lemma notes (1,777 occurrences) lack both a Dodson gloss and a Strong's number; John 7:53-8:11 is not lexicalised. | holds | safe | 3 |  |
| C21 | NT text is sound; Romans 16:25-27 (Advent 4B) lacks Greek in the body, and the Trinity A embed stops before the English Grace. | holds | safe | 1 | done (B6) |
| C22 (= G37) | In 1,116 LXX notes, 27,573 verse IDs sit mid-paragraph, so verse links and embeds likely fail; confirm in Obsidian. | holds | safe | 3 |  |
| C23 | LXX Ezra 11-23 duplicates Nehemiah 1-13 as a second Brenton transcription; the Ezra copy is cleaner, the Nehemiah copy has typos. | holds | decision | 3 |  |
| C24 | Every LXX note has a plain English alias (e.g. 'Psalms 111'); for Psalms 9-147, Jeremiah 25-51 and Proverbs 24-31 it names a different Hebrew chapter. | holds | decision | 3 |  |
| C25 | The Septuagint is English only; the index note still carries the builder's working remark | not checked (proposal) | decision | 3 |  |
| C26 (= G46) | The sample homily cites Job (not Acts) for Easter 5A, quotes words absent from Tractate 69, and is invisible to the hub and Sunday queries. | holds | decision | 1 | marked type: sample (your choice) |
| C27 | Two BCP notes are named 'Concerning the Celebration - Holy Eucharist (...)' but hold pp. 934 and 888; 'Individials' is misspelt. | holds | safe | 1 | done (B6) |
| C28 (= E13) | Proper-7C's Psalm section (Psalm 42 and 43) is empty, the only empty reading section among 874. | holds | safe | 1 | done (B6) |
| C29 | The Daily Office lectionary is complete and the script resolves 1,188 days to 2029 without warnings; three Wikisource differences favour the vault. | holds | safe | 8 |  |
| C30 | 121 Daily Office lessons are plain text, not about 95: all Apocrypha and Ecclesiastes plus about 30 other forms; 21 of 24 days from 16 Oct to 8 Nov affected. | partly | safe | 1 | done (B6: 120 of 121 lessons) |
| C31 | The BCP notes' Sunday lectionary is the 1979 table that resolution 2006-A077 replaced with the RCL from Advent 2007; nothing says so. | holds | safe | 1 | done (B6) |
| C32 | Four Christianity catalog notes omit or misstate title-page facts (ANF vol. 1, Brightman 1903, Schweitzer English 1910, Mishkan article on Luther). | partly | safe | 1 | done (B6) |
| C33 | The library lacks a modern commentary on John or any gospel, a Greek grammar, homiletics and BCP or lectionary commentary; patristic John commentary is held. | partly | decision | 7 |  |
| C34 | All 221 RCL notes cite 'Daily Readings © 2005'; CCT requires 'Revised Common Lectionary, Copyright © 1992 Consultation on Common Texts. Used by permission.' | holds | safe | 3 |  |
| C35 | What would make Saturday night easier: one 'for the preacher' block in the homily note, fed by properties on the RCL note | not checked (proposal) | decision | 6 |  |

## D. Philosophy of technics and memory

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| D1 (= E21, G47) | The hub's 'Plato — Phaedrus (Thamus & Theuth)' link and the concept note's 'Plato's Dialogues' link open Graham's Presocratics Part 2; the Matrix row also says Plato. | holds | decision | 3 |  |
| D2 (= E21, G47) | Links labelled 'Pirkei Avot' in the Second Domestication hub and in Engineered Cognitive Friction open the Rashi index; the vault has no Avot text. | holds | decision | 3 |  |
| D3 | The vault has no Plato dialogue and no Phaedrus 274-277, but Graham's Part 2 holds Protagoras 320c8-322d5 (the Epimetheus myth) in Greek and English. | partly | decision | 7 |  |
| D4 | The catalog's Leviathan is Bennett's 2004 modernised adaptation of Parts 1-2, yet three notes present it as the primary text, as 1651, or as complete. | holds | safe | 3 | done (B6); the Incomplete Sets entry in b5 |
| D5 | No complete Leviathan in Hobbes's words; Part IV and much of Part III are missing, though Baumgold prints ch. 39-41 and 43 whole. | partly | decision | 7 |  |
| D6 | The Ricoeur Writings and Lectures 4 catalog note names Daniel Frey as editor; the editor is Pierre-Olivier Monteil and the translator Kathleen Blamey. | holds | safe | 3 | done (B6) |
| D7 | Six catalog dates or editions taken from file names disagree with the copyright pages: Oneself, Acting Out, TT2, D&D2, Eichmann, Minima Moralia. | holds | safe | 3 | done (B6) |
| D8 | The 'Glendinning' catalog note is Iain Hamilton Grant's encyclopedia chapter, the source of his key Leviathan phrase, and no note links it. | holds | safe | 3 | done (B6) |
| D9 | The Time of the Image catalog note has no author and says 'not confirmed'; the book is by Zeigam Azizov (Halem 2020, series vol. 9). | holds | safe | 3 | done (B6) |
| D10 | The Technics and Time 2 file is an uncorrected 2008 proof; its old-style numerals are garbled in the text layer, so years and page numbers cannot be searched. | holds | decision | 3 |  |
| D11 | The Model of the Text scan breaks off mid-sentence at p. 333, and Disbelief and Discredit 1 lacks its index; neither catalog note says so. | holds | safe | 1 | done (B6) |
| D12 | Figuring the Sacred lacks pp. 259-304 (end of ch. 14, chs 15-19, start of ch. 20); the catalog note doesn't say which pages. | partly | safe | 1 | done (B6) |
| D13 | Incomplete Sets guide calls Bennett's Leviathan 1-2 complete, omits five partial philosophy files from section B, and lacks Ricoeur W&L vol. 5. | holds | safe | 1 | done (b5 and B6) |
| D14 (= F20) | Technics hub Literature Feed keeps the 10 newest-created name-matched notes; Leviathan, Technics and Time, Symbolic Misery and MHF are cut. | holds | decision | 6 |  |
| D15 (= F17) | Stiegler.base's author clause matches nothing, so the Nanjing Lectures and Neganthropocene catalog notes are missing (their PDFs likely appear). | partly | safe | 1 | done (b1: Bases) |
| D16 (= G3, G49, E23 (part)) | 26 unresolved links: hub 2, Scapegoat Reflex 1, Cybernetic Anamnesis CFP 1, and 22 links to 12 missing Cybernetic Leviathan .docx originals. | holds | decision | 3 |  |
| D17 | Seven concept notes' up: property disagrees with the hubs' hand-written matrices (or, for Engineered Cognitive Friction, with its own body Up: line). | holds | decision | 6 |  |
| D18 | Concept notes rarely point at the library: 18 of the 28 philosophy concepts link no catalog note, and only one gives a page | not checked (proposal) | decision | 6 |  |
| D19 | Husserl's time lectures, Being and Time, Dissemination and The Postmodern Condition are cited in his notes and papers but not held. | holds | decision | 7 |  |
| D20 | None of the Sea Peoples flowchart's thirteen core reads (R1-R13) is in the library; the essay's 17 Aug deadline has passed. | holds | decision | 7 |  |
| D21 | 102 of 120 philosophy catalog notes are linked from none of his notes; several central to the projects are among them | not checked (proposal) | decision | 6 |  |
| D22 | Stiegler and Ricoeur catalog notes mostly lack translator, publisher and pages, though the title and copyright pages give them. | holds | safe | 1 | done (B6) |
| D23 | Philosophy catalog: 39 off-pattern names, many empty fields, 53 notes without provenance, 13 stale .trash sentences (114 vault-wide), 88 bare file links. | holds | decision | 3 |  |
| D24 | His page citations in Cybernetic Anamnesis check out against the held copies, with one quotation not found | not checked (proposal) | decision | - |  |
| D25 | Foucault (spaced letters), For a New Critique (garbled ClearScan OCR) and Automatic Society 1 (CJK running heads, rn/m misreads) are marked searchable but search poorly. | holds | safe | 4 |  |
| D26 | Fink conversion is structurally complete (323 markers, 404 matched footnotes); its type:book index note shows as a second Fink work in the Library-wide bases. | holds | safe | 1 | nothing left (b1) |
| D27 | All 16 English Stiegler books on Kinsley's list are held; the free Ars Industrialis 'Anamnesis and Hypomnesis' essay is not; Bifurcate is CC open access. | partly | decision | 7 |  |
| D28 | Ricoeur gaps: Time and Narrative 1-3, From Text to Action, and Writings and Lectures 3 and 5 are not held. | partly | decision | 7 |  |
| D29 | Wiener's Cybernetics: the catalog has no year or edition; the file is the 1961 second edition, and MIT Press offers that edition open access | not checked (proposal) | decision | 3 |  |
| D30 | A small Texts/ shelf for the philosophy projects, so passages can be linked the way scripture is | not checked (proposal) | decision | 7 |  |
| D31 | The Scholars guide has only Indological scholars and Sanskrit collections; the Matrix's philosophy rows are code text, mislabel Graham as Plato and cite the wrong Heidegger. | holds | safe | 3 |  |
| D32 | All 45 concept notes have type, status and up:. There are 28 philosophy concepts (9 in both hubs) and 6 Claude drafts; nine notes are linked only from their hub. | holds | safe | 6 |  |
| D33 (= F17, G1, G2) | Library.base 'All' was filtered to Dyczkowski, and 7 of 12 bases took all 10,162 Library files; fixed in the live vault at 16:56. | partly | safe | 1 | done (b1: Bases) |
| D34 | 20 of the 32 Philosophy 'Also in your library' lists miss later same-author notes (32 of 73 vault-wide). | holds | safe | 3 |  |
| D35 | Russell's History of Western Philosophy carries subject 'Other', so the Philosophy index and the hub feed cannot see it; a few more subject placements to decide | not checked (proposal) | decision | 3 |  |

## E. Connections across traditions

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| E1 (= B9 (overlaps)) | Ten Zohar folio links in six Pritzker notes split folios like '149a' into part 1 plus '49a' and open the wrong folio. | holds | safe | 1 | done (B6) |
| E2 | 7 of 42 BCP psalm-verse links open the wrong JPS verse because the BCP Psalter numbers verses its own way; 145:14 is doubtful. | holds | safe | 1 | done (B6) |
| E3 (= B21, G42) | Four parashah-range links in the RCL concordance (rows 8, 25, 42, 51) were shifted and open one verse late or in the previous parashah. | holds | safe | 1 | done (B6) |
| E4 | Six 'Zohar' cells in the RCL concordance (Masei, Eikev, Re'eh, Shoftim, Nitzavim, V'Zot HaBerachah) open notes on other parashiyot. | holds | safe | 1 | done (B6) |
| E5 (= C4) | The concordance's tractate ranges for John 13–17 are wrong, and straddling tractates follow no single rule (rows 2, 8, 11, 20, 21). | partly | safe | 1 | done (B6) |
| E6 (= C3, G35) | Tractate 17 is labelled John 4:1–18 (passage, heading, index link) but expounds John 5:1–18, following a CCEL heading slip; Tractate 64 leaves out 13:33. | holds | safe | 1 | done (B6) |
| E7 | Five links were shifted although the writer used LXX or Hebrew numbering (LXX Ps 81:6 twice, Ehrman's Ps 22:2 and 69:22, Joel 3:1). | partly | safe | 1 | done (B6) |
| E8 | Two links follow a slip in the source text itself | not checked (proposal) | decision | 3 |  |
| E9 (= B19, G18) | About 370 Mei HaShiloach citations of the Prophets and Writings are unlinked; many use variant or English book names the linker lacks. | partly | safe | 3 |  |
| E10 | Tikkunei Zohar notes hold about 364 unlinked scripture citations under abbreviations the linker lacked (Is., Ez., Song., Ecc., Jon., King., Tzeph., Rut.). | partly | safe | 3 |  |
| E11 | About 120 BCP references to Ecclesiastes, Chronicles and the Apocrypha are unlinked in 19 notes; the lectionary psalm numbers are plain text. | partly | safe | 3 | Daily Office lessons done with C30 (B6); the rest phase 3 |
| E12 (= C1) | The 124 tractates link nothing. Footnotes are lost in 1-48, but in 49-124 the footnote text is spliced into the prose, sometimes mid-word. | partly | decision | 3 |  |
| E13 (= C28) | Block links and Bible-link arithmetic are clean, but RCL Proper 7C's 'Psalm 42 and 43' slot is empty, contrary to the hand-check claim. | partly | safe | 1 | done (B6) |
| E14 | The Guide and linking prompt say bare chapters are not linked, but 1,207 bare-chapter links exist in 96 notes. | holds | decision | 1 | Guide and linking prompt corrected (your choice) |
| E15 | The matrix's secondary column is unlinked code text. 15 of 31 names miss as written, but 29 of the 31 map to real catalog notes. | partly | safe | 3 | done (B6) |
| E16 | The alphabet crosswalk misattributes TĀ 11's kṣa-as-earth to āhnika 3, miscounts the consonants (33 for 34), mislabels the 12 'simple' letters, and cites few sources. | partly | decision | 3 |  |
| E17 (= G50) | The Parātrīśikā crosswalk misstates MSV's KSTS volume and Padoux's series and pages, names an unheld Singh Śivasūtra, leaves held works unlinked, and has unsourced glosses. | holds | safe | 3 | mechanical part done (B6); the rest phase 3 |
| E18 | The RCL concordance's Psalter list skips Psalms 117-146 and overstates the links; the Psalm 151 row of Psalms numbering is one cell short. | holds | safe | 3 | done (B6) |
| E19 (= B18) | The Tanya's 382 Roman-numeral Zohar citations are unlinked; Texts/Chasidut has no link to any Zohar note. | holds | safe | 3 |  |
| E20 | No Tantrāloka passage links to or from any Jewish or Christian text; Stephen's Writing links no TĀ note. | holds | decision | 6 |  |
| E21 (= D1, D2, G47) | The 'Plato — Phaedrus' links open Graham's Presocratics volume and the 'Pirkei Avot' links open the Rashi index; neither text is in the vault. | holds | decision | 7 |  |
| E22 | Concept notes cite eight primary works that are not in the library: Phaedrus, Protagoras, Life of Moses, Ambiguum 7, Ad Thalassium, Being and Time, Husserl's time lectures, Dissemination. | holds | decision | 7 |  |
| E23 (= D16, G49) | Three unresolved links (Technics hub x2, Scapegoat Reflex); the hub concept lists disagree with up: in four hubs; Engineered Cognitive Friction's body and up: differ. | holds | decision | 6 |  |
| E24 | Twenty-seven of 45 concepts link no text note, the Tantrāloka concepts link only the top of an āhnika, and no hub links a crosswalk | not checked (proposal) | decision | 6 |  |
| E25 | Parashah notes link only Rashi; JPS psalms link neither BCP nor LXX; tractates and John chapters do not link each other. | holds | safe | 3 |  |
| E26 | The folder-keyed numbering rule misfires when an author crosses numbering systems: 9 of 28 shifted links outside RCL and BCP are wrong. | partly | safe | 3 |  |
| E27 | Link error rates by stratum: large strata are clean; errors concentrate in BCP psalm verses and the 28 shifted links outside the lectionaries. | partly | safe | 3 |  |
| E28 | 'About 55,000 links' is right: the run log records 55,247 links added in two linking passes on 5 Oct. | **disproved** | safe | – |  |
| E29 | New crosswalk row "First stirring": Zohar 1:15a, Tantrāloka 3.66-67, John 1:1 | not checked (proposal) | decision | 6 |  |
| E30 | The Linguistic Creation crosswalk links only note tops and a catalog note; anchor it to Zohar 1:2b-3b, TĀ 3.149-153, 3.180-181, 3.198 and EK 08. | partly | safe | 6 |  |
| E31 | Add the Tanya (Sha'ar ha-Yichud 1) to the crosswalk as a third textual anchor on creation by letters | not checked (proposal) | decision | 6 |  |
| E32 | Source the "Speech Stages" row: Zohar 1:246b and 2:25b, Tantrāloka 3.235-245, Augustine on the inner word (Tractate 1 §8) | not checked (proposal) | decision | 6 |  |
| E33 | Give the recognition concept its two missing texts: Utpaladeva's simile (ĪPK IV 17, Torella p. 218) and Augustine on Mary's recognition (Tractate 121 §2) | not checked (proposal) | decision | 6 |  |
| E34 | Link the Anupāya concept to the verses it paraphrases: Tantrāloka 2.9-2.14 | not checked (proposal) | decision | 6 |  |
| E35 | The Twelve Kālīs concept links no verse; link TĀ 4.145–176 and Dyczkowski's catalogued translation of 4.122–180. | holds | safe | 6 | done (B6) |
| E36 | Point the "garments" concept at the teaching where the Ishbitzer says it: Mei HaShiloach, Chukat, Teaching 2 | not checked (proposal) | decision | 6 |  |
| E37 | New hub section "Leviathan in the texts" for the Technics hub | not checked (proposal) | decision | 6 |  |
| E38 | Give the Phaedrus concept and hub a text that is in the library: Ricoeur's reading of 274e-276d (Memory, History, Forgetting, pp. 141-145) | not checked (proposal) | decision | 6 |  |
| E39 | The pharmakon concept cites Stiegler's What Makes Life Worth Living without pages; pp. 2 and 25 (PDF 10, 33) tie the pharmakon to the Phaedrus. | holds | decision | 6 |  |
| E40 | Answer the liturgical-memory draft's open question with two texts the vault holds: the Prayer Book's anamnesis and Gschwandtner on liturgy as anamnesis | not checked (proposal) | decision | 6 |  |
| E41 | Connect "calendarity" in Stiegler to the vault's three calendars: the Church Year, the Daily Office cycle and the Tantrāloka plan | not checked (proposal) | decision | 6 |  |
| E42 | Add to the RCL concordance a table of John days whose first lesson the Zohar or Hasidut cites, starting with Numbers 21, John 3:14, Tractate 12 and Zohar 2:148b. | partly | decision | 6 |  |
| E43 | Link the oudeis concept to the word itself and to Augustine on the verse: lexicon note οὐδείς, John 6:44 and 1:18, Tractate 69 §2 | not checked (proposal) | decision | 6 |  |

## F. Workflow, dashboards and scripts

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| F1 (= F25 (part)) | Home's buttons make empty notes and rely on Templater's per-device create-trigger. It was ON on the laptop at 16:06; on the phone it is unknown. | partly | safe | 1 | done in part (b4: buttons fill the note); the phone switch is yours |
| F2 | The Guide's remedy ('Replace templates in the active file') does nothing on a blank note, because it runs the note as its own template. | holds | safe | 1 | done (b5: Guide remedy, tested) |
| F3 | Dataview does not await a view's async body, so Today-block order is not fixed, view errors are silent, and a re-render mid-run can duplicate output. | holds | safe | 3 |  |
| F4 | Any vault change re-renders visible dataviewjs blocks 2.5 s later, closing open verses or Office details and clearing lookup boxes. | holds | safe | 3 |  |
| F5 | When the tables end (plan 1 Dec, Shabbat 29 Dec, panchang 31 Dec 2029), Home silently loses the homily button, portion, Shabbat line, panchang and Hebrew-date turn. | partly | safe | 3 |  |
| F6 | today-header reads the Eastern-time tables in the device's zone, so outside Eastern time the Shabbat status, Hebrew-date turn and panchang are hours off. | partly | decision | 3 |  |
| F7 | 'Practice day N of 57' counts the two open days, matching the table's P1-P57 numbering, while the notes speak of 55 portions; a wording mismatch. | partly | decision | 3 | done (B6, your choice) |
| F8 | A single-verse portion is labelled as a doubled range ('1.1–1 (1)'). This hits 119 cycle days and 2 practice days, starting 31 Oct 2026. | holds | safe | 1 | done (B6) |
| F9 | 'Not yet written' only ever grows, and the only way to clear a day is to create a note for it | not checked (proposal) | decision | 3 |  |
| F10 (= C14) | The plan tables' structure, coverage, parashot and Sundays all check out, but 2027-28 All Saints/Thanksgiving link Year A readings, and Annunciation sits on Palm Sunday 2029. | partly | safe | 1 | done in part (b2); Presentation, Annunciation, Visitation in Years 1–2: phase 3 |
| F11 | Daily Office engine matches the BCP lectionary notes and BCP transfer rules on every date tested; no fault. | holds | safe | 8 |  |
| F12 | Shabbat table, Hebrew date and Sanskrit card are right; table times are within one minute of hebcal and astral. | holds | safe | 8 |  |
| F13 (= C13, G44, B23) | Homily (Polyphonic) template's five RCL links/embeds and four parashah queries can never resolve; Welcome line 59 still promises them. | holds | decision | 1 | done (b2: homily) |
| F14 (= C11) | Homily template always takes the last lectionary link, so feast-day and weekday homilies silently get the coming Sunday's readings. | holds | safe | 1 | done (b2: homily) |
| F15 | Already fixed on 6 Oct at 13:53: today-verses now matches 'pp.' callouts, so all 1,154 plan days show the Translation line. | **disproved** | safe | – | already fixed |
| F16 (= G1) | Library.base: at the snapshot the view called 'All' was filtered to one author (a filter set in the app that morning) | not checked (proposal) | decision | 1 | done (b1: Bases) |
| F17 (= G1, G2, D33) | By author, By subject, Library.base and Stiegler.base scan all 10,162 files under Library; Stiegler.base also misses 2 Stiegler works. | holds | safe | 1 | done (b1: Bases) |
| F18 | Vault Health's 'Phantom Links Detector' lists every hub outlink, not the two unresolved ones; Welcome and Guide rely on it. | holds | safe | 1 | done (B6) |
| F19 | Home's date, portion and buttons are fixed at render time; with no vault change overnight it stays on yesterday. | holds | safe | 3 |  |
| F20 (= D14) | Hub 'recent literature' feeds sort by creation time, but 619 of 648 catalog files were created on the same day | not checked (proposal) | decision | 6 |  |
| F21 | Home's three Tasks queries are valid; they are empty because the vault has only 7 undated checkbox lines, all in one Library note. | holds | safe | 8 |  |
| F22 | Every Bases count checked is right (subject indexes 652 rows over 640 notes); two notes in Catalog/Sanskrit-Study lack that subject. | holds | decision | 3 |  |
| F23 | Home's 11 view scripts and the MW TSV are 'other types' that sync only with a per-device switch; the Guide now warns but still advises it off. | partly | decision | 8 | a setting for you; Guide in phase 8 |
| F24 | The Guide has no new-device checklist; Sync's settings and Templater's trigger are per device, while Dataview JS and the mobile homepage are vault settings in plugin data. | partly | safe | 8 |  |
| F25 | Templater's create-trigger is on on the laptop and runs on any new note outside Templates/; two analysis notes now carry live template tags. | holds | decision | 1 | a setting for you (Templater excluded folders) |
| F26 | Sync headroom: 8.28 GB of live files against a 10 GB plan that also holds version history; photographed pages and re-OCR'd PDFs eat it fastest | not checked (proposal) | decision | 4 |  |
| F27 (= A23, G8 (part)) | Guide, Welcome, the actions note, Devi Mahatmya.md, daily-office view.js and 112 catalog notes have outdated sentences; Callout Manager is already fixed. | partly | safe | 1 | Guide .trash and audio sentences done (b5, B6); catalog notes phase 3 |
| F28 (= G5) | Two Devi Mahatmya notes keep dead 'Audio recitation' links to .mp3 files that remove-audio missed. | holds | safe | 1 | done (B6) |
| F29 | Ten small silent-failure points in the Home scripts and templates hold on reading the code; item (i) understates what a stray re-run of the review buttons does. | partly | safe | 3 |  |
| F30 | The plugin dependency map and versions are right; two calls listed as undocumented are public API, and Tasks feeds four lists, not three. | partly | safe | 8 |  |
| F31 | Panchang tables: sunrise, sunset and the limbs agree with an independent computation and with Drik Panchang on four dates | not checked (proposal) | decision | - |  |
| F32 | Six small changes that would smooth the daily, weekly and Sunday rhythm | not checked (proposal) | decision | 3 |  |

## G. Micro sample

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| G1 (= F17, F16) | Library.base's 'All' view has its own filter author == "Mark S. G. Dyczkowski", saved from the toolbar at 10:14 on 6 Oct, so it does not list the library. | holds | decision | 1 | done (b1: Bases) |
| G2 (= F17) | By author, By subject and Library.base filter only on folder 'Library', so they take in all 10,162 files under Library/ instead of the 640 catalog notes. | partly | safe | 1 | done (b1: Bases) |
| G3 (= D16) | Three of Stephen's notes keep 23 links to 13 removed .docx originals (12 Leviathan, 1 Gospel of Recognition). | partly | decision | 3 |  |
| G4 | From Moral Injury to Moral Repair (part 2) embeds a missing figure; the image is inside the handout .docx in _Originals. | holds | safe | 1 | done (B6: figure restored) |
| G5 (= F28) | Two Devi Mahatmya notes still link .mp3 files that were removed on 6 Oct; the removal button only matched links with the Audio/ folder path. | holds | safe | 1 | done (B6) |
| G6 | Three wikilinks added inside <td> cells of the Easter People facilitator guide show as raw brackets and do not work. | holds | decision | 3 |  |
| G7 (= A23, B26) | 112 catalog notes and Vault Guide line 110 still say the pre-OCR originals are in .trash/ocr-originals-2026-10-05, which was emptied. | partly | safe | 3 | the Guide sentence (b5) and 6 notes (B6); the rest phase 3 |
| G8 (= F28, G5) | Vault Guide (Layout row Audio/) and Welcome (section 9) still say the Devi Mahatmya recitation audio is in the vault; it was removed on 6 Oct. | holds | safe | 1 | done (B6) |
| G9 | Already fixed: the Guide's plugin table now names Callout Studio, the installed plugin. | **disproved** | safe | – | already fixed |
| G10 | Four catalog notes give the old Library/Books/ location, and a dated build log keeps old Library/Data, Tantrāloka and tools/ paths. | partly | safe | 1 | done (B6) |
| G11 | 525 of 685 catalog files: links (in 519 notes) are bare file names; all resolve today because no library name is duplicated. | holds | decision | 3 |  |
| G12 | 572 of 640 catalog notes lack physical_copy (67 false, 1 true), so the Shelf check column is empty for them. | holds | safe | 3 |  |
| G13 | 11 subject values outside the Guide's list in 9 notes; Kalikapurana and SBE sit in Sanskrit-Study without that subject. | holds | decision | 3 |  |
| G14 | File and note names against the Guide's naming rules | not checked (proposal) | decision | 3 |  |
| G15 | Several property names hold different types across families; parasha/parashah differ in spelling and type; the Daily note's list-valued verses clashes with numeric verses. | partly | decision | 3 |  |
| G16 | Link targets are sound, but page links number 11,825 to 143 PDFs, and a table link added later to the Guide lacks \\|. | partly | safe | 1 | done (B6) |
| G17 (= B16) | 73 Mei HaShiloach Prophets/Writings headings give chapter:ordinal; in 57 of 68 with a cited verse, the verse differs. | holds | safe | 3 |  |
| G18 (= B19, E9) | About 945 'Name, c:v' citations in 66 Mei HaShiloach notes are unlinked; the Torah lines cover most Torah-book ones, leaving 370 Prophets/Writings citations without backlinks. | partly | safe | 3 |  |
| G19 (= B17) | About 1,720 text notes (LXX, Tractates, Markandeya, Pritzker Zohar, Tanya, Mei HaShiloach) have no previous/next links. | holds | safe | 3 |  |
| G20 (= C1) | Tractates 49-124 carry about 950 glued footnote numbers and pasted note blocks; Tractates 1-48 lost their footnotes; callout URLs are wrong. | holds | safe | 3 |  |
| G21 | 85 verse-labelled OT references in 46 New Testament notes link only to the chapter or a #Chapter heading. | holds | safe | 3 |  |
| G22 | Rashi notes keep references to printed illustrations that are not in the vault | not checked (proposal) | decision | 3 |  |
| G23 | Author names spelled several ways split the By author table | not checked (proposal) | decision | 3 |  |
| G24 (= G43 (part)) | 29 of the 30 Devi Mahatmya notes are stubs with no Sanskrit text, yet the Guide lists the Devi Mahatmya among the 'Full reading texts'. | holds | decision | 7 | Incomplete Sets entry corrected (B6); the Sanskrit phase 7 |
| G25 | Zohar 2.11 Index of Sources ends at line 1646, then repeats all 3,272 vol-2 endnotes as headings and a table of contents (1 MB). | holds | safe | 1 | done (B6) |
| G26 | The real debris is about 2,500 unspaced italics in about 508 LXX notes and 108 BCP 'Preface of' rubric headings; the orphan footnotes and the mojibake are false. | partly | safe | 3 |  |
| G27 | The Hock catalog note has an invented subtitle, year 2006 (book: 2007), no Sanskrit in language, empty pages and no source statement. | holds | safe | 3 | done (B6) |
| G28 | Paramarthasara title page credits Sen Sharma as translator only; series, Emeryville and 2007 are printed, so the note's open questions close. | holds | safe | 3 | done (B6) |
| G29 | McClellan's 'Use of the Old Testament in the New Testament' is chapter 28 (pp. 497-513) of Blumell's 2019 volume, catalogued as a book. | holds | safe | 3 | done (B6) |
| G30 | TAK note omits English and German, its files are pre-press layouts with series on vol. II; Kalikapurana leaves year (1991-92) and pages (1,596) empty. | holds | safe | 3 |  |
| G31 | Text layers exist everywhere sampled, but some are of little use for searching | not checked (proposal) | decision | 4 |  |
| G32 | 123 of 640 catalog notes lack a 'Checked against' line; about 117 have no source statement at all; nearly all have empty pages. | partly | safe | 3 |  |
| G33 | About 87 catalog notes keep superseded text-layer or 'status review' sentences; the 73 'Also in your library' lists resolve but carry about 18 out-of-date labels. | partly | safe | 3 |  |
| G34 | Ruiz, Structural Violence (print-only) matches OUP's hardcover page: 2024, 466 pages, ISBN 9780197634028. | holds | safe | 3 |  |
| G35 (= C3, E6) | Tractate 17 is labelled and indexed as John 4:1-18, but it expounds John 5:1-18 (Bethesda). | holds | safe | 1 | done (B6) |
| G36 (= A1, A2) | 84 of the 2,721 Tantraloka verse notes compared with the DCS have a faulty mula: 36 with commentary run in, 44 missing a half-line, 4 with wrong text. | partly | safe | 2 | āhnika 37 and 34.3 done (b3, b3b, B6); the rest phase 2 |
| G37 (= C22) | 27,573 LXX verse ids in 1,116 notes sit mid-paragraph; 16 RCL embeds depend on them (Obsidian test pending). | holds | safe | 3 |  |
| G38 (= B15) | 219 of 452 pages in Zohar vol. 1's three text notes lack [p. N] markers; all other volumes are complete. | holds | safe | 3 |  |
| G39 (= C15 (part)) | 128 BCP collect ids (117 'preface-of' plus 11 others) are named after the wrong heading; nothing links to them; Psalm 79 lacks page 701. | partly | safe | 1 |  |
| G40 | MSV duplicate ids ^1-259 and ^2-71 and the jumps copy GRETIL; verses 1.541-1.603 (60) are missing but survive in the vault's Muktabodha e-text. | holds | safe | 1 | done (B6) |
| G41 | Ten Zohar vol. 10/12 folio ids sit on H1 lines; 111 links use five of them (Obsidian behaviour untested). | **disproved** | safe | – | nothing to do |
| G42 (= B21, E3) | Four parashah range links in the RCL concordance open one verse late or in the previous parashah. | holds | safe | 1 | done (B6) |
| G43 (= A25, G24 (part)) | Incomplete Sets guide recommends a book already held, says twelve volumes (it is 14), lists stub Devi Mahatmya as complete, and keeps stale tasks. | holds | safe | 1 | done (B6) |
| G44 (= C13, F13, B23) | Homily (Polyphonic) template links nonexistent RCL paths and parashah notes, while Welcome says it works. | holds | decision | 1 | done (b2: homily) |
| G45 | Hub, Catalog Item and Concept templates write a property no note has, a stale Location line, and keys that differ from the 45 concept notes. | holds | safe | 1 | done (B6) |
| G46 (= C26) | Sample homily quotes words not found in Tractate 69, is dated 10 May (Easter 6), gives Job instead of Acts 7, and is listed in the Homilies base. | holds | decision | 1 | marked type: sample (your choice) |
| G47 (= D1, D2, E21) | Two notes label links 'Plato/Phaedrus' and 'Pirkei Avot' that open Graham's Presocratics (Part 2) and the Rashi index; the vault has neither text. | holds | decision | 7 |  |
| G48 | Strict line breaks is on, so verse lines in Reading view join into paragraphs: about 34,500 breaks outside the Tantraloka (mostly LXX), plus 19,800 inside it. | partly | decision | 3 | a setting for you, or phase 3 |
| G49 (= D16, E23) | Six links point to missing things: Thomas 'Christianity copy', Scapegoat '1967', two planned hub notes, the Ricoeur CFP PDF, and a drawing's `[[try this]]`. | holds | decision | 3 |  |
| G50 (= E17) | Paratrisika crosswalk: M0160 should be M00160, the Singh catalog note is unlinked, 'MSV Ahnika' should be kāṇḍa, and the vault can't support 'Muller-Ortega (1992)'. | holds | safe | 1 | done (B6) |
| G51 | Zohar vols 10 and 12: 12 front-matter notes are fused numbered paragraphs, not footnotes; 17 notes have doubled H1s and 4 have letter-spaced H1s. | partly | safe | 1 |  |
| G52 | Zohar vols 3 and 4 have no Index of Sources note; their e-books are not in the vault, so it cannot be added from vault files. | holds | decision | 7 |  |

## H. OCR quality

| ID | Finding, as checked | Verdict | Fix | Phase | Now |
|---|---|---|---|---|---|
| H1 | 95 catalog notes, the Guide, Welcome and the OCR prompt say diacritics come through; Tesseract's Latin model cannot output ṃ ḥ ṛ ḍ ṅ ṭ ṇ, and about half of diacritic words are wrong. | partly | safe | 4 |  |

## What was disproved, and why

- **A5** and **G9**: already fixed before phase 1 (Welcome now says the KSTS map gives 228 anchor verses, 88 of them estimated; the Guide names Callout Studio).
- **A15 = F15**: already fixed on 6 Oct at 13:53; *Today's verses* shows the translation line on every one of the 1,154 plan days.
- **E28**: "about 55,000 links" is right; the run log records 55,247 links added in two passes on 5 Oct.
- **G41**: disproved in Obsidian. The ten Zohar folio ids on heading lines are all registered, and a link to `^zh-59a` resolves.

## Where the two checks disagreed

- **B22**: first check *partly*, second *holds*; the table gives the second.
- **G40**: first check *partly*, second *holds*. The second found that verses 1.541–1.603 of the Mālinīślokavārttika are not a lacuna: they survive in the vault's Muktabodha e-text.

## Tested in Obsidian

- **F3** holds: `await dv.view` returns after 10–20 ms, before the view draws; an error in a view shows nothing.
- **F17, G1, G2** hold: the Bases counts before and after are in the [[Phase 1 changes (6 Oct 2026)|phase 1 change list]].
- **G37** holds: 28,690 LXX verse ids in the text, 1,117 registered.
- **G41** disproved (above).
- **G48** holds: with *Strict line breaks* on, the verse lines of an LXX chapter and of the Gita show as one paragraph in Reading view.

