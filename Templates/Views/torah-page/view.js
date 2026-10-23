// Torah page: a passage of the Torah (or of the Prophets and Writings) laid out like a page of a Mikraot Gedolot, from the
// vault's JPS notes and what links to them. 22 Oct 2026, from the mock-up Stephen approved (canvas "Page views: Torah, NT,
// Tantrāloka").
// In a note:   await dv.view("Templates/Views/torah-page")
// The calling note's properties:
//   ref    where the passage starts: "Genesis 1:1", "Gen 1", "Isaiah 53:4", "Ps 23", or a parashah's name ("Noach").
//          Empty: the portion of the coming Shabbat (Calendar/Parashot 2026-2029 (diaspora).md), from its first verse.
//          "Genesis 1:1-12" also sets the length.
//   span   how many verses to show (empty: 8).
// The box and the buttons change these properties (processFrontMatter) and draw the page again.
// What it shows, all read when the note is shown (nothing is copied into the calling note):
//   centre        the verses (JPS 1985) with the translators' notes, and the chapter's Compare links (NRSVue, LXX,
//                 Douay-Rheims)
//   inner column  Rashi on these verses (Torah only)
//   left margin   the daf sides of the Talmud whose Torah Or names these verses (one line quoted), the Mishneh Torah
//                 chapters and Kitzur chapters whose Verses box names them
//   outer column  the Hasidic texts and the Zohar on these verses, quoted where they cite them, then every other note
//                 that links them ("Cited by")
//   right margin  the haftarah (Torah), the Guide for the Perplexed on these verses, and your own question::, claim::,
//                 connects::, answer:: and cites:: lines that link them ("Glosses")
// Narrow screens: view.css puts the columns under the text.
const VIEW = "torah-page";
const opt = Object.assign({}, typeof input === "undefined" || !input ? {} : input);
const MC = app.metadataCache, V = app.vault;
const PARASHOT = "Calendar/Parashot 2026-2029 (diaspora).md";
const TORAH_DIR = "Texts/Bible/Torah/", RASHI_DIR = "Texts/Bible/Torah/Rashi/", TANAKH_DIR = "Texts/Bible/Tanakh/";
const GLOSS_DIRS = ["Journal/", "Study/", "Projects/", "Notes/"];
const SPAN = 8;

