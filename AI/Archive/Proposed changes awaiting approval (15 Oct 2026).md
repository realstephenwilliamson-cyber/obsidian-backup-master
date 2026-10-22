---
updated: 2026-10-15
---
# Proposed changes awaiting approval (15 Oct 2026)

**Applied on 15 Oct 2026, 08:01 EDT:** Stephen approved D01 and D03.

Decisions D01 and D03 (see [[Audit decisions (15 Oct 2026)]]) asked for a diff before anything changes. Nothing below has been applied. Reply "D01 approved" or "D03 approved", or say what to change. Claude then makes exactly these changes through Obsidian, with backups, and records them in the [[AI log]].

## D01. House rules and the ten prompts

What changes: the end-of-task clean-up no longer trashes all of `.work` (that would throw away the job runner and every backup); the figures, the project-doc range and the list of AI tools are brought up to date; the runner, the file bridge and the PDFs-off Sync decision are added.

### `AI/Prompts/House rules for AI work.md`

Now:

> updated: 2026-10-05

Proposed:

> updated: 2026-10-15

Now:

> Sync is sometimes paused; ask before assuming it is on.

Proposed:

> Sync is sometimes paused; ask before assuming it is on. PDFs are kept off Sync on every device (decided 14 Oct 2026; the Guide's *Sync and backups* has the settings), so the remote vault holds about 0.6 GB.

Now:

> - About 22,400 files and 20,300 notes. PDFs take about 7.7 GB of the 8.9 GB.

Proposed:

> - About 33,800 files and 31,100 notes (14 Oct 2026). PDFs take about 8.0 GB of the 9.0 GB.

Now:

> - Previous AI work is recorded in the Claude project "Obsidian Assit" (docs `00`–`06` in `claude/vault-rescue-2026-10-04/`), when that project is attached.

Proposed:

> - Previous AI work is recorded in the Claude project "Obsidian Assit", when that project is attached: docs `00`–`21` in `claude/vault-rescue-2026-10-04/` (doc `07` has the job runner's restart line), the audit of 14 Oct 2026 in `claude/audit-2026-10-14/`, and the Fable chat's design notes in `claude/fable/`.

Now:

> (Claudian, Smart Chat agents, another Claude or ChatGPT session)

Proposed:

> (Claudian, another Claude, Gemini or ChatGPT session)

Add before the *Large files* bullet:

> - **The job runner** (October 2026): instead of pasting each script, a runner in the console works through a queue.
>   - It lives in `.work/plan/phase-3-tools/runner.js`. It runs each file put in `.work/queue/` in turn (one `(async () => { ... })()` expression, as above), writes the result to `.work/out/<job>.result.txt`, and moves the job to `.work/queue/done/`.
>   - A job is a dry run unless its first line is `// APPLY`, which sets `window.DRY = false` for that job.
>   - When Obsidian restarts, the runner stops. Stephen restarts it by pasting this line into the console:
>     `window.W = async n => await eval(await app.vault.adapter.read('.work/' + n + '.js')); await W('plan/phase-3-tools/runner')`
> - **Working from the cloud through the file bridge:** copy (stage) the notes you need into your workspace, write job files and their data into `.work/` on the computer, and read the results back the same way. The bridge moves files; it does not run commands on the computer, so every change to the vault goes through a job.

Now:

>   - Move `.work/` into the vault trash. It is a hidden folder Obsidian doesn't index, so use the adapter: `await app.vault.adapter.rename('.work', '.trash/work-<task>-<YYYY-MM-DD>')`.

Proposed:

>   - Clean up only your session's scratch in `.work/`: the bundles you made, the result files you wrote in `.work/out/`, and `.work/queue/done/`. Move them into the vault trash with the adapter, since `.work` is a hidden folder Obsidian doesn't index: `await app.vault.adapter.rename('.work/<folder>', '.trash/work-<task>-<YYYY-MM-DD>/<folder>')`.
>   - Never move `.work/plan/` (the job runner lives there) or the `.work/backup-*` folders. The backups stay until Stephen decides they can go.

### The ten prompts

In these nine prompts, the last line's

> Clean up .work at the end.

becomes

> At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).

- [[Extend the calendar tables]]
- [[Monthly check-up]]
- [[Redundancy sweep]]
- [[Vault health assessment]]
- [[Add scholar pages]]
- [[Check catalog notes against their files]]
- [[Convert an e-book to notes]]
- [[Add a primary text to Texts]]
- [[Map new connections]]

In [[Add new files from Downloads]]:

> Clean up .work as the house rules describe when you are done.

becomes

> Clean up your scratch in .work as the house rules describe when you are done (never .work/plan or the backups).

## D03. Vault wish list (your note)

Only status lines change; your highlighted lines and everything else stay as they are.

### `Notes/Vault wish list.md`

Now:

> - **Status:** discussed, waiting for a decision.
> - The daily note is the hub. It already shows the day's study portion, verses, Office and letter, so the habits are properties on it (Office, Tantrāloka portion, letter written, and so on). A Base or Habit Tracker 21 shows streaks.

Proposed:

> - **Status:** planned. Designed with Stephen on 9 Oct 2026 (Fable chat, *Planner and letters design* in the project docs); not built yet.
> - The daily note is the hub. It already shows the day's study portion, verses, Office and letter, so the habits are properties on it (Office, Tantrāloka portion, letter written, and so on). A Base (`Bases/Habits.base`) shows streaks; Habit Tracker 21 is not used.

Now:

> ## 3. Daily letter system
>
> - **Status:** discussed.

Proposed:

> ## 3. Daily letter system
>
> - **Status:** planned. Same design, 9 Oct 2026; not built yet.

Now:

> - **Status:** discussed. Dial-in is in phase 9.

Proposed:

> - **Status:** decided 9 Oct 2026 (*Plugin review* in the project docs). There was no phase 9: the October plan ended with phase 8 on 14 Oct.

Now:

> - Overlaps to settle: Day Planner and Day Planner OG; Tasks and TaskNotes; Editing Toolbar and Note Toolbar; Notebook Navigator and the core file explorer.

Proposed:

> - Overlaps: settled. Day Planner OG, TaskNotes, Editing Toolbar and Notebook Navigator are no longer installed (audit of 14 Oct 2026); Day Planner, Tasks and Note Toolbar stay. Habit Tracker 21 is not installed either.

Now:

> - Sanskrit study plan: work through the CIS (Ruppel) slowly but steadily, alongside the daily Devanagari. Stephen may add HTML files from Ruppel's online course, so the notes can link to them. **Status:** open.

Proposed:

> - Sanskrit study plan: work through the CIS (Ruppel) slowly but steadily, alongside the daily Devanagari. Stephen may add HTML files from Ruppel's online course, so the notes can link to them. **Status:** planned. Drafted with Stephen on 9 Oct 2026 (*CIS study plan (draft)* and *CIS study plan - decisions* in the project docs); the plan note is not in the vault yet.

### Open items in the wish list

No record answered these, so they are now also on the [[AI log]]'s list of what is left:
- §3, your highlighted line "Get rid of the latin letter in the bought to you by and add a colon." Claude needs to know which line you mean (Home's letter line?).
- §4, your highlighted line "Notthe in project filees the in project file". Its meaning is unclear; please say what you meant.
- §1 *Later*: bios from the free *Lesser Feasts and Fasts 2022* PDF for the 56 newer commemorations; filing the *Great Cloud of Witnesses* PDF with a catalog note.
- §2, §3 and §6: the planner, the 108 letter notes and the CIS study plan were designed on 9 Oct 2026 (the Fable chat's HANDOFF in the project lists the files to make) but are not built. They wait for your go-ahead.
- §3: the 216 card images go to `.trash` only after you have checked the 108 letter notes, once those exist.
