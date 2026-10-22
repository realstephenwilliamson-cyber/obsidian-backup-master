# Track 6, part 1 – change list (dry run)

Catalog and philosophy: everything in this track except the 113-note title-page check, which is part 2 (`batch2/t6b.md`). Built 7 Oct 2026 against the 04:08 UTC snapshot, from the drafts in `drafts/t6/{named,stale,props,feed,ten}` after their checkers. Nothing has been applied.

Files, all in `/home/claude/p3/batch2/`:

- `t6a-ready-ops.json`: the 722 ready changes, in the order to apply them.
- `t6a-ready-renames.json`: 1 rename (the Grant PDF), run inside Obsidian.
- `t6a-changes.tsv`: every ready change, one row each (group, note, before, after, source).
- `t6a-question-ops.json`: the changes for the recommended answer to each question, by question ID. C4's answer is built into C3's ops (12 core works); C7 and C11 have none (see below).

## Counts (ready)

| Kind | Changes | Notes | Finding | Checker |
|---|---|---|---|---|
| Bennett's Leviathan labelled | 2 | 2 | D4, your request | 2 of 2 right |
| TT2 marked as an uncorrected proof | 1 | 1 | D10, your request | right after rewording (see below) |
| Links to texts not in the vault made plain | 4 | 2 | D1, D2, your request | 4 of 4 right |
| PDF inventory row for the Grant rename | 1 | 1 | D8 (named checker) | asked for by the checker |
| .trash sentences | 109 | 108 | A23 = G7, B26, F27 | 109 of 109 right |
| "(status `review` …)" brackets removed | 47 | 47 | G33 | 47 of 47 right |
| Superseded text-layer clauses removed | 39 | 38 | G33 | 39 of 39 right |
| Catena Aurea sentence removed | 1 | 1 | G33 | right |
| "Also in your library" lists | 40 | 40 | D34, G33 | 40 of 40 right |
| Muktabodha year as a number | 245 | 245 | A19 | 245 of 245 right |
| Muktabodha empty year as `year:` | 233 | 233 | A19 | 233 of 233 right |
| **All** | **722** | **667** (+1 rename) | | |

The "Also in your library" changes add 137 same-author links to 32 lists, set 24 link labels to the target's title, and recase 2 author headings (counts by script; the stale checker recomputed them independently).

## Ready: the small items, in full

