---
updated: 2026-10-15
---
# Audit decisions for Stephen

From the complete vault audit of 14 Oct 2026 (full report in the Claude project, `claude/audit-2026-10-14/`). Items already fixed are not listed. Each decision has a number (D01…), the audit's finding ids in brackets, what the problem is, the options and a recommendation. Answer with the number and a letter (for example "D04: A"), add a note if you like, or say "skip" to leave it for later.

Claude carries out the answers. Anything in Obsidian's settings (`.obsidian`) is yours to change; Claude only tells you where. Your own writing (Projects/, Journal/, concept and hub notes) changes only after you approve a diff.

## Status (15 Oct 2026, 11:00 EDT)

All of D01–D31 that Claude can do are done, except the parts listed as left (details in the [[AI log]]):
- **D01, D03:** your approved wording is in the house rules, the ten prompts and the wish list.
- **D08:** done in full (4,594 markers *[PDF n]*; Törzsök, the *Mālinīvijayottara* and *Questions and Doubts* read from their pages).
- **D09:** a, b done for the five Devanagari PDFs named (the other OCRmyPDF-17 Devanagari PDFs and *The Inner Pilgrimage* left); c done (*Questions and Doubts* PDF and note names; Graham); e done (new OCR, 12 page labels corrected); h done for Wilke and Macdonell, *Atharvavedins* left.
- **D14:** stays A. **D15–D21, D26–D29:** done (D21 with your approved diffs).
- **D20 B:** 169 PDFs renamed; every link kept its form.
- **D22, D23, D24, D25:** yours, in Obsidian's settings (exact steps in the AI log). **D24.3:** done (DjVu books to `.trash`).
- **D30.1:** done (the flash-card catalog note). **D30.2, D30.3:** yours.
- **D31:** a, b, d, e, f done; c done for Goodall; Finn and the other footnote books left.

## Status (15 Oct 2026, 02:00 EDT)

Your answers to D01–D14 came from the Gemini walk-through; D15–D31 are still to come. Carried out tonight (details in the [[AI log]]):
- **D01 A, D03 B:** drafts for you to approve in [[Proposed changes awaiting approval (15 Oct 2026)]]; nothing applied.
- **D02 A:** the Guide stands. Before the first sync, set the excluded folders again for the new remote vault.
- **D04, D06, D07 A; D05 A:** done.
- **D08 A:** first part done (448 labels). Left: about 4,300 markers where the pages around do not settle the number, and the three worst books, which need page reads (see the AI log).
- **D09:** d and f done (to `.trash`), h done for Wilke; a, b, c, e and the rest of h (OCR) not started; no better copy of the *Mālinīvijayottara* was found in Downloads, so e means a new OCR.
- **D10 A:** done for the 40 terms whose form is certain (219 occurrences) and the dashes; 71 terms left, either uncertain or (like samayin) right as they stand.
- **D11:** later. **D12 A, D13 A, D14 A:** done.

## Part 1. Rules and records

**D01. House rules: the end-of-task clean-up** [K-01, K-02; audit action 2]
The house rules say "move `.work/` into the vault trash" at the end of a task, and ten prompts repeat "Clean up .work". Done literally, that throws away the job runner (`.work/plan/phase-3-tools/`) and every backup. Phase 8 actually cleaned only the bundles, `out` and `queue/done`. The rules also carry 5 Oct figures (about 22,400 files; now about 33,800), point to project docs 00–06 (now 00–21), mention Smart Chat, and say nothing about the runner, staging files through the bridge, or keeping PDFs off Sync.
- A. Claude drafts new wording: clean only the session's scratch, never `.work/plan` or the backups. The draft adds the runner restart line, current figures and docs, and the PDFs-off Sync decision. You see a diff before it goes into the rules and the ten prompts.
- B. Leave the rules as they are.
- Recommended: A.

**D02. Has the remote vault been replaced?** [J2-12]
The Guide says the old remote vault was deleted and a new one created on 14 Oct. The records give it as your to-do, and at the audit Obsidian's Sync state still showed the old link (paused).
- A. It is done; the Guide stands.
- B. Not yet; Claude rewords the Guide's two lines as steps still to do.

