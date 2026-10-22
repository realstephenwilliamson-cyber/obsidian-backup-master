# Phase 3 – dry run, batch 3 (Home follow-ups)

Question B2 in *Phase 3 - decisions, batch 3*. Nothing here has been applied. The drafter's list comes first; the independent checker's report follows it.


Built on 7 Oct 2026 from your ★ answers to D1, D2, D3 (1) and (6b), D4, and D6 (b) and (c). It also merges the F4, F5 and F19 parts of `today-study`, `today-verses` and `daily-office` that did not fit the F3 rewrite. Nothing here has been applied.

**10 ops in 9 files.** They go in after track 7's ops. Seven of them rewrite whole files: five of Home's scripts as track 7 leaves them, the Sanskrit card's script, and `Library.base`. Each is checked against the hash of the text it replaces, so if a file has changed in between, its op is refused and nothing is overwritten.

| # | File | Op | What changes |
|---|---|---|---|
| 1 | `Templates/Views/today-study/view.js` | write | D2, F5 (the last week, and after the plan), F19 (the buttons) |
| 2 | `Templates/Views/today-verses/view.js` | write | F4: *Today's verses* and *Translation* stay open |
| 3 | `Templates/Views/daily-office/view.js` | write | F4: the Office stays open or closed |
| 4 | `Templates/Views/today-header/view.js` | write | D1 (the time-zone line), D4 (the red line) |
| 5 | `Templates/Views/sanskrit-card/view.js` | write | D4 (the red line) |
| 6 | `Templates/Views/quick-capture/view.js` | write | D6 (b) (the form and the filter survive a redraw), D4 (the red line) |
| 7 | `Library/Library.base` | write | D3 (6b): a *Scratch* view |
| 8 | `Templates/Daily note.md` | replace | D3 (1): the first line under the title |
| 9, 10 | `Templates/Homily (Polyphonic).md` | replace ×2 | D6 (c): the Sunday date (as D5), and a taken name |

Bases:
- Scripts 1–3 and 6: the `content` of track 7's ready ops.
- Script 4: D6 (a)'s version.
- Script 5 and `Library.base`: the files as they are now. Neither has changed since 6 Oct; their sizes in the 12:23 file list are the same.
- The two templates: as they will be after track 7 (D5 and the taken-name fix in `Templates/Homily.md`) and track 4's template package (`t4/ops.json`). My three template ops do not touch the lines track 4 changes, so they apply with or without track 4, in either order (tested).
- `Templates/Homily.md` needs nothing from me: track 7 already has D5 and the taken-name fix for it.

## What you will see

### Home: the Today block

**"Not yet written" (D2).** Only the 14 days before today are counted and listed. Nothing is written to the vault. As now, at most 7 days are listed, most recent first. The label now says what it counts.

| Day | Before | After |
|---|---|---|
| today, 7 Oct 2026 | **Not yet written: 4** · Tue 6 Oct, Mon 5 Oct, Sun 4 Oct, Sat 3 Oct | **Not yet written in the last 14 days: 4** · the same four |
| Advent Sunday, 29 Nov 2026 | **Not yet written: 55** · Thu 26 Nov … Fri 20 Nov | **Not yet written in the last 14 days: 12** · the same seven |
| 1 Jun 2027 | **Not yet written: 239** | **Not yet written in the last 14 days: 14** |
| 10 Dec 2029 | **Not yet written: 1154** · Sat 1 Dec … Sun 25 Nov | **Not yet written in the last 14 days: 6** · Sat 1 Dec … Mon 26 Nov |

**The plan's last week, and after it (F5).**
- 26 Nov to 1 Dec 2029: the coming Sunday (2 Dec) has no row in the plan, so no homily button showed. It now comes from today's row: `Start a homily for Advent 1B`, which makes `Writing/Homilies/2029-12-02 Advent 1B.md`.
- From 2 Dec 2029: `No portion today.` → `The study plan ended on Saturday 1 December 2029 (day 1,099); see [[Tantraloka study plan]].`

**The day and week buttons (F19).** Each button takes the date when you press it, not when Home was drawn. Home drawn at 11:50 pm on Wed 7 Oct, buttons pressed at 7:10 am on Thu 8 Oct:
- Before: `Journal/2026/2026-10-07.md` (yesterday).
- After: `Journal/2026/2026-10-08.md`, and Dataview is asked to redraw Home.

Drawn on Saturday night and pressed on Sunday morning, the week button now makes `Week of 2026-10-11`, not `Week of 2026-10-04`. Pressed on the day Home was drawn, the buttons behave exactly as now.

**Open sections stay open (F4).**
- Open *Today's verses*, *Translation* or *Daily Office*. When Dataview redraws Home (any note changes, or Sync brings a file), they stay open, and the translation page is shown again.
- Before, all three closed.
- The next day they start closed.
- In a daily note, the Office still opens by itself the first time. If you close it, it stays closed after a redraw.
- An Office opened only because of an error is not remembered as opened.

### Home: the date box (D1, D4)

**On a device not on Eastern time**, one line is added at the end of the box. Nothing else changes. Example: phone on Pacific time, 4 pm Fri 9 Oct (7 pm in Hickory). The box is as now, plus the last line:

```
> **Next: Shabbat** (times) · begins Fri 9 Oct: 6:39 pm Hickory · 6:06 pm New York · ends Sat 10 Oct: 7:34 pm · 7:04 pm<br>
> Times are for Hickory (Eastern); this device is on another time zone.
```