const root = opt.container ? opt.container : (() => {
  const el = dv.container.createDiv({ attr: { "data-tr-view": VIEW } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-tr-view") === VIEW);
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
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

// --- The books: the Torah by parashah notes (frontmatter book, parasha, range), the rest by chapter notes
const TORAH_BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"];
const parseCV = s => { const m = String(s || "").match(/(\d+):(\d+)/); return m ? [+m[1], +m[2]] : null; };
const cmp = (a, b) => a[0] - b[0] || a[1] - b[1];
const index = (() => {
  const torah = [], tanakh = {}, order = [], bookOfPath = {};
  for (const f of V.getMarkdownFiles()) {
    if (f.path.startsWith(TORAH_DIR) && !f.path.startsWith(RASHI_DIR)) {
      const fm = fmOf(f); if (!fm.parasha_number || !fm.book || !fm.range) continue;
      const [a, b] = String(fm.range).split(/[–-]/);
      const s = parseCV(a), e0 = parseCV(b) || (b && s ? [s[0], +b.match(/\d+/)[0]] : null);
      if (s && e0) torah.push({ f, book: fm.book, num: +fm.parasha_number, parasha: fm.parasha || "", s, e: e0 });
    } else if (f.path.startsWith(TANAKH_DIR)) {
      const m = f.basename.match(/^(.+?) (\d+)$/); if (!m) continue;
      (tanakh[m[1]] = tanakh[m[1]] || {})[+m[2]] = f; bookOfPath[f.path] = m[1];
    }
  }
  torah.sort((x, y) => x.num - y.num);
  for (const b of TORAH_BOOKS) order.push(b);
  // the Prophets and Writings in the order of the folders (JPS)
  for (const f of V.getMarkdownFiles().filter(f => f.path.startsWith(TANAKH_DIR)).sort((a, b) => a.path.localeCompare(b.path))) {
    const m = f.basename.match(/^(.+?) (\d+)$/); if (m && !order.includes(m[1])) order.push(m[1]);
  }
  return { torah, tanakh, books: order, bookOfPath };
})();
const ABBR = { gen: "Genesis", ge: "Genesis", gn: "Genesis", ex: "Exodus", exod: "Exodus", lev: "Leviticus", lv: "Leviticus", num: "Numbers", nm: "Numbers",
  deut: "Deuteronomy", dt: "Deuteronomy", josh: "Joshua", judg: "Judges", jdg: "Judges", isa: "Isaiah", is: "Isaiah", jer: "Jeremiah", ezek: "Ezekiel",
  ez: "Ezekiel", hos: "Hosea", obad: "Obadiah", mic: "Micah", nah: "Nahum", hab: "Habakkuk", zeph: "Zephaniah", hag: "Haggai", zech: "Zechariah",
  mal: "Malachi", ps: "Psalms", psa: "Psalms", psalm: "Psalms", prov: "Proverbs", pr: "Proverbs", eccl: "Ecclesiastes", qoh: "Ecclesiastes",
  qoheleth: "Ecclesiastes", song: "Song of Songs", cant: "Song of Songs", sos: "Song of Songs", songofsolomon: "Song of Songs", lam: "Lamentations",
  esth: "Esther", dan: "Daniel", neh: "Nehemiah", jon: "Jonah" };
const bookOf = raw => {
  let s = String(raw || "").trim().toLowerCase().replace(/\./g, "");
  let num = ""; const nm = s.match(/^(1|2|i|ii|first|second)\s*(.+)$/);
  if (nm && /^(sam|kg|ki|chr|ch)/.test(nm[2])) { num = /^(2|ii|second)$/.test(nm[1]) ? "II " : "I "; s = nm[2]; }
  const flat = s.replace(/[^a-z]/g, "");
  if (num) { const base = /^sam/.test(flat) ? "Samuel" : /^(kg|ki)/.test(flat) ? "Kings" : "Chronicles"; return index.books.includes(num + base) ? num + base : null; }
  if (ABBR[flat]) return ABBR[flat];
  const hit = index.books.filter(b => b.toLowerCase().replace(/[^a-z]/g, "").startsWith(flat));
  return flat.length >= 2 && hit.length === 1 ? hit[0] : (hit.find(b => b.toLowerCase().replace(/[^a-z]/g, "") === flat) || null);
};
// a parashah's name in any common spelling (as homily-parashah reads it)
const pkey = s => String(s).toLowerCase().replace(/^.*?\b(parashat|parshat)\s+/, "").replace(/^torah \d+ - /, "")
  .replace(/[\s-]+le(kh|ch|k)a$/, "").replace(/q/g, "k").replace(/kh/g, "h").replace(/ch/g, "h").replace(/tz/g, "ts")
  .replace(/[^a-z]/g, "").replace(/(.)\1+/g, "$1").replace(/[aeiou]/g, "").replace(/h$/, "");

// "Genesis 1:1", "Gen 1", "Genesis 1:1-12", "Noach" -> { book, c, v, span }
const parse = t => {
  const s = String(t || "").trim().replace(/\s+/g, " "); if (!s) return null;
  const m = s.match(/^(.+?)\s+(\d+)(?:\s*[:.]\s*(\d+))?(?:\s*[-–]\s*(\d+))?$/);
  if (m) { const book = bookOf(m[1]); if (book) { const v = m[3] ? +m[3] : 1; return { book, c: +m[2], v, span: m[4] && m[3] ? Math.max(1, +m[4] - v + 1) : null }; } }
  const p = index.torah.find(x => pkey(x.parasha) === pkey(s) || pkey(x.f.basename) === pkey(s));
  return p ? { book: p.book, c: p.s[0], v: p.s[1], span: null } : null;
};
// the note that holds a verse, and its verses in order (block ids "c-v")
const noteFor = (book, c, v) => {
  if (TORAH_BOOKS.includes(book)) { const t = index.torah.find(x => x.book === book && cmp(x.s, [c, v]) <= 0 && cmp([c, v], x.e) <= 0); return t ? t.f : null; }
  return (index.tanakh[book] || {})[c] || null;
};
const versesOf = f => Object.values((MC.getFileCache(f) || {}).blocks || {}).filter(b => /^\d+-\d+$/.test(b.id))
  .sort((a, b) => a.position.start.offset - b.position.start.offset).map(b => b.id.split("-").map(Number));
// the notes of a book in reading order (for the arrows)
const notesOf = book => TORAH_BOOKS.includes(book) ? index.torah.filter(x => x.book === book).map(x => x.f)
  : Object.keys(index.tanakh[book] || {}).map(Number).sort((a, b) => a - b).map(c => index.tanakh[book][c]);

// the coming Shabbat's portion (or the next one when a festival reading replaces it)
const thisWeek = async notices => {
  const f = V.getAbstractFileByPath(PARASHOT); if (!f) return null;
  const d = window.moment ? window.moment().format("YYYY-MM-DD") : new Date().toISOString().slice(0, 10);
  const rows = (await V.cachedRead(f)).split("\n").filter(l => /^\| \d{4}-\d\d-\d\d \|/.test(l)).map(l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim()));
  let skipped = null;
  for (const r of rows.filter(r => r[0] >= d)) {
    const m = (r[2] || "").match(/\[\[([^\]\\|]+)/);
    if (!m) { skipped = skipped || r; continue; }
    if (skipped && notices) notices.push(`Shabbat ${skipped[0]} has the festival reading (${skipped[1].replace(/[()]/g, "").replace(/^.*?:\s*/, "")}); shown is the next portion, read on ${r[0]}.`);
    const t = index.torah.find(x => x.f.basename === m[1].trim());
    return t ? { book: t.book, c: t.s[0], v: t.s[1], span: null, shabbat: r[0], name: r[1] } : null;
  }
  return null;
};


// --- The list of books, parashot and chapters above the page (23 Oct 2026, Stephen's request), like the table of contents on
// Sefaria: small, each name a link that draws the page there. Open or folded as last left on this device (localStorage).
// The order of the Prophets and the Writings is the order of the Tanakh index note's headings.
const TANAKH_INDEX = "Texts/Bible/Tanakh/Tanakh.md";
const tanakhOrder = async () => {
  const f = V.getAbstractFileByPath(TANAKH_INDEX); const out = { Prophets: [], Writings: [] }; if (!f) return out;
  let sec = null;
  for (const l of (await V.cachedRead(f)).split("\n")) {
    const h2 = l.match(/^## (.+?)\s*$/); if (h2) { sec = out[h2[1]] ? h2[1] : null; continue; }
    const h3 = l.match(/^### (.+?)\s*$/); if (h3 && sec && index.tanakh[h3[1]]) out[sec].push(h3[1]);
  }
  return out;
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
const torahNav = async (host, p, file, first, last) => {
  const order = await tanakhOrder();
  const rows = [{ label: "Torah", items: TORAH_BOOKS.map(b => ({ text: b, ref: `${b} 1:1`, on: b === p.book })) },
    { label: "Prophets", items: order.Prophets.map(b => ({ text: b, ref: `${b} 1:1`, on: b === p.book })) },
    { label: "Writings", items: order.Writings.map(b => ({ text: b, ref: `${b} 1:1`, on: b === p.book })) }];
  let chs = [];
  if (TORAH_BOOKS.includes(p.book)) {
    const ps = index.torah.filter(x => x.book === p.book);
    rows.push({ label: "Parashot", items: ps.map(x => ({ text: x.parasha, ref: `${x.book} ${x.s[0]}:${x.s[1]}`, on: x.f === file, title: `Parashat ${x.parasha}, ${x.book} ${x.s[0]}:${x.s[1]}–${x.e[0]}:${x.e[1]}` })) });
    if (ps.length) for (let c = Math.min(...ps.map(x => x.s[0])); c <= Math.max(...ps.map(x => x.e[0])); c++) chs.push(c);
  } else chs = Object.keys(index.tanakh[p.book] || {}).map(Number).sort((a, b) => a - b);
  rows.push({ label: "Chapters", grid: true, items: chs.map(c => ({ text: String(c), ref: `${p.book} ${c}:1`, on: !!first && c >= first[0] && c <= last[0], title: `${p.book} ${c}` })) });
  navBanner(host, "tr", `Books, parashot and chapters · ${p.book}`, rows, r => save({ ref: r }));
};

// --- Reading notes
// the paragraph that ends with a block id
const blockText = (text, id) => {
  const m = text.match(new RegExp(`(?:^|\\n\\n)((?:(?!\\n\\n)[\\s\\S])*?) \\^${esc(id)}(?:\\n|$)`));
  return m ? m[1] : null;
};
const letters = i => { let s = ""; i++; while (i > 0) { i--; s = String.fromCharCode(97 + (i % 26)) + s; i = Math.floor(i / 26); } return s; };
const footDefs = text => { const o = {}; for (const m of text.matchAll(/^\[\^(\d+)\]:\s*(.+)$/gm)) o[m[1]] = m[2]; return o; };
// shorten at a sentence or clause, never leaving a link or emphasis open
const balance = s => { if ((s.match(/\*\*/g) || []).length % 2) s += "**"; if ((s.replace(/\*\*/g, "").match(/\*/g) || []).length % 2) s += "*"; return s; };
const clip = (t, max) => {
  if (!max || t.length <= max) return t;
  let s = t.slice(0, max);
  const cut = Math.max(s.lastIndexOf(". "), s.lastIndexOf("; "), s.lastIndexOf(": "));
  s = cut > max * 0.5 ? s.slice(0, cut + 1) : s.replace(/\s\S*$/, "");
  const open = s.lastIndexOf("[["); if (open > s.lastIndexOf("]]")) s = s.slice(0, open);
  return balance(s.trimEnd()) + " …";
};
// plain-ish text for a quotation: links shown by their label, notes and block ids removed
const plainLinks = s => s.replace(/\[\[([^\]|]*?)\|([^\]]*?)\]\]/g, "$2").replace(/\[\[([^\]]*?)\]\]/g, (m, a) => a.split("#")[0].split("/").pop())
  .replace(/\[\^\d+\]/g, "").replace(/\^\[[^\]]*\]/g, "").replace(/ \^[\w-]+$/gm, "").replace(/\s+/g, " ").trim();
// the words around a position in a paragraph: from the sentence start before it, about max characters
const around = (par, at, max) => {
  let a = Math.max(0, at - Math.floor(max * 0.55));
  if (a > 0) { const lo = Math.max(0, a - 80), m = par.slice(lo, Math.max(lo, at - 40)).match(/[.!?;:]["”’)]?\s+/); a = m ? lo + m.index + m[0].length : par.indexOf(" ", a) + 1; }
  let s = par.slice(a);
  // emphasis opened before the cut stays open
  const pre = par.slice(0, a), bold = (pre.match(/\*\*/g) || []).length % 2, ital = (pre.replace(/\*\*/g, "").match(/\*/g) || []).length % 2;
  // never start inside a link
  const o = s.indexOf("]]"), c = s.indexOf("[["); if (o >= 0 && (c < 0 || o < c)) s = s.slice(o + 2);
  return (a > 0 ? "… " : "") + clip((bold ? "**" : "") + (ital ? "*" : "") + plainLinks(s).trim(), max);
};
// the paragraph around a position in a note's text; a line that only lists the verses ("**Torah:** [[…]], [[…]]") points
// to the paragraph before it
const paraAt = (text, off) => {
  const s = text.lastIndexOf("\n\n", off), e = text.indexOf("\n\n", off);
  let a = s < 0 ? 0 : s + 2, b = e < 0 ? text.length : e;
  let p = text.slice(a, b);
  if (/^\s*(?:\*\*[^*]+:\*\*|>)/.test(p) && (p.replace(/\[\[[^\]]*\]\]/g, "").replace(/[\s,;·*:>A-Za-z]/g, "").length < 4 || /^\*\*Torah:\*\*/.test(p))) {
    const s2 = text.lastIndexOf("\n\n", a - 3); const prev = text.slice(s2 < 0 ? 0 : s2 + 2, a - 2);
    if (prev && !/^#/.test(prev.trim())) return { text: prev, at: Math.floor(prev.length / 2), moved: true };
  }
  return { text: p, at: off - a, moved: false };
};

// --- Who links these verses: every link into the passage's note whose block is one of its verses
const linksInto = (file, ids) => {
  const want = new Set(ids.map(x => x.join("-")));
  const out = [];
  for (const [src, tg] of Object.entries(MC.resolvedLinks)) {
    if (!tg[file.path] || src === file.path) continue;
    const sf = V.getAbstractFileByPath(src); if (!sf) continue;
    const c = MC.getFileCache(sf) || {};
    for (const l of [...(c.links || []), ...(c.embeds || [])]) {
      const [p, sub] = l.link.split("#");
      if (!sub || !sub.startsWith("^") || !want.has(sub.slice(1))) continue;
      if (MC.getFirstLinkpathDest(p, src) !== file) continue;
      out.push({ f: sf, id: sub.slice(1), cv: sub.slice(1).split("-").map(Number), off: l.position.start.offset, line: l.position.start.line });
    }
  }
  return out;
};
const sideAt = (f, off) => { const hs = ((MC.getFileCache(f) || {}).headings || []).filter(h => h.level === 2 && h.position.start.offset < off); return hs.length ? hs[hs.length - 1].heading : null; };
const vlist = (cvs, oneChapter) => {
  const xs = [...new Set(cvs.map(x => x.join(":")))].map(s => s.split(":").map(Number)).sort(cmp);
  const lab = x => oneChapter ? String(x[1]) : `${x[0]}:${x[1]}`;
  const out = []; let run = null;
  for (const x of xs) { if (run && run.b[0] === x[0] && run.b[1] + 1 === x[1]) run.b = x; else { run = { a: x, b: x }; out.push(run); } }
  return out.map(r => cmp(r.a, r.b) ? `${lab(r.a)}–${r.b[1]}` : lab(r.a)).join(", ");
};

const draw = async (want, span, notices) => {
  const token = root.__trToken = (root.__trToken || 0) + 1; const stale = () => root.__trToken !== token;
  root.empty();
  const wrap = root.createDiv({ cls: "tr-wrap" });
  notices = [...(notices || [])];
  let p = parse(want);
  if (!p && String(want || "").trim()) notices.push(`“${String(want).trim()}” is not a verse or a parashah (write it as “Genesis 1:1” or “Noach”), so this is the coming Shabbat’s portion.`);
  if (!p) p = await thisWeek(notices);
  if (!p) p = { book: "Genesis", c: 1, v: 1 };
  if (p.span) span = p.span;
  span = Math.max(1, Math.min(60, +span || SPAN));
  const file = noteFor(p.book, p.c, p.v);

  // the bar
  const bar = wrap.createDiv({ cls: "tr-bar" });
  const box = bar.createEl("input", { cls: "tr-input", attr: { type: "text", value: `${p.book} ${p.c}:${p.v}`, "aria-label": "Verse or parashah, e.g. Genesis 1:1 or Noach", placeholder: "Genesis 1:1" } });
  const go = bar.createEl("button", { text: "Go", attr: { type: "button" } });
  go.addEventListener("click", () => save({ ref: box.value })); box.addEventListener("keydown", ev => { if (ev.key === "Enter") save({ ref: box.value }); });
  const navs = bar.createDiv({ cls: "tr-navs" });
  const tw = bar.createEl("button", { text: "This week’s portion", attr: { type: "button" } }); tw.addEventListener("click", () => save({ ref: "" }));
  const sp = bar.createEl("select", { cls: "tr-span", attr: { "aria-label": "Verses shown" } });
  for (const n of [4, 8, 12, 20, 30]) { const o = sp.createEl("option", { text: `${n} verses`, attr: { value: String(n) } }); if (n === span) o.selected = true; }
  if (![4, 8, 12, 20, 30].includes(span)) { const o = sp.createEl("option", { text: `${span} verses`, attr: { value: String(span) } }); o.selected = true; }
  sp.addEventListener("change", () => save({ span: sp.value }));
  for (const n of notices) wrap.createDiv({ cls: "tr-notice", text: n });
  const navHost = wrap.createDiv({ cls: "tr-nav-host" });
  if (!file) { await torahNav(navHost, p, null, null, null); fail(new Error(`there is no note in the vault for ${p.book} ${p.c}:${p.v}`), wrap); return; }

  // the passage: span verses from the one asked for, inside its note
  const all = versesOf(file);
  let i0 = all.findIndex(x => x[0] === p.c && x[1] === p.v);
  if (i0 < 0) { notices.push(`${p.book} ${p.c}:${p.v} is not in ${file.basename}; showing its first verse.`); i0 = 0; }
  const ids = all.slice(i0, i0 + span);
  const first = ids[0], last = ids[ids.length - 1];
  const oneChapter = first[0] === last[0];
  // the arrows: the passage before and after (into the neighbouring note at either end)
  const sib = notesOf(p.book), si = sib.indexOf(file);
  const startOf = (f, idx) => { const vs = versesOf(f); const x = vs[Math.max(0, Math.min(vs.length - 1, idx < 0 ? vs.length + idx : idx))]; return x ? `${p.book} ${x[0]}:${x[1]}` : null; };
  const prevRef = i0 > 0 ? `${p.book} ${all[Math.max(0, i0 - span)][0]}:${all[Math.max(0, i0 - span)][1]}` : (si > 0 ? startOf(sib[si - 1], -span) : null);
  const nextRef = i0 + span < all.length ? `${p.book} ${all[i0 + span][0]}:${all[i0 + span][1]}` : (si >= 0 && si + 1 < sib.length ? startOf(sib[si + 1], 0) : null);
  for (const [r, t] of [[prevRef, "← earlier"], [nextRef, "later →"]]) {
    const b = navs.createEl("button", { text: t, attr: { type: "button", "aria-label": r || t } });
    if (!r) b.disabled = true; else b.addEventListener("click", () => save({ ref: r }));
  }
  for (const n of notices.slice(wrap.querySelectorAll(".tr-notice").length)) navHost.before(wrap.createDiv({ cls: "tr-notice", text: n }));
  await torahNav(navHost, p, file, first, last); if (stale()) return;

  const text = await V.cachedRead(file); if (stale()) return;
  const fm = fmOf(file);
  const isTorah = TORAH_BOOKS.includes(p.book);
  const tnote = isTorah ? index.torah.find(x => x.f === file) : null;

  // running head
  const head = wrap.createDiv({ cls: "tr-head" });
  const hl = head.createDiv({ cls: "tr-head-left" });
  hl.createDiv({ cls: "tr-num", text: oneChapter ? `${first[0]}:${first[1]}${ids.length > 1 ? "–" + last[1] : ""}` : `${first[0]}:${first[1]}–${last[0]}:${last[1]}` });
  hl.createDiv({ cls: "tr-book", text: p.book });
  const hc = head.createDiv({ cls: "tr-head-centre" });
  hc.createDiv({ cls: "tr-sub", text: isTorah ? `Torah · ${p.book} · Parashah ${tnote.num}` : `${fm.section || "Tanakh"} · ${p.book}` });
  md(hc, isTorah ? linkTo(file, null, `Parashat ${tnote.parasha}`) : linkTo(file, null, file.basename), "tr-title");

  const grid = wrap.createDiv({ cls: "tr-grid" });
  const left = grid.createDiv({ cls: "tr-margin tr-left" }), inner = grid.createDiv({ cls: "tr-inner" }), centre = grid.createDiv({ cls: "tr-centre" });
  const outer = grid.createDiv({ cls: "tr-outer" }), right = grid.createDiv({ cls: "tr-margin tr-right" });
  const titled = (where, title, cls) => { const b = where.createDiv({ cls: "tr-box " + (cls || "") }); b.createDiv({ cls: "tr-box-title", text: title }); return b; };

  // centre: the verses
  const defs = footDefs(text); const used = [];
  let chap = null;
  for (const [c, v] of ids) {
    if (c !== chap) { centre.createDiv({ cls: "tr-chapter", text: `Chapter ${c}` }); chap = c; }
    let t = blockText(text, `${c}-${v}`) || "";
    t = t.replace(/^\*\*\d+:\d+\*\*\s*/, "").replace(/\[\^(\d+)\]/g, (m, n) => { if (!used.includes(n)) used.push(n); return `<sup class="tr-fn">${letters(used.indexOf(n))}</sup>`; });
    const d = centre.createDiv({ cls: "tr-verse" });
    md(d, `<span class="tr-vn">${oneChapter ? v : c + ":" + v}</span> ${t.replace(/ {2}\n/g, "<br>")}`, "tr-verse-text");
  }
  if (used.length) {
    const fb = centre.createDiv({ cls: "tr-notes" });
    used.forEach((n, k) => md(fb, `<sup>${letters(k)}</sup> ${defs[n] || ""}`, "tr-note"));
  }
  // compare: the chapter's line in the note, and the LXX and Douay-Rheims chapter where the book's name and numbering agree
  const cmpLine = isTorah ? (text.match(new RegExp(`^## Chapter ${first[0]}\\s*\\n+(Compare:[^\\n]*)`, "m")) || [])[1] : (text.match(/^Compare:[^\n]*/m) || [])[0];
  const extra = [];
  if (p.book !== "Psalms") {
    for (const [dir, lab] of [["Texts/Bible/LXX/", "LXX"], ["Texts/Bible/Douay-Rheims/", "Douay-Rheims"]]) {
      const f = V.getMarkdownFiles().find(f => f.path.startsWith(dir) && (fmOf(f).english_book || fmOf(f).book) === p.book && +fmOf(f).chapter === first[0]);
      if (f) extra.push(linkTo(f, `^${first[0]}-${first[1]}`, lab));
    }
  }
  if (cmpLine || extra.length) md(centre.createDiv({ cls: "tr-compare" }), `${cmpLine ? cmpLine.replace(/\s*$/, "") : "Compare:"}${extra.length ? " · " + extra.join(" · ") : ""}`, "tr-compare-text");

  // inner column: Rashi (Torah only)
  inner.createDiv({ cls: "tr-col-title", text: "Rashi" });
  if (!isTorah) inner.createDiv({ cls: "tr-empty", text: "Rashi’s commentary in this vault is on the Torah only." });
  else {
    const rf = V.getMarkdownFiles().find(f => f.path.startsWith(RASHI_DIR) && +fmOf(f).parasha_number === tnote.num);
    if (!rf) inner.createDiv({ cls: "tr-empty", text: "No Rashi note for this parashah." });
    else {
      const rt = await V.cachedRead(rf); if (stale()) return;
      let any = false;
      for (const [c, v] of ids) {
        const m = rt.match(new RegExp(`^### ${c}:${v}\\s*\\n([\\s\\S]*?)(?=^#{2,3} |(?![\\s\\S]))`, "m"));
        if (!m) continue;
        const paras = m[1].split(/\n{2,}/).map(x => x.trim()).filter(x => x && !/^\[\[[^\]]+\]\]$/.test(x));
        paras.forEach((x, k) => {
          const d = inner.createDiv({ cls: "tr-rashi" });
          md(d, `${k ? "" : `<span class="tr-vn">${oneChapter ? v : c + ":" + v}</span> `}${clip(x.replace(/\[\^\d+\]/g, ""), 420)}`, "tr-quote-text");
        });
        any = true;
      }
      if (!any) inner.createDiv({ cls: "tr-empty", text: "Rashi has no comment on these verses." });
      md(inner, `${fmOf(rf).translation || "Rashi"}, from ${linkTo(rf, null, rf.basename)}`, "tr-src");
    }
  }
  // no Rashi on this page (the Prophets and Writings, or verses he does not comment on): his column narrows (23 Oct 2026)
  if (!inner.querySelector(".tr-rashi")) grid.classList.add("tr-norashi");

  // who links these verses
  const L = linksInto(file, ids);
  const rashiPath = isTorah ? (V.getMarkdownFiles().find(f => f.path.startsWith(RASHI_DIR) && +fmOf(f).parasha_number === tnote.num) || {}).path : null;
  const cat = l => { const s = l.f.path;
    if (s === rashiPath || s.startsWith("Texts/Bible/NRSVue/") || s.startsWith("Texts/Bible/LXX/") || s.startsWith("Texts/Bible/Douay-Rheims/") || s.startsWith(TORAH_DIR) || s.startsWith(TANAKH_DIR)) return "bible";
    if (s.startsWith("AI/")) return "skip";
    if (GLOSS_DIRS.some(d => s.startsWith(d))) return "gloss";
    if (s.startsWith("Texts/Talmud/")) return "talmud";
    if (s.startsWith("Texts/Maimonides/Mishneh Torah/")) return "mt";
    if (s.startsWith("Texts/Maimonides/Guide for the Perplexed/")) return "guide";
    if (s.startsWith("Texts/Kitzur Shulchan Arukh/")) return "kitzur";
    if (s.startsWith("Texts/Chasidut/") || s.startsWith("Texts/Zohar/")) return "hz";
    return "other"; };
  const by = {}; for (const l of L) (by[cat(l)] = by[cat(l)] || []).push(l);
  const group = (ls, keyf) => { const g = new Map(); for (const l of ls) { const k = keyf(l); if (!g.has(k)) g.set(k, []); g.get(k).push(l); } return [...g.entries()]; };
  const firstCv = ls => ls.map(l => l.cv).sort(cmp)[0];

  // left margin: the Talmud (with one line quoted), the Mishneh Torah, the Kitzur
  const tb = titled(left, "In the Talmud", "tr-talmud");
  const nv = ls => new Set(ls.map(l => l.id)).size;
  const daf = group(by.talmud || [], l => `${l.f.path}|${sideAt(l.f, l.off) || ""}`).sort((a, b) => cmp(firstCv(a[1]), firstCv(b[1])) || nv(b[1]) - nv(a[1]));
  if (!daf.length) tb.createDiv({ cls: "tr-empty", text: "No daf names these verses in its Torah Or." });
  for (const [k, ls] of daf.slice(0, 10)) { const side = k.split("|")[1]; md(tb, `${linkTo(ls[0].f, side || null, ls[0].f.basename.replace(/ (\d+)$/, ` $1${side ? side.replace(/^\d+/, "") : ""}`))} · ${vlist(ls.map(l => l.cv), oneChapter)}`, "tr-item"); }
  if (daf.length > 10) tb.createDiv({ cls: "tr-empty", text: `and ${daf.length - 10} more dapim` });
  if (daf.length) {
    // the first daf's line: the Torah Or entry says which lines quote the verse
    const [k, ls] = daf[0]; const side = k.split("|")[1];
    const dt = await V.cachedRead(ls[0].f); if (stale()) return;
    const ln = (dt.split("\n")[ls[0].line] || "").match(/\(lines? (\d+)/);
    if (side && ln) {
      const q = blockText(dt, `${side}-${ln[1]}`);
      if (q) { const d = left.createDiv({ cls: "tr-dafquote" }); d.createDiv({ cls: "tr-box-title", text: `${ls[0].f.basename.replace(/ \d+$/, "")} ${side}:${ln[1]}` }); md(d, clip(plainLinks(q), 300), "tr-quote-text"); }
    }
  }
  const halakhah = (title, ls, label, cls) => {
    const b = titled(left, title, cls);
    const g = group(ls, l => l.f.path).sort((a, c) => cmp(firstCv(a[1]), firstCv(c[1])));
    for (const [, xs] of g.slice(0, 10)) md(b, `${linkTo(xs[0].f, null, label(xs[0].f))} · ${vlist(xs.map(l => l.cv), oneChapter)}`, "tr-item");
    if (g.length > 10) b.createDiv({ cls: "tr-empty", text: `and ${g.length - 10} more` });
  };
  if ((by.mt || []).length) halakhah("Mishneh Torah", by.mt, f => f.basename.replace(/^Mishneh Torah - /, "").replace(/ 0*(\d+)$/, " $1"), "tr-mt");
  if ((by.kitzur || []).length) halakhah("Kitzur Shulchan Arukh", by.kitzur, f => f.basename.replace(/^Kitzur Shulchan Arukh 0*/, "Chapter "), "tr-kitzur");

  // outer column: the Hasidic texts and the Zohar, quoted where they cite these verses; the portion's own first
  const hz = by.hz || [];
  outer.createDiv({ cls: "tr-col-title", text: "Hasidut and Zohar" });
  const own = f => isTorah && pkey(f.basename).includes(pkey(tnote.parasha));
  const rank = l => (own(l.f) ? 0 : 2) + (l.f.path.startsWith("Texts/Chasidut/") ? 0 : 1);
  const picks = [], seenPara = new Set();
  for (const l of [...hz].sort((a, b) => rank(a) - rank(b) || cmp(a.cv, b.cv) || a.off - b.off)) {
    if (picks.length >= 10) break;
    if (picks.filter(x => x.l.f === l.f).length >= 2) continue;
    const t = await V.cachedRead(l.f); if (stale()) return;
    const pa = paraAt(t, l.off); const key = l.f.path + "|" + pa.text.slice(0, 60);
    if (seenPara.has(key)) continue; seenPara.add(key);
    picks.push({ l, q: pa.moved ? clip(plainLinks(pa.text), 280) : around(pa.text, pa.at, 280) });
  }
  picks.sort((a, b) => cmp(a.l.cv, b.l.cv));
  if (!picks.length) outer.createDiv({ cls: "tr-empty", text: "No Hasidic text or Zohar note cites these verses." });
  const label = f => f.basename.replace(/ \d+ - /, ", ").replace(/ - /g, ", ").replace(/ 0+(\d)/g, " $1");
  const quoted = q => /^(?:… )?\**[“"‘]/.test(q) ? q : `“${q}”`;
  for (const x of picks) md(outer.createDiv({ cls: "tr-quote" }), `<span class="tr-vn">${oneChapter ? x.l.cv[1] : x.l.cv.join(":")}</span> ${linkTo(x.l.f, null, label(x.l.f))}: ${quoted(x.q)}`, "tr-quote-text");
  if (hz.length) {
    const work = s => { const ps = s.split("/"); return ps[1] === "Zohar" ? (ps[2] === "Sefaria" ? ps[3] : "Zohar") : ps[2]; };
    const works = group(hz, l => work(l.f.path));
    md(outer, `All that cite these verses: ${works.map(([w, ls]) => `${w} (${new Set(ls.map(l => l.f.path)).size})`).join(" · ")}`, "tr-src");
  }
  // your own lines (question::, claim::, connects::, answer::, cites::) that link these verses
  const want2 = new Set(ids.map(x => x.join("-")));
  const re = new RegExp(`\\[\\[(?:[^\\]|#]*/)?${esc(file.basename)}(?:#\\^([\\d-]+))?(?:\\|[^\\]]*)?\\]\\]`, "g");
  const glossFiles = Object.entries(MC.resolvedLinks).filter(([s, tg]) => tg[file.path] && GLOSS_DIRS.some(d => s.startsWith(d))).map(([s]) => s);
  const lines = [];
  for (const s of glossFiles) {
    const f = V.getAbstractFileByPath(s); if (!f) continue;
    for (const l of (await V.cachedRead(f)).split("\n")) {
      if (!/^\s*- (?!\[.\])(question|claim|connects|answer|cites)::\s*\S/.test(l)) continue;
      const hits = [...l.matchAll(re)]; if (hits.some(h => !h[1] || want2.has(h[1]))) lines.push({ f, l: l.replace(/^\s*-\s*/, "") });
    }
    if (stale()) return;
  }
  // cited by: every other note, by book or folder
  const cb = titled(outer, "Cited by", "tr-cited");
  // notes in the gloss folders that link these verses without a question::/claim:: line count here too
  const glossed = new Set(lines.map(g => g.f.path));
  const others = [...(by.other || []), ...(by.gloss || []).filter(l => !glossed.has(l.f.path))];
  if (!others.length) cb.createDiv({ cls: "tr-empty", text: "No other note links these verses." });
  const shelf = s => { const ps = s.replace(/\.md$/, "").split("/"), base = ps[ps.length - 1];
    if (ps[0] === "Texts") return ps[1] === "Bible" ? ps[2] : ps.length === 3 ? base : ps[1];
    if (ps[0] === "Library") return ps.length >= 4 ? ps[2] : base;
    if (ps[0] === "Projects" || ps[0] === "Journal") return ps.length > 2 ? ps[1] === "AI" ? base : (ps[0] === "Journal" ? "Journal" : ps[1]) : base;
    return ps.length > 2 ? ps[1] : base; };
  const shelves = group(others, l => shelf(l.f.path)).sort((a, b) => new Set(b[1].map(l => l.f.path)).size - new Set(a[1].map(l => l.f.path)).size);
  for (const [s, ls] of shelves.slice(0, 14)) { const n = new Set(ls.map(l => l.f.path)).size; md(cb, `${linkTo(ls[0].f, null, s)}${n > 1 ? ` (${n} notes)` : ""} · ${vlist(ls.map(l => l.cv), oneChapter)}`, "tr-item"); }
  if (shelves.length > 14) cb.createDiv({ cls: "tr-empty", text: `and ${shelves.length - 14} more books` });

  // right margin: haftarah, the Guide, glosses
  if (isTorah) {
    const hb = titled(right, "Haftarah", "tr-haftarah");
    const hs = (text.match(/^## Haftarah\s*\n([\s\S]*?)(?=^## |(?![\s\S]))/m) || [])[1];
    if (hs) for (const l of hs.split("\n").filter(l => /^- /.test(l))) md(hb, l.slice(2), "tr-item"); else hb.createDiv({ cls: "tr-empty", text: "—" });
  }
  else {
    // the parashot whose haftarah (in their ## Haftarah list) covers these verses
    const hits = [];
    for (const t of index.torah) {
      const tt = await V.cachedRead(t.f); if (stale()) return;
      const hs = (tt.match(/^## Haftarah\s*\n([\s\S]*?)(?=^## |(?![\s\S]))/m) || [])[1] || "";
      for (const line of hs.split("\n").filter(l => /^- /.test(l))) {
        const who = (line.match(/^- \*\*([^*]+?):?\*\*/) || [])[1];
        for (const m of line.matchAll(/\[\[([^\]#|]+)#\^(\d+)-(\d+)\|([^\]]+)\]\]/g)) {
          const tf = MC.getFirstLinkpathDest(m[1], t.f.path); if (!tf || index.bookOfPath[tf.path] !== p.book) continue;
          const a = [+m[2], +m[3]], r = m[4].match(/(\d+):(\d+)(?:\s*[–-]\s*(?:(\d+):)?(\d+))?\s*$/);
          const b = r ? [r[3] ? +r[3] : a[0], r[4] ? +r[4] : a[1]] : a;
          if (cmp(b, first) < 0 || cmp(a, last) > 0) continue;
          hits.push({ t, who: (who || "").replace(/:$/, ""), lab: m[4] });
        }
      }
    }
    if (hits.length) {
      const hb = titled(right, "Read as haftarah", "tr-haftarah");
      for (const h of hits) md(hb, `${linkTo(h.t.f, "Haftarah", h.t.parasha)}${h.who ? ` (${h.who})` : ""} · ${h.lab}`, "tr-item");
    }
  }
  const gb = titled(right, "The Guide", "tr-guide");
  const gs = group(by.guide || [], l => l.f.path).sort((a, b) => cmp(firstCv(a[1]), firstCv(b[1])));
  if (!gs.length) gb.createDiv({ cls: "tr-empty", text: "The Guide for the Perplexed does not cite these verses." });
  for (const [, ls] of gs.slice(0, 6)) {
    md(gb, `${linkTo(ls[0].f, null, ls[0].f.basename.replace(/^Guide for the Perplexed /, ""))} · ${vlist(ls.map(l => l.cv), oneChapter)}`, "tr-item");
    if (gs.indexOf(gs.find(g => g[1] === ls)) < 2) { const t = await V.cachedRead(ls[0].f); if (stale()) return; const pa = paraAt(t, ls[0].off); md(gb, `“${around(pa.text, pa.at, 200)}”`, "tr-gquote"); }
  }
  if (gs.length > 6) gb.createDiv({ cls: "tr-empty", text: `and ${gs.length - 6} more chapters` });
  const gl = titled(right, "Glosses", "tr-gloss");
  if (!lines.length) gl.createDiv({ cls: "tr-empty", text: "Your question::, claim:: and connects:: lines that link these verses show here." });
  for (const g of lines) md(gl, `${g.l} — ${linkTo(g.f, null, g.f.basename)}`, "tr-item");

  md(wrap.createDiv({ cls: "tr-foot" }), `${fm.translator || fm.translation || ""}${fm.license ? `, ${fm.license}` : ""}${isTorah ? " · Rashi: Metsudah (Davis), CC BY" : ""} · margins: the notes that link these verses · [[${isTorah ? "Torah" : "Tanakh"}]]`, "tr-foot-text");
};

const here = dv.currentFilePath ? V.getAbstractFileByPath(dv.currentFilePath) : null;
const props = () => (here && (MC.getFileCache(here) || {}).frontmatter) || {};
const save = async ch => {
  try {
    const cur = props();
    const ref = "ref" in ch ? String(ch.ref || "").trim() : (opt.ref !== undefined ? opt.ref : (cur.ref || ""));
    let span = "span" in ch ? ch.span : (opt.span || cur.span);
    const pp = parse(ref); if ("ref" in ch && pp && pp.span) span = pp.span;
    const refOut = pp && pp.span ? `${pp.book} ${pp.c}:${pp.v}` : ref;
    if (here && opt.ref === undefined) await app.fileManager.processFrontMatter(here, fm => { fm.ref = refOut; fm.span = span ? +span : ""; });
    await draw(refOut, span, []);
  } catch (e) { fail(e); }
};
try {
  const cur = props();
  await draw(opt.ref !== undefined ? opt.ref : cur.ref, opt.span || cur.span, []);
} catch (e) { fail(e); }
