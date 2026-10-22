# Build reports

Four rounds (the fourth is headed "Round 5" below). All output is in `Texts/` and `Library/`; build scripts are in `tools/`.

**6 Oct 2026:** the paths below are as they were when each round was written. Some have changed since: Monier-Williams is now in `Library/Sanskrit/Monier-Williams/`, the Tantrāloka folder is `Texts/Tantraloka/`, and the `tools/` scripts are not in the vault.

---

## Round 1 — Sefaria (Torah, Rashi, Tanakh, Mei HaShiloach, Tanya)

Script: `tools/build_texts.py`. Caches downloads in `.cache/` (git-ignored); a rebuild gives identical output. All checks passed: verse counts, parasha boundaries, footnotes, HTML leftovers, 8,645 wikilinks (4,668 of them to block IDs), Windows file names and path lengths. Longest path: 109 characters.

| Work | Notes (incl. index) | Footnotes | Divine name in source |
|---|---:|---:|---:|
| Torah (JPS) | 55 | 734 | 2 |
| Rashi (Metsudah) | 55 | 0 | 2 |
| Tanakh (JPS) | 743 | 4,069 | 1 |
| Mei HaShiloach (Edwards) | 67 | 441 | 13 |
| Tanya (Kehot) | 123 | 3,460 | 5 |

Total: 1,043 notes, 8.5 MB.

