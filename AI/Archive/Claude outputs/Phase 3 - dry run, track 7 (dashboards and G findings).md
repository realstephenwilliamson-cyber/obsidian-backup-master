# Track 7 – dashboards, scripts and the remaining G findings: full change list (batch 2)

Companion to `/home/claude/p3/batch2/t7.md`. Built on 7 Oct 2026 from the 04:08 UTC snapshot, brought up to the vault as it is now: last night's track 5 (LXX blank lines), track 2 (Tanya and Mei HaShiloach links), track 1 (Zohar) and the Zohar 8.03/8.04 swap, with Obsidian's link rewriting (1,348 link targets) and the 52 follow-up ops. Nothing in this track has been applied.

## Files

- Ready ops, in the order they are applied: `/home/claude/p3/batch2/t7-ready-ops.json` (4,321 ops). Each op keeps its `why` and `source`, and names its draft (`draft`) and kind (`kind`).
- Ops that wait for an answer: `/home/claude/p3/batch2/t7-question-ops.json`, keyed by question and option (D5, D6, D8, D9, D10, D11). D1–D4, D6 (b, c) and D7 (B or C) are built after your answer.
- Every change, one row per op (ready and question ops): `/home/claude/p3/batch2/t7-changes.tsv` (columns: n, set, kind, note, op, before, after, why, source, draft; newlines written `\n`). Whole-file script rewrites show their hash, not their text; their diffs are in `drafts/t7/today/dryrun.md` and `drafts/t7/fsafe/dryrun.md`.
- Scripts, in `/tmp/claude-0/-home-claude/20317441-6de2-5779-9466-04abb26557ee/scratchpad/t7b2/`: `current.py` (rebuilds the vault as it is now), `build.py` (assembles and checks the ops), `order.py` (order against the other tracks).

## 1. Counts by kind (ready)

| Finding | What | Ops | Notes or files |
|---|---|---|---|
| F3 | Home's Today block: fixed order, red error lines | 5 | Home, Home (mobile), 3 view scripts |
| F5, F19, F29 (a, b) | Date box (`today-header`): table ends named, keeps itself current | 1 | 1 script |
| F4, F29 (d) | Monier-Williams lookup keeps its state; unreadable dictionary reported | 1 | 1 script |
| F4 | Devanagari search keeps its state | 1 | 1 script |
| F29 (e, f) | Quick capture: names without Latin letters; empty heading reused | 1 | 1 script |
| F29 (i) | Review and sweep buttons work only in the actions note | 2 | 2 scripts |
| F29 (g) | Homily template: a taken name no longer leaves the note blank | 1 | Templates/Homily |
| F29 (h) | Hub template: 11 placeholder links become italic words | 4 | Templates/Hub |
| F5 | Prompt *Extend the calendar tables*: the date-box sentence | 1 | 1 prompt |
| F23, F24 | *Setting up a new device* in the Guide, and pointers | 4 | Vault Guide (3), Welcome (1) |
| G21 | NT footnote references open the JPS verse | 72 (85 links) | 46 NT notes |
| G21 | NT index sentence | 1 | NT index |
| G26 | A space after an italic label in LXX footnotes | 2,370 (2,544 places) | 509 LXX notes |
| G39 | Collect block ids named after their occasion | 128 | 4 collect notes |
| G51 | Zohar vols 10 and 12: footnotes and spaced titles | 28 | 5 notes |
| G19 | Previous/index/next line | 1,701 | LXX 1,112; Tractates 124; Mārkaṇḍeya 136; Pritzker vols 2–10 and 12 141; Tanya 122; Mei HaShiloach 66 |
| **Total** | | **4,321** | |

## 2. Checks run for this list (by script, on a copy of the notes rebuilt as they are now)

