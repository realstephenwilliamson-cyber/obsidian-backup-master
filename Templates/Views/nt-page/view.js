// New Testament page: one section of the New Testament laid out like a page of a glossed Bible, from the vault's BSB,
// SBLGNT and NRSVue notes, the Jewish Annotated New Testament's notes, and what links to them. 22 Oct 2026, from the
// mock-up Stephen approved (canvas "Page views: Torah, NT, Tantrāloka").
// In a note:   await dv.view("Templates/Views/nt-page")
// The calling note's properties:
//   ref          a verse: "Matthew 5:3", "Mt 5", "1 Cor 13:4", "Rev 21". The page shows the BSB section that holds it.
//                Empty: Matthew 5:1.
//   translation  bsb | nrsvue (empty: bsb).
//   greek        true: the SBLGNT line under each verse, each word linked to its lexicon note.
// The box, the switch and the buttons change these properties (processFrontMatter) and draw the page again.
// What it shows, all read when the note is shown (nothing is copied into the calling note):
//   centre        the verses, with the translators' notes; Compare links (the other translation, Douay-Rheims, JANT)
//   inner column  the JANT notes on these verses (and on the sections that hold them)
//   left margin   the Synoptic parallels (rows of Texts/Crosswalks/Synoptic parallels.md), the Scripture and the
//                 rabbinic texts the JANT notes cite, the rest of the New Testament they cite
//   outer column  the Fathers and Aquinas, quoted where they cite these verses; the books in the Library that cite them
//   right margin  every other note that links these verses ("Cited by") and your own question::, claim::, connects::,
//                 answer:: and cites:: lines that link them ("Glosses")
// Narrow screens: view.css puts the columns under the text.
const VIEW = "nt-page";
const opt = Object.assign({}, typeof input === "undefined" || !input ? {} : input);
const MC = app.metadataCache, V = app.vault;
const NT_DIR = "Texts/Bible/New Testament/", NRSV_DIR = "Texts/Bible/NRSVue/", DRB_DIR = "Texts/Bible/Douay-Rheims/";
const JANT_DIR = "Texts/Bible/Jewish Annotated New Testament/Annotations/", LEX_DIR = "Library/Lexicons/Greek NT/";
const TABLE = "Texts/Crosswalks/Synoptic parallels.md", READER = "Texts/Bible/Synoptic reader.md";
const GLOSS_DIRS = ["Journal/", "Study/", "Projects/", "Notes/"];
const DEFAULT = "Matthew 5:1", MAXV = 30;