The box compares the device's clock with New York's, now and half a year ahead.
- Any zone that keeps Eastern time with the same summer-time rules gets no line, for example Detroit or Toronto.
- A zone that differs in either season gets the line all year, for example Chicago, London or Panama.
- Panama gets it although its clock agrees with New York's in winter.

**If the date box fails** (for example, a calendar table cannot be read), it no longer simply vanishes. A red line takes its place: `today-header failed: <message>`. A redraw that lands while the box is still drawing no longer shows it twice. At sunrise, sunset and the Shabbat times it still redraws itself in place, as one box.

### Sanskrit card and quick capture (D4)

The same guard: `sanskrit-card failed: <message>` and `quick-capture failed: <message>` in red, and never shown twice. On Home, in the daily notes and in *Sanskrit Daily Letter Cycle* the card looks as now.

### Quick capture keeps what you typed (D6 b)

This is on Home (mobile). A Dataview redraw now keeps all of these:
- what you typed in *Filter by title or author*, and the filtered list;
- the *Add a book* form: title, subtitle, authors, year, publisher, subject, link, and the two ticks;
- the last message, such as `Added "Kaplan - Sefer ha-Bahir" to Library/Catalog/Judaica.`;
- which of the two parts are open.

Before, all of it was cleared. After *Add book* the form empties as now, and the message stays through the redraw that the new note causes. Opening Home (mobile) afresh starts empty. This is the same method as the lookup boxes.

### The daily note (D3 1)

A new daily note gets one line under its title, with full paths, so a note made from the links goes into `Journal/`. For 7 Oct 2026:

```
# Wednesday 7 October 2026

[[Journal/2026/2026-10-06|← Tue 6 Oct]] · [[Journal/Weeks/Week of 2026-10-04|this week]] · [[Journal/2026/2026-10-08|Thu 8 Oct →]] · [[Home]]
```

Across the year end, the 31 Dec 2026 note links `[[Journal/2027/2027-01-01|Fri 1 Jan →]]`. Notes already written are not changed. The template itself shows no unresolved links: they are written in the template's own `wl` style, as in Homily (Polyphonic).

### Homily (Polyphonic) (D6 c)

- **A taken name.** Before, the note stayed blank, and Templater reported "Destination file already exists!". After, the note is filled, keeps its name and place, and says under its title: `*Not moved to "Writing/Homilies/2026-10-11 Proper 23A (polyphonic)": Destination file already exists!*`
- **The date it suggests when it has to ask.** Made on Sun 11 Oct: `2026-10-18` → `2026-10-11`. On weekdays, unchanged (made on Wed 7 Oct or Sat 10 Oct: `2026-10-11`).

### Library.base (D3 6b)

A seventh view, **Scratch**, at the end: a table of title, author, subject, type and status, sorted by title, with no filter. Use it for one-off filters, so *All* and the other named views stay as saved. The six views and the base's own filter are unchanged.

### What does not change

On every day from 1 Oct 2026 to 15 Jan 2030, the harness gave the same output as track 7's versions, apart from the changes above.
- Home's *Today's verses* and *Daily Office*: identical.
- The study lines: identical except "Not yet written", the 6 last-week days and the 45 days after the plan.
- The date box: identical at four times a day in Eastern time.
- The Sanskrit card (Home and dated) and quick capture: identical.

The CSS snippets select these parts by class, without child selectors (`.block-language-dataviewjs:has(.vp-today)`, `.vp-card-row > img`). So the extra element around each part does not change their look. Check this against the screenshots in tests.md.

## Exact diffs: the templates and Library.base

```diff
--- a/Templates/Daily note.md
+++ b/Templates/Daily note.md
@@ -46,2 +46,10 @@
 out += `# ${isDate ? moment(date, "YYYY-MM-DD").format("dddd D MMMM YYYY") : tp.file.title}\n\n`;
+// First line: yesterday, this week, tomorrow and Home (F32 (1), 7 Oct 2026). The links give full paths, so a note made from
+// one of them goes into Journal/ (and gets this template there), not into the default folder for new notes.
+if (isDate) {
+  const d = moment(date, "YYYY-MM-DD"), prev = d.clone().subtract(1, "day"), next = d.clone().add(1, "day");
+  const wl = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]"; // a wikilink, written so that this template shows no unresolved link
+  const day = m => `Journal/${m.format("YYYY")}/${m.format("YYYY-MM-DD")}`;
+  out += `${wl(day(prev), "← " + prev.format("ddd D MMM"))} · ${wl(`Journal/Weeks/Week of ${d.clone().subtract(d.day(), "days").format("YYYY-MM-DD")}`, "this week")} · ${wl(day(next), next.format("ddd D MMM") + " →")} · ${wl("Home")}\n\n`;
+}
 if (verses.length) {
```

```diff
--- a/Templates/Homily (Polyphonic).md
+++ b/Templates/Homily (Polyphonic).md
@@ -32,3 +32,3 @@
   occ = pick ? pick.basename : "";
-  if (!date) { date = await tp.system.prompt("Date preached or planned (YYYY-MM-DD)", moment().day(7).format("YYYY-MM-DD")); row = date ? await rowFor(date) : null; }
+  if (!date) { date = await tp.system.prompt("Date preached or planned (YYYY-MM-DD)", moment().add((7 - moment().day()) % 7, "days").format("YYYY-MM-DD")); row = date ? await rowFor(date) : null; }
 }
