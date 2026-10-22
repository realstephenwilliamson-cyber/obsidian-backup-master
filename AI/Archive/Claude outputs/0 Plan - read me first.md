---
type: prompt
updated: 2026-10-06
---
# October 2026 plan - read me first

**What this is:** one plan that carries out everything still waiting:

- the fixes from the 6 Oct 2026 analysis (areas A to G);
- the repair of the Tantrāloka's root text;
- the library in Markdown;
- Dyczkowski's English in the verse notes;
- the dynamic hubs and the new connections;
- the missing texts;
- a final check, with the Guide and the Welcome note brought up to date.

It runs in eight phases, one Cowork task at a time, each with its own prompt in this folder. When the plan is finished, phase 8 moves this folder to the trash; the routine prompts in `Prompts/` stay.

| Phase | Prompt | What it does | Rough length |
|---|---|---|---|
| 1 | [[AI/Archive/Claude outputs/1 Check the analysis and urgent fixes]] | A second look at every finding; the fixes due before 1 Nov and 17 Nov | 1 session |
| 2 | [[AI/Archive/Claude outputs/2 Repair the Tantraloka root text]] | Every Mūla block checked against DCS and the KSTS edition; a real verse-page map | 1–2 sessions |
| 3 | [[AI/Archive/Claude outputs/3 Links, catalog and structure]] | Zohar links, missing links (Augustine, Tanya, Mei HaShiloach, BCP), lectionary tracks, haftarot, LXX verse ids, Bases, catalog | 2 sessions |
| 4 | [[AI/Archive/Claude outputs/4 Convert the library PDFs to Markdown]] | Every PDF as notes with page anchors, OCR fixes folded in; the PDFs stay on this computer | 4–8 sessions |
| 5 | [[AI/Archive/Claude outputs/5 Dyczkowski into the verse notes]] | His English inside each verse note, his numbering recorded | 1–2 sessions |
| 6 | [[AI/Archive/Claude outputs/6 Dynamic hubs and connections]] | Inline fields, live hub sections, the proposed connections, links inside the converted books | 1–2 sessions |
| 7 | [[AI/Archive/Claude outputs/7 New texts and gaps]] | Phaedrus, Pirkei Avot, the complete Leviathan, a list of books still wanted | 1 session |
| 8 | [[AI/Archive/Claude outputs/8 Wrap-up]] | Health check, Sync settings, the Guide and the Welcome note, retiring this folder | 1 session |

A session here means one usage window. The lengths are guesses: phase 4's pilot will show the real pace, and the task will say so.

## Before phase 1 (you, once)

1. **Get the analysis files into the vault.** They are still in the analysis task's own workspace. Open that task and paste the message below. Wait until it reports the counts before starting phase 1.
2. **Back up the vault.** Copy `C:\Vaults\Obsidian Vault` to a place outside it, such as another drive. It is about 9 GB.
3. **Templater, on every device.** Turn on Settings → Templater → *Trigger Templater on new file creation*. The switch is kept per device and doesn't sync; where it is off, Home's note buttons make blank notes. That is how the 4 Oct homily note came out empty.
4. **Optional:** the *All* view of `Library.base` has a filter `author == "Mark S. G. Dyczkowski"`, saved from the Bases toolbar on 6 Oct. Phase 1 will ask about it. To clear it yourself, open *Library.base*, choose *All* → *Filter*, and delete that line.
5. Close other AI tools, and leave Obsidian open on this computer.

The message for the analysis task:

````text
Please copy your work into my vault, then stop. Change nothing else. No other AI is working on the vault now.
1. Every file in /home/claude/work/reports/ → C:\Vaults\Obsidian Vault\Notes\Vault analysis (6 Oct 2026)\ (same names).
2. Your inventory and /home/claude/work/scratch/A to G (skip files over 5 MB and list them) → C:\Vaults\Obsidian Vault\.work\analysis-2026-10-06\ (same layout).
Copy each file once to a fresh folder under /mnt/user-data/outputs, wait 45 seconds, then commit, then list both vault folders and check every size matches. Tell me the counts, and say if any file is gone from your workspace.
````

