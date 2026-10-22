// Holy Days (BCP 1979): which Holy Day belongs to a date, what the Prayer Book's rules say about it on a Sunday, and the
// choice between the Sunday's readings and collect and the feast's. Added 18 Oct 2026.
//   - The dates and the transfers come from the Daily Office view's engine (its CORE block), as in the date header.
//   - The ranks, psalms, readings, collects and the RCL notes come from the table Calendar/Holy Days (BCP 1979).md,
//     which is made from the BCP 1979 notes only.
//   - The choice (Sunday or feast) is kept in the note "Holy Days - my choices", one row per date.
// Rules used (BCP 1979 page numbers; the quotations are in the table's note):
//   p. 15  Principal Feasts take precedence of any other day; All Saints' Day may always be observed on the Sunday
//          following November 1 as well.
//   p. 16  Only the Holy Name, the Presentation and the Transfiguration take precedence of a Sunday. Other Feasts of our Lord
//          and Major Feasts on a Sunday are normally transferred; "when desired" the Collect, Preface and one or more of the
//          Lessons of the feast may be used on the Sunday, but not from the Last Sunday after Pentecost through the First Sunday
//          after the Epiphany, or from the Last Sunday after the Epiphany through Trinity Sunday.
//   p. 17  Fixed feasts are not kept in Holy Week or Easter Week; a feast on a weekday may be kept on any open day that week.
// Used as:  dv.view("Templates/Views/holyday", { container, date })  (the switch, on Home), and loaded by the other views and
// the homily templates with HD.load(app).
// ---- CORE BEGIN (pure logic apart from load(); evaluated by the views and the templates) ----
const HD = (() => {
  const TABLE = "Holy Days (BCP 1979)", CHOICES = "Holy Days - my choices", DO_VIEW = "Templates/Views/daily-office/view.js";
  const CONT = "BCP - Collects - Contemporary (Holy Days)", TRAD = "BCP - Collects - Traditional (Holy Days)";
  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const cells = l => l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim());
  const unesc = s => s.replace(/\\\|/g, "|");
  const LINK = /\[\[([^\]|]+)(?:\|([^\]]*))?\]\]/g;
  const plain = s => s.replace(LINK, (m, a, b) => b ?? a).replace(/\*/g, "").replace(/<br>/g, " ").replace(/\s+/g, " ").trim();
  const linkParts = s => [...s.matchAll(LINK)].map(m => ({ target: m[1], text: m[2] ?? m[1] }));

  // The table's feast rows: | October 18 | **Saint Luke the Evangelist** | rank | psalm | lessons | collect | Office | RCL | pages |
  function parseTable(text) {
    const byKey = {};
    for (const l of text.split("\n")) {
      if (!l.startsWith("| ")) continue;
      const c = cells(l);
      if (c.length < 9 || !/^\*\*/.test(c[1])) continue;
      const m = /^([A-Za-z]+) (\d{1,2})$/.exec(c[0]);
      const key = m ? `${MONTHS.indexOf(m[1]) + 1}-${+m[2]}` : "thanksgiving";
      const collect = unesc(c[5]);
      byKey[key] = { key, title: c[1].replace(/\*\*/g, ""), rank: c[2], psalm: unesc(c[3]), lessons: unesc(c[4]), collect, office: unesc(c[6]), rcl: unesc(c[7]), pages: c[8],
        anchor: (/#\^(collect-[a-z0-9-]+)/.exec(collect) || [])[1] || "", preface: (/\*(Preface of [^*]+)\*/.exec(collect) || [])[1] || "" };
    }
    return byKey;
  }
  function parseChoices(text) {
    const m = {};
    for (const l of text.split("\n")) { const c = l.startsWith("| ") ? cells(l) : []; if (c.length >= 3 && /^\d{4}-\d{2}-\d{2}$/.test(c[0]) && /^(feast|sunday|both)$/.test(c[2])) m[c[0]] = c[2]; }
    return m;
  }
  // "or this" sets in a lessons cell are separated by <br>*or this:*; the lessons of a set by " · "
  const setsOf = cell => cell.split(/<br>\*or this:\* ?/).map(s => s.trim());
  // a lesson with alternatives ("Mark 1:1-15 *or* Mark 16:15-20") is one lesson with several alts
  const lessonsOf = (cell, i) => (setsOf(cell)[i || 0] || "").replace(/<br>\*[^*]*\*$/, "").split(" · ").map(s => s.trim()).filter(Boolean).map(s => {
    const alts = s.split(/\s\*or\*\s/).map(a => ({ label: plain(a), target: (linkParts(a)[0] || {}).target || null }));
    return { label: alts.map(a => a.label).join(" or "), target: alts[0].target, alts };
  });
  const rclLinks = cell => linkParts(cell).map(x => x.target);

  // The verses a lesson's label names ("Hebrews 10:35--11:1", "Acts 6:8--7:2a,51c-60", "Ephesians 1:(11-14)15-23"): [{c, v1, v2}]
  // (v2 = Infinity to the end of the chapter, for "--")
  function refsOf(label) {
    const i = label.search(/\d+:\d/); if (i < 0) return [];
    const refs = []; let c = null;
    for (const m of label.slice(i).replace(/[()]/g, " ").matchAll(/(\d+):|(--)|(\d+)[a-c]?(?:-(\d+)[a-c]?)?/g)) {
      if (m[1]) c = +m[1];
      else if (m[2]) { if (refs.length) refs[refs.length - 1].v2 = Infinity; }
      else if (c != null) refs.push({ c, v1: +m[3], v2: m[4] ? +m[4] : +m[3] });
    }
    return refs;
  }

  function make(DO, holyText, tableText, choiceText) {
    const holy = DO.parseHolyDays(holyText), meta = parseTable(tableText), choices = parseChoices(choiceText);
    const cache = {};
    const obsYear = y => cache[y] || (cache[y] = DO.observances(y, holy));
    const obsAround = y => [...obsYear(y - 1), ...obsYear(y), ...obsYear(y + 1)];
    const metaOf = o => meta[o.month ? `${o.month}-${o.day}` : "thanksgiving"] || null;
    const fmt = T => { const p = DO.parts(T); return `${DO.DAYS[p.dow].slice(0, 3)} ${p.d} ${DO.MON3[p.m - 1]}`; };
    const BY_RIGHT = /^(The Presentation|The Transfiguration)$/;            // p. 16 (the Holy Name is in the seasonal notes)
    const dress = o => { const m = metaOf(o); return { ...o, title: m ? m.title : o.name, rank: m ? m.rank : "", meta: m }; };
    const firstSundayAfterNov1 = y => { const n = DO.mk(y, 11, 1); return DO.add(n, 7 - DO.parts(n).dow); };
    // p. 16: the two stretches of the year in which the feast's collect and lessons may not be put in place of the Sunday's
    function barred(T) {
      const F = DO.frame(T), e1 = DO.add(F.epiph, ((7 - DO.parts(F.epiph).dow) % 7) || 7), lastEpiph = DO.add(F.ashWed, -3), lastPent = DO.add(F.nextAdv, -7);
      if (T <= e1 || T >= lastPent) return "BCP p. 16: not from the Last Sunday after Pentecost through the First Sunday after the Epiphany";
      if (T >= lastEpiph && T <= F.trin) return "BCP p. 16: not from the Last Sunday after the Epiphany through Trinity Sunday";
      return null;
    }
    // RCL year letter of a date: the year that begins on the First Sunday of Advent of year Y is A when Y mod 3 is 0 (Advent 2025, 2028),
    // B when it is 1 (2026), C when it is 2 (2027)
    const rclYear = T => ({ 0: "A", 1: "B", 2: "C" })[DO.frame(T).advY % 3];

    function info(iso) {
      const T = DO.parseISO(iso), P = DO.parts(T), cal = DO.calendar(T), obs = obsAround(P.y);
      const r = { iso, T, dow: P.dow, cal, feast: null, cand: null, kind: null, canSwitch: false, def: null, use: null, feastUsed: false, reason: null, choice: choices[iso] || null };
      const today = obs.find(o => o.observed === T);
      // 19 Oct 2026 (decision 16c): a feast transferred from a Sunday on which its readings and collect were used (a `feast` or `both` row
      // for that Sunday in the choices note) is not kept again on the weekday it was transferred to
      const isoOf = X => { const q = DO.parts(X); return `${q.y}-${String(q.m).padStart(2, "0")}-${String(q.d).padStart(2, "0")}`; };
      const usedOnSunday = !!(today && today.transferred && DO.parts(today.nominal).dow === 0 && choices[isoOf(today.nominal)] && choices[isoOf(today.nominal)] !== "sunday");
      if (usedOnSunday) r.sundayUsed = dress(today);
      else if (today) r.feast = dress(today);
      if (P.dow === 0) {
        const displaced = obs.find(o => o.nominal === T && o.observed !== T);
        const after = T === firstSundayAfterNov1(P.y) && DO.parts(DO.mk(P.y, 11, 1)).dow !== 0 ? obs.find(o => /^All Saints/.test(o.name) && o.nominal === DO.mk(P.y, 11, 1)) : null; // not offered again when 1 Nov is itself a Sunday (19 Oct 2026, decision 16b)
        if (today && BY_RIGHT.test(today.name)) { r.kind = "by-right"; r.cand = r.feast; r.canSwitch = true; r.def = "feast"; }
        else if (today && /^All Saints/.test(today.name)) { r.kind = "principal"; r.cand = r.feast; r.def = "feast"; }
        else if (displaced) {
          r.cand = dress(displaced); r.def = "sunday"; const b = barred(T);
          if (b) { r.kind = "barred"; r.reason = b; } else { r.kind = "optional"; r.canSwitch = true; }
        } else if (after) { r.cand = dress(after); r.kind = "after"; r.canSwitch = true; r.def = "sunday"; }
      } else if (today && !usedOnSunday) { r.kind = "weekday"; r.cand = r.feast; r.def = "feast"; }
      if (r.def) { r.use = r.canSwitch && r.choice ? r.choice : r.def; r.feastUsed = r.use !== "sunday"; }
      return r;
    }
    // The lines for the date header: church = the short form for Home's one line (or null to leave the day as it is), holy = a second
    // short piece, lines = the paragraph lines of the full box
    function describe(iso) {
      const i = info(iso), out = { info: i, church: null, holy: null, lines: [] };
      if (!i.kind) { if (i.sundayUsed) out.lines.push(`<small>${i.sundayUsed.title} was kept on ${fmt(i.sundayUsed.nominal)} at your choice and is not kept again today.</small>`); return out; }
      const f = i.cand, tbl = `[[${TABLE}|Holy Days table]]`, use = i.feastUsed ? "in use" : "not chosen";
      const moved = f.transferred ? ` · transferred from ${fmt(f.nominal)}` : "";
      if (i.kind === "weekday") {
        out.church = f.title + (f.transferred ? ` (transferred from ${fmt(f.nominal)})` : "");
        out.lines.push(`Holy Day: ${f.rank || "Holy Day"}${moved} (${tbl})`);
        if (f.transferred && f.reason) out.lines.push(`<small>${f.title} (${fmt(f.nominal)}) ${f.reason}.</small>`);
      } else if (i.kind === "by-right" || i.kind === "principal") {
        out.church = i.use === "sunday" ? null : f.title;
        out.lines.push(`Holy Day: **${f.title}**, ${f.rank} · takes precedence of the Sunday (BCP p. ${i.kind === "principal" ? 15 : 16})` +
          (i.kind === "by-right" ? ` · ${i.feastUsed ? "the feast's readings and collect are in use" : "you chose the Sunday's readings and collect"}` : "") + ` (${tbl})`);
      } else if (i.kind === "optional") {
        out.church = i.feastUsed ? `${f.title} (in place of the Sunday)` : null;
        out.holy = i.feastUsed ? null : `${f.title}, kept ${fmt(f.observed)}`;
        out.lines.push(`Holy Day: **${f.title}** (${f.rank}) falls today and is kept ${fmt(f.observed)}. BCP p. 16: "When desired" its collect and readings may be used today instead of the Sunday's: ${use} (${tbl})`);
      } else if (i.kind === "barred") {
        out.holy = `${f.title}, kept ${fmt(f.observed)}`;
        out.lines.push(`Holy Day: **${f.title}** (${f.rank}) falls today and is kept ${fmt(f.observed)}; its readings cannot be used on this Sunday (${i.reason}) (${tbl})`);
      } else if (i.kind === "after") {
        out.church = i.feastUsed ? `${f.title} (the Sunday following 1 November)` : null;
        out.lines.push(`Holy Day: **${f.title}** may also be observed today, the Sunday following 1 November (BCP p. 15): ${use} (${tbl})`);
      }
      return out;
    }
    // The Holy Days observed after a date, within `days` days (date first)
    function upcoming(iso, days) {
      const T0 = DO.parseISO(iso), P = DO.parts(T0);
      const seen = new Set();
      return obsAround(P.y).filter(o => o.observed > T0 && o.observed <= DO.add(T0, days)).sort((a, b) => a.observed - b.observed)
        .filter(o => !seen.has(o.observed + o.name) && seen.add(o.observed + o.name)).map(dress);
    }
    // Every Holy Day observed in calendar year y, with the rule that applies on a Sunday, for the table's second part
    function yearRows(y) {
      const rows = [];
      for (const o of obsYear(y)) {
        if (DO.parts(o.observed).y !== y && DO.parts(o.nominal).y !== y) continue;
        const f = dress(o), nom = DO.parts(o.nominal), obsd = DO.parts(o.observed);
        const nomDay = DO.DAYS[nom.dow], obsDay = DO.DAYS[obsd.dow];
        let what, sunday;
        if (o.transferred) what = `kept ${fmt(o.observed)}: ${o.reason}`; else what = "kept on its date";
        if (nom.dow === 0 && BY_RIGHT.test(o.name)) { what = "takes precedence of the Sunday (BCP p. 16)"; sunday = "its readings are the Sunday's replacement; the Sunday's may be chosen instead (added at your request)"; }
        else if (nom.dow === 0 && /^All Saints/.test(o.name)) { what = "Principal Feast; takes precedence of the Sunday (BCP p. 15)"; sunday = "—"; }
        else if (nom.dow === 0) { const b = barred(o.nominal); sunday = b ? `no (${b.replace(/^BCP p\. 16: /, "")})` : "yes, \"when desired\" (BCP p. 16)"; }
        else sunday = "—";
        rows.push({ observed: o.observed, nominal: o.nominal, f, nomDay, obsDay, what, sunday });
      }
      for (const o of obsYear(y).filter(o => /^All Saints/.test(o.name) && DO.parts(o.nominal).y === y)) {
        const T = firstSundayAfterNov1(y), f = dress(o);
        rows.push({ observed: T, nominal: o.nominal, f, nomDay: DO.DAYS[DO.parts(o.nominal).dow], obsDay: "Sunday", what: "may also be observed on the Sunday following November 1 (BCP p. 15)", sunday: "yes, always (BCP p. 15)" });
      }
      return rows.sort((a, b) => a.observed - b.observed);
    }
    return { DO, holy, meta, choices, info, describe, upcoming, yearRows, metaOf, fmt, rclYear, barred, dress };
  }

  // Loads the engine, the Holy Days notes, the table and the choices; returns make()'s object with the readers and the writer added.
  async function load(app) {
    const rd = async n => { const f = app.metadataCache.getFirstLinkpathDest(n, ""); return f ? await app.vault.cachedRead(f) : ""; };
    const src = await app.vault.adapter.read(DO_VIEW);
    // (the marker text is built in two pieces, so that this file's own block cannot be cut short by it)
    const core = src.split("// ---- CORE " + "BEGIN")[1]?.split("// ---- CORE " + "END")[0];
    if (!core) throw new Error(`${DO_VIEW}: the engine's CORE markers were not found`);
    const DO = new Function(core.replace(/^[^\n]*\n/, "") + "\nreturn DO;")();
    const holyText = await rd("BCP - Daily Office - Holy Days");
    if (!holyText) throw new Error("BCP - Daily Office - Holy Days not found");
    const hd = make(DO, holyText, await rd(TABLE), await rd(CHOICES));
    hd.TABLE = TABLE; hd.CHOICES = CHOICES; hd.CONT = CONT; hd.TRAD = TRAD;
    hd.lessonsOf = lessonsOf; hd.setsOf = setsOf; hd.rclLinks = rclLinks; hd.plain = plain; hd.linkParts = linkParts;
    // the embeds for a lesson (one per verse, as the RCL notes do): { embeds, missing }
    hd.verseEmbeds = lesson => {
      const out = { embeds: [], missing: [] };
      if (!lesson.target) { out.missing.push(lesson.label); return out; }
      const name = lesson.target.split("#")[0].trim(), m = /^(.*?)(\d+)$/.exec(name);
      const noteFor = c => { if (!m) return name; for (const cand of [`${m[1]}${String(c).padStart(2, "0")}`, `${m[1]}${c}`]) if (app.metadataCache.getFirstLinkpathDest(cand, "")) return cand; return null; };
      const has = (n, c, v) => { const f = n ? app.metadataCache.getFirstLinkpathDest(n, "") : null; return !!(f && app.metadataCache.getFileCache(f)?.blocks?.[`${c}-${v}`]); };
      for (const r of refsOf(lesson.label)) {
        const n = noteFor(r.c);
        for (let v = r.v1; v <= r.v2 && v < r.v1 + 400; v++) {
          if (has(n, r.c, v)) out.embeds.push(`${n}#^${r.c}-${v}`);
          else if (r.v2 === Infinity && v > r.v1) break;
          else out.missing.push(`${r.c}:${v}`);
        }
      }
      return out;
    };
    // Records the choice for a date: a row in the note "Holy Days - my choices" (made if it is missing)
    hd.setChoice = async (iso, title, use) => {
      const f = app.metadataCache.getFirstLinkpathDest(CHOICES, "");
      const row = `| ${iso} | ${title} | ${use} |`;
      const head = "---\ntype: data\ncssclasses:\n  - wide\n---\n# Holy Days - my choices\n\nOne row for each date on which you chose between the Sunday's readings and collect and the feast's (the buttons on Home, and the homily template, write here; you can also edit a row by hand). *Use* is `sunday`, `feast` or `both` (both is for a homily). A date with no row follows the Prayer Book's rules ([[Holy Days (BCP 1979)]]). Home, the Daily Office and the homily template read this note.\n\n| Date | Holy Day | Use |\n|---|---|---|\n";
      const upd = t => {
        const keep = t.split("\n").filter(l => !l.startsWith(`| ${iso} |`));
        let k = keep.findIndex(l => l.startsWith("|---")); if (k < 0) k = keep.length - 1;
        const head2 = keep.slice(0, k + 1), body = keep.slice(k + 1).filter(l => l.startsWith("| ")).concat(row).sort();
        return head2.join("\n") + "\n" + body.join("\n") + "\n";
      };
      if (f) await app.vault.process(f, upd); else await app.vault.create(CHOICES + ".md", upd(head));
    };
    return hd;
  }
  return { load, make, parseTable, parseChoices, lessonsOf, setsOf, refsOf, plain, TABLE, CHOICES };
})();
// ---- CORE END ----

