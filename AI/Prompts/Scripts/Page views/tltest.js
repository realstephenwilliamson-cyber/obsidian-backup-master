const fs = require("fs"), path = require("path");
const { JSDOM } = require("jsdom");
const dom = new JSDOM("<!doctype html><body></body>"); const { document } = dom.window; const HE = dom.window.HTMLElement.prototype;
const mk = (parent, tag, o = {}) => { const e = document.createElement(tag); if (o.cls) e.className = o.cls; if (o.text) e.textContent = o.text; for (const [k, v] of Object.entries(o.attr || {})) e.setAttribute(k, v); parent.appendChild(e); return e; };
HE.createDiv = function (o) { return mk(this, "div", o); }; HE.createSpan = function (o) { return mk(this, "span", o); };
HE.createEl = function (t, o) { return mk(this, t, o); }; HE.empty = function () { this.innerHTML = ""; };
HE.addClass = function (c) { this.classList.add(c); }; HE.toggleClass = function (c, on) { this.classList.toggle(c, !!on); }; HE.setAttr = function (k, v) { this.setAttribute(k, v); };
const U = "/mnt/user-data/uploads/Obsidian Vault/";
const files = {};
for (const p of ["Texts/Tantraloka/Ahnika 01/Tantraloka 01.001.md", "Texts/Tantraloka/Ahnika 01/Tantraloka 01.002.md", "Texts/Tantraloka/Ahnika 08/Tantraloka 08.036.md",
  "Library/Trika/Tantraloka (Dyczkowski)/Tantraloka vol 01 (Dyczkowski)/Tantraloka Dyczkowski v01 02 - Chapter One, part 1.md",
  "Library/Trika/Tantraloka (Dyczkowski)/Tantraloka vol 05 (Dyczkowski)/Tantraloka Dyczkowski v05 04 - Chapter Eight, part 2.md",
  "Texts/Tantraloka/Study plan/Study plan - Year 1 (2026-27).md", "Texts/Tantraloka/Study plan/Study plan - Practice run 2026.md",
  "Texts/Tantraloka/Tantraloka - secondary literature.md", "Texts/Tantraloka/Tantraloka.md"]) files[p] = U + p;
files["Library/Sanskrit/Tantraloka words/01/Tantraloka 01.001 - words.md"] = "words/Tantraloka 01.001 - words.md";
const extra = { "Texts/Tantraloka/Tantraloka page.md": "---\nverse: \"" + (process.argv[2] ?? "1.1") + "\"\nviveka: \"" + (process.argv[3] ?? "both") + "\"\n---\n",
  "Journal/2026/2026-10-22.md": "- claim:: [[Tantraloka 01.001|TĀ 1.1]] opens with the parents.\n", "Library/Trika/X/Some book 01.md": "see [[Tantraloka 01.001|TĀ 1.1]]", "Study/Concepts/Prakasa and Vimarsa.md": "[[Texts/Tantraloka/Ahnika 01/Tantraloka 01.001|TĀ 1.1]]" };
const F = {}, byBase = {};
for (const p of [...Object.keys(files), ...Object.keys(extra)]) { const f = { path: p, basename: path.basename(p, ".md") }; F[p] = f; byBase[f.basename] = byBase[f.basename] || f; }
const read = f => extra[f.path] !== undefined ? extra[f.path] : fs.readFileSync(files[f.path], "utf8");
const dest = n => { n = n.split("#")[0]; return F[n + ".md"] || F[n] || byBase[path.basename(n)] || null; };
const fc = f => { const t = read(f); const c = { links: [] }; const m = t.match(/^---\n([\s\S]*?)\n---/); if (m) { c.frontmatter = {}; for (const l of m[1].split("\n")) { const mm = l.match(/^(\w+): "?(.*?)"?$/); if (mm) c.frontmatter[mm[1]] = mm[2]; } } for (const mm of t.matchAll(/\[\[([^\]|]+)(?:\|[^\]]*)?\]\]/g)) c.links.push({ link: mm[1] }); return c; };
const resolvedLinks = {}; for (const f of Object.values(F)) { const r = {}; for (const l of fc(f).links) { const d = dest(l.link); if (d) r[d.path] = 1; } resolvedLinks[f.path] = r; }
global.window = { moment: (d) => ({ format: (s) => s === "YYYY-MM-DD" ? "2026-11-29" : "Sun 29 Nov 2026" }) };
const app = { metadataCache: { getFirstLinkpathDest: dest, getFileCache: fc, resolvedLinks }, vault: { getAbstractFileByPath: p => F[p] || null, cachedRead: async f => read(f), getMarkdownFiles: () => Object.values(F) }, fileManager: { processFrontMatter: async () => {} } };
const container = document.createElement("div"); document.body.appendChild(container);
const dv = { container, currentFilePath: "Texts/Tantraloka/Tantraloka page.md", el: (tag, text, o) => { const e = mk(o.container, tag, { cls: o.cls, attr: o.attr }); e.innerHTML = "<p>" + String(text).replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '<a class="internal-link">$2</a>') + "</p>"; return e; },
  pages: () => ({ file: { lists: { where: fn => ({ array: () => [] }) } } }) };
const code = fs.readFileSync("/home/claude/view/tantraloka-page/view.js", "utf8");
new Function("dv", "app", "input", "window", `return (async () => {${code}\n})();`)(dv, app, undefined, global.window).then(() => {
  const q = s => [...container.querySelectorAll(s)];
  console.log("errors:", q(".vp-view-error").map(e => e.textContent));
  console.log("buttons:", q(".tl-bar button").map(b => b.textContent + (b.disabled ? "(off)" : "")).join(" | "));
  console.log("head:", q(".tl-head")[0] && q(".tl-head")[0].textContent);
  console.log("mula lines:", q(".tl-mula div").length, "iast:", q(".tl-iast div").length, "tr paras:", q(".tl-tr-para").length);
  console.log("viveka EN paras:", q(".tl-viv-para").length, "notes:", q(".tl-note").length, "pages:", q(".tl-pg").length, "SA:", q(".tl-viv-sa-text").length);
  q(".tl-viv-para").slice(0, 4).forEach(e => console.log("  EN:", e.textContent.slice(0, 160)));
  for (const c of ["tl-left", "tl-right"]) console.log("==", c, q("." + c)[0].textContent.slice(0, 900));
  console.log(require("./navprint.js")(container, "tl"));
  console.log("notices:", q(".tl-notice").map(e => e.textContent));
}).catch(e => console.error("THROWN", e));