**D03. The vault wish list** [G-18, K-27]
`Notes/Vault wish list.md` has stale statuses. It names plugins no longer installed (Day Planner OG, TaskNotes, Editing Toolbar, Notebook Navigator, Habit Tracker 21) and says "Dial-in is in phase 9", but the plan ended at phase 8. It also has open items no record mentions, including two of your highlighted lines that were never answered.
- A. You update it yourself.
- B. Claude proposes the updates as a diff (it is your note) and adds the open items to the AI log's list of what is left.
- C. Leave it.
- Recommended: B.

## Part 2. Scripture links and readings

**D04. Misprinted references where the intended verse is certain** [E-21, J1-06, E-05, E-18]
Some books print a wrong verse number for a quotation whose real verse is not in doubt. Examples:
- Pritzker Zohar vol. 5, p. 361, quotes "Before I formed you in the belly, I knew you" and prints "Jeremiah 1:3". It is 1:5, and the volume's own index has 1:3, so the error is the book's.
- "Be as wise as serpents" is printed "Mt 10.6"; it is 10:16.
- Six rows in `AI/Bible references to decide later.md` are marked "leave unlinked" although the intended verse is known and its Septuagint note exists.
The vault treats such cases inconsistently: some link the printed number, some are left unlinked.
- A. Link the verse actually meant, keep the printed text as the link's label, and add a note after it, such as "(printed 1:3)".
- B. Link the printed number, which opens the wrong verse but follows the print.
- C. Leave such references unlinked.
- Recommended: A. The link opens what the author quotes, and the note still shows what the book prints.

**D05. Six wrong rows in the JANT table of Synoptic parallels** [C-04]
Six rows of the table of parallels in the *Jewish Annotated New Testament* print wrong ranges; for example, the Temptation is given as Luke 3.3–12, which is John's preaching (the Temptation is Luke 4.3–12). On 14 Oct the page images were checked: the JANT prints them so. The note `Texts/Crosswalks/Synoptic parallels.md` now says this. The rows still link the printed ranges, so the Synoptic reader shows the wrong passages for those six.
- A. Link the right passages in the table and keep the printed ranges in the note's list.
- B. Keep the printed ranges as the links, as now.
- Recommended: A.

**D06. The leftover Bible references** [`AI/Bible references to decide later.md`; E-06, E-07]
33 rows remain:
- 11 low-confidence decisions;
- 20 references recommended to stay unlinked (misprints, texts the vault lacks);
- 2 Pirkei Avot rows with no recommendation. They belong at Avot 5:21 and 6:2.
There is also a rule question. On 14 Oct some references were linked as guesses even though no candidate verse contains what the author cites, while others were left unlinked for the same reason.
- A. Accept the recommendations as they stand and link the two Avot rows. Adopt the rule "no candidate verse contains the content → leave unlinked"; Claude re-checks the few guesses under it.
- B. You review the 11 low-confidence rows yourself in that note first.
- C. Leave the note as it is.
- Recommended: A (or B if you want to see them).

**D07. Pelikan's "(Vulg.)" references** [E-19]
When Pelikan marks a reference "(Vulg.)" and the verse number is the same in every system, the vault links the JPS translation. The JPS lacks the Vulgate wording he is pointing to.
- A. Link the Douay-Rheims note for references marked "(Vulg.)".
- B. Keep the JPS links.
- Recommended: A.

## Part 3. Page labels

**D08. Pages that print no number** [J2-11, A-01, A-02, H-16]
Each page in a converted book starts with *[p. N]*. Where a page prints no number (blank pages, front matter, plates), the converter used the PDF page number instead. That number looks like a printed page and can repeat a real one: in *Seekers of the Face*, PDF pages 1–16 are labelled "1"–"16", and the real pp. 1–14 come later. About 600 markers across the library are affected. In a few books most labels are PDF numbers: Törzsök's *Doctrine of Magic Female Spirits*, the *Mālinīvijayottara* translation and Whitney's *Grammar*.
- A. A blank page inside a numbered run takes its number from its neighbours (between pp. 13 and 15 it becomes 14). Other unnumbered pages are labelled "PDF n" instead of a page number.
- B. Unnumbered pages get no page number at all, only the PDF block id.
- C. Leave.
- Recommended: A. Claude then relabels the worst books from page reads and corrects the 61 Törzsök citations in the Tantrāloka secondary-literature note. This is a medium-sized job.

## Part 4. Text quality and OCR (the largest job left)