@@ -82,5 +82,9 @@
 out += "## Homiletical Draft\n\n> [!reflection] The Proclamation (*Praedicatio*)\n> \n";
+const name = `${date || moment().format("YYYY-MM-DD")} ${label} (polyphonic)`;
+// a name that is already taken makes the move throw, and the note was left blank (F29 g): keep this name, fill the note, say why
+if (!tp.file.folder(true).startsWith("Writing/Homilies") || tp.file.title !== name) {
+  try { await tp.file.move(`Writing/Homilies/${name}`); }
+  catch (e) { out = out.replace(`# Homily: ${label}\n\n`, `# Homily: ${label}\n\n*Not moved to "Writing/Homilies/${name}": ${e && e.message ? e.message : e}*\n\n`); }
+}
 tR += out;
-const name = `${date || moment().format("YYYY-MM-DD")} ${label} (polyphonic)`;
-if (!tp.file.folder(true).startsWith("Writing/Homilies") || tp.file.title !== name) await tp.file.move(`Writing/Homilies/${name}`);
 %>
```

(Line numbers are those after track 4's template package. Without it, the second hunk starts at line 59.)

```diff
--- a/Library/Library.base
+++ b/Library/Library.base
@@ -80 +80,12 @@
         direction: ASC
+  - type: table
+    name: Scratch
+    order:
+      - title
+      - author
+      - subject
+      - type
+      - status
+    sort:
+      - property: title
+        direction: ASC
```

The diffs of the six scripts are in the appendix.

## Tests and results (cloud harness, not Obsidian)

The harness is `scripts/harness8.js`, a copy of track 7's harness (Node, a mock of Dataview 0.5.68, the vault's real tables from a copy of the notes as they stood before batch 2's question items). Additions, all in the mock:
- `<details>` fires `toggle` as a browser does;
- `dv.pages`, `isConnected` and `getResourcePath`;
- a Templater runner with `tp.file.move`.

"Old" means track 7's versions; "new" means these. Time zone America/New_York unless stated.

| Test | Result |
|---|---|
| **Every day** 1 Oct 2026 – 15 Jan 2030 (1,203 days): Home's Today block, old against new (`sweep.js`) | Study lines: 1,152 identical apart from "Not yet written"; 6 add the Advent 1B button (26 Nov – 1 Dec 2029); 45 have the plan-ended line in place of "No portion today." (2 Dec 2029 – 15 Jan 2030); 0 other differences. *Today's verses* and the Office: 1,203 identical each. |
| D2's window, every day | 1,203 of 1,203: the count and the list match a separate count from the plan tables (the 14 days before the date, portion days only, without a note). The count changes on 1,186 days and is the same on the first 17. Edge check: on 1 Jun 2027, 18 May counts and 17 May does not. 2 Oct 2026, which has a note, is never listed. |
| The same days, each view in a block of its own: `today-verses` with and without `{date}`, `daily-office` with and without `{date, open: true}`, `sanskrit-card` with and without `{date}` | 1,203 identical for each of the six. |
| Date box, 4 times a day (05:00, 12:00, 18:45, 22:30), every day | 4,812 of 4,812 identical. |
| D1, every day, 4 times a day, device on Pacific time | 4,812 of 4,812: old box plus the one line, nothing else. |
| D1, 1 Oct 2026 – 31 Mar 2027, 728 times each | Detroit and Toronto: no line in all 728. Chicago, London, Kolkata and Panama: the line, and nothing else, in all 728. |
| Quick capture, every day | 1,203 identical. |
| Last-week button pressed (28 Nov 2029) | Makes `Writing/Homilies/2029-12-02 Advent 1B.md`. |
| F19 buttons: drawn 23:50, pressed 07:10 next day | Old: yesterday's note. New: today's note, and Dataview asked to redraw (2 calls). Drawn Sat, pressed Sun: new week. Same day: no redraw call, same notes as before. |
| F4: open the three parts, then a Dataview redraw | Old: all closed, translation page gone. New: all open, page shown again. Next day: all closed. Daily note's Office: opens the first time; closed by hand, stays closed (old: reopened). Opened by an error, then redrawn without it: closed. |
| D4 forced errors | `today-header` with the 2026 panchang, the Shabbat table, or the flashcard register unreadable; `sanskrit-card` with the register unreadable; `quick-capture` with `dv.pages` failing. Old: nothing shown, error uncaught. New: one red line, e.g. `today-header failed: forced test error reading Library/Calendars/Panchang 2026 (Hickory).md`. The Today block's own red lines (F3) are unchanged. |
| D4, a redraw while drawing (timing model, 40 runs each) | Shown other than once: `today-header` 40 → 0, `sanskrit-card` 24 → 0, `quick-capture` 11 → 0. The Today block with the merged views: each part once, in place, in 40 of 40. This is a model of Dataview's timing, not Obsidian. |
| Date box's own redraw at sunset (the minute timer fired at 19:05) | One box, one element; the first line moves from `26 Tishri … begins at sunset` to `27 Tishri 5787 (since sunset, 7:00 pm)`. |
| D6 (b): filter, 3 fields, subject, a tick and both parts open, then a redraw | Old: everything reset. New: everything back, the list still filtered. After *Add book* and a redraw: form empty, message still there. A fresh Home (mobile): empty. |
| Daily note template, every day 1 Oct 2026 – 15 Jan 2030 | 1,203 of 1,203: the only change is the new line, with the expected links; 7 Oct 2026 matches the example in t7.md exactly. |
| Homily (Polyphonic), taken name | Old: error, note blank. New: filled, with the *Not moved* line. With no taken name: the same note and new name as before on all 201 plan Sundays and feast days. |
| Ops (`build_ops.py`, applied with `sim.py`) | After track 7 (ready, D6 a, D5) and track 4's template package: 10 applied, 0 refused. Without track 4's package: 10 applied, 0 refused. Track 4's package after these instead: 6 applied, 0 refused, the same result. No `find` is shared with a track 4 or track 7 op. Every script parses as Dataview runs it. |

To rerun (from `scripts/`): `python3 make_mini.py` (reads a copy of the notes as they stood before batch 2's question items), then `node sweep.js`, `TZ=America/Los_Angeles node sweep_tz.js`, `node tests.js`, `node timing_today.js`, and `python3 build_ops.py` (rebuilds and checks `ops.json`). The scripts use moment from the scratchpad's `npm/node_modules`.

Outputs: `test-output/sweep.txt`, `sweep-tz.txt`, `tests.out.md` (28 checks, 28 passed), `timing-today.txt`, `ops-check.txt`, `d1-example.txt`, `diffs.txt`.

Not tested here, only in Obsidian (see `tests.md`):
- that Dataview keeps the same block element across a redraw (F4 and D6 b rely on it, as the lookup boxes do);
- that `index.touch()` makes Dataview redraw (the same gate as the date-box op);
- the look of the three guarded parts.

## Appendix: the six scripts (diff against track 7's versions)

```diff
--- a/Templates/Views/today-study/view.js
+++ b/Templates/Views/today-study/view.js
@@ -8,2 +8,5 @@
 // before the first await, so it keeps its place.
