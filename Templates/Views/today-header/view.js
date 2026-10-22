// Date header for Home: today's date, the Hebrew date, the day's Sanskrit letter, the panchang for Hickory,
// and when Shabbat or Yom Tov begins and ends in Hickory and New York.
// Changed 8 Oct 2026 (Home calendar redesign): three groups, one paragraph each and in this order, with no labels:
//   the Church year (the BCP 1979 day from the Daily Office engine, a Holy Day, today's commemoration from
//     Lesser Feasts and Fasts 2022 (by date).md, linked to A Great Cloud of Witnesses);
//   the panchang (each limb linked to Panchang - the five limbs.md, karana added) and the time in India (IST);
//   the Hebrew date, the coming Shabbat's parashah (Parashot 2026-2029 (diaspora).md), the day's daf (Daf Yomi 2026-2029.md, since 21 Oct 2026)
//   and the Shabbat and Yom Tov times.
// All times are 24-hour.
// Data: Panchang <year> (Hickory).md (column 11 = festivals) and Shabbat and Yom Tov times 2026-2029.md
// Changed 12 Oct 2026 (restructure): every note is found by its name, not its folder, so the calendar tables, the BCP and the
// Sanskrit notes can move without editing this view; links are written without folders.
// (precomputed tables, so this works offline); the Hebrew date comes from the system's Hebrew calendar.
// Changed 7 Oct 2026 (phase 3 of the October plan): a missing table or row is named instead of dropped, a table that ends
// within 60 days is announced (F5, F29), and the header keeps itself current while Home stays open (F19, end of file).
// Also changed 7 Oct 2026: a line says so when this device is not on Eastern time (D1), and an error is shown in red in
// place of the box (D4), as in the Today block (F3).
// Changed 12 Oct 2026 (restructure, Home in four parts): dv.view("Templates/Views/today-header", { compact: true }) draws one
// line for Home (date, Church day, Hebrew date, parashah, tithi, Shabbat when it is near, a link to the Calendar note); without
// the option it draws the full box, which the Calendar note shows.
// Where it draws (D4): an element of its own in the block, in place of any left by an earlier run of the block, so a
// re-render that starts while that run is still reading the tables cannot show the box twice. It is made before the first await.
const COMPACT = !!(typeof input === "object" && input && input.compact);
const VIEW = "today-header", KEY = VIEW + (COMPACT ? "-compact" : "");
const root = (() => {
  const el = dv.container.createDiv({ attr: { "data-vp-view": KEY } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-vp-view") === KEY);
  if (old) old.replaceWith(el);
  return el;
})();
// An error is shown here, in red, instead of leaving the box silently missing.
const fail = e => {
  console.error(VIEW, e);
  root.createDiv({ cls: "vp-view-error", text: `${VIEW} failed: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
try { // (the body is not indented, to keep the change small)
// A date in the input ({ date: "2026-10-18" }) shows that day, at noon, with no timers; it is how the Holy Days were tested (18 Oct 2026).
const OVERRIDE = typeof input === "object" && input && input.date ? String(input.date) : null;
const now = OVERRIDE ? moment(OVERRIDE + " 12:00", "YYYY-MM-DD HH:mm") : moment();
const byName = n => app.metadataCache.getFirstLinkpathDest(n, "");
const pathOf = n => byName(n)?.path || n + ".md";   // a missing note reads as empty and is reported below
const SHABBAT = pathOf("Shabbat and Yom Tov times 2026-2029");
const REGISTER = pathOf("Sanskrit 108 Flashcard Register");
const EPOCH = await (async () => { try { return JSON.parse(await app.vault.adapter.read("Templates/Views/paths.json")).letterCycleStart || "2026-10-03"; } catch (e) { return "2026-10-03"; } })(); // one copy in paths.json since 19 Oct 2026
const EXTEND = "[[Extend the calendar tables]]";
const LFF = pathOf("Lesser Feasts and Fasts 2022 (by date)");
const PARASHOT = pathOf("Parashot 2026-2029 (diaspora)");
const DAF = pathOf("Daf Yomi 2026-2029");   // the day's daf (21 Oct 2026): one row per day; the vault's Talmud note is linked once it exists, else Sefaria
const LIMBS = "Panchang - the five limbs";
const HOLYDAYS = pathOf("BCP - Daily Office - Holy Days");
const DO_VIEW = "Templates/Views/daily-office/view.js";
const limb = (h, w) => `[[${LIMBS}#${h}|${w || h.toLowerCase()}]]`;
const to24 = s => String(s || "").replace(/\b(\d{1,2}):(\d{2}) ?(am|pm)\b/gi, (m, h, mi, ap) => `${String((+h % 12) + (/p/i.test(ap) ? 12 : 0)).padStart(2, "0")}:${mi}`);
const west = [], east = [], mid = [], foot = [];
const cmp = {};   // the parts of the one-line header (compact mode)
const read = async p => { const f = app.vault.getAbstractFileByPath(p); return f ? await app.vault.cachedRead(f) : ""; };
const cells = l => l.split("|").slice(1, -1).map(s => s.trim());
const panchangFile = y => pathOf(`Panchang ${y} (Hickory)`);
const rowFor = async d => { const t = await read(panchangFile(d.format("YYYY"))); const l = t.split("\n").find(x => x.startsWith(`| ${d.format("YYYY-MM-DD")} |`)); return l ? cells(l) : null; };
const at = (date, hm) => moment(`${date} ${hm}`, "YYYY-MM-DD h:mm a");
const hhmm = m => m.format("HH:mm");
// The time in India (IST, UTC+5:30, no summer time), with the day when it differs from here
const istNow = () => {
  try {
    const d = new Date(), f = o => new Intl.DateTimeFormat("en-GB", Object.assign({ timeZone: "Asia/Kolkata" }, o)).format(d);
    const hm = f({ hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
    const dIN = f({ year: "numeric", month: "2-digit", day: "2-digit" }), dHere = new Intl.DateTimeFormat("en-GB", { year: "numeric", month: "2-digit", day: "2-digit" }).format(d);
    return dIN === dHere ? hm : `${f({ weekday: "short" })} ${hm}`;
  } catch (e) { return moment().utcOffset(330).format("HH:mm"); }
};

// Register the "Devanagari search" command (Ctrl+P); it opens the note Devanagari search and puts the cursor in the box
if (app.commands.addCommand && !app.commands.commands["vault-devanagari-search"]) app.commands.addCommand({
  id: "vault-devanagari-search", name: "Devanagari search", icon: "languages",
  callback: async () => {
    const f = byName("Devanagari search"); if (!f) return;
    let leaf = app.workspace.getLeavesOfType("markdown").find(l => l.view?.file?.path === f.path);
    if (!leaf) { leaf = app.workspace.getLeaf("tab"); await leaf.openFile(f); }
    app.workspace.setActiveLeaf(leaf, { focus: true });
    setTimeout(() => leaf.view.containerEl.querySelector("input.vp-deva-input")?.focus(), 600);
  }
});

// ---------- the Church year (BCP 1979) ----------
// The Daily Office view's engine (the block between its CORE markers) gives the season, the week and the Holy Days
// with their transfers; the Holy Days come from the Daily Office lectionary's Holy Days note, as in the Office block.
let DO = null, cal = null, feast = null, T = null, HDH = null;
try {
  const core = (await read(DO_VIEW)).split("// ---- CORE BEGIN")[1]?.split("// ---- CORE END")[0];
  if (!core) throw new Error(`${DO_VIEW}: CORE markers not found`);
  DO = new Function(core.replace(/^[^\n]*\n/, "") + "\nreturn DO;")();
  T = DO.parseISO(now.format("YYYY-MM-DD"));
  cal = DO.calendar(T);
  const holyText = await read(HOLYDAYS);
  if (holyText) {
    const holy = DO.parseHolyDays(holyText), y = now.year();
    feast = [...DO.observances(y - 1, holy), ...DO.observances(y, holy), ...DO.observances(y + 1, holy)].find(o => o.observed === T) || null;
  }
  // The Holy Days (18 Oct 2026): the shared holyday view gives the feast's full title and rank, what the Prayer Book does with it on a
  // Sunday, and the choice made on Home; the Calendar note's full box also lists the next Holy Days.
  let HDD = null;
  try {
    const hs = await app.vault.adapter.read("Templates/Views/holyday/view.js");
    HDH = await new Function(hs.split("// ---- CORE " + "BEGIN")[1].split("// ---- CORE " + "END")[0].replace(/^[^\n]*\n/, "") + "\nreturn HD;")().load(app);
    HDD = HDH.describe(now.format("YYYY-MM-DD"));
  } catch (e) { console.error(VIEW, "holy days", e); }
  if (HDD && HDD.info && HDD.info.sundayUsed) feast = null; // 19 Oct 2026 (decision 16c): the feast's readings were used on the Sunday it fell on; not kept again today
  const hdTitle = HDD && HDD.info.feast ? HDD.info.feast.title : null;
  const desc = DO.describe(cal), first = desc.split(" · ")[0];
  const dp = desc.split(" · ");
  cmp.church = HDD && HDD.church ? HDD.church : feast ? (hdTitle || feast.name) : dp.length >= 3 ? `${dp[1]}, ${dp[2]}` : dp.join(", ");
  cmp.holy = HDD ? HDD.holy : null;
  const day = feast ? `**${hdTitle || feast.name}**${feast.transferred ? " (transferred)" : ""} · ${cal.season} · ${cal.dayName}`
    : new RegExp(cal.season.split(" ").pop()).test(first) || /Day|Sunday|Pentecost|Holy Name|Epiphany/.test(first) ? `**${first}**${desc.slice(first.length)}` : `**${cal.season}** · ${desc}`;
  west.push(`${day} ([[BCP - The Calendar of the Church Year|calendar]])`);
  if (HDD) for (const l of HDD.lines) west.push(l);
  if (HDH && !COMPACT) {
    const up = HDH.upcoming(now.format("YYYY-MM-DD"), 21).slice(0, 3);
    if (up.length) west.push(`Holy Days coming up: ${up.map(o => `${o.title.replace(/, (Deacon|Apostle|Brother|Mother).*$/, "").replace(/ of Our Lord Jesus Christ.*$/, "")} (${HDH.fmt(o.observed)}${o.transferred ? `, transferred from ${HDH.fmt(o.nominal)}` : ""})`).join(" · ")} ([[Holy Days (BCP 1979)|table]])`);
  }
} catch (e) { console.error(VIEW, e); west.push(`Church year: could not be worked out (${e.message}).`); }

// Today's commemoration (Lesser Feasts and Fasts 2022). It gives way to a Sunday, a Principal Feast or a Holy Day
// (BCP pp. 17-18), and no fixed-date feast is kept in Holy Week, Easter Week or on Ash Wednesday (BCP p. 17).
const lffText = await read(LFF);
if (lffText) {
  const md = now.format("MM-DD");
  const comm = lffText.split("\n").filter(l => l.startsWith(`| ${md} |`)).map(l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim()));
  if (comm.length) {
    const shown = comm.map(c => {
      const trial = /\[[^\]]*\]/.test(c[1]);
      const text = c[1].replace(/[\[\]]/g, "").replace(/\s+,/g, ",").trim() + (trial ? " (trial use)" : "");
      const links = [...(c[2] || "").matchAll(/\[\[([^\]|\\]+)/g)].map(m => m[1]);
      if (!links.length) return text;
      return `[[${links[0]}|${text}]]` + links.slice(1).map(l => ` · [[${l}|${l.split("/").pop().replace(/^\d\d-\d\d /, "")}]]`).join("");
    }).join(" · or ");
    let why = null;
    if (cal) {
      const F = cal.frame;
      const principal = [F.E, F.asc, F.pent, F.trin, F.xmas, F.epiph, DO.mk(now.year(), 11, 1)].includes(T);
      if (T >= F.palm && T <= DO.add(F.E, 6)) why = T < F.E ? "not kept in Holy Week" : "not kept in Easter Week";
      else if (T === F.ashWed) why = "not kept on Ash Wednesday";
      else if (principal) why = "gives way to the Principal Feast";
      else if (feast) why = `gives way to ${feast.name}`;
      else if (cal.dow === 0) why = "gives way to the Sunday";
    }
    west.push(why ? `*${shown}* (${why}, [[BCP - The Calendar of the Church Year|BCP pp. 17–18]])` : shown);
    if (!why) cmp.comm = comm[0][1].replace(/[\[\]]/g, "").split(",")[0].trim();
  }
} else west.push(`Commemorations: ${LFF} not found.`);

// ---------- the panchang ----------
// The day's letter from the 108-day Sanskrit cycle
const n = ((now.clone().startOf("day").diff(moment(EPOCH), "days") % 108) + 108) % 108 + 1;
const regText = await read(REGISTER);
const reg = regText.split("\n").find(l => new RegExp("^\\|\\s*" + n + "\\s*\\|").test(l));
if (reg) {
  const c = reg.split(/(?<!\\)\|/).slice(1, -1).map(s => s.replace(/<[^>]+>/g, "").replace(/\*\*/g, "").trim());
  // the Devanagari is shown large; a vowel sign or other combining mark sits on a dotted circle so it can be seen on its own
  const dev = /^\p{M}/u.test(c[2]) ? "◌" + c[2] : c[2];
  east.push(`Brought to you by the letter **${c[1]}** <span class="vp-letter" style="font-size:1.8em; line-height:1">${dev}</span>`);
} else east.push(regText ? `Sanskrit letter: card ${n} is not in [[${REGISTER.slice(0, -3)}|the register]].` : `Sanskrit letter: ${REGISTER} not found.`);

// Panchang: the Hindu day runs from sunrise to sunrise; each limb links to its explanation
const today = await rowFor(now);
const sunset = today ? at(today[0], today[3]) : null;
let p = today;
if (today && now.isBefore(at(today[0], today[2]))) p = (await rowFor(now.clone().subtract(1, "day"))) || today;
if (p) {
  east.push(`**Panchang** ([[Panchang ${p[0].slice(0, 4)} (Hickory)|Hickory]]): ${p[1]} (${limb("Vāra")}) · ${to24(p[4])} (${limb("Tithi")}) · ${to24(p[5])} (${limb("Nakṣatra")})`);
  cmp.tithi = `${to24(p[4])} (${limb("Tithi")})`;
  east.push(`${to24(p[6])} (${limb("Yoga")}) · ${to24(p[7])} (${limb("Karaṇa")}) · ${p[8]} (${limb("Māsa")}) · ${p[9].replace(/ · Śaka \d+/, "")} (${limb("Saṃvat")})`);
  east.push(`Sunrise ${to24(today ? today[2] : p[2])} · sunset ${to24(today ? today[3] : p[3])} · India <span class="vp-ist">${istNow()}</span> IST`);
  if (p[10]) east.push(`**Today:** ${to24(p[10])}`);
  // the next three marked days within 15 days (festivals, Ekādaśī, Pūrṇimā, Amāvāsyā, Saṅkrānti)
  const from = moment(p[0]), soon = [];
  for (const y of [...new Set([from.format("YYYY"), from.clone().add(15, "days").format("YYYY")])]) {
    for (const l of (await read(panchangFile(y))).split("\n")) {
      if (!/^\| \d{4}-\d{2}-\d{2} \|/.test(l)) continue;
      const c = cells(l), d = moment(c[0]);
      if (c[10] && d.isAfter(from, "day") && d.diff(from, "days") <= 15) soon.push(`${c[10].replace(/ \(\d.*?\)/g, "")} (${d.format("ddd D MMM")})`);
    }
  }
  if (soon.length) east.push(`Coming up: ${soon.slice(0, 3).join(" · ")}`);
} else {
  // say which: the year's table is missing, or it has no row for today (F5, F29 b)
  const pf = panchangFile(now.format("YYYY"));
  east.push(app.vault.getAbstractFileByPath(pf) ? `Panchang: no row for ${now.format("D MMM YYYY")} in [[${pf.slice(0, -3)}|the ${now.format("YYYY")} table]].`
    : `Panchang: no table for ${now.format("YYYY")} (${pf} not found); see ${EXTEND}.`);
  east.push(`India <span class="vp-ist">${istNow()}</span> IST`);
}

// ---------- the Hebrew calendar ----------
// Hebrew date: the Jewish day begins at sunset (Hickory)
// a device whose engine lacks the Hebrew calendar gives the Gregorian date here without an error, so check first (F29 a)
const hebOK = (() => { try { return new Intl.DateTimeFormat("en-u-ca-hebrew").resolvedOptions().calendar === "hebrew"; } catch (e) { return false; } })();
const heb = d => { if (!hebOK) return ""; try { return new Intl.DateTimeFormat("en-u-ca-hebrew", { day: "numeric", month: "long", year: "numeric" }).format(d); } catch (e) { return ""; } };
const hNow = heb(now.toDate()), hNext = heb(now.clone().add(1, "day").toDate());
if (hNow) {
  cmp.heb = sunset && !now.isBefore(sunset) ? hNext : hNow;
  if (sunset && now.isBefore(sunset)) mid.push(`**${hNow}** · ${hNext.replace(/ \d+$/, "")} begins at sunset, ${hhmm(sunset)}`);
  else if (sunset) mid.push(`**${hNext}** (since sunset, ${hhmm(sunset)})`);
  else mid.push(`**${hNow}** (no sunset time for today, so this date does not turn at sunset)`);
} else mid.push("Hebrew date: not shown, because this device has no Hebrew calendar.");

// The parashah of the coming Shabbat (today's, on a Saturday until havdalah in Hickory, which the Shabbat rows give)
const parText = await read(PARASHOT);
const parRows = parText.split("\n").filter(l => /^\| \d{4}-\d{2}-\d{2} \|/.test(l)).map(l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim()));

// Shabbat and Yom Tov, Hickory and New York
const shabbatText = await read(SHABBAT);
const rows = shabbatText.split("\n").filter(l => /^\| \d{4}-\d{2}-\d{2} \|/.test(l)).map(cells);
const blocks = rows
  .map(c => ({ occ: c[2], hb: moment(c[3], "YYYY-MM-DD HH:mm"), he: moment(c[4], "YYYY-MM-DD HH:mm"), nb: moment(c[5], "YYYY-MM-DD HH:mm"), ne: moment(c[6], "YYYY-MM-DD HH:mm") }));
const t = m => m.format("HH:mm"), day = m => m.format("ddd D MMM");
const cur = blocks.find(b => (now.isSameOrAfter(b.hb) && now.isBefore(b.he)) || (now.isSameOrAfter(b.nb) && now.isBefore(b.ne)));
const next = blocks.find(b => b.hb.isAfter(now) && b.nb.isAfter(now));

if (parText) {
  const sat = now.clone().day(6), hav = cur && now.day() === 6 ? cur.he : null;   // Saturday of this week
  const target = (now.day() === 6 && hav && now.isBefore(hav)) || now.day() < 6 ? sat : sat.clone().add(7, "days");
  const r = parRows.find(c => c[0] === target.format("YYYY-MM-DD"));
  if (r) {
    const links = [...(r[2] || "").matchAll(/\[\[([^\]|\\]+)\\?\|([^\]]+)\]\]/g)];
    const tab = `[[${PARASHOT.slice(0, -3)}|diaspora]]`;
    if (/^\(holiday reading: /.test(r[1])) mid.push(`Shabbat ${target.format("D MMM")}: holiday reading (${r[1].replace(/^\(holiday reading: (.*)\)$/, "$1")}, ${tab})`);
    else if (/^\(/.test(r[1])) mid.push(`Shabbat ${target.format("D MMM")}: ${r[1].replace(/^\((.*)\)$/, "$1")} (${tab})`);
    else { cmp.par = `Parashat ${links.length ? links.map(m => `[[${m[1]}|${m[2]}]]`).join("–") : r[1]}`; mid.push(`${cmp.par} (Shabbat ${target.format("D MMM")}, ${tab})`); }
  } else mid.push(`Parashah: no row for ${target.format("D MMM YYYY")} in [[${PARASHOT.slice(0, -3)}|the table]]; see ${EXTEND}.`);
} else mid.push(`Parashah: ${PARASHOT} not found.`);

// The day's daf (Daf Yomi, 21 Oct 2026): the table's row for today; the note named in its Note column when it exists, else the Sefaria link
const dafText = await read(DAF);
const dafRows = dafText.split("\n").filter(l => /^\| \d{4}-\d{2}-\d{2} \|/.test(l)).map(l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim()));
if (dafText) {
  const dr = dafRows.find(c => c[0] === now.format("YYYY-MM-DD"));
  if (dr) {
    const tab = `[[${DAF.slice(0, -3)}|daf yomi]]`, url = (String(dr[2] || "").match(/\((https?:[^)]+)\)/) || [])[1], note = dr[3] ? byName(dr[3]) : null;
    const label = note ? `[[${note.basename}|${dr[1]}]]` : url ? `[${dr[1]}](${url})` : dr[1];
    cmp.daf = `Daf ${label}`; mid.push(`Daf Yomi: ${label} (${tab})`);
  } else mid.push(`Daf Yomi: no row for ${now.format("D MMM YYYY")} in [[${DAF.slice(0, -3)}|the table]]; see ${EXTEND}.`);
} else mid.push(`Daf Yomi: ${DAF} not found.`);

const link = `[[${SHABBAT}|times]]`;
if (cur) {
  const inH = now.isSameOrAfter(cur.hb) && now.isBefore(cur.he), inN = now.isSameOrAfter(cur.nb) && now.isBefore(cur.ne);
  mid.push(`**${cur.occ} now** (${link}): ` + [inH ? `ends ${day(cur.he)} ${t(cur.he)} in Hickory` : (now.isBefore(cur.hb) ? `begins ${t(cur.hb)} in Hickory` : `over in Hickory`), inN ? `ends ${t(cur.ne)} in New York` : (now.isBefore(cur.nb) ? `begins ${t(cur.nb)} in New York` : `over in New York`)].join(" · "));
}
if (cur) cmp.shabbat = `**${cur.occ} now**, ends ${t(now.isBefore(cur.he) ? cur.he : cur.ne)}`;
else if (next && next.hb.isSame(now, "day")) cmp.shabbat = `**${next.occ}** begins ${t(next.hb)}`;
if (next) mid.push(`**Next: ${next.occ}** (${link}) · begins ${day(next.hb)}: ${t(next.hb)} Hickory · ${t(next.nb)} New York · ends ${day(next.he)}: ${t(next.he)} · ${t(next.ne)}`);
else if (!cur) mid.push(!shabbatText ? `Shabbat times: ${SHABBAT} not found.`
  : rows.length ? `Shabbat times: [[${SHABBAT}|the table]] ended on ${moment(rows[rows.length - 1][1]).format("D MMM YYYY")}; see ${EXTEND}.`
  : `Shabbat times: no rows in [[${SHABBAT}|the table]].`);

// A table that ends within the next 60 days is announced, so it can be extended in time (F5)
const ending = [], horizon = now.clone().add(60, "days");
let pEnd = null;
for (const y of [+now.format("YYYY") + 1, +now.format("YYYY")]) {
  const ds = (await read(panchangFile(y))).match(/^\| \d{4}-\d{2}-\d{2}(?= \|)/gm);
  if (ds) { pEnd = moment(ds[ds.length - 1].slice(2)); break; }
}
if (pEnd && pEnd.isSameOrAfter(now, "day") && pEnd.isBefore(horizon, "day")) ending.push(`the panchang on ${pEnd.format("D MMM YYYY")}`);
const sEnd = rows.length ? moment(rows[rows.length - 1][1]) : null;
if (sEnd && (cur || next) && sEnd.isBefore(horizon, "day")) ending.push(`the Shabbat and Yom Tov times on ${sEnd.format("D MMM YYYY")}`);
const parEnd = parRows.length ? moment(parRows[parRows.length - 1][0]) : null;
if (parEnd && parEnd.isBefore(horizon, "day")) ending.push(`the parashot on ${parEnd.format("D MMM YYYY")}`);
const dafEnd = dafRows.length ? moment(dafRows[dafRows.length - 1][0]) : null;
if (dafEnd && dafEnd.isBefore(horizon, "day")) ending.push(`the daf yomi on ${dafEnd.format("D MMM YYYY")}`);
if (ending.length) foot.push(`**Tables ending soon:** ${ending.join(" · ")}; see ${EXTEND}.`);

// The tables are in Hickory (Eastern) time and are compared with this device's clock (D1): say so when the device's clock
// differs from New York's, now or half a year from now (a zone with other summer-time rules)
const offEastern = (() => {
  try {
    const o = { hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" };
    const ny = new Intl.DateTimeFormat("en-US", Object.assign({ timeZone: "America/New_York" }, o)), here = new Intl.DateTimeFormat("en-US", o);
    return [0, 182].some(d => { const x = now.clone().add(d, "days").toDate(); return ny.format(x) !== here.format(x); });
  } catch (e) { return false; }
})();
if (offEastern) foot.push("Times are for Hickory (Eastern); this device is on another time zone.");

// One callout; each group is its own paragraph (a blank line in the callout), lines within a group joined by <br>
const groups = [west, east, mid, foot].filter(g => g.length).map(g => g.join("<br>\n> "));
// Compact (Home): one line, and the warnings (tables ending, another time zone) on a second line
const calLink = (() => { const f = byName("Calendar"); return f ? `[[${f.basename}|full calendar]]` : ""; })();
const line = [`**${now.format("ddd D MMM")}**`, cmp.church, cmp.holy, cmp.comm, cmp.heb, cmp.par, cmp.daf, cmp.tithi, cmp.shabbat, calLink].filter(Boolean).join(" · ");
const box = COMPACT ? dv.el("div", line + (foot.length ? "<br>\n<small>" + foot.join(" ") + "</small>" : ""), { container: root, cls: "vp-today vp-today-compact" })
  : dv.el("div", `> [!today] ${now.format("dddd, D MMMM YYYY")}\n> ` + groups.join("\n>\n> "), { container: root, cls: "vp-today" });

// Keep Home current while it stays open (F19). Dataview re-renders a block only when some note changes, so a Home left
// open overnight would go on showing yesterday. Once a minute this compares the clock with the next change: at midnight
// it has Dataview re-render every open block (the Today block moves on to the new day too); at sunrise, sunset and the
// Shabbat times it redraws only this header, so verses or Office lines opened elsewhere on the page stay open.
if (!OVERRIDE) { // (a test date has no timers)
const due = [sunset, today && at(today[0], today[2]), ...(cur ? [cur.hb, cur.nb, cur.he, cur.ne] : []), ...(next ? [next.hb, next.nb] : [])]
  .filter(m => m && m.isValid() && m.isAfter(now)).map(m => m.valueOf());
const midnight = now.clone().add(1, "day").startOf("day").valueOf();
const c0 = dv.container, run = (c0.__vpHeaderRun = (c0.__vpHeaderRun || 0) + 1);
clearInterval(c0.__vpHeaderTick);
const tick = () => {
  if (c0.__vpHeaderRun !== run) return clearInterval(tick.id);   // a newer run of this header has taken over
  if (!c0.isConnected) return;                                    // Home is closed or not on screen: wait
  for (const el of box.querySelectorAll?.(".vp-ist") || []) el.textContent = istNow();   // the India clock, every minute
  const ms = Date.now();
  if (ms >= midnight) {
    clearInterval(tick.id);
    const ix = app.plugins.plugins.dataview?.index;
    if (typeof ix?.touch === "function") { ix.touch(); return; } // Dataview re-renders the open blocks about 2.5 s later
  } else if (!due.some(d => ms >= d)) return;
  clearInterval(tick.id);
  box.remove();
  dv.view("Templates/Views/today-header", input);                 // this header again (same mode), with a new timer
};
tick.id = c0.__vpHeaderTick = setInterval(tick, 60 * 1000);
dv.component?.registerInterval?.(tick.id);                         // stopped when the block is closed
}
} catch (e) { fail(e); }
