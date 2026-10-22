/*
  Daily Office (BCP 1979) - Dataview view for Stephen's vault
  ----------------------------------------------------------------
  Installed as  Templates/Views/daily-office/view.js
  Use in a note (DataviewJS block):
      await dv.view("Templates/Views/daily-office")
      await dv.view("Templates/Views/daily-office", { date: "2026-12-25", open: true })
  Home passes { container }, the part of the page it made for this view; without
  one the view draws into an element of its own in the block (F3, 7 Oct 2026).
  If it was opened or closed by hand, it stays so when Dataview redraws the block (F4, 7 Oct 2026).

  What it does: reads the eight Daily Office Lectionary notes in
  the BCP 1979's Daily Office Lectionary (found by name), parses them, works out
  today's place in the Church Year, and renders the appointed Psalms and
  Lessons as a <details> block. Nothing is hard-coded from memory: every
  reading comes from the notes, and every calendar rule below cites the BCP
  page it is taken from.

  Rules used (BCP 1979 page numbers):
   p. 934  Two-year cycle. Year One begins on the First Sunday of Advent
           preceding odd-numbered years; Year Two before even-numbered years.
   p. 15   Advent = the four Sundays before Christmas Day. Easter Day is the
           first Sunday after the paschal full moon on/after March 21
           (pp. 880-883 give the tables; the computus here is checked
           against the printed table in test.mjs). Ash Wednesday and
           Ascension (Thursday, 40 days after Easter) follow from Easter.
   p. 15   Principal Feasts (Easter, Ascension, Pentecost, Trinity, All
           Saints, Christmas, Epiphany) take precedence of any other day.
   p. 16   Only Holy Name, the Presentation and the Transfiguration take
           precedence of a Sunday; other fixed Major Feasts falling on a
           Sunday are transferred to the first open day in the week.
   p. 17   Fixed feasts are not observed in Holy Week or Easter Week (they
           move to the week after 2 Easter, in order), nor on Ash Wednesday.
   p. 158, 884-885, 964  The numbered Proper is the one whose date is closest
           to the Sunday; weekdays after Pentecost and after Trinity Sunday
           use the Proper closest to those Sundays' dates.
   p. 942  The dated days after the Epiphany are used only until the
           following Saturday evening.
   p. 996-1000  Holy Day Psalms and Lessons (Morning and Evening Prayer).
   Thanksgiving Day: a Major Feast (p. 17) with its own readings (p. 1000);
           the BCP gives no date, so the fourth Thursday of November is used
           (U.S. federal observance). Set { thanksgiving: false } to skip it.
*/