+// Also changed 7 Oct 2026: "Not yet written" counts only the last 14 days (D2); in the plan's last week the coming Sunday's
+// homily button comes from today's row, and after the last plan day a line says when the plan ended (F5); the day and
+// week buttons take the date when they are pressed (F19).
 const VIEW = "today-study", KEY = VIEW;
@@ -68,3 +71,5 @@
   const next = plan.find(r => r[0] > today);
-  dv.paragraph(next ? `No portion today. The plan starts on ${moment(next[0]).format("dddd D MMMM")}.` : "No portion today.", { container: root });
+  const last = plan.length ? plan[plan.length - 1][0] : null;
+  dv.paragraph(next ? `No portion today. The plan starts on ${moment(next[0]).format("dddd D MMMM")}.`
+    : last && today > last ? `The study plan ended on ${moment(last).format("dddd D MMMM YYYY")} (day 1,099); see [[Tantraloka study plan]].` : "No portion today.", { container: root });
 }
@@ -72,3 +77,5 @@
 const b1 = dv.el("button", exists(dayPath(today)) ? "Open today's note" : "Start today's note", { container: root });
-b1.onclick = () => openOrCreate(dayPath(today));
+// Home may have been drawn yesterday (F19): take the date when the button is pressed, and have Dataview redraw Home if it has changed
+const refreshAll = () => { const ix = app.plugins.plugins.dataview?.index; if (typeof ix?.touch === "function") ix.touch(); };
+b1.onclick = () => { const d = moment().format("YYYY-MM-DD"); if (d !== today) refreshAll(); openOrCreate(dayPath(d)); };
 const sundayStart = now.clone().subtract(now.day(), "days").format("YYYY-MM-DD");
@@ -76,3 +83,3 @@
 const b2 = dv.el("button", exists(weekPath) ? "This week's note" : "Start this week's note", { container: root });
-b2.onclick = () => openOrCreate(weekPath);
+b2.onclick = () => { const m = moment(); if (m.format("YYYY-MM-DD") !== today) refreshAll(); openOrCreate(`Journal/Weeks/Week of ${m.clone().subtract(m.day(), "days").format("YYYY-MM-DD")}.md`); };
 // homily buttons: the coming Sunday, and before it any feast with its own readings from today on (in the plan's
@@ -89,2 +96,4 @@
 }
+// in the plan's last week (26 Nov - 1 Dec 2029) the coming Sunday has no row of its own; today's row names it after "→" (F5)
+if (row && comingSunday > today && !plan.some(r => r[0] === comingSunday)) occasions.push([comingSunday, links(row[6]).pop(), false]);
 for (const [d, occ, weekday] of occasions.filter(o => o[1])) {
@@ -99,6 +108,7 @@
 }
-// days not yet written
-const missed = plan.filter(r => r[0] < today && isPortion(r) && !exists(dayPath(r[0])));
+// days not yet written: only the 14 days before today are counted and listed (D2); older days drop off by themselves
+const from = now.clone().subtract(14, "days").format("YYYY-MM-DD");
+const missed = plan.filter(r => r[0] >= from && r[0] < today && isPortion(r) && !exists(dayPath(r[0])));
 if (missed.length) {
-  dv.paragraph(`**Not yet written: ${missed.length}** (most recent first)`, { container: root });
+  dv.paragraph(`**Not yet written in the last 14 days: ${missed.length}** (most recent first)`, { container: root });
   const ul = dv.el("ul", "", { container: root });
```

```diff
--- a/Templates/Views/today-verses/view.js
+++ b/Templates/Views/today-verses/view.js
@@ -5,2 +5,3 @@
 //         (without a container it draws into an element of its own in the block)
+// Changed 7 Oct 2026 (F4): the verses and the translation stay open after Dataview redraws the block.
 // The portion comes from the study-plan tables; the text from each verse note's ^mula and ^iast blocks.
@@ -31,2 +32,5 @@
 }
