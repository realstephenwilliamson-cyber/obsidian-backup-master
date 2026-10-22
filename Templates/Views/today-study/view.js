// Today's study block for Home and Home (mobile): progress in the Tantrāloka plan, today's portion, Dyczkowski pages,
// parashah and lectionary, buttons for today's and this week's notes and the coming homily.
// Moved here from Home.md unchanged on 5 Oct 2026 so both homepages share it.
// Home calls it as  await dv.view("Templates/Views/today-study", { container })  (see below).
// Where it draws (F3, 7 Oct 2026): Home passes the part of the page it made for this view ({container}). Without one,
// the view makes an element of its own in the block, in place of any left by an earlier run of the block (same
// view), so a re-render that starts while that run is still reading files cannot show it twice. It is made
// before the first await, so it keeps its place.
// Also changed 7 Oct 2026: in the plan's last week the coming Sunday's
// homily button comes from today's row, and after the last plan day a line says when the plan ended (F5); the day and
// week buttons take the date when they are pressed (F19).
const VIEW = "today-study", KEY = VIEW;
const root = input && input.container ? input.container : (() => {
  const el = dv.container.createDiv({ attr: { "data-vp-view": KEY } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-vp-view") === KEY);
  if (old) old.replaceWith(el);
  return el;
})();
// An error is shown here, in red, instead of leaving this part of the page silently empty.
const fail = e => {
  console.error(VIEW, e);
  root.createDiv({ cls: "vp-view-error", text: `${VIEW} failed: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
try { // (the body is not indented, to keep the change small)
const dir = "Texts/Tantraloka/Study plan/";
// the homilies folder is wherever the note "Homilies" (its folder note) is (12 Oct 2026, restructure)
const HOMILIES = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Writing/Homilies";
// A date in the input ({ date: "2026-10-18" }) shows that day (18 Oct 2026, for testing the Holy Days); the buttons still use the real date.
const now = input && input.date ? moment(String(input.date) + " 12:00", "YYYY-MM-DD HH:mm") : moment(); const today = now.format("YYYY-MM-DD");
// The Holy Days (18 Oct 2026): the shared holyday view; without it the view works as before.
let hd = null;
try {
  const hs = await app.vault.adapter.read("Templates/Views/holyday/view.js");
  hd = await new Function(hs.split("// ---- CORE " + "BEGIN")[1].split("// ---- CORE " + "END")[0].replace(/^[^\n]*\n/, "") + "\nreturn HD;")().load(app);
} catch (e) { console.error(VIEW, "holy days", e); }
const split = l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim().replace(/\\\|/g, "|"));
const links = s => [...(s || "").matchAll(/\[\[([^\]|]+)/g)].map(x => x[1]);
const plan = [];
for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith(dir)))
  for (const l of (await app.vault.cachedRead(f)).split("\n"))
    if (/^\| \d{4}-\d{2}-\d{2} \|/.test(l)) plan.push(split(l));
plan.sort((a, b) => a[0].localeCompare(b[0]));
const dayPath = d => `Journal/${d.slice(0, 4)}/${d}.md`;
const exists = p => !!app.vault.getAbstractFileByPath(p);
const isPortion = r => r[3] && !r[3].startsWith("Catch-up");
async function openOrCreate(p) {
  let f = app.vault.getAbstractFileByPath(p);
  if (!f) {
    const folder = p.slice(0, p.lastIndexOf("/"));
    if (!app.vault.getAbstractFileByPath(folder)) await app.vault.createFolder(folder);
    // Changed 12 Oct 2026: the note is made from its folder's template (Templater's folder templates) before it opens,
    // with Templater's own "create new note from template". Notes made empty and left to Templater's "Trigger on new
    // file creation" sometimes stayed blank (7 and 12 Oct 2026).
    const tpl = app.plugins.plugins["templater-obsidian"];
    const pair = (tpl?.settings?.folder_templates || []).filter(x => x.folder && p.startsWith(x.folder + "/"))
      .sort((a, b) => b.folder.length - a.folder.length)[0];
    const tf = pair ? app.vault.getAbstractFileByPath(pair.template) : null;
    if (tpl?.templater && tf) {
      try { f = await tpl.templater.create_new_note_from_template(tf, app.vault.getAbstractFileByPath(folder), p.split("/").pop().replace(/\.md$/, ""), false); }
      catch (e) { console.error(VIEW, e); }
    }
    f = f || app.vault.getAbstractFileByPath(p);
    if (!f) { f = await app.vault.create(p, ""); new Notice("This note was made empty: its folder has no template in Templater's settings, or Templater is off."); }
  }
  await app.workspace.getLeaf(false).openFile(f);
}
const row = plan.find(r => r[0] === today);
if (row) {
  const practice = row[2].startsWith("P");
  const n = parseInt(practice ? row[2].slice(1) : row[2]);
  const ah = (row[3].match(/Tantraloka (\d\d)\./) || [])[1];
  const next = plan.find(r => r[0] > today && /begins:/.test(r[3]));
  const progress = practice ? (isPortion(row) ? `Practice day ${n} of ${plan.filter(r => r[2].startsWith("P") && isPortion(r)).length}` : "Practice run: open day")
    : `Day ${n} of 1,099 (${(n / 10.99).toFixed(1)}%)`;
  dv.paragraph(`**${progress}**${ah ? ` · Āhnika ${+ah}` : ""}${next ? ` · next: Āhnika ${+next[3].match(/Āhnika (\d+)/)[1]} on ${moment(next[0]).format("ddd D MMM")}` : ""}`, { container: root });
  dv.paragraph(isPortion(row) ? row[3] : "No new portion today: catch up or review.", { container: root });
  dv.paragraph((row[4] ? `Dyczkowski ${row[4]} · ` : "") + `Parashah: ${row[5]} · Lectionary: ${row[6]}`, { container: root });
} else {
  const next = plan.find(r => r[0] > today);
  const last = plan.length ? plan[plan.length - 1][0] : null;
  dv.paragraph(next ? `No portion today. The plan starts on ${moment(next[0]).format("dddd D MMMM")}.`
    : last && today > last ? `The study plan ended on ${moment(last).format("dddd D MMMM YYYY")} (day 1,099); see [[Tantraloka study plan]].` : "No portion today.", { container: root });
}
{ // the collect and readings in use today, when a Holy Day's are (the Sunday's are in the plan's Lectionary cell above)
  const i = hd ? hd.info(today) : null;
  if (i && i.cand && i.feastUsed) dv.paragraph(`**Collect and readings today:** ${i.cand.title}${i.kind === "optional" || i.kind === "after" ? " (in place of the Sunday's, at your choice)" : ""} ([[Holy Days (BCP 1979)|Holy Days table]])`, { container: root });
}
// buttons
const b1 = dv.el("button", exists(dayPath(today)) ? "Open today's note" : "Start today's note", { container: root });
// Home may have been drawn yesterday (F19): take the date when the button is pressed, and have Dataview redraw Home if it has changed
const refreshAll = () => { const ix = app.plugins.plugins.dataview?.index; if (typeof ix?.touch === "function") ix.touch(); };
b1.onclick = () => { const d = moment().format("YYYY-MM-DD"); if (d !== today) refreshAll(); openOrCreate(dayPath(d)); };
const sundayStart = now.clone().subtract(now.day(), "days").format("YYYY-MM-DD");
const weekPath = `Journal/Weeks/Week of ${sundayStart}.md`;
const b2 = dv.el("button", exists(weekPath) ? "This week's note" : "Start this week's note", { container: root });
b2.onclick = () => { const m = moment(); if (m.format("YYYY-MM-DD") !== today) refreshAll(); openOrCreate(`Journal/Weeks/Week of ${m.clone().subtract(m.day(), "days").format("YYYY-MM-DD")}.md`); };
// homily buttons: the coming Sunday, and before it any feast with its own readings from today on (in the plan's
// Lectionary cell a feast is in italics). On a Sunday a feast replaces the Sunday only if the Prayer Book lets it take
// precedence of a Sunday (BCP pp. 15-16: the Principal Feasts, and the Holy Name, the Presentation and the Transfiguration).
const comingSunday = now.clone().add((7 - now.day()) % 7, "days").format("YYYY-MM-DD");
const feastOf = cell => ((cell || "").match(/(?<!\*)\*\[\[([^\]|]+)/) || [])[1] || null;
const SUNDAY_FEAST = /^(All-Saints|Christmas|Epiphany|Holy-Name|Presentation|Transfiguration)/;
const occasions = [];
for (const r of plan.filter(r => r[0] >= today && r[0] <= comingSunday)) {
  const feast = feastOf(r[6]);
  if (r[0] < comingSunday) { if (feast) occasions.push([r[0], feast, true]); }
  else occasions.push([r[0], feast && SUNDAY_FEAST.test(feast) ? feast : links(r[6]).pop(), false]);
}
// in the plan's last week (26 Nov - 1 Dec 2029) the coming Sunday has no row of its own; today's row names it after "→" (F5)
if (row && comingSunday > today && !plan.some(r => r[0] === comingSunday)) occasions.push([comingSunday, links(row[6]).pop(), false]);
// The Holy Days the plan does not list (it lists only feasts with an RCL note) and the Sunday choice (18 Oct 2026). An entry is
// [date, RCL note or null, on a weekday, Holy Day or null]; a Holy Day with no RCL note takes its readings from the BCP.
const rclFor = (c, d) => {
  const ls = c.meta ? hd.rclLinks(c.meta.rcl) : [], y = hd.rclYear(hd.DO.parseISO(d)), ok = n => !/Special/.test(n);
  return ls.find(n => n.endsWith(y) && ok(n)) || ls.find(n => !/[ABC]$/.test(n) && ok(n)) || ls.find(ok) || null;
};
if (hd) for (let m = now.clone().startOf("day"); m.format("YYYY-MM-DD") <= comingSunday; m.add(1, "day")) {
  const d = m.format("YYYY-MM-DD"), i = hd.info(d), k = occasions.findIndex(o => o[0] === d);
  if (!i.cand) continue;
  if (i.kind === "weekday" && d < comingSunday) { if (k < 0) occasions.push([d, rclFor(i.cand, d), true, i.cand]); }
  else if (d === comingSunday && i.feastUsed && ["optional", "after", "by-right"].includes(i.kind) && i.use === "feast") {
    const o = [d, rclFor(i.cand, d), false, i.cand]; if (k >= 0) occasions[k] = o; else occasions.push(o);
  } else if (d === comingSunday && i.kind === "by-right" && !i.feastUsed) {
    const pr = plan.find(r => r[0] === d), o = [d, pr ? links(pr[6]).pop() : null, false]; if (k >= 0) occasions[k] = o; else occasions.push(o);
  }
}
for (const [d, occ, weekday, cand] of occasions.filter(o => o[1] || o[3])) {
  const f = occ ? app.metadataCache.getFirstLinkpathDest(occ, "") : null;
  const yr = /^Year [ABC]$/.test(f?.parent?.name ?? "") ? f.parent.name.slice(-1) : "";
  const base = yr && occ.endsWith(yr) ? occ.slice(0, -1) : occ;
  const label = occ ? base.replace(/-/g, " ") + (yr ? (/\d$/.test(base) ? yr : ` (${yr})`) : "") : cand.title;
  const hp = `${HOMILIES}/${d} ${label}.md`;
  const when = weekday ? ` (${moment(d).format("ddd D MMM")})` : "";
  const b3 = dv.el("button", exists(hp) ? `Homily: ${label}${when}` : `Start a homily for ${label}${when}`, { container: root });
  b3.onclick = () => openOrCreate(hp);
}
// The "Not yet written in the last 14 days" list (D2, 7 Oct 2026) was removed on 19 Oct 2026 at Stephen's request; a missed day is one click away in the study plan.
} catch (e) { fail(e); }
