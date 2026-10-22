// Synoptic parallels: the gospel passages of one pericope side by side, one column per gospel, in the NRSVue, the BSB
// or the Douay-Rheims. The text is read when the note is shown, from the verse paragraphs the chapter notes already
// have ("**C:V** text ^C-V"); nothing is copied into the note that calls it.
// Phase 7 (13 Oct 2026). The pericopes are the rows of the table in Texts/Crosswalks/Synoptic parallels.md.
// In a note:   await dv.view("Templates/Views/synoptic")
// The calling note's properties:
//   pericope     the row's id in the table: 1 … 48 (the JANT rows) or a section row such as 8b. Default: the first row.
//   translation  nrsvue | bsb | drb (Douay-Rheims). Default: nrsvue.
//   greek        true: under each BSB verse, the SBLGNT line.
// The select box and the buttons above the columns change these properties (processFrontMatter); the view draws
// itself again at once, and Dataview draws the block again when it sees the change.
// Options (input):  container  as in today-verses: draw into this element instead of one of the view's own.
//                   table      the path of the table note, if it is not the usual one.
//                   pericope, translation, greek   override the properties (for a block that shows one fixed row).
// Narrow screens (the Fold's cover screen): view.css puts the columns under one another, each with its heading.
const VIEW = "synoptic";
const opt = Object.assign({}, typeof input === "undefined" || !input ? {} : input);
const TABLE = opt.table || "Texts/Crosswalks/Synoptic parallels.md";

// --- The three translations: where their chapter notes are and what the notes are called.
const pad = n => String(n).padStart(2, "0");
const TRANSLATIONS = {
  nrsvue: { label: "NRSVue",       folder: "Texts/Bible/NRSVue/",         note: (book, c) => `NRSVue ${book} ${pad(c)}` },
  bsb:    { label: "BSB",          folder: "Texts/Bible/New Testament/",  note: (book, c) => `${book} ${pad(c)}` },
  drb:    { label: "Douay-Rheims", folder: "Texts/Bible/Douay-Rheims/",   note: (book, c) => `DRB ${book} ${pad(c)}` },
};
// The gospels, in the order of the columns: key, name (as in the note names), abbreviation in the table.
const GOSPELS = [["mt", "Matthew", "Mt"], ["mk", "Mark", "Mk"], ["lk", "Luke", "Lk"], ["jn", "John", "Jn"]];

