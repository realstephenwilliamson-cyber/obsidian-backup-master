<%*
// ================================================================================================================
// HOMILY (POLYPHONIC) TEMPLATE — read me (for Stephen; 21 Oct 2026)
// What it makes: a homily note that sets the Sunday's or feast's readings beside the week's parashah with Rashi, Mei
//   HaShiloach and the Zohar (drawn by the view Templates/Views/homily-parashah from the note's parashah property): the
//   occasion box, the collect, the readings, the Prayer Book's psalm, a box of fixed links (patristic and canonical echoes),
//   headings for your notes on each reading, and a Homiletical Draft section. It names and files itself:
//   "<date> <occasion> (polyphonic)" in the homilies folder.
// When it runs: the command "Templater: Create new note from template" → Homily (Polyphonic), from anywhere (a new note
//   made directly in Projects/Homilies gets the ordinary Homily template instead). It asks for the Sunday or feast and the
//   date unless the note's name begins with a date in the study plan. Opening this file does nothing. After Pentecost
//   (Propers 4–29) it takes the complementary track's first reading and psalm, which is what the parish reads (T24, 21 Oct 2026).
// What you may edit: the links in the "Patristic & Canonical Echoes" box, the reading headings and the draft section (the
//   quoted strings after `out +=` below); the two tags it sets (homily, liturgy) are yours.
// Don't rename: the properties type, date, occasion, feast, propers, rcl_year, readings, parashah, stage, preached_at — the
//   Homily list Base, the RCL notes' lists and the parashah view read them.
// To test an edit: run the command, pick any Sunday and a future date, read the note, delete it through Obsidian. A typo
//   makes Templater show an error and leave the note empty; the previous version of this file is in
//   .work/backup-orient-2026-10-21/Templates/ and in Sync's version history.
// ================================================================================================================
// Homily (Polyphonic): a Sunday's or feast's readings beside the week's parashah, Rashi, Mei HaShiloach and the Zohar.
// Use it with Templater's "Create new note from template" (a note made directly in Writing/Homilies gets the ordinary
// Homily template). If the new note's title starts with a date in the study plan, the occasion and the parashah come
// from that day's row; otherwise it asks for the occasion and the date. The note is then named
// "<date> <occasion> (polyphonic)" and filed in Writing/Homilies. The parashah texts are found from the note's
// `parashah` property each time the note is shown, so you can change it by hand.
// Rebuilt 6 Oct 2026 (phase 1 of the October plan): the old version built links to paths that do not exist.
// Changed 18 Oct 2026 (Holy Days): the same choice as in the Homily template between the Sunday's collect and readings and a Holy Day's
// (Calendar/Holy Days (BCP 1979), BCP p. 16; All Saints on the Sunday after November 1, p. 15); the choice is kept in the note
// "Holy Days - my choices" and in this note's properties `feast` and `propers`.
const dir = "Texts/Tantraloka/Study plan/";
const split = l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim().replace(/\\\|/g, "|"));
const links = s => [...(s || "").matchAll(/\[\[([^\]|]+)/g)].map(x => x[1]);
const feastOf = cell => ((cell || "").match(/(?<!\*)\*\[\[([^\]|]+)/) || [])[1] || null;
const SUNDAY_FEAST = /^(All-Saints|Christmas|Epiphany|Holy-Name|Presentation|Transfiguration)/;
const rowFor = async d => {
  for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith(dir))) {
    const line = (await app.vault.read(f)).split("\n").find(l => l.startsWith(`| ${d} |`));
    if (line) return split(line);
  }
  return null;
};
let date = (tp.file.title.match(/^(\d{4}-\d{2}-\d{2})/) || [])[1];
let occ = null, sundayOcc = null, row = date ? await rowFor(date) : null;
if (row) {
  const ls = links(row[6]), feast = feastOf(row[6]);
  if (moment(date).day() === 0) { sundayOcc = ls[ls.length - 1]; occ = feast && SUNDAY_FEAST.test(feast) ? feast : ls[ls.length - 1]; }
  else occ = feast || ls[ls.length - 1];
}
// The Holy Days (18 Oct 2026)
let hd = null, feastC = null, use = "sunday", rclFeast = null, bcpFeast = false, hdKind = null;
try {
  const hs = await app.vault.adapter.read("Templates/Views/holyday/view.js");
  hd = await new Function(hs.split("// ---- CORE " + "BEGIN")[1].split("// ---- CORE " + "END")[0].replace(/^[^\n]*\n/, "") + "\nreturn HD;")().load(app);
} catch (e) { console.error("Homily (Polyphonic): Holy Days", e); }
if (hd && date) {
  const i = hd.info(date);
  if (i.cand) {
    feastC = i.cand; use = i.use; hdKind = i.kind;
    const ls = i.cand.meta ? hd.rclLinks(i.cand.meta.rcl) : [], y = hd.rclYear(hd.DO.parseISO(date)), ok = n => !/Special/.test(n);
    rclFeast = occ && ls.includes(occ) ? occ : (ls.find(n => n.endsWith(y) && ok(n)) || ls.find(n => !/[ABC]$/.test(n) && ok(n)) || ls.find(ok) || null);
    if (i.canSwitch && !i.choice) {
      const t = i.cand.title, S = ["sunday", "The Sunday's readings and collect"], F = ["feast", `${t}: its readings and collect`], B = ["both", "Both: the Sunday's, then the feast's"];
      const pick = await tp.system.suggester(o => o[1], i.kind === "by-right" ? [F, S, B] : [S, F, B], false, `${t} falls on this Sunday. Which readings and collect?`);
      if (pick) { use = pick[0]; await hd.setChoice(date, t, use); }
    }
    if (use === "feast") { occ = rclFeast; bcpFeast = !rclFeast; }
  }
}
if (!occ && !bcpFeast) {
  const files = app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Texts/RCL/Lectionary/RCL/") && !/RCL Index/.test(f.basename))
    .sort((a, b) => a.path.localeCompare(b.path));
  const pick = await tp.system.suggester(f => `${f.parent.name}: ${f.basename.replace(/-/g, " ")}`, files, false, "Which Sunday or feast?");
  occ = pick ? pick.basename : "";
  if (!date) { date = await tp.system.prompt("Date preached or planned (YYYY-MM-DD)", moment().add((7 - moment().day()) % 7, "days").format("YYYY-MM-DD")); row = date ? await rowFor(date) : null; }
}
const parashah = row ? links(row[5])[0] : null;
const fmOf = n => { const f = n ? app.metadataCache.getFirstLinkpathDest(n, "") : null; return f ? (app.metadataCache.getFileCache(f)?.frontmatter ?? {}) : {}; };
const occFile = occ ? app.metadataCache.getFirstLinkpathDest(occ, "") : null;
// Track 2 (21 Oct 2026, T24): after Pentecost the parish reads the complementary track (the bulletins of 23 Aug, 27 Sep and 11 Oct 2026),
// so where the lectionary note offers one (`first_reading_complementary`; Propers 4–29) the Sunday's first reading and psalm are the
// complementary ones, by the note's own headings; the second reading and gospel are the same in both tracks. A feast's readings are not
// affected. No `psalm_bcp_complementary` exists yet, so a part of a psalm shows as a link to the Prayer Book psalm until one is added.
const t2 = f => f && f.first_reading_complementary ? Object.assign({}, f, { first_reading: f.first_reading_complementary, psalm: f.psalm_complementary, psalm_bcp: f.psalm_bcp_complementary, track2: true }) : f;
const track2Embeds = n => { // the four sections, each by the lectionary note's own heading
  const f = n ? app.metadataCache.getFirstLinkpathDest(n, "") : null; if (!f) return null;
  const hs = (app.metadataCache.getFileCache(f)?.headings ?? []).map(h => h.heading), find = p => hs.find(h => h.startsWith(p));
  const h = [find("First reading (complementary)"), find("Psalm (complementary)"), find("Second reading"), find("Gospel")];
  return h.every(Boolean) ? h.map(x => emb(`${n}#${x}`)).join("\n") : null;
};
const fm = t2(fmOf(occ));
const year = /^Year [ABC]$/.test(occFile?.parent?.name ?? "") ? occFile.parent.name.slice(-1) : "";
const base = year && occ.endsWith(year) ? occ.slice(0, -1) : occ;
const label = bcpFeast ? feastC.title : (base || "Homily").replace(/-/g, " ") + (year ? (/\d$/.test(base) ? year : ` (${year})`) : "");
const feastFm = use !== "sunday" && rclFeast ? fmOf(rclFeast) : null;
const feastLessons = use !== "sunday" && feastC && !rclFeast && feastC.meta ? hd.lessonsOf(feastC.meta.lessons, 0) : [];
const readings = [...["first_reading", "psalm", "second_reading", "gospel"].map(k => fm[k]), ...(use === "both" && feastFm ? ["first_reading", "psalm", "second_reading", "gospel"].map(k => feastFm[k]) : []), ...feastLessons.map(l => l.label)].filter(Boolean);
const q = s => `"${String(s).replace(/"/g, '\\"')}"`;
const wl = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]"; // a wikilink, written so that Obsidian does not list this template's placeholders as unresolved
// The collect of the day and the psalm as the Prayer Book prints it (phase 3 of the October plan), from the lectionary
// note's `collect` (links to the collects in the BCP 1979's "03 The Collects") and `psalm_bcp` (the psalm in the Prayer
// Book's own verse numbers). Without `psalm_bcp` a whole psalm is still shown (it needs no renumbering); part of a psalm gets a link.
const emb = t => "!" + "[" + "[" + t + "]" + "]"; // an embed, written so that this template shows no unresolved link
const lnk = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]";
const collectsOf = f => [].concat(f.collect ?? []).filter(Boolean).map(s => String(s).replace(/^!?\[\[|\]\]$/g, "").split("|")[0]);
const bcpPsalm = n => `BCP Psalm ${String(n).padStart(3, "0")}`;
const psalmParts = s => String(s ?? "").split(/ or | and /).map(p => p.trim().replace(/^(?=\d+(?::|$))/, "Psalm ")).filter(p => /^Psalm \d/.test(p));
const bcpVerses = c => { // "Psalm 90:1-6, 13-17" or "Psalm 23" -> one embed per verse; a half verse (35b) or an optional part ("(19-22)") shows whole verses
  const m = c.match(/^Psalm (\d+)(?::(.+))?$/);
  const f = m ? app.metadataCache.getFirstLinkpathDest(bcpPsalm(+m[1]), "") : null;
  if (!f) return "";
  const range = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a + i);
  const vs = m[2] ? m[2].split(",").flatMap(p => { const r = p.replace(/[\s()]/g, "").match(/^(\d+)[a-c]?(?:-(\d+)[a-c]?)?$/); return r ? range(+r[1], +(r[2] || r[1])) : []; })
    : range(1, +(app.metadataCache.getFileCache(f)?.frontmatter?.verses || 0));
  return vs.map(v => emb(`${f.basename}#^${+m[1]}-${v}`)).join("\n");
};
const psalmOf = f => {
  const psalmBcp = f.psalm_bcp ? psalmParts(f.psalm_bcp) : psalmParts(f.psalm).every(p => /^Psalm \d+$/.test(p)) ? psalmParts(f.psalm) : [];
  let out = psalmBcp.map(p => [p, bcpVerses(p)]).filter(x => x[1]).map(([p, e]) => `#### ${p}\n\n${e}\n\n`).join("");
  if (!out && psalmParts(f.psalm).length) out = `The lectionary gives ${f.psalm} in the verse numbers of English Bibles; the Prayer Book numbers some psalms differently. ` +
    psalmParts(f.psalm).map(p => lnk(bcpPsalm(+p.match(/\d+/)[0]), p.replace(/:.*/, "") + " in the Prayer Book")).join(" · ") + "\n\n";
  return out;
};
// The Prayer Book's own collect, lessons and psalm for a Holy Day with no RCL note (from the Holy Days table)
const bcpCollect = c => emb(`${hd.CONT}#^${c.meta.anchor}`) + (c.meta.preface ? `\n\n*${c.meta.preface}*` : "") + `\n\n*In traditional language:* ` + lnk(`${hd.TRAD}#^${c.meta.anchor}`, "the collect, traditional") + "\n\n";
const bcpReadings = c => {
  let s = ""; const miss = [];
  for (const l of hd.lessonsOf(c.meta.lessons, 0)) {
    s += `### ${l.label}\n\n`;
    for (const a of l.alts) {
      if (l.alts.length > 1) s += `*${a.label}*\n\n`;
      const r = hd.verseEmbeds(a);
      s += r.embeds.length ? r.embeds.map(emb).join("\n") + "\n\n" : (a.target ? lnk(a.target, a.label) + "\n\n" : "");
      if (r.missing.length) miss.push(`${a.label}: ${r.missing.join(", ")}`);
    }
  }
  if (hd.setsOf(c.meta.lessons).length > 1) s += `*The Prayer Book gives a second set: ${hd.lessonsOf(c.meta.lessons, 1).map(x => x.label).join("; ")}.*\n\n`;
  return s + (miss.length ? `*Not shown as text (no verse note): ${miss.join("; ")}.*\n\n` : "");
};
const feastPsalmFm = c => { const first = hd.plain(c.meta.psalm).split(" or ")[0].trim(); return { psalm: first, psalm_bcp: first }; };
// the parts: the Sunday's (or the day's) and the feast's; "both" gives the Sunday's first
const parts = [];
if (use !== "feast" || !feastC) parts.push({ sunday: true, occ, fm, title: "" });
if (use !== "sunday" && feastC) parts.push({ sunday: false, occ: rclFeast, fm: feastFm || {}, title: feastC.title, bcp: !rclFeast });
const two = parts.length > 1;
const sundayPart = parts.find(p => p.sunday), feastPart = parts.find(p => !p.sunday);
const keepSunday = !!sundayPart || (feastPart && sundayOcc && ["optional", "after"].includes(hdKind));
const psalmFm = sundayPart ? sundayPart.fm : keepSunday ? t2(fmOf(sundayOcc)) : feastPart && feastPart.bcp ? feastPsalmFm(feastC) : feastPart ? feastPart.fm : {};
const psalmOut = psalmOf(psalmFm);
let out = ["---", "cssclasses:", "  - manuscript", "type: homily", "stage: drafting", `occasion: ${bcpFeast ? q(lnk(hd.TABLE)) : occ ? q(wl(occ)) : '""'}`,
  ...(feastC && use !== "sunday" ? [`feast: ${q(feastC.title)}`, `propers: ${use}`] : []),
  `date: ${date || ""}`, `rcl_year: ${q(bcpFeast ? hd.rclYear(hd.DO.parseISO(date)) : fm.cycle ?? year)}`,
  readings.length ? "readings:\n" + readings.map(r => "  - " + q(r)).join("\n") : "readings: []",
  `parashah: ${parashah ? q(wl(parashah)) : '""'}`, 'preached_at: ""', "tags:", "  - homily", "  - liturgy", "---", ""].join("\n");
