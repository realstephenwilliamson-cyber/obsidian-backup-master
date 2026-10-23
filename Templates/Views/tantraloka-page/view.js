// Tantrāloka page: one verse laid out like a page of the printed śāstra, from the vault's verse note and what links to it.
// 22 Oct 2026, from the mock-up Stephen approved (canvas "Page views: Torah, NT, Tantrāloka").
// In a note:   await dv.view("Templates/Views/tantraloka-page")
// The calling note's properties:
//   verse    the verse to show, as "1.1" (āhnika.verse). Empty: the first verse of today's portion in the study plan.
//   viveka   english | sanskrit | both: which Viveka to show (empty: english).
// The box, the arrows and the switches change these properties (processFrontMatter) and draw the page again.
// What it shows, all read when the note is shown (nothing is copied into the calling note):
//   centre   the mūla (Devanagari and IAST), Dyczkowski's translation, and Jayaratha's Viveka: in English from the
//            sections of Dyczkowski's volume that the verse note's [!viveka] box embeds (his notes folded, page breaks
//            joined, the page numbers kept), and in Sanskrit from the verse note's own Viveka section
//   left     the word analysis (DCS), and your word:: lines whose word is one of this verse's lemmas
//   right    the secondary-literature index line for the verse, every other note that links it, the concepts that
//            link it, Compare lines, the day of the study plan that reads it, and your question::/claim::/connects:: lines
// Narrow screens: view.css puts the columns under the text.
const VIEW = "tantraloka-page";
const opt = Object.assign({}, typeof input === "undefined" || !input ? {} : input);
const MC = app.metadataCache, V = app.vault;
const PLAN = "Texts/Tantraloka/Study plan/", SECLIT = "Texts/Tantraloka/Tantraloka - secondary literature.md", INDEX = "Texts/Tantraloka/Tantraloka.md";
const GLOSS_DIRS = ["Journal/", "Study/", "Projects/", "Notes/"];