const root = opt.container ? opt.container : (() => {
  const el = dv.container.createDiv({ attr: { "data-nt-view": VIEW } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-nt-view") === VIEW);
  if (old) old.replaceWith(el);
  return el;
})();
const fail = (e, where) => {
  console.error(VIEW, e);
  (where || root).createDiv({ cls: "vp-view-error", text: `${VIEW}: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
const md = (container, text, cls, attr) => dv.el("div", text, { container, cls, attr });
const fmOf = f => (MC.getFileCache(f) || {}).frontmatter || {};
const linkTo = (f, sub, label) => `[[${f.path.replace(/\.md$/, "")}${sub ? "#" + sub : ""}|${label}]]`;
const cmp = (a, b) => a[0] - b[0] || a[1] - b[1];
const pad = n => String(n).padStart(2, "0");
const letters = i => { let s = ""; i++; while (i > 0) { i--; s = String.fromCharCode(97 + (i % 26)) + s; i = Math.floor(i / 26); } return s; };

// --- The books: the BSB chapter notes ("Matthew 05") in the folders "01 Matthew" … "27 Revelation"
const index = (() => {
  const books = {}, order = [];
  for (const f of V.getMarkdownFiles().filter(f => f.path.startsWith(NT_DIR)).sort((a, b) => a.path.localeCompare(b.path))) {
    const m = f.basename.match(/^(.+?) (\d+)$/); if (!m) continue;
    if (!books[m[1]]) { books[m[1]] = {}; order.push(m[1]); }
    books[m[1]][+m[2]] = f;
  }
  return { books, order };
})();
const ABBR = { mt: "Matthew", mat: "Matthew", matt: "Matthew", mk: "Mark", mar: "Mark", mrk: "Mark", lk: "Luke", luk: "Luke", jn: "John", jhn: "John",
  joh: "John", ac: "Acts", act: "Acts", ro: "Romans", rom: "Romans", co: "Corinthians", cor: "Corinthians", ga: "Galatians", gal: "Galatians",
  eph: "Ephesians", php: "Philippians", phil: "Philippians", col: "Colossians", th: "Thessalonians", thes: "Thessalonians", thess: "Thessalonians",
  ti: "Timothy", tim: "Timothy", tit: "Titus", phm: "Philemon", phlm: "Philemon", philem: "Philemon", heb: "Hebrews", jas: "James", jam: "James",
  pe: "Peter", pet: "Peter", pt: "Peter", jud: "Jude", jude: "Jude", re: "Revelation", rev: "Revelation", apoc: "Revelation", apocalypse: "Revelation",
  jo: "John", jh: "John" };
const bookOf = raw => {
  let s = String(raw || "").trim().toLowerCase().replace(/\./g, "");
  let num = ""; const nm = s.match(/^(1|2|3|i{1,3}|first|second|third)\s*(.+)$/);
  if (nm) { num = ({ i: "1", ii: "2", iii: "3", first: "1", second: "2", third: "3" })[nm[1]] || nm[1]; s = nm[2]; }
  const flat = s.replace(/[^a-z]/g, "");
  const cands = index.order.filter(b => num ? b.startsWith(num + " ") : !/^\d /.test(b));
  const base = b => b.replace(/^\d /, "").toLowerCase().replace(/[^a-z]/g, "");
  if (ABBR[flat]) { const hit = cands.find(b => base(b) === ABBR[flat].toLowerCase()); if (hit) return hit; }
  const hits = cands.filter(b => base(b).startsWith(flat));
  return flat.length >= 2 && hits.length === 1 ? hits[0] : (hits.find(b => base(b) === flat) || null);
};
// "Matthew 5:3", "Mt 5", "1 Cor 13:4" -> { book, c, v }
const parse = t => {
  const s = String(t || "").trim().replace(/\s+/g, " "); if (!s) return null;
  const m = s.match(/^(.+?)\s+(\d+)(?:\s*[:.]\s*(\d+))?(?:\s*[-–]\s*\d+)?$/); if (!m) return null;
  const book = bookOf(m[1]); return book ? { book, c: +m[2], v: m[3] ? +m[3] : 1 } : null;
};
const noteOf = (book, c) => (index.books[book] || {})[c] || null;
const otherNote = (dir, name) => { const same = V.getMarkdownFiles().filter(f => f.basename === name); return same.find(f => f.path.startsWith(dir)) || same[0] || null; };
// a chapter note's verses in order, and its ### headings
const versesOf = f => Object.values((MC.getFileCache(f) || {}).blocks || {}).filter(b => /^\d+-\d+$/.test(b.id))
  .sort((a, b) => a.position.start.offset - b.position.start.offset).map(b => ({ cv: b.id.split("-").map(Number), off: b.position.start.offset }));
const sectionsOf = f => ((MC.getFileCache(f) || {}).headings || []).filter(h => h.level === 3).map(h => ({ title: h.heading, off: h.position.start.offset }));


// --- The list of books, chapters and sections above the page (23 Oct 2026, Stephen's request), like the table of contents on
// Sefaria: small, each name a link that draws the page there. Open or folded as last left on this device (localStorage).
const navBanner = (host, pre, summary, rows, go) => {
  host.empty();
  const det = host.createEl("details", { cls: `${pre}-nav` });
  let open = true; try { const v = window.localStorage.getItem(`${VIEW}-nav-open`); if (v !== null) open = v === "1"; } catch (e) { }
  det.open = open;
  det.createEl("summary", { text: summary });
  det.addEventListener("toggle", () => { try { window.localStorage.setItem(`${VIEW}-nav-open`, det.open ? "1" : "0"); } catch (e) { } });
  for (const r of rows) {
    if (!r.items.length) continue;
    const row = det.createDiv({ cls: `${pre}-nav-row${r.grid ? ` ${pre}-nav-grid` : ""}` });
    if (r.label) row.createSpan({ cls: `${pre}-nav-label`, text: r.label });
    const list = row.createSpan({ cls: `${pre}-nav-items` });
    for (const it of r.items) {
      const a = list.createSpan({ cls: `${pre}-nav-item${it.on ? " is-on" : ""}`, text: it.text, attr: { role: "link", tabindex: "0", title: it.title || it.text } });
      a.addEventListener("click", () => go(it.ref));
      a.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); go(it.ref); } });
    }
  }
};
// the books in the order of their folders (01 Matthew … 27 Revelation), the chapters of this book, the sections of this chapter
const ntNav = (host, p, all, secs, cur) => {
  const chs = Object.keys(index.books[p.book] || {}).map(Number).sort((a, b) => a - b);
  const rows = [{ label: "Books", items: index.order.map(b => ({ text: b, ref: `${b} 1:1`, on: b === p.book })) },
    { label: "Chapters", grid: true, items: chs.map(c => ({ text: String(c), ref: `${p.book} ${c}:1`, on: c === p.c, title: `${p.book} ${c}` })) }];
  if (all && all.length) {
    const items = [];
    if (!secs.length || all[0].off < secs[0].off) items.push({ text: `${p.c}:1`, ref: `${p.book} ${all[0].cv.join(":")}`, on: !cur, title: "the verses before the chapter's first heading" });
    for (const s of secs) { const v = all.find(x => x.off > s.off); if (v) items.push({ text: s.title, ref: `${p.book} ${v.cv.join(":")}`, on: s === cur, title: `${s.title} (${p.book} ${v.cv.join(":")})` }); }
    rows.push({ label: `Chapter ${p.c}`, items });
  }
  navBanner(host, "nt", `Books, chapters and sections · ${p.book} ${p.c}`, rows, r => save({ ref: r }));
};

// --- Reading notes (as on the Torah page)
const blockText = (text, id) => {
  const m = text.match(new RegExp(`(?:^|\\n\\n)((?:(?!\\n\\n)[\\s\\S])*?) \\^${id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?:\\n|$)`));
  return m ? m[1] : null;
};
const balance = s => { if ((s.match(/\*\*/g) || []).length % 2) s += "**"; if ((s.replace(/\*\*/g, "").match(/\*/g) || []).length % 2) s += "*"; return s; };
const clip = (t, max) => {
  if (!max || t.length <= max) return t;
  let s = t.slice(0, max);
  const cut = Math.max(s.lastIndexOf(". "), s.lastIndexOf("; "), s.lastIndexOf(": "));
  s = cut > max * 0.5 ? s.slice(0, cut + 1) : s.replace(/\s\S*$/, "");
  const open = s.lastIndexOf("[["); if (open > s.lastIndexOf("]]")) s = s.slice(0, open);
  return balance(s.trimEnd()) + " …";
};
const plainLinks = s => s.replace(/\[\[([^\]|]*?)\|([^\]]*?)\]\]/g, "$2").replace(/\[\[([^\]]*?)\]\]/g, (m, a) => a.split("#")[0].split("/").pop())
  .replace(/\[\^\d+\]/g, "").replace(/\^\[[^\]]*\]/g, "").replace(/ \^[\w-]+$/gm, "").replace(/\s+/g, " ").trim();
const around = (par, at, max) => {
  let a = Math.max(0, at - Math.floor(max * 0.55));
  if (a > 0) { const lo = Math.max(0, a - 80), m = par.slice(lo, Math.max(lo, at - 40)).match(/[.!?;:]["”’)]?\s+/); a = m ? lo + m.index + m[0].length : par.indexOf(" ", a) + 1; }
  let s = par.slice(a);
  const pre = par.slice(0, a), bold = (pre.match(/\*\*/g) || []).length % 2, ital = (pre.replace(/\*\*/g, "").match(/\*/g) || []).length % 2;
  const o = s.indexOf("]]"), c = s.indexOf("[["); if (o >= 0 && (c < 0 || o < c)) s = s.slice(o + 2);
  return (a > 0 ? "… " : "") + clip((bold ? "**" : "") + (ital ? "*" : "") + plainLinks(s).trim(), max);
};
const paraAt = (text, off) => {
  const s = text.lastIndexOf("\n\n", off), e = text.indexOf("\n\n", off);
  const a = s < 0 ? 0 : s + 2, b = e < 0 ? text.length : e;
  return { text: text.slice(a, b), at: off - a };
};
const quoted = q => /^(?:… )?\**[“"‘]/.test(q) ? q : `“${q}”`;
// inline notes "^[Gk *he*]" (brackets may nest) -> markers; the texts go to notes
const inlineNotes = (t, add) => {
  let out = "", i = 0;
  while (i < t.length) {
    const at = t.indexOf("^[", i); if (at < 0) { out += t.slice(i); break; }
    let depth = 0, j = at + 1;
    for (; j < t.length; j++) { if (t[j] === "[") depth++; else if (t[j] === "]" && --depth === 0) break; }
    if (j >= t.length) { out += t.slice(i); break; }
    out += t.slice(i, at) + add(t.slice(at + 2, j)); i = j + 1;
  }
  return out;
};
const greekLine = l => (l.match(/[Ͱ-Ͽἀ-῿]/g) || []).length > l.replace(/\s/g, "").length / 3;
const gnorm = w => w.normalize("NFD").replace(/\u0300/g, "\u0301").replace(/[^\p{L}\p{M}]/gu, "").toLowerCase().normalize("NFC");

// --- Who links these verses: links into any of the given notes whose block is one of the verses
const linksInto = (targets, ids) => {
  const want = new Set(ids.map(x => x.join("-"))), paths = new Set(targets.filter(Boolean).map(f => f.path));
  const out = [];
  for (const [src, tg] of Object.entries(MC.resolvedLinks)) {
    if (paths.has(src) || ![...paths].some(p => tg[p])) continue;
    const sf = V.getAbstractFileByPath(src); if (!sf) continue;
    const c = MC.getFileCache(sf) || {};
    for (const l of [...(c.links || []), ...(c.embeds || [])]) {
      const [p, sub] = l.link.split("#");
      if (!sub || !sub.startsWith("^") || !want.has(sub.slice(1))) continue;
      const d = MC.getFirstLinkpathDest(p, src); if (!d || !paths.has(d.path)) continue;
      out.push({ f: sf, id: sub.slice(1), cv: sub.slice(1).split("-").map(Number), off: l.position.start.offset });
    }
  }
  return out;
};
const headingAt = (f, off, level) => { const hs = ((MC.getFileCache(f) || {}).headings || []).filter(h => h.level === level && h.position.start.offset < off); return hs.length ? hs[hs.length - 1].heading : null; };
const group = (ls, keyf) => { const g = new Map(); for (const l of ls) { const k = keyf(l); if (!g.has(k)) g.set(k, []); g.get(k).push(l); } return [...g.entries()]; };
const vlist = (cvs, oneChapter) => {
  const xs = [...new Set(cvs.map(x => x.join(":")))].map(s => s.split(":").map(Number)).sort(cmp);
  const lab = x => oneChapter ? String(x[1]) : `${x[0]}:${x[1]}`;
  const out = []; let run = null;
  for (const x of xs) { if (run && run.b[0] === x[0] && run.b[1] + 1 === x[1]) run.b = x; else { run = { a: x, b: x }; out.push(run); } }
  return out.map(r => cmp(r.a, r.b) ? `${lab(r.a)}–${r.b[1]}` : lab(r.a)).join(", ");
};
const firstCv = ls => ls.map(l => l.cv).sort(cmp)[0];

// --- The Synoptic parallels table: rows whose cell for this gospel overlaps the passage
const GOSPELS = [["Matthew", "Mt"], ["Mark", "Mk"], ["Luke", "Lk"], ["John", "Jn"]];
const parseCell = text => {        // "Mt 3:1–6, 11–12", "(Mt 7:28–29; 8:14–17)" -> [{a:[c,v], b:[c,v]}]
  const s = String(text || "").replace(/\[\[[^\]]*?\\?\|([^\]]*)\]\]/g, "$1").replace(/\b(?:Mt|Mk|Lk|Jn)\b\.?/g, " ").replace(/[()*_]/g, " ").replace(/\s*([–—-])\s*/g, "$1");
  const parts = []; let c = null;
  for (const t of s.match(/[^\s,;]+/g) || []) {
    const m = t.match(/^(?:(\d+)[:.])?(\d+)(?:[–—-](?:(\d+)[:.])?(\d+))?$/); if (!m) continue;
    if (m[1]) c = +m[1]; if (c === null) continue;
    const a = [c, +m[2]]; if (m[3]) c = +m[3];
    parts.push({ a, b: m[4] ? [c, +m[4]] : a });
  }
  return parts;
};
const synoptic = async (book, first, last) => {
  const g = GOSPELS.findIndex(x => x[0] === book); if (g < 0) return null;
  const f = V.getAbstractFileByPath(TABLE); if (!f) return [];
  const rows = []; let cols = null;
  for (const line of (await V.cachedRead(f)).split("\n")) {
    if (!line.trim().startsWith("|")) { if (cols && rows.length) break; continue; }
    const cells = line.trim().split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim());
    if (!cols) { const h = cells.map(s => s.replace(/[*_]/g, "").toLowerCase()); if (["id", "title", "matthew"].every(k => h.includes(k))) cols = h; continue; }
    if (cells.every(c => /^:?-{3,}:?$/.test(c))) continue;
    const cell = n => (cells[cols.indexOf(n)] || "").replace(/\\\|/g, "|");
    const mine = parseCell(cells[cols.indexOf(book.toLowerCase())] || "");
    if (!mine.some(p => cmp(p.b, first) >= 0 && cmp(p.a, last) <= 0)) continue;
    rows.push({ id: cell("id"), title: cell("title"), others: GOSPELS.filter(x => x[0] !== book).map(x => [x[0], cell(x[0].toLowerCase())]).filter(x => x[1]) });
  }
  return rows;
};

const draw = async (want, tr, greek, notices) => {
  const token = root.__ntToken = (root.__ntToken || 0) + 1; const stale = () => root.__ntToken !== token;
  root.empty();
  const wrap = root.createDiv({ cls: "nt-wrap" });
  notices = [...(notices || [])];
  tr = tr === "nrsvue" ? "nrsvue" : "bsb";
  let p = parse(want);
  if (!p && String(want || "").trim()) notices.push(`“${String(want).trim()}” is not a verse of the New Testament (write it as “Matthew 5:3” or “1 Cor 13”), so this is ${DEFAULT}.`);
  if (!p) p = parse(DEFAULT);
  const file = noteOf(p.book, p.c);

  // the bar
  const bar = wrap.createDiv({ cls: "nt-bar" });
  const box = bar.createEl("input", { cls: "nt-input", attr: { type: "text", value: `${p.book} ${p.c}:${p.v}`, "aria-label": "Verse, e.g. Matthew 5:3", placeholder: "Matthew 5:3" } });
  const go = bar.createEl("button", { text: "Go", attr: { type: "button" } });
  go.addEventListener("click", () => save({ ref: box.value })); box.addEventListener("keydown", ev => { if (ev.key === "Enter") save({ ref: box.value }); });
  const navs = bar.createDiv({ cls: "nt-navs" });
  const sw = bar.createDiv({ cls: "nt-switch", attr: { role: "group", "aria-label": "Translation" } });
  for (const [k, lab] of [["bsb", "BSB"], ["nrsvue", "NRSVue"]]) {
    const b = sw.createEl("button", { text: lab, cls: k === tr ? "nt-on" : "", attr: { type: "button", "aria-pressed": String(k === tr) } });
    b.addEventListener("click", () => save({ translation: k }));
  }
  const gl = bar.createEl("label", { cls: "nt-greek-toggle" });
  const gc = gl.createEl("input", { attr: { type: "checkbox" } }); gc.checked = !!greek; gl.appendText ? gl.appendText(" Greek") : gl.createSpan({ text: " Greek" });
  gc.addEventListener("change", () => save({ greek: gc.checked }));
  if (!file) { for (const n of notices) wrap.createDiv({ cls: "nt-notice", text: n }); ntNav(wrap.createDiv({ cls: "nt-nav-host" }), p, null, [], null); fail(new Error(`there is no note in the vault for ${p.book} ${p.c}`), wrap); return; }

  // the passage: the BSB section (### heading) that holds the verse, at most MAXV verses
  const all = versesOf(file), secs = sectionsOf(file);
  let i = all.findIndex(x => x.cv[0] === p.c && x.cv[1] === p.v);
  if (i < 0) { notices.push(`${p.book} ${p.c}:${p.v} is not in ${file.basename}; showing its first verse.`); i = 0; }
  const secBefore = secs.filter(s => s.off < all[i].off).pop(), secAfter = secs.find(s => s.off > all[i].off);
  let i0 = all.findIndex(x => x.off > (secBefore ? secBefore.off : -1)), i1 = secAfter ? all.findIndex(x => x.off > secAfter.off) - 1 : all.length - 1;
  if (i1 < 0) i1 = all.length - 1;
  if (i1 - i0 + 1 > MAXV) { i0 = Math.max(i0, Math.min(i, i1 - MAXV + 1)); i1 = i0 + MAXV - 1; notices.push(`This section is long; ${MAXV} verses are shown. The arrows go on through it.`); }
  const ids = all.slice(i0, i1 + 1).map(x => x.cv), first = ids[0], last = ids[ids.length - 1];
  const title = secBefore ? secBefore.title : `Chapter ${p.c}`;
  // the arrows: the verse before and after the passage, into the neighbouring chapter at either end
  const chs = Object.keys(index.books[p.book]).map(Number).sort((a, b) => a - b), ci = chs.indexOf(p.c);
  const edge = (c, end) => { const f = noteOf(p.book, c); const vs = f ? versesOf(f) : []; const x = vs.length ? vs[end ? vs.length - 1 : 0].cv : null; return x ? `${p.book} ${x[0]}:${x[1]}` : null; };
  const prevRef = i0 > 0 ? `${p.book} ${all[i0 - 1].cv.join(":")}` : (ci > 0 ? edge(chs[ci - 1], true) : null);
  const nextRef = i1 + 1 < all.length ? `${p.book} ${all[i1 + 1].cv.join(":")}` : (ci + 1 < chs.length ? edge(chs[ci + 1], false) : null);
  for (const [r, t] of [[prevRef, "← earlier"], [nextRef, "later →"]]) {
    const b = navs.createEl("button", { text: t, attr: { type: "button", "aria-label": r || t } });
    if (!r) b.disabled = true; else b.addEventListener("click", () => save({ ref: r }));
  }
  for (const n of notices) wrap.createDiv({ cls: "nt-notice", text: n });
  ntNav(wrap.createDiv({ cls: "nt-nav-host" }), p, all, secs, secBefore);

  const bsbText = await V.cachedRead(file); if (stale()) return;
  const nrsv = otherNote(NRSV_DIR, `NRSVue ${p.book} ${pad(p.c)}`), drb = otherNote(DRB_DIR, `DRB ${p.book} ${pad(p.c)}`), jant = otherNote(JANT_DIR, `JANT ${p.book} ${pad(p.c)}`);
  const nrsvText = nrsv ? await V.cachedRead(nrsv) : ""; if (stale()) return;
  if (tr === "nrsvue" && !nrsv) { wrap.createDiv({ cls: "nt-notice", text: `There is no NRSVue note for ${p.book} ${p.c}; the BSB is shown.` }); tr = "bsb"; }

  // running head
  const head = wrap.createDiv({ cls: "nt-head" });
  const hl = head.createDiv({ cls: "nt-head-left" });
  hl.createDiv({ cls: "nt-num", text: first[0] === last[0] ? `${first[0]}:${first[1]}${ids.length > 1 ? "–" + last[1] : ""}` : `${first[0]}:${first[1]}–${last[0]}:${last[1]}` });
  hl.createDiv({ cls: "nt-book", text: p.book });
  const hc = head.createDiv({ cls: "nt-head-centre" });
  hc.createDiv({ cls: "nt-sub", text: `New Testament · ${p.book} ${p.c}` });
  md(hc, linkTo(file, title, title), "nt-title");

  const grid = wrap.createDiv({ cls: "nt-grid" });
  const left = grid.createDiv({ cls: "nt-margin nt-left" }), inner = grid.createDiv({ cls: "nt-inner" }), centre = grid.createDiv({ cls: "nt-centre" });
  const outer = grid.createDiv({ cls: "nt-outer" }), right = grid.createDiv({ cls: "nt-margin nt-right" });
  const titled = (where, t, cls) => { const b = where.createDiv({ cls: "nt-box " + (cls || "") }); b.createDiv({ cls: "nt-box-title", text: t }); return b; };
  const oneChapter = first[0] === last[0];
  const vlab = cv => oneChapter ? String(cv[1]) : cv.join(":");

  // the lexicon: for each verse, the form (the heading over the link in a lemma note) -> that lemma note
  const LL = linksInto([file, nrsv, drb], ids), lex = {};
  if (greek) for (const l of LL) if (l.f.path.startsWith(LEX_DIR)) {
    const form = headingAt(l.f, l.off, 2); if (!form) continue;
    (lex[l.id] = lex[l.id] || {})[gnorm(form.replace(/\s*\(\d+\)\s*$/, ""))] = l.f;
  }

  // centre: the verses
  const notes = []; let sec = null;
  const bsbDefs = {}; for (const m of bsbText.matchAll(/^\[\^(\d+)\]:\s*(.+)$/gm)) bsbDefs[m[1]] = m[2];
  const bsbUsed = {};
  for (const cv of ids) {
    const id = cv.join("-");
    const raw = blockText(bsbText, id) || "";
    const lines = raw.replace(/^\*\*\d+:\d+\*\*\s*/, "").split("\n");
    const gk = lines.filter(greekLine).join(" ").trim();
    let t;
    if (tr === "bsb") {
      // a ### heading inside the passage starts a new part of it
      const at = all.find(x => x.cv[0] === cv[0] && x.cv[1] === cv[1]).off, h = secs.filter(s => s.off < at).pop();
      if (h && h !== secBefore && h !== sec) { centre.createDiv({ cls: "nt-heading", text: h.title }); sec = h; }
      t = lines.filter(l => !greekLine(l)).join("\n").replace(/\s+$/, "").replace(/\[\^(\d+)\]/g, (m, n) => { if (!(n in bsbUsed)) { bsbUsed[n] = notes.length; notes.push(bsbDefs[n] || ""); } return `<sup class="nt-fn">${letters(bsbUsed[n])}</sup>`; });
    } else {
      t = (blockText(nrsvText, id) || "").replace(/^\*\*\d+:\d+\*\*\s*/, "");
      t = inlineNotes(t, x => { notes.push(x); return `<sup class="nt-fn">${letters(notes.length - 1)}</sup>`; });
    }
    const d = centre.createDiv({ cls: "nt-verse" });
    md(d, `<span class="nt-vn">${vlab(cv)}</span> ${t.replace(/ {2}\n/g, "<br>").replace(/\n/g, " ")}`, "nt-verse-text");
    if (greek && gk) {
      const L = lex[id] || {};
      md(d, gk.split(/(\s+)/).map(w => { const m = w.match(/^([^\p{L}]*)([\p{L}\p{M}’']+)(.*)$/u); if (!m) return w; const f = L[gnorm(m[2])];
        return f ? `${m[1]}[[${f.path.replace(/\.md$/, "")}|${m[2]}]]${m[3]}` : w; }).join(""), "nt-greek", { lang: "grc" });
    }
  }
  if (notes.length) { const fb = centre.createDiv({ cls: "nt-notes" }); notes.forEach((n, k) => md(fb, `<sup>${letters(k)}</sup> ${n}`, "nt-note")); }
  const cmpl = [tr === "bsb" ? (nrsv ? linkTo(nrsv, `^${first.join("-")}`, "NRSVue") : null) : linkTo(file, `^${first.join("-")}`, "BSB and SBLGNT"),
    drb ? linkTo(drb, `^${first.join("-")}`, "Douay-Rheims") : null, jant ? linkTo(jant, null, "JANT notes") : null].filter(Boolean);
  if (cmpl.length) md(centre.createDiv({ cls: "nt-compare" }), `Compare: ${cmpl.join(" · ")}`, "nt-compare-text");

  // inner column: the JANT notes (section notes that overlap the passage, then the verse notes)
  inner.createDiv({ cls: "nt-col-title", text: "Jewish Annotated New Testament" });
  const cited = [];      // links in the JANT paragraphs shown: { link, label, cv }
  if (!jant) inner.createDiv({ cls: "nt-empty", text: `No JANT notes for ${p.book} ${p.c} in the vault.` });
  else {
    const jt = (await V.cachedRead(jant)).replace(/^---\n[\s\S]*?\n---\n/, ""); if (stale()) return;
    let secTitle = null, shown = 0;
    for (const para of jt.split(/\n{2,}/)) {
      const s = para.trim();
      const h = s.match(/^#{2,3}\s+(\d+)\.(\d+)(?:[–-](?:(\d+)\.)?(\d+))?:\s*(.+)$/);
      if (h) { const a = [+h[1], +h[2]], b = h[4] ? [h[3] ? +h[3] : a[0], +h[4]] : a; secTitle = { a, b, title: `${h[1]}.${h[2]}${h[4] ? "–" + (h[3] ? h[3] + "." : "") + h[4] : ""}: ${h[5]}` }; continue; }
      if (/^#/.test(s) || !s) continue;
      let a, b, body, lab;
      const vn = s.match(/^\*\*\[\[[^\]|#]+#\^(\d+)-(\d+)\|([^\]]+)\]\]:?\*\*:?\s*/);
      if (vn) { a = [+vn[1], +vn[2]]; const r = vn[3].match(/(\d+)\s*[–-]\s*(\d+)$/); b = r ? [a[0], +r[2]] : a; body = s.slice(vn[0].length); lab = vn[3]; }
      else if (secTitle && /^\*\[\[[^\]]+\]\],?\s*p\.\s*\d+\*/.test(s)) { a = secTitle.a; b = secTitle.b; body = s.replace(/^\*\[\[[^\]]+\]\],?\s*p\.\s*\d+\*\s*·\s*/, ""); lab = null; }
      else continue;
      if (cmp(b, first) < 0 || cmp(a, last) > 0) continue;
      body = body.replace(/\s*\^[\w-]+\s*$/, "");
      const on = lab || secTitle.title.split(":")[0];
      for (const m of body.matchAll(/\[\[([^\]|]+?)(?:\|([^\]]*))?\]\]/g)) cited.push({ link: m[1], label: m[2] || m[1].split("#")[0], on });
      const d = inner.createDiv({ cls: lab ? "nt-jant" : "nt-jant nt-jant-sec" });
      md(d, lab ? `<span class="nt-vn">${lab}</span> ${body}` : `<span class="nt-jant-head">${secTitle.title}</span> ${body}`, "nt-quote-text");
      shown++;
    }
    if (!shown) inner.createDiv({ cls: "nt-empty", text: "The JANT has no note on these verses." });
    md(inner, `${fmOf(jant).annotator ? fmOf(jant).annotator + "’s notes" : "Notes"}, from ${linkTo(jant, null, jant.basename)}`, "nt-src");
  }

  // left margin: parallels, then what the JANT notes cite
  const rows = await synoptic(p.book, first, last); if (stale()) return;
  if (rows) {
    const pb = titled(left, "Parallels", "nt-parallels");
    if (!rows.length) pb.createDiv({ cls: "nt-empty", text: "No row of the Synoptic parallels table holds these verses." });
    for (const r of rows) {
      md(pb, `**${r.title}** (row ${r.id})${r.others.length ? "<br>" + r.others.map(x => x[1]).join("<br>") : ""}`, "nt-item");
      const b = pb.createEl("button", { cls: "nt-small", text: "Side by side", attr: { type: "button", "aria-label": `Open row ${r.id} in the Synoptic reader` } });
      b.addEventListener("click", async () => {
        try { const rf = V.getAbstractFileByPath(READER); if (!rf) throw new Error("the Synoptic reader note is not in the vault");
          await app.fileManager.processFrontMatter(rf, fm => { fm.pericope = String(r.id); }); await app.workspace.openLinkText(rf.path, here ? here.path : "", false); } catch (e) { fail(e, pb); }
      });
    }
  }
  const kind = l => { const d = MC.getFirstLinkpathDest(l.link.split("#")[0], jant ? jant.path : ""); const s = d ? d.path : "";
    if (/^Texts\/Bible\/(Torah|Tanakh|LXX)\//.test(s)) return "ot";
    if (s.startsWith(NT_DIR) || s.startsWith(NRSV_DIR)) return /^Texts\/Bible\/NRSVue\/(0\d|[1-4]\d|5[0-7]) /.test(s) ? "ot" : "nt";
    if (/^Texts\/(Talmud|Pirkei Avot|Maimonides|Zohar|Kitzur Shulchan Arukh|Chasidut)\//.test(s)) return "rab";
    return null; };
  const list = (t, k, cls, empty) => {
    const xs = cited.filter(l => kind(l) === k), seen = new Set(), out = [];
    for (const l of xs) { const key = l.link; if (seen.has(key)) { const o = out.find(o => o.l.link === key); if (!o.vs.includes(l.on)) o.vs.push(l.on); continue; } seen.add(key); out.push({ l, vs: [l.on] }); }
    if (!out.length && !empty) return;
    const b = titled(left, t, cls);
    if (!out.length) b.createDiv({ cls: "nt-empty", text: empty });
    for (const o of out.slice(0, 18)) md(b, `[[${o.l.link}|${o.l.label}]] · ${o.vs.join(", ")}`, "nt-item");
    if (out.length > 18) b.createDiv({ cls: "nt-empty", text: `and ${out.length - 18} more in the notes` });
  };
  list("Scripture behind it", "ot", "nt-ot", jant ? "The JANT notes here cite no verse of the Hebrew Bible." : null);
  list("Rabbinic texts", "rab", "nt-rab", null);
  list("Elsewhere in the New Testament", "nt", "nt-ntx", null);

  // who links these verses (in the BSB, the NRSVue or the Douay-Rheims)
  const L = LL.filter(l => !(jant && l.f === jant) && !l.f.path.startsWith(LEX_DIR) && !l.f.path.startsWith("AI/"));
  const isGloss = s => GLOSS_DIRS.some(d => s.startsWith(d));
  // outer column: the Fathers and Aquinas, quoted; then the Library's books
  outer.createDiv({ cls: "nt-col-title", text: "The Fathers and Aquinas" });
  const fa = L.filter(l => /^Texts\/(Fathers|Aquinas)\//.test(l.f.path));
  const picks = [], seen = new Set();
  for (const l of [...fa].sort((a, b) => cmp(a.cv, b.cv) || a.off - b.off)) {
    if (picks.length >= 8) break;
    if (picks.filter(x => x.l.f === l.f).length >= 2) continue;
    const t = await V.cachedRead(l.f); if (stale()) return;
    const pa = paraAt(t, l.off), key = l.f.path + "|" + pa.text.slice(0, 60);
    if (seen.has(key)) continue; seen.add(key);
    picks.push({ l, q: around(pa.text, pa.at, 260) });
  }
  const flabel = f => f.basename.replace(/^Aquinas Summa /, "Summa ").replace(/\bQ0*(\d+)/, "q. $1").replace(/\bHom 0*(\d+)/, "Hom. $1").replace(/ 0+(\d)/g, " $1");
  if (!picks.length) outer.createDiv({ cls: "nt-empty", text: "No Father and no question of the Summa cites these verses." });
  for (const x of picks) md(outer.createDiv({ cls: "nt-quote" }), `<span class="nt-vn">${vlab(x.l.cv)}</span> ${linkTo(x.l.f, null, flabel(x.l.f))}: ${quoted(x.q)}`, "nt-quote-text");
  if (fa.length) {
    const works = group(fa, l => l.f.path.split("/")[2]);
    md(outer, `All that cite these verses: ${works.map(([w, ls]) => `${w} (${new Set(ls.map(l => l.f.path)).size})`).join(" · ")}`, "nt-src");
  }
  const lib = L.filter(l => l.f.path.startsWith("Library/"));
  const lb = titled(outer, "In the library", "nt-library");
  const book = s => { const ps = s.replace(/\.md$/, "").split("/"); return ps.length >= 4 ? ps[2] : ps[ps.length - 1]; };
  const shelves = group(lib, l => book(l.f.path)).sort((a, b) => cmp(firstCv(a[1]), firstCv(b[1])));
  if (!shelves.length) lb.createDiv({ cls: "nt-empty", text: "No book in the Library cites these verses." });
  for (const [s, ls] of shelves.slice(0, 12)) md(lb, `${linkTo(ls[0].f, null, s)} · ${vlist(ls.map(l => l.cv), oneChapter)}`, "nt-item");
  if (shelves.length > 12) lb.createDiv({ cls: "nt-empty", text: `and ${shelves.length - 12} more books` });

  // right margin: glosses, then cited by
  const wantIds = new Set(ids.map(x => x.join("-"))), names = [file, nrsv, drb].filter(Boolean).map(f => f.basename);
  const re = new RegExp(`\\[\\[(?:[^\\]|#]*/)?(?:${names.map(n => n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})(?:#\\^([\\d-]+))?(?:\\|[^\\]]*)?\\]\\]`, "g");
  const lines = [];
  for (const [s, tg] of Object.entries(MC.resolvedLinks)) {
    if (!isGloss(s) || ![file, nrsv, drb].some(f => f && tg[f.path])) continue;
    const f = V.getAbstractFileByPath(s); if (!f) continue;
    for (const l of (await V.cachedRead(f)).split("\n")) {
      if (!/^\s*- (?!\[.\])(question|claim|connects|answer|cites)::\s*\S/.test(l)) continue;
      const hits = [...l.matchAll(re)]; if (hits.some(h => !h[1] || wantIds.has(h[1]))) lines.push({ f, l: l.replace(/^\s*-\s*/, "") });
    }
    if (stale()) return;
  }
  const glossed = new Set(lines.map(g => g.f.path));
  const others = L.filter(l => !/^Texts\/(Fathers|Aquinas)\//.test(l.f.path) && !l.f.path.startsWith("Library/") && !(isGloss(l.f.path) && glossed.has(l.f.path)));
  const cb = titled(right, "Cited by", "nt-cited");
  const shelf = s => { const ps = s.replace(/\.md$/, "").split("/"), base = ps[ps.length - 1];
    if (ps[0] === "Texts") return ps[1] === "Bible" ? ps[2] : ps.length === 3 ? base : ps[1];
    if (ps[0] === "Journal") return "Journal";
    if (ps[0] === "Projects") return ps.length > 2 ? ps[1] : base;
    return ps.length > 2 ? ps[1] : base; };
  const sh = group(others, l => shelf(l.f.path)).sort((a, b) => new Set(b[1].map(l => l.f.path)).size - new Set(a[1].map(l => l.f.path)).size);
  if (!sh.length) cb.createDiv({ cls: "nt-empty", text: "No other note links these verses." });
  for (const [s, ls] of sh.slice(0, 14)) { const n = new Set(ls.map(l => l.f.path)).size; md(cb, `${linkTo(ls[0].f, null, s)}${n > 1 ? ` (${n} notes)` : ""} · ${vlist(ls.map(l => l.cv), oneChapter)}`, "nt-item"); }
  if (sh.length > 14) cb.createDiv({ cls: "nt-empty", text: `and ${sh.length - 14} more` });
  const nlex = new Set(LL.filter(l => l.f.path.startsWith(LEX_DIR)).map(l => l.f.path)).size, nl = `${nlex} lexicon note${nlex === 1 ? "" : "s"}`;
  if (nlex) cb.createDiv({ cls: "nt-empty", text: greek ? `The Greek words link to their ${nl}.` : `${nl}; tick Greek to see the words linked.` });
  const glb = titled(right, "Glosses", "nt-gloss");
  if (!lines.length) glb.createDiv({ cls: "nt-empty", text: "Your question::, claim:: and connects:: lines that link these verses show here." });
  for (const g of lines) md(glb, `${g.l} — ${linkTo(g.f, null, g.f.basename)}`, "nt-item");

  const fm = fmOf(tr === "bsb" ? file : nrsv);
  md(wrap.createDiv({ cls: "nt-foot" }), `${tr === "bsb" ? "Berean Standard Bible (public domain)" : (fm.translation || "NRSVue")}${greek || tr === "bsb" ? " · SBLGNT (CC BY 4.0)" : ""}${jant ? ` · JANT, 2nd ed. (${fmOf(jant).annotator || "notes"})` : ""} · margins: the notes that link these verses · [[New Testament]]`, "nt-foot-text");
};

const here = dv.currentFilePath ? V.getAbstractFileByPath(dv.currentFilePath) : null;
const props = () => (here && (MC.getFileCache(here) || {}).frontmatter) || {};
const state = () => { const c = props(); return { ref: opt.ref !== undefined ? opt.ref : c.ref, tr: opt.translation || c.translation, greek: opt.greek !== undefined ? opt.greek : c.greek === true || c.greek === "true" }; };
const save = async ch => {
  try {
    const s = state();
    if ("ref" in ch) { const pp = parse(ch.ref); s.ref = pp ? `${pp.book} ${pp.c}:${pp.v}` : String(ch.ref || "").trim(); }
    if ("translation" in ch) s.tr = ch.translation;
    if ("greek" in ch) s.greek = !!ch.greek;
    if (here && opt.ref === undefined) await app.fileManager.processFrontMatter(here, fm => {
      fm.ref = s.ref || ""; fm.translation = s.tr || "bsb"; if (s.greek) fm.greek = true; else delete fm.greek; });
    await draw(s.ref, s.tr, s.greek, []);
  } catch (e) { fail(e); }
};
try { const s = state(); await draw(s.ref, s.tr, s.greek, []); } catch (e) { fail(e); }
