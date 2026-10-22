---
type: prompt
updated: 2026-10-05
---
# Extend the calendar tables

**Use when:**

- during 2029, before the tables run out (they end on 31 Dec 2029);
- or if you move, want another place, or want more festivals in the panchang's festival column.

Home's date box reads these tables. Once fewer than 60 days of a table are left, the box says so; once a table has run out, the box names it instead of leaving its line out.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder; it needs its Linux workspace to run the Python scripts.

**Who runs it, model, size:** an AI session with the Linux workspace; Sonnet, the scripts are tested ([[Calendar scripts]]). S.

````text
Extend the calendar tables in my Obsidian vault (C:\Vaults\Obsidian Vault) that Home's date box reads: the panchang for Hickory, the Shabbat and Yom Tov times for Hickory and New York, and the Daf Yomi table.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- AI/Prompts/Scripts/Calendar scripts.md (the exact method, conventions, checks and the three scripts compute.py, fest.py, gen.py used on 4 Oct 2026)
- Templates/Views/today-header/view.js (how Home reads the tables)
Confirm with me that no other AI tool is working on the vault.

1. Ask me for the new range (default: the next three calendar years after the last table) and whether the places stay Hickory, NC and New York, NY. Any other change of method needs my approval: ayanāṃśa, the Shabbat conventions (candles 18 minutes before sunset, havdalah at 8.5°), the festival rules.
2. In your Linux workspace, build a Python venv with pyswisseph (Moshier mode, no data files) and pyluach. Put compute.py, fest.py and gen.py in one folder (/tmp/cal), cd there and make an out/ folder; compute.py writes /tmp/cal/rows.pkl, which the others read from the current folder. The dates are hard-coded in several places; change all of them:
   - compute.py: start, stop (start a few days before the range, stop two days after);
   - compute.py: the new-moon list. Start it on 1 February of the year BEFORE the range's first year, so the preceding Caitra is included, and end it two months after the range;
   - gen.py: the panchang date filter (2026-10-01 … 2029-12-31);
   - gen.py: the Shabbat loop's start and end and its "a < 2026-10-01" skip;
   - gen.py: the output file name of the Shabbat table.
   Run compute.py, then fest.py, then gen.py.
3. Check before anything goes into the vault:
   - new and full moons for three months of the new range against a published source;
   - one day's tithi, nakṣatra, yoga and karaṇa ends against a published panchang;
   - New York candle lighting for three months against Hebcal;
   - the major festivals of the first new year against Drik Panchang (New York) or a comparable source.
   Cite every source with its URL, and report agreements and differences. Expect some festivals a day earlier than Indian calendars, because Hickory is a western location.
4. Write one "Calendar/Panchang <year> (Hickory).md" per year, with the same columns, structure and festival column 11 as the existing years. The header text must describe THIS computation: its date, and only the checks you made in step 3. Don't copy the 4 Oct 2026 check statements. Don't change the existing years.
5. Shabbat and Yom Tov: the date box reads one file, named in view.js (const SHABBAT). Either write a new table for the new range and update view.js to read both files, or extend the existing table, rename it through Obsidian and update const SHABBAT in view.js (Obsidian does not update names inside scripts). Either way, show me the view.js diff. Propose one and wait for my choice.
5a. The Daf Yomi table: run dafyomi.py (in AI/Prompts/Scripts/Calendar scripts.md; pure arithmetic, no data files) for the new range, check three dates against Sefaria's calendar (https://www.sefaria.org/api/calendars?year=…&month=…&day=…), write Calendar/Daf Yomi <first>-<last>.md with the same columns and header form, and point const DAF in view.js at it.
6. Check: Home renders and shows today's line; a test of the date box with a date in the new range (temporarily, in the console) shows the right row. Then update Vault Guide → Daily study ("they run to the end of …") and add a History line.

Report what was added, the checks with sources, and anything that differed. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** open Home on a date in the new range, or wait for it, and compare one day against a printed panchang you trust.