// --- Where it draws (as today-verses): an element of its own in the block, made before the first await so it keeps
// its place, in place of one left by an earlier run of the same block.
const root = opt.container ? opt.container : (() => {
  const el = dv.container.createDiv({ attr: { "data-sy-view": VIEW } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-sy-view") === VIEW);
  if (old) old.replaceWith(el);
  return el;
})();
// An error is shown here, in red, instead of leaving this part of the page silently empty.
const fail = (e, where) => {
  console.error(VIEW, e);
  (where || root).createDiv({ cls: "vp-view-error", text: `${VIEW}: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
// A smaller red line inside a column (a chapter note that is missing, a row that cannot be read).
const warn = (where, text) => where.createDiv({ cls: "sy-warn", text });

// --- Small helpers for text.
const esc = s => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
// "[[Mark 01#^1-2\|Mk 1:2–8]]" -> "Mk 1:2–8"; "*word*" -> "word" (for table cells and tooltips)
const plain = s => String(s || "")
  .replace(/\[\[([^\]]*?)\]\]/g, (_, inner) => { const p = inner.split(/\\?\|/); return p.length > 1 ? p[p.length - 1] : p[0]; })
  .replace(/[*_]/g, "").trim();

// --- Reading the references of a table cell: "Mt 3:1–6, 11–12", "(Mt 7:28–29; 8:14–17)", "Mk 2:23–3:30",
// "Lk 19:28–38, 45–48; 20:1–44; (10:25–28)". A verse after a comma is in the chapter last named; brackets mark the
// parts inside them as partial parallels (the JANT's own brackets). Returns { parts: [{c1, v1, c2, v2, partial}], error }.
const parseRefs = text => {
  const s = String(text || "").replace(/\b(?:Matthew|Mark|Luke|John|Matt|Mt|Mk|Lk|Jn)\b\.?/g, " ")
    .replace(/\s*([–—-])\s*/g, "$1").trim();
  const parts = [];
  if (!s || /^[—–-]$/.test(s)) return { parts };
  const tokens = s.match(/\(|\)|;|,|[^\s(),;]+/g) || [];
  let depth = 0, chapter = null;
  for (const t of tokens) {
    if (t === "(") { depth++; continue; }
    if (t === ")") { depth--; if (depth < 0) return { parts, error: `a “)” without its “(” in “${text}”` }; continue; }
    if (t === ";" || t === ",") continue;
    const m = t.match(/^(?:(\d+)[:.])?(\d+)(?:[–—-](?:(\d+)[:.])?(\d+))?$/);
    if (!m) return { parts, error: `cannot read “${t}” in “${text}”` };
    if (m[1]) chapter = +m[1];
    if (chapter === null) return { parts, error: `a verse without a chapter in “${text}”` };
    const c1 = chapter, v1 = +m[2];
    if (m[3]) chapter = +m[3];
    const c2 = m[4] ? chapter : c1, v2 = m[4] ? +m[4] : v1;
    if (c2 < c1 || (c2 === c1 && v2 < v1)) return { parts, error: `the range “${t}” runs backwards in “${text}”` };
    parts.push({ c1, v1, c2, v2, partial: depth > 0 });
  }
  if (depth !== 0) return { parts, error: `a “(” without its “)” in “${text}”` };
  return { parts };
};
// One part as a short label: "Mt 3:1–6", "Mk 2:23–3:30", "Lk 12:10".
const partLabel = (p, abbr) => `${abbr} ${p.c1}:${p.v1}` +
  (p.c2 !== p.c1 ? `–${p.c2}:${p.v2}` : p.v2 !== p.v1 ? `–${p.v2}` : "");
// All the parts of a cell, as the table writes them: "Mt 3:1–6, 11–12", "(Mt 7:28–29; 8:14–17)",
// "Lk 19:28–38, 45–48; 20:1–44; (10:25–28)". A run of partial parts shares one pair of brackets.
const refText = (parts, abbr) => parts.map((p, i) => {
  const prev = parts[i - 1], after = parts[i + 1];
  const same = prev && prev.c2 === p.c1 && p.c1 === p.c2;
  let core = same ? `${p.v1}` + (p.v2 !== p.v1 ? `–${p.v2}` : "") : partLabel(p, "").trim();
  if (i === 0) core = `${abbr} ${core}`;
  const open = p.partial && !(prev && prev.partial), close = p.partial && !(after && after.partial);
  return (i === 0 ? "" : same ? ", " : "; ") + (open ? "(" : "") + core + (close ? ")" : "");
}).join("");

// --- The table: the rows of the first table in the note whose header has the columns id, title, Matthew, Mark, Luke,
// John and source (in any order). A cell's links are read by their labels.
const readTable = async () => {
  const f = app.vault.getAbstractFileByPath(TABLE);
  if (!f) throw new Error(`the table note “${TABLE}” is not in the vault`);
  const rows = [];
  let cols = null;
  for (const line of (await app.vault.cachedRead(f)).split("\n")) {
    if (!line.trim().startsWith("|")) { if (cols && rows.length) break; continue; }
    const cells = line.trim().split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim());
    if (!cols) {
      const h = cells.map(s => plain(s).toLowerCase());
      if (["id", "title", "mark"].every(k => h.includes(k))) cols = h;
      continue;
    }
    if (cells.every(c => /^:?-{3,}:?$/.test(c))) continue;          // the line under the header
    const cell = name => cells[cols.indexOf(name)] || "";
    const row = { id: plain(cell("id")), title: plain(cell("title")), source: cell("source").replace(/\\\|/g, "|"), errors: [] };
    if (!row.id) continue;
    for (const [k, name, abbr] of GOSPELS) {
      const r = parseRefs(plain(cell(name.toLowerCase())));
      row[k] = r.parts;
      if (r.error) row.errors.push(`${name}: ${r.error}`);
    }
    const m = row.id.match(/^(\d+)[a-z]$/);                          // "8b" is a section of row 8
    row.parent = m ? m[1] : null;
    rows.push(row);
  }
  if (!rows.length) throw new Error(`no table with the columns id, title, Matthew, Mark, Luke, John in “${TABLE}”`);
  return rows;
};

// --- Finding a chapter note: by its name, in the translation's folder (any note of that name if it has moved).
const files = app.vault.getMarkdownFiles();
const findNote = (tr, book, c) => {
  const name = TRANSLATIONS[tr].note(book, c);
  const same = files.filter(f => f.basename === name);
  return same.find(f => f.path.startsWith(TRANSLATIONS[tr].folder)) || same[0] || null;
};
// The last verse number of a note, from Obsidian's list of its block ids (the note is not opened).
const lastVerse = f => Math.max(0, ...Object.keys((f && app.metadataCache.getFileCache(f) || {}).blocks || {})
  .map(k => (k.match(/^\d+-(\d+)$/) || [])[1]).filter(Boolean).map(Number));

// --- Reading a chapter note's verses. Every paragraph that ends in " ^C-V" is one verse; a "##"/"###" heading just
// before it is kept (shown small above the verse). NRSVue notes: footnotes inline as "^[…]". BSB notes: English lines,
// then the SBLGNT line, in one paragraph, with Markdown footnotes "[^N]" whose texts are at the end of the note.
const greekLine = l => (l.match(/[Ͱ-Ͽἀ-῿]/g) || []).length > l.replace(/\s/g, "").length / 3;
const noteMarker = (text, n) => `<sup class="sy-fn" title="${esc(plain(text))}" aria-label="note: ${esc(plain(text))}">${n}</sup>`;
const letters = i => { let s = ""; i++; while (i > 0) { i--; s = String.fromCharCode(97 + (i % 26)) + s; i = Math.floor(i / 26); } return s; };
const inlineNotes = (t, next) => {                                   // "^[Or *gospel*]" (brackets may nest)
  let out = "", i = 0;
  while (i < t.length) {
    const at = t.indexOf("^[", i);
    if (at < 0) { out += t.slice(i); break; }
    let depth = 0, j = at + 1;
    for (; j < t.length; j++) { if (t[j] === "[") depth++; else if (t[j] === "]" && --depth === 0) break; }
    if (j >= t.length) { out += t.slice(i); break; }                 // no closing bracket: leave the text as it is
    out += t.slice(i, at) + noteMarker(t.slice(at + 2, j), next());
    i = j + 1;
  }
  return out;
};
// A line that Markdown would take for a list, a heading or a quotation gets a backslash, so it stays text.
const keepText = s => s.split("\n").map(l => l.replace(/^(\s*)(\d+)\.(\s)/, "$1$2\\.$3").replace(/^(\s*)([-+>#])(\s)/, "$1\\$2$3")).join("\n");
const cache = new Map();
const chapter = async (tr, book, c) => {
  const key = `${tr} ${book} ${c}`;
  if (cache.has(key)) return cache.get(key);
  const f = findNote(tr, book, c);
  const ch = { file: f, link: f ? f.path.replace(/\.md$/, "") : "", verses: new Map(), last: 0 };
  if (f) {
    const body = (await app.vault.cachedRead(f)).replace(/^---\n[\s\S]*?\n---\n/, "");
    const defs = {};                                                 // BSB footnote texts: "[^12]: …"
    body.replace(/^\[\^([^\]]+)\]:[ \t]*(.*)$/gm, (_, k, t) => { defs[k] = t; return ""; });
    let heading = null;
    for (const para of body.split(/\n[ \t]*\n/)) {
      const p = para.trim();
      const h = p.match(/^#{2,3}\s+(.+)$/);
      if (h && !p.includes("\n")) { if (!/^Chapter \d+$/.test(h[1])) heading = h[1].trim(); continue; }
      const m = p.match(/(?:^|\s)\^(\d+)-(\d+)\s*$/);
      if (!m || +m[1] !== c) continue;
      let t = p.slice(0, m.index).replace(/\s+$/, "").replace(/^\*\*\d+:\d+\*\*\s*/, "");
      let greek = "";
      if (tr === "bsb") {
        const lines = t.split("\n");
        greek = lines.filter(greekLine).join(" ").trim();
        t = lines.filter(l => !greekLine(l)).join("\n").replace(/\s+$/, "");
      }
      ch.verses.set(+m[2], { text: t, greek, heading, defs });
      heading = null;
      ch.last = Math.max(ch.last, +m[2]);
    }
  }
  cache.set(key, ch);
  return ch;
};

// --- The settings: the options, else the calling note's properties (Obsidian's copy, which is current), else
// Dataview's copy of them.
const here = dv.currentFilePath ? app.vault.getAbstractFileByPath(dv.currentFilePath) : null;
const props = (here && (app.metadataCache.getFileCache(here) || {}).frontmatter) || {};
const cur = (typeof dv.current === "function" && dv.current()) || {};
const pick = k => opt[k] !== undefined ? opt[k] : props[k] !== undefined ? props[k] : cur[k];

// --- Saving a change in the calling note's properties, then drawing again with the new settings.
let rows = [];
const save = async (state, patch) => {
  try {
    if (!here) throw new Error("the note this block is in was not found, so the change cannot be saved");
    await app.fileManager.processFrontMatter(here, fm => {
      if ("pericope" in patch) fm.pericope = String(patch.pericope);   // always text: "1" and "8b" are one property type
      if ("translation" in patch) fm.translation = patch.translation;
      if ("greek" in patch) { if (patch.greek) fm.greek = true; else delete fm.greek; }
    });
    await draw(Object.assign({}, state, { notices: [] }, patch));
  } catch (e) { fail(e); }
};

// --- Drawing. A newer drawing (after a change) stops an older one that is still reading notes.
const draw = async state => {
  const token = root.__syToken = (root.__syToken || 0) + 1;
  const stale = () => root.__syToken !== token;
  root.empty();
  const wrap = root.createDiv({ cls: "sy-wrap" });
  const row = rows.find(r => r.id === state.pericope);
  const T = TRANSLATIONS[state.translation];

  // The controls: the pericope, the translation, and (for the BSB) the Greek line.
  const bar = wrap.createDiv({ cls: "sy-bar" });
  const sel = bar.createEl("select", { cls: "dropdown sy-select", attr: { "aria-label": "Pericope" } });
  for (const r of rows) {
    const lead = r.mk.length ? refText(r.mk, "Mk") : r.mt.length ? refText(r.mt, "Mt") : r.lk.length ? refText(r.lk, "Lk") : "";
    const o = sel.createEl("option", { text: `${r.parent ? "\u2003" : ""}${r.id} · ${r.title}${lead ? " — " + lead : ""}`, value: r.id });
    if (row && r.id === row.id) o.selected = true;
  }
  if (!row) { const o = sel.createEl("option", { text: `${state.pericope} (not in the table)`, value: state.pericope }); o.selected = true; }
  sel.addEventListener("change", () => save(state, { pericope: sel.value }));
  const sw = bar.createDiv({ cls: "sy-switch", attr: { role: "group", "aria-label": "Translation" } });
  for (const [k, t] of Object.entries(TRANSLATIONS)) {
    const b = sw.createEl("button", { text: t.label, cls: k === state.translation ? "sy-on" : "",
      attr: { type: "button", "aria-pressed": String(k === state.translation) } });
    b.addEventListener("click", () => k === state.translation ? null : save(state, { translation: k }));
  }
  if (state.translation === "bsb") {
    const lab = bar.createEl("label", { cls: "sy-greek-switch" });
    const box = lab.createEl("input", { attr: { type: "checkbox" } });
    box.checked = !!state.greek;
    lab.createSpan({ text: " Greek (SBLGNT)" });
    box.addEventListener("change", () => save(state, { greek: box.checked }));
  }
  for (const n of state.notices || []) wrap.createDiv({ cls: "sy-notice", text: n });
  if (!row) { fail(new Error(`there is no row “${state.pericope}” in ${TABLE}; choose one above`), wrap); return; }

  // Where the row comes from, and its place among the section rows.
  const info = wrap.createDiv({ cls: "sy-info" });
  dv.el("span", `**${row.id} · ${row.title}** · ${row.source || "no source given"}`, { container: info });
  const goTo = (box, r, text) => {
    const b = box.createEl("button", { text, cls: "sy-goto", attr: { type: "button", title: r.title } });
    b.addEventListener("click", () => save(state, { pericope: r.id }));
  };
  if (row.parent) {
    const p = rows.find(r => r.id === row.parent);
    if (p) {
      const line = wrap.createDiv({ cls: "sy-info" });
      line.createSpan({ text: "A section of " });
      goTo(line, p, `row ${p.id}`);
      const whole = GOSPELS.filter(([k]) => p[k].length).map(([k, , a]) => refText(p[k], a)).join(" · ");
      line.createSpan({ text: `: ${whole}. A gospel missing here may still be in the row.` });
    }
  } else {
    const kids = rows.filter(r => r.parent === row.id);
    if (kids.length) {
      const line = wrap.createDiv({ cls: "sy-info" });
      line.createSpan({ text: "Sections (the NRSVue’s headings): " });
      for (const k of kids) goTo(line, k, k.id);
    }
  }
  for (const e of row.errors) warn(wrap, `This row cannot be read in full: ${e}`);

  // One column per gospel the row has.
  const present = GOSPELS.filter(([k]) => row[k].length);
  if (!present.length) { warn(wrap, "This row gives no passages."); return; }
  const grid = wrap.createDiv({ cls: "sy-grid", attr: { style: `--sy-cols: ${present.length};` } });
  // A footnote marker shows its note when tapped (a tooltip needs a mouse); a second tap hides it again.
  grid.addEventListener("click", ev => {
    try {
      const fn = ev.target && ev.target.closest ? ev.target.closest(".sy-fn") : null;
      if (!fn) return;
      const open = fn.nextElementSibling;
      if (open && open.classList.contains("sy-fn-text")) { open.remove(); return; }
      const span = document.createElement("span");
      span.className = "sy-fn-text";
      span.textContent = ` [${fn.getAttribute("title")}] `;
      fn.after(span);
    } catch (e) { fail(e); }
  });
  const cols = present.map(([k, name, abbr]) => {
    const col = grid.createDiv({ cls: "sy-col", attr: { "data-gospel": k } });
    const head = col.createDiv({ cls: "sy-head" });
    head.createSpan({ cls: "sy-gospel", text: name });
    head.createSpan({ cls: "sy-ref", text: ` ${refText(row[k], abbr)} · ${T.label}` });
    return { k, name, abbr, col };
  });
  for (const { k, name, abbr, col } of cols) {
    let n = 0;
    const told = new Set();                                          // chapters whose numbering notice is shown
    const next = () => letters(n++);                                 // footnote markers a, b, c … in each column
    const multi = row[k].length > 1;
    for (const part of row[k]) {
      const box = col.createDiv({ cls: "sy-part" + (part.partial ? " sy-partial" : "") });
      if (multi || part.partial) box.createDiv({ cls: "sy-part-head", text: partLabel(part, abbr) + (part.partial ? " (partial parallel)" : "") });
      for (let c = part.c1; c <= part.c2; c++) {
        const ch = await chapter(state.translation, name, c);
        if (stale()) return;
        if (!ch.file) { warn(box, `No note “${T.note(name, c)}” in the vault.`); continue; }
        if (state.translation === "drb") {                         // the Vulgate's numbering, where it differs
          const bsbLast = lastVerse(findNote("bsb", name, c));
          if (bsbLast && ch.last && bsbLast !== ch.last && !told.has(c) && told.add(c))
            box.createDiv({ cls: "sy-notice", text: `The Douay-Rheims ends ${name} ${c} at verse ${ch.last} (the NRSVue and the BSB at ${bsbLast}): its verse numbers here follow the Vulgate and may not match theirs.` });
        }
        const from = c === part.c1 ? part.v1 : 1;
        const to = c === part.c2 ? part.v2 : ch.last;
        // verses past the note's last verse are one line, not one dash each (a misprinted range cannot run on)
        const stop = Math.min(to, Math.max(ch.last, from - 1));
        for (let v = from; v <= stop; v++) {
          const vs = ch.verses.get(v);
          const label = (v === from || v === 1) ? `${c}:${v}` : `${v}`;
          if (vs && vs.heading) box.createDiv({ cls: "sy-heading", text: vs.heading });
          const line = box.createDiv({ cls: vs ? "sy-verse" : "sy-verse sy-missing" });
          if (!vs) {
            line.createSpan({ cls: "sy-num", text: label });
            line.createSpan({ cls: "sy-text", text: " —", attr: { title: `The ${T.label} has no verse ${c}:${v}` } });
            continue;
          }
          let text = state.translation === "nrsvue" ? inlineNotes(vs.text, next) : vs.text;
          const notes = t => t.replace(/\[\^([^\]]+)\]/g, (_, id) => vs.defs[id] ? noteMarker(vs.defs[id], next()) : "");
          text = notes(text);
          dv.el("span", `[[${ch.link}#^${c}-${v}|${label}]]`, { container: line, cls: "sy-num" });
          line.createSpan({ text: " " });
          dv.el("span", keepText(text), { container: line, cls: "sy-text" });
          if (state.translation === "bsb" && state.greek && vs.greek)
            dv.el("div", keepText(notes(vs.greek)), { container: line, cls: "sy-greek", attr: { lang: "grc" } });
        }
        if (to > stop) {
          const a = stop + 1, label = a === to ? `${c}:${a}` : `${c}:${a}–${to}`;
          const line = box.createDiv({ cls: "sy-verse sy-missing" });
          line.createSpan({ cls: "sy-num", text: label });
          line.createSpan({ cls: "sy-text", text: " —", attr: { title: `The ${T.label} has no verse ${label}; its ${name} ${c} ends at verse ${ch.last}` } });
        }
      }
    }
  }
};

try {
  rows = await readTable();
  const notices = [];
  let translation = String(pick("translation") || "nrsvue").trim().toLowerCase();
  if (!TRANSLATIONS[translation]) {
    notices.push(`“${translation}” is not one of the translations here (nrsvue, bsb, drb); showing the NRSVue.`);
    translation = "nrsvue";
  }
  const p = pick("pericope");
  const pericope = p === undefined || p === null || String(p).trim() === "" ? rows[0].id : String(p).trim();
  const greek = pick("greek") === true || String(pick("greek")).toLowerCase() === "true";
  if (opt.inspect) opt.inspect.rows = rows;                          // for the test harness: the rows as read
  await draw({ pericope, translation, greek, notices });
} catch (e) { fail(e); }