+// Dataview re-renders this block whenever a note changes (F4): which parts were open is kept, per day, on the block's container
+const st = dv.container.__vpOpen || (dv.container.__vpOpen = {});
+const keepOpen = (el, key) => { el.open = !!st[key]; el.addEventListener("toggle", () => { st[key] = el.open; }); };
 const ends = row ? [...(row[3] || "").matchAll(/\[\[Tantraloka (\d\d)\.(\d{3})/g)].map(m => [+m[1], +m[2]]) : [];
@@ -47,2 +51,3 @@
     const det = dv.el("details", "", { container: root, cls: "vp-verses" });
+    keepOpen(det, "verses " + day);
     const range = list.length === 1 ? `${c0}.${v0}` : `${c0}.${v0}–${c1 === c0 ? "" : c1 + "."}${v1}`;
@@ -69,2 +74,3 @@
       });
+      keepOpen(d2, "translation " + day);
     }
```

```diff
--- a/Templates/Views/daily-office/view.js
+++ b/Templates/Views/daily-office/view.js
@@ -9,2 +9,3 @@
   one the view draws into an element of its own in the block (F3, 7 Oct 2026).
+  If it was opened or closed by hand, it stays so when Dataview redraws the block (F4, 7 Oct 2026).
 
@@ -432,3 +433,9 @@
   const details = container.createEl("details", { cls: "daily-office" });
-  if (opts.open) details.setAttribute("open", "");
+  // Dataview re-renders this block whenever a note changes (F4): whether it was opened or closed by hand is kept, per date,
+  // on the block's container; {open: true} (the daily note) still opens it the first time. Opened by an error, it is not kept.
+  const st = dv.container.__vpOpen || (dv.container.__vpOpen = {});
+  const openKey = "office " + (opts.date ? (typeof opts.date === "string" ? opts.date : moment(opts.date).format("YYYY-MM-DD")) : moment().format("YYYY-MM-DD"));
+  let failed = false;
+  if (st[openKey] ?? opts.open) details.setAttribute("open", "");
+  details.addEventListener("toggle", () => { if (!failed) st[openKey] = details.open; });
   const summaryEl = details.createEl("summary");
@@ -473,2 +480,3 @@
     summaryEl.setText("Daily Office · error");
+    failed = true;
     details.setAttribute("open", "");
```

```diff
--- a/Templates/Views/today-header/view.js
+++ b/Templates/Views/today-header/view.js
@@ -6,2 +6,20 @@
 // within 60 days is announced (F5, F29), and the header keeps itself current while Home stays open (F19, end of file).
