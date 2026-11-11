// Homily page: the collect of the day, the readings, the psalm as the Prayer Book prints it and the earlier homilies on the same
// readings, built each time a homily note is shown, from the note's own properties. Nothing is copied into the note: it keeps its
// properties and your writing (Notes, Draft), so a correction to a text reaches every homily at once. 5 Nov 2026, first version
// (Stephen: page above, writing below). 10 Nov 2026: a closed drawer of glosses under each New Testament reading (JANT, the Fathers and
// Aquinas, Synoptic parallels), option C of the mock-up he chose; see "glosses" below.
// In a note:   await dv.view("Templates/Views/homily-page")
//              await dv.view("Templates/Views/homily-page", { earlier: false })   (without the Earlier homilies table)
// The calling note's properties (written by the Homily templates; you may change them by hand):
//   date       the day preached or planned (YYYY-MM-DD)
//   occasion   the RCL note ("[[Proper-27A]]"), or the Holy Days table for a Holy Day with no RCL note
//   feast      the Holy Day's title, when its collect and readings are used
//   propers    sunday | feast | both (empty: sunday)
// What it shows, with the rules of the Homily template (18-21 Oct 2026):
//   - On a Holy Day: the feast's collect and readings where `propers` says so; with `both`, the Sunday's first, then the feast's.
//     A feast with an RCL note uses it; the others take the Prayer Book's lessons from the Holy Days table.
//   - After Pentecost (Propers 4-29) the complementary track's first reading and psalm (Track 2), which the parish reads.
//   - The readings are read from the verse lists in the RCL note's Readings section (so the Hebrew/English psalm and verse
//     numbering already matched there is kept). Footnotes become lettered notes under each reading; the Greek line of the New
//     Testament (and its apparatus notes) is left out. Each verse number links to its verse (hover shows it).
//   - The psalm in the Prayer Book's own words and numbers (`psalm_bcp` in the RCL note); the Sunday's psalm when a feast replaces
//     only the collect and lessons (BCP p. 16), with the feast's psalm named beside it.
// If a part cannot be built, the part falls back to the old embed and says why; the rest of the page is still drawn.
const VIEW = "homily-page";
const opt = Object.assign({ earlier: true }, typeof input === "undefined" || !input ? {} : input);
const MC = app.metadataCache, V = app.vault;
const me = dv.current();
const myFile = V.getAbstractFileByPath(me.file.path);
const F = (myFile && MC.getFileCache(myFile)?.frontmatter) || {};
const root = dv.container.createDiv({ cls: "hp-page" });
const md = (container, text, cls) => dv.el("div", text, { container, cls });
const say = (where, text, cls) => where.createDiv({ cls: cls || "hp-notice", text });
const fail = (e, where) => {
  console.error(VIEW, e);
  (where || root).createDiv({ cls: "hp-error", text: `${VIEW}: ${e && e.message ? e.message : e}` });
};
const emb = t => "!" + "[" + "[" + t + "]" + "]";
const lnk = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]";
const nameOf = v => String(v ?? "").replace(/^\[\[|\]\]$/g, "").split("|")[0].split("#")[0].trim();
const fileOf = n => n ? MC.getFirstLinkpathDest(n, me.file.path) : null;
const fmOf = n => { const f = fileOf(n); return f ? (MC.getFileCache(f)?.frontmatter ?? {}) : {}; };
const noExt = p => p.replace(/\.md$/, "");

