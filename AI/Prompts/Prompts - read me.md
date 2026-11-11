---
type: prompt
updated: 2026-11-03
---
# Prompts - read me

The build of October 2026 is finished; its one-off prompts went to the trash (3 Nov 2026). What it left undone is the *Open work* list at the top of the [[AI log]], with where its data is; the two prompts written for it, [[SDK 2 - Page labels, held and misread (Nov 2026)]] and [[SDK 3 - Footnote leftovers in Dyczkowski, Kubjika and Finn (Nov 2026)]], were meant for the Agent SDK on the laptop, but a chat session can follow their scope and method. Stephen's own to-dos are in [[Open items]], the Bible references left plain in [[Bible references to decide later]].

The routine prompts below are ready-made instructions for an AI (a Claude Cowork task, or any assistant that can reach the vault folder) to update or maintain this vault the way it was set up. Each note says when to use it, what to connect first and — since 21 Oct 2026 — who runs it, which model is enough and roughly what it costs, and has the prompt in a box. Use the box's copy button and paste the whole prompt into a new task, editing anything in `<angle brackets>`.

Every prompt begins by sending the AI to [[House rules for AI work|House rules for AI work]] and [[Vault Guide]], so the rules live in one place: one AI at a time, back up first, renames, moves and deletes only through Obsidian, no config overwrites, no zip files, nothing made up, ASCII names, and the divine name left as the sources write it. Update those two notes, not the prompts, when a rule changes.

**Sizes** are rough, from the October 2026 sessions, as a share of a week's usage on the plan Stephen had then: **S** is one short session, under an hour, about 1–3%; **M** is half a day to a day, about 5–10% (the orientation chat of 20–21 Oct, a day and a half of conversation and small jobs on Fable, had cost about 8% of the week and 12% of the Fable allowance by mid-afternoon on the 21st); **L** is a day or more with agents, 15% and up (the complete audit of 19 Oct). **Model:** *Sonnet* means a mid-tier model is enough because the work is scripted or mechanical; *Opus/Fable* means the step needs judgment (reading title pages against the catalog, deciding which of two copies is better, checking another agent's work). On the lower tier Stephen has had since 6 Nov 2026 (no Fable), keep the strongest model for the judgment steps and let the no-AI scripts do the measuring.

| Prompt | Use it for | Changes the vault? | Who runs it, model | Size |
|---|---|---|---|---|
| [[Monthly check-up\|Monthly check-up]] | The monthly look at everything: a runner job writes `AI/Health reports/Health report <date>.md`; an AI session only for what it marks red | Read-only; the follow-up fixes what you approve | You and the runner, no AI; follow-up: Sonnet | None; follow-up S |
| [[Add new files from Downloads\|Add new files from Downloads]] | Filing new PDFs, DjVu or EPUBs with catalog notes and a Markdown copy; collect them in the Downloads folder *Add to Obsidian* and file them in batches | Yes: new files and notes | AI; Sonnet for plain PDFs, Opus/Fable when the batch has scans or hard title pages | S for up to ten files, M for twenty to forty (OCR time, not tokens) |
| [[Make scans searchable (OCR)\|Make scans searchable (OCR)]] | Adding a text layer to scans and fixing gibberish text layers | Yes: replaces PDFs (originals kept in `.trash`) | AI; Sonnet, the work is scripted | S in usage, hours of OCR time |
| [[Map new connections\|Map new connections]] | Linking new scripture, Zohar, Tantrāloka and concept references; suggesting related notes | Yes: adds links after a dry run | AI; Sonnet for the linking pass ([[Reference linker]]), Opus/Fable for the related-notes suggestions | S for a month's writing, M for a quarter's |
| [[Check catalog notes against their files\|Check catalog notes against their files]] | Settling *Review* items from title pages | Yes: corrects properties after approval | AI; Sonnet | S for twenty notes |
| [[Add scholar pages\|Add scholar pages]] | A page for each scholar on the [[Scholars]] list: position, works in the library, free sources | Yes: new notes, after you see the list | AI with web search; Sonnet | S–M for ten names |
| [[Redundancy sweep\|Redundancy sweep]] | Duplicates, leftovers, misfiled or out-of-place items | Read-only, then changes you approve | AI; Opus/Fable (which copy is better is a judgment) | M |
| [[Convert an e-book to notes\|Convert an e-book to notes]] | Turning an EPUB into chapter notes | Yes: new notes | AI; Sonnet | S per book |
| [[Add a primary text to Texts\|Add a primary text to Texts]] | A whole text as one note per verse or chapter | Yes: new notes | AI; Opus/Fable for a text whose structure is new, Sonnet for one like those done | M per text |
| [[Extend the calendar tables\|Extend the calendar tables]] | Panchang and Shabbat tables past 2029, or new places | Yes: new tables | AI; Sonnet (Python scripts) | S |
| [[Second opinion on decisions\|Second opinion on decisions]] | Talking a decisions note through with another AI that has no vault access, and bringing its answers back | No | You, with any chat model (Gemini, a free tier) | S, costs nothing here |
| [[Complete vault audit\|Complete vault audit]] | One independent, thorough look at everything after a large piece of work, with a verification of what the last AI sessions claim to have done; many agents; ends in a report | Read-only; the report only | AI; Opus/Fable lead with agents | L |
| [[Audit of the work since 3 Nov 2026]] | An independent check of the AI sessions' work from 3 Nov 2026: new texts, links, the homily page, Home, subjects and Bases, the Guide and prompts, size and Git; two waves, the cheap one first | Read-only; the report only | AI; Sonnet for wave 1, Fable page readers for wave 2 | M |