const root = opt.container ? opt.container : (() => {
  const el = dv.container.createDiv({ attr: { "data-tl-view": VIEW } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-tl-view") === VIEW);
  if (old) old.replaceWith(el);
  return el;
})();
const fail = (e, where) => {
  console.error(VIEW, e);
  (where || root).createDiv({ cls: "vp-view-error", text: `${VIEW}: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
const md = (container, text, cls, attr) => dv.el("div", text, { container, cls, attr });
const pad = (c, v) => `Tantraloka ${String(c).padStart(2, "0")}.${String(v).padStart(3, "0")}`;
const noteOf = (c, v) => MC.getFirstLinkpathDest(pad(c, v), "");
const parse = t => { const m = String(t || "").trim().match(/^(\d{1,2})\s*[.:/ ]\s*(\d{1,3})$/); return m ? { c: +m[1], v: +m[2] } : null; };
const strip = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

// the study plan: today's row, and the day that reads a given verse
const planRows = async () => {
  const rows = [];
  for (const f of V.getMarkdownFiles().filter(f => f.path.startsWith(PLAN))) {
    for (const l of (await V.cachedRead(f)).split("\n")) {
      if (!/^\| \d{4}-\d\d-\d\d \|/.test(l)) continue;
      const cells = l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim());
      const ends = [...(cells[3] || "").matchAll(/\[\[Tantraloka (\d\d)\.(\d{3})/g)].map(m => [+m[1], +m[2]]);
      if (ends.length) rows.push({ date: cells[0], day: cells[1], cells, a: ends[0], b: ends[ends.length - 1] });
    }
  }
  return rows;
};
const key = (c, v) => c * 10000 + v;
const today = async () => {
  const d = window.moment ? window.moment().format("YYYY-MM-DD") : new Date().toISOString().slice(0, 10);
  const r = (await planRows()).find(r => r.date === d);
  return r ? { c: r.a[0], v: r.a[1] } : null;
};

// the verse note's parts
const section = (t, h) => { const m = t.match(new RegExp(`^## ${h}[ \\t]*\\n([\\s\\S]*?)(?=^## |(?![\\s\\S]))`, "m")); return m ? m[1] : ""; };
const readTranslation = t => {
  const m = t.match(/> \[!source\] (Dyczkowski, vol\. [IVXL]+)[ \t]*\n> \[\[([^\]|#]+)#\^pg(\d+)\|(pp?\. [^\]]+)\]\][^\n]*((?:\n>[^\n]*)*)/);
  if (!m) return null;
  const lines = m[5].split("\n").slice(1).map(l => l.replace(/^>\s?/, ""));
  const notes = [], paras = []; let blank = false;
  for (const l of lines) { if (!l.trim()) { blank = true; continue; } (blank ? paras : notes).push(l); }
  return { vol: m[1], note: m[2], K: m[3], label: m[4], notes, paras };
};
const vivekaEmbeds = t => [...t.matchAll(/^> !\[\[([^\]#|]+)#([^\]|]+)\]\]/gm)].map(m => ({ note: m[1], heading: m[2] }));
const afterLine = t => ((t.match(/^> \*((?:Dyczkowski gives the commentary|No commentary follows this verse)[^*]*)\*/m) || [])[1] || "").replace(/\.\s*$/, "");

// one section of Dyczkowski's volume: from its heading to the next heading of level 3 or 4
const readSection = async (noteName, heading) => {
  const f = MC.getFirstLinkpathDest(noteName, ""); if (!f) return null;
  const lines = (await V.cachedRead(f)).split("\n");
  const i = lines.findIndex(l => /^#{3,4} /.test(l) && l.replace(/^#+ /, "").trim() === heading.trim());
  if (i < 0) return null;
  let j = i + 1; while (j < lines.length && !/^#{1,4} /.test(lines[j])) j++;
  return { file: f, text: lines.slice(i + 1, j).join("\n") };
};
// body paragraphs (page breaks joined) and his notes, for reading
const JUNK = /(?<=[\p{L})’”.,;])(?:TM|™|®|°|\\\*)+/gu;
const shapeSection = (text, fileName) => {
  const body = [], notes = []; let page = null, inFoot = false, pending = null;
  for (const raw of text.split(/\n\s*\n/)) {
    const p = raw.trim(); if (!p) continue;
    const pm = p.match(/^\*\[p\. ([^\]]+)\]\* \^pg(\d+)$/);
    if (pm) { page = { label: pm[1], K: pm[2] }; inFoot = false; if (pending) pending.pages.push(page); continue; }
    if (/^(?:\\\*|\*)?\d{1,4}\s*\??\s*\\?\.\s|^\[\^\d+\]:/.test(p) || inFoot) {
      // a lower-case paragraph just before the page's first note is the end of a note carried over from the page before
      if (!inFoot && pending && pending.page === page && /^[a-z]/.test(pending.text)) { body.pop(); notes.push({ text: pending.text, page }); pending = body[body.length - 1] || null; }
      inFoot = true; notes.push({ text: p.replace(JUNK, ""), page }); continue;
    }
    const t = p.replace(JUNK, "").replace(/\[\^\d+\]/g, "");
    // a lower-case paragraph after a finished sentence is not the text running on: a note carried over from the page before
    if (/^[a-z]/.test(t) && (!pending || /[.!?”’")\]]\s*$/.test(pending.text))) { notes.push({ text: t, page }); continue; }
    if (pending && !/[.!?:;”’")\]]\s*$/.test(pending.text) && /^[a-z(‘'"“]/.test(t)) {
      pending.text = pending.text.endsWith("-") ? pending.text.slice(0, -1) + t : pending.text + " " + t; continue;
    }
    pending = { text: t, page, pages: [] }; body.push(pending);
  }
  return { body, notes, fileName };
};

// the words of the verse (DCS) and the word:: lines that name one of its lemmas
const readWords = async c_v => {
  const f = MC.getFirstLinkpathDest(`${pad(c_v.c, c_v.v)} - words`, ""); if (!f) return null;
  const padas = []; let cur = null;
  for (const l of (await V.cachedRead(f)).split("\n")) {
    if (/^## /.test(l)) { cur = { name: l.slice(3).trim(), rows: [] }; padas.push(cur); continue; }
    const cells = l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim());
    if (cur && cells.length >= 5 && !/^-+$/.test(cells[0]) && cells[0] !== "Form") cur.rows.push({ form: cells[0], lemma: cells[1], pos: cells[3], feat: cells[4].replace(/\\\|/g, "|") });
  }
  return { file: f, padas };
};
const FEAT = s => s.replace(/Case=Cpd/, "cpd.").replace(/Case=(\w+)/, (m, c) => c.toLowerCase().slice(0, 3) + ".").replace(/Gender=(\w)\w*/, (m, g) => g.toLowerCase() + ".")
  .replace(/Number=(\w)\w*/, (m, n) => n.toLowerCase() === "s" ? "sg." : n.toLowerCase() === "p" ? "pl." : "du.").replace(/VerbForm=Part/, "part.").replace(/Tense=(\w+)/, (m, t) => t.toLowerCase() + ".")
  .replace(/Mood=(\w+)/, (m, t) => t.toLowerCase() + ".").replace(/Person=(\d)/, "$1").replace(/\|/g, " ");
const POS = { NOUN: "noun", ADJ: "adj.", VERB: "verb", PRON: "pron.", CONJ: "conj.", ADV: "adv.", NUM: "num.", PART: "part." };


// --- The list of āhnikas above the page (23 Oct 2026, Stephen's request), like the table of contents on Sefaria: the 37 āhnikas
// as numbers (the name on hover, and the current one's in the heading line), and, for the current āhnika, every 25th verse
// rather than all of them (up to 613). Read from the Tantrāloka index note's list ("[[…|Āhnika 1: Name]] (332 verses, 1–333)").
// Open or folded as last left on this device (localStorage).
const ahnikas = async () => {
  const f = V.getAbstractFileByPath(INDEX); if (!f) return [];
  return [...(await V.cachedRead(f)).matchAll(/\|Āhnika (\d+): ([^\]]+)\]\](?: \((\d+) verses?, (\d+)[–-](\d+)\))?/g)]
    .map(m => ({ c: +m[1], name: m[2].trim(), first: m[4] ? +m[4] : 1, last: m[5] ? +m[5] : null }));
};
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

const draw = async (want, mode, notices) => {
  const token = root.__tlToken = (root.__tlToken || 0) + 1; const stale = () => root.__tlToken !== token;
  root.empty();
  const wrap = root.createDiv({ cls: "tl-wrap" });
  notices = [...(notices || [])];
  let p = parse(want);
  if (!p && String(want || "").trim()) notices.push(`“${String(want).trim()}” is not a verse (write it as 1.1), so this is today’s verse.`);
  if (!p) p = await today();
  if (!p) p = { c: 1, v: 1 };
  const file = noteOf(p.c, p.v);

  // the bar
  const bar = wrap.createDiv({ cls: "tl-bar" });
  const box = bar.createEl("input", { cls: "tl-input", attr: { type: "text", value: `${p.c}.${p.v}`, "aria-label": "Āhnika and verse, e.g. 1.1", placeholder: "1.1" } });
  const go = bar.createEl("button", { text: "Go", attr: { type: "button" } });
  go.addEventListener("click", () => save({ verse: box.value })); box.addEventListener("keydown", ev => { if (ev.key === "Enter") save({ verse: box.value }); });
  const nb = (c, v, dir) => { for (let k = 1; k < 6; k++) { const vv = v + dir * k; if (vv > 0 && noteOf(c, vv)) return { c, v: vv }; } const cc = c + dir; if (cc < 1 || cc > 37) return null; if (dir > 0) return noteOf(cc, 1) ? { c: cc, v: 1 } : null; for (let vv = 500; vv > 0; vv--) if (noteOf(cc, vv)) return { c: cc, v: vv }; return null; };
  const prev = nb(p.c, p.v, -1), next = nb(p.c, p.v, 1);
  for (const [q, txt] of [[prev, q => `← ${q.c}.${q.v}`], [next, q => `${q.c}.${q.v} →`]]) {
    const b = bar.createEl("button", { text: q ? txt(q) : "—", attr: { type: "button" } });
    if (!q) b.disabled = true; else b.addEventListener("click", () => save({ verse: `${q.c}.${q.v}` }));
  }
  const tb = bar.createEl("button", { text: "Today’s verses", attr: { type: "button" } }); tb.addEventListener("click", () => save({ verse: "" }));
  const sw = bar.createDiv({ cls: "tl-switch", attr: { role: "group", "aria-label": "Viveka" } });
  sw.createSpan({ cls: "tl-switch-label", text: "Viveka" });
  for (const [k, t] of [["english", "English"], ["sanskrit", "Sanskrit"], ["both", "Both"]]) {
    const b = sw.createEl("button", { text: t, attr: { type: "button", "aria-pressed": String(mode === k) } });
    if (mode === k) b.addClass("tl-on"); b.addEventListener("click", () => save({ viveka: k }));
  }
  for (const n of notices) wrap.createDiv({ cls: "tl-notice", text: n });
  const AH = await ahnikas(); if (stale()) return;
  const curA = AH.find(a => a.c === p.c), STEP = 25;
  const firstAt = (c, v) => { for (let k = 0; k < STEP; k++) if (noteOf(c, v + k)) return `${c}.${v + k}`; return `${c}.${v}`; }; // a number with no verse note opens the next that has one
  const steps = []; if (curA && curA.last) for (let v = curA.first; v <= curA.last; v += STEP) steps.push(v);
  navBanner(wrap.createDiv({ cls: "tl-nav-host" }), "tl", `Āhnikas · ${p.c}${curA ? " " + curA.name : ""}`, [
    { label: "Āhnikas", grid: true, items: AH.map(a => ({ text: String(a.c), ref: firstAt(a.c, a.first), on: a.c === p.c, title: `Āhnika ${a.c}: ${a.name}${a.last ? ` (verses ${a.first}–${a.last})` : ""}` })) },
    { label: `Verses of ${p.c}`, grid: true, items: steps.map(v => ({ text: String(v), ref: firstAt(p.c, v), on: p.v >= v && p.v < v + STEP, title: `${p.c}.${v}–${Math.min(v + STEP - 1, curA.last)}` })) }
  ], v => save({ verse: v }));
  if (!file) { fail(new Error(`there is no verse note for ${p.c}.${p.v}`), wrap); return; }
  const t = await V.cachedRead(file); if (stale()) return;

  // running head
  const idx = V.getAbstractFileByPath(INDEX);
  const chName = idx ? ((await V.cachedRead(idx)).match(new RegExp(`\\|Āhnika ${p.c}: ([^\\]]+)\\]\\]`)) || [])[1] : null;
  const head = wrap.createDiv({ cls: "tl-head" });
  const hl = head.createDiv({ cls: "tl-head-left" });
  hl.createDiv({ cls: "tl-num", text: `${p.c}.${p.v}` });
  hl.createDiv({ cls: "tl-ahnika", text: `Āhnika ${p.c}${chName ? " · " + chName : ""}` });
  const hc = head.createDiv({ cls: "tl-head-centre" });
  hc.createDiv({ cls: "tl-sub", text: "Abhinavagupta, with the Viveka of Jayaratha" });
  md(hc, `[[${file.path.replace(/\.md$/, "")}|Tantrāloka ${p.c}.${p.v}]]`, "tl-title");

  const grid = wrap.createDiv({ cls: "tl-grid" });
  const left = grid.createDiv({ cls: "tl-left" }), centre = grid.createDiv({ cls: "tl-centre" }), right = grid.createDiv({ cls: "tl-right" });
  const titled = (where, title, cls) => { const b = where.createDiv({ cls: "tl-box " + (cls || "") }); b.createDiv({ cls: "tl-box-title", text: title }); return b; };

  // centre: mūla, IAST, translation
  const mula = (t.match(/## Mūla\s*\n([\s\S]*?)\s*\^mula/) || [])[1];
  const iast = (t.match(/\^mula\s*\n([\s\S]*?)\s*\^iast/) || [])[1];
  if (mula) { const d = centre.createDiv({ cls: "tl-mula", attr: { lang: "sa" } }); for (const l of mula.trim().split("\n")) d.createDiv({ text: l.trim() }); }
  if (iast) { const d = centre.createDiv({ cls: "tl-iast", attr: { lang: "sa-Latn" } }); for (const l of iast.trim().split("\n")) d.createDiv({ text: l.trim() }); }
  const tr = readTranslation(t);
  const trBox = centre.createDiv({ cls: "tl-translation" });
  if (tr) {
    for (const x of tr.paras) md(trBox, x, "tl-tr-para");
    for (const n of tr.notes) md(trBox, n, "tl-tr-note");
    md(trBox, `${tr.vol}, [[${tr.note}#^pg${tr.K}|${tr.label}]]`, "tl-tr-src");
  } else trBox.createDiv({ cls: "tl-empty", text: "No translation callout in this verse note." });

  // centre: the Viveka
  const viv = centre.createDiv({ cls: "tl-viveka" });
  viv.createDiv({ cls: "tl-col-title", text: "Viveka of Jayaratha" });
  if (mode !== "sanskrit") {
    const en = viv.createDiv({ cls: "tl-viv-en" });
    const embeds = vivekaEmbeds(section(t, "Viveka"));
    const after = afterLine(t);
    if (after) en.createDiv({ cls: "tl-tr-note", text: after + "." });
    if (!embeds.length) en.createDiv({ cls: "tl-empty", text: "Dyczkowski’s English of the Viveka has not been located for this verse." });
    for (const e of embeds) {
      const s = await readSection(e.note, e.heading); if (stale()) return;
      if (!s) { en.createDiv({ cls: "tl-empty", text: `Section “${e.heading}” not found in ${e.note}.` }); continue; }
      const sh = shapeSection(s.text, e.note);
      for (const b of sh.body) {
        const d = en.createDiv({ cls: "tl-viv-para" });
        if (b.page && b === sh.body.find(x => x.page && x.page.K === b.page.K)) md(d, `[[${e.note}#^pg${b.page.K}|p. ${b.page.label}]]`, "tl-pg");
        md(d, b.text, "tl-viv-text");
      }
      if (sh.notes.length) {
        const det = en.createEl("details", { cls: "tl-notes" });
        det.createEl("summary", { text: `Dyczkowski’s notes (${sh.notes.length})` });
        for (const n of sh.notes) md(det, n.text, "tl-note");
      }
      md(en, `From [[${e.note}#${e.heading}|${e.heading}]] in Dyczkowski’s volume`, "tl-tr-src");
    }
  }
  if (mode !== "english") {
    const sa = viv.createDiv({ cls: "tl-viv-sa", attr: { lang: "sa" } });
    // the verse note's own Viveka: its section without the English box and the repeated verse
    let s = section(t, "Viveka").replace(/^> \[!viveka\][^\n]*\n(?:>[^\n]*\n?)*/m, "").replace(/^\s*(?:>[^\n]*\n)+/, "").trim();
    if (s) md(sa, s, "tl-viv-sa-text"); else sa.createDiv({ cls: "tl-empty", text: "No Viveka in this verse note." });
  }

  // left: words
  const w = await readWords(p); if (stale()) return;
  const wb = titled(left, "Words", "tl-words");
  const lemmas = new Set();
  const DCS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 16, 17, 18, 19, 20, 21, 26];
  if (!w) wb.createDiv({ cls: "tl-empty", text: DCS.includes(p.c) ? "No word-analysis note for this verse." : "The word analysis (DCS) covers āhnikas 1–9, 11–12, 16–21 and 26." });
  else {
    for (const pd of w.padas) {
      if (w.padas.length > 1) wb.createDiv({ cls: "tl-pada", text: pd.name });
      for (const r of pd.rows) {
        lemmas.add(strip(r.lemma));
        const d = wb.createDiv({ cls: "tl-word" });
        d.createSpan({ cls: "tl-form", text: r.form });
        d.createSpan({ cls: "tl-gram", text: ` ${POS[r.pos] || r.pos.toLowerCase()}${r.feat ? " · " + FEAT(r.feat) : ""}${r.lemma !== r.form ? " · " + r.lemma : ""}` });
      }
    }
    md(wb, `[[${w.file.path.replace(/\.md$/, "")}|The full table]]`, "tl-more");
  }
  const yw = titled(left, "Your words", "tl-yourwords");
  try {
    const items = dv.pages('"Journal"').file.lists.where(l => l.word && lemmas.has(strip(String(l.word).split(/[:,(]/)[0].trim()))).array();
    if (!items.length) yw.createDiv({ cls: "tl-empty", text: lemmas.size ? "No word:: line in your daily notes names one of these lemmas yet." : "—" });
    for (const l of items.slice(0, 20)) md(yw, `${l.word} — [[${l.path.replace(/\.md$/, "")}|${l.path.split("/").pop().replace(/\.md$/, "")}]]`, "tl-item");
  } catch (e) { yw.createDiv({ cls: "tl-empty", text: "—" }); }

  // right: secondary literature, other citations, concepts, compare, study plan, glosses
  const back = Object.entries(MC.resolvedLinks).filter(([src, tg]) => tg[file.path]).map(([src]) => src);
  const sl = titled(right, "Secondary literature", "tl-seclit");
  const slf = V.getAbstractFileByPath(SECLIT);
  const line = slf ? (await V.cachedRead(slf)).split("\n").find(l => l.startsWith(`- [[${pad(p.c, p.v)}|`)) : null;
  if (line) for (const it of line.replace(/^- \[\[[^\]]+\]\]\s*·\s*/, "").split(/\s+·\s+/)) md(sl, it.replace(/\s*\(\[pdf\]\(<[^>]*>\)\)/g, ""), "tl-item");
  else sl.createDiv({ cls: "tl-empty", text: "The secondary-literature index has no line for this verse." });
  const skip = f => f.startsWith("Texts/Tantraloka/") || f.startsWith("AI/") || f === SECLIT || GLOSS_DIRS.some(d => f.startsWith(d)) || f.startsWith("Library/Sanskrit/Tantraloka words/");
  const others = back.filter(f => !skip(f) && !f.startsWith("Study/Concepts/"));
  const ob = titled(right, "Also cited in", "tl-cited");
  if (!others.length) ob.createDiv({ cls: "tl-empty", text: "No other note links this verse." });
  const byBook = {};
  for (const f of others) { const k = f.split("/").slice(0, -1).pop() || f; (byBook[k] = byBook[k] || []).push(f); }
  for (const [k, fs] of Object.entries(byBook).sort()) md(ob, `[[${fs[0].replace(/\.md$/, "")}|${k}]]${fs.length > 1 ? ` (${fs.length} notes)` : ""}`, "tl-item");
  const concepts = back.filter(f => f.startsWith("Study/Concepts/") || f.startsWith("Study/Hubs/"));
  if (concepts.length) { const cb = titled(right, "Concepts", "tl-concepts"); for (const f of concepts) md(cb, `[[${f.replace(/\.md$/, "")}|${f.split("/").pop().replace(/\.md$/, "")}]]`, "tl-item"); }
  const cmp = t.split("\n").filter(l => /^Compare:/.test(l));
  if (cmp.length) { const cb = titled(right, "Compare", "tl-compare"); for (const l of cmp) md(cb, l.replace(/^Compare:\s*/, ""), "tl-item"); }
  const rows = await planRows(); if (stale()) return;
  const k = key(p.c, p.v), row = rows.find(r => key(...r.a) <= k && k <= key(...r.b));
  const pb = titled(right, "Study plan", "tl-plan");
  if (row) md(pb, `${window.moment ? window.moment(row.date).format("ddd D MMM YYYY") : row.date}${row.cells[4] ? ` · ${row.cells[4].replace(/\s*\(\[pdf\]\(<[^>]*>\)\)/g, "")}` : ""}`, "tl-item");
  else pb.createDiv({ cls: "tl-empty", text: "Not in the study plan’s tables." });
  const gb = titled(right, "Glosses", "tl-gloss");
  const gl = [];
  const re = new RegExp(`\\[\\[(?:[^\\]|#]*/)?${pad(p.c, p.v).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?:[#|\\]])`);
  for (const f of back.filter(f => GLOSS_DIRS.some(d => f.startsWith(d)))) {
    const ff = V.getAbstractFileByPath(f); if (!ff) continue;
    for (const l of (await V.cachedRead(ff)).split("\n")) if (/^\s*- (?!\[.\])(question|claim|connects|answer|cites)::\s*\S/.test(l) && re.test(l)) gl.push({ f, l: l.replace(/^\s*-\s*/, "") });
    if (stale()) return;
  }
  if (!gl.length) gb.createDiv({ cls: "tl-empty", text: "Your question::, claim:: and connects:: lines that link this verse show here." });
  for (const g of gl) md(gb, `${g.l} — [[${g.f.replace(/\.md$/, "")}|${g.f.split("/").pop().replace(/\.md$/, "")}]]`, "tl-item");

  md(wrap.createDiv({ cls: "tl-foot" }), `Mūla and Sanskrit Viveka: KSTS as transcribed by Muktabodha, CC BY-NC 4.0 · English: Dyczkowski’s translation · words: DCS, CC BY 4.0 · [[Tantraloka]]`, "tl-foot-text");
};

const here = dv.currentFilePath ? V.getAbstractFileByPath(dv.currentFilePath) : null;
const props = () => (here && (MC.getFileCache(here) || {}).frontmatter) || {};
const modeOf = v => ["english", "sanskrit", "both"].includes(String(v || "").trim()) ? String(v).trim() : "english";
const save = async ch => {
  try {
    const cur = props();
    const verse = "verse" in ch ? String(ch.verse || "").trim() : (opt.verse !== undefined ? opt.verse : cur.verse);
    const mode = modeOf("viveka" in ch ? ch.viveka : (opt.viveka || cur.viveka));
    if (here && opt.verse === undefined) await app.fileManager.processFrontMatter(here, fm => { fm.verse = verse; fm.viveka = mode; });
    await draw(verse, mode, []);
  } catch (e) { fail(e); }
};
try {
  const cur = props();
  await draw(opt.verse !== undefined ? opt.verse : cur.verse, modeOf(opt.viveka || cur.viveka), []);
} catch (e) { fail(e); }