**Notes on what didn't fit the plan:**
- **Mei HaShiloach:** only Volume I has English text on Sefaria. Volume II and the Anthology are empty in this translation, so they have no notes, and the index note says so. In Volume I, the Introduction, Miscellany and every Talmud tractate except Shabbat are also empty. That leaves 54 parasha notes plus 12 for other sections (Ruth, Ecclesiastes, seven books of Prophets, Psalms, Proverbs and Shabbat). 465 of the 561 teachings link to Torah verses. Where a link points to a range of verses, it opens the first one. 6 links that point to a whole chapter rather than a verse were left out.
- **Verse counts:** Sefaria's schemas only give each book's number of chapters and total verses, not a count per chapter. Both numbers were checked and every verse appears exactly once. [[Joshua 21#^21-36|Joshua 21:36–37]] have no text in the JPS version, so those two verses are marked as having no text.
- **Parashot:** all five schemas had the parasha divisions, so the fallback list of the standard 54 was never used.
- **Version titles:** `books.json` lists slightly different titles from the files themselves. Titles were matched on exact strings you gave; the files' own titles are in the `translation` field.
- **Translator field:** the metadata has none, so it was filled in by hand. "Avrohom Davis" for the Metsudah Rashi is from general knowledge, not Sefaria. The Tanya notes say "Kehot Publication Society".
- **JPS footnotes:** JPS marks a footnoted phrase at both its start and its end. The footnote reference goes at the end of the phrase; the end marker is dropped, since Markdown has nothing like it. Of 9 markers in the Tanya text that have no footnote text, 2 are kept as superscript characters.
- **Divine name:** occurrences include the name in Hebrew with hyphens between the letters, transliterations with apostrophes between the letters, and the four letters listed by name. The Tanya occurrences read "four letters: *the LORD*" in the source. Substitute names (Hashem, Adonoy, Havaya, G–d) were left as they are.
- **Broken HTML:** 3 broken tags in the Mei HaShiloach source HTML were fixed on read.
- **Hebrew:** no paragraph is Hebrew alone. The Hebrew that remains is words the translators put inside the English, mostly in Rashi.
- **Tanya names:** the front matter got notes of its own, such as "Tanya - Likkutei Amarim - Title Page". The part's name was used rather than its number, so chapters are named "Tanya - Likkutei Amarim 01".
- **Line breaks:** the Mei HaShiloach source uses `<br>` between paragraphs inside a teaching. As specified, these became line breaks, so each teaching shows as one block with line breaks.

---

## Round 2 — New Testament (BSB + SBLGNT)

Script: `tools/build_nt.py`, run after `build_texts.py`. A rebuild of the Sefaria notes gave identical output; they are unchanged. All checks pass.

**Sources:** BSB `BSB_usfm.zip` from bsb2usfm release v5.16 (bereanbible edition). Greek and apparatus from LogosBible/SBLGNT (master).

| Work | Notes (incl. index) | Footnotes | Size | Divine name in source |
|---|---:|---:|---:|---:|
| New Testament (BSB + SBLGNT) | 261 | 8,254 | 3.6 MB | 0 |

260 chapter notes with 7,944 verses in all: 7,941 in the BSB and 7,939 in the SBLGNT. The footnotes are 1,312 from the BSB, 6,934 from the apparatus and 8 for the disagreements listed below.

**Checks:**
- Every SBLGNT verse appears with its full Greek text.
- The Greek is NFC-normalized; accents and breathings are intact: 192,958 combining marks in the source and the same number in the notes.
- No USFM markers or critical signs remain in the output.
- Footnotes, links and file names pass the same checks as the Sefaria round; longest path 109 characters.

**Verses only one edition has** (kept, with a footnote on the missing side):
- [[Acts 19#^19-41|Acts 19:41]] is not in the SBLGNT, which prints those words at the end of 19:40.
- [[Romans 16#^16-24|Romans 16:24]] is not in the BSB.
- [[Romans 16#^16-25|Romans 16:25–27]] are not in the SBLGNT text; its apparatus gives the doxology as the reading of WH, Treg and NA28.
- [[2 Corinthians 13#^13-14|2 Corinthians 13:14]] is not in the SBLGNT, which numbers it 13:13; its 13:12 covers BSB 13:12–13.
- 3 John 15 is not in the BSB, which includes it in verse 14.
- [[Revelation 12#^12-18|Revelation 12:18]] is not in the BSB, which includes it at the end of 12:17.

**Verse numbers that neither edition has** (no paragraph written): Matthew 17:21, 18:11, 23:14; Mark 7:16, 9:44, 9:46, 11:26, 15:28; Luke 17:36, 23:17; John 5:4; Acts 8:37, 15:34, 24:7, 28:29. The BSB gives these only in footnotes.

**Old Testament links:** 394 point to a verse and 102 to a chapter.
- An English-to-Hebrew versification table and the Psalm titles decide which. The table was compiled from standard lists.
- To check the table, verse counts in every chapter were compared between the BSB and JPS. Only four chapters differ in ways the table doesn't explain, and they always link to the chapter: Exodus 20, Deuteronomy 5, 1 Kings 22 and Nehemiah 7.
- 17 citations land on a different JPS number, for example [[Malachi 3#^3-23|Malachi 4:5]] → [[Malachi 3#^3-23|Malachi 3:23]] and [[Joel 3#^3-1|Joel 2:28]] → [[Joel 3#^3-1|Joel 3:1]]. These are listed in `tools/NT_BUILD_REPORT.md`.

**Notes on what didn't fit the plan:**
- **Torah citations:** there are no Tanakh chapter notes for the Torah. Torah citations link to the parasha note instead, at the verse's block or at its `## Chapter N` heading.
- **Extra links:** 84 Old Testament citations in BSB footnotes and 71 New Testament references in footnotes were also linked; the original request only asked for Old Testament references in the main text.
- **Words the translators supplied** (USFM `\add`) are in italics, as in the printed BSB.
- **Apparatus footnotes** sit at the exact word or phrase using SBLGNT's critical signs, which are then removed. Six variants that span two verses are attached where they open.
- **Sigla key and translator field:** the index note's key to the apparatus sigla (WH, Treg, NA28, RP and so on) is from general knowledge, not the repository. So are the `translator` names (the Berean Bible Translation Committee; Michael W. Holmes as SBLGNT editor).
- **Note names:** chapters are always two digits, so "Jude 01".
- **SBLGNT attribution:** the index note quotes the license and copyright lines word for word from the repository's README.

---

## Round 3 — Lexicon, Zohar, BCP and Monier-Williams

Scripts: `tools/build_lexicon.py`, `tools/build_zohar.py`, `tools/build_bcp.py`, `tools/build_mw.py`. Vault check passes across all 8,432 notes and 153,619 links; longest path 120 characters.

**Before starting:** PR #1 (rounds 1–2) was opened and merged. The branch was restarted from main and the new commits pushed to the same branch name.

### 0. Earlier notes — divine name

Rebuilt without replacement. Exactly 20 lines in 17 notes changed; each change only puts back the divine name where the source has it. The builds now count occurrences instead of replacing them.

**Counts (earlier works, for the record):**

| Work | Divine name in source |
|---|---:|
| Torah | 2 |
| Rashi | 2 |
| Tanakh | 1 |
| Mei HaShiloach | 13 |
| Tanya | 5 |
| New Testament | 0 |

### 1. Septuagint (Swete) — not built

The verse divisions in Swete's text are wrong in many places. The faults are in the upstream TEI (Open Greek and Latin's First1KGreek), not only in the conversion:
- Verses are merged: [[Torah 01 - Bereshit#^2-25|Genesis 2:25]] sits inside 3:1, and 15:19–21 are folded into 15:18 with a stray "20".
- 260 of 1,138 chapters have gaps or verses out of order.
- Psalm titles are detached and numbered as extra verses.
- 1,165 words carry OCR damage.
- Ecclesiastes has no text upstream.

Block IDs would point at the wrong words, so the NT footnotes were not linked to it either. Brenton's 1851 English is on GitHub (eBible's `eng-Brenton` USFM, public domain) and was correct on spot verses, but it wasn't used without the Greek. Details are in `tools/SKIPPED.md`.

### 2. Greek NT lexicon

5,462 notes (9.5 MB) in `Library/Lexicons/Greek NT/`: one per lemma plus an index. Each occurrence is linked to its verse.

- **Licenses:** MorphGNT CC BY-SA 3.0; SBLGNT CC BY 4.0; Dodson public domain (CC0, `biblicalhumanities/Dodson-Greek-Lexicon`).
- **Gaps:** MorphGNT lacks [[John 07#^7-53|John 7:53–8:11]]. Eleven verses differ from SBLGNT in punctuation or capitalisation. 541 lemmas have no Dodson entry with exactly the same headword, so they have no gloss.
- **Names:** 17 capitalised lemmas end in "(proper name)" so they don't collide with the lowercase lemma on Windows.

### 3. Zohar

| Work | Notes (incl. index) | Size | License | Divine name in source |
|---|---:|---:|---|---:|
| Zohar (Soncino) | 1,275 | 5.7 MB | Public domain | 1 |
| Zohar Chadash | 31 | 3.5 MB | Aramaic public domain; English CC0 | 247 |
| Tikkunei Zohar | 94 | 1.1 MB | CC BY-NC (English and Aramaic) | 25 |

- **Zohar:** Soncino-only notes. The vocalized Aramaic's license on Sefaria is "unknown", so it was left out rather than substitute another text. Soncino translates 10,782 of 16,852 passages; untranslated passages are noted in place. 405 folio sides have no Soncino text and so no note.
- **Zohar Chadash:** only 65 of its 4,421 paragraphs have an English translation.
- **Tikkunei Zohar:** Solomon covers folios 17a–63a only. It is paired with the Constantinople 1740 Aramaic, which aligns with it exactly. Solomon's 1,703 endnote markers were dropped because the endnotes aren't in Sefaria's export.

### 4a. BCP 1979

265 notes (1.4 MB) from `bcponline/BCP-Source`, which preserves the printed page numbers. The book is public domain; the repository states no license of its own.

- **Contents:** 114 service and section notes, 150 psalm notes each linked to its JPS psalm, and an index.
- **Block IDs:** 365 collects, 70 prayers, 11 thanksgivings plus a 2007 version of the first, 123 catechism questions and 39 Articles.
- **Divine name in source:** 10.
- **Page markers:** the source has no footers for pages 700 and 737, so pages 701 and 738 have no marker; the text there is unbroken. The other unmarked pages are the unnumbered front matter (1–8) and the blank and section title pages.
- **Psalm numbering:** in 63 psalms the 1979 Psalter's own verse numbering differs from other English Bibles. It is kept as printed.

### 4b. Lectionary — not built

Advent 1, Year A checks out in `bcponline/BCP-Source`. But the RCL is copyright © 1992 Consultation on Common Texts, and none of the repositories found states a license for the tables themselves. Details are in `tools/SKIPPED.md`.

### 4c. Monier-Williams

`Library/Data/Monier-Williams/monier-williams.tsv` (30.3 MB, 286,525 entries, IAST) plus a README note.

- **License:** the data's own header says CC BY-NC-SA 3.0, while the repository's LICENSE file says CC BY-SA 4.0. The stricter terms are followed and the required credit is quoted verbatim in the README.
- **Divine name in source:** 0.

---

## Round 5 — Septuagint (Brenton), Psalms Crosswalk, Tantrāloka (DCS), NT LXX links

### 5a. Septuagint — Brenton English

Script: `tools/build_lxx.py`. Source: GZancewicz/hypomnema (Brenton 1851 English Septuagint), public domain.

- **Notes:** 1,117 chapter notes across 53 LXX books, in canonical LXX order (`Texts/LXX/NN BookName/`)
- **Verses:** 28,690
- **Footnotes:** 2,596 Brenton translator footnotes
- **Errors:** 0
- **Index:** `LXX (Brenton).md` at `Texts/LXX/`
- **Greek text:** excluded. The Rahlfs 1935 LXX (eliranwong/LXX-Rahlfs-1935) requires a signed CCAT user declaration; Brenton English is built alone. This is documented in the index note.
- **Book names:** LXX canonical names used throughout (1 Kingdoms, 2 Kingdoms, 3 Kingdoms, 4 Kingdoms, 1 Paralipomenon, 2 Paralipomenon, Esdras B (Ezra), Esdras B (Nehemiah), Esther (Greek), Daniel (Greek), Wisdom of Solomon, Sirach, Epistle of Jeremy).
- **Psalm numbering:** LXX Psalms 1–151 in LXX numbering; Hebrew Psalm aliases in each LXX Psalm note; combined Psalms (LXX 9 = Heb 9+10; LXX 113 = Heb 114+115) are noted.
- **Divine name in source:** kept exactly as Brenton wrote it in the English text; not added to any file names, headings, aliases, or frontmatter written by the build script.

### 5b. Psalms Crosswalk

Script: `tools/build_crosswalk.py`.

- **Note:** `Texts/Crosswalks/Psalms numbering.md`
- **Table:** 155 rows mapping Hebrew/MT/JPS/BSB/BCP 1979 Psalm numbers to LXX/Rahlfs numbers, with wikilinks to both Hebrew (`Psalms NNN`) and LXX (`LXX Psalms NN`) chapter notes.
- **Special cases documented:** Heb 9+10 = LXX 9; Heb 114+115 = LXX 113; Heb 116 split; Heb 147 split; LXX Psalm 151 (no Hebrew equivalent).

### 5c. Haftarot — not built

Sefaria haftarah data was not available in the export corpus in a usable form. Skipped per Round 4 prompt (Part 3).

### 5d. Tantrāloka — Digital Corpus of Sanskrit

Script: `tools/build_tantraloka.py`. Source: OliverHellwig/sanskrit DCS, CC BY 4.0. Glosses: Monier-Williams Sanskrit-English Dictionary (1899), public domain.

- **Āhnikas in DCS:** 19 of 37 (1–9, 11–12, 16–22, 26). Āhnika 22 file is present but empty; 18 āhnikas yielded notes.
- **Verse notes:** 2,726 (one per verse, `Tantrāloka NN.VVV`), in `Texts/Tantrāloka/Āhnika NN/`
- **Total tokens:** 41,313
- **Errors:** 0
- **Per-āhnika index notes:** 18, linking all verses in that āhnika
- **Main index:** `Tantrāloka (DCS).md` at `Texts/Tantrāloka/`
- **Word table columns:** Form · Lemma · Unsandhied · POS · Features · MW Gloss
- **Other Śaiva/tantric texts in DCS:** Tantrasāra, Mṛgendratantra, Spandakārikā, Spandakārikānirṇaya, Bhairavastava, Mahācīnatantra, Mātṛkābhedatantra, Toḍalatantra, Uḍḍāmareśvaratantra — documented in the report for future builds.

### 5e. NT BSB footnotes → LXX wikilinks

Script: `tools/patch_nt_lxx_links.py`. Post-processes the NT BSB notes built in Round 2.

- **Lines patched:** 79 footnote lines in 56 NT note files
- **Pattern:** `(see also LXX)` or `; see also LXX` replaced with `[[LXX BookName CH|LXX]]` wikilinks pointing to the corresponding LXX chapter note
- **Books linked:** Amos, Deuteronomy, Exodus, Genesis, Habakkuk, Hosea, Isaiah, Jeremiah, Joel, Numbers, Proverbs, Psalms (with Hebrew→LXX psalm number mapping applied)
- **Psalm 116 special case:** verse ≥ 10 maps to LXX 115; verse ≤ 9 maps to LXX 114
- **Multi-book footnotes:** both wikilinks inserted (e.g. Isaiah 65 and 66 in the same footnote)
- **All 55 distinct LXX note targets verified to exist.**

---

## Changes made on import into the vault (1 Oct)

- **Tantrāloka (DCS)** moved to `Library/Sanskrit/Tantraloka words/NN/` and renamed "Tantraloka CC.VVV - words", with index notes "Tantraloka words NN" and [[Tantraloka words (DCS)]]. Each note links to the verse note it matches by text (2647 same number, 18 numbered one higher in the DCS in 1.59–1.76, 53 divided differently, 8 unmatched). The Monier-Williams gloss column was dropped: it took the first dictionary entry for each lemma, often the wrong word of the same spelling. Aliases changed to "TĀ C.V words" so they don't duplicate the verse notes' aliases.
- **Psalms crosswalk:** added a BCP 1979 column and a line on verse numbering.
- **Zohar notes** from this download were not imported: the vault copies already carry the Pritzker cross-links.
- **Haftarot** were not built (5c), so no parasha notes changed.