**Scripts:** `AI/Prompts/Scripts/` holds the tested code the prompts point to ([[OCR scripts|OCR scripts]], [[Calendar scripts|Calendar scripts]], [[Library conversion scripts|Library conversion scripts]], the [[Reference linker|Reference linker]], the [[Health check scripts|Health check scripts]] of 14 Oct 2026 with the no-AI `health-report.js` of 21 Oct, the [[Footnote and endnote scripts|Footnote and endnote scripts]] and the [[Devanagari re-OCR scripts|Devanagari re-OCR scripts]] of 15 Oct 2026), so a new session doesn't have to reinvent it. The runner that lets a cloud session work inside Obsidian (`.work/plan/phase-3-tools/runner.js`) is described under *Runner jobs* in [[Library conversion scripts]]; the line that starts it after an Obsidian restart is in the [[House rules for AI work|house rules]] (*The job runner*).

## Maintenance mode (from 6 Nov 2026)

From 6 November 2026 Stephen is on a lower paid tier of Claude, with no Fable allowance (he said so on 7 Nov 2026), so the vault's upkeep is arranged to need as little AI as possible, in separate small pieces that can each wait for a quiet moment:

- **Monthly, no AI:** the [[Monthly check-up]]'s report (`health-report.js` through the runner). Most months that is the whole check-up; the queues it lists are yours to work through in Obsidian, and its numbers show the vault moving month by month.
- **Filing, batched:** new books and articles collect in the Downloads folder *Add to Obsidian* and are filed in one [[Add new files from Downloads]] session when there are ten or twenty, not one at a time.
- **Linking, quarterly:** one [[Map new connections]] session over the quarter's new writing; the report counts the notes that need it.
- **Decisions without the vault:** [[Second opinion on decisions]] works in any chat model with no vault access and costs nothing here.
- **Between sessions:** write what you want to raise in [[Discuss next session]] (in `Notes/`). The session reads it first, records each item's outcome in its AI log entry and clears the list.
- **Not in maintenance mode:** agents, the [[Complete vault audit]] and anything else marked L.
- **When an AI session is needed:** one prompt per session; the model the prompt's *Who runs it* line names (keep the strongest model for the judgment steps); dry run, then apply; the AI log entry at the end. The no-AI scripts do the measuring.

**Habits that make these work:**

- Close other AI tools first.
- Copy the vault folder before anything big.
- Look at the dry run before saying yes.
- Empty `.trash` only after you've checked the result: open the vault folder in Windows Explorer and delete what's inside `.trash`. That is the one deletion that's fine outside Obsidian.
- Batching saves usage: one task that files twenty books costs far less than twenty tasks that file one each.
