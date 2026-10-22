---
type: decisions
created: 2026-10-19
updated: 2026-10-19
---
# Audit decisions (19 Oct 2026, second round)

The decisions the complete vault audit of 19 Oct 2026 asks of Stephen (the merged report is in the Claude project, `claude/audit-2026-10-19/Complete vault audit.md`, section 5; the agents' edit files are in `.work/edits/audit-2026-10-19/`). Taken with Stephen in the Fable chat of 19 Oct 2026, a few at a time; each item gets his answer and the date below it as **Answer (19 Oct):** …. Items without an answer are open. The corrections prompt for the week of 26 Oct (`AI/Prompts/Audit corrections (Oct 2026).md`) carries out the answers and the safe fixes.

**Status (19 Oct 2026, 17:45):** all 33 answered (Stephen, Fable chat, 16:05–16:55). Done the same evening, for testing this week: 1 (Spaced Repetition installed; folders as decks, ignore list in chat), 2 (Day Planner OG chosen and integrated: Daily mode, the template writes OG's form), 3 (the Guide's plugin table), 4 (Meta Bind toggles in the template; placeholders kept; `date` type not needed), 16 (all four Holy Days points), 27 (`<book> - marked pages`; the blank Ruiz note trashed), 33 (one `letterCycleStart` in paths.json). The corrections prompt `AI/Prompts/Audit corrections (Oct 2026).md` carries out the rest in the week of 26 Oct.


Grouped; each item names the finding ids. "Safe" fixes need no decision and go straight into the corrections prompt; they are listed in section 6.

**A. Plugins and the Fable build**
1. Spaced Repetition (K-07, F-17, J3-25): (a) install it on the PC (the design's choice; decks by folder, as built), (b) a plugin-free review line in `today-items` computed from the cycle day (the wish list's original idea), (c) leave the card notes as a register for now.
   **Answer (19 Oct, 16:05):** (a) install it on the PC (Stephen installs; decks by folder as built; the Fold trial stays pending; the Guide gets its row).
2. Time blocks (F-01, Stephen 14:42): (a) Day Planner back on the PC only, (b) a lighter plugin — the lead brings a sourced comparison of the candidates that read `- [ ] HH:MM - HH:MM` tasks, (c) the plain checklist as it is.
   **Answer (19 Oct, 16:05):** (b) the lead brings a sourced comparison of the lighter plugins that read `- [ ] HH:MM - HH:MM` tasks into the corrections prompt; Day Planner may return on the PC after that; the section stays a checklist meanwhile; Android undecided.
3. The Guide's plugin table and Sync section after (1) and (2): rows for Day Planner, JotDrop, Homepage, QuickAdd, Pane Relief, PDF++ ("removed, 19 Oct"), Ink (on), Text Extractor (gone), Spaced Repetition and Tag Wrangler (as decided); plugins per device, plugin sync off (K-05, K-06, F-02, I-06).
   **Answer (19 Oct, 16:05, follows from 1 and 2):** rows: Spaced Repetition on (PC); Tag Wrangler (when added); Day Planner removed 19 Oct, alternative under review; JotDrop, Homepage, QuickAdd, Pane Relief, PDF++ removed; Ink on; Text Extractor gone; plugins per device, community-plugin sync off.
4. Placeholders in the daily template: Friday calls 14:00–15:00, pūjā 12:00–12:45 (J3-27); `reading_min` as a number (K-15); habits ticked in the File properties pane or Meta Bind (J3-28). The `date` property's type (F-07/check-F): give it the Date type in Obsidian's property settings, or leave `date(note.date)` as applied.
   **Answer (19 Oct, 16:05):** placeholders (calls 14:00–15:00, pūjā 12:00–12:45) stay until Stephen changes them in the template; Stephen gives `date` the Date type in Obsidian's property settings (then Habits.base may compare `date` directly; `date(note.date)` works either way); Meta Bind: yes — Stephen installs it, the corrections prompt un-comments the toggle line in `Templates/Daily note.md` so habits are ticked in the note body (also on the phone); `reading_min` stays a number.
5. The 108 card notes rest on the images in `.trash` (J3-20): Stephen checks a sample (or accepts the independent check's 13 × 18 fields), then the images may go.
   **Answer (19 Oct, 16:05):** the independent check (13 cards × 18 fields) stands as the check; the images may go with the rest of `.trash` when (10) and (23) are settled.

**B. Texts and OCR**
6. Radhakrishnan: English-only re-OCR (the lead's measure: 92% of pages carry stray Devanagari; no Devanagari printed) — yes / no. Singh *Parātrīśikā* and Kālikāpurāṇa 1: leave / English pages only.
   **Answer (19 Oct, 16:15):** Radhakrishnan: English-only re-OCR in the corrections week; Singh and the Kālikāpurāṇa: leave.
7. The 26 fpdf2 PDFs with the junk after ि (H-01), starting with the 11 Dyczkowski volumes (1.10 GB): redo now / later / leave; Hock, Speijer, the Mālinī typescript, the Macdonell Dictionary (H-02): check first whether those pages print Devanagari.
   **Answer (19 Oct, 16:15):** the 11 Dyczkowski volumes now (the 15 Oct pipeline, eng+san); the other 15 later; Hock, Speijer, the Mālinī typescript and the Macdonell Dictionary: check first whether the affected pages print Devanagari.
8. Redo the poor layers (H): Mālinī typescript, Gonda, Lanman, Abbinnett now; Singh *Vedanta*, Graham, Hanumad, Durga700 optional.
   **Answer (19 Oct, 16:15):** all eight (Mālinī typescript, Gonda, Lanman, Abbinnett; Singh *Vedanta*, Graham, Hanumad, Durga700).
9. Dillon & Gerson: left (settled 19 Oct). *Questions and Doubts*' garbled Greek Markdown (C-13, J3-08): re-extract from the re-OCR'd PDF / leave.
   **Answer (19 Oct, 16:40):** *Questions and Doubts*: re-extract the 4 notes from the re-OCR'd (Greek-model) PDF, markers and labels kept, backup first.
10. Whitney (H-06, I-09, G-11, K-29, J3-04): the 15 notes point to a trashed PDF — reword to "no PDF in the vault" / restore the PDF from `.trash` / wait for the 400 ppi download.
   **Answer (19 Oct, 16:15):** trash the weak notes too (the 15 Whitney notes and their catalog note, through Obsidian); both lists keep the 400 ppi download as wanted.
11. Mūla readings (A-02, A-03): 1.46 ज्ञानाज्ञानगतं (KSTS) — fix; 13.205 योग्यतां and 15.95 तत्कौलिकं त्रयम् — follow the print or keep; "Aaṣāḍha" (A-05) printed that way.
   **Answer (19 Oct, 16:20):** follow the print in all three: 1.46 ज्ञानाज्ञानगतं, 13.205 योग्यतां, 15.95 तत्कौलिकं त्रयम्; the verse-page map's misprint list records the two editorial readings as 'KSTS reading kept'. "Aaṣāḍha" (A-05) is printed that way: keep.
12. The secondary-literature index (A-08): PDF pages or printed pages (one convention; 564 of 625 labels differ from the page they point to); Törzsök's 12 relabels wait for this (check-A).
   **Answer (19 Oct, 16:20):** printed page numbers as the one convention (labels become the printed page, the link target stays the PDF page, the header reworded); Törzsök's 12 relabels (A-06c) follow.
13. The Dhvanyāloka's 179 stray marks after calls (J2-05): strip / leave.
   **Answer (19 Oct, 16:40):** strip them, each checked against the page line first (J2's job 3 lists them).

**C. Zohar and Bible**
14. B-01: re-point the 733 links to the text the reference names (by line; 37 "Tos" cases reviewed by Stephen); B-02 un-split the italics; link the vol. 11 notes' 1,159 plain references and the 153 Soncino-folio links (check-B M1, M2); J1-02's 419 ZḤ folios with a block.
   **Answer (19 Oct, 16:20):** all of it, by line: the 733 (the 37 'Tos' cases shown to Stephen first), the 1,466 split italics, the vol. 11 notes' 1,159 plain references, the 153 Soncino-folio links and J1-02's 419 ZḤ folios with a block; one batch, dry run, 50-link check.
15. Hoffmeier Jer 44:14 → 46:14 (B-07, the book's misprint): link the right verse with a note / keep as printed. JANT Hebrews 11 L84 (B-12): the LXX pair. E-05's 11 references with a certain intended verse (D04 vs D06): link / keep plain.
   **Answer (19 Oct, 16:20):** link the intended verse and mark the misprint — Hoffmeier → Jer 46:14 "(printed 44:14)"; JANT Hebrews 11 L84 → the LXX note; the 11 references of E-05 linked the same way (D04 wins; the decide-later note records it).
16. Holy Days: the Christmas transfers (C-07; Stephen's rule, document it in `Daily Office Engine.md` L61); All Saints on 8 Nov when 1 Nov is a Sunday (C-08, J2-09); the Monday after a Sunday feast choice (J2-08); the 18 Oct row in the choices note.
   **Answer (19 Oct, 16:25):** all four: document the Christmas rule in `Daily Office Engine.md` L61; `holyday/view.js` L79 offers no second All Saints when 1 Nov is a Sunday; a feast whose readings were used on the Sunday is not kept again on the Monday (L91–106); the row `| 2026-10-18 | Saint Luke the Evangelist | feast |` goes into `Calendar/Holy Days - my choices.md`.
17. The synoptic rows (C-05): follow the BSB as the note declares, or the gospel text (4 rows + 19g).
   **Answer (19 Oct, 16:25):** follow the gospel text (rows 14a, 19e, 23g, 25b and the 19g/19h overlap corrected) and add a line to the note saying where and why it departs from the BSB.
18. The Christmas-feast rule quotation "appointed of fixed days" → "on fixed days" (check-C N-1; the BCP Calendar note L108, Holy Days L28).
   **Answer (19 Oct, 16:25):** correct both notes to "on fixed days" (BCP p. 17).

**D. Library structure**
19. The 15 Oct books (D-02…D-06, L-01, L-02, J3-05): fix the converter first, then re-derive labels, ranges and names; *Anti-Oedipus* f-ligatures (D-01); Coogan's missing chapters (D-04); Brown's chapters (D-10); Hume's OCR (D-11); the 141 junk names (D-12); *A Thousand Plateaus*' plateaus (L-01).
   **Answer (19 Oct, 16:25):** the converter first (`conv.py` L1414/1441/1445 and the Add-new-files prompt L57–58: `page_range`, `[PDF n]` for unprinted pages), then all of it, one batch per book: 153 `pages` → `page_range`; Lim, Butler, Coogan PDF numbers; *Anti-Oedipus* 551 markers → `[PDF n]` and 3,190 f-ligatures; TT3's 21 markers; Brown, Coogan, Hume and *A Thousand Plateaus* re-split from the PDF outline; the 141 junk names and 10 run-together names by Obsidian rename; the Hatcher entities.
20. Romdenh-Romluc twice (D-07, I-11, G-10, L-09): which copy stays.
   **Answer (19 Oct, 16:35):** keep the 14 Oct set (catalog note A and its 10 notes); the 15 Oct PDF, catalog note and 10 notes go to `.trash` through Obsidian; links checked after.
21. *Gifts from the Goddess*: merge the 103 "Section" notes (D-23) / leave; the 66 Word-bookmark labels (J1-09).
   **Answer (19 Oct, 16:35):** merge the 103 'Section' notes into the titled note before each (≈93 notes); fix the 66 Word-bookmark labels; rename the 'Part N' notes from the contents (Goodall, *Neganthropocene*, D-14/D-15).
22. D28's downloads on no list (Plato *Laws*/*Letters*, the Davidson Talmud, the SUP Aramaic Zohar; D-21, B-13, J3-16); the six free technics works Area D found.
   **Answer (19 Oct, 16:35–16:40):** Free downloads gets: the William Davidson Talmud (Sefaria, CC BY-NC 4.0) — English only, one note per folio, about 25–35 MB (estimate; the export is downloaded only with permission in the corrections week); the technics works: Hobbes *De Corpore* and Aristotle *On Memory* (pages confirmed), Bergson, Augustine *Confessions* X, Ashby marked 'to confirm'; no Plato *Laws*/*Letters* ("we have all the Plato I want already"); the SUP Aramaic Zohar: not listed (not chosen).
23. D15 (J3-01): the *Recognition Sutras* companion PDF in `.trash` — restore and merge as answered / leave deleted.
   **Answer (19 Oct, 16:35):** not chosen: the Wallis companion PDF and its notes stay deleted (Stephen's word now).
24. Bang's thesis (J3-02) and Jayaratha's letters (J3-03): Stephen's word, recorded.
   **Answer (19 Oct, 16:35):** Bang's thesis: do it (footnotes whose text is in the PDF layer, as for Rastogi, option 3; the Devanagari-image notes stay); Jayaratha: leave the Š (printed).

**E. Hygiene, size and documentation**
25. `.trash` (1.1 GB) and the backups (I): empty `.trash` after (5) and (10) and (23); delete the 24 verified backups of 6–14 Oct (706 MB) and the 182 MB scratch now; `backup-audit-fixes` (1.23 GB, holds the only original page images of *Questions and Doubts*) after the new layers are accepted; today's three backups: keep until the corrections week.
   **Answer (19 Oct, 16:40):** keep everything until after the corrections week.
26. The OCR tags in the Mālinī notes (G-05, K-31, M-02): remove — a tag, so Stephen's word.
   **Answer (19 Oct, 16:40):** remove the 8 junk tags (Stephen's word).
27. Marked-pages naming (G-02): `quick-capture` names the note after the book — a suffix "(marked pages)" or a folder? The Ruiz duplicate.
   **Answer (19 Oct, 16:40–16:50):** `quick-capture/view.js` L54 names a marked-pages note '<book> — marked pages'; the existing blank Ruiz marked-pages note goes to `.trash` (Stephen: the existing ones are blank and can be deleted); the Guide's and Welcome's bare link then resolves to the catalog note. **Added by Stephen:** delete all the "not yet written" tasks dated before 19 Oct 2026 (to the corrections to-do; located by job c40).
28. The 1,547 page markers without ids in 350 notes (M-01; BCP, Paramārthasāra, Essential Kabbalah…): add ids / reword Guide L31.
   **Answer (19 Oct, 16:40):** add the missing ids (the Guide's sentence stays true).
29. `work` on the Devī Māhātmya side notes (M-05, check: `collection` fits the 16 auxiliary hymns; 5 name another source) and the Paramārthasāra notes (M-06; the catalog note's title).
   **Answer (19 Oct, 16:40):** add `work`/`collection` to the 42 notes as the check pass corrected it: `work: "Devī Māhātmya"` on the main notes, `collection` on the 16 auxiliary hymns (5 name another source), the Paramārthasāra notes with the catalog note's title and the missing frontmatter.
30. Stephen's own notes (report only): `type: daily` on 7 journal notes (G-17); `occasion` "Easter 5A" (J1-24); `Journal/2026/2026-10-03.md` L15 first mention (E-10); the wish-list lines 35 and 45 — diffs for him.
   **Answer (19 Oct, 16:50):** diffs for `type: daily` on the 7 journal notes, `occasion: Easter-5A`, and the 2026-10-03 first mention; the wish-list lines 35 and 45 stay his.
31. House rules (K-17): the plugin-save exception, laptop agents editing directly, `vault_agent`, runner order, the size and wait figures; and the record of the tags rule being shown first (J3-18).
   **Answer (19 Oct, 16:55):** yes — the lead drafts the six wording changes; Stephen approves the text before they go in.
32. The routine prompts (L-07, K-19…K-27): baselines, scripts, the 14 Oct figures, the Gemini walk-through's archiving; the "after October" note on routine prompts and the Dataview watch (Part 3's own item).
   **Answer (19 Oct, 16:55):** yes — refresh with the 19 Oct baseline, the scripts named, the Gemini walk-through archived, the Dataview watch added.
33. `EPOCH` in one place (M-03, F-11); `type: text` note for the Devī Māhātmya collection (J3-12); the lexicon on the phone (D24.4, I-15).
   **Answer (19 Oct, 16:55):** one copy of the cycle start date in `paths.json`, read by the five scripts; a `type: text` index note for the Devī Māhātmya collection; the Greek lexicon stays on the phone (not chosen).

