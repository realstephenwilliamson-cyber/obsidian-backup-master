---
type: prompt
updated: 2026-10-21
---
# Monthly check-up

**Use when:** about once a month, and after any big change. Since 21 Oct 2026 the measuring needs no AI: a runner job writes the report, you read it, and an AI session is needed only for what the report marks as needing attention. It replaces the *Vault health assessment* and the *Sync and size check* (both kept in `AI/Archive/`).

**Who runs it, model, size:** step 1, you alone with the runner — no AI, no usage; step 2, you; step 3 only when the report has red items: one short AI session, Sonnet is enough (S).

**Step 1 — the report (no AI).** In Obsidian on the laptop: start the runner if it is not running (the line under *The job runner* in [[House rules for AI work]]), then copy `AI/Prompts/Scripts/Health checks/health-report.js` into `.work/queue/`. Within a minute or two the job writes `AI/Health reports/Health report <date>.md` and moves itself to `.work/queue/done/`. While it renders the dashboards it opens and closes a few tabs; leave Obsidian alone until the note appears. Nothing else is changed. The report has four parts: *Needs attention* (with exact paths and the prompt that settles each item), *Worth knowing*, *Fine*, and the *Numbers* against the previous report.

**Step 2 — read it.** Most months everything is under *Fine* and *Worth knowing*, and the month's upkeep is yours: work through the queues it lists (catalog notes in review, scans without text, files waiting in Downloads), empty `.trash` if it has grown, set the property types it names. No AI session.

**Step 3 — only for red items.** Paste the box into a new task with the vault folder connected and Obsidian open. It fixes the mechanical items you approve from the report and points at the right full prompt for the rest.

````text
Act on the latest health report of my Obsidian vault (C:\Vaults\Obsidian Vault): AI/Health reports/Health report <date>.md, written by AI/Prompts/Scripts/Health checks/health-report.js.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md
- AI/Prompts/Prompts - read me.md (the list of the full prompts)
Confirm with me that no other AI tool is working on the vault.

1. Read the report's Needs attention section. Check each item yourself (the figures are in .work/out/health-report-<date>.json; AI/Prompts/Scripts/Health checks/health-counts.js gives the deeper numbers if the report's are not enough) and sort it: mechanical and reversible (a files: link that does not resolve, an empty note, a stray file, a name), or a decision for me.
2. Show me the list with your proposed fix for each mechanical item. Fix only what I approve: through Obsidian, dry run first, backups in .work/backup-health-<date>/. For the rest, name the prompt to run (Add new files from Downloads, Map new connections, Redundancy sweep, Extend the calendar tables, Make scans searchable (OCR)) and stop there.
3. If I ask about Sync or size: look up the current Obsidian Sync plan limits on obsidian.md (storage, per-file size, version history) and cite the pages, compare them with the report's size figures, and recommend Selective sync toggles in plain steps. Do not change any Obsidian setting yourself.
4. Record the session in AI/AI log.md as the house rules describe, and clean up your scratch in .work (never .work/plan or the backups).
````

**Afterwards:** the next report shows the numbers moving. [[Vault Health & Phantom Link Manager|Vault Health]] shows unresolved links live between runs. The retired [[Vault health assessment]] keeps the long checklist, and `health-counts.js` and `health-settings.js` ([[Health check scripts]]) still measure everything it asked for.