// ---------- the switch on Home (Obsidian / Dataview only) ----------
if (typeof dv !== "undefined") {
  const opts = (typeof input === "object" && input) ? input : {};
  const root = opts.container || (() => {
    const el = dv.container.createDiv({ attr: { "data-vp-view": "holyday" } });
    const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-vp-view") === "holyday");
    if (old) old.replaceWith(el);
    return el;
  })();
  try {
    const iso = opts.date || moment().format("YYYY-MM-DD");
    const hd = await HD.load(app), i = hd.info(iso);
    if (i.canSwitch) {
      const f = i.cand, label = "the Sunday's";
      const p = root.createEl("p");
      p.createEl("strong", { text: `${f.title}: ` });
      p.appendText(i.use === "both" ? "the Sunday's and the feast's readings and collect are both in the homily. " : i.feastUsed ? "the feast's readings and collect are in use. " : "the Sunday's readings and collect are in use. ");
      const go = async use => {
        await hd.setChoice(iso, f.title, use);
        new Notice(use === "sunday" ? "Back to the Sunday's readings and collect." : `Using ${f.title}'s readings and collect.`);
        const ix = app.plugins.plugins.dataview?.index; if (typeof ix?.touch === "function") ix.touch();
      };
      const b = p.createEl("button", { text: i.feastUsed ? `Use ${label} readings and collect instead` : `Use ${f.title}'s readings and collect` });
      b.onclick = () => go(i.feastUsed ? "sunday" : "feast");
    }
  } catch (e) {
    console.error("holyday", e);
    root.createDiv({ cls: "vp-view-error", text: `holyday failed: ${e && e.message ? e.message : e}`,
      attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
  }
}