out += `# Homily: ${label}\n\n`;
out += "> [!abstract] Liturgical Context & Occasion\n";
const occLinks = parts.map(p => p.bcp ? lnk(hd.TABLE, p.title) : p.occ ? wl(p.occ, p.sunday ? label : p.title || p.occ) : "(not set)").join(" and ");
const readLinks = parts.map(p => p.bcp ? lnk(hd.TABLE, `${p.title}: the Prayer Book's lessons`) : p.occ ? wl(p.occ + "#Readings", "Full RCL Lectionary Texts") : "(set the occasion)").join(" · ");
out += `> **Date:** ${date ? moment(date).format("D MMMM YYYY") : ""} · **Sunday / Feast:** ${occLinks}\n`;
out += `> **Eucharistic Readings:** ${readLinks}\n\n---\n\n`;
out += "## The Polyphonic Matrix (Concurrent Traditions)\n\n### Concurrent Shabbat Parashah\n\n```dataviewjs\nawait dv.view(\"Templates/Views/homily-parashah\")\n```\n\n";
out += "> [!hermeneutics]+ Patristic & Canonical Echoes\n";
out += "> - **Johannine Patristics:** [[Augustine - Tractates on John|Augustine's Tractates]] · [[Catena Aurea on John - page map|Aquinas (Catena Aurea)]]\n";
out += "> - **Psalter Crosswalk:** [[Texts/Crosswalks/Psalms numbering|Psalms Numbering Crosswalk]] · [[BCP - Concerning the Psalter|BCP 1979 Psalter]]\n";
out += "> - **Relevant Conceptual Hubs:** [[Hub - Gospel of John|Gospel of John]] · [[Hub - Technics, memory and the Leviathan|Technics & Leviathan]]\n\n---\n\n";
for (const p of parts) {
  const tag = two ? `: ${p.sunday ? "the Sunday" : p.title}` : "";
  if (p.bcp) out += `## Collect of the Day${tag}\n\n${bcpCollect(feastC)}---\n\n`;
  else { const cs = collectsOf(p.fm); if (cs.length) out += `## Collect of the Day${tag}\n\n` + cs.map(emb).join("\n\n*or this*\n\n") + "\n\n---\n\n"; }
}
out += "## Readings & Exegetical Notes\n\n";
for (const p of parts) {
  const tag = two ? `### Readings: ${p.sunday ? "the Sunday" : p.title}\n\n` : "";
  const t2e = !p.bcp && p.occ && p.sunday && p.fm.track2 ? track2Embeds(p.occ) : null;
  out += p.bcp ? tag + bcpReadings(feastC) : p.occ ? tag + (t2e ? "*The complementary track (Track 2), as read after Pentecost.*\n\n" + t2e : "!" + wl(p.occ + "#Readings")) + "\n\n" : "";
}
if (psalmOut) out += `### Psalm in the Prayer Book${feastPart && keepSunday ? " (the Sunday's)" : ""}\n\n` + psalmOut;
if (feastPart && keepSunday && feastC.meta) out += `The feast's psalm in the Prayer Book: ${feastC.meta.psalm}\n\n`;
out += "### First Reading (Hebrew Bible / Old Testament)\n\n\n\n### Psalm\n\n\n\n### Second Reading (Epistle)\n\n\n\n### The Holy Gospel\n\n\n\n---\n\n";
out += "## Homiletical Draft\n\n> [!reflection] The Proclamation (*Praedicatio*)\n> \n\n- claim:: \n- cites:: \n";
const name = `${date || moment().format("YYYY-MM-DD")} ${label} (polyphonic)`;
// the homilies folder is wherever the note "Homilies" (its folder note) is (12 Oct 2026, restructure)
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Writing/Homilies";
// a name that is already taken makes the move throw, and the note was left blank (F29 g): keep this name, fill the note, say why
if (!tp.file.folder(true).startsWith(HF) || tp.file.title !== name) {
  try { await tp.file.move(`${HF}/${name}`); }
  catch (e) { out = out.replace(`# Homily: ${label}\n\n`, `# Homily: ${label}\n\n*Not moved to "${HF}/${name}": ${e && e.message ? e.message : e}*\n\n`); }
}
tR += out;
%>