If the files are gone, phase 1 works from [[Agent summaries|the agents' summaries]] instead. That takes it longer.

## Starting a phase (you)

1. Start a new Cowork task **in the Obsidian Assit project**. In the same project, it can read the project's docs, where each phase records its progress.
2. Connect `C:\Vaults\Obsidian Vault`. For phase 7, also connect `Downloads`.
3. Pick the model.
4. When asked, allow control of the computer (it runs scripts in Obsidian's console). Allow the downloads it lists.
5. Copy the prompt from the phase's box and paste it.
6. Stay near for the first 20 minutes, when it asks its first questions. After that it works for hours and stops only at the approval points named in its prompt.

## When it stops

- **Usage limit:** after the reset, type `Continue` in the same task.
- **Starting the phase again in a new task.** Do this when the task has grown very long, when it seems confused, or when you want to switch model. Start a new task with the same phase prompt and add `Resume: read the progress doc first.` Everything is saved as it goes, so it picks up where the last task stopped.
- **Never two at once.** Only one task may work on the vault. Before starting a new task, make sure the old one has finished or been cut off, and don't type in the old one again.

## Usage and the cloud credit

- **The credit comes first.** Your usage page says the cloud session credit "applies automatically to cloud sessions. After it's used or expires, your plan's regular usage applies." These tasks run in the cloud, so they spend the $184 credit before the plan's own usage. The credit expires at 2:59 AM EST on 5 Nov.
- **Each prompt is built to use the compute well.** It runs agents in parallel, works for hours without you, saves its progress as it goes, and checks its own work.
- **Fable has its own weekly limit.** If the main limit runs out in the middle of a phase, you can carry on with Fable: start a new task with the same prompt, add `Resume`, and pick Fable.
- **To get the most from each window:**
  - start the next phase as soon as one is done;
  - answer approval questions quickly. The task keeps working on other items while it waits, but some steps can't start without your answer.

## Between phases: what to look at (you)

- **After 1:**
  - Home on the computer and on the phone;
  - the homily button on 1 Nov (the task shows its test);
  - *Library.base → All* lists all your books.
- **After 2:**
  - *Today's verses* on a few dates;
  - the list of repaired verses.
- **After 3:**
  - a Zohar citation in the Tanya opens its folio;
  - a John verse's backlinks show Augustine;
  - a Proper's second track;
  - an LXX verse embed.
- **After 4:**
  - a converted book on the phone;
  - the *Open the PDF* button on the computer;
  - how fast searches feel.
- **After 5:** *Today's verses* shows the English on the phone.
- **After 6:** write a `question::` line in today's note and see it on the hub.
- **After 7:** the new texts.
- **After 8:**
  - set Sync on each device as the report says;
  - check the result;
  - empty `.trash`.

## Decisions already made (6 Oct 2026)

- **PDFs stay in the vault on this computer.** Sync will leave them off the phone and tablet.
  - Your condition: no lag in searches or views.
  - Phase 4 measures this before and after, and names what causes lag: Omnisearch indexing PDFs, Bases that take in whole folders, Smart Connections. Fixing those is your call, because they're settings.
  - If there is still lag after that, moving the PDFs out is reconsidered.
- **Downloads approved** (free and legal only, each listed with its size before it downloads):
  - **Sanskrit:** the KSTS Tantrāloka volumes from archive.org, and the DCS data.
  - **Jewish:** from Sefaria, Pirkei Avot, the haftarah table and reference data.
  - **Christian:** the RCL tables (citations only; the verse texts come from the vault).
  - **Philosophy:** Plato's *Phaedrus* (Perseus or Gutenberg) and Hobbes's complete *Leviathan* (Gutenberg).
- **Order:** as in the table above.
- **Retired on 6 Oct:** the one-off prompts *Convert the library PDFs to Markdown*, *Convert Dyczkowski's translation into the verse notes* and *Build the dynamic hubs*, whose content is in phases 4, 5 and 6, and the Names survey. *Vault analysis (micro and macro)* is kept.
- **Callout Studio** is installed and has replaced Callout Manager.
- **Unchanged rules:**
  - same-work pairs are listed, not deleted;
  - plugin settings are yours to change (the AI tells you what to set);
  - your writing is yours.

## Rules for every phase (the AI reads this)

1. **Read first:**
   - `Prompts/House rules for AI work.md`, `Vault Guide.md` and this note.
   - The progress doc: the project doc `claude/vault-rescue-2026-10-04/07 October plan - progress.md`. Read it with the Projects tool and update it with `project_write`.
   - The analysis files for the areas your phase names, in `Notes/Vault analysis (6 Oct 2026)/`: the A–G reports, `*-findings.json`, and from phase 2 on, `Checked findings.md`.
   - The analysis agents' scripts in `.work/analysis-2026-10-06/`. Reuse them rather than writing new ones.
   - Where the analysis says "nothing was run in Obsidian", test in Obsidian before acting.
2. **One AI on the vault.** Confirm with Stephen that no other AI tool is working on it, and that the previous task is stopped.
3. **Multi-agent work.** Stephen opts in to multi-agent orchestration for every phase.
   - Use the Workflow tool for the fan-out steps, or parallel subagents if it isn't available.
   - The usual size guideline doesn't apply. This work calls for a large scale: up to about 50 agents in one workflow, where the work divides that finely.
   - Agents read, extract, compare, draft and check in the cloud workspace and return their results. Only the lead writes to the vault.
4. **How to write to the vault:**
   - **Bulk changes:**
     - build the content in the cloud workspace;
     - commit JSON bundles of 25 MB or less to `.work/`;
     - apply them with a script run in Obsidian's console (the `W` helper; dry by default, `window.DRY = false` to apply), using `app.vault.create`, `app.vault.process` and `processFrontMatter`.
     - Renames, moves and deletions only with Obsidian's own functions, into `.trash`.
   - **Single files:** write once to a fresh local path, wait 45 seconds, commit, then check the size on disk. The bridge can send an older copy of a file that was edited seconds before.
   - Before applying, back up every note you will change in `.work/backup-phase<N>-<date>/`, as copies.
   - No zip files, and no configuration overwrites: `app.json`, `workspace.json`, `community-plugins.json`, any plugin's `data.json`. Tell Stephen the setting instead.
   - ASCII file names; diacritics in titles and text are fine.
   - The divine name appears only as the sources write it.
   - Stephen's writing (`Writing/`, `Journal/`, his concept notes): read it, but don't change it. List what would change and ask.
5. **Nothing made up.**
   - Every changed link, text or property traces to a file in the vault or a cited source. What can't be checked is listed as unverified and left alone.
   - **Downloads:**
     - only the free, legal sources named in your phase, which Stephen approved on 6 Oct 2026;
     - show them in a dry run with their sizes first;
     - don't get round a block or a rate limit: wait and retry later, or list it;
     - files over 25 MB can't go through the bridge: give Stephen the link, and file the file from `Downloads` with the steps in `Prompts/Add new files from Downloads.md`.
6. **Approval points.** Your phase lists them.
   - Ask them early and together, with before/after examples, so Stephen can answer quickly.
   - While waiting, keep working on anything that doesn't depend on the answer. Never sit idle.
7. **Checkpoints.**
   - After every batch, update the progress doc (done, counts, next step, open questions) and `.work/plan/phase-<N>-state.json`. Then a usage cut-off, a container restart or a new task loses nothing.
   - For long jobs in the cloud workspace, keep a Monitor watching the job's log. Otherwise the container may be reclaimed while it looks idle.
8. **Before calling a batch done:**
   - counts before and after;
   - no new unresolved links;
   - a random sample read against the source by a checking agent that didn't make the change;
   - Home opens without errors on the computer.
9. **End of phase:**
   - a short report to Stephen: what changed, counts, checks, what's left, and settings for him to change;
   - fix any sentence in the Vault Guide or the Welcome note that this phase made untrue, and add a History line to the Guide;
   - update the progress doc with "Phase N done";
   - clean `.work` except backups, `.work/plan/` and `.work/analysis-2026-10-06/`;
   - tell Stephen the next phase.
10. **Use the compute.** Stephen wants every usage window spent on this plan.
    - Prefer more checking to less, and run independent tracks in parallel.
    - If your phase is done and the window has room, do the next phase's read-only preparation: study files, build tables, draft. Save it in `.work/plan/phase-<N+1>-prep/` for the next task, and write nothing else to the vault.
