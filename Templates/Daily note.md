<%* /* Guard (13 Oct 2026, D8): a note named after its own folder is that folder's folder note, so it gets a short folder-note body (a list of the folder's notes) instead of this template. */ if (tp.file.title === tp.file.folder(false)) { tR += "---\ntype: index\n---\n# " + tp.file.title + "\n\n```dataview\nLIST FROM \"" + tp.file.folder(true) + "\" WHERE file.path != this.file.path SORT file.name ASC\n```\n"; } else { -%>
<%*
// ================================================================================================================
// DAILY NOTE TEMPLATE — read me (for Stephen; 21 Oct 2026)
// What it makes: the day's note, Journal/<year>/<YYYY-MM-DD>.md: the date line; Today (the portion, the CIS step, the
//   day's letter card); Habits (toggles); Chores (from Journal/Chores.md); Day Planner (the time blocks); Mūla (the
//   verses); Phoneme of the day; Letter practice; Daily Office; Reflection; Words; Earlier on these verses; This week.
// When it runs: Templater applies it to a NEW, EMPTY note in Journal/ — Home's "Start today's note", a day clicked in
//   the Calendar, the core "Open today's daily note" command. It never touches a note that already has text, and
//   opening this file does nothing. The text between the tags is JavaScript; Obsidian shows it as plain text.
// What you may edit: the YOUR SETTINGS block just below — times, days, labels. Chores live in Journal/Chores.md and
//   the CIS minutes on the CIS study plan note (cis_mwf, cis_tth), so they are not here. Everything after "end of your
//   settings" is the machinery: leave it unless you know what you are changing.
// Don't rename these, other things read them: the headings "## Day Planner" (Day Planner OG, capital P), "## Chores"
//   (the weekly note's list), "## Habits", "## Words" (the Vocabulary reads the word:: lines), and the property names
//   type, date, office … church, reading_min, verses_read, parashah, sunday, feasts (Habits.base, the weekly note, Home).
// To test an edit: click a day a week ahead in the Calendar sidebar on the laptop — the note is made from this template —
//   read it, then delete it through Obsidian (right-click, Delete) or keep it. A typo (a missing quote, comma or bracket)
//   makes Templater show an error and leave the note empty or half made; the previous version of this file is in
//   .work/backup-orient-2026-10-21/Templates/ and in Sync's version history (right-click this file, Open version history).
// ================================================================================================================
// ============================== YOUR SETTINGS — the lines you may edit ==========================================
// Days are numbers: 0 Sunday, 1 Monday, 2 Tuesday, 3 Wednesday, 4 Thursday, 5 Friday, 6 Saturday.
// Times are "HH:mm" in quotes (24-hour clock). Keep every comma, quote and bracket as in the lines you copy.
//
// 1. The time blocks a new note starts with, by weekday. To add one, copy a line and change its days, times and title;
//    to drop one, delete its line. Blocks must not overlap (the template puts a BREAK in each gap and END after the last).
//    Don't begin a title with "Break" or "End": those are Day Planner OG's keywords.
const TIME_BLOCKS = [
  { days: [4],                   start: "06:30", end: "07:00", title: "Morning Prayer" },
  { days: [0],                   start: "09:00", end: "12:00", title: "Church" },
  { days: [2, 4],                start: "10:00", end: "11:00", title: "Exercise" },
  { days: [5],                   start: "14:00", end: "15:00", title: "Phone calls" },   // time to confirm (Stephen)
  { days: [0, 1, 2, 3, 4, 5, 6], start: "19:00", end: "19:45", title: "Reading" },
];
// 2. Two blocks whose days come from elsewhere: the pūjā block on Pūrṇimā and Amāvāsyā (read from the panchang table)
//    and the CIS session on weekdays (its length from the CIS study plan note). Only the times are set here.
const PUJA_BLOCK = { start: "12:00", end: "12:45", title: "Pūjā" };   // length to confirm (Stephen)
const CIS_START = "15:00";
// 3. Habits: the weekdays each toggle appears on, in the order they appear in the note. Not listed here because their
//    days come from elsewhere: office, letter and reading_min (every day), tantraloka (days with a portion), cis (weekdays
//    from the CIS plan's start date). puja keeps the words "moon days": it appears on Pūrṇimā and Amāvāsyā, read from the
//    panchang table. To add a habit, add an entry such as `piano: [1, 3, 5],` and give it a label in HABIT_LABELS; to
//    track it in Journal/Habits.base, add its column there too (the Base lists its columns by name).
const HABIT_DAYS = { exercise: [2, 4], calls: [5], puja: "moon days", church: [0] };
// 4. The labels shown in the note's Habits line, and the reading target shown beside the minutes field.
const READING_TARGET = 45;
const HABIT_LABELS = { office: "Office", tantraloka: "Tantrāloka", letter: "Letter", reading_min: `Reading (minutes; target ${READING_TARGET})`,
  cis: "CIS", exercise: "Exercise", calls: "Phone calls", puja: "Pūjā", church: "Church" };
// ============================ end of your settings — nothing below needs changing ===============================
// ---- The machinery. Its history first, then the code. ----
// Daily note for the Tantrāloka study plan. Applied automatically to new notes in Journal/.
// Changed 19 Oct 2026 (from the Fable design of 9 Oct 2026, "Planner and letters design" §2–3): the note also gets
//   - habit properties, only on the days they apply: office, letter, reading_min (minutes, target 45) every day; tantraloka on
//     days with a portion; cis Mon–Fri from the CIS plan's cis_start; exercise Tue and Thu; calls Fri; church Sun; puja on
//     Pūrṇimā and Amāvāsyā (the Festival column of "Panchang <year> (Hickory)", which marks the tithi current at sunrise);
//   - the date line (today-header, compact, for this note's date) and "## Today" (the portion, then the CIS step and the
//     day's letter card from the today-items view);
//   - "## Habits" (Meta Bind toggles bound to the properties, 19 Oct 2026 evening; the File properties pane works too) and
//     "## Day Planner" (the time blocks in Day Planner OG's form, 19 Oct 2026 evening: "- [ ] HH:mm Title", a gap marked BREAK,
//     the day closed with END; the plugin in its Daily mode draws the timeline from this section; Home's undated-tasks list
//     leaves out this heading);
//   - "## Letter practice" (a place for an Ink writing section on the pen devices, and the scratchpad);
//   - "## Chores" (21 Oct 2026): the weekday's chores from Journal/Chores.md (one line per chore, "- Name — days"), written as
//     tasks dated that day, so Home's "Due today or overdue" list and the phone page show them (Stephen's wish of 21 Oct 2026).
// Everything else is as before: the verses (Mūla), the Phoneme of the day, the Daily Office, Reflection, Words, Earlier on
// these verses and This week, and the properties verses_read, parashah, sunday, feasts.
const date = tp.file.title;
const isDate = /^\d{4}-\d{2}-\d{2}$/.test(date);
const dir = "Texts/Tantraloka/Study plan/";
const split = l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim().replace(/\\\|/g, "|"));
let cells = null;
if (isDate) {
  for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith(dir))) {
    const line = (await app.vault.read(f)).split("\n").find(l => l.startsWith(`| ${date} |`));
    if (line) { cells = split(line); break; }
  }
}
const verses = [];
if (cells) {
  const m = [...cells[3].matchAll(/Tantraloka (\d\d)\.(\d\d\d)/g)];
  if (m.length) {
    const c = m[0][1];
    for (let v = +m[0][2]; v <= +m[m.length - 1][2]; v++) {
      const name = `Tantraloka ${c}.${String(v).padStart(3, "0")}`;
      if (app.metadataCache.getFirstLinkpathDest(name, "")) verses.push(name);
    }
  }
}
const targets = s => [...(s || "").matchAll(/\[\[([^\]|]+)/g)].map(x => x[1]);
const parashah = cells ? targets(cells[5]) : [];
const lect = cells ? targets(cells[6]) : [];
const sunday = lect.length ? lect[lect.length - 1] : "";
const feasts = lect.slice(0, -1);
const q = s => `"[[${s}]]"`;
const list = (k, arr) => arr.length ? `${k}:\n${arr.map(x => "  - " + q(x)).join("\n")}` : `${k}: []`;
// ---- habits and time blocks (19 Oct 2026) ----
const day = isDate ? moment(date, "YYYY-MM-DD") : moment().startOf("day");
const wd = day.day();   // 0 Sunday … 6 Saturday
let puja = false;
try {
  const pf = app.metadataCache.getFirstLinkpathDest(`Panchang ${day.format("YYYY")} (Hickory)`, "");
  if (pf) {
    const row = (await app.vault.read(pf)).split("\n").find(l => l.startsWith(`| ${day.format("YYYY-MM-DD")} |`));
    const fest = row ? (row.split("|").slice(1, -1).map(s => s.trim())[10] || "") : "";
    puja = /P[uū]r[nṇ]im[aā]|Am[aā]v[aā]sy[aā]/.test(fest.normalize("NFC"));
  }
} catch (e) { console.error("Daily note template: panchang", e); }
const cisPlan = app.metadataCache.getFirstLinkpathDest("CIS study plan", "");
const cfm = cisPlan ? (app.metadataCache.getFileCache(cisPlan)?.frontmatter || {}) : {};
const cisStart = cfm.cis_start ? moment(String(cfm.cis_start).slice(0, 10), "YYYY-MM-DD") : null;
const cisOn = !!cisPlan && wd >= 1 && wd <= 5 && !(cisStart && day.isBefore(cisStart, "day"));
const cisMin = Number([1, 3, 5].includes(wd) ? cfm.cis_mwf : cfm.cis_tth) || 15;
// The habit properties for this day, in the order they appear in the note (21 Oct 2026: the days now come from YOUR SETTINGS above)
const habits = [ ["office", "false"] ]; // the space keeps Obsidian from reading the brackets as a link
if (verses.length) habits.push(["tantraloka", "false"]);
habits.push(["letter", "false"], ["reading_min", "0"]);
if (cisOn) habits.push(["cis", "false"]);
for (const [k, days] of Object.entries(HABIT_DAYS)) if (days === "moon days" ? puja : days.includes(wd)) habits.push([k, "false"]);
const hm = (t, add) => moment(`${day.format("YYYY-MM-DD")} ${t}`, "YYYY-MM-DD HH:mm").add(add || 0, "minutes").format("HH:mm");
// The time blocks for this day: the weekday's from TIME_BLOCKS, then the pūjā block on a moon day and the CIS session on a CIS day
const blocks = TIME_BLOCKS.filter(b => b.days.includes(wd)).map(b => [b.start, b.end, b.title]);
if (puja) blocks.push([PUJA_BLOCK.start, PUJA_BLOCK.end, PUJA_BLOCK.title]);
if (cisOn) blocks.push([CIS_START, hm(CIS_START, cisMin), "CIS session"]);
// ---- chores (21 Oct 2026): Journal/Chores.md, one line per chore "- Name — days"; days: daily | weekdays | weekend | Sun, Mon, Tue, Wed, Thu, Fri, Sat (first three letters, any case) ----
const chores = [];
try {
  const cf = app.vault.getAbstractFileByPath("Journal/Chores.md");
  if (cf) {
    const DN = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
    for (const l of (await app.vault.read(cf)).split("\n")) {
      const m = l.match(/^-\s+(.+?)\s+[\u2014\u2013-]\s+(.+?)\s*$/);
      if (!m) continue;
      const spec = m[2].toLowerCase();
      const on = /\bdaily\b|\bevery day\b/.test(spec)
        || (/\bweekdays?\b/.test(spec) && wd >= 1 && wd <= 5)
        || (/\bweekends?\b/.test(spec) && (wd === 0 || wd === 6))
        || spec.split(/[,\s]+/).some(t => t.slice(0, 3) === DN[wd]);
      if (on) chores.push(m[1].trim());
    }
  }
} catch (e) { console.error("Daily note template: chores", e); }
let out = [
  "---",
  "type: daily",
  `date: ${isDate ? date : tp.date.now("YYYY-MM-DD")}`,
  ...habits.map(([k, v]) => `${k}: ${v}`),
  `tantraloka_day: "${cells ? cells[2] : ""}"`,
  list("verses_read", verses),
  list("parashah", parashah),
  `sunday: ${sunday ? q(sunday) : '""'}`,
  list("feasts", feasts),
  "cssclasses:",
  "  - manuscript",
  "---",
  ""
].join("\n");
out += `# ${isDate ? moment(date, "YYYY-MM-DD").format("dddd D MMMM YYYY") : tp.file.title}\n\n`;
// First line: yesterday, this week, tomorrow and Home (F32 (1), 7 Oct 2026). The links give full paths, so a note made from
// one of them goes into Journal/ (and gets this template there), not into the default folder for new notes.
const wl = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]"; // a wikilink, written so that this template shows no unresolved link
if (isDate) {
  const d = moment(date, "YYYY-MM-DD"), prev = d.clone().subtract(1, "day"), next = d.clone().add(1, "day");
  const dayLink = m => `Journal/${m.format("YYYY")}/${m.format("YYYY-MM-DD")}`;
  out += `${wl(dayLink(prev), "← " + prev.format("ddd D MMM"))} · ${wl(`Journal/Weeks/Week of ${d.clone().subtract(d.day(), "days").format("YYYY-MM-DD")}`, "this week")} · ${wl(dayLink(next), next.format("ddd D MMM") + " →")} · ${wl("Home")}\n\n`;
  out += "```dataviewjs\nawait dv.view(\"Templates/Views/today-header\", {compact: true, date: dv.current().file.name})\n```\n\n";
}
out += "## Today\n\n";
if (verses.length) {
  const plan = cells[2].startsWith("P") ? "[[Study plan - Practice run 2026|practice run]]" : "[[Tantraloka study plan|study plan]]";
  out += `**Tantrāloka:** ${cells[3]} · day ${cells[2]} of the ${plan}\n**Dyczkowski:** ${cells[4]}\n\n`;
} else if (cells) {
  out += "No new portion today: review.\n\n";
}
out += "```dataviewjs\nawait dv.view(\"Templates/Views/today-items\", {date: dv.current().file.name})\n```\n\n";
out += "## Habits\n\n";
out += habits.map(([k]) => `${HABIT_LABELS[k] || k} ` + (k === "reading_min" ? "`INPUT[number:reading_min]`" : "`INPUT[toggle:" + k + "]`")).join(" · ") + "\n\n";
out += "<small>The toggles are Meta Bind fields bound to this note's properties; the File properties pane (on the phone: ⋮ → File properties) shows the same values.</small>\n\n";
// Chores (21 Oct 2026): the weekday's lines from Journal/Chores.md as tasks dated this day (the Tasks plugin's form), so Home lists them
if (chores.length) out += "## Chores\n\n" + chores.map(c => `- [ ] ${c} 📅 ${day.format("YYYY-MM-DD")}`).join("\n") + "\n\n";
// Day Planner OG (Daily mode) reads "## Day Planner": start times only, a block ends where the next begins, BREAK marks a gap, END closes the day
blocks.sort((x, y) => x[0].localeCompare(y[0]));
const planner = [];
blocks.forEach(([a, b, t], i) => { planner.push(`- [ ] ${a} ${t}`); const nx = blocks[i + 1]; if (!nx) planner.push(`- [ ] ${b} END`); else if (nx[0] !== b) planner.push(`- [ ] ${b} BREAK`); });
out += "## Day Planner\n\n" + planner.join("\n") + "\n\n";
if (verses.length) {
  out += "## Mūla\n\n";
  for (const v of verses) {
    const n = v.replace(/^Tantraloka (\d\d)\.(\d\d\d)$/, (_, c, x) => `${+c}.${+x}`);
    out += `[[${v}|${n}]]\n![[${v}#^mula]]\n\n`;
  }
}
out += "## Phoneme of the day\n\n```dataviewjs\nawait dv.view(\"Templates/Views/phoneme-card\", {date: dv.current().date})\n```\n\n";
out += `## Letter practice\n\nWrite today's letter (the card in *Today* above) in an Ink writing section here (*Ink: New handwriting section*, on a pen device), on the card note under *Practice*, or on the ${wl("Sanskrit scratchpad")}.\n\n`;
out += "## Daily Office\n\n```dataviewjs\nawait dv.view(\"Templates/Views/daily-office\", {date: dv.current().file.name, open: true})\n```\n\n";
out += "## Reflection\n\n- question:: \n- connects:: \n\n";
if (verses.length) out += "## Words\n\n- word:: \n\n";
if (verses.length) {
  out += "## Earlier on these verses\n\n```dataview\nTABLE WITHOUT ID file.link AS \"Note\", tantraloka_day AS \"Day\"\nFROM \"Journal\"\nWHERE type = \"daily\" AND file.path != this.file.path AND any(map(verses_read, (v) => contains(this.verses_read, v)))\nSORT date DESC\n```\n\n";
}
if (cells) out += `## This week\n\n**Parashah:** ${cells[5]}\n**Lectionary:** ${cells[6]}\n`;
tR += out;
%>
<%* } -%>
