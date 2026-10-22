// Today's study items: the CIS step and the day's letter card (made 19 Oct 2026 from the Fable design of 9 Oct 2026,
// "Planner and letters design" §3 and "CIS study plan - decisions" 12).
//   await dv.view("Templates/Views/today-items", {date: "2026-10-20"})  -> both lines for that day (the daily note's "## Today")
//   await dv.view("Templates/Views/today-items", {only: "cis"})        -> the CIS line for today only (Home, Home (mobile))
// The CIS line (Monday to Friday, from cis_start on): the first unticked step "- [ ] N.k …" in the note "CIS study plan",
// with that day's session length from its properties cis_mwf (Mon, Wed, Fri) or cis_tth (Tue, Thu). On Tuesday and Thursday,
// when the current step is a M/W/F step, the line says "review" and names the step as next. Nothing on Saturday or Sunday.
// Nothing is copied into the note, so ticking a step changes the line everywhere; in a note for another day the line is the
// plan's current step, not that day's.
// The letter line: the card of the 108-day cycle (card 1 = 3 Oct 2026, the same count as sanskrit-card, phoneme-card and
// today-header), linked to its note "Card NNN …" (Study/Sanskrit/Flashcards); until those notes exist, the register's row.
// The Tantrāloka portion and the Daily Office are not drawn here: the daily note has them (the template writes the portion,
// the daily-office view draws the Office), and on Home the today-study and daily-office views draw them.
// Notes are found by name, not folder (as the other views since 12 Oct 2026).
const VIEW = "today-items";
const KEY = VIEW + (input && input.date ? " " + String(input.date).slice(0, 10) : "") + (input && input.only ? " " + input.only : "");
const root = (() => {
  const el = dv.container.createDiv({ attr: { "data-vp-view": KEY } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-vp-view") === KEY);
  if (old) old.replaceWith(el);
  return el;
})();
const fail = e => {
  console.error(VIEW, e);
  root.createDiv({ cls: "vp-view-error", text: `${VIEW} failed: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
try {
const EPOCH = await (async () => { try { return JSON.parse(await app.vault.adapter.read("Templates/Views/paths.json")).letterCycleStart || "2026-10-03"; } catch (e) { return "2026-10-03"; } })(); // one copy in paths.json since 19 Oct 2026
const byName = n => app.metadataCache.getFirstLinkpathDest(n, "");
const DATE = input && input.date ? String(input.date).slice(0, 10) : moment().format("YYYY-MM-DD");
const day = moment(DATE, "YYYY-MM-DD");
const wd = day.day();                                   // 0 Sunday … 6 Saturday
const isToday = DATE === moment().format("YYYY-MM-DD");
const want = k => !(input && input.only) || input.only === k;
const lines = [];

// ---- CIS ----
if (want("cis") && wd >= 1 && wd <= 5) {
  const plan = byName("CIS study plan");
  if (!plan) lines.push("**CIS:** the note *CIS study plan* was not found.");
  else {
    const fm = app.metadataCache.getFileCache(plan)?.frontmatter || {};
    const start = fm.cis_start ? moment(String(fm.cis_start).slice(0, 10), "YYYY-MM-DD") : null;
    if (!start || !day.isBefore(start, "day")) {
      const heavy = wd === 1 || wd === 3 || wd === 5;
      const min = heavy ? fm.cis_mwf : fm.cis_tth;
      const mins = min ? ` · ${min} min` : "";
      const link = `[[${plan.basename}|plan]]`;
      const m = (await app.vault.cachedRead(plan)).split("\n")
        .map(l => l.match(/^\s*- \[[ /]\] (\d+a?\.\d+) (.+?)\s*$/)).find(Boolean); // [ ] or [/] (In Progress) counts as the current step (19 Oct 2026)
      if (!m) lines.push(`**CIS:** every step is ticked · ${link}`);
      else {
        const kind = (m[2].match(/—\s*(M\/W\/F|T\/Th)$/) || [])[1];
        const step = `${m[1]} ${m[2].replace(/\s*—\s*(M\/W\/F|T\/Th)$/, "")}`;
        const later = isToday ? "" : " *(the plan's current step)*";
        lines.push(!heavy && kind === "M/W/F"
          ? `**CIS:** review (the cards that are due)${mins} · next: ${step} · ${link}${later}`
          : `**CIS:** ${step}${mins} · ${link}${later}`);
      }
    }
  }
}

// ---- the letter card of the 108-day cycle ----
if (want("letter")) {
  const n = ((day.clone().startOf("day").diff(moment(EPOCH, "YYYY-MM-DD"), "days") % 108) + 108) % 108 + 1;
  const pad = String(n).padStart(3, "0");
  const mark = s => (/^\p{M}/u.test(s || "") ? "◌" + s : (s || ""));   // a vowel sign or other mark on a dotted circle
  const note = app.vault.getMarkdownFiles().find(f => f.basename.startsWith(`Card ${pad} `));
  let label;
  if (note) {
    const fm = app.metadataCache.getFileCache(note)?.frontmatter || {};
    label = `[[${note.basename}|${(mark(fm.devanagari) + " " + (fm.iast || "")).trim() || note.basename}]]`;
  } else {
    // until the card notes exist: the register's row (the same table sanskrit-card reads)
    label = `card ${n}`;
    const reg = byName("Sanskrit 108 Flashcard Register");
    if (reg) {
      const row = (await app.vault.cachedRead(reg)).split("\n").find(l => new RegExp("^\\|\\s*" + n + "\\s*\\|").test(l));
      if (row) {
        const c = row.split(/(?<!\\)\|/).slice(1, -1).map(s => s.replace(/<[^>]+>/g, "").replace(/\*\*/g, "").trim());
        label = `${mark(c[2])} ${c[1]}`;
      }
    }
    label += " · [[Sanskrit Daily Letter Cycle|the card]]";
  }
  lines.push(`**Letter:** card ${n} of 108 · ${label} · write it, then review the cards that are due (Spaced Repetition)`);
}

for (const l of lines) dv.paragraph(l, { container: root });
} catch (e) { fail(e); }