- **Primary to Secondary Literature Matrix** (Bennett label; `Library/Crosswalks/Primary to Secondary Literature Matrix.md`)
  - before: `` | **`Writing/The Cybernetic Leviathan/`** | [[Hobbes - Leviathan (parts 1-2)]]<br> ``
  - after: `` | **`Writing/The Cybernetic Leviathan/`** | [[Hobbes - Leviathan (parts 1-2)\|Hobbes - Leviathan, Parts 1–2 (Bennett's modernised adaptation)]]<br> ``
  - source: Library/Catalog/Philosophy/Hobbes - Leviathan (parts 1-2).md (editor Jonathan Bennett; body: Bennett's modernised version of Parts 1-2, not Hobbes's 1651 wording); D4 evidence: Part 1 PDF p. 1 'Copyright © Jonathan Bennett ... First launched: July 2004'
- **Hobbes - Dialogues between Philosopher and English Lawyer** (Bennett label; `Library/Catalog/Philosophy/Hobbes - Dialogues between Philosopher and English Lawyer.md`)
  - before: `See also [[Hobbes - Leviathan (parts 1-2)]].`
  - after: `See also [[Hobbes - Leviathan (parts 1-2)|Leviathan, Parts 1–2 (Bennett's modernised adaptation)]].`
  - source: Library/Catalog/Philosophy/Hobbes - Leviathan (parts 1-2).md; D4 evidence (Part 1 PDF p. 1)
- **Stiegler - Technics and Time (vols 1-3)** (TT2 proof note; `Library/Catalog/Philosophy/Stiegler - Technics and Time (vols 1-3).md`)
  - before: `…(2011). All three are in Library/Philosophy.⏎`
  - after: `…(2011). All three are in Library/Philosophy.⏎⏎*Note (7 Oct 2026):* The vol. 2 file is an uncorrected page proof, not the published book (checked 6 Oct 2026): its PDF pp. 5–7 have crop marks, a contents page with '000' for its page numbers, and a copyright page that ends '[USE CIP DATA FROM VOL 1]'; the PDF was made in Adobe InDesign CS3 on 3 July 2008. Its old-style numerals have no text mapping, so searching the file for a year or a page number finds nothing. The passages your Cybernetic Anamnesis paper cites at pp. 191 and 225–227 are on those pages of this file, but whether the proof's pages are the printed book's has not been checked; check against a published copy before quoting page numbers.⏎`
  - source: D10 evidence (checked 6 Oct 2026, verdict holds): Library/Philosophy/Bernard Stiegler - Technics and Time, 2_ Disorientation (...)(2008).pdf, 285 pp.; pdfinfo Creator 'Adobe InDesign CS3', CreationDate 3 Jul 2008; rendered PDF pp. 5-7: crop marks, contents page numbers '000', copyright page ends '[USE CIP DATA FROM VOL 1]'; pdftotext gives 'QUU(' for 2009; PDF p. 203 = folio 191, PDF pp. 237-239 = folios 225-227, cited in Writing/Cybernetic Anamnesis/Cybernetic Anamnesis text 2025-11-05.md
- **Hub - The Second Domestication** (not in the vault yet; `Notes/Hubs/Hub - The Second Domestication.md`)
  - before: `[[Library/Catalog/Philosophy/The Texts of Early Greek Philosophy The Complete Fragments and Selected Testimonies of the Major Presocratics. 2|Plato — Phaedrus (Thamus & Theuth)]]`
  - after: `Plato — Phaedrus (Thamus & Theuth) (not in the vault yet)`
  - source: D1 evidence: Graham PDF has 0 'Theuth'/'Thamus'; its catalog note says Part 2 only (Sophists and Pythagoras appendix); D3 (partly): no Plato dialogue in the vault
- **Hub - The Second Domestication** (not in the vault yet; `Notes/Hubs/Hub - The Second Domestication.md`)
  - before: `[[Texts/Torah/Rashi/Rashi (Metsudah)|Pirkei Avot / Rabbinic Dialectic]]`
  - after: `Pirkei Avot / Rabbinic Dialectic (not in the vault yet)`
  - source: D2 evidence: 'avot' occurs 0 times in Texts/Torah/Rashi/Rashi (Metsudah).md; no note or file holds Pirkei Avot
- **Engineered Cognitive Friction** (not in the vault yet; `Notes/Concepts/Engineered Cognitive Friction.md`)
  - before: `[[Texts/Torah/Rashi/Rashi (Metsudah)|Pirkei Avot]]`
  - after: `Pirkei Avot (not in the vault yet)`
  - source: D2 evidence: 'avot' occurs 0 times in Texts/Torah/Rashi/Rashi (Metsudah).md; no note or file holds Pirkei Avot
- **Engineered Cognitive Friction** (not in the vault yet; `Notes/Concepts/Engineered Cognitive Friction.md`)
  - before: `[[Library/Catalog/Philosophy/The Texts of Early Greek Philosophy The Complete Fragments and Selected Testimonies of the Major Presocratics. 2|Plato's Dialogues]]`
  - after: `Plato's Dialogues (not in the vault yet)`
  - source: D1 evidence: Graham PDF has 0 'Theuth'/'Thamus'; its catalog note says Part 2 only (Sophists and Pythagoras appendix); D3 (partly): no Plato dialogue in the vault
- **PDF inventory (6 Oct 2026).csv** (Grant rename (CSV row); `Prompts/Scripts/PDF inventory (6 Oct 2026).csv`)
  - before: `Library/Philosophy/GlendinningSimo_1999_84PostModernismLyotar_TheEdinburghEncyclope.pdf,13,253965,born-digital text,`
  - after: `"Library/Philosophy/Grant - Post-Modernism, Lyotard and Baudrillard (1999).pdf",13,253965,born-digital text,`
  - source: drafts/t6/named/check.md (Rename: the PDF inventory is an input); renames.json
- **Rename (inside Obsidian):** `Library/Philosophy/GlendinningSimo_1999_84PostModernismLyotar_TheEdinburghEncyclope.pdf` → `Library/Philosophy/Grant - Post-Modernism, Lyotard and Baudrillard (1999).pdf`. Its one inbound link, the catalog note's `files:` line, is rewritten by Obsidian. Why: D8 / Stephen's request ('file it under its author'): the file name names Simon Glendinning, the encyclopedia's editor; the chapter is by Iain Hamilton Grant (PDF p. 1: '8.4 Post-Modernism: Lyotard and Baudrillard / Iain Hamilton Grant', 'Copyright @ 1999. Edinburgh University Press'). New name follows the Guide's 'Author - Short title (year).pdf' and matches the catalog note, renamed in phase 1. Only inbound link: the catalog note's files: line, which Obsidian updates.

The TT2 line goes after the volumes line, and part 2 puts its dated check line before the `---` that comes after it, so the note reads: volumes line, the proof *Note*, part 2's **Checked against the file** line, then *Also in your library*. Same result in either order.

## Ready: the large groups (20 examples)

Full list: `t6a-changes.tsv` (every row), and `drafts/t6/stale/dryrun.md`, which quotes for each removed sentence the later line that supersedes it.

1. **A Preamble to the Study of Sri Siddhantasikhamani** (trash sentence): `` The previous file is in `.trash/ocr-originals-2026-10-05`. `` → `The previous file went with the trash when it was emptied on 6 Oct 2026.`
2. **The Crazy Wisdom of Ganesh Baba Psychedelic Sadhana, Kriya Yoga, Kundalini, and the Cosmic Energy in Man** (trash sentence): `` The previous file is in `.trash/ocr-originals-2026-10-05`. `` → `The previous file went with the trash when it was emptied on 6 Oct 2026.`
3. **Bansat-Boudon - The Contribution of Nondual Saivism of Kashmir to the Debate on Jivanmukti** (trash sentence): `` The previous file is in `.trash/ocr-originals-2026-10-05`. `` → `The previous file went with the trash when it was emptied on 6 Oct 2026.`
4. **Trika, the Kashmir Saiva Essence** (trash sentence): `` The scan without text is in `.trash/ocr-originals-2026-10-05`. `` → `The scan without text went with the trash when it was emptied on 6 Oct 2026.`
5. **Walch - Papyrus 66** (status bracket): `` …by Claude; change it if the item belongs elsewhere (status `review` until you have looked at it). `` → `…by Claude; change it if the item belongs elsewhere.`
6. **Baumer - An Introduction to Hindu Tantra (Bir lectures 2011)** (status bracket): `` …by Claude; change it if the item belongs elsewhere (status `review` until you have looked at it). `` → `…by Claude; change it if the item belongs elsewhere.`
7. **Torzsok - Yogini and Goddess Possession in Early Saiva Tantras** (status bracket): `` …by Claude; change it if the item belongs elsewhere (status `review` until you have looked at it). `` → `…by Claude; change it if the item belongs elsewhere.`
8. **Lakshman Joo - Vatulanatha Sutra** (text-layer clause): `'Swami Lakshman Joo'. Scan with no text layer.` → `'Swami Lakshman Joo'.`
9. **Tripurarahasyam - The Secret Beyond The Three Cities** (text-layer clause): `Scan without a text layer; end of file not available to check.` → `End of file not available to check.`
10. **Dyczkowski - The Inner Pilgrimage of the Tantras** (text-layer clause): `Offprint scan without a text layer (Franz Steiner Verlag).` → `Offprint scan (Franz Steiner Verlag).`
11. **Bansat-Boudon - The Contribution of Nondual Saivism of Kashmir to the Debate on Jivanmukti** (text-layer clause): `mis-encoded (every character shifted), so the PDF cannot be searched or copied.` → `mis-encoded (every character shifted).`
12. **Aquinas - Catena Aurea, St John** (Catena Aurea sentence): `searchable but with errors. Year and publisher are not legible in the OCR of the opening pages.` → `searchable but with errors.`
13. **Kiss of the Yogini Tantric Sex in its South Asian Contexts** (Also-in-library list): `…White:** [[Tantra in Practice|Tantra in Practice]]` → `…White:** [[Tantra in Practice|Tantra in Practice]], [[White - Netra Tantra at the Crossroads of the Demonological Cosmopolis|Netra Tantra at the Crossroads of the Demonological Cosmopolis]]`
14. **Ricoeur - Lectures on Ideology and Utopia** (Also-in-library list): `… History, Forgetting|Memory, History, Forgetting]]` → `… History, Forgetting|Memory, History, Forgetting]]⏎    - [[Ricoeur - Figuring the Sacred|Figuring the Sacred: Religion, Narrative, and Imagination]]⏎    - [[Ricoeur - Hermeneutics (Writings and Lectures Vol 2)|Hermeneutics: Writings and Lectures, Volume 2]]⏎    - [[Ricoeur - On Psychoanalysis (Writings and Lectures Vol 1)|On Psychoanalysis: Writings and Lectures, Volume 1]]⏎    - [[Ricoeur - Poli…`
15. **Stiegler, During - Philosophising by Accident** (Also-in-library list): `…- Technics and Time (vols 1-3)|Technics and Time]]` → `…- Technics and Time (vols 1-3)|Technics and Time]]⏎    - [[Stiegler - Automatic Society 1, The Future of Work (2016)|Automatic Society, Volume 1: The Future of Work]]⏎    - [[Nanjing Lectures 2016-2019|Nanjing Lectures 2016–2019]]⏎    - [[Stiegler - Telecracy Against Democracy|Telecracy Against Democracy]]⏎    - [[The Neganthropocene|The Neganthropocene]]`
16. **ASTaprakaraNa bhogakArikA-M00005** (A19 year number): `year: "1925"⏎` → `year: 1925⏎`
17. **mahArthamaJjarI-M00035** (A19 year number): `year: "1919"⏎` → `year: 1919⏎`
18. **zrIvidyArNavatantra-M00217** (A19 year number): `year: "1947"⏎` → `year: 1947⏎`
19. **AcArasAratantra-M00501** (A19 year empty): `year: ""⏎` → `year:⏎`
20. **zukavAkya-M00270** (A19 year empty): `year: ""⏎` → `year:⏎`

## Order of applying (for the lead)

- The ready ops apply in either order with part 2's list: 29 notes are in both, and applying mine first or theirs first gives the same text (script). None of my finds lies in the frontmatter of a note part 2 changes with `fm` ops, so processFrontMatter cannot disturb them.
- C5 (if yes): `physical_copy` ops **before** part 2's list; their finds include the status line, which part 2 changes in 5 notes.
- C6 (if yes): the Kālikāpurāṇa move **last**, after the C5, stale and part 2 changes on its current path.
- C9 (if yes): the Sen Sharma rename **after** the stale ops, which add 2 links to the old name; Obsidian then rewrites them.
- The Grant PDF rename and the CSV row go together. The CSV is not a note: if the applier takes only notes, make the same one-row replacement through the adapter.

## Checks run (script, 7 Oct)

- All 722 ready ops applied in order to a copy of the snapshot: every find occurs exactly once at its turn; 0 errors.
- Only the A19 ops touch frontmatter; every other ready op is in the body.
- Every new link target resolves to exactly one note; the 4 unlinked labels equal the old label plus " (not in the vault yet)".
- No replacement contains the divine name.
- None of these notes was changed by the overnight applies (tracks 1, 2 and 5), and none mentions the renamed Zohar 8.03 or 8.04.
- Other tracks' drafts touch the Matrix (t7) and the Guide (t3, t4, t7) with other finds; no clash.
- Question ops: each applies cleanly to the snapshot and after the ready ops and part 2's text ops. Both feed blocks parse with Dataview 0.5.68's own parser.

## Question previews

### C1 – the Grant link (exact addition)

`Writing/The Cybernetic Leviathan/The Cybernetic Leviathan.md`, after line 13:

```text
Hobbes's Leviathan read against cybernetics and digital society. The 2019 working title was *The {Post-Modern, Cybernetic, Capitalist} Leviathan*.

Source of the phrase: [[Grant - Post-Modernism, Lyotard and Baudrillard]].

**There's no current draft.** …
```

Evidence (D8, holds): Grant's chapter reads "But this post-modern, cybernetic, capitalist Leviathan is sublime". *Leviathan fragments 2018-2024* quotes the sentence at line 17, gives the attribution ("From *Post-Modernism: Lyotard and Baudrillard* by Iain Hamilton … p 628") at line 19, and repeats the sentence at line 27.

### C2 – Leviathan labels

- `Notes/Hubs/Hub - Technics, memory and the Leviathan.md`: `[[Library/Catalog/Philosophy/Hobbes - Leviathan (parts 1-2)|Leviathan (Hobbes)]]` → `[[Library/Catalog/Philosophy/Hobbes - Leviathan (parts 1-2)|Leviathan, Parts 1–2 (Hobbes, Bennett's adaptation)]]`
- `Library/Catalog/Philosophy/Hobbes - Leviathan (parts 1-2).md` (property): `aliases` `["Leviathan"]` → `["Leviathan (Bennett's adaptation, Parts 1–2)"]`
- `Library/Catalog/Philosophy/Hobbes - Leviathan (parts 1-2).md`: `# Leviathan (Hobbes), parts 1–2` → `# Leviathan (Hobbes), parts 1–2, in Bennett's modernised adaptation`

### C3 and C4 – what the Technics feed would show

Both tables assume C4 as recommended (12 core works, Grant included) and part 2's list applied (it sets Wiener 1961 and Abbinnett 2018, and moves Nancy and Bradley between author and editor). Dataview prints an empty year as "-". The three Stiegler sets show "-" unless C10 gives them a year; under (b), Disbelief and Discredit would then sort with 2011.

**Now** (10 rows): Gschwandtner, Gregor, Ricoeur WL2, Ricoeur WL1, Bilimoria and Baindur, Stiegler Telecracy, Ricoeur Figuring the Sacred, Stiegler Automatic Society 1, Ricoeur WL4, Ville. None of the hub's Core Library works.

**Option (b), list in the block** (recommended): 54 rows

| # | File | author | year | Core |
|---|---|---|---|---|
| 1 | Hobbes - Leviathan (parts 1-2) | Thomas Hobbes | 2004 | core |
| 2 | Stiegler - Technics and Time (vols 1-3) | Bernard Stiegler | - | core |
| 3 | Stiegler - Symbolic Misery (vols 1-2) | Bernard Stiegler | - | core |
| 4 | Ricoeur - Memory, History, Forgetting | Paul Ricoeur | 2004 | core |
| 5 | Ricoeur - Oneself as Another | Paul Ricoeur | 1992 | core |
| 6 | Wiener - Cybernetics | Norbert Wiener | 1961 | core |
| 7 | Stiegler - The Age of Disruption | Bernard Stiegler | 2019 | core |
| 8 | Grant - Post-Modernism, Lyotard and Baudrillard | Iain Hamilton Grant | 1999 | core |
| 9 | Green Leviathan or the Poetics of Political Liberty Navigating Freedom in the Age of Climate Change and Artificial Intelligence | Mark Coeckelbergh | 2021 | core |
| 10 | Hobbes on Resistance Defying the Leviathan | Susanne Sreedhar | 2010 | core |
| 11 | Playing with Leviathan Interpretation and Reception of Monsters from the B | – | 2017 | core |
| 12 | Returning to Judgment Bernard Stiegler and Continental Political Theory | Ben Turner | 2023 | core |
| 13 | Bilimoria and Baindur - Ricoeurian Hermeneutics and Indian Thought | Purushottama Bilimoria, Meera Baindur | 2025 |  |
| 14 | Bradley (ed.) - Critical Essays on Bernard Stiegler | Joff P. N. Bradley | 2024 |  |
| 15 | Buseyne, Tsagdis, Willemarck (eds.) - Bernard Stiegler, Memories of the Future | – | 2024 |  |
| 16 | Nancy - On Bernard Stiegler, Philosopher of Friendship | – | 2024 |  |
| 17 | Fitzpatrick, O'Dwyer, O'Hara (eds.) - Aesthetics, Digital Studies and Bernard Stiegler | – | 2021 |  |
| 18 | Gschwandtner - Reading Religious Ritual with Ricoeur | Christina M. Gschwandtner | 2021 |  |
| 19 | Ricoeur - Politics, Economy, and Society (Writings and Lectures Vol 4) | Paul Ricoeur | 2021 |  |
| 20 | Moore - Bernard Stiegler, 1952-2020 | Gerald Moore | 2020 |  |
| 21 | Gregor - Ricoeur's Hermeneutics of Religion | Brian Gregor | 2019 |  |
| 22 | Abbinnett - The Thought of Bernard Stiegler | Ross Abbinnett | 2018 |  |
| 23 | Invisible Leviathan | Murray E. G. Smith | 2018 |  |
| 24 | Stiegler, During - Philosophising by Accident | Bernard Stiegler | 2017 |  |
| 25 | Three-Text Edition of Thomas Hobbes's Political Theory The Elements of Law, De Cive and Leviathan | Thomas Hobbes | 2017 |  |
| 26 | Stiegler - Automatic Society 1, The Future of Work (2016) | Bernard Stiegler | 2016 |  |
| 27 | Stiegler - States of Shock | Bernard Stiegler | 2015 |  |
| 28 | Stiegler - The Re-Enchantment of the World | Bernard Stiegler | 2014 |  |
| 29 | Howells, Moore (eds.) - Stiegler and Technics | – | 2013 |  |
| 30 | Limiting Leviathan Hobbes on Law and International Affairs | Larry May | 2013 |  |
| 31 | Ricoeur - Hermeneutics (Writings and Lectures Vol 2) | Paul Ricoeur | 2013 |  |
| 32 | Stiegler - What Makes Life Worth Living | Bernard Stiegler | 2013 |  |
| 33 | Ricoeur - On Psychoanalysis (Writings and Lectures Vol 1) | Paul Ricoeur | 2012 |  |
| 34 | Ricoeur - Psychiatry and Moral Values | Paul Ricoeur | 2012 |  |
| 35 | Ville - Deconstructing the Leviathan | Jacques de Ville | 2012 |  |
| 36 | Stiegler - For a New Critique of Political Economy | Bernard Stiegler | 2010 |  |
| 37 | Stiegler - Taking Care of Youth and the Generations | Bernard Stiegler | 2010 |  |
| 38 | Stiegler - Telecracy Against Democracy | Bernard Stiegler | 2010 |  |
| 39 | The Platonian Leviathan | Leon Harold Craig | 2010 |  |
| 40 | Stiegler - Acting Out | Bernard Stiegler | 2009 |  |
| 41 | Taming the Leviathan | Jon Parkin | 2007 |  |
| 42 | Ricoeur - The Course of Recognition | Paul Ricoeur | 2005 |  |
| 43 | Leviathan after 350 Years (Mind Association Occasional Series) | – | 2004 |  |
| 44 | Derrida, Stiegler - Echographies of Television | Jacques Derrida, Bernard Stiegler | 2002 |  |
| 45 | Ely - Revisiting Paul Ricoeur on the Symbolism of Evil | Peter B. Ely | 2001 |  |
| 46 | Liberty, Rationality, and Agency in Hobbes's Leviathan | David van Mill | 2001 |  |
| 47 | Ricoeur - Figuring the Sacred | Paul Ricoeur | 1995 |  |
| 48 | Ricoeur - Lectures on Ideology and Utopia | Paul Ricoeur | 1986 |  |
| 49 | Ricoeur - Freud and Philosophy | Paul Ricoeur | 1970 |  |
| 50 | The new Leviathan or, Man, society, civilization and barbarism | R. G. Collingwood | 1942 |  |
| 51 | A Summary of Bernard Stiegler, Technics and Time, 4 | Daniel Ross | - |  |
| 52 | Bernard Stiegler - A Glossary of Terms | – | - |  |
| 53 | Ricoeur - The Model of the Text | Paul Ricoeur | - |  |
| 54 | Stiegler - Disbelief and Discredit (vols 1-3) | Bernard Stiegler | - |  |

**Option (a), `projects` property**: 54 rows

| # | File | author | year | Core |
|---|---|---|---|---|
| 1 | Grant - Post-Modernism, Lyotard and Baudrillard | Iain Hamilton Grant | 1999 | core |
| 2 | Green Leviathan or the Poetics of Political Liberty Navigating Freedom in the Age of Climate Change and Artificial Intelligence | Mark Coeckelbergh | 2021 | core |
| 3 | Hobbes - Leviathan (parts 1-2) | Thomas Hobbes | 2004 | core |
| 4 | Hobbes on Resistance Defying the Leviathan | Susanne Sreedhar | 2010 | core |
| 5 | Playing with Leviathan Interpretation and Reception of Monsters from the B | – | 2017 | core |
| 6 | Returning to Judgment Bernard Stiegler and Continental Political Theory | Ben Turner | 2023 | core |
| 7 | Ricoeur - Memory, History, Forgetting | Paul Ricoeur | 2004 | core |
| 8 | Ricoeur - Oneself as Another | Paul Ricoeur | 1992 | core |
| 9 | Stiegler - Symbolic Misery (vols 1-2) | Bernard Stiegler | - | core |
| 10 | Stiegler - Technics and Time (vols 1-3) | Bernard Stiegler | - | core |
| 11 | Stiegler - The Age of Disruption | Bernard Stiegler | 2019 | core |
| 12 | Wiener - Cybernetics | Norbert Wiener | 1961 | core |
| 13 | A Summary of Bernard Stiegler, Technics and Time, 4 | Daniel Ross | - |  |
| 14 | Abbinnett - The Thought of Bernard Stiegler | Ross Abbinnett | 2018 |  |
| 15 | Bernard Stiegler - A Glossary of Terms | – | - |  |
| 16 | Bilimoria and Baindur - Ricoeurian Hermeneutics and Indian Thought | Purushottama Bilimoria, Meera Baindur | 2025 |  |
| 17 | Bradley (ed.) - Critical Essays on Bernard Stiegler | Joff P. N. Bradley | 2024 |  |
| 18 | Buseyne, Tsagdis, Willemarck (eds.) - Bernard Stiegler, Memories of the Future | – | 2024 |  |
| 19 | Derrida, Stiegler - Echographies of Television | Jacques Derrida, Bernard Stiegler | 2002 |  |
| 20 | Ely - Revisiting Paul Ricoeur on the Symbolism of Evil | Peter B. Ely | 2001 |  |
| 21 | Fitzpatrick, O'Dwyer, O'Hara (eds.) - Aesthetics, Digital Studies and Bernard Stiegler | – | 2021 |  |
| 22 | Gregor - Ricoeur's Hermeneutics of Religion | Brian Gregor | 2019 |  |
| 23 | Gschwandtner - Reading Religious Ritual with Ricoeur | Christina M. Gschwandtner | 2021 |  |
| 24 | Howells, Moore (eds.) - Stiegler and Technics | – | 2013 |  |
| 25 | Invisible Leviathan | Murray E. G. Smith | 2018 |  |
| 26 | Leviathan after 350 Years (Mind Association Occasional Series) | – | 2004 |  |
| 27 | Liberty, Rationality, and Agency in Hobbes's Leviathan | David van Mill | 2001 |  |
| 28 | Limiting Leviathan Hobbes on Law and International Affairs | Larry May | 2013 |  |
| 29 | Moore - Bernard Stiegler, 1952-2020 | Gerald Moore | 2020 |  |
| 30 | Nancy - On Bernard Stiegler, Philosopher of Friendship | – | 2024 |  |
| 31 | Ricoeur - Figuring the Sacred | Paul Ricoeur | 1995 |  |
| 32 | Ricoeur - Freud and Philosophy | Paul Ricoeur | 1970 |  |
| 33 | Ricoeur - Hermeneutics (Writings and Lectures Vol 2) | Paul Ricoeur | 2013 |  |
| 34 | Ricoeur - Lectures on Ideology and Utopia | Paul Ricoeur | 1986 |  |
| 35 | Ricoeur - On Psychoanalysis (Writings and Lectures Vol 1) | Paul Ricoeur | 2012 |  |
| 36 | Ricoeur - Politics, Economy, and Society (Writings and Lectures Vol 4) | Paul Ricoeur | 2021 |  |
| 37 | Ricoeur - Psychiatry and Moral Values | Paul Ricoeur | 2012 |  |
| 38 | Ricoeur - The Course of Recognition | Paul Ricoeur | 2005 |  |
| 39 | Ricoeur - The Model of the Text | Paul Ricoeur | - |  |
| 40 | Stiegler - Acting Out | Bernard Stiegler | 2009 |  |
| 41 | Stiegler - Automatic Society 1, The Future of Work (2016) | Bernard Stiegler | 2016 |  |
| 42 | Stiegler - Disbelief and Discredit (vols 1-3) | Bernard Stiegler | - |  |
| 43 | Stiegler - For a New Critique of Political Economy | Bernard Stiegler | 2010 |  |
| 44 | Stiegler - States of Shock | Bernard Stiegler | 2015 |  |
| 45 | Stiegler - Taking Care of Youth and the Generations | Bernard Stiegler | 2010 |  |
| 46 | Stiegler - Telecracy Against Democracy | Bernard Stiegler | 2010 |  |
| 47 | Stiegler - The Re-Enchantment of the World | Bernard Stiegler | 2014 |  |
| 48 | Stiegler - What Makes Life Worth Living | Bernard Stiegler | 2013 |  |
| 49 | Stiegler, During - Philosophising by Accident | Bernard Stiegler | 2017 |  |
| 50 | Taming the Leviathan | Jon Parkin | 2007 |  |
| 51 | The new Leviathan or, Man, society, civilization and barbarism | R. G. Collingwood | 1942 |  |
| 52 | The Platonian Leviathan | Leon Harold Craig | 2010 |  |
| 53 | Three-Text Edition of Thomas Hobbes's Political Theory The Elements of Law, De Cive and Leviathan | Thomas Hobbes | 2017 |  |
| 54 | Ville - Deconstructing the Leviathan | Jacques de Ville | 2012 |  |

The (b) block (the names are the catalog notes' file names):

`````text
```dataview
TABLE author, year, choice(rank < 99, "core", "") AS "Core"
FROM "Library/Catalog"
FLATTEN default(object(
  "Hobbes - Leviathan (parts 1-2)", 1,
  "Stiegler - Technics and Time (vols 1-3)", 2,
  "Stiegler - Symbolic Misery (vols 1-2)", 3,
  "Ricoeur - Memory, History, Forgetting", 4,
  "Ricoeur - Oneself as Another", 5,
  "Wiener - Cybernetics", 6,
  "Stiegler - The Age of Disruption", 7,
  "Grant - Post-Modernism, Lyotard and Baudrillard", 8,
  "Green Leviathan or the Poetics of Political Liberty Navigating Freedom in the Age of Climate Change and Artificial Intelligence", 9,
  "Hobbes on Resistance Defying the Leviathan", 10,
  "Playing with Leviathan Interpretation and Reception of Monsters from the B", 11,
  "Returning to Judgment Bernard Stiegler and Continental Political Theory", 12
)[file.name], 99) AS rank
WHERE rank < 99 OR (contains(subject, "Philosophy") AND (contains(file.name, "Leviathan") OR contains(file.name, "Stiegler") OR contains(file.name, "Ricoeur")))
SORT rank ASC, year DESC, file.name ASC
```
`````

Option (a) adds these two lines above `aliases:` in each of the 12 core catalog notes, replaces the block with one that lists notes carrying them first (then alphabetical), and adds one optional-property line to the Guide's catalog section:

```yaml
projects:
  - "[[Hub - Technics, memory and the Leviathan]]"
```

**C4 evidence for the core list** (from the feed draft, corrected by its checker):

| Work | Why it is core |
|---|---|
| Leviathan (Bennett), Technics and Time, Symbolic Misery, Memory, History, Forgetting | Hub, Core Library, Primary |
| Green Leviathan, Hobbes on Resistance, Playing with Leviathan, Returning to Judgment | Hub, Core Library, Secondary (the last three rest on the hub line alone) |
| Oneself as Another | Crisis of Attestation (concept); one of the three references of *Cybernetic Anamnesis text 2025-11-05* |
| Wiener, Cybernetics | The State as a Technical System (concept, "Wiener (1948)"); the fragments quote Wiener's 1948 definition |
| The Age of Disruption | The fragments quote it twice with pages (p. 7, p. 11). The two concept notes that name it are Claude drafts of 5 Oct quoting the fragments, so they add nothing independent. |
| Grant, Post-Modernism: Lyotard and Baudrillard (proposed here) | The 2018 fragment (*CyberLevi (1)*, 14 Jun 2018) quotes its sentence and calls it "the key to my train of thought"; the attribution adds "I would love to have this whole article". You asked to link it (C1). No concept note names it. |
| Russell, A History of Western Philosophy (offered) | The 2024 Hobbes fragment cites pp. 546 and 548; your Second Domestication hub lists it; subject Other. |

"Close" works, not proposed (add any): Lectures on Ideology and Utopia, For a New Critique of Political Economy, What Makes Life Worth Living, Leviathan after 350 Years, Memories of the Future (each linked by one concept note); Writings and Lectures 4 and Automatic Society 1 (tied to the hub only by their own catalog text).

Not verified: neither block has been run in Obsidian. The renders assume Dataview's `contains()` is false on a missing property and that `object(…)[file.name]` gives null for a name not in the list (both untested here); null years sorting last under DESC and `localeCompare` for names are confirmed from the 0.5.68 library. Run the chosen block once through the Dataview API before applying.

### C5 – `physical_copy`

572 catalog notes (every non-index catalog note without the property). Example: `status: keep⏎files:` → `status: keep⏎physical_copy: false⏎files:`. Four notes say "owned" but mean the PDFs; they get `false` like the rest, so look for them on the shelf: Sacred Books of the East, Chakravarty and Marjanovic's Tantrasāra, Muller-Ortega's Triadic Heart of Śiva, and the Tāntrikābhidhānakośa.

### C6 – subjects

- `Vault Guide.md`: adds the line `` - **subject:** one or more of the eight subjects in the block above (a note with two shows in both indexes). A narrower term may follow them, for example `[Philosophy, Political-philosophy]`; no index or base reads it. `` before the `status` line
- rename inside Obsidian: `Library/Catalog/Sanskrit-Study/Kalikapurana (B.N. Shastri tr., parts 1-3).md` → `Library/Catalog/Hinduism/Kalikapurana (B.N. Shastri tr., parts 1-3).md`
- `Library/Catalog/Sanskrit-Study/Sacred Books of the East (series).md`: `subject` `["Hinduism","Comparative-religion"]` → `["Hinduism","Sanskrit-Study","Comparative-religion"]`
- `Library/Catalog/Other/A History of Western Philosophy.md`: `subject` `["Other"]` → `["Other","Philosophy"]`

The 11 values outside the Guide's list, by note: Pelikan *Historical-theology*; Koren Sanhedrin *Talmud*; Pritzker Zohar *Kabbalah*, *Zohar*; Leviathan *Political-philosophy*; Kālikāpurāṇa *Purana*, *Shaktism*; Sacred Books of the East *Comparative-religion*; Dyczkowski Tantrāloka *Tantraloka*; Rastogi *Krama*; Tāntrikābhidhānakośa *Lexicon*. No base, query or script filters on any of them.

### C7 – what `verses_read` would change (built after your answer)

- `Templates/Daily note.md` line 37 (`list("verses", verses),`) and line 62 (*Earlier on these verses*).
- The Guide's Daily study sentence ("The links are stored as properties (`verses`, `parashah`, `sunday`).").
- `Notes/Dynamic hubs - proposal.md` lines 89 and 171; `Prompts/Scripts/Dynamic hubs/hub-fields.js` line 42 and its copies in `queries.json`; `Prompts/Scripts/Dynamic hubs/sample-fixture.txt` (the test daily note: `verses:` and `parashah:` as lists).
- Your `Notes/Hubs/Hub - Tantraloka.md` line 75: `length(verses) AS "Verses"` → `length(verses_read) AS "Verses"`.

### C8 – the 21 "Pre-1900" Muktabodha notes

Each: `year: "Pre-1900"` → `year:`; the Published line, which keeps "Pre-1900", is unchanged.

- brhattantrasAra-M00013: "dhuṇḍhirāja gaṇeśa, <kazi>, India, Pre-1900"
- haThayogapradIpikA-M00243: "Bombay, India, Pre-1900"
- kaGkAlamAlinItantra-M00026: "Calcutta, India, Pre-1900"
- kramadIpikA-M00029: "kalikātā, India, Pre-1900"
- kubjikAtantra-M00030: "India, Pre-1900"
- parAtantra-M00062: "India, Pre-1900"
- prANatoSiNI arthakANDa-M00072: "kalikātā, India, Pre-1900"
- prANatoSiNI bhaktikANDa-M00060: "kalikātā, India, Pre-1900"
- prANatoSiNI dharmakANDa-M00071: "kalikātā, India, Pre-1900"
- prANatoSiNI kamyakANDa-M00073: "kalikātā, India, Pre-1900"
- prANatoSiNI part 6-M00061: "kalikātā, India, Pre-1900"
- prANatoSiNI sargakANDa-M00070: "kalikātā, India, Pre-1900"
- pratiSThAlakSaNasArasamuccaya-M00065: "India, Pre-1900"
- sakalAgamasArasaGgraha-M00063: "Muktabodha Indological Research Institute, India, Pre-1900"
- sanatkumAratantra-M00530: "Rasika Monana Caṭṭopādhyāya, Calcutta, India, Pre-1900"
- tArArahasya-M00095: "Calcutta Press, Calcutta, India, Pre-1900"
- tArArahasyavRttikA-M00096: "Calcutta Press (first publisher), Calcutta, India, Pre-1900"
- tripurArahasya jJAnakhaNDa-M00344: "India, Pre-1900"
- tripurAsArasamuccaya-M00669: "jīānandavidyāsāgarabhaṭṭacāryya, Calcutta, India, Pre-1900"
- visvasAratantra-M00101: "Calcutta, India, Pre-1900"
- yoginiitantra-M00064: "kṣemarāja śrī  kṛṣṇa dāsa, Bombay, India, Pre-1900"

Three more notes already have an empty year and say "unknown-pree 1900" in their Published line: kAmAkhyAtantra-M00132, kAmadhenutantra-M00133, zAktAnandataraGgiNI-M00134. Under (b) all 24 read the same way.

### C9 – rename

`Library/Catalog/Trika/Sen Sharma (ed. and tr.) - Paramarthasara of Abhinavagupta.md` → `Library/Catalog/Trika/Sen Sharma (tr.) - Paramarthasara of Abhinavagupta.md`. Inbound links: 1 today (`Library/Crosswalks/Scholars - library and free sources.md`), plus 2 that the stale ops add (Tantrasāra and Essence of the Exact Reality lists). The new name is free.

### C10 – set years

- `Library/Catalog/Philosophy/Stiegler - Technics and Time (vols 1-3).md`: `year` empty → `1998` (vol. 1, D22 evidence)
- `Library/Catalog/Philosophy/Stiegler - Symbolic Misery (vols 1-2).md`: `year` empty → `2014` (vol. 1, D22 evidence)
- `Library/Catalog/Philosophy/Stiegler - Disbelief and Discredit (vols 1-3).md`: `year` empty → `2011` (vol. 1, D22 evidence)

After part 2 there are 17 set notes (`type: multi-volume-set`). Besides these three, 8 carry a year (112 Upanishads 2007, KSTS Tantrāloka 1918, Kumārikākhaṇḍa 2009, Dyczkowski Tantrāloka 2023, Leviathan 2004, Kālikāpurāṇa 1991, Koren Sanhedrin 2017, Tulsi Ram Rigveda 2013) and 6 leave it empty (Brahmavaivarta, Pelikan, Rastogi, Tāntrikābhidhānakośa, Vivekananda, Pritzker Zohar; Pritzker on purpose, phase 1 B33, because its dates conflict).

## Not established

- The PDFs are not in this workspace. The TT2 proof description rests on D10 (held, 6 Oct); the Grant chapter's identity on D8 (held, 6 Oct); part 2 did not re-read the Grant file (its note was checked in phase 1).
- Whether the TT2 proof's page numbers are the printed book's.
- How Bases draws a missing `physical_copy` today, and whether the box can be ticked from the Shelf check table.
- Text-layer sentences left alone because the evidence is unclear: Philosophy of Gorakhnath (says no text layer, `text: searchable`, no later line), Khacakrapañcakastotra (the later line contradicts the property), Veda and Tantra ("OCR of the opening pages is poor" might be read as about the new layer), Linzer and Törzsök ("poor OCR"), Rubenstein ("turned sideways").
- The A23 count: the analysis counted 112 catalog notes; phase 1 fixed 6; the snapshot has 109 sentences in 108 notes, all drafted. The difference of two was not reconciled.