- All 4,321 ready ops applied in order: every `find` occurs once at its turn, every whole-file rewrite matches its hash, **0 refused**. Every question option applied on top of them: 0 refused (D6 (a) in place of the date-box op, which it replaces).
- The nine rewritten scripts, and the D6 (a) variant of the date box, parse as Dataview runs them (wrapped in an async function; `node --check`).
- Every new link resolves to one note (base names from `meta.json`, with the 8.03/8.04 swap), and every `#^id` or heading it names exists after the ops.
- G21: with link markup removed, every changed line reads as before. G26: only spaces added. G39: only ids change. G19: one line added per note, right under the note's first heading, in the NT and Tanakh form.
- No op adds the divine name; nothing under `.obsidian/` changes; no note of yours is touched.
- **Order against the other tracks** (`order.py`): with their pending ops first and these after, 0 of these are refused (apart from G39's 128 renames, which are refused after track 4's identical step, as they should be). The other way round, theirs would be refused: the Augustine map (124 tractates, where G19 puts its line; its `find` spans the title and the Source callout) and track 2's BCP links (2 notes shared with D9). So these go in **after** the other tracks' batch-2 ops on the same notes.

## 3. Twenty examples

1. **Home and Home (mobile), Today block** (F3):
   ```
   await dv.view("Templates/Views/today-study")
   await dv.view("Templates/Views/today-verses")
   await dv.view("Templates/Views/daily-office")
   ```
   →
   ```
   // The three parts are made first, in this order, and each view draws into its own, so the order is fixed (F3)
   const study = dv.container.createDiv(), verses = dv.container.createDiv(), office = dv.container.createDiv();
   await dv.view("Templates/Views/today-study", { container: study })
   await dv.view("Templates/Views/today-verses", { container: verses })
   await dv.view("Templates/Views/daily-office", { container: office })
   ```
2. **today-study, an error** (F3): before, the study lines are simply missing; after, a red line `today-study failed: <message>` in their place.
3. **Date box, 15 Nov 2029** (F5): before, nothing; after, `Tables ending soon: the panchang on 31 Dec 2029 · the Shabbat and Yom Tov times on 29 Dec 2029; see Extend the calendar tables.`
4. **Date box, from 1 Jan 2030** (F5, F29 b): `Panchang: no row for today in Library/Calendars (the tables run to 2029).` → `Panchang: no table for 2030 (Library/Calendars/Panchang 2030 (Hickory).md not found); see Extend the calendar tables.`
5. **Quick capture, title सौन्दर्यलहरी, no author** (F29 e): file `Library/Catalog/Hinduism/.md` → `Library/Catalog/Hinduism/Untitled 2026-10-07 1046.md`, with a message asking you to rename it.
6. **Review button pasted into another note** (F29 i): a live "Do this" button → `These buttons work only in Vault review - actions.`
7. **Templates/Hub** (F29 h): `- **Primary:** [[Link to Text 1]] · [[Link to Text 2]]` → `- **Primary:** *Link to Text 1* · *Link to Text 2*`
8. **Templates/Homily, a taken name** (F29 g): before, Templater stops and the note stays blank; after, the note is filled, keeps its name, and under *Notes* says `Not renamed to "2026-10-11 Proper 23A": Destination file already exists!`
9. **Prompts/Extend the calendar tables** (F5): `Home's date box reads these tables. Once they run out it shows only the date.` → `Home's date box reads these tables. Once fewer than 60 days of a table are left, the box says so; once a table has run out, the box names it instead of leaving its line out.`
10. **Vault Guide, Sync and backups, Careful** (F23): `The October 2026 plan (phases 3 and 8) works out the settings for each device.` → `So [[#Setting up a new device]] turns it on, and keeps the e-texts and old drafts off the phone with excluded folders instead.`
11. **Welcome, On the phone** (F24): adds `The other settings a new phone or tablet needs are in [[Vault Guide#Setting up a new device|Setting up a new device]].`
12. **Romans 11, note 29** (G21): `[[Job 41|Job 41:11]]` → `[[Job 41#^41-3|Job 41:11]]`
13. **Romans 3, note 3** (G21): `[[Psalms 051|Psalm 51:4]]` → `[[Psalms 051#^51-6|Psalm 51:4]]`
14. **Matthew 5, note 6** (G21): `[[Torah 17 - Yitro#Chapter 20|Exodus 20:13]]` → `[[Torah 17 - Yitro#^20-13|Exodus 20:13]]`
15. **LXX Judges 12, note 5** (G26): `*Alex.*σύνθημα, *q. d.*watchword.` → `*Alex.* σύνθημα, *q. d.* watchword.`
16. **BCP collects, Holy Days, both rites** (G39): `^collect-preface-of-the-apostles-4` → `^collect-all-saints-day`
17. **Zohar 12.02 Preface** (G51): `“glimpsed and was wounded.”2` → `“glimpsed and was wounded.”[^2]`, and the numbered paragraph `2. See Vol. 9, pp. 791–92, n. 74.` → `[^2]: See Vol. 9, pp. 791–92, n. 74.`
18. **Zohar 10.02 Preface** (G51): `# M I D R A S H H A - N E ’ L A M` → `# MIDRASH HA-NE’LAM`
19. **Zohar 8.03 - Parashat Qedoshim** (G19, new name): under `# Parashat Qedoshim`, a new line `← [[Zohar 8.02 - Preface]] · [[Zohar (Pritzker)]] · [[Zohar 8.04 - Parashat Emor]] →`
20. **Tanya - Likkutei Amarim 53** (G19, one run through the five parts): `← [[Tanya - Likkutei Amarim 52]] · [[Tanya (Kehot)]] · [[Tanya - Shaar HaYichud VehaEmunah - Chinukh Katan]] →`

