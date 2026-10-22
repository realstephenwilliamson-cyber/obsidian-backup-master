// Templates/Views/hub-fields/view.js
// Phase 6 (13 Oct 2026): installed from the dynamic-hubs proposal, with the paths of the 12 Oct restructure (Study/Concepts,
// Study/Hubs, Projects, Catalog, Texts/BCP 1979) and the texts added since (Douay-Rheims, Plato, Hobbes, Aquinas, Pirkei Avot, DCS).
// Collects the inline-field lines (question::, claim::, connects::, cites::) that belong to a hub.
// Call it from a hub note:
//   await dv.view("Templates/Views/hub-fields", {show: "questions", folders: ["Texts/Tantraloka"]})
// input:
//   show     "questions" | "claims" | "connections" | "cites" | "all"   (default "all")
//   folders  text folders that count as this hub's: a link into one of them ties a line to the hub
//   limit    rows per table (default 40)
//   hub      path of the hub note (default: the note the block is in)
(() => {
const opts = Object.assign({ show: "all", folders: [], limit: 40 }, typeof input === "undefined" ? {} : input);
const hub = opts.hub ? dv.page(opts.hub) : dv.current();
if (!hub) { dv.paragraph("hub-fields: no hub note found."); return; }

const arr = x => x == null ? [] : (typeof x === "string" || typeof x[Symbol.iterator] !== "function") ? [x] : Array.from(x);
const pageOf = l => l == null ? undefined : dv.page(typeof l === "string" ? l : l.path);
const folders = arr(opts.folders).map(f => String(f).replace(/\/+$/, "") + "/");

// 1. The hub's own notes: the hub itself, every note the hub links, and every concept whose up: names the hub.
const own = new Set([hub.file.path]);
for (const l of arr(hub.file.outlinks)) { const p = pageOf(l); if (p) own.add(p.file.path); }
for (const c of dv.pages('"Study/Concepts"')) {
  if (arr(c.up).some(u => pageOf(u)?.file.path === hub.file.path)) own.add(c.file.path);
}
const belongs = l => {
  const p = pageOf(l);
  return !!p && (own.has(p.file.path) || folders.some(f => p.file.path.startsWith(f)));
};

// 2. Field lines in your own notes only (never Texts/ or Library/). A line is tied to the hub by its links;
//    a line with no link counts for the note it sits in and, in a daily note, for the day's verses.
const FIELDS = ["question", "claim", "connects", "cites"];
const filled = v => v != null && String(v).trim() !== "";
const isDate = v => !!v && typeof v.toMillis === "function";
const rows = [];
for (const p of dv.pages('"Journal" or "Notes" or "Projects" or "Study"')) {
  if (p.file.path.startsWith("Projects/_Originals/")) continue;
  for (const L of arr(p.file.lists)) {
    if (L.task) continue; // a task (- [ ] question::) is not a field line
    const field = FIELDS.find(f => filled(L[f]));
    if (!field) continue;
    const links = arr(L.outlinks);
    const ctx = links.length ? links : [p.file.link, ...arr(p.verses_read)];
    if (!ctx.some(belongs)) continue;
    const answered = field === "question" && arr(L.children).some(c => filled(c.answer));
    const when = [p.date, p.updated, p.created, p.file.mtime].find(isDate);
    rows.push({ field, value: L[field], where: L.section ?? p.file.link, page: p, ctx, answered, when });
  }
}
rows.sort((a, b) => (b.when ? b.when.toMillis() : 0) - (a.when ? a.when.toMillis() : 0));

// 3. Rendering.
const TRAD = [
  ["Texts/Tantraloka/", "Trika"], ["Texts/Malinislokavarttika/", "Trika"], ["Texts/Muktabodha/", "Trika"],
  ["Texts/Bible/New Testament/", "NT"], ["Texts/Fathers/", "Fathers"], ["Texts/Bible/LXX/", "LXX"], ["Texts/Bible/Tanakh/", "Tanakh"],
  ["Texts/Bible/Torah/", "Torah"], ["Texts/Zohar/", "Zohar"], ["Texts/Chasidut/", "Hasidut"], ["Texts/RCL/", "Lectionary"],
  ["Texts/Devi Mahatmya/", "Purana"], ["Texts/Markandeya Purana/", "Purana"], ["Texts/BCP 1979/", "BCP"],
  ["Texts/Bible/Douay-Rheims/", "Vulgate (DRB)"], ["Texts/Bible/NRSVue/", "NRSVue"], ["Texts/Bible/Jewish Annotated New Testament/", "JANT"], ["Texts/Pirkei Avot/", "Mishnah"], ["Texts/DCS/", "Tantra"],
  ["Texts/Aquinas/", "Aquinas"], ["Texts/Plato/", "Plato"], ["Texts/Hobbes/", "Hobbes"],
  ["Study/Concepts/", "Concept"], ["Study/Hubs/", "Hub"], ["Projects/", "Writing"], ["Journal/", "Journal"]
];
const tradition = path => {
  const t = TRAD.find(([f]) => path.startsWith(f));
  if (t) return t[1];
  if (path.startsWith("Catalog/")) return path.split("/")[1];
  return path.split("/")[0];
};
const traditions = r => [...new Set(r.ctx.map(pageOf).filter(Boolean).map(p => tradition(p.file.path)))].join(" · ");
const fmt = d => isDate(d) ? d.toFormat("yyyy-LL-dd") : "";
const want = k => opts.show === "all" || arr(opts.show).includes(k);
const table = (headers, rs, mapRow, empty) => {
  if (rs.length) dv.table(headers, rs.slice(0, opts.limit).map(mapRow));
  else dv.paragraph(empty);
};

if (want("questions")) {
  if (opts.show === "all") dv.header(3, "Open questions");
  table(["Question", "Where", "Date"],
    rows.filter(r => r.field === "question" && !r.answered),
    r => [r.value, r.where, fmt(r.when)],
    "No open questions yet. Write `- question:: …` with a link to a passage of this hub; an indented `- answer:: …` under it closes it.");
}
if (want("claims")) {
  if (opts.show === "all") dv.header(3, "Claims");
  table(["Claim", "Where", "Date"],
    rows.filter(r => r.field === "claim"),
    r => [r.value, r.where, fmt(r.when)],
    "No claims yet. Write `- claim:: …` with a link to the passage or concept it rests on.");
}
if (want("connections")) {
  if (opts.show === "all") dv.header(3, "Connections across traditions");
  table(["Connection", "Traditions", "Where"],
    rows.filter(r => r.field === "connects"),
    r => [r.value, traditions(r), r.where],
    "No connections yet. Write `- connects:: [[passage]] ↔ [[passage]]: …` with passages from two traditions.");
}
if (want("cites")) {
  if (opts.show === "all") dv.header(3, "Sources cited");
  const groups = new Map();
  for (const r of rows.filter(r => r.field === "cites")) {
    const pages = r.ctx.map(pageOf).filter(Boolean);
    const work = pages.find(p => p.file.path.startsWith("Catalog/")) ?? pages.find(p => p.file.path.startsWith("Library/")) ?? pages[0];
    const key = work ? work.file.path : "";
    const g = groups.get(key) ?? { work: work ? work.file.link : "(no link)", n: 0, where: new Map() };
    g.n += 1;
    g.where.set(r.page.file.path, r.page.file.link);
    groups.set(key, g);
  }
  const gs = [...groups.values()].sort((a, b) => b.n - a.n).slice(0, opts.limit);
  if (gs.length) dv.table(["Work", "Cited", "In"], gs.map(g => [g.work, g.n, [...g.where.values()]]));
  else dv.paragraph("Nothing cited yet. Write `- cites:: [[catalog note]] p. N, on [[passage]]`.");
}
})();