**D09. Which OCR work to do, and when** [H-01, H-02, H-07, H-08, C-06, A-03, H-04, H-13, D-02]
For each item: now, later or never.
- a. In several Devanagari PDFs the text layer has a junk character after almost every short i (ि): Kula Chudamani, Leelamma's Devī Māhātmya, the Taittirīya, Śivādvaita Nirṇaya and others. The Markdown copies are clean, but the junk is what Obsidian's PDF viewer searches and copies.
- b. In some of the same PDFs, the combined Latin+Sanskrit OCR model put Devanagari and digits into the English.
- c. In Graham and in Maximus's *Questions and Doubts*, the Greek is missing or garbled into Latin letters. *Questions and Doubts* also has 34 wrong page labels and 6 note names with OCR junk.
- d. The Knepper excerpt has lost its diacritics, and it duplicates pages of the full Knepper book already in the vault. You choose: keep only the full book (you delete the excerpt, or tell Claude to send it to `.trash`), or re-OCR the excerpt.
- e. The *Mālinīvijayottara* typescript: the English is readable but not reliable. On p. 226, about 6 of 24 lines are lost or partly lost. A higher-resolution OCR might help.
- f. Whitney's *Sanskrit Grammar* is a Google scan with no text layer, and its Markdown copy is a weak OCR (about 1,260 stand-in letters left). A better 400 ppi scan is on the Free downloads list, and you would download it.
- g. Rastogi's *Krama Tantricism* I has no diacritics anywhere in the PDF. The Devanagari quotations are images that could be read; the diacritics need a better copy.
- h. Other letter fixes:
  - Wilke's *Sound and Communication* has ã for ā, a cheap mechanical fix.
  - Macdonell's *Vedic Reader* has stand-in letters.
  - Sanderson's *Atharvavedins* has lost letters.
- Recommended:
  - a, b, c and e: do them; they affect reading and search.
  - d: keep only the full book.
  - f: once you have downloaded the scan.
  - g: only if you find a better copy.
  - h: Wilke now; the others together with the OCR work.
  - Start this in a fresh usage week.

**D10. Dyczkowski's English in the verse notes, second pass** [H-17, J2-14]
In the 5,845 Tantrāloka verse notes, about 105 Sanskrit terms (about 355 occurrences) in Dyczkowski's English have lost their diacritics. The 14 Oct mechanical pass also put an em dash where he prints a spaced en dash.
- A. Restore the diacritics where Monier-Williams gives a single form, checked on page images, and normalise the dashes.
- B. Leave.
- Recommended: A (a medium job).

**D11. Hebrew phrases stored in reverse word order** [B-01, B-02; audit action 14]
In the Pritzker Zohar notes, multi-word Hebrew and Aramaic phrases (6,770 runs in 99 notes) are stored in reverse word order. Invisible direction marks make them display correctly, but search, copying and links get them backwards. Short Hebrew phrases in McClellan's *Deity and Divine Agency* are reversed and also display reversed.
- A. A script stores them in reading order (about 8 need a hand fix), after someone who reads Hebrew checks a sample of about 30.
- B. Leave (the Pritzker display is right).
- Recommended: A if a Hebrew reader can check the sample; otherwise B for now.

## Part 5. Names, properties and structure

**D12. The `pages` property** [LEAD-01, G-09]
Obsidian treats `pages` as a number. Catalog notes use it for a page count, which is fine, but about 5,300 notes (converted chapters, the Zohar notes and others) hold ranges like "887–904", and the properties pane flags those with a warning. Nothing filters on `pages` today.
- A. A script moves the ranges to a new property, `page_range`, in those notes. Catalog `pages` stays a number, and the Guide defines both.
- B. You set `pages` to Text in Settings → Properties (one click; page counts then sort as text).
- C. Leave.
- Recommended: A, before Sync's first upload.

**D13. Chapter notes named after Word bookmarks or file names** [G-07]
About 255 converted chapter notes have names like "Gifts from the Goddess 135 - _Hlk523528562" or "… 9789004432802_webready_content_text, part 2" instead of chapter titles. Most are in *Gifts from the Goddess*; the rest are in about a dozen other books.
- A. Rename them through Obsidian from each book's contents (links update automatically) and fix their headings.
- B. Leave.
- Recommended: A (a medium job).

