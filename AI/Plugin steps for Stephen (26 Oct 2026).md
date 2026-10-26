---
type: note
created: 2026-10-26
---
# Plugin steps for Stephen (26 Oct 2026)

Four things from the corrections week's S11 that only you can do, because they live in plugin settings and workspace files, which an AI does not write. Prepared by Claude (Opus), 26 Oct 2026; each syntax was checked against the installed plugins' code (Meta Bind 1.5.1, Spaced Repetition 1.15.4).

## 1. Meta Bind button templates (D3)

On the laptop (and on each other device where the buttons should work): copy one block below, then **Settings → Meta Bind → Button templates → Add → From clipboard**; the button builder opens; press **Add**. Repeat for each block. For *Timeline*, before **Add**, use the builder's **Command → Change** and pick Day Planner's timeline command by name (its id could not be checked here).

### Review this note

```yaml
label: Review this note
id: sr-note
style: primary
tooltip: "Spaced Repetition: review the cards in this note"
action:
  type: command
  command: obsidian-spaced-repetition:srs-review-flashcards-in-note
```

### Cram this note

```yaml
label: Cram this note
id: sr-cram
style: default
tooltip: "Spaced Repetition: go through every card in this note, due or not; the schedule is not changed"
action:
  type: command
  command: obsidian-spaced-repetition:srs-cram-flashcards-in-note
```

### Review all cards

```yaml
label: Review all cards
id: sr-all
style: default
tooltip: "Spaced Repetition: review flashcards from all notes (the deck list)"
action:
  type: command
  command: obsidian-spaced-repetition:srs-review-flashcards
```

### Timeline (Day Planner)

```yaml
label: Timeline
id: dp-timeline
style: default
tooltip: "Day Planner OG: show the timeline"
action:
  type: command
  command: ""
```

Notes:
- *Cram this note* goes through every card in the note, due or not, and does not change the schedule.
- Before reviewing another note, close the open review tab: a second click only brings the open review tab forward.
- When the templates are in, tell the AI: a job then adds the line `BUTTON[sr-note, sr-cram]` under the *Card N of 108* line of the 108 card notes and under the heading of the 4 `CIS Ch. N cards` notes (backup first; inserted in place, never regenerated). Not on the Ruppel notes: *Review this note* ignores Spaced Repetition's ignore list and would turn their `word::` lines into cards.

## 2. A Study session workspace layout (D7)

**The layout (laptop only, like the other three):**

- **Main area, left tab group:** [[CIS study plan]] (reading view; it shows the current step), then [[The Cambridge Introduction to Sanskrit (Ruppel)]] (the book's index note, from which the day's chapter opens), then `Flashcards.base` (the card notes).
- **Main area, right side, split top and bottom:**
  - top: [[Sanskrit scratchpad]] (Ink), for "write, flip, compare" beside the review;
  - bottom: [[CIS - Vocabulary (Ruppel)]], with [[CIS - Reference Grammar (Ruppel)]] and [[Conjunct Consonants - Reference List (Ruppel)]] as tabs.
- **Left sidebar:** file explorer, search and bookmarks, as in the other layouts.
- **Right sidebar:** Calendar, File properties (the day's `cis` toggle), Outline and Backlinks. No Smart Connections, Smart Environment or Callout Studio panes.
- **No Spaced Repetition tab.** Start a review from a card or chapter note in the **left** group. With *Open in new tab* on, the review opens as a tab in the active group (`workspace.getLeaf(true)`), so the scratchpad on the right stays in view.

**Do not save the layout with a review tab open.** On restore, the tab is rebuilt by `TabViewManager`'s view creator. At start-up the manager's review queue is `null`, so `SRTabView.onOpen` returns at once and leaves a blank tab. Later in a session it would hold the previous review's queue instead. Every later review button then only brings that blank tab forward (`getLeavesOfType(…)[0]`) until it is closed.

**Steps for Stephen (laptop):**

1. Close the tabs you do not want, or load *Sanskrit* as a starting point.
2. Open the three notes of the left group as tabs.
3. Right-click the last tab → *Split right*. Open the scratchpad there.
4. Split it down and open the three reference notes as tabs.
5. In the right sidebar, close the Smart Connections, Smart Environment status and Callout Studio occurrences panes. Keep Calendar, File properties, Outline and Backlinks.
6. Check that no Spaced Repetition tab is open.
7. Save the layout with the ribbon's *Manage workspace layouts* button (or Ctrl+P → *Workspaces: Save layout*; both are named in the Guide) under the name **Study session**.

A saved layout also records the ribbon's hidden items (`left-ribbon.hiddenItems` in each layout). Save it with the ribbon as you want it. Vertical Tabs' group names are kept per device and may not come back with a layout (Guide).

**Steps (laptop):**

1. Close the tabs you do not want, or load *Sanskrit* as a starting point.
2. Open the three notes of the left group as tabs.
3. Right-click the last tab → *Split right*; open the scratchpad there.
4. Split it down and open the three reference notes as tabs.
5. In the right sidebar, close the Smart Connections, Smart Environment status and Callout Studio occurrences panes; keep Calendar, File properties, Outline and Backlinks.
6. Check that no Spaced Repetition tab is open (a layout saved with one comes back as a blank tab).
7. Save: the ribbon's *Manage workspace layouts* button, or Ctrl+P → *Workspaces: Save layout*, name **Study session**.

The Note Toolbar's *Layout* item can then run *Workspaces: Load workspace layout* (it opens the picker: two clicks).

## 3. Omnisearch, unsupported files (D9)

You said yes on 26 Oct, and Omnisearch and Smart Connections get a detailed review at the very end of the project (performance and stability on each device). Omnisearch is not enabled at the moment, so its setting could not be changed through the plugin. In that review, or when you turn it on: **Settings → Omnisearch → Index unsupported files → No** (it is now *Default*). That drops about 2,500 file-name-only entries (PDFs, `.txt`); a PDF is then found through its catalog note.

## 4. A separate config folder for the phone and tablet (D10)

You said yes on 26 Oct; it belongs with the end-of-project device review. What Obsidian's help says (*Sync → Settings*, "Settings profiles"): Sync can sync several configuration folders to the same remote vault, so the phone and tablet can have their own profile. The setting is **Settings → Files and links → Override config folder**: enter a name starting with a period, for example `.obsidian-mobile`, then relaunch Obsidian. Changing the profile means setting up that device's Sync settings again, and the help recommends first copying the existing `.obsidian` folder and renaming the copy to the new profile name, so that plugins and themes need not be downloaded again. Source: https://obsidian.md/help/sync/settings (read 26 Oct 2026). Things to decide in the review: which device makes the copy, and that the phone's and tablet's plugin choices (the Guide's *Plugins* section) are then made in `.obsidian-mobile`, not in `.obsidian`.