// ---- CORE BEGIN (pure logic; test.mjs evaluates this block in node) ----
const DO = (() => {
  // 12 Oct 2026 (restructure): no folders. The lectionary notes are found by name and the links name the notes only
  // (each name is unique in the vault), so the BCP folder can move. A test may still pass opts.folder.
  const FOLDER = "";
  const PSALTER = "";
  const NOTE = {
    advent: "BCP - Daily Office - Advent",
    christmas: "BCP - Daily Office - Christmas",
    epiphany: "BCP - Daily Office - Epiphany",
    lent: "BCP - Daily Office - Lent",
    easter: "BCP - Daily Office - Easter",
    pentecost: "BCP - Daily Office - The Season after Pentecost",
    holydays: "BCP - Daily Office - Holy Days",
    special: "BCP - Daily Office - Special Occasions",
  };
  const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const MON3 = MONTHS.map((m) => m.slice(0, 3));

  // ---------- dates (UTC day arithmetic; no time zones involved) ----------
  const DAY = 86400000;
  const mk = (y, m, d) => Date.UTC(y, m - 1, d);
  const parts = (t) => { const x = new Date(t); return { y: x.getUTCFullYear(), m: x.getUTCMonth() + 1, d: x.getUTCDate(), dow: x.getUTCDay() }; };
  const iso = (t) => new Date(t).toISOString().slice(0, 10);
  const parseISO = (s) => { const m = /^(\d{4})-(\d{1,2})-(\d{1,2})/.exec(String(s)); return m ? mk(+m[1], +m[2], +m[3]) : null; };
  const add = (t, n) => t + n * DAY;
  const daysBetween = (a, b) => Math.round((b - a) / DAY);
  const longDate = (t) => { const p = parts(t); return `${MONTHS[p.m - 1]} ${p.d}, ${p.y}`; };

  // Easter Day (Gregorian computus; the BCP's rules and tables are on pp. 880-883).
  function easter(y) {
    const a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4,
      f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30,
      i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7,
      m = Math.floor((a + 11 * h + 22 * l) / 451), month = Math.floor((h + l - 7 * m + 114) / 31),
      day = ((h + l - 7 * m + 114) % 31) + 1;
    return mk(y, month, day);
  }
  // First Sunday of Advent in calendar year y: the fourth Sunday before Christmas Day (p. 15).
  function advent1(y) { const xmas = mk(y, 12, 25); const dow = parts(xmas).dow; return add(xmas, -(dow === 0 ? 7 : dow) - 21); }
  // Proper N is headed "Week of the Sunday closest to <date>"; Proper 1 = May 11, then weekly (pp. 966-995).
  const properDate = (y, n) => add(mk(y, 5, 11), (n - 1) * 7);
  // The Proper whose date is closest to a Sunday, "whether before or after" (p. 158).
  function properForSunday(sun) { const { y } = parts(sun); for (let n = 1; n <= 29; n++) if (Math.abs(daysBetween(properDate(y, n), sun)) <= 3) return n; return null; }
  // Fourth Thursday of November (not in the BCP; U.S. federal observance).
  function thanksgiving(y) { const nov1 = mk(y, 11, 1); const firstThu = add(nov1, (4 - parts(nov1).dow + 7) % 7); return add(firstThu, 21); }

  // The liturgical-year frame that contains t.
  function frame(t) {
    const { y } = parts(t);
    const advY = t >= advent1(y) ? y : y - 1;
    const E = easter(advY + 1);
    return {
      advY, adv: advent1(advY), xmas: mk(advY, 12, 25), epiph: mk(advY + 1, 1, 6),
      E, ashWed: add(E, -46), lent1: add(E, -42), palm: add(E, -7), asc: add(E, 39), pent: add(E, 49), trin: add(E, 56),
      nextAdv: advent1(advY + 1),
      year: (advY + 1) % 2 === 1 ? 1 : 2, // p. 934
    };
  }

  // ---------- the Church Year position of a date ----------
  function calendar(t) {
    const F = frame(t), P = parts(t), dow = P.dow;
    const r = { t, iso: iso(t), dow, dayName: DAYS[dow], year: F.year, yearLabel: F.year === 1 ? "Year One" : "Year Two",
      season: null, note: null, section: null, key: null, eves: [], notes: [], frame: F };
    if (t < F.xmas) { // Advent (pp. 936-939)
      const n = Math.floor(daysBetween(F.adv, t) / 7) + 1;
      r.season = "Advent"; r.note = "advent"; r.section = `Week of ${n} Advent`;
      if (P.m === 12 && P.d === 24) { r.key = dow === 0 ? "Sunday" : "Dec 24"; r.eves.push({ note: "advent", key: "Christmas Eve" }); }
      else r.key = DAYS[dow];
    } else if (t < F.epiph) { // Christmas (pp. 940-941)
      r.season = "Christmas"; r.note = "christmas"; r.section = "Christmas Day and Following";
      if (P.m === 12 && P.d === 25) r.key = "Christmas Day";
      else if (P.m === 1 && P.d === 1) r.key = "Holy Name"; // takes precedence of a Sunday (p. 16)
      else if (dow === 0) r.key = P.m === 12 ? "First Sunday after Christmas" : "Second Sunday after Christmas";
      else if (P.m === 12 && P.d >= 29) r.key = `Dec ${P.d}`;
      else if (P.m === 1) r.key = `Jan ${P.d}`;
      else r.key = null; // Dec 26-28 are St. Stephen, St. John, Holy Innocents (pp. 996)
      if (P.m === 12 && P.d === 31) r.eves.push({ note: "christmas", key: "Eve of Holy Name" });
      if (P.m === 1 && P.d === 5) r.eves.push({ note: "christmas", key: "Eve of Epiphany" });
    } else if (t < F.lent1) { // Epiphany, including Ash Wednesday and the three days after it (pp. 942-951)
      r.season = "Epiphany"; r.note = "epiphany";
      const e1 = add(F.epiph, ((7 - parts(F.epiph).dow) % 7) || 7); // First Sunday after the Epiphany
      if (t === F.epiph) { r.section = "The Epiphany and Following"; r.key = "Epiphany"; }
      else if (t < e1) { // dated days, used only until the following Saturday evening (p. 942 note)
        r.section = "The Epiphany and Following"; r.key = `Jan ${P.d}`;
        if (dow === 6) r.eves.push({ note: "epiphany", key: "Eve of 1 Epiphany" });
      } else {
        const sun = add(t, -dow), n = Math.floor(daysBetween(e1, sun) / 7) + 1;
        r.section = sun === add(F.ashWed, -3) ? "Week of Last Epiphany" : `Week of ${n} Epiphany`;
        r.key = t === F.ashWed ? "Ash Wednesday" : DAYS[dow];
      }
    } else if (t < F.palm) { // Lent (pp. 952-957)
      const n = Math.floor(daysBetween(F.lent1, t) / 7) + 1;
      r.season = "Lent"; r.note = "lent"; r.section = `Week of ${n} Lent`; r.key = DAYS[dow];
    } else if (t < F.E) { // Holy Week (pp. 956-957)
      r.season = "Holy Week"; r.note = "lent"; r.section = "Holy Week";
      r.key = dow === 0 ? "Palm Sunday" : dow === 4 ? "Maundy Thursday" : dow === 5 ? "Good Friday" : dow === 6 ? "Holy Saturday" : DAYS[dow];
    } else if (t < F.pent) { // Easter (pp. 958-965)
      r.season = "Easter"; r.note = "easter";
      const n = Math.floor(daysBetween(F.E, t) / 7) + 1;
      r.section = n === 1 ? "Easter Week" : `Week of ${n} Easter`;
      if (t === F.E) r.key = "Easter Day";
      else if (t === F.asc) r.key = "Ascension Day";
      else {
        r.key = DAYS[dow];
        if (t === add(F.asc, -1)) r.eves.push({ note: "easter", key: "Eve of Ascension" });
        if (t === add(F.pent, -1)) r.eves.push({ note: "easter", key: "Eve of Pentecost" });
      }
    } else { // Pentecost, Trinity, and the Season after Pentecost (pp. 964-995)
      const sun = add(t, -dow), p = properForSunday(sun);
      r.season = "Season after Pentecost"; r.proper = p;
      if (t === F.pent) { r.note = "easter"; r.section = "Week of 7 Easter"; r.key = "The Day of Pentecost"; }
      else if (t === F.trin) { r.note = "easter"; r.section = "Week of 7 Easter"; r.key = "Trinity Sunday"; }
      else {
        r.note = "pentecost"; r.section = `Proper ${p}`; r.key = DAYS[dow];
        if (t === add(F.trin, -1)) r.eves.push({ note: "easter", key: "Eve of Trinity Sunday" });
        if (t < F.trin) r.notes.push(`Weekdays after the Day of Pentecost: readings from the numbered Proper closest to the date of Pentecost (BCP p. 964).`);
        else if (t < add(F.trin, 7)) r.notes.push(`Weekdays after Trinity Sunday: readings from the numbered Proper closest to the date of Trinity Sunday (BCP p. 964).`);
      }
    }
    return r;
  }

  // ---------- Holy Days: when each fixed feast is actually observed in calendar year y ----------
  const isPrincipalFixed = (name) => /^All Saints/.test(name); // Christmas and Epiphany live in the seasonal notes
  const takesSunday = (name) => isPrincipalFixed(name) || /^(The Presentation|The Transfiguration)$/.test(name); // p. 16
  function observances(y, holy, opts) {
    const E = easter(y), ashWed = add(E, -46), palm = add(E, -7), asc = add(E, 39);
    const inHolyOrEasterWeek = (t) => t >= palm && t <= add(E, 6); // p. 17
    const blocked = (t) => inHolyOrEasterWeek(t) || t === ashWed || t === asc; // pp. 15, 17
    const list = [];
    for (const h of holy.days) {
      let nominal = h.month ? mk(y, h.month, h.day) : null;
      if (!nominal && /^Thanksgiving/.test(h.name) && (!opts || opts.thanksgiving !== false)) nominal = thanksgiving(y);
      if (!nominal) continue;
      list.push({ ...h, nominal, observed: null, transferred: false, reason: null });
    }
    list.sort((a, b) => a.nominal - b.nominal);
    // One pass in order of occurrence (p. 17): each feast takes the first open day at or after its
    // target. A feast whose own date has just been taken by a transferred feast moves on too, so
    // when Dec 26 is a Sunday, St. Stephen, St. John and Holy Innocents fall on Dec 27, 28, 29.
    const taken = new Set();
    for (const o of list) {
      let t = o.nominal, why = null;
      if (!isPrincipalFixed(o.name)) {
        if (inHolyOrEasterWeek(t)) { t = add(E, 8); why = "falls in Holy Week or Easter Week; transferred to the week after the Second Sunday of Easter (BCP p. 17)"; }
        else if (t === ashWed) { t = add(t, 1); why = "does not take precedence of Ash Wednesday (BCP p. 17)"; }
        else if (t === asc) { t = add(t, 1); why = "yields to Ascension Day, a Principal Feast (BCP p. 15)"; }
        else if (parts(t).dow === 0 && !takesSunday(o.name)) { t = add(t, 1); why = "falls on a Sunday; transferred to the first open day in the week (BCP p. 16)"; }
        const sundayBad = (d) => parts(d).dow === 0 && !(d === o.nominal && takesSunday(o.name)); // Holy Name/Presentation/Transfiguration may keep their own Sunday (p. 16)
        while (sundayBad(t) || blocked(t) || taken.has(t)) {
          if (!why) why = "falls on a date taken by a feast transferred onto it; moved to the next open day, in order of occurrence (BCP pp. 16-17)";
          t = add(t, 1);
        }
      }
      o.observed = t; o.transferred = t !== o.nominal; o.reason = why; taken.add(t);
    }
    return list;
  }
  // Does an "Eve of X" entry belong to this feast? ("Eve of Holy Cross" -> "Holy Cross Day", "Eve of St. John the Baptist" -> "Nativity of St. John the Baptist")
  function eveMatches(eveName, feastName) {
    const want = eveName.replace(/^Eve of (the )?/, "").toLowerCase();
    return feastName.toLowerCase().includes(want);
  }

  // ---------- parsing the vault notes ----------
  const normKey = (s) => s.replace(/\\\*/g, "").replace(/\./g, "").replace(/\s+/g, " ").trim();
  const noPsalms = (s) => !s || /^[\\\-–—\s]*$/.test(s);
  function footnoteSegments(line) { // "*\*For the Invitatory \*\*Intended for use in the morning*" -> [{mark, text}]
    const body = line.replace(/^\*|\*$/g, "");
    const out = []; const re = /((?:\\\*)+)\s*([^\\]+?)(?=\s*(?:\\\*)|\s*·|$)/g; let m;
    while ((m = re.exec(body))) out.push({ mark: m[1], text: m[2].replace(/\*$/g, "").trim() });
    return out;
  }
  // One seasonal note (pages alternate: even page = Year One, odd page = Year Two; see test.mjs for the check).
  function parseSeasonal(noteKey, text) {
    const entries = [];
    let page = null, year = null, section = null, cur = null;
    const pageFootnotes = {}; // page -> [{mark,text}]
    const lines = text.split(/\r?\n/);
    for (const raw of lines) {
      const line = raw.trim();
      if (!line) continue;
      let m;
      if ((m = /^\[p\. (\d+)\]$/.exec(line))) { page = +m[1]; year = page % 2 === 0 ? 1 : 2; cur = null; continue; }
      if (page == null) continue; // title, header line
      if ((m = /^\*\*\*([A-Za-z]+)\*\*\*\s*(.*)$/.exec(line))) { // ***Monday*** psalms v psalms
        cur = startEntry(m[1], m[2]); continue;
      }
      if ((m = /^\*\*([^*]+)\*\*(.*)$/.exec(line))) { // **Week of 1 Advent** / **Proper 22** *Week of the Sunday closest to October 5*
        section = m[1].trim(); cur = null;
        const c = /closest to ([A-Za-z]+) (\d+)/.exec(m[2]);
        entries.push({ heading: true, year, page, section, closest: c ? { month: MONTHS.indexOf(c[1]) + 1, day: +c[2] } : null });
        continue;
      }
      if (/^\*\\\*/.test(line)) { (pageFootnotes[page] = pageFootnotes[page] || []).push(...footnoteSegments(line)); continue; }
      if ((m = /^\*([^*\\](?:[^*\\]|\\.)*?)\*\s*·\s*(.*)$/.exec(line))) { // *Dec. 24* · psalms v psalms
        cur = startEntry(m[1], m[2]); continue;
      }
      if (/^\*[^*]+\*$/.test(line) || /^Directions for/.test(line)) continue; // italic directions
      if (cur) cur.lessonLines.push(line.replace(/^\\` · /, "").replace(/\\</g, ""));
    }
    for (const e of entries) {
      if (e.heading) continue;
      const marks = new Set((e.text.match(/(?:\\\*)+/g) || []));
      e.footnotes = (pageFootnotes[e.page] || []).filter((f) => marks.has(f.mark)).map((f) => `${f.mark} ${f.text}`);
    }
    return entries.filter((e) => !e.heading).concat(entries.filter((e) => e.heading));

    function startEntry(rawKey, rest) {
      const key = normKey(rawKey);
      let mp = null, ep = null;
      const v = /^(.*?)\s+v\s+(.*)$/.exec(rest.trim());
      if (v) { mp = noPsalms(v[1]) ? null : v[1].trim(); ep = noPsalms(v[2]) ? null : v[2].trim(); }
      else if (!noPsalms(rest)) mp = rest.trim();
      const e = { noteKey, year, page, section, key, rawKey, mp, ep, lessonLines: [], get text() { return [this.rawKey, this.mp, this.ep, ...this.lessonLines].join(" "); } };
      entries.push(e);
      return e;
    }
  }
  // Holy Days note (pp. 996-1000): "**St. Luke** *October 18* · <MP psalms + lessons> · <EP psalms + lessons>"
  function parseHolyDays(text) {
    const days = [], eves = [];
    let page = null, cur = null;
    for (const raw of text.split(/\r?\n/)) {
      const line = raw.trim();
      if (!line) { continue; }
      let m;
      if ((m = /^\[p\. (\d+)\]$/.exec(line))) { page = +m[1]; cur = null; continue; }
      if (page == null || /^#/.test(line)) continue;
      if (/^\*\*Morning Prayer\*\*/.test(line)) { cur = null; continue; }
      if ((m = /^\*\*([^*]+)\*\*\s*(?:\*([A-Za-z]+) (\d{1,2})\*)?\s*(.*)$/.exec(line))) {
        cur = { name: m[1].replace(/\s*&\s*/g, " & ").trim(), month: m[2] ? MONTHS.indexOf(m[2]) + 1 : null, day: m[3] ? +m[3] : null, page, body: m[4].replace(/^·\s*/, "") };
        (/^Eve/.test(cur.name) ? eves : days).push(cur);
        continue;
      }
      if (cur) cur.body += " " + line; // continuation ("or ...")
    }
    for (const h of [...days, ...eves]) {
      const offices = h.body.split(/\s·\s/).map((s) => s.trim()).filter(Boolean);
      h.mp = offices[0] ? splitOffice(offices[0]) : null;
      h.ep = offices[1] ? splitOffice(offices[1]) : null;
      if (/^Eve/.test(h.name)) { h.ep = h.mp; h.mp = null; } // an eve is an Evening Prayer entry
      delete h.body;
    }
    return { days, eves };
    function splitOffice(s) { // leading psalm tokens, then the lessons
      const toks = s.split(/\s+/);
      let i = 0;
      while (i < toks.length) {
        const tok = toks[i], next = toks[i + 1] || "";
        const psalmish = /^[\[\]\d:,\-()ab]+,?$/.test(tok) || tok === "*or*";
        if (!psalmish) break;
        if (/^[123]$/.test(tok) && /^[A-Z]/.test(next)) break; // "2 Esdras", "1 Kings" (a book, not a psalm)
        i++;
      }
      return { psalms: toks.slice(0, i).join(" ").replace(/,(?=\S)/g, ", ") || null, lessons: toks.slice(i).join(" ") };
    }
  }
  // Break a lesson line into lessons (a new lesson starts at a book name); used only to place separators.
  function splitLessons(text) {
    const toks = text.match(/\[\[[^\]]*\]\][^\s\[]*|\S+/g) || [];
    const display = (tok) => { const m = /^\[\[([^\]|]+)(?:\|([^\]]*))?\]\]/.exec(tok); return m ? (m[2] != null ? m[2] : m[1]) : tok; };
    const isBook = (d) => /^[A-Z][a-z]/.test(d.replace(/^(?:[123]|I{1,3})\s+/, ""));
    const segs = []; let cur = [];
    for (let i = 0; i < toks.length; i++) {
      const prev = toks[i - 1] || "";
      const afterOr = /^\*?or\*?$/.test(prev) || /;$/.test(prev); // "*or* ..." and "; 5:2-4" continue the lesson before
      let d = display(toks[i]), consume = 1;
      if (/^(?:[123]|I{1,3})$/.test(d) && i + 1 < toks.length && /^[A-Za-z]/.test(display(toks[i + 1]))) { d += " " + display(toks[i + 1]); consume = 2; } // plain "2 John 1-13"
      const starts = !afterOr && (consume === 2 || isBook(d));
      if (starts && cur.length) { segs.push(cur.join(" ")); cur = []; }
      for (let j = 0; j < consume; j++) cur.push(toks[i + j]);
      i += consume - 1;
    }
    if (cur.length) segs.push(cur.join(" "));
    return segs;
  }

  function buildData(texts) { // texts: { advent, christmas, epiphany, lent, easter, pentecost, holydays }
    const seasonal = { 1: { sections: {}, byKey: {} }, 2: { sections: {}, byKey: {} } };
    const headings = [];
    for (const k of ["advent", "christmas", "epiphany", "lent", "easter", "pentecost"]) {
      if (!texts[k]) continue;
      for (const e of parseSeasonal(k, texts[k])) {
        if (e.heading) { headings.push(e); continue; }
        const Y = seasonal[e.year];
        (Y.sections[e.section] = Y.sections[e.section] || {})[e.key] = e;
        if (!DAYS.includes(e.key)) Y.byKey[e.key] = e;
      }
    }
    const holy = texts.holydays ? parseHolyDays(texts.holydays) : { days: [], eves: [] };
    return { seasonal, holy, headings };
  }

  // ---------- put it together for one date ----------
  function resolve(t, data, opts) {
    const cal = calendar(t);
    const Y = data.seasonal[cal.year];
    const find = (noteKey, section, key) => (section && Y.sections[section] && Y.sections[section][key]) || Y.byKey[key] || null;
    const blocks = [], warnings = [];
    const base = cal.key ? find(cal.note, cal.section, cal.key) : null;
    if (cal.key && !base) warnings.push(`No entry for "${cal.section} / ${cal.key}" in ${cal.yearLabel}.`);

    // Holy Days observed today, and eves of Holy Days observed tomorrow (pp. 996-1000)
    const P = parts(t);
    const obs = [...observances(P.y - 1, data.holy, opts), ...observances(P.y, data.holy, opts), ...observances(P.y + 1, data.holy, opts)];
    let feast = obs.find((o) => o.observed === t) || null;
    if (opts && opts.skipFeast && feast && feast.transferred) feast = null; // 19 Oct 2026 (decision 16c): its readings were used on the Sunday it fell on
    // 18 Oct 2026: the choice between the Sunday's readings and the feast's (BCP p. 16, "When desired"; p. 15 for All Saints on the
    // Sunday following November 1). opts.useFeast = the name of a feast to use in place of the Sunday's entry; opts.useSunday = use the
    // Sunday's entry on a Sunday that a feast takes (the Presentation, the Transfiguration). Both come from the holyday view.
    let usedSunday = null;
    if (opts && opts.useFeast && !feast) {
      const c = obs.filter((o) => o.name === opts.useFeast).sort((a, b) => Math.abs(a.nominal - t) - Math.abs(b.nominal - t))[0];
      if (c) feast = { ...c, transferred: false, reason: null, substituted: true };
    } else if (opts && opts.useSunday && feast) { usedSunday = feast; feast = null; }
    const F = cal.frame;
    const principalDay = t === F.E || t === F.asc || t === F.pent || t === F.trin || t === F.xmas || t === F.epiph || t === mk(P.y, 11, 1);
    const eveAllowed = !principalDay && !(t >= F.palm && t <= add(F.E, 6)) && t !== F.ashWed; // Principal Feasts, Holy Week, Easter Week and Ash Wednesday keep their own evening (pp. 15, 17)
    const holyEves = eveAllowed ? data.holy.eves
      .map((ev) => ({ ev, feast: obs.find((o) => eveMatches(ev.name, o.name) && !o.transferred && add(o.observed, -1) === t) }))
      .filter((x) => x.feast) : [];

    let summary, displaced = null;
    if (feast) {
      displaced = base ? describe(cal) : null;
      summary = `${feast.name}${feast.transferred ? " (transferred)" : ""} · ${cal.dayName}`;
      const why = feast.transferred ? `${feast.name} (${longDate(feast.nominal)}) ${feast.reason}.` : null;
      blocks.push(holyBlock(feast, "Morning Prayer", feast.mp), holyBlock(feast, "Evening Prayer", feast.ep));
      if (why) cal.notes.push(why);
      if (displaced) cal.notes.push(feast.substituted ? `${feast.name} is used in place of the Sunday entry (${displaced}) at your choice (BCP p. 16, "When desired"; for All Saints, p. 15).`
        : cal.dow === 0 && takesSunday(feast.name) ? `${feast.name} takes precedence of the Sunday (BCP pp. 15-16); the Sunday entry (${displaced}) is not used.` : `In place of ${displaced} (BCP pp. 16-17).`);
    } else {
      summary = describe(cal);
      if (base) blocks.push(seasonalBlock(base, null));
      if (usedSunday) cal.notes.push(`The Sunday entry is used at your choice; ${usedSunday.name} would take precedence of this Sunday (BCP p. 16).`);
    }
    for (const ev of cal.eves) {
      const e = find(ev.note, null, ev.key);
      if (e) blocks.push(seasonalBlock(e, `Evening Prayer · ${ev.key}`)); else warnings.push(`No entry for "${ev.key}" in ${cal.yearLabel}.`);
    }
    for (const { ev } of holyEves) blocks.push(holyBlock(ev, `Evening Prayer · ${ev.name}`, ev.ep));
    return { cal, summary, blocks, warnings, feast, base };
  }
  function describe(cal) {
    if (!cal.key) return `${cal.section} · ${cal.dayName}`;
    if (DAYS.includes(cal.key)) return `${cal.section} · ${cal.key}`;
    const keyLabel = /^(Dec|Jan) \d+$/.test(cal.key) ? cal.key.replace(" ", ". ") : cal.key;
    const impliesDay = /Sunday|Wednesday|Thursday|Friday|Saturday|Easter Day|Ascension Day|Pentecost/.test(cal.key);
    const withDay = impliesDay ? keyLabel : `${keyLabel} · ${cal.dayName}`;
    const dropSection = /and Following$/.test(cal.section) || /^(Trinity Sunday|The Day of Pentecost)$/.test(cal.key);
    return dropSection ? withDay : `${cal.section} · ${withDay}`;
  }
  function seasonalBlock(e, title) {
    return { kind: "seasonal", title, mp: e.mp, ep: e.ep, lessons: e.lessonLines, footnotes: e.footnotes || [], page: e.page, noteKey: e.noteKey, section: e.section, key: e.key };
  }
  function holyBlock(h, title, office) {
    return { kind: "holy", title, psalms: office ? office.psalms : null, lessons: office ? [office.lessons] : [], footnotes: [], page: h.page, noteKey: "holydays", name: h.name };
  }

  // ---------- markdown helpers ----------
  const pad3 = (n) => String(n).padStart(3, "0");
  function psalmsMD(s) { // "20, 21:1-7(8-14)" -> each psalm linked to its Psalter note
    if (!s) return "—";
    return s.replace(/,(?=\S)/g, ", ").split(/\s+/).map((tok) => {
      const m = /^(\[?)(\d{1,3})([:\d\-()ab]*)(.*)$/.exec(tok);
      if (!m) return tok;
      const [, open, num, range, tail] = m;
      return `${open ? "\\[" : ""}[[${PSALTER}BCP Psalm ${pad3(+num)}|${num}${range}]]${tail.replace(/\]/g, "\\]")}`;
    }).join(" ");
  }
  function lessonsMD(lines) {
    const joined = lines.join(" ").trim();
    if (!joined) return "—";
    const segs = splitLessons(joined);
    return segs.length >= 2 ? segs.join(" · ") : joined;
  }
  const noteLink = (noteKey, page, label) => `[[${FOLDER}${NOTE[noteKey]}|${label || `BCP p. ${page}`}]]`;

  return { FOLDER, NOTE, PSALTER, DAYS, MONTHS, MON3, mk, parts, iso, parseISO, add, daysBetween, longDate,
    easter, advent1, properDate, properForSunday, thanksgiving, frame, calendar, observances, eveMatches,
    parseSeasonal, parseHolyDays, splitLessons, buildData, resolve, describe, psalmsMD, lessonsMD, noteLink };
})();
// ---- CORE END ----

// ---------- Obsidian / Dataview rendering ----------
if (typeof dv !== "undefined") {
  const opts = (typeof input === "object" && input) ? input : {};
  // Where it draws (F3, 7 Oct 2026): Home passes the part of the page it made for this view. Without one, an element
  // of its own in the block, in place of any left by an earlier run of the block with the same date, so a re-render
  // that starts while that run is still reading the lectionary cannot show the Office twice.
  const KEY = "daily-office" + (opts.date ? " " + String(opts.date) : "");
  const container = opts.container || (() => {
    const el = dv.container.createDiv({ attr: { "data-vp-view": KEY } });
    const old = Array.from(dv.container.children).find((e) => e !== el && e.getAttribute("data-vp-view") === KEY);
    if (old) old.replaceWith(el);
    return el;
  })();
  const details = container.createEl("details", { cls: "daily-office" });
  // Dataview re-renders this block whenever a note changes (F4): whether it was opened or closed by hand is kept, per date,
  // on the block's container; {open: true} (the daily note) still opens it the first time. Opened by an error, it is not kept.
  const st = dv.container.__vpOpen || (dv.container.__vpOpen = {});
  const openKey = "office " + (opts.date ? (typeof opts.date === "string" ? opts.date : moment(opts.date).format("YYYY-MM-DD")) : moment().format("YYYY-MM-DD"));
  let failed = false;
  if (st[openKey] ?? opts.open) details.setAttribute("open", "");
  details.addEventListener("toggle", () => { if (!failed) st[openKey] = details.open; });
  const summaryEl = details.createEl("summary");
  const para = (md, cls) => dv.paragraph(md, { container: details, cls: cls || "daily-office-line", attr: { style: "margin: 0.15em 0 0.15em 1em;" } });
  try {
    const todayISO = opts.date ? (typeof opts.date === "string" ? opts.date : moment(opts.date).format("YYYY-MM-DD")) : moment().format("YYYY-MM-DD");
    const t = DO.parseISO(todayISO);
    if (t == null) throw new Error(`Bad date: ${opts.date}`);
    const folder = opts.folder || DO.FOLDER;
    const texts = {};
    for (const k of ["advent", "christmas", "epiphany", "lent", "easter", "pentecost", "holydays"]) {
      const f = folder ? app.vault.getAbstractFileByPath(`${folder}${DO.NOTE[k]}.md`) : app.metadataCache.getFirstLinkpathDest(DO.NOTE[k], "");
      if (!f) throw new Error(`Missing lectionary note: ${folder}${DO.NOTE[k]}.md`);
      texts[k] = await app.vault.cachedRead(f);
    }
    const data = DO.buildData(texts);
    // the choice between the Sunday's entry and the feast's (the holyday view; 18 Oct 2026); without it the Prayer Book's default stands
    let ropts = opts;
    try {
      const hs = await app.vault.adapter.read("Templates/Views/holyday/view.js");
      const hcore = hs.split("// ---- CORE " + "BEGIN")[1].split("// ---- CORE " + "END")[0].replace(/^[^\n]*\n/, "");
      const hi = (await new Function(hcore + "\nreturn HD;")().load(app)).info(todayISO);
      if (hi.cand && (hi.kind === "optional" || hi.kind === "after") && hi.feastUsed) ropts = { ...opts, useFeast: hi.cand.name };
      else if (hi.cand && hi.kind === "by-right" && !hi.feastUsed) ropts = { ...opts, useSunday: true };
      else if (hi.sundayUsed) ropts = { ...opts, skipFeast: true };
    } catch (e) { console.error("daily-office: the Holy Days choice could not be read", e); }
    const r = DO.resolve(t, data, ropts);
    summaryEl.setText(`Daily Office · ${r.cal.yearLabel} · ${r.summary}`);
    if (!r.blocks.length) {
      para(`No Daily Office entry found for **${r.summary}** (${r.cal.yearLabel}, ${DO.longDate(t)}). ${r.warnings.join(" ")} See ${DO.noteLink(r.cal.note || "holydays", null, "the lectionary note")}.`);
    }
    for (const b of r.blocks) {
      if (b.title) para(`**${b.title}**`);
      if (b.kind === "seasonal") {
        const ps = [];
        if (b.mp) ps.push(`Morning: ${DO.psalmsMD(b.mp)}`);
        if (b.ep) ps.push(`Evening: ${DO.psalmsMD(b.ep)}`);
        if (ps.length) para(`Psalms — ${ps.join(" · ")}`);
        para(`Lessons — ${DO.lessonsMD(b.lessons)}`);
      } else {
        para(`Psalms — ${DO.psalmsMD(b.psalms)} · Lessons — ${DO.lessonsMD(b.lessons)}`);
      }
      for (const f of b.footnotes) para(`<small>${f}</small>`);
    }
    for (const n of r.cal.notes) para(`<small>${n}</small>`);
    for (const w of r.warnings) para(`<small>${w}</small>`);
    const srcs = [...new Set(r.blocks.map((b) => `${b.noteKey}|${b.page}`))].map((s) => { const [k, p] = s.split("|"); return DO.noteLink(k, p); });
    para(`<small>${DO.longDate(t)} · ${r.cal.dayName} · ${srcs.join(" · ") || DO.noteLink(r.cal.note || "holydays", null, "lectionary")} · [[Daily Office Engine|about]]</small>`);
  } catch (err) {
    // shown open and in red, so the error is seen without opening the block (F3)
    console.error("daily-office", err);
    summaryEl.setText("Daily Office · error");
    failed = true;
    details.setAttribute("open", "");
    details.createDiv({ cls: "vp-view-error", text: `Could not build today's Daily Office: ${err && err.message ? err.message : err}`,
      attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
  }
}
