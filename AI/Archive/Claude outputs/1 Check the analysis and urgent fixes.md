---
type: prompt
updated: 2026-10-06
---
# 1 Check the analysis and urgent fixes

**Use when:** first, after the steps in [[AI/Archive/Claude outputs/0 Plan - read me first]] → *Before phase 1*.

**What it does:**
- gives every finding of the 6 Oct analysis a second, independent check (the step the analysis was cut off before);
- writes the merged report;
- fixes what can't wait: the homily button on 1 Nov, *Today's verses* from 17 Nov, and the five broken verses on 21–25 Nov;
- fixes the Bases, the Templater remedy, and the sentences in the Guide and the Welcome note that aren't true.

**Expect:** one session. It asks you about a few decisions early on.

````text
Phase 1 of my October 2026 plan for my Obsidian vault (C:\Vaults\Obsidian Vault): check the 6 Oct analysis, then make the urgent fixes.

FIRST read Prompts/October 2026 plan/0 Plan - read me first.md and follow its "Rules for every phase". It covers the house rules, one AI at a time, my opt-in to multi-agent workflows at large scale, how to write, nothing made up, approval points, checkpoints and using the compute. Create the progress doc if it doesn't exist.

Inputs:
- Notes/Vault analysis (6 Oct 2026)/: the A to G reports and findings JSON (about 260 findings), and Agent summaries.md;
- .work/analysis-2026-10-06/: the agents' scripts.
If the reports or the JSON are missing, say so and work from Agent summaries.md, finding each named problem in the vault again before acting on it.

PART A. The checking pass the analysis didn't finish
1. Check the findings in one workflow, batched by area, about 10 findings per agent.
   - Which findings: every one of kind wrong, broken, gap or fragile, and every proposed "safe" fix of any kind.
   - Each agent tries to disprove its findings against the vault and the cited source.
   - It returns, with evidence: holds, disproved, partly (with the corrected count) or unverified.
   - Where the analysis says nothing was run in Obsidian (Bases, Dataview, Templater, block ids: F3, F17, G1, G2, G37, G41, G48), test in Obsidian.
2. Write Notes/Vault analysis (6 Oct 2026)/Checked findings.md:
   - First, a one-page summary: the ten most valuable improvements, each with its effort, safe or decision, and area.
   - Then a table per area, one row per finding: ID, the finding in one line, the verdict, safe or decision, and the phase of the plan that acts on it (see the table in the plan note).
   - Merge duplicates: G36 = A1/A2, E12 = C1, E21 = D1/D2, F17 = G1/G2; E1 overlaps B9.
   - List what was disproved, and why.
3. Gather every "decision" finding into one list, grouped by phase, each with the choice in one line.
   - Ask me the phase 1 ones now.
   - Put the rest in the progress doc under their phase.

PART B. Urgent fixes (only findings that held)
1. Bases.
   - Library.base: its All view has a filter author == "Mark S. G. Dyczkowski", saved from the Bases toolbar at 10:14 on 6 Oct 2026. Ask me, then remove it (unless I have already).
   - Library.base and Bases/By author, By subject, Stiegler, Currently reading, Needs review and To delete filter only on file.folder.startsWith("Library"), so they also take in PDFs, TSVs and other files.
     - Limit each to the catalog notes. Test which filter gives exactly the catalog notes (about 640): for example, file.folder.startsWith("Library/Catalog"), or file.ext == "md" with a type check.
     - Make Stiegler.base include his two missing books.
     - Show the count of each view before and after.
2. Homily week (C11–C13, B21).
   - The homily button (C's report names its script):
     - on Sunday 1 Nov 2026 it must offer All Saints, not Proper 26A;
     - a dated note on a weekday feast (25 Dec; Thanksgiving, 26 Nov 2026; All Saints on a weekday) must take that feast's readings, not the coming Sunday's.
     - Fix it, then test these dates by script: 11 Oct, 1 Nov, 22 Nov, 26 Nov, 29 Nov, 24 Dec and 25 Dec 2026; 1 Nov 2027; 1 Nov 2028.
   - The "Fixed" All Saints and Thanksgiving notes hold only Year A.
     - Add Years B and C: the citations from the RCL tables (Vanderbilt's site; download approved), the verse text from the vault's Bible notes, in the same format as the other lectionary notes.
     - Make the button pick the right year.
   - Templates/Homily (Polyphonic).md: its parashah links point to Texts/Torah/<parashah>, but the Torah is filed by book (Texts/Torah/1 Genesis, ...).
     - Make every link resolve, or replace the inline queries with ones that find the parashah's note.
     - Test with three parashiyot.
3. Tantrāloka dates coming soon.
   - "Today's verses" shows no translation link on five days, the first on 17 Nov 2026 (A15).
     - Find the cause and fix it.
     - Test every day of the practice run and Year 1 by script: each verse of each day has its translation link.
   - 37.49, 37.50, 37.58, 37.62 and 37.75 hold only the last quarter of the verse (A1); they fall on 21–25 Nov.
     - Repair those five Mūla blocks now, from the DCS text or the KSTS edition (both approved).
     - Cite the source in the change list.
     - The full repair is phase 2.
4. Blank notes from Templater (F1, F2).
   - Tell me the per-device switch: Templater → "Trigger Templater on new file creation". I'm turning it on on each device.
   - The Guide's remedy ("Replace templates in the active file") doesn't fill a blank note. Test a remedy that does, and put it in the Guide.
   - The blank 4 Oct homily note is in Writing/. List it, and fill it from the template only if I say so.
5. Sentences in the Guide and the Welcome note that the analysis found untrue.
   - Already fixed on 6 Oct (check them): the KSTS sentences and the Callout Studio row.
   - Still to fix:
     - New Testament references in the Fathers "are linked": Augustine's aren't, until phase 3;
     - Leviathan listed as "Complete" in the Incomplete Sets guide (D19): it's Bennett's adaptation of Parts 1–2;
     - stale sentences about .trash (D23, F27): I emptied it on 6 Oct.
   - Fix each with one tested sentence.
6. Anything else the check marks holds, safe and small (about 20 notes or fewer, no new source needed), from any area: do it now, from one dry-run list I approve.

Approval points: the Library.base filter; the phase 1 decisions; the dry-run list for B6; filling the 4 Oct note.

At the end: the report, the progress doc, and a History line in the Guide.

If the window still has room, prepare phase 2 (read-only) and save it in .work/plan/phase-2-prep/:
- fetch the DCS Tantrāloka data and the archive.org item list for the KSTS Tantrāloka volumes into the cloud workspace;
- build the tables you can (verse id → DCS half-lines).
````

**Afterwards:** look at what [[AI/Archive/Claude outputs/0 Plan - read me first]] lists under *After 1*, then start [[AI/Archive/Claude outputs/2 Repair the Tantraloka root text]].
