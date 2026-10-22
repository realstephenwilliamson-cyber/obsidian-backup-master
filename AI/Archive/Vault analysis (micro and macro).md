---
type: prompt
updated: 2026-10-07
---
# Vault analysis (micro and macro)

> **Retired 21 Oct 2026**, superseded by [[Complete vault audit]]; kept in `AI/Archive/`.

**Use when:** you want a fresh, independent, in-depth look at the whole vault. It covers how the vault hangs together (macro) and where single notes, scripts or files fall short (micro). The work is split among several agents. Each takes one area and reads it closely with a fresh context. A checking pass then removes findings that don't hold up, and the lead agent merges what is left into one report.

**Before you start:**

- Close other AI tools, and let any other AI work on the vault finish first.
- In a new Cowork task, pick the model (Fable, for example) and connect the vault folder. Giving it control of Obsidian is optional; with control, it can read link data from Obsidian itself.
- Expect it to take a while and to use a good deal more than a single-agent pass. For a lighter run, add "no agents" at the end of the prompt.
- It changes nothing. Fixes come afterwards, only the ones you choose.

````text
Give me an independent, in-depth analysis of my Obsidian vault (C:\Vaults\Obsidian Vault): the whole (macro) and the parts (micro). This is read-only: neither you nor any agent changes anything in the vault. At the end, offer to save the report as a note in Notes/.

I'm opting in to multi-agent work: use a workflow if your environment has one, otherwise parallel subagents. You are the lead: you plan, brief the agents, check their work and write the report.

FIRST (lead) read, in the vault:
- AI/Prompts/House rules for AI work.md
- Welcome to the vault.md and Vault Guide.md (what the vault is meant to be, and its conventions)
- Home.md, Home (mobile).md, the four "Hub - " notes, Study/Study.md
Confirm with me that no other AI tool is working on the vault.
Then make an inventory for the agents:
- file and note counts by top folder;
- the list of catalog notes with title, author, subject, text and status;
- the scripts in Templates/Views and the Bases.
Save it in your own workspace, not in the vault.

Rules for every agent (put them in each brief):
- Read-only. No renames, moves, edits or deletions, and no writes to the vault, .obsidian or .work.
- My own writing (Projects/, Journal/ and my concept notes) is mine. Read it to understand what I am working on, but don't critique the prose unless I ask.
- Every finding has an exact path, what is wrong or missing, the evidence (a quote, a count or a page), and a proposed fix marked safe (mechanical) or decision (needs me).
- Anything not checked in the vault or in a cited source is marked unverified. No made-up works, editions, links or page numbers. Download nothing.
- Leave the divine name as the sources write it; don't add it anywhere else.

AGENTS (run in parallel; each gets the house rules, the inventory and its area):

A. Trika and the Tantrāloka. Look at Texts/Tantraloka, the KSTS volumes, Dyczkowski, Jayaratha, the secondary literature and its verse index, the study plan, and Muktabodha. Report coverage, quality, and the most important gaps for a three-year Tantrāloka study (works and editions, which are free and legal, with links).
B. Torah, Rashi, Zohar and Hasidut. Look at Texts/Torah, Tanakh, Zohar Pritzker with the Sefaria folio notes, Mei HaShiloach, Tanya, and Judaica in the Library. Report the same as A.
C. Bible and Christian sources. Look at the New Testament and lexicon, the LXX, the Fathers and Catena Aurea, the BCP 1979, the RCL, the homilies and their templates. Report the same as A, plus how well the Sunday homily workflow is supported.
D. Philosophy of technics and memory: Stiegler, Ricoeur, Fink, cybernetics and the rest of Library/Philosophy and its hub. Report the same as A.
E. Connections across traditions. Review the crosswalks, hubs, concepts and the shared scripture, Zohar and Tantrāloka references. Propose 15 concrete links, crosswalk rows or hub sections, each naming the notes involved and why. Also list places where a link exists but is wrong or misleading.
F. Workflow, dashboards and scripts. Look at Home, Home (mobile), the daily, weekly and homily templates, Tasks, every script in Templates/Views, every Base, and the calendar and study-plan tables. Report errors, fragile assumptions, silent failures, and what would make the daily, weekly and Sunday rhythm smoother. Also report the risks: single points of failure, tables that run out (the calendar ends in 2029), plugin dependencies, size and Sync.
G. Micro sample:
   - at least 120 notes, chosen at random within each top folder (say how many from each);
   - 25 catalog notes compared with their file's title and copyright pages, including any notes with text: print, which are books I have only on paper: check those against the publisher's page;
   - broken or ambiguous links, wrong or inconsistent properties, empty sections, stale instructions, and duplicates.
H. OCR quality. Pick 15 OCR'd PDFs (their catalog notes have a "Text layer (5 Oct 2026)" line), spread across subjects and scripts (English, IAST, Devanagari, Hebrew). Extract the text of 3 pages from each and rate it. List any file that should be redone, and say why.
I. Bloat assessment. What weighs on the vault without earning its place: size, note count, render time, search noise, Sync storage or upkeep. Measure and report:
   - the vault's size by kind (PDF, e-text, image, audio, Markdown) and by top folder, and the growth since the last recorded figures (the Guide's Sync section, or the last report);
   - the 30 largest files and the 30 largest notes;
   - folders of many small generated notes (word, lexicon and verse notes): how many there are, and how much they are linked, embedded or queried;
   - notes and views that embed or query a great deal, and how long Home, Home (mobile) and the Bases take to open;
   - material held twice: a PDF and its Markdown conversion, one work in two files, superseded drafts, old approval and dry-run files;
   - hidden and AI leftovers: .trash, .work, .smart-env and other plugin caches, Claude outputs, loose scripts;
   - properties, tags, templates, Bases views and scripts that nothing uses.
   For each item: its size or count, what it costs (Sync storage, speed, search noise, upkeep), what it is for, and a recommendation: keep, slim, exclude from Sync, move out of the vault, or delete (listed for me, never deleted). Size alone is not bloat: the library, the texts and my writing are what the vault is for.

CHECK (after the agents report): give every finding marked "wrong", "broken" or "gap" to a separate checking agent (one per area, or one for all), with instructions to try to disprove it against the vault or the cited source. Drop what is disproved, mark what couldn't be checked as unverified, and keep the rest.

REPORT (lead):
- A one-page summary first: the ten most valuable improvements, each with its effort (small, medium or large), safe or decision, and the agent area it came from.
- Then one section per area (A to I), with exact paths. The bloat assessment (I) is always included, even in a lighter run. Merge duplicate findings across agents.
- Last, a short list of what the agents disagreed about, and what was dropped in the checking pass and why.
Change nothing. When I say which improvements to make, follow the house rules: dry runs, backups, and Obsidian's own rename, move and trash functions, with one AI working on the vault at a time. For a big improvement, point me to the matching prompt in AI/Prompts/.
````

**Afterwards:** choose the improvements you want. Small, safe ones can be done in the same task. For a big one, start a new task with the matching prompt, such as [[Map new connections|Map new connections]] or [[Add new files from Downloads|Add new files from Downloads]].