**D14. Misnamed chapter notes in Dyczkowski's Tantrāloka volumes** [A-07]
19 chapter notes in `Library/Trika/Tantraloka (Dyczkowski)/` are misdescribed:
- front-matter contents pages are titled as chapters;
- chapter 14 is filed as "Chapter Twelve";
- most of chapter 25 sits under another chapter's name.
- A. Rename the notes. Obsidian then rewrites about 5,845 verse-note links and 1,156 study-plan links.
- B. Correct only the contents lists in the volume index notes.
- C. Leave.
- Recommended: B.

**D15. Two catalog notes for one work** [G-16]
*The Recognition Sutras* has two catalog notes: one for Wallis's 27-page audiobook companion and one for the Kṣemarāja book, by the same translator. *Dawning of the Cycles of Consciousness* also has two.
- A. Merge each pair into one catalog note that lists both files.
- B. Keep both.
- Recommended: A.

**D16. Catalog names, titles and two open reviews** [G-20, G-21, G-04, G-01]
1. 33 catalog note names carry a year or publisher, against the "Author - Short title" rule; some need it to tell editions apart. A: rename the ones that don't need it. B: leave.
2. 8 catalog notes kept an old heading after their title was corrected. A: fix the headings.
3. Homer's *Odyssey* (Lattimore) is in review because "the copyright page was not read". The vault's Markdown copy has it: © 1965, 1967; the e-book is from 2009, ISBN 978-0-06-176020-4. A: year 1965, as the vault does for reprints, with the e-book noted; close the review. B: year 2009.
4. The JANT catalog note is still in review as "not checked against a printed copy"; the 44 other primary texts with that same reason were set to `keep` on 14 Oct. Macdonell's dictionary note still says "in review" while its status is `reading`. A: set the JANT to `keep` and refresh the Macdonell line. B: keep the JANT in review.
- Recommended: 1A, 2A, 3A, 4A.