## 4. F3 in detail: what changes, and the tests

**What you will see on Home and Home (mobile).**
- The order is fixed: the study lines and buttons, then *Today's verses*, *Translation*, *Daily Office*. Now the parts appear in whatever order their file reads finish.
- If one part fails, a red line takes its place (`today-study failed: …`, `today-verses failed: …`), and the other parts still draw. The Office already caught its errors but stayed folded as "Daily Office · error"; it now opens itself and shows the message in red.
- A refresh that lands while Home is still drawing no longer shows a part twice.
- Everything else is the same: text, buttons, links, one framed box.

**Evidence so far (cloud, not Obsidian).** The checker ran old and new on every day from 1 Oct 2026 to 15 Jan 2030 (1,203 days): 0 differences in output. In a timing model, a refresh mid-draw showed a part twice in 30 of 30 runs before and 0 after; the order was study, verses, translation, Office every time after. That is a model of Dataview's timing, not Obsidian; the Obsidian tests below are the evidence.

**Obsidian tests I run** (they change no file; a console helper swaps the file reader for a moment and puts it back):
- Before applying: a screenshot of both Homes; a forced read error in the study plan (expected: the study lines vanish with no message, which is the fault); a refresh forced mid-draw (expected: a part shows twice; if not, I lengthen the delay until it does, so the test after means something).
- After applying: the screenshot comparison (same single box, same order, no red line, spacing as before); three reloads (same order, nothing doubled); folded sections and a homily button behave as before; forced errors in the study plan, a verse note and the lectionary (red lines where expected, the Office opened with its message); the mid-draw refresh (each part once, in order); the same on Home (mobile).
- If anything is wrong, the five files go back from the applier's backup.

## 5. The F fixes in detail (12 ops)

- **Date box** (`today-header`, F5, F19, F29 a–b). Same output as today on every date up to 30 Oct 2029 (checker: 12,509 date-times). Then: "Tables ending soon" from 31 Oct 2029 (Shabbat table) and 2 Nov 2029 (panchang); "Shabbat times: the table ended on 29 Dec 2029" after its last row; from 1 Jan 2030 the missing panchang table is named, and the Hebrew date says it does not turn at sunset. A device without the Hebrew calendar says so instead of showing the civil date as if Hebrew. The box checks the clock once a minute: at sunrise, sunset and the Shabbat times it redraws itself only (open sections below stay open); at midnight it asks Dataview to redraw Home.
  - **Gate before applying:** the midnight redraw uses Dataview's `index.touch()`. Nothing in the workspace shows that it makes Dataview redraw (the checker's point). Before applying, I run the checker's test in the console with Home open: mark the date box, call `touch()`, and see after 4 s whether the box was replaced. If it was not, this op waits, and I add a fallback (Dataview's own refresh command) and show it to you first.
