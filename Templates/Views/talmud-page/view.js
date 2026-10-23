// Talmud page: one side of a daf laid out like the printed page (the Vilna layout), from the vault's daf notes.
// 22 Oct 2026, approved by Stephen from the mock-up (canvas "Talmud page view").
// In a note:   await dv.view("Templates/Views/talmud-page")
// The calling note's property:
//   amud   the side to show, as text: "Berakhot 2a" (or "Berakhot 2", which shows 2a). Empty: today's daf from the
//          Daf Yomi table (Calendar/Daf Yomi 2026-2029.md), side a.
// The box and the buttons above the page change the property (processFrontMatter) and draw the page again.
// What it shows, all read when the note is shown (nothing is copied into the calling note):
//   centre        the side's lines in full (the translation in bold, Steinsaltz's explanation around it), numbered
//   inner column  the halakhot of the Mishneh Torah that the side's Ein Mishpat names, quoted from their notes, and
//                 the passages "In this vault" (Hasidic texts, Kitzur, Guide) that Sefaria links to it
//   corners       Ein Mishpat and Torah Or (left), Mesoret HaShas (right)
//   outer column  every other note that links this daf ("Cited by"), and your own field lines (question::, claim::,
//                 connects::, answer::, cites::) in Journal, Study, Projects and Notes that link it ("Glosses")
// Narrow screens: view.css puts the columns under one another.
const VIEW = "talmud-page";
const opt = Object.assign({}, typeof input === "undefined" || !input ? {} : input);
const DAFYOMI = "Calendar/Daf Yomi 2026-2029.md";
const MC = app.metadataCache;