+// Also changed 7 Oct 2026: a line says so when this device is not on Eastern time (D1), and an error is shown in red in
+// place of the box (D4), as in the Today block (F3).
+// Where it draws (D4): an element of its own in the block, in place of any left by an earlier run of the block, so a
+// re-render that starts while that run is still reading the tables cannot show the box twice. It is made before the first await.
+const VIEW = "today-header", KEY = VIEW;
+const root = (() => {
+  const el = dv.container.createDiv({ attr: { "data-vp-view": KEY } });
+  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-vp-view") === KEY);
+  if (old) old.replaceWith(el);
+  return el;
+})();
+// An error is shown here, in red, instead of leaving the box silently missing.
+const fail = e => {
+  console.error(VIEW, e);
+  root.createDiv({ cls: "vp-view-error", text: `${VIEW} failed: ${e && e.message ? e.message : e}`,
+    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
+};
+try { // (the body is not indented, to keep the change small)
 const now = moment();
@@ -109,3 +127,14 @@
 
-const box = dv.el("div", `> [!today] ${now.format("dddd, D MMMM YYYY")}\n> ` + lines.join("<br>\n> "), { cls: "vp-today" });
+// The tables are in Hickory (Eastern) time and are compared with this device's clock (D1): say so when the device's clock
+// differs from New York's, now or half a year from now (a zone with other summer-time rules)
+const offEastern = (() => {
+  try {
+    const o = { hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" };
+    const ny = new Intl.DateTimeFormat("en-US", Object.assign({ timeZone: "America/New_York" }, o)), here = new Intl.DateTimeFormat("en-US", o);
+    return [0, 182].some(d => { const x = now.clone().add(d, "days").toDate(); return ny.format(x) !== here.format(x); });
+  } catch (e) { return false; }
+})();
+if (offEastern) lines.push("Times are for Hickory (Eastern); this device is on another time zone.");
+
+const box = dv.el("div", `> [!today] ${now.format("dddd, D MMMM YYYY")}\n> ` + lines.join("<br>\n> "), { container: root, cls: "vp-today" });
 
@@ -135 +164,2 @@
 dv.component?.registerInterval?.(tick.id);                         // stopped when the block is closed
+} catch (e) { fail(e); }
```

```diff
--- a/Templates/Views/sanskrit-card/view.js
+++ b/Templates/Views/sanskrit-card/view.js
@@ -5,2 +5,18 @@
 // All card data comes from the Flashcard Register table, so fixing a row there fixes it everywhere.
+// Changed 7 Oct 2026 (D4, as F3 for the Today block): the card draws into an element of its own in the block, in place of any
+// left by an earlier run of the block (same date), so a re-render that starts while that run is still reading the register
+// cannot show the card twice; an error is shown in red instead of leaving the card silently missing.
+const VIEW = "sanskrit-card", KEY = VIEW + (input && input.date ? " " + String(input.date).slice(0, 10) : "");
+const root = (() => {
+  const el = dv.container.createDiv({ attr: { "data-vp-view": KEY } });
+  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-vp-view") === KEY);
+  if (old) old.replaceWith(el);
+  return el;
+})();
+const fail = e => {
+  console.error(VIEW, e);
+  root.createDiv({ cls: "vp-view-error", text: `${VIEW} failed: ${e && e.message ? e.message : e}`,
+    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
+};
+try { // (the body is not indented, to keep the change small)
 const EPOCH = "2026-10-03";
@@ -12,3 +28,3 @@
 if (!file) {
-  dv.paragraph("Flashcard Register not found at " + REGISTER);
+  dv.paragraph("Flashcard Register not found at " + REGISTER, { container: root });
 } else {
@@ -28,3 +44,3 @@
   if (!row) {
-    dv.paragraph("Card " + n + " is not in the register.");
+    dv.paragraph("Card " + n + " is not in the register.", { container: root });
   } else {
@@ -33,4 +49,4 @@
     const img = s => (s.match(/!\[\[([^\]|\\]+)/) || [])[1];
-    dv.paragraph(`**Sanskrit card ${n} of 108** · ${plain(c[1])} ${plain(c[2])} · ${plain(c[3])} · ${plain(c[4])}`);
-    const box = dv.el("div", "", { cls: "vp-card-row", attr: { style: "display:flex;flex-wrap:wrap;gap:1em;margin:.4em 0;" } });
+    dv.paragraph(`**Sanskrit card ${n} of 108** · ${plain(c[1])} ${plain(c[2])} · ${plain(c[3])} · ${plain(c[4])}`, { container: root });
+    const box = dv.el("div", "", { container: root, cls: "vp-card-row", attr: { style: "display:flex;flex-wrap:wrap;gap:1em;margin:.4em 0;" } });
     for (const p of [img(c[5]), img(c[6])]) {
@@ -41,4 +57,5 @@
     const placement = c.length > 8 ? plain(c[8]) : "";
-    if (placement && placement !== "—") dv.paragraph(`**Body place** ([[Library/Sanskrit/Scriptural Anatomical Mapping (Anga-sthana)|TĀ 15.117–120]]): ${placement}`);
-    dv.paragraph(`[[Library/Sanskrit/Sanskrit 108 Flashcard Register|Register]] · [[Library/Sanskrit/Sanskrit Daily Letter Cycle|About the cycle]] · [[${DRAWING}|Mātṛkā drawing]]`);
+    if (placement && placement !== "—") dv.paragraph(`**Body place** ([[Library/Sanskrit/Scriptural Anatomical Mapping (Anga-sthana)|TĀ 15.117–120]]): ${placement}`, { container: root });
+    dv.paragraph(`[[Library/Sanskrit/Sanskrit 108 Flashcard Register|Register]] · [[Library/Sanskrit/Sanskrit Daily Letter Cycle|About the cycle]] · [[${DRAWING}|Mātṛkā drawing]]`, { container: root });
   }
 }
+} catch (e) { fail(e); }
```

The `quick-capture` diff (116 lines) is in `test-output/diffs.txt`. In short:
- The same guard as above.
- Every `dv.el` draws into the guard's element.
- The state (`dv.container.__vpCapture`) is restored into the filter box, the six fields (`mk` now takes a key), the subject list, the two ticks (`tick` takes a key), the message line (`msg.setText` → `say`) and the two `<details>`.
- After *Add book*, the stored fields are cleared together with the boxes.


---

## Independent check


**10 ops checked, 0 wrong.** All 10 apply, in every order tested. Each does what its ★ says. I found nothing else changed apart from comments and the small additions the drafter already lists in `unsure.md`. One test instruction in `tests.md` needs a fix (note 6). The other notes are for information.

### How I checked

- **Bases.** I rebuilt each base from the op files myself, not from `work/`:
  - `today-study`, `today-verses`, `daily-office` and `quick-capture`: the `content` of track 7's ready writes (`t7-ready-ops.json` indexes 2, 3, 4 and 8);
  - `today-header`: D6 (a) (`t7-question-ops.json`);
  - `sanskrit-card` and `Library.base`: `other.json`.

  Copies are in `check/base` and `check/new`.
- **oldSha.** All 7 write ops match the sha256 of their base.
  - `sanskrit-card` and `Library.base` have the same byte size in the 12:23 file list (2,763 and 1,369 bytes).
  - Their last changes were on 4 Oct and 6 Oct at 22:59 UTC, both before the 04:08 `other.json`.
- **Diffs.** I read each view's full diff against its base. The diffs in `dryrun.md` and `test-output/diffs.txt` match the ops line for line. The only difference is one hunk-header count for `sanskrit-card`.
- **Simulation** (`sim.py`, p3e plus the view files) in four orders. In every one, all 10 follow-up ops applied, with 0 refused on the 9 files:
  - (a) tracks 1, 3, 4, 6 and both Augustine sets, then `t7-final-ops.json`, then these;
  - (b) track 7, then these;
  - (c) track 7, these, then tracks 4 and 6;
  - (d) (a) without track 4.

  The final text of all 9 files is the same in (a) and (c). No `find` overlaps another track's `find`.
  - **Track 6 also edits `Templates/Daily note.md`** (two replaces: `verses` → `verses_read`). The drafter did not test with track 6. Both orders work.
- **Harness.** I used my own copy of `harness8.js` with inputs rebuilt from a copy of the notes as they stood before batch 2's question items. The sweep and tests are mine:
  - the expected D2 count and list are computed in Python from the plan tables;
  - D1's expected answer comes from Python `zoneinfo`, not `Intl`;
  - the nav line's expected text is built without moment.
- **Drafter's tests reproduced** in a scratch copy: `tests.js` 28 of 28 passed, and `timing_today.js` 40 of 40.

### Each op

| # | File | Op | ★ | Verdict |
|---|---|---|---|---|
| 1 | `Templates/Views/today-study/view.js` | write | D2, plus F5 and F19 (merged pass) | D2: window `[today − 14, today − 1]`. F5: the last-week Advent 1B button and the plan-ended line (day 1,099 is the last row's number). F19: buttons read the date when pressed. The rest is unchanged. The label "in the last 14 days" is new wording (note 2). |
| 2 | `Templates/Views/today-verses/view.js` | write | F4 | `keepOpen` on the verses and the translation, keyed per day. Nothing else. |
| 3 | `Templates/Views/daily-office/view.js` | write | F4 | Open or closed is kept per date. `{open: true}` still opens it the first time. An error-opened Office is not kept. Nothing else. |
| 4 | `Templates/Views/today-header/view.js` | write | D1, D4 | D1 line text exactly as the ★. D4 guard the same as F3's. Base: D6 (a) (note 4). |
| 5 | `Templates/Views/sanskrit-card/view.js` | write | D4 | Guard. Every `dv.paragraph` and `dv.el` now draws into the guard's element. Nothing else. |
| 6 | `Templates/Views/quick-capture/view.js` | write | D6 (b), D4 | Filter, fields, subject, ticks, open parts and the last message are kept on the container. Guard. Keeping the message goes slightly beyond "form and filter" (note 3). |
| 7 | `Library/Library.base` | write | D3 (6b) | Valid YAML. The new text is the old text plus one appended view, `Scratch`. The six views and the base filter are byte-identical. |
| 8 | `Templates/Daily note.md` | replace | D3 (1) | Nav line under the H1, with full paths. No literal `[[` is added to the template. |
| 9 | `Templates/Homily (Polyphonic).md` | replace | D6 (c), as D5 | The same expression as track 7's D5 op for `Homily.md`. |
| 10 | `Templates/Homily (Polyphonic).md` | replace | D6 (c), taken name | Move wrapped in try/catch, with the *Not moved…* line under the title. |

D3 (4) "not now" and (6a) "later" are correctly not built.

### Harness results

Range: every day from 1 Oct 2026 to 15 Jan 2030 (1,203 days). Old means the bases; new means the ops. Time zone America/New_York unless stated.

### Home's Today block, study lines (`out-sweep.txt`)
- **D2:** the count and the list equal Python's on 1,203 of 1,203 days.
  - Each listed item (label and portion text) is identical to the old item for that day.
  - The old count equals Python's all-days count on 1,203 of 1,203 days, which checks the expectation itself.
- **The rest of the study lines:**
  - 1,152 days identical apart from D2;
  - 6 days (26 Nov – 1 Dec 2029) add exactly one button, `Start a homily for Advent 1B`, after the other buttons;
  - 45 days (2 Dec 2029 – 15 Jan 2030): `No portion today.` → `The study plan ended on Saturday 1 December 2029 (day 1,099); see [[Tantraloka study plan]].`;
  - 0 unexpected.
  - The link target is unique: `Texts/Tantraloka/Study plan/Tantraloka study plan.md`.

### Everything else on Home
- Home's verses and Office: 1,203 identical each. There were 0 red lines.
- **Each view in a block of its own** (run through the block renderer, not `runView`): 1,203 identical for each of six calls, all wrapped in their own element. The six calls:
  - `today-verses`, with and without `{date}`;
  - `daily-office`, with and without `{date, open}`;
  - `sanskrit-card`, with and without `{date}`.
- **Date box** at 00:05, 05:00, 07:30, 12:00, 18:45 and 23:55: 7,218 of 7,218 identical.
- **Quick capture:** 1,203 identical.

### D1 (`out-tz.txt`)
- **Los Angeles,** 4 times a day: 4,812 of 4,812 are the old box plus the line, and nothing else.
- **13 more zones,** at noon on every day (1,203 runs each). 0 wrong, and 0 other differences:
  - the line in Chicago, Panama, Phoenix, Honolulu, London, Kolkata and UTC;
  - no line in Detroit, Toronto, Indianapolis, Louisville, Nassau and Havana.
- The dry run's Pacific example (4 pm Fri 9 Oct) reproduces exactly.

### Templates (`out-templates.txt`)
- **Daily note:** on 1,203 of 1,203 days, the new note is the old note plus the nav line and a blank line right after the H1.
  - The 7 Oct 2026 line equals the t7.md example character for character.
  - Edges checked: 31 Dec → 1 Jan of 2026/27, 2028/29 and 2029/30; month ends; 29 Feb 2028; the DST days.
    - Example: `[[Journal/2026/2026-12-30|← Wed 30 Dec]] · [[Journal/Weeks/Week of 2026-12-27|this week]] · [[Journal/2027/2027-01-01|Fri 1 Jan →]] · [[Home]]`.
  - The week name is `Week of <Sunday>`, the same as the Weekly note template, Home's week button, and Templater's `Journal/Weeks` folder template.
  - A title that is not a date: unchanged.
- **Homily (Polyphonic), on 1,156 plan days:**
  - Name free: identical text and identical move target.
  - Name taken: the old version errors and leaves the note blank. The new one gives the same text plus `*Not moved to "Writing/Homilies/<name>": Destination file already exists!*` under the title.
- **Homily (Polyphonic), the suggested date** (4–17 Oct 2026 and 29 Dec 2029 – 6 Jan 2030):
  - on Sundays, that Sunday (old: the next one);
  - on weekdays, unchanged;
  - with the same date typed, the note is identical.

### Targeted tests (`out-tests.txt`): 21 of 21 passed
- **F4:** the three sections stay open after a redraw, and the translation page is embedded once. The next day they start closed. One closed by hand stays closed.
- **Daily note's Office:** open the first time; closed by hand, it stays closed; in a new block it opens again. An error-opened Office is not kept.
- **F19:**
  - Drawn 31 Dec 2026 at 23:50, pressed 1 Jan 2027 at 07:10: makes `Journal/2027/2027-01-01.md` and `Week of 2026-12-27`, and asks for a redraw.
  - Drawn Sat, pressed Sun: makes the new week's note.
  - Same day: no redraw call.
- **F5:** the button makes `Writing/Homilies/2029-12-02 Advent 1B.md`.
- **D4 forced errors:** one red line for each of the panchang, Shabbat, register and `dv.pages` cases. The old versions show nothing, and the error goes uncaught.
- **D4, a redraw while drawing** (50 runs each): shown other than once, before → after:
  - `today-header`: 50 → 0;
  - `sanskrit-card`: about 40 → 0;
  - `quick-capture`: 17 → 0.

  The merged Today block: each part once in 50 of 50.
- **D6 (b):** everything comes back after a redraw. A fresh block starts empty.
- **CSS:** `vault-panels.css` selects these parts only through `.block-language-dataviewjs:has(.vp-today)` and `.vp-card-row > img`. No rule uses a child combinator from the block. So the new wrapper elements do not change the look.

### Notes for the lead

1. **D2: the list still stops at 7.** The ★ says "Count and list only the last 14 days". The ops count all 14 days but list at most 7, as before. The ★ can be read either way: option 2 in t7.md says "List the last 14 days", which suggests up to 14. This is stated in `dryrun.md` and `unsure.md` (1), with the one-line change (`slice(-7)` → `slice(-14)`). Not counted as wrong.
2. **D2: the label.** "Not yet written **in the last 14 days**" is new wording that the ★ did not give. It is listed in `unsure.md` (2).
3. **D6 (b): the message and the open state.** Quick capture also keeps the last message and which parts are open. The lookup boxes also keep their open entries, so this is the same method. Keeping the message is a small extra (`unsure.md` 5).
4. **Op 4 depends on D6 (a)** as composed in `t7-final-ops.json`, which puts D6 (a) in place of ready op index 5. If D6 (a) is held, op 4 is refused by its oldSha (safe), and the rest still apply.
5. **The order inside Homily (Polyphonic) changed.** The move now runs before `tR += out`, so that a failed move can add its line. Templater writes the output to the file object after the script ends, and that object follows a move, so the order should not matter. This could not be run here.
   - Test 15 makes two notes. Add a check on the first one, whose name is free: it is filled and filed in `Writing/Homilies`.
6. **`tests.md` test 11 (fix before running).** The regex is written as `/^Library\/(Calendars\|Sanskrit)\//` inside a table cell. Copied from the raw file, `\|` is a literal pipe, so it matches nothing. The test would then "pass" without slowing anything. Run it outside the table as `f3.slow(/^Library\/(?:Calendars|Sanskrit)\//, 150)`.
7. **`tests.md` test 5, timing.** With `moment.now` set to yesterday, the date box's minute timer finds itself past "midnight" and calls `touch()` within about 60 s.
   - If that redraws Home after `moment.now` is restored but before the button is pressed, Home already shows today, and the test no longer shows the contrast.
   - So press the button within a few seconds of restoring the clock, and check that Home still shows yesterday first.
8. **Not established here, only in Obsidian** (the drafter lists these too):
   - that Dataview keeps the same block container across a redraw (F4 and D6 b depend on it);
   - that `index.touch()` triggers a redraw. F19's buttons open the right note either way;
   - that setting `<details>.open` from a script fires `toggle`;
   - that Obsidian creates a missing `Journal/<year>/` folder when a full-path link is clicked.
9. **D1 is decided from two moments** (now, and 182 days on). In theory, a zone with New York's offsets but different switch dates could match at both and differ for a few weeks. All 13 zones tested behave as expected.

### Files

- Under `t7-follow/check/`:
  - `base/` and `new/`: the texts compared;
  - `out-sweep.txt`, `out-tz.txt`, `out-templates.txt` and `out-tests.txt`: the results.
- Scripts, in `check/scripts/`:
  - `simcheck.py`: the apply orders;
  - `make_inputs.py`: the harness inputs and the Python expectations;
  - `csweep.js`: the sweep;
  - `ctz.js` with `ctz_check.py`: D1;
  - `ctpl.js`: the templates;
  - `ctests.js`: the targeted tests;
  - `harness.js`: a copy of `harness8.js`.

None of these touch the vault.