// ---- reading texts
const texts = new Map(), defsOf = new Map();
const textOf = async f => { if (!texts.has(f.path)) texts.set(f.path, await V.cachedRead(f)); return texts.get(f.path); };
const footDefs = async f => {
  if (!defsOf.has(f.path)) { const d = {}; for (const m of (await textOf(f)).matchAll(/^\[\^([^\]]+)\]:[ \t]*(.*)$/gm)) d[m[1]] = m[2]; defsOf.set(f.path, d); }
  return defsOf.get(f.path);
};
// "Revelation 07#^7-16" -> [{ f, id, raw }]; "Psalms 008#Chapter 8" -> every verse block under that heading
const versesOf = async target => {
  const [name, sub] = target.split("#"), f = fileOf(name.trim());
  if (!f) throw new Error(`no note "${name}"`);
  const c = MC.getFileCache(f) || {}, t = await textOf(f), blocks = Object.values(c.blocks || {});
  if (sub && sub.startsWith("^")) {
    const b = (c.blocks || {})[sub.slice(1).toLowerCase()];
    if (!b) throw new Error(`no verse ${sub} in ${f.basename}`);
    return [{ f, id: b.id, raw: t.slice(b.position.start.offset, b.position.end.offset) }];
  }
  let a = 0, e = t.length;
  if (sub) {
    const hs = c.headings || [], k = hs.findIndex(h => h.heading === sub.trim());
    if (k < 0) throw new Error(`no heading "${sub}" in ${f.basename}`);
    a = hs[k].position.start.offset;
    const nx = hs.slice(k + 1).find(h => h.level <= hs[k].level); e = nx ? nx.position.start.offset : t.length;
  }
  return blocks.filter(b => b.position.start.offset >= a && b.position.end.offset <= e && /^\d+-\d+$/.test(b.id))
    .sort((x, y) => x.position.start.offset - y.position.start.offset)
    .map(b => ({ f, id: b.id, raw: t.slice(b.position.start.offset, b.position.end.offset) }));
};
const letters = i => { let s = ""; i++; while (i > 0) { i--; s = String.fromCharCode(97 + (i % 26)) + s; i = Math.floor(i / 26); } return s; };
const foreign = l => { const s = l.replace(/\s/g, "").length; return s > 0 && ((l.match(/[Ͱ-Ͽἀ-῿]/g) || []).length > s / 3 || (l.match(/[֐-׿]/g) || []).length > s / 3); };
const inlineNotes = (t, add) => { // "^[note]" (brackets may nest) -> a marker; the text goes to the notes
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
// ---- glosses (10 Nov 2026, Stephen chose option C of the mock-up): under each New Testament reading a closed drawer holds the JANT
// notes on its verses, the Fathers and Aquinas where they cite them, and the Synoptic parallels, found as New Testament View finds
// them (nt-page). Nothing is drawn when a reading has none (the Old Testament and the psalms have none here yet). Closed on opening;
// a Father's lines are clipped at about 260 characters, with "more" (about 900); an open drawer prints, a closed one does not.
const NT_DIR = "Texts/Bible/New Testament/", NRSV_DIR = "Texts/Bible/NRSVue/", DRB_DIR = "Texts/Bible/Douay-Rheims/";
const JANT_DIR = "Texts/Bible/Jewish Annotated New Testament/Annotations/", LEX_DIR = "Library/Lexicons/Greek NT/", SYN_TABLE = "Texts/Crosswalks/Synoptic parallels.md";
const cmp = (a, b) => a[0] - b[0] || a[1] - b[1];
let bibleIdx = null;
const bibleNote = (dir, book, c) => {   // "Matthew", 25 -> the chapter note in that folder (BSB "Matthew 25", "NRSVue Matthew 25", "DRB …", "JANT …")
  if (!bibleIdx) {
    bibleIdx = {};
    for (const f of V.getMarkdownFiles()) for (const d of [NT_DIR, NRSV_DIR, DRB_DIR, JANT_DIR]) if (f.path.startsWith(d)) {
      const m = f.basename.match(/^(?:NRSVue |DRB |JANT )?(.+?) (\d+)$/); if (m) (bibleIdx[d] = bibleIdx[d] || {})[m[1] + "|" + (+m[2])] = f; break;
    }
  }
  return (bibleIdx[dir] || {})[book + "|" + c] || null;
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
const linksInto = (targets, ids) => {   // links into any of the given notes whose block is one of the verses
  const want = new Set(ids.map(x => x.join("-"))), paths = new Set(targets.filter(Boolean).map(f => f.path)), out = [];
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
const GOSPELS = [["Matthew", "Mt"], ["Mark", "Mk"], ["Luke", "Lk"], ["John", "Jn"]];
const parseCell = text => {        // "Mt 3:1–6, 11–12" -> [{a:[c,v], b:[c,v]}]
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
const synopticRows = async (book, first, last) => {
  const g = GOSPELS.findIndex(x => x[0] === book); if (g < 0) return [];
  const f = V.getAbstractFileByPath(SYN_TABLE); if (!f) return [];
  const rows = []; let cols = null;
  for (const line of (await V.cachedRead(f)).split("\n")) {
    if (!line.trim().startsWith("|")) { if (cols && rows.length) break; continue; }
    const cells = line.trim().split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim());
    if (!cols) { const h = cells.map(s => s.replace(/[*_]/g, "").toLowerCase()); if (["id", "title", "matthew"].every(k => h.includes(k))) cols = h; continue; }
    if (cells.every(c => /^:?-{3,}:?$/.test(c))) continue;
    const cell = n => (cells[cols.indexOf(n)] || "").replace(/\\\|/g, "|");
    const mine = parseCell(cells[cols.indexOf(book.toLowerCase())] || "");
    if (!mine.some(p => cmp(p.b, first) >= 0 && cmp(p.a, last) <= 0)) continue;
    rows.push({ id: cell("id"), title: cell("title"), others: GOSPELS.filter(x => x[0] !== book).map(x => cell(x[0].toLowerCase())).filter(Boolean) });
  }
  return rows;
};
const flabel = f => f.basename.replace(/^Aquinas Summa /, "Summa ").replace(/\bQ0*(\d+)/, "q. $1").replace(/\bHom 0*(\d+)/, "Hom. $1").replace(/ 0+(\d)/g, " $1");
// the glosses of one reading: vs = its verse notes [{ f, id }]
const drawGlosses = async (box, vs) => {
  const per = new Map();
  for (const v of vs) {
    const p = v.f.path; if (!(p.startsWith(NT_DIR) || p.startsWith(NRSV_DIR) || p.startsWith(DRB_DIR))) continue;
    const m = v.f.basename.match(/^(?:NRSVue |DRB )?(.+?) (\d+)$/), cv = v.id.split("-").map(Number);
    if (!m || cv.length !== 2 || cv.some(isNaN)) continue;
    const k = m[1] + "|" + (+m[2]); if (!per.has(k)) per.set(k, { book: m[1], c: +m[2], ids: [] }); per.get(k).ids.push(cv);
  }
  const jant = [], fathers = [], rows = [], jantFiles = [], seenRow = new Set(), seenPar = new Set();
  for (const g of per.values()) {
    const bsb = bibleNote(NT_DIR, g.book, g.c); if (!bsb) continue;          // not a New Testament chapter (the NRSVue also holds the Old)
    const nrsv = bibleNote(NRSV_DIR, g.book, g.c), drb = bibleNote(DRB_DIR, g.book, g.c), jf = bibleNote(JANT_DIR, g.book, g.c);
    const ids = g.ids.sort(cmp), first = ids[0], last = ids[ids.length - 1];
    if (jf) {
      jantFiles.push(jf);
      const jt = (await V.cachedRead(jf)).replace(/^---\n[\s\S]*?\n---\n/, "");
      let sec = null;
      for (const para of jt.split(/\n{2,}/)) {
        const s = para.trim();
        const h = s.match(/^#{2,3}\s+(\d+)\.(\d+)(?:[–-](?:(\d+)\.)?(\d+))?:\s*(.+)$/);
        if (h) { const a = [+h[1], +h[2]], b = h[4] ? [h[3] ? +h[3] : a[0], +h[4]] : a; sec = { a, b, title: `${h[1]}.${h[2]}${h[4] ? "–" + (h[3] ? h[3] + "." : "") + h[4] : ""}: ${h[5]}` }; continue; }
        if (/^#/.test(s) || !s) continue;
        let a, b, body, lab;
        const vn = s.match(/^\*\*\[\[[^\]|#]+#\^(\d+)-(\d+)\|([^\]]+)\]\]:?\*\*:?\s*/);
        if (vn) { a = [+vn[1], +vn[2]]; const r = vn[3].match(/(\d+)\s*[–-]\s*(\d+)$/); b = r ? [a[0], +r[2]] : a; body = s.slice(vn[0].length); lab = vn[3]; }
        else if (sec && /^\*\[\[[^\]]+\]\],?\s*p\.\s*\d+\*/.test(s)) { a = sec.a; b = sec.b; body = s.replace(/^\*\[\[[^\]]+\]\],?\s*p\.\s*\d+\*\s*·\s*/, ""); lab = null; }
        else continue;
        if (cmp(b, first) < 0 || cmp(a, last) > 0) continue;
        jant.push({ head: lab || sec.title, body: body.replace(/\s*\^[\w-]+\s*$/, "") });
      }
    }
    const L = linksInto([bsb, nrsv, drb], ids).filter(l => /^Texts\/(Fathers|Aquinas)\//.test(l.f.path));
    for (const l of L.sort((a, b) => cmp(a.cv, b.cv) || a.off - b.off)) {
      if (fathers.length >= 6) break;
      if (fathers.filter(x => x.l.f === l.f).length >= 2) continue;
      const t = await V.cachedRead(l.f), pa = paraAt(t, l.off), key = l.f.path + "|" + pa.text.slice(0, 60);
      if (seenPar.has(key)) continue; seenPar.add(key);
      fathers.push({ l, q: around(pa.text, pa.at, 260), more: around(pa.text, pa.at, 900) });
    }
    for (const r of await synopticRows(g.book, first, last)) if (!seenRow.has(r.id)) { seenRow.add(r.id); rows.push(r); }
  }
  const parts = [jant.length ? `JANT ${jant.length}` : "", fathers.length ? `Fathers ${fathers.length}` : "", rows.length ? `Parallels ${rows.length}` : ""].filter(Boolean);
  if (!parts.length) return;
  const d = box.createEl("details", { cls: "hp-gl" });
  d.createEl("summary", { text: `Glosses: ${parts.join(" · ")}` });
  const sect = t => { const s = d.createDiv({ cls: "hp-gl-sec" }); s.createDiv({ cls: "hp-gl-title", text: t }); return s; };
  if (jant.length) {
    const s = sect("Jewish Annotated New Testament");
    for (const x of jant) md(s, `<span class="hp-gl-vn">${x.head}</span> ${x.body}`, "hp-gl-item");
    md(s, "From " + jantFiles.map(f => lnk(noExt(f.path), f.basename)).join(" · "), "hp-aside");
  }
  if (fathers.length) {
    const s = sect("The Fathers and Aquinas");
    for (const x of fathers) {
      const it = s.createDiv({ cls: "hp-gl-item" });
      md(it, `<span class="hp-gl-vn">${x.l.cv.join(":")}</span> ${lnk(noExt(x.l.f.path), flabel(x.l.f))}: ${quoted(x.q)}`, "hp-gl-q");
      if (x.more.length > x.q.length + 40) { const m = it.createEl("details", { cls: "hp-gl-more" }); m.createEl("summary", { text: "more" }); md(m, quoted(x.more), "hp-gl-q"); }
    }
  }
  if (rows.length) {
    const s = sect("Parallels");
    for (const r of rows) md(s, `**${r.title}** (row ${r.id})${r.others.length ? "<br>" + r.others.join("<br>") : ""}`, "hp-gl-item");
    md(s, "From " + lnk(noExt(SYN_TABLE), "Synoptic parallels"), "hp-aside");
  }
};
// draws one reading into a box: groups of verses (an alternative reading starts a group, after its line "*or* Amos 5:18-24"),
// each verse with its number (a link to the verse) and its text, then the reading's lettered notes
const drawVerses = (box, targets) => drawReading(box, [{ lead: null, targets }]);
const drawReading = async (box, groups) => {
  const notes = [], used = {}, missing = [], allv = [];
  let count = 0;
  for (const g of groups) {
    if (g.lead) md(box, g.lead, "hp-alt");
    const vs = [];
    for (const tg of g.targets) { try { vs.push(...await versesOf(tg)); } catch (e) { missing.push(e.message); } }
    const chapters = new Set(vs.map(v => v.f.path + ":" + v.id.split("-")[0]));
    count += vs.length; allv.push(...vs);
    for (const v of vs) {
      const defs = await footDefs(v.f);
      let lines = v.raw.replace(/\s*\^[\w-]+\s*$/, "").split("\n");
      const lab = (lines[0].match(/^\*\*(\d+:\d+)\*\*\s*/) || [])[1];
      if (lab) lines[0] = lines[0].replace(/^\*\*\d+:\d+\*\*\s*/, "");
      let t = lines.filter(l => !foreign(l)).join("\n").replace(/\s+$/, "");
      t = t.replace(/\[\^([^\]]+)\]/g, (m, n) => { const k = v.f.path + "|" + n; if (!(k in used)) { used[k] = notes.length; notes.push(defs[n] || "(note text not found)"); } return `<sup class="hp-fn">${letters(used[k])}</sup>`; });
      t = inlineNotes(t, x => { notes.push(x); return `<sup class="hp-fn">${letters(notes.length - 1)}</sup>`; });
      const num = lab ? (chapters.size > 1 ? lab : lab.split(":")[1]) : v.id.replace("-", ":");
      md(box.createDiv({ cls: "hp-verse" }), `<span class="hp-vn">${lnk(noExt(v.f.path) + "#^" + v.id, num)}</span> ${t.replace(/ {2}\n/g, "<br>").replace(/\n/g, " ")}`, "hp-verse-text");
    }
  }
  if (notes.length) { const nb = box.createDiv({ cls: "hp-notes" }); notes.forEach((n, k) => md(nb, `<sup>${letters(k)}</sup> ${n}`, "hp-note")); }
  if (missing.length) say(box, `Not shown: ${missing.join("; ")}.`);
  try { await drawGlosses(box, allv); } catch (e) { fail(e, box); }
  return count;
};
// the plain text of a block (a collect)
const blockText = async target => {
  const [name, sub] = target.split("#"), f = fileOf(name.trim()), b = f && sub ? (MC.getFileCache(f)?.blocks || {})[sub.replace(/^\^/, "").toLowerCase()] : null;
  if (!b) return null;
  return (await textOf(f)).slice(b.position.start.offset, b.position.end.offset).replace(/\s*\^[\w-]+\s*$/, "");
};

// ---- the RCL note's readings: [{ title, groups: [{ lead, targets }] }], by its own headings; a line between the embeds
// ("*or* **[[Amos 5#^5-18|Amos 5:18-24]]**") starts the next group
const rclReadings = async (occ, track2) => {
  const f = fileOf(occ); if (!f) throw new Error(`no lectionary note "${occ}"`);
  const t = await textOf(f), hs = MC.getFileCache(f)?.headings || [];
  const sec = h => { const k = hs.indexOf(h), nx = hs.slice(k + 1).find(x => x.level <= h.level); return t.slice(h.position.end.offset, nx ? nx.position.start.offset : t.length); };
  const groupsOf = s => {
    const gs = [{ lead: null, targets: [] }];
    for (const l of s.split("\n")) {
      const m = l.trim().match(/^!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]$/);
      if (m) gs[gs.length - 1].targets.push(m[1]);
      else if (l.trim() && !l.startsWith(">")) { const g = gs[gs.length - 1]; if (g.targets.length || g.lead) gs.push({ lead: l.trim(), targets: [] }); else g.lead = l.trim(); }
    }
    return gs;
  };
  const readH = hs.find(h => h.level === 2 && h.heading === "Readings");
  const about = readH ? (sec(readH).match(/^(?:>.*\n?)+/m) || [""])[0].trim() : "";
  let picked;
  if (track2) {
    const find = p => hs.find(h => h.level === 3 && h.heading.startsWith(p));
    picked = [find("First reading (complementary)"), find("Psalm (complementary)"), find("Second reading"), find("Gospel")];
    if (!picked.every(Boolean)) throw new Error(`${occ}: the complementary track's headings were not all found`);
  } else {
    if (!readH) throw new Error(`${occ}: no Readings section`);
    const k = hs.indexOf(readH), nx = hs.slice(k + 1).findIndex(h => h.level <= 2);
    picked = hs.slice(k + 1, nx < 0 ? hs.length : k + 1 + nx).filter(h => h.level === 3);
  }
  return { file: f, about, list: picked.map(h => ({ title: h.heading, groups: groupsOf(sec(h)) })) };
};

// ---- the Prayer Book psalm (as the Homily template did): "Psalm 90:1-6, 13-17" or "Psalm 23" -> verse targets
const bcpPsalm = n => `BCP Psalm ${String(n).padStart(3, "0")}`;
const psalmParts = s => String(s ?? "").split(/ or | and /).map(p => p.trim().replace(/^(?=\d+(?::|$))/, "Psalm ")).filter(p => /^Psalm \d/.test(p));
const bcpTargets = c => {
  const m = c.match(/^Psalm (\d+)(?::(.+))?$/), f = m ? fileOf(bcpPsalm(+m[1])) : null;
  if (!f) return [];
  const range = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a + i);
  const vs = m[2] ? m[2].split(",").flatMap(p => { const r = p.replace(/[\s()]/g, "").match(/^(\d+)[a-c]?(?:-(\d+)[a-c]?)?$/); return r ? range(+r[1], +(r[2] || r[1])) : []; })
    : range(1, +(MC.getFileCache(f)?.frontmatter?.verses || 0));
  return vs.map(v => `${f.basename}#^${+m[1]}-${v}`);
};
const t2 = f => f && f.first_reading_complementary ? Object.assign({}, f, { first_reading: f.first_reading_complementary, psalm: f.psalm_complementary, psalm_bcp: f.psalm_bcp_complementary, track2: true }) : f;
const collectsOf = f => [].concat(f.collect ?? []).filter(Boolean).map(s => String(s).replace(/^!?\[\[|\]\]$/g, "").split("|")[0]);

// ---- the study plan's Sunday for a date (for the psalm when a feast replaces only the Sunday's collect and lessons)
const planSunday = async iso => {
  if (!iso || moment(iso).day() !== 0) return null;
  const split = l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim().replace(/\\\|/g, "|"));
  for (const f of V.getMarkdownFiles().filter(f => f.path.startsWith("Texts/Tantraloka/Study plan/"))) {
    const line = (await V.cachedRead(f)).split("\n").find(l => l.startsWith(`| ${iso} |`));
    if (line) { const ls = [...(split(line)[6] || "").matchAll(/\[\[([^\]|]+)/g)].map(x => x[1]); return ls[ls.length - 1] || null; }
  }
  return null;
};

try {
  const iso = String(F.date ?? "").slice(0, 10);
  const occName = nameOf(F.occasion);
  const use = /^(feast|both)$/.test(String(F.propers ?? "")) ? String(F.propers) : "sunday";
  let hd = null;
  if (use !== "sunday" || occName === "Holy Days (BCP 1979)") {
    try {
      const hs = await V.adapter.read("Templates/Views/holyday/view.js");
      hd = await new Function(hs.split("// ---- CORE " + "BEGIN")[1].split("// ---- CORE " + "END")[0].replace(/^[^\n]*\n/, "") + "\nreturn HD;")().load(app);
    } catch (e) { fail(new Error("the Holy Days could not be read: " + (e && e.message ? e.message : e))); }
  }
  const info = hd && /^\d{4}-\d{2}-\d{2}$/.test(iso) ? hd.info(iso) : null;
  const feastC = use !== "sunday" && info ? info.cand : null;
  const isTable = !!hd && occName === hd.TABLE;
  if (!occName) say(root, "This homily has no occasion yet: set the occasion property to the Sunday's or feast's lectionary note.");
  // the parts, as the Homily template makes them: the Sunday's (or the day's) and the feast's; "both" gives the Sunday's first
  const parts = [];
  if (use === "sunday" || !feastC) { if (occName && !isTable) parts.push({ sunday: use === "sunday", occ: occName, fm: use === "sunday" ? t2(fmOf(occName)) : fmOf(occName), title: "" }); }
  else if (use === "feast") parts.push({ sunday: false, occ: isTable ? null : occName, bcp: isTable, fm: isTable ? {} : fmOf(occName), title: feastC.title });
  else {
    const ls = feastC.meta ? hd.rclLinks(feastC.meta.rcl) : [], y = hd.rclYear(hd.DO.parseISO(iso)), ok = n => !/Special/.test(n);
    const rclFeast = ls.find(n => n.endsWith(y) && ok(n)) || ls.find(n => !/[ABC]$/.test(n) && ok(n)) || ls.find(ok) || null;
    parts.push({ sunday: true, occ: occName, fm: t2(fmOf(occName)), title: "" });
    parts.push({ sunday: false, occ: rclFeast, bcp: !rclFeast, fm: rclFeast ? fmOf(rclFeast) : {}, title: feastC.title });
  }
  if (use !== "sunday" && !feastC) say(root, `propers is "${use}", but no Holy Day was found for ${iso || "this date"}; the occasion's own readings are shown.`);
  const two = parts.length > 1;
  const h2 = t => root.createEl("h2", { cls: "hp-h2", text: t });

  for (const p of parts) {
    const tag = two ? `: ${p.sunday ? "the Sunday" : p.title}` : "";
    // the collect
    try {
      if (p.bcp) {
        h2(`Collect of the day${tag}`);
        const tx = await blockText(`${hd.CONT}#^${feastC.meta.anchor}`);
        md(root, (tx ?? emb(`${hd.CONT}#^${feastC.meta.anchor}`)) + (feastC.meta.preface ? `\n\n*${feastC.meta.preface}*` : "") +
          `\n\n*In traditional language:* ${lnk(`${hd.TRAD}#^${feastC.meta.anchor}`, "the collect, traditional")}`, "hp-collect");
      } else {
        const cs = collectsOf(p.fm);
        if (cs.length) {
          h2(`Collect of the day${tag}`);
          const out = [];
          for (const c of cs) out.push((await blockText(c)) ?? emb(c));
          md(root, out.join("\n\n*or this*\n\n") + `\n\n${cs.map(c => lnk(c, "source")).join(" · ")}`, "hp-collect");
        }
      }
    } catch (e) { fail(e); }
    // the readings
    h2(`Readings${tag}`);
    try {
      if (p.bcp) {
        const dash = s => s.replace(/--/g, "–");
        for (const l of hd.lessonsOf(feastC.meta.lessons, 0)) {
          const box = root.createDiv({ cls: "hp-reading" });
          box.createEl("h3", { cls: "hp-h3", text: dash(l.label) });
          const groups = [], miss = [];
          l.alts.forEach((a, k) => {
            const r = hd.verseEmbeds(a);
            const lead = l.alts.length > 1 ? (k ? "*or* " : "") + `*${dash(a.label)}*` : null;
            groups.push({ lead: r.embeds.length || !a.target ? lead : (lead ? lead + " · " : "") + lnk(a.target, dash(a.label)), targets: r.embeds });
            if (r.missing.length) miss.push(`${dash(a.label)}: ${r.missing.join(", ")}`);
          });
          await drawReading(box, groups);
          if (miss.length) say(box, `Not shown as text (no verse note): ${miss.join("; ")}.`);
        }
        if (hd.setsOf(feastC.meta.lessons).length > 1) md(root, `*The Prayer Book gives a second set: ${hd.lessonsOf(feastC.meta.lessons, 1).map(x => x.label).join("; ")}.*`, "hp-aside");
      } else if (p.occ) {
        const track2 = p.sunday && !!p.fm.track2;
        try {
          const R = await rclReadings(p.occ, track2);
          if (track2) md(root, "*The complementary track (Track 2), as read after Pentecost.*", "hp-aside");
          if (R.about) md(root, R.about, "hp-about");
          for (const r of R.list) {
            const box = root.createDiv({ cls: "hp-reading" });
            box.createEl("h3", { cls: "hp-h3", text: r.title.replace(/ \(complementary\)/, "") });
            await drawReading(box, r.groups);
          }
          md(root, `From ${lnk(noExt(R.file.path), R.file.basename)}.`, "hp-aside");
        } catch (e) { fail(e); md(root, emb(`${p.occ}#Readings`), "hp-fallback"); }
      }
    } catch (e) { fail(e); }
  }

  // the psalm: the feast's own where the feast has the day; the Sunday's where only the collect and lessons are substituted (BCP p. 16)
  try {
    const sundayPart = parts.find(p => p.sunday), feastPart = parts.find(p => !p.sunday);
    const sundayOcc = !sundayPart && feastPart && info && ["optional", "after"].includes(info.kind) ? await planSunday(iso) : null;
    const keepSunday = !!sundayPart || !!sundayOcc;
    const feastPsalm = c => { const first = hd.plain(c.meta.psalm).split(" or ")[0].trim(); return { psalm: first, psalm_bcp: first }; };
    const pf = sundayPart ? sundayPart.fm : sundayOcc ? t2(fmOf(sundayOcc)) : feastPart && feastPart.bcp ? feastPsalm(feastC) : feastPart ? feastPart.fm : {};
    const list = pf.psalm_bcp ? psalmParts(pf.psalm_bcp) : psalmParts(pf.psalm).every(x => /^Psalm \d+$/.test(x)) ? psalmParts(pf.psalm) : [];
    const shown = list.map(x => [x, bcpTargets(x)]).filter(x => x[1].length);
    if (shown.length || psalmParts(pf.psalm).length) {
      h2(`Psalm in the Prayer Book${feastPart && keepSunday ? " (the Sunday's)" : ""}`);
      if (shown.length) for (const [x, tg] of shown) { const box = root.createDiv({ cls: "hp-reading hp-psalm" }); box.createEl("h3", { cls: "hp-h3", text: x }); await drawVerses(box, tg); }
      else md(root, `The lectionary gives ${pf.psalm} in the verse numbers of English Bibles; the Prayer Book numbers some psalms differently. ` +
        psalmParts(pf.psalm).map(x => lnk(bcpPsalm(+x.match(/\d+/)[0]), x.replace(/:.*/, "") + " in the Prayer Book")).join(" · "), "hp-aside");
      if (feastPart && keepSunday && feastC && feastC.meta) md(root, `The feast's psalm in the Prayer Book: ${hd.setsOf(feastC.meta.psalm).filter((x, i, a) => a.indexOf(x) === i).join(" *or* ")}`, "hp-aside");
    }
  } catch (e) { fail(e); }

  // the earlier homilies on the same readings (the same feast only)
  if (opt.earlier) {
    try {
      h2("Earlier homilies on these readings");
      const base = l => String(l?.path ?? l ?? "").split("/").pop().replace(/\.md$/, "");
      const hs = dv.pages('"' + me.file.folder + '"').where(p => p.file.path !== me.file.path && p.occasion && base(p.occasion) === base(me.occasion) && String(p.feast ?? "") === String(me.feast ?? "")).sort(p => p.date, "desc");
      if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
      else md(root, "None yet. These readings come round again in three years.", "hp-aside");
    } catch (e) { fail(e); }
  }
} catch (e) { fail(e); }
