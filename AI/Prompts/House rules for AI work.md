---
type: prompt
updated: 2026-10-26
---
# House rules for AI work

Every prompt in this folder tells the AI to read this note and [[Vault Guide]] before doing anything. This note is written for the AI. Stephen can read it to know what to expect.

## The vault

- Location: `C:\Vaults\Obsidian Vault` on Stephen's Windows laptop.
- Stephen uses Obsidian Sync Plus: 10 GB in all, including version history. Sync keeps older versions of notes for 12 months and older versions of attachments (PDFs, images, audio) for two weeks ([Version history](https://obsidian.md/help/Obsidian+Sync/Version+history)). Assume Sync is on (rule 14). PDFs are kept off Sync on every device (decided 14 Oct 2026; the Guide's *Sync and backups* has the settings), so the remote vault holds about 0.6 GB.
- About 39,400 files and 36,800 notes (25 Oct 2026). PDFs take about 8.0 GB of the 9.0 GB.
- Layout, catalog properties, naming, links and callouts are described in [[Vault Guide]], which is the authority. Where this note and the Guide disagree, follow the Guide and tell Stephen.
- Previous AI work is recorded in the Claude project "Obsidian Assit", when that project is attached: docs `00`–`21` in `claude/vault-rescue-2026-10-04/` (doc `07` has the job runner's restart line), the audits of 14 and 19 Oct 2026 in `claude/audit-2026-10-14/` and `claude/audit-2026-10-19/`, the Fable chat's design notes in `claude/fable/`, and the records of the completion and corrections weeks in `claude/completion-2026-10/` (*State (22 Oct 2026) - read first* first).

## Rules that are never broken

1. **One AI at a time.** Before starting, ask Stephen to confirm that no other AI tool (Claudian, another Claude, a `vault_agent` window on the laptop, Gemini or ChatGPT session) is working on the vault.
2. **Back up before bulk changes.** Before you change more than a handful of notes, either ask Stephen to copy the whole vault folder, or copy every note you will change into `.work/backup-<task>-<YYYY-MM-DD>/` first, keeping the vault path.
3. **Rename, move and delete only through Obsidian.** Use Obsidian's file explorer or, in the developer console, `app.fileManager.renameFile(file, newPath)` and `app.vault.trash(file, false)`. The trash call sends files to the vault's `.trash` folder, which Stephen empties himself. Never rename, move or delete vault files with Windows Explorer, a shell or a sync tool, because only Obsidian rewrites the links.
4. **Never overwrite Obsidian's configuration.** Do not write to `.obsidian/` (`app.json`, `workspace.json`, `community-plugins.json`, plugin `data.json` files, snippets, themes). If a setting should change, tell Stephen where it is and what to change. Two exceptions: the saved layouts of the Workspaces core plugin (`.obsidian/workspaces.json`) may be made or changed through the plugin when Stephen asks for it (7 Oct 2026); and a plugin setting that Stephen names in the chat may be changed on the laptop through that plugin's own settings save (what its settings screen does), never by writing its files, and the change is recorded in the AI log (25 Oct 2026; rule 13). Nothing else in `.obsidian/`.
5. **No zip files.** Do not create or deliver archives.
6. **No made-up facts.** Every title, author, year, publisher, page count or quotation must come from the file itself (title page, copyright page, PDF metadata) or from a source you cite with its URL. If you cannot establish a value, leave it empty, set `status: review` and say why in the note. Say "I don't know" rather than guess.
7. **File names in plain ASCII.** Use `Author - Short title (year).ext`, with no diacritics and no `[ ] # ^ | : * ? " < > \ /`. Diacritics belong in the `title` property and in the text. Keep the full Windows path at 240 characters or less, counting `C:\Vaults\Obsidian Vault\` (25 characters) as well as the path inside the vault: Windows and the Git backup stop at 259, and on 26 Oct 2026 two notes at 261 and 262 stopped a Git commit (Stephen, 26 Oct 2026).
8. **The divine name.** Do not write the Tetragrammaton in anything you produce: names, headings, aliases, link labels, summaries or chat. Leave it exactly as written inside quoted source texts.
9. **Downloads need permission.** Ask Stephen before downloading any book, article or other content file from the web. If a site refuses automated access or a fetch is blocked, do not work around it; give Stephen the link to click himself. Installing software and OCR models in your own Linux workspace is fine; list what you install.
10. **Same work, two files:** list the pair for Stephen and say which copy looks better and why. Do not delete either one yourself.
11. **Don't touch Stephen's own writing** (`Projects/`, `Journal/`, his concept and hub notes) unless the task is about it. Never rewrite his prose.
12. **Tags are Stephen's.** Tags (`#tag` in text, `tags:` in frontmatter) are his own way of organizing. AIs never add, remove, rename or rely on a tag unless he asks for that in so many words; a view, template, Base or query written by an AI reads properties, never tags. Since 19 Oct 2026 no machine-made note (texts, library, catalog, calendar) carries a tag.
13. **Plugins are Stephen's.** An AI never installs, removes, updates, enables or disables a plugin and never changes a plugin setting, except a setting Stephen names in the chat (rule 4: on the laptop, through the plugin's own settings save, logged); otherwise it reports the exact setting (name, from → to, why, risk). Before a view or script relies on a plugin it checks that the plugin is loaded and degrades without it; it never assumes a plugin is on on the phone or tablet. It remembers the plugins that write on their own: no empty note in `Journal`, `Projects/Homilies`, `Study/Concepts` or `Study/Hubs` (Templater fills it; a non-dated note in `Journal` becomes a daily note), test notes only in `Notes/`, no `::` line in `Study/Sanskrit/Flashcards` or `CIS cards` unless it is a card, no edits under `## Day Planner` or to Spaced Repetition's `<!--SR:…-->` comments, no edit to a drawing that may be open. It writes no executable plugin syntax into prose notes (dataviewjs blocks, inline code beginning with a dollar sign and an equals sign, Templater commands, Meta Bind fields and buttons) except in templates and views Stephen has approved, and it reports any such syntax in material it brings in. The whole account is in [[Vault Guide#For AIs]].
14. **Sync is live on the phone and tablet.** Assume that Obsidian Sync is running on the Android devices, and that Obsidian may be open on one or both of them, the whole time you work: a change made on the laptop reaches them within seconds, and a note or a plugin's `data.json` that is open there can travel back. If a step needs Sync paused, or Obsidian closed on a device, say so and wait for Stephen to do it; never assume it has been done. (Added 20 Oct 2026.)

## How to work on the files

- **Reading:** read notes and files directly (with a shell on the computer if you have one, or by listing and copying them into your workspace). Reading never needs Obsidian.
- **New files** (a new note, a PDF copied in from Downloads) may be written from outside Obsidian; Obsidian picks them up within a second or two.
- **Editing existing notes:**
  - For one or two notes Stephen isn't editing, write the file only if it is unchanged since you read it (compare the modification time).
  - For more than that, use a script in the Obsidian console. `app.fileManager.processFrontMatter(file, fm => { ... })` changes properties, and `app.vault.process(file, text => newText)` changes text.
  - Run every script as a dry run first: it writes a report and changes nothing.
- **The Obsidian console:**
  - Stephen opens it with Ctrl+Shift+I and then the Console tab. If you have computer control of Obsidian, you can type into it; otherwise give Stephen one line to paste.
  - Chrome may ask the person to type `allow pasting` once. Stephen does that, not you.
  - Put each script in a file in `.work/` (a hidden scratch folder Obsidian does not index), then define this helper once per session:
    `window.W = async (n) => await eval(await app.vault.adapter.read('.work/' + n + '.js'))`
  - Each script is a single `(async () => { ... })()` expression that returns a one-line summary and writes details to `.work/out/`. Run it with `await W('name')`.
  - A script reads `window.DRY !== false` as "dry run"; set `window.DRY = false` only for the real run, then set it back to `true`.
- **The job runner** (October 2026): instead of pasting each script, a runner in the console works through a queue.
  - It lives in `.work/plan/phase-3-tools/runner.js`. It runs each file put in `.work/queue/` in turn (one `(async () => { ... })()` expression, as above), writes the result to `.work/out/<job>.result.txt`, and moves the job to `.work/queue/done/`.
  - Jobs run one at a time, in the alphabetical order of their file names (so number them); `window.RUNNER_STOP()` in the console stops the runner.
  - A job is a dry run unless its first line is `// APPLY`, which sets `window.DRY = false` for that job. Write job files as UTF-8 without a byte-order mark: a BOM hides the `// APPLY` line, and the apply runs as a dry run (18 Oct 2026).
  - Before telling Stephen that the runner, or anything else, is running, check that it is: queue a trivial job and read its result.
  - When Obsidian restarts, the runner stops. Stephen restarts it by pasting this line into the console:
    `window.W = async n => await eval(await app.vault.adapter.read('.work/' + n + '.js')); await W('plan/phase-3-tools/runner')`
- **Working on the laptop** (Claude Code or the Agent SDK, since 18 Oct 2026): the same rules apply. A laptop agent may write a note directly with its file tools only after copying it into `.work/backup-<task>-<YYYY-MM-DD>/`, and its AI log entry lists the notes it wrote that way. Bulk edits (more than a handful of notes), renames, moves and deletes still go through the runner or Obsidian. Obsidian keeps the old size and date of a file written from outside until it restarts, so ask Stephen to restart it after direct writes.
- **Working from the cloud through the file bridge:** copy (stage) the notes you need into your workspace, write job files and their data into `.work/` on the computer, and read the results back the same way. The bridge moves files; it does not run commands on the computer, so every change to the vault goes through a job.
- **Large files:** the file bridge writes at most 30 MB per file and 100 MB per call (25 Oct 2026). Split a larger file into 20 MB parts in `.work/` and join them in a runner job; check the joined file's size and checksum against the original's before it replaces anything, and copy the old file to the task's backup folder first (`pdfrep-apply.js` in the Devanagari re-OCR scripts does all of this). A large file that is already on the computer (in Downloads) is copied in by a runner job with Node's `fs` and registered with `app.vault.adapter.reconcileFile(path, path)`.
- **Writing through a bridge:** the cloud side's output folder can lag behind your local writes, and a file committed seconds after it was edited has gone over in its older form (it happened three times on 5–6 Oct). Write each file once, in its final form, to a new local path; wait about 15 seconds before committing (Stephen, 25 Oct 2026); then check the written size on the computer, and re-commit if it differs.
- **Obsidian's file list can lag:** files replaced from outside Obsidian (bridge writes, Node's `fs`) can keep their old size and date in `app.vault` until Obsidian restarts. Take sizes from the disk, not from Obsidian, and ask the user to restart Obsidian after a large batch.
- **When you finish:**
  - **Keep what a later session will use.** Before the clean-up, save into the vault every script, job template and data list this session built that a later session may need (a linker, a parser, a list of undecided items), with a line saying what it does: scripts in `AI/Prompts/Scripts/<topic>/`, job templates and data for open items in `.work/edits/`. A handoff never says "re-derive" for something that exists when it is written. Such a tool is removed only when it is clearly no longer needed, and the AI log says so. (Stephen, 26 Oct 2026.)
  - Clean up only your session's scratch in `.work/`: the bundles you made, the result files you wrote in `.work/out/`, and `.work/queue/done/`. Move them into the vault trash with the adapter, since `.work` is a hidden folder Obsidian doesn't index: `await app.vault.adapter.rename('.work/<folder>', '.trash/work-<task>-<YYYY-MM-DD>/<folder>')`.
  - Never move `.work/plan/` (the job runner lives there) or the `.work/backup-*` folders. The backups stay until Stephen decides they can go.
  - Any other scratch file you created inside the vault goes to `.trash` with `app.vault.trash(file, false)`.
  - Close the developer tools, and release computer control.
- **Emptying `.trash`** is Stephen's job: open the vault folder in Windows Explorer and delete what is inside `.trash`. This is the one deletion outside Obsidian that is fine, because nothing links into `.trash`.

## Verification and the report

- After any change, check:
  - unresolved links (`app.metadataCache.unresolvedLinks`), compared with before;
  - that every changed note still has valid properties;
  - that [[Home]] still renders, if you touched anything it reads (Templates/Views, Calendar, the study plan, the Flashcard Register).
- End with a short report:
  - what changed, with numbers;
  - what you checked;
  - anything left for Stephen to decide, listed in the AI log entry as well.
- After every session, add a dated entry at the top of the [[AI log]] (what changed, with counts; where the backups are; where the full record is). If you change the vault's structure or conventions, also update the part of the [[Vault Guide]] that describes it, and add a line at the top of [[Vault Guide history]] (the Guide keeps no history of its own since 23 Oct 2026).
- Keep replies plain and short. Stephen prefers precise, plain-spoken answers, and pushes back when an inference runs ahead of the evidence.
