// Homily page: the collect of the day, the readings, the psalm as the Prayer Book prints it and the earlier homilies on the same
// readings, built each time a homily note is shown, from the note's own properties. Nothing is copied into the note: it keeps its
// properties and your writing (Notes, Draft), so a correction to a text reaches every homily at once. 5 Nov 2026, first version
// (Stephen: page above, writing below; the glossed page with JANT notes, the Fathers and parallels is the next step).
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
// draws one reading into a box: groups of verses (an alternative reading starts a group, after its line "*or* Amos 5:18-24"),
// each verse with its number (a link to the verse) and its text, then the reading's lettered notes
const drawVerses = (box, targets) => drawReading(box, [{ lead: null, targets }]);
const drawReading = async (box, groups) => {
  const notes = [], used = {}, missing = [];
  let count = 0;
  for (const g of groups) {
    if (g.lead) md(box, g.lead, "hp-alt");
    const vs = [];
    for (const tg of g.targets) { try { vs.push(...await versesOf(tg)); } catch (e) { missing.push(e.message); } }
    const chapters = new Set(vs.map(v => v.f.path + ":" + v.id.split("-")[0]));
    count += vs.length;
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