const root = opt.container ? opt.container : (() => {
  const el = dv.container.createDiv({ attr: { "data-tp-view": VIEW } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-tp-view") === VIEW);
  if (old) old.replaceWith(el);
  return el;
})();
const fail = (e, where) => {
  console.error(VIEW, e);
  (where || root).createDiv({ cls: "vp-view-error", text: `${VIEW}: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
const note = name => MC.getFirstLinkpathDest(name, "");
const md = (container, text, cls) => dv.el("div", text, { container, cls });

// "Berakhot 2a" -> {tr, d, s}; "Berakhot 2" -> side a
const parse = t => {
  const m = String(t || "").trim().replace(/\s+/g, " ").match(/^(.+?) (\d{1,3})([ab])?$/i);
  return m ? { tr: m[1], d: +m[2], s: (m[3] || "a").toLowerCase() } : null;
};
const label = p => `${p.tr} ${p.d}${p.s}`;

// Today's daf from the Daf Yomi table (its Note column names the daf note)
const today = async () => {
  const f = app.vault.getAbstractFileByPath(DAFYOMI); if (!f) return null;
  const d = window.moment ? window.moment().format("YYYY-MM-DD") : new Date().toISOString().slice(0, 10);
  const row = (await app.vault.cachedRead(f)).split("\n").find(l => l.startsWith(`| ${d} |`));
  if (!row) return null;
  const cells = row.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim());
  return parse(cells[3] || cells[1]);
};

// One side of a daf note: its margins (the callouts under the side's heading) and its lines (" ^2a-N" blocks)
const readSide = async (file, side) => {
  const text = await app.vault.cachedRead(file);
  const parts = text.split(/^## /m);
  const sec = parts.find(p => p.startsWith(side + "\n"));
  if (!sec) return null;
  const margins = {}, lines = [];
  for (const block of sec.slice(side.length + 1).split(/\n{2,}/)) {
    const b = block.trim(); if (!b) continue;
    const c = b.match(/^> \[!(\w+)\]-? ([^\n]+)\n([\s\S]*)$/);
    if (c) { margins[c[2].replace(/\s*\(\d+[ab]\)\s*$/, "")] = c[3].split("\n").map(l => l.replace(/^>\s?/, "")).filter(l => l.startsWith("- ")); continue; }
    const m = b.match(/^([\s\S]*?)\s\^\d+[ab]-(\d+)$/);
    // a paragraph with no block id (the edition's opening words before a Mishnah) is shown unnumbered, in its place
    lines.push(m ? { n: +m[2], text: m[1] } : { n: null, text: b });
  }
  return { margins, lines };
};

// "[[Mishneh Torah - Reading the Shema 01#^1-9|…]] (lines 1, 2, 3)" -> {link, target, sub, lines}
const items = list => (list || []).map(l => {
  const m = l.match(/^- (\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|[^\]]*)?\]\]|\[[^\]]*\]\([^)]*\)|[^(]+?)(?: \((?:line|lines) ([\d, ]+)\))?$/);
  return m ? { md: m[1], target: m[2] || null, sub: m[3] || null, lines: m[4] ? m[4].split(/,\s*/).map(Number) : [] } : { md: l.slice(2), lines: [] };
}).sort((a, b) => (a.lines.length ? Math.min(...a.lines) : 999) - (b.lines.length ? Math.min(...b.lines) : 999)); // in the order of the lines, as the printed margins run

// The text a link points at: a block (^c-h) or a heading (#Teaching 3, #2), from that note
const excerpt = async (target, sub, max) => {
  const f = note(target); if (!f) return null;
  const text = await app.vault.cachedRead(f);
  let t = null;
  if (sub && sub.startsWith("^")) {
    const id = sub.slice(1).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    // the paragraph that ends with the block id (never across a blank line)
    const m = text.match(new RegExp(`(?:^|\\n\\n)((?:(?!\\n\\n)[\\s\\S])*?) \\^${id}(?:\\n|$)`));
    t = m ? m[1] : null;
  } else if (sub) {
    const parts = text.split(/^#{2,6} /m); const p = parts.find(x => x.split("\n")[0].trim() === sub.trim());
    // the section under the heading, without its callouts (margins) and footnote definitions
    t = p ? p.split("\n").slice(1).join("\n").split(/\n{2,}/).filter(x => !/^\s*(>|\[\^)/.test(x)).join("\n\n").trim() : null;
  }
  if (!t) return null;
  t = t.replace(/\[\^\d+\]/g, "").replace(/^\*\*\d+\.\*\*\s*/, "").replace(/ \^[\w-]+$/gm, "");
  return clip(t, max);
};
// shorten at a sentence or clause, never leaving a link or emphasis open
const clip = (t, max) => {
  if (!max || t.length <= max) return t;
  let s = t.slice(0, max);
  const cut = Math.max(s.lastIndexOf(". "), s.lastIndexOf("; "), s.lastIndexOf(": "));
  s = cut > max * 0.5 ? s.slice(0, cut + 1) : s.replace(/\s\S*$/, "");
  const open = s.lastIndexOf("[["); if (open > s.lastIndexOf("]]")) s = s.slice(0, open);
  s = s.trimEnd();
  if ((s.match(/\*\*/g) || []).length % 2) s += "**";
  if ((s.replace(/\*\*/g, "").match(/\*/g) || []).length % 2) s += "*";
  return s + " …";
};

// Notes outside the Talmud that link this daf note; with the side when the link names it
const citedBy = (file, side) => {
  const out = [];
  for (const [src, targets] of Object.entries(MC.resolvedLinks)) {
    if (!targets[file.path] || src.startsWith("Texts/Talmud/")) continue;
    const f = app.vault.getAbstractFileByPath(src); if (!f) continue;
    const links = ((MC.getFileCache(f) || {}).links || []).filter(l => MC.getFirstLinkpathDest(l.link.split("#")[0], src) === file);
    const sides = new Set(links.map(l => (l.link.split("#")[1] || "").replace(/^\^/, "").replace(/-\d+$/, "")).filter(Boolean));
    out.push({ f, here: !sides.size || sides.has(side) });
  }
  return out.filter(x => x.here).map(x => x.f);
};
const GLOSS_DIRS = ["Journal/", "Study/", "Projects/", "Notes/"];

// --- The list of tractates and dapim above the page (23 Oct 2026, Stephen's request), like the table of contents on Sefaria:
// small, each name a link that draws the page there. The tractates, their order and their dapim are read from the Talmud index
// note ("## Seder …", "- [[Berakhot]] (dapim 2–64)"). Open or folded as last left on this device (localStorage).
const TALMUD_INDEX = "Texts/Talmud/Talmud.md";
const tractates = async () => {
  const f = app.vault.getAbstractFileByPath(TALMUD_INDEX); if (!f) return [];
  const out = []; let seder = null;
  for (const l of (await app.vault.cachedRead(f)).split("\n")) {
    const h = l.match(/^## Seder (.+?)\s*$/); if (h) { seder = { name: h[1], tr: [] }; out.push(seder); continue; }
    if (/^## /.test(l)) { seder = null; continue; }
    const m = seder && l.match(/^- \[\[([^\]|#]+)(?:\|[^\]]*)?\]\](?: \(dapim (\d+)[–-](\d+)\))?/);
    if (m) seder.tr.push({ name: m[1].trim(), first: m[2] ? +m[2] : 2, last: m[3] ? +m[3] : null });
  }
  return out.filter(x => x.tr.length);
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

const draw = async (want, notices) => {
  const token = root.__tpToken = (root.__tpToken || 0) + 1;
  const stale = () => root.__tpToken !== token;
  root.empty();
  const wrap = root.createDiv({ cls: "tp-wrap" });
  notices = [...(notices || [])];
  let p = parse(want);
  if (!p && String(want || "").trim()) notices.push(`“${String(want).trim()}” is not a daf (write it as “Berakhot 2a”), so this is today’s daf.`);
  if (!p) p = await today();
  if (!p) { fail(new Error(`there is no daf for today in ${DAFYOMI}: type one in the box, e.g. “Berakhot 2a”`), wrap); return; }
  const name = `${p.tr} ${p.d}`, file = note(name);

  // the bar: a box for any daf, the neighbouring sides, today's daf, the note itself
  const bar = wrap.createDiv({ cls: "tp-bar" });
  const box = bar.createEl("input", { cls: "tp-input", attr: { type: "text", value: label(p), "aria-label": "Daf and side, e.g. Berakhot 2a", placeholder: "Berakhot 2a" } });
  const go = bar.createEl("button", { text: "Go", attr: { type: "button" } });
  const prevS = p.s === "b" ? { ...p, s: "a" } : { ...p, d: p.d - 1, s: "b" };
  const nextS = p.s === "a" ? { ...p, s: "b" } : { ...p, d: p.d + 1, s: "a" };
  const has = q => { const f = note(`${q.tr} ${q.d}`); return f && ((MC.getFileCache(f) || {}).headings || []).some(h => h.heading === `${q.d}${q.s}`); };
  const nav = (q, txt) => { const b = bar.createEl("button", { text: txt, attr: { type: "button", "aria-label": label(q) } }); if (!has(q)) b.disabled = true; b.addEventListener("click", () => save(label(q))); };
  nav(prevS, `← ${prevS.d}${prevS.s}`); nav(nextS, `${nextS.d}${nextS.s} →`);
  const tb = bar.createEl("button", { text: "Today’s daf", attr: { type: "button" } }); tb.addEventListener("click", () => save(""));
  // Steinsaltz's explanation folded away, leaving the bold translation (folded to begin with on a narrow screen)
  if (root.__tpFold === undefined) root.__tpFold = (root.clientWidth || 800) < 600;
  const fb = bar.createEl("button", { text: "Translation only", attr: { type: "button" } });
  const fold = () => { wrap.toggleClass("tp-folded", root.__tpFold); fb.toggleClass("tp-on", root.__tpFold); fb.setAttr("aria-pressed", String(root.__tpFold)); };
  fb.addEventListener("click", () => { root.__tpFold = !root.__tpFold; fold(); }); fold();
  go.addEventListener("click", () => save(box.value)); box.addEventListener("keydown", ev => { if (ev.key === "Enter") save(box.value); });
  for (const n of notices) wrap.createDiv({ cls: "tp-notice", text: n });
  // the tractates by seder, and the dapim of this tractate (a number opens its side a, or b where the daf starts on b)
  const sedarim = await tractates(); if (stale()) return;
  const cur = sedarim.flatMap(x => x.tr).find(t => t.name === p.tr);
  const startOf = (tr, d) => has({ tr, d, s: "a" }) ? `${tr} ${d}a` : `${tr} ${d}b`;
  const rows = sedarim.map(x => ({ label: x.name, items: x.tr.map(t => ({ text: t.name, ref: startOf(t.name, t.first), on: t.name === p.tr, title: `${t.name}, dapim ${t.first}–${t.last}` })) }));
  if (cur && cur.last) { const ds = []; for (let d = cur.first; d <= cur.last; d++) if (note(`${cur.name} ${d}`)) ds.push(d);
    rows.push({ label: "Dapim", grid: true, items: ds.map(d => ({ text: String(d), ref: startOf(cur.name, d), on: d === p.d, title: `${cur.name} ${d}` })) }); }
  navBanner(wrap.createDiv({ cls: "tp-nav-host" }), "tp", `Tractates and dapim · ${p.tr}`, rows, v => save(v));
  if (!file) { fail(new Error(`there is no note “${name}” in the vault (Shekalim, Kinnim and Middot have none)`), wrap); return; }
  const side = await readSide(file, `${p.d}${p.s}`);
  if (stale()) return;
  if (!side) { fail(new Error(`“${name}” has no side ${p.d}${p.s}`), wrap); return; }
  const fm = (MC.getFileCache(file) || {}).frontmatter || {};

  // running head
  const head = wrap.createDiv({ cls: "tp-head" });
  head.createDiv({ cls: "tp-page", text: `${p.d}${p.s}` });
  const t = head.createDiv({ cls: "tp-title" });
  t.createDiv({ cls: "tp-seder", text: `Seder ${fm.seder || ""}` });
  md(t, `[[${name}#${p.d}${p.s}|${p.tr} · Daf ${p.d}]]`, "tp-tractate");

  const grid = wrap.createDiv({ cls: "tp-grid" });
  const left = grid.createDiv({ cls: "tp-margin tp-left" });
  const inner = grid.createDiv({ cls: "tp-inner" });
  const centre = grid.createDiv({ cls: "tp-centre" });
  const outer = grid.createDiv({ cls: "tp-outer" });
  const right = grid.createDiv({ cls: "tp-margin tp-right" });
  const box2 = (where, title, list, cls) => {
    const b = where.createDiv({ cls: "tp-box " + (cls || "") });
    b.createDiv({ cls: "tp-box-title", text: title });
    if (!list.length) { b.createDiv({ cls: "tp-empty", text: "—" }); return b; }
    for (const it of list) md(b, it.md + (it.lines && it.lines.length ? ` · ${it.lines.join(", ")}` : ""), "tp-item");
    return b;
  };
  const M = side.margins;
  const ein = items(M["Ein Mishpat"]), torah = items(M["Torah Or"]), mes = items(M["Mesoret HaShas"]), inVault = items(M["In this vault"]);
  box2(left, "Ein Mishpat", ein, "tp-ein");
  box2(left, "Torah Or", torah, "tp-torah");
  box2(right, "Mesoret HaShas", mes, "tp-mesoret");

  // centre: the lines, with Mishnah and Gemara headings where the text turns
  for (const l of side.lines) {
    const turn = l.text.match(/^\*\*(MISHNA|GEMARA):\*\*\s*/m);
    if (turn) centre.createDiv({ cls: "tp-rubric", text: turn[1] === "MISHNA" ? "Mishnah" : "Gemara" });
    const div = centre.createDiv({ cls: "tp-line" });
    if (l.n !== null) div.createSpan({ cls: "tp-n", text: String(l.n) });
    md(div, l.text.replace(/^\*\*(MISHNA|GEMARA):\*\*\s*/m, ""), "tp-text");
  }

  // inner column (beside the text, as Rashi stands on the printed page): the Rambam's halakhot that Ein Mishpat names,
  // then the passages of the vault's own texts that Sefaria links to these lines, each quoted from its note
  const quote = async (x, max) => {
    const q = x.target && x.sub ? await excerpt(x.target, x.sub, max) : null;
    md(inner.createDiv({ cls: "tp-quote" }), `${x.lines.length ? `**${x.lines.join(", ")}** ` : ""}${x.md}${q ? `: ${q}` : ""}`, "tp-quote-text");
  };
  inner.createDiv({ cls: "tp-col-title", text: "The Rambam on these lines" });
  const mt = ein.filter(x => x.target && x.target.startsWith("Mishneh Torah - ") && x.sub);
  if (!mt.length) inner.createDiv({ cls: "tp-empty", text: "Ein Mishpat names no halakhah of the Mishneh Torah for this side." });
  for (const x of mt.slice(0, 8)) { await quote(x, 420); if (stale()) return; }
  if (mt.length > 8) inner.createDiv({ cls: "tp-empty", text: `and ${mt.length - 8} more in Ein Mishpat` });
  const work = x => (x.target || "").split(/\s+(?=(?:[IVX]+\s*(?:-|\d))|\d)/)[0];
  const byWork = {};
  for (const x of inVault.filter(x => x.target)) (byWork[work(x)] = byWork[work(x)] || []).push(x);
  for (const [w, xs] of Object.entries(byWork)) {
    inner.createDiv({ cls: "tp-col-title tp-gap", text: w });
    for (const x of xs.slice(0, 4)) { await quote(x, 320); if (stale()) return; }
  }

  // outer column: the vault's passages as a list, then every other note that links this side
  box2(outer, "In this vault", inVault, "tp-vault");
  const cb = outer.createDiv({ cls: "tp-box tp-cited" });
  cb.createDiv({ cls: "tp-box-title", text: "Cited by" });
  const cites = citedBy(file, `${p.d}${p.s}`);
  const shown = cites.filter(f => !mt.some(x => note(x.target) === f) && !inVault.some(x => x.target && note(x.target) === f));
  if (!shown.length) cb.createDiv({ cls: "tp-empty", text: "No other note links this side yet." });
  const byTop = {};
  for (const f of shown) { const top = f.path.split("/").slice(0, 2).join("/"); (byTop[top] = byTop[top] || []).push(f); }
  for (const [top, fs] of Object.entries(byTop).sort()) {
    const g = cb.createDiv({ cls: "tp-cite-group" });
    g.createDiv({ cls: "tp-cite-top", text: top });
    md(g, fs.slice(0, 12).map(f => `[[${f.path.replace(/\.md$/, "")}|${f.basename}]]`).join(" · ") + (fs.length > 12 ? ` · and ${fs.length - 12} more` : ""), "tp-cite-list");
  }

  // right margin, under Mesoret HaShas: your own lines on this side (the five fields, read as the hubs read them)
  const glosses = [];
  const linkRe = new RegExp(`\\[\\[(?:[^\\]|#]*/)?${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?:#([^\\]|]+))?(?:\\|[^\\]]*)?\\]\\]`, "g");
  for (const f of cites.filter(f => GLOSS_DIRS.some(d => f.path.startsWith(d)))) {
    const text = await app.vault.cachedRead(f); if (stale()) return;
    for (const line of text.split("\n")) {
      if (!/^\s*- (?!\[.\])(question|claim|connects|answer|cites)::\s*\S/.test(line)) continue;
      const sides = [...line.matchAll(linkRe)].map(m => (m[1] || "").replace(/^\^/, "").replace(/-\d+$/, ""));
      if (sides.length && sides.some(s => !s || s === `${p.d}${p.s}`)) glosses.push({ f, line: line.replace(/^\s*-\s*/, "") });
    }
  }
  const gb = right.createDiv({ cls: "tp-box tp-gloss" });
  gb.createDiv({ cls: "tp-box-title", text: "Glosses" });
  if (!glosses.length) gb.createDiv({ cls: "tp-empty", text: "Your question::, claim:: and connects:: lines that link this side show here." });
  for (const g of glosses) md(gb, `${g.line} — [[${g.f.path.replace(/\.md$/, "")}|${g.f.basename}]]`, "tp-item");

  const foot = wrap.createDiv({ cls: "tp-foot" });
  const td = await today();
  md(foot, `${td ? `Daf Yomi today: [[${td.tr} ${td.d}|${td.tr} ${td.d}]] · ` : ""}${fm.translation || ""}${fm.license ? `, ${fm.license}` : ""} · margins from Sefaria’s links · [[Talmud]]`, "tp-foot-text");
};

const here = dv.currentFilePath ? app.vault.getAbstractFileByPath(dv.currentFilePath) : null;
const save = async v => {
  try {
    if (here && !opt.amud) await app.fileManager.processFrontMatter(here, fm => { fm.amud = String(v || "").trim(); });
    await draw(v, []);
  } catch (e) { fail(e); }
};
try {
  const props = (here && (MC.getFileCache(here) || {}).frontmatter) || {};
  await draw(opt.amud !== undefined ? opt.amud : props.amud, []);
} catch (e) { fail(e); }
