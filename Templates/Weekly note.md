<%* /* Guard (13 Oct 2026, D8): a note named after its own folder is that folder's folder note, so it gets a short folder-note body (a list of the folder's notes) instead of this template. */ if (tp.file.title === tp.file.folder(false)) { tR += "---\ntype: index\n---\n# " + tp.file.title + "\n\n```dataview\nLIST FROM \"" + tp.file.folder(true) + "\" WHERE file.path != this.file.path SORT file.name ASC\n```\n"; } else { -%>
<%*
// ================================================================================================================
// WEEKLY NOTE TEMPLATE — read me (for Stephen; 21 Oct 2026)
// What it makes: the week's note, Journal/Weeks/Week of <Sunday>.md: the Sunday and the Shabbat; a table of the week's
//   Tantrāloka portions with a link to each day's note; Habits this week (the daily notes' habit properties, an embed of
//   Journal/Habits.base); Chores this week (the daily notes' Chores tasks, by day); Reflections this week; Threads.
// When it runs: Templater applies it to a NEW, EMPTY note in Journal/Weeks — Home's week's-note button, or a note you make
//   there named "Week of YYYY-MM-DD" (the Sunday). It reads the week's rows from the study plan tables. It never touches a
//   note that already has text, and opening this file does nothing.
// What you may edit: the wording of the headings and of the Threads line — the quoted strings after `out +=` below.
//   There are no settings here: the habit columns are in Journal/Habits.base, the chores in Journal/Chores.md.
// Don't rename: the embed must stay `Habits.base#This week` (the view's name in the Base); the Chores query looks for the
//   daily notes' "## Chores" heading; the note name "Week of <Sunday>" is what the daily notes link; the properties type,
//   week_of, parashah and sunday are the note's identity for Home and the hubs.
// To test an edit: make a note named "Week of <a future Sunday>" in Journal/Weeks (Home's button makes the current week
//   only), read it, delete it through Obsidian. A typo (a missing quote, comma or bracket) makes Templater show an error
//   and leave the note empty; the previous version of this file is in .work/backup-orient-2026-10-21/Templates/ and in Sync's version history.
// ================================================================================================================
// Weekly note, Sunday to Saturday. Applied to new notes in Journal/Weeks, named "Week of YYYY-MM-DD" (the Sunday).
// Changed 19 Oct 2026 (from the Fable design of 9 Oct 2026, "Planner and letters design" §4): a "Habits this week" section
// embeds the view "This week" of Journal/Habits.base (the daily notes' habit properties for this note's Sunday to Saturday).
// Changed 21 Oct 2026: a "Chores this week" section lists the week's chores (the daily notes' "## Chores" tasks) by day (Dataview TASK query).
const dir = "Texts/Tantraloka/Study plan/";
const split = l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim().replace(/\\\|/g, "|"));
const links = s => [...(s || "").matchAll(/\[\[([^\]|]+)/g)].map(x => x[1]);
const m0 = tp.file.title.match(/(\d{4}-\d{2}-\d{2})/);
const start = m0 ? moment(m0[1], "YYYY-MM-DD") : moment().day(0);
const days = [...Array(7)].map((_, i) => start.clone().add(i, "days").format("YYYY-MM-DD"));
const rows = {};
for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith(dir)))
  for (const l of (await app.vault.read(f)).split("\n")) { const d = l.slice(2, 12); if (days.includes(d) && l.startsWith("| ")) rows[d] = split(l); }
const sun = rows[days[0]], sat = rows[days[6]];
const sunday = sun ? links(sun[6]).pop() : "";
const parashah = sat ? links(sat[5]) : [];
const q = s => `"${s}"`;
let out = ["---", "type: weekly", `week_of: ${days[0]}`,
  parashah.length ? "parashah:\n" + parashah.map(p => `  - "[[${p}]]"`).join("\n") : "parashah: []",
  `sunday: ${sunday ? q(`[[${sunday}]]`) : '""'}`, "cssclasses:", "  - manuscript", "---", ""].join("\n");
out += `# Week of ${start.format("D MMMM YYYY")}\n\n`;
out += `**Sunday:** ${sun ? sun[6].replace(/\*\*/g, "") : "—"} · **Shabbat:** ${sat ? sat[5].replace(/\*\*/g, "") : "—"}\n\n`;
out += "## Tantrāloka this week\n\n| Day | Portion | Note |\n|---|---|---|\n";
for (const d of days) {
  const r = rows[d]; const label = moment(d).format("ddd D MMM");
  out += `| ${label} | ${r ? r[3].replace(/\|/g, "\\|") : "—"} | [[Journal/${d.slice(0, 4)}/${d}\\|note]] |\n`;
}
out += "\n## Habits this week\n\n" + "!" + "[" + "[Habits.base#This week]" + "]" + "\n\n";
out += `## Chores this week\n\n\`\`\`dataview\nTASK FROM "Journal"\nWHERE file.day >= date(${days[0]}) AND file.day <= date(${days[6]}) AND meta(section).subpath = "Chores"\nGROUP BY file.link\n\`\`\`\n\n`;
out += `## Reflections this week\n\n\`\`\`dataview\nTABLE WITHOUT ID file.link AS "Day", tantraloka_day AS "Portion"\nFROM "Journal"\nWHERE type = "daily" AND date >= date(${days[0]}) AND date <= date(${days[6]})\nSORT date ASC\n\`\`\`\n\n`;
out += "## Threads\n\n*Where the Tantrāloka, the parashah and Sunday's readings met this week.*\n\n- connects:: \n";
tR += out;
%>
<%* } -%>