- **Monier-Williams lookup** (F4, F29 d): the typed word, the results and opened entries survive a redraw; a fresh open still starts empty. An unreadable dictionary file is reported instead of "Loading…" for ever. The headword column is found by name (same column as now).
- **Devanagari search** (F4): typed text and the two tick boxes survive a redraw.
- **Quick capture** (F29 e, f): see example 5; a Hebrew author with a Latin title no longer gives `- Title`; tapping a book twice without a photo reuses the empty dated heading.
- **Review and sweep buttons** (F29 i): see example 6. In the actions note nothing changes (every place still shows "✓ Done …").
- **Homily template** (F29 g): example 8. The suggested date on a Sunday is question D5.
- **Hub template** (F29 h): 11 placeholder links → 0; the words stay, in italics. Your four hubs are not touched.
- **Prompt sentence** (F5): example 9, reworded as the checker found (the box first shows a table 59 days before its last day, so "from 60 days before" was a day off). Its source line is 12, not 13.
- **Obsidian tests afterwards** (from `drafts/t7/fsafe/tests.md`): the date box looks the same today; fake dates in the console for the table ends (no buttons pressed while a fake date is set; Obsidian restarted afterwards, since the fake date affects other plugins too); the lookup boxes keep their text after a redraw; quick capture with a Devanagari title; review buttons inert in a scratch note; two homilies for the same Sunday; a new hub without placeholder links. Notes the tests make are deleted.

## 6. The device section, as it will read

Inserted between *Sync and backups* and *History*:

```markdown
## Setting up a new device

Obsidian Sync's own settings stay on the device where you set them, and so does Templater's trigger. Everything else the vault needs comes through Sync once the switches below are on. Sync has been off since the upgrade began on 4 Oct 2026. When it is turned back on, go through this list on this computer first, then on the phone and on the tablet as each one first opens the vault; later, on any new device and after reinstalling Obsidian.

1. **Connect.** On this computer, turn Sync back on in Settings → Sync; on a phone or tablet, connect it to the remote vault there. If Obsidian lets you, set step 2 before the first sync starts, so that what step 2 leaves out is never synced.
2. **Sync settings on this device** (Settings → Sync):
    - *Sync all other types*: **on**. Home's scripts (`Templates/Views/*/view.js`) and the Monier-Williams dictionary (a `.tsv` file) are "other types"; without them Home's blocks show *custom view not found* and the lookup box cannot load the dictionary.
    - *Images*: on, for the Sanskrit card's pictures and the photos of marked pages.
    - *PDFs*: off on every device, this computer included. The PDFs stay in the vault on this computer and out of Sync, so on a phone or tablet *Translation* under *Today's verses* and the catalog's `files:` links do not open.
    - On a phone or tablet, under *Excluded folders*: `Texts/MUKTABODHA-LIBRARY-DEVANAGARI`, `Texts/MUKTABODHA-LIBRARY-IAST_2026_02_20` and `Writing/_Originals`. That is about 0.4 GB: the Muktabodha e-texts (plain `.txt` files, which Obsidian does not open) and the old drafts in `Writing/_Originals`.
    - Every switch that syncs settings: main settings, appearance, themes and snippets, hotkeys, core plugins and their settings, and the active and installed community plugins. They bring the plugins with their settings, the Minimal theme and the three CSS snippets, the daily-note folder, and the main settings: links updated when a note is renamed, deleted files to `.trash`, pasted images and photos to `Attachments`, `Writing/_Originals` kept out of search, and *Strict line breaks* (Settings → Editor), so a note looks the same in Reading view on every device.
    - Conflicts: the same choice on every device.
3. **Let the first sync finish**, then close and reopen Obsidian. In Settings → Community plugins, turn community plugins on if they are off (Restricted mode), and check that the plugins listed under [[#Plugins]] are there and on (Pane Relief runs only on a computer, and Editing Toolbar is set not to load on a phone or tablet). Then check Settings → Dataview → *Enable JavaScript queries*: it comes on with the plugin settings, but a Dataview installed by hand has it off, and Home then says *Dataview JS queries are disabled*.
4. **Templater, once the first sync is done:** Settings → Templater → *Trigger Templater on new file creation*: on. This switch is kept on each device and does not sync. Home's buttons fill their notes without it, but the Calendar, the core Daily notes command and notes you make yourself in `Journal`, `Writing/Homilies`, `Notes/Concepts` or `Notes/Hubs` come out blank. While it is on, Templater also acts on new notes that arrive through Sync, so turn it on only after the first sync is over. Its other settings (the folder templates, and any excluded folders) come with the plugin settings.
5. **The phone's start page** (once, on any device; it syncs with the plugin settings): Settings → Homepage → *Separate mobile homepage* → `Home (mobile)`. Until it is set, the phone opens the full Home.
6. **Smart Connections**, if you use it there: each device builds its own index in `.smart-env/`, which Sync leaves out. Before the first index, open *Manage excluded folders* and check it has the list given under *AI plugins* above.
7. **Test** (one minute). Open Home, or Home (mobile) on the phone: the date box, the Today block with the Daily Office, and the Sanskrit card with its pictures all show. Press *Start today's note* (or *Open today's note*): the note opens filled in. In the [[Monier-Williams Quick Lookup Guide|Monier-Williams lookup]], look up `prakasa`: entries appear (the first search takes a moment).

Omnisearch (with its PDF indexing setting), Tasks, Excalidraw, PDF++ and Calendar need nothing set on the device: their settings come with the plugin settings.
```

The *On Standard* and *Careful* bullets under *Sync and backups* become:

```markdown
    - **On Standard:** in Settings → Sync, turn off *PDFs* and *Audio*, keep *Sync all other types* on, and exclude the e-text folders and `Writing/_Originals` (see [[#Setting up a new device]]). Notes, images, scripts and Bases then come to about 0.17 GB. Standard does not sync a file over 5 MB: the Monier-Williams dictionary (30 MB) and two DjVu books stay on this computer, and the lookup box works only here.
    - **Careful:** Home's scripts (`Templates/Views/*/view.js`) and the Monier-Williams TSV count as other types too, so with that switch off they don't reach the phone or tablet, and Home's Today block and the lookup box won't work there. So [[#Setting up a new device]] turns it on, and keeps the e-texts and old drafts off the phone with excluded folders instead.
```

