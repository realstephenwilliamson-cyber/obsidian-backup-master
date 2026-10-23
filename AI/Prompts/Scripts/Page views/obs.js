// A small stand-in for Obsidian's vault and metadata cache, built from the staged vault copy plus extra notes.
const fs = require("fs"), path = require("path"), yaml = require("js-yaml");
const { JSDOM } = require("jsdom");
module.exports = (extra = {}, opts = {}) => {
  const dom = new JSDOM("<!doctype html><body></body>"); const { document } = dom.window; const HE = dom.window.HTMLElement.prototype;
  const mk = (parent, tag, o = {}) => { const e = document.createElement(tag); if (o.cls) e.className = o.cls; if (o.text) e.textContent = o.text; for (const [k, v] of Object.entries(o.attr || {})) e.setAttribute(k, v); parent.appendChild(e); return e; };
  HE.createDiv = function (o) { return mk(this, "div", o); }; HE.createSpan = function (o) { return mk(this, "span", o); };
  HE.createEl = function (t, o) { return mk(this, t, o); }; HE.empty = function () { this.innerHTML = ""; };
  HE.addClass = function (c) { this.classList.add(c); }; HE.toggleClass = function (c, on) { this.classList.toggle(c, !!on); }; HE.setAttr = function (k, v) { this.setAttribute(k, v); };
  const U = "/mnt/user-data/uploads/Obsidian Vault/";
  const files = {};
  const walk = d => { for (const n of fs.readdirSync(U + d)) { if (n.startsWith(".")) continue; const p = d ? d + "/" + n : n; const st = fs.statSync(U + p); if (st.isDirectory()) walk(p); else if (n.endsWith(".md")) files[p] = U + p; } };
  walk("");
  const F = {}, byBase = {};
  for (const p of [...Object.keys(files), ...Object.keys(extra)]) { const f = { path: p, basename: path.basename(p, ".md"), extension: "md", name: path.basename(p) }; F[p] = f; if (!byBase[f.basename]) byBase[f.basename] = f; }
  const read = f => extra[f.path] !== undefined ? extra[f.path] : fs.readFileSync(files[f.path], "utf8");
  const dest = n => { n = n.split("#")[0].split("|")[0]; return F[n + ".md"] || F[n] || byBase[path.basename(n)] || null; };
  const posAt = (t, off) => { const before = t.slice(0, off); const line = (before.match(/\n/g) || []).length; return { line, col: off - (before.lastIndexOf("\n") + 1), offset: off }; };
  const cache = {};
  const fc = f => { if (cache[f.path]) return cache[f.path]; const t = read(f); const c = { links: [], embeds: [], headings: [], blocks: {} };
    let body0 = 0; const m = t.match(/^---\n([\s\S]*?)\n---\n?/); if (m) { try { c.frontmatter = yaml.load(m[1]) || {}; } catch (e) { c.frontmatter = {}; } body0 = m[0].length; }
    for (const mm of t.matchAll(/^(#{1,6}) (.+)$/gm)) if (mm.index >= body0) c.headings.push({ heading: mm[2].trim(), level: mm[1].length, position: { start: posAt(t, mm.index) } });
    for (const mm of t.matchAll(/(!?)\[\[([^\]|]+?)(?:\|([^\]]*))?\]\]/g)) { if (mm.index < body0) continue; const o = { link: mm[2].replace(/\\$/, ""), original: mm[0], displayText: mm[3], position: { start: posAt(t, mm.index), end: posAt(t, mm.index + mm[0].length) } }; (mm[1] ? c.embeds : c.links).push(o); }
    for (const mm of t.matchAll(/(?:^|\s)\^([A-Za-z0-9-]+)[ \t]*$/gm)) { if (mm.index < body0) continue; const ps = t.lastIndexOf("\n\n", mm.index); const s = ps < 0 ? 0 : ps + 2; c.blocks[mm[1].toLowerCase()] = { id: mm[1], position: { start: posAt(t, s), end: posAt(t, mm.index + mm[0].length) } }; }
    return cache[f.path] = c; };
  const resolvedLinks = {}; for (const f of Object.values(F)) { const r = {}; const c = fc(f); for (const l of [...c.links, ...c.embeds]) { const d = dest(l.link); if (d) r[d.path] = (r[d.path] || 0) + 1; } resolvedLinks[f.path] = r; }
  const fmWrites = [];
  const app = { metadataCache: { getFirstLinkpathDest: dest, getFileCache: fc, resolvedLinks },
    vault: { getAbstractFileByPath: p => F[p] || null, cachedRead: async f => read(f), read: async f => read(f), getMarkdownFiles: () => Object.values(F) },
    fileManager: { processFrontMatter: async (f, fn) => { const o = Object.assign({}, fc(f).frontmatter || {}); fn(o); fmWrites.push(o); } } };
  const container = document.createElement("div"); document.body.appendChild(container);
  const render = s => String(s).replace(/!?\[\[([^\]|]+)\|([^\]]+)\]\]/g, '<a class="internal-link" data-href="$1">$2</a>').replace(/!?\[\[([^\]|]+)\]\]/g, '<a class="internal-link" data-href="$1">$1</a>')
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/(^|[^*])\*([^*\n]+?)\*/g, "$1<em>$2</em>");
  const dv = { container, currentFilePath: opts.current, el: (tag, text, o) => { const e = mk(o.container, tag, { cls: o.cls, attr: o.attr }); e.innerHTML = "<p>" + render(text) + "</p>"; return e; },
    pages: () => ({ file: { lists: { where: fn => ({ array: () => [] }) } } }) };
  const win = { moment: () => ({ format: s => s === "YYYY-MM-DD" ? (opts.today || "2026-10-22") : "Thu 22 Oct 2026" }) };
  global.window = win;
  const run = async code => { await new Function("dv", "app", "input", "window", `return (async () => {${code}\n})();`)(dv, app, opts.input, win); };
  return { app, dv, container, run, fmWrites, F, read };
};
