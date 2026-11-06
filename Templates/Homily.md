<%* /* Guard (13 Oct 2026, D8): a note named after its own folder is that folder's folder note, so it gets a short folder-note body (a list of the folder's notes) instead of this template. */ if (tp.file.title === tp.file.folder(false)) { tR += "---\ntype: index\n---\n# " + tp.file.title + "\n\n```dataview\nLIST FROM \"" + tp.file.folder(true) + "\" WHERE file.path != this.file.path SORT file.name ASC\n```\n"; } else { -%>
<%*
// ================================================================================================================
// HOMILY TEMPLATE — read me (for Stephen; 21 Oct 2026)
// What it makes: a homily note in Projects/Homilies, named "<date> <occasion>": its properties, the view that draws the
//   collect of the day, the readings, the psalm as the Prayer Book prints it and the earlier homilies on the same readings
//   (Templates/Views/homily-page, 5 Nov 2026), then Notes and Draft. On a Holy Day it follows the Prayer Book's rules (the history below) and may ask which readings
//   and collect to use; the answer is kept in Calendar/Holy Days - my choices. After Pentecost (Propers 4–29) it takes the
//   complementary track's first reading and psalm, which is what the parish reads (T24, 21 Oct 2026).
// When it runs: Home's "Start a homily for …" button, or a NEW, EMPTY note in Projects/Homilies. A name that begins with a
//   date in the study plan ("2026-11-08", or "2026-11-08 Proper 27A") settles the occasion; any other name asks for the
//   Sunday or feast and the date from a list. A note named with the bare date is then renamed to the occasion. Opening
//   this file does nothing.
// What you may edit: the fixed text of the note — the title line and the "Notes" and "Draft" lines (the quoted strings after
//   `out +=` near the end). What the page shows above them is the view's (Templates/Views/homily-page/view.js).
// Don't rename: the properties type, date, occasion, feast, propers, rcl_year, readings, stage, preached_at — the Homily
//   list Base, the RCL notes' Homilies lists, Home's homily button and the "Earlier homilies" table read them; stage takes
//   idea, drafting, finished or preached.
// To test an edit: make a note named with a future Sunday's date (2026-11-15) in Projects/Homilies, read it, delete it
//   through Obsidian. A typo makes Templater show an error and leave the note empty; the previous version of this file is
//   in .work/backup-homily-view-2026-11-05/Templates/ and in Sync's version history.
// ================================================================================================================
// Homily note. Applied to new notes in Projects/Homilies. A title like "2026-10-04 Proper 22A"
// picks the readings from the study plan (the feast of that day, if it has one); otherwise you choose from a list.
// It also shows the collect of the day and the psalm as the Prayer Book prints it, when the lectionary note has them.
// Changed 18 Oct 2026 (Holy Days): a date with a Holy Day of the Prayer Book (Calendar/Holy Days (BCP 1979)) takes the feast's collect and
// readings where the Prayer Book gives the feast the day, and on a Sunday where the feast may be used "when desired" (BCP p. 16; All Saints
// on the Sunday after November 1, p. 15) it asks which: the Sunday's, the feast's, or both. The answer is kept in the note "Holy Days - my
// choices" (Home and the Daily Office read it too) and in this note's properties `feast` and `propers`. A feast with an RCL note uses it;
// the others take the Prayer Book's lessons from the Holy Days table. The psalm stays the Sunday's when the feast replaces only the
// collect and lessons (p. 16 names no psalm).
const dir = "Texts/Tantraloka/Study plan/";
const split = l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim().replace(/\\\|/g, "|"));
const links = s => [...(s || "").matchAll(/\[\[([^\]|]+)/g)].map(x => x[1]);
// The plan's Lectionary cell: a feast on the day is a link in italics, the Sunday a link in bold, the coming Sunday a link after "→".
// On a Sunday, only the feasts the Prayer Book lets take precedence of a Sunday replace it (BCP pp. 15-16:
// the Principal Feasts, and the Holy Name, the Presentation and the Transfiguration). On a weekday with no feast, the coming Sunday, as before.
const feastOf = cell => ((cell || "").match(/(?<!\*)\*\[\[([^\]|]+)/) || [])[1] || null;
const SUNDAY_FEAST = /^(All-Saints|Christmas|Epiphany|Holy-Name|Presentation|Transfiguration)/;
let date = (tp.file.title.match(/^(\d{4}-\d{2}-\d{2})/) || [])[1];
let occ = null, sundayOcc = null; // sundayOcc: the plan's own Sunday, for the psalm when a feast's collect and lessons replace the Sunday's
if (date) {
  for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith(dir))) {
    const line = (await app.vault.read(f)).split("\n").find(l => l.startsWith(`| ${date} |`));
    if (line) {
      const cell = split(line)[6], ls = links(cell), feast = feastOf(cell);
      if (moment(date).day() === 0) { sundayOcc = ls[ls.length - 1]; occ = feast && SUNDAY_FEAST.test(feast) ? feast : ls[ls.length - 1]; }
      else occ = feast || ls[ls.length - 1]; // a weekday: its feast, or else the coming Sunday
      break;
    }
  }
}
// The Holy Days (18 Oct 2026)
let hd = null, feastC = null, use = "sunday", rclFeast = null, bcpFeast = false, hdKind = null;
try {
  const hs = await app.vault.adapter.read("Templates/Views/holyday/view.js");
  hd = await new Function(hs.split("// ---- CORE " + "BEGIN")[1].split("// ---- CORE " + "END")[0].replace(/^[^\n]*\n/, "") + "\nreturn HD;")().load(app);
} catch (e) { console.error("Homily: Holy Days", e); }
if (hd && date) {
  const i = hd.info(date);
  if (i.cand) {
    feastC = i.cand; use = i.use; hdKind = i.kind;
    const ls = i.cand.meta ? hd.rclLinks(i.cand.meta.rcl) : [], y = hd.rclYear(hd.DO.parseISO(date)), ok = n => !/Special/.test(n);
    rclFeast = occ && ls.includes(occ) ? occ : (ls.find(n => n.endsWith(y) && ok(n)) || ls.find(n => !/[ABC]$/.test(n) && ok(n)) || ls.find(ok) || null);
    if (i.canSwitch && !i.choice) {
      const t = i.cand.title, S = ["sunday", "The Sunday's readings and collect"], F = ["feast", `${t}: its readings and collect`], B = ["both", "Both: the Sunday's, then the feast's"];
      const pick = await tp.system.suggester(o => o[1], i.kind === "by-right" ? [F, S, B] : [S, F, B], false, `${t} falls on this Sunday. Which readings and collect?`);
      if (pick) { use = pick[0]; await hd.setChoice(date, t, use); }
    }
    if (use === "feast") { occ = rclFeast; bcpFeast = !rclFeast; }
  }
}
if (!occ && !bcpFeast) {
  const files = app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Texts/RCL/Lectionary/RCL/") && !/RCL Index/.test(f.basename))
    .sort((a, b) => a.path.localeCompare(b.path));
  const pick = await tp.system.suggester(f => `${f.parent.name}: ${f.basename.replace(/-/g, " ")}`, files, false, "Which Sunday or feast?");
  occ = pick ? pick.basename : "";
  if (!date) date = await tp.system.prompt("Date preached or planned (YYYY-MM-DD)", moment().add((7 - moment().day()) % 7, "days").format("YYYY-MM-DD"));
}
const fmOf = n => { const f = n ? app.metadataCache.getFirstLinkpathDest(n, "") : null; return f ? (app.metadataCache.getFileCache(f)?.frontmatter ?? {}) : {}; };
const occFile = occ ? app.metadataCache.getFirstLinkpathDest(occ, "") : null;
// Track 2 (21 Oct 2026, T24): after Pentecost the parish reads the complementary track (the bulletins of 23 Aug, 27 Sep and 11 Oct 2026),
// so where the lectionary note offers one (`first_reading_complementary`; Propers 4–29) the Sunday's first reading and psalm are the
// complementary ones, by the note's own headings; the second reading and gospel are the same in both tracks. A feast's readings are not
// affected. No `psalm_bcp_complementary` exists yet, so a part of a psalm shows as a link to the Prayer Book psalm until one is added.
const t2 = f => f && f.first_reading_complementary ? Object.assign({}, f, { first_reading: f.first_reading_complementary, psalm: f.psalm_complementary, psalm_bcp: f.psalm_bcp_complementary, track2: true }) : f;
const fm = t2(fmOf(occ));
const year = /^Year [ABC]$/.test(occFile?.parent?.name ?? "") ? occFile.parent.name.slice(-1) : "";
const base = year && occ.endsWith(year) ? occ.slice(0, -1) : occ;
const label = bcpFeast ? feastC.title : (base || "Homily").replace(/-/g, " ") + (year ? (/\d$/.test(base) ? year : ` (${year})`) : "");
const feastFm = use !== "sunday" && rclFeast ? fmOf(rclFeast) : null;
const feastLessons = use !== "sunday" && feastC && !rclFeast && feastC.meta ? hd.lessonsOf(feastC.meta.lessons, 0) : [];
const readings = [...["first_reading", "psalm", "second_reading", "gospel"].map(k => fm[k]), ...(use === "both" && feastFm ? ["first_reading", "psalm", "second_reading", "gospel"].map(k => feastFm[k]) : []), ...feastLessons.map(l => l.label)].filter(Boolean);
const q = s => `"${String(s).replace(/"/g, '\\"')}"`;
const lnk = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]";
let out = ["---", "type: homily", `date: ${date || ""}`, `occasion: ${bcpFeast ? q(lnk(hd.TABLE)) : occ ? q(`[[${occ}]]`) : '""'}`,
  ...(feastC && use !== "sunday" ? [`feast: ${q(feastC.title)}`, `propers: ${use}`] : []),
  `rcl_year: ${q(bcpFeast ? hd.rclYear(hd.DO.parseISO(date)) : fm.cycle ?? year)}`,
  readings.length ? "readings:\n" + readings.map(r => "  - " + q(r)).join("\n") : "readings: []",
  "stage: idea", 'preached_at: ""', "cssclasses:", "  - manuscript", "---", ""].join("\n");
out += `# ${label}${date ? " · " + moment(date).format("D MMMM YYYY") : ""}\n\n`;
// The collect, the readings, the psalm in the Prayer Book and the earlier homilies are not written into the note: the view
// Templates/Views/homily-page draws them each time the note is shown, from the properties above (5 Nov 2026, Stephen: the
// note keeps only its properties and your writing). The Holy Day and Track 2 rules that used to be here are in that view.
out += "```dataviewjs\nawait dv.view(\"Templates/Views/homily-page\")\n```\n\n";
out += "## Notes\n\n- claim:: \n- cites:: \n\n## Draft\n\n";
// a name that is already taken makes the rename throw, and the note was left blank (F29 g): keep this name, fill the note, say why
if (!/^\d{4}-\d{2}-\d{2} /.test(tp.file.title) && date) {
  try { await tp.file.rename(`${date} ${label}`); }
  catch (e) { out = out.replace("## Notes\n\n", `## Notes\n\n*Not renamed to "${date} ${label}": ${e && e.message ? e.message : e}*\n\n`); }
}
tR += out;
%>
<%* } -%>