Sizes from `meta.json` (7 Oct): notes 101.5 MB, images 70.8 MB, other types outside the three folders 73.9 MB; less the dictionary (30.3 MB) and the two DjVu books (11.5 and 30.6 MB): 173.7 MB. The three folders hold 1,098 files, 433.7 MB. `Writing/_Originals` holds 100 files: 86 .docx, 1 .doc, 2 .pptx, 3 .txt, 5 .pdf and 3 .md (`gospel_recognition_revised_complete`, `second_domestication_outline`, `sea-peoples-flowchart`).

Changes from the checked draft: the *On Standard* bullet (checker problem 1: it still advised the switch off); the `Writing/_Originals` wording (problem 2); the opening paragraph and step 1 written for turning Sync back on (your message of 00:45); *PDFs* off on every device (the same message: the PDFs are to be kept out of Sync); Editing Toolbar named in step 3 (checker's minor note); step 4's reason worded as an instruction. Obsidian tests after applying: the section shows as one numbered list with the bullets nested under step 2; the three heading links jump to it; the lookup link opens the guide note.

## 7. The G findings in detail

**G21: the 61 distinct references changed (85 links).** Before, each opened the chapter (or the parashah note's `#Chapter` heading); after, the JPS verse that holds the words. Each row: the label as printed → the JPS verse it opens after the change.

| Label | After (JPS) | | Label | After (JPS) |
|---|---|---|---|---|
| Psalm 4:4 | Psalms 004 ^4-5 | | Psalm 69:4 | Psalms 069 ^69-5 |
| Psalm 5:9 | Psalms 005 ^5-10 | | Psalm 69:9 (×2) | Psalms 069 ^69-10 |
| Psalm 8:2 | Psalms 008 ^8-3 | | Psalm 69:21 (×3) | Psalms 069 ^69-22 |
| Psalm 8:4–6 | Psalms 008 ^8-5 | | Psalm 69:22–23 | Psalms 069 ^69-23 |
| Psalm 8:6 | Psalms 008 ^8-7 | | Psalm 69:25 | Psalms 069 ^69-26 |
| Psalm 18:49 | Psalms 018 ^18-50 | | Psalm 102:25–27 | Psalms 102 ^102-26 |
| Psalm 19:4 | Psalms 019 ^19-5 | | Psalm 140:3 | Psalms 140 ^140-4 |
| Psalm 22:1 (×2) | Psalms 022 ^22-2 | | Job 41:11 | Job 41 ^41-3 |
| Psalm 22:7 | Psalms 022 ^22-8 | | Isaiah 9:1–2 | Isaiah 08 ^8-23 |
| Psalm 22:8 | Psalms 022 ^22-9 | | Isaiah 64:4 | Isaiah 64 ^64-3 |
| Psalm 22:15 | Psalms 022 ^22-16 | | Jeremiah 9:24 (×2) | Jeremiah 09 ^9-23 |
| Psalm 22:18 (×4) | Psalms 022 ^22-19 | | Ezekiel 20:11 (×2) | Ezekiel 20 ^20-11 |
| Psalm 22:22 | Psalms 022 ^22-23 | | Ezekiel 20:34 | Ezekiel 20 ^20-34 |
| Psalm 31:5 | Psalms 031 ^31-6 | | Hosea 1:10 | Hosea 02 ^2-1 |
| Psalm 34:12–16 | Psalms 034 ^34-13 | | Hosea 2:23 (×2) | Hosea 02 ^2-25 |
| Psalm 34:20 | Psalms 034 ^34-21 | | Hosea 11:1 | Hosea 11 ^11-1 |
| Psalm 36:1 | Psalms 036 ^36-2 | | Hosea 13:14 | Hosea 13 ^13-14 |
| Psalm 38:19 | Psalms 038 ^38-20 | | Exodus 20:12, 20:12–16 (×6) | Yitro ^20-12 |
| Psalm 40:6–8 | Psalms 040 ^40-7 | | Exodus 20:13, 20:14, 20:13–17 (×5) | Yitro ^20-13 |
| Psalm 41:9 | Psalms 041 ^41-10 | | Exodus 20:17 | Yitro ^20-14 |
| Psalm 44:22 | Psalms 044 ^44-23 | | Exodus 22:28 | Mishpatim ^22-27 |
| Psalm 45:6–7 | Psalms 045 ^45-7 | | Numbers 16:5 | Korach ^16-5 |
| Psalm 51:4 | Psalms 051 ^51-6 | | Numbers 30:2 | Matot ^30-3 |
| Psalm 53:1–3 | Psalms 053 ^53-2 | | Deuteronomy 5:16, 5:16–20 (×6) | Vaetchanan ^5-16 |
| Psalm 62:12 | Psalms 062 ^62-13 | | Deuteronomy 5:17, 5:18, 5:17–21 (×5) | Vaetchanan ^5-17 |
| Psalm 68:18 | Psalms 068 ^68-19 | | Deuteronomy 5:21 | Vaetchanan ^5-18 |
| | | | Deuteronomy 13:5 | Re'eh ^13-6 |
| | | | Deuteronomy 29:4 (×3) | Ki Tavo ^29-3 |
| | | | Deuteronomy 29:18 | Nitzavim ^29-17 |

JPS counts psalm titles as verse 1, and joins the commandments against murder, adultery, theft and false witness in Exodus 20:13 and Deuteronomy 5:17 (so "Exodus 20:14" opens 20:13, "20:17" opens 20:14). The checker matched every one against the standard Hebrew–English numbering. The NT index sentence that said "otherwise to the chapter" becomes: "A verse reference opens the JPS verse that holds the words cited, which may be numbered differently: Psalm 69:9 opens Psalms 69:10."

**G26: 2,544 places in 509 LXX notes.** Labels: *Gr.* 1,589; *Or,* 353; *Heb.* 172; *Alex.* 132; *Lit.* 110; *i. e.* 55; *q. d.* 39; others 94 (*or,* 20, *sc.* 16, *A. V.* 8 …). This is the checker's recount; the draft's breakdown was wrong, its total right. None of these labels is followed by a space anywhere in the LXX notes now. Full list: `drafts/t7/gtext/g26-lines.tsv`.

**G39: 128 ids in 4 notes** (both rites, Seasons of the Year and Holy Days): 117 `preface-of-…` and 11 others, each renamed after the occasion title above its collect, with `-2`, `-3` for the second and third Christmas collects. Map: `drafts/t7/gtext/g39-id-map.tsv`. Track 4's R2 contains the same 128 renames; they are applied once.

**G51: 28 ops in 5 notes.** Zohar 10.02 (4 footnotes), 12.02 (5) and 12.03 (3): the fused numbers become Markdown footnotes, and the numbered paragraphs become their definitions; the trailing `[p. 1]` moves out of the last footnote onto its own line. Four letter-spaced titles closed up, letters unchanged: `MIDRASH HA-NE’LAM` (10.02), `REFERENCE MATTER` (10.14, 12.12), `ZOHARIC COMPOSITIONS` (12.03).

**G19: 1,701 notes.** The line sits right under the note's first heading (in Mārkaṇḍeya, its `##` chapter heading; in 8.04, its Hebrew title), in the NT and Tanakh form. First and last notes of a run have one arrow. Runs: LXX by book (48 runs; the five one-chapter books get no line), Tractates 1–124, Mārkaṇḍeya in the index's order, Pritzker one run per volume (vols 2–10 and 12; 8.03 and 8.04 under their new names), Tanya one run through all five parts, Mei HaShiloach in the index's order. Where a breadcrumb line already links the index (LXX, Tanya, Mei HaShiloach), it stays, so the index is linked twice there. The five one-chapter LXX books get no line: it would hold only the index link, which their breadcrumb already gives. Every previous link is answered by a next link (1,639 pairs in 62 runs), and all resolve. Examples: `LXX Malachi 03`: `← [[LXX Malachi 02]] · [[LXX (Brenton)]]`; `Tractate 017`: `← [[Tractate 016]] · [[Augustine - Tractates on John]] · [[Tractate 018]] →`; `Markandeya Purana 000 - Acknowledgements…`: `[[Markandeya Purana (Debroy)]] · [[Markandeya Purana 000 - Introduction]] →`.

## 8. Ops waiting for an answer

| Question | Option | Ops | Notes |
|---|---|---|---|
| D5 | a: on a Sunday, suggest that Sunday | 1 | Templates/Homily |
| D6 | a: candle-lighting fix (a new version of the date-box op) | 1 | today-header |
| D8 | a: cited verse or range / b: first verse / c: chapter only | 62 / 58 / 73 | 11 Mei HaShiloach notes |
| D9 | a: rubrics italic, occasion titles headings | 403 | 12 BCP notes |
| D10 | G21 beyond the count / G26 beyond the count | 9 / 71 | 9 NT notes / 56 LXX notes |
| D11 | B14 / B34 / C20 / C34 / E25 psalms / E25 John / A12 / D31 (B) | 7 / 301 / 1 / 450 / 301 / 21 / 4 / 1 | 2 / 77 / 1 / 225 / 301 / 21 / 1 / 1 |

D11's B14 index op carries the words "annotated copy:" before the second set. Each option was applied on top of the ready ops: 0 refused, links resolve.

## 9. Held or left out

- **G19, Pritzker vol. 1 (13 notes):** 11 lines (1.02–1.12) were drafted above the page marker and the title (checker). The whole run is held, to be rebuilt under the title.
- **notes-for-today** (F4 for *Today's verses* and the Office, F5's last-week homily button and "plan ended" line, F19's day and week buttons taking the date when pressed): written against the old scripts, they no longer apply to the F3 texts. Merged later with D2's answer.
- Everything else left out is listed under *Not done* in the section.
