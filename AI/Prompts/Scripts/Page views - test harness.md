---
type: prompt
updated: 2026-10-23
---
# Page views - test harness

How the four page views (`Templates/Views/talmud-page`, `torah-page`, `nt-page`, `tantraloka-page`; the notes [[Talmud View]], [[Torah View]], [[New Testament View]], [[Tantraloka View]]) were tested outside Obsidian, 22–23 Oct 2026, so that a later AI can change them without guessing. The scripts are in `AI/Prompts/Scripts/Page views/`.

They run in the cloud workspace with Node and `jsdom` and `js-yaml` (`npm install jsdom js-yaml`), against a copy of the vault's notes staged under `/mnt/user-data/uploads/Obsidian Vault/` (stage the notes a test needs: the page's text notes, the notes that link them, the index notes, the calendars).

| File | What it does |
|---|---|
| `obs.js` | A small stand-in for Obsidian: walks the staged copy and builds what the views use from the metadata cache — frontmatter (YAML), headings, links and embeds with their positions, block ids with their offsets, `resolvedLinks`, `getFirstLinkpathDest` — plus `app.vault` (`cachedRead`, `getMarkdownFiles`, `getAbstractFileByPath`), `processFrontMatter` (recorded, not written), Obsidian's element helpers (`createDiv`, `createEl`, `createSpan`, `empty`, `addClass`, `toggleClass`, `setAttr`) and a `dv` whose `el` renders a little Markdown. `obs(extraNotes, { current, today })` returns `{ app, dv, container, run }`; `run(code)` runs a view's `view.js` |
| `torahtest.js`, `nttest.js`, `talmudtest.js` | Run one view for a place given on the command line (`node torahtest.js "Isaiah 53:4"`, `node nttest.js "Matthew 5:3" bsb 1`, `node talmudtest.js "Chagigah 12a"`) and print what each column drew; they write the HTML to `*-out.html` |
| `tltest.js` | The same for the Tantrāloka page (`node tltest.js 1.1 both`); it has its own short list of notes instead of `obs.js` |
| `navprint.js` | Prints the list of books, chapters or āhnikas above a page |

Paths at the top of the scripts point to where the views were edited (`/home/claude/view/<view>/view.js`); change them to wherever you edit.

What the harness cannot show: CSS (the layout, the widths, the narrow-screen rules) and anything Obsidian draws itself. For those, a runner job opens the page in Obsidian and measures it — with Obsidian's window in front and focused (in the background nothing draws and timers run about once a minute), and on a tab that is already open the job should redraw that tab (`leaf.view.previewMode.rerender(true)`) rather than open a second tab on the same note, which stays blank in reading view.