**D17. Small property and tag tidy-ups** [G-10, G-13, L-07, G-12]
- 42 Ruppel notes store `chapter` as text instead of a number.
- `volume` is written three ways ("Vol. 14", 7, "1-12").
- One note in Projects/ has a `text` property holding a link.
- Some tag families split in two and no query reads either form: `#text`/`#texts`, `#Tantrāloka`/`#Tantraloka`, `#zohar`/`#texts/zohar`, `#parashah`/`#parasha`, `#bcp1979`/`#library/bcp-1979`.
- The Tantrāloka word notes call the chapter `ahnika`, where the verse notes say `chapter`.
- Three accidental tags are in Devanagari digits (\#१९like, \#१, \#४).
- A. Claude tidies all of these:
  - Ruppel chapters become numbers and `volume` gets one form;
  - each tag family merges into its more used form;
  - `ahnika` becomes `chapter`, after checking that no view reads it;
  - the three Devanagari-digit tags are escaped.
  The note in Projects/ waits for your diff.
- B. Only the Ruppel numbers and the three tags.
- C. Leave.
- Recommended: A.

**D18. The archived "Vault review - actions" note** [G-15, K-17]
`AI/Archive/Vault review - actions.md` carries 22 one-off `done_*` properties (22 of the vault's 150 property names). It also calls a retired view 17 times; that view is in `.trash`, so those blocks show errors. The Welcome note lists it among its dashboards.
- A. Turn the properties into a checklist in the note's body, replace the 17 blocks with their values, and drop the note from the Welcome's dashboards.
- B. Leave.
- Recommended: A.

**D19. Text collections without a catalog note** [G-22]
13 collections in `Texts/` have no catalog note, unlike the 44 primary texts given `type: text` on 14 Oct: the Tanakh, Torah with Rashi, the NT, the LXX, the Sefaria Zohar, Augustine's Tractates, Tanya, Mei HaShiloach, the BCP 1979, the RCL and others.
- A. Add `type: text` catalog notes for them.
- B. Say in the Guide that collections in `Texts/` need no catalog note.
- Recommended: B (nothing reads them).

**D20. PDF file names** [L-08]
Some PDF names have braces, trailing hyphens or long paths. Renaming them means rewriting `source_pdf` in hundreds of notes and thousands of page links in the verse notes.
- A. Leave.
- B. One rename job, with link checks before and after.
- Recommended: A.

**D21. Your own files** [G-26, G-19; doc 20 item 9]
- In `Projects/_Originals/My Writing`, 2 file names are not plain ASCII, 2 end in "(n)", and one is "Untitled document(1).docx".
- 7 of your 11 daily notes have no properties (`type`, `date`, `verses_read`).
- The two Creed AI notes in `Projects/` have 18 Word footnote links (`#_ftn1` …) that do not resolve.
- A. You handle them when convenient.
- B. Claude prepares diffs (for the footnotes: convert them to Obsidian footnotes).
- C. Leave.
- Recommended: B for the footnotes; A or C for the rest. They are yours.

## Part 6. Obsidian settings and plugins (yours to change)

**D22. Calendar week numbers** [F-01]
Clicking a week number in the Calendar sidebar creates an empty weekly note named like "2026-W42" in the vault root (after a confirmation dialog), not in `Journal/Weeks` as "Week of <Sunday>".
- A. In Settings → Calendar, set the weekly note folder to `Journal/Weeks` and the format to match "Week of YYYY-MM-DD"; Claude gives you the exact string.
- B. Turn week numbers off in the Calendar settings.
- Recommended: B, unless you want to open weekly notes from the Calendar.

**D23. Omnisearch and Smart Connections** [F-12, K-04, F-03]
Both are installed and off. With both on, Obsidian on the laptop used about 3.6–3.8 GB of its 4.4 GB memory limit. If Sync shares the list of active plugins, the phone and tablet get the same on/off state.
- A. Omnisearch on the laptop; Smart Connections stays off for now.
- B. Both on the laptop and off on the phone and tablet. This needs the phone to keep its own plugin list (don't sync the active plugin list).
- C. Both off.
- Recommended: A first; add Smart Connections on the laptop later if memory allows.

**D24. Before Sync's first upload** [I-03, F-14, I-06, I-07, I-12]
1. Text Extractor is off but keeps a 318 MB cache in `.obsidian`. A: delete the cache folder in Explorer, or uninstall the plugin. B: leave.
2. The last full copy of the vault folder dates from 12 Oct, before phases 6–8 and the audit fixes. The PDFs and Muktabodha texts exist only on the laptop. A: make a dated copy of the whole vault folder now.
3. Two DjVu books (42 MB) would go to every device, though Obsidian cannot open DjVu. A: accept. B: move both, through Obsidian, into one folder excluded from Sync on every device.
4. The Greek NT lexicon is 5,462 notes (17.5% of all notes), with 131,567 links into the NT chapters. A: keep it. B: exclude it from the phone's Sync.
5. The 216 flash-card scans are 65 MB of what the phone receives. A: keep them. B: downscale the copies the cards display.
- Recommended: 1A, 2A (strongly), 3B, 4A, 5A.

**D25. Dataview's "no results" boxes** [F-06]
Empty Dataview queries draw "No results" boxes in 9 notes: Study, Notes, the four hubs, a daily note, Scholars and Vocabulary. The daily template's "Earlier on these verses" will be empty on most plan days.
- A. In Settings → Dataview, turn off "Warn on empty result".
- B. Claude rewrites those tables to show a quiet "none yet" line (the hubs are your notes, so a diff first).
- C. Leave.
- Recommended: A.

**D26. Hub feeds and concept links** [E-13, E-14, E-15, E-16]
- The Guide says every hub collects open questions, claims, connections and sources cited. The hubs you approved on 13 Oct have subsets:
  - John: no cites;
  - Tantrāloka: no claims or cites;
  - Technics: no connections;
  - Second Domestication: no cites.
- The feed script would also read task lines (`- [ ] question::`), which the Guide says it skips.
- Two concepts are in a hub's matrix, but their `up` property lacks that hub.
- First mentions of concepts are unlinked in 10 of 81 notes checked.
- A. Correct the Guide to match your hubs and add the task-line filter to the script. With your diffs: fix the two `up` lines and link the first mentions.
- B. Add the missing feed blocks to the hubs instead (your notes, so a diff first).
- C. Leave.
- Recommended: A.

## Part 7. Lists, downloads and housekeeping

**D27. Stale entries on the Wanted and Free downloads lists** [K-18, K-19, A-05]
- Zohar vol. 11 and Ambiguum 7 are now held.
- Origen on John: the vault has Books 1, 2, 4, 5, 6 and 10, so Book XIII is a gap, not held.
- The *Tāntrikābhidhānakośa* I and II are both held, but vol. II's text layer garbles diacritics, so the publisher's open-access PDF may be a better copy.
- GRETIL's Tantrāloka is listed, though on 6 Oct you decided to keep one of two matching copies (it duplicates DCS).
- A. Claude corrects the stale entries, keeps TAK II only as "for a better text layer", and drops GRETIL.
- B. The same, but keep GRETIL with a note of why.
- Recommended: A.

**D28. Free texts to add to the lists** [A-11, D-12, B-10, C-10]
The audit found these free, legal texts missing from both the vault and the lists:
1. Sanderson, "The Śaiva Age" (2009), CC BY 4.0.
2. Plato, *Laws* and *Letters* (Bury's translation, on Perseus), which would complete the dialogues.
3. The Hebrew Tanakh, "Miqra according to the Masorah" (CC BY-SA, Wikisource).
4. The William Davidson Talmud in English (Sefaria, CC BY-NC).
5. The Aramaic text of the Pritzker Zohar (Stanford University Press site; terms of use not stated).
6. For Year B (Mark), which begins 29 Nov 2026:
   - Aquinas's *Catena Aurea* on Mark (CCEL);
   - Chrysostom's Homilies on Matthew (NPNF, CCEL);
   - Cyril of Alexandria on Luke (tertullian.org);
   - Augustine's *Harmony of the Gospels* (New Advent).
- For each: A. add it to the lists (you download; Claude files it) or B. no.
- Recommended: A for all, Year B first.

**D29. The decide-later note and stale verse-note flags** [E-03, E-22, L-03]
- 65 plain-text references stand next to references linked on 14 Oct, and none of them is on any list.
- 27 of the 44 per-book tables in `AI/Bible references to decide later.md` are empty.
- 89 Tantrāloka verse notes keep a `check: "line count"` flag that phase 2 already resolved, and the Tantrāloka hub still says 140.
- 101 other verse notes have 1, 3 or 4 root-text lines and no flag.
- A. Claude links the 65 (as printed; the ones marked LXX to the LXX notes), drops the empty tables, removes the 89 stale flags, corrects the hub's count, and flags the 101 for a look.
- B. The same, without flagging the 101.
- Recommended: A.

**D30. Before you empty `.trash`** [G-03, I-09, L-09]
1. The only file that can close the *108 Sanskrit Flash Cards* review is the booklet cover, now `.trash/Cover.jpeg`; it names the maker (Nicolai Bachman). A: Claude reads it and fills in the catalog note before you empty `.trash`. B: you do it.
2. `.trash` (about 0.9 GB) and the `.work/backup-*` folders (about 0.9 GB) can go once you are happy with the results. Keep `.work/plan/phase-3-tools` (the runner), `.work/out` and `.work/queue`; tonight's backups are in `.work/backup-audit-fixes-2026-10-14/`. When?
3. `Downloads/narrative-engine.zip` (1.7 KB, saved 14 Oct at 19:02) holds a single skill file unrelated to the vault. Is it yours?
- Recommended: 1A; 2 after you have looked at tonight's changes; 3 your answer.

**D31. Improvements that cost usage, no fault to fix** [C-03, C-05, A-13, D-11; doc 20 items 10–11]
For each: now, later or never.
- a. Refill the Synoptic section rows so the reader shows Matthew and Luke beside Mark for the Transfiguration, Gethsemane, the Last Supper and others (52 of 75 rows give Mark only).
- b. Record which passage of John each Chrysostom homily treats, and add a Chrysostom column to the concordance.
- c. Re-convert books whose footnotes came out as plain paragraphs: Goodall (ed.), *Śaivism and the Tantric Traditions* (about 87% of its footnotes), Finn and others, one book at a time.
- d. Link endnote numbers to their notes in the books that keep them as raised numbers.
- e. Make scholar pages (the prompt *Add scholar pages*).
- f. Zohar vol. 11 follow-ups: re-point the 933 Zohar Ḥadash references in the other volumes that now have a Pritzker note.
- Recommended: a and f now-ish (Year B and the Zohar); b, c, d and e later.

## Jobs that need no decision, only usage

Claude can do these whenever you have usage to spare:
- re-point the OCR-split verse links ("Jonah 4:1 1" → 4:11) after reading each on its page (about 37);
- correct the about 54 iota subscripts the Greek pass added to Ehrman's *Fourth Gospel in Origen* where the print has none;
- small safe fixes:
  - the two "no English Zohar note" rows;
  - the 2 Esdras lesson link;
  - the folio index's "Volume 11 is not in the vault" sentence;
  - TĀ 16.203, 16.206 and 16.210;
  - the "hence `status: review`" sentence in the 44 primary-text catalog notes.
