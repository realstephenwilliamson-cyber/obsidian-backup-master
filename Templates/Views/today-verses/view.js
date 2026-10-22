// Today's Tantrāloka portion: for each verse, the mūla (Devanagari and IAST) and below it Dyczkowski's English, read
// from the verse note's [!source] callout (phase 5, 12 Oct 2026). A paragraph he gives for several verses is shown once,
// under the first of them; the later verses point back to it. Below the verses, a fold for the portion's first page:
// the page in the Markdown copy of his volume (every device) and, on the computer only, the PDF page.
// Used by Home:  await dv.view("Templates/Views/today-verses", { container })  (the part of the page Home made for it)
//         a given day:  await dv.view("Templates/Views/today-verses", {date: "2026-10-05"})
//         (without a container it draws into an element of its own in the block)
// Changed 7 Oct 2026 (F4): the verses and the translation stay open after Dataview redraws the block.
// Changed 12 Oct 2026 (phase 5): the English inline; the fold gives the Markdown page, and the PDF only on the computer.
// The portion comes from the study-plan tables; the text from each verse note's ^mula and ^iast blocks and its callout.
const dir = "Texts/Tantraloka/Study plan/";
const day = input && input.date ? String(input.date).slice(0, 10) : moment().format("YYYY-MM-DD");
// Where it draws (F3, 7 Oct 2026): Home passes the part of the page it made for this view ({container}). Without one,
// the view makes an element of its own in the block, in place of any left by an earlier run of the block (same
// view and date), so a re-render that starts while that run is still reading files cannot show it twice. It is made
// before the first await, so it keeps its place.
const VIEW = "today-verses", KEY = `${VIEW} ${day}`;
const root = input && input.container ? input.container : (() => {
  const el = dv.container.createDiv({ attr: { "data-vp-view": KEY } });
  const old = Array.from(dv.container.children).find(e => e !== el && e.getAttribute("data-vp-view") === KEY);
  if (old) old.replaceWith(el);
  return el;
})();
// An error is shown here, in red, instead of leaving this part of the page silently empty.
const fail = e => {
  console.error(VIEW, e);
  root.createDiv({ cls: "vp-view-error", text: `${VIEW} failed: ${e && e.message ? e.message : e}`,
    attr: { style: "color: var(--text-error); border-left: 3px solid var(--text-error); padding: .2em .6em; margin: .3em 0;" } });
};
// The translation callout of a verse note: volume, Markdown page link, PDF link, numbering line, paragraphs.
// "> [!source] Dyczkowski, vol. N" / "> [[<chapter note>#^pgK|p. N]] ([pdf](<…pdf#page=K>))" / "> <numbering line>" /
// ">" / "> <paragraph>" …
const readCallout = t => {
  const m = t.match(/> \[!source\] (Dyczkowski, vol\. [IVXL]+)[ \t]*\n> \[\[([^\]|#]+)#\^pg(\d+)\|(pp?\. [^\]]+)\]\] \(\[pdf\]\(<([^>]+?\.pdf)#page=(\d+)>\)\)((?:\n>[^\n]*)*)/);
  if (!m) return null;
  const lines = m[7].split("\n").slice(1).map(l => l.replace(/^>\s?/, ""));
  const notes = [], paras = [];
  let seenBlank = false;
  for (const l of lines) {
    if (!l.trim()) { seenBlank = true; continue; }
    if (!seenBlank) notes.push(l); else paras.push(l);
  }
  return { vol: m[1], mdNote: m[2], K: m[3], label: m[4], pdf: m[5], pdfPage: m[6], notes, paras };
};
const mobile = !!(app.isMobile);
try { // (the body is not indented, to keep the change small)
let row = null;
for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith(dir))) {
  const l = (await app.vault.cachedRead(f)).split("\n").find(x => x.startsWith(`| ${day} |`));
  if (l) { row = l.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim()); break; }
}
// Dataview re-renders this block whenever a note changes (F4): which parts were open is kept, per day, on the block's container
const st = dv.container.__vpOpen || (dv.container.__vpOpen = {});
const keepOpen = (el, key) => { el.open = !!st[key]; el.addEventListener("toggle", () => { st[key] = el.open; }); };
const ends = row ? [...(row[3] || "").matchAll(/\[\[Tantraloka (\d\d)\.(\d{3})/g)].map(m => [+m[1], +m[2]]) : [];
if (ends.length) {
  const name = (c, v) => `Tantraloka ${String(c).padStart(2, "0")}.${String(v).padStart(3, "0")}`;
  const note = (c, v) => app.metadataCache.getFirstLinkpathDest(name(c, v), "");
  // every verse from the first link to the last, crossing into the next āhnika if the portion does
  const [c0, v0] = ends[0], [c1, v1] = ends[ends.length - 1], list = [];
  // a missing verse number inside the portion is skipped, not taken as the end (A16); at most 400 numbers are tried
  let tried = 0, missing = 0;
  for (let c = c0, v = v0; tried < 400; v++, tried++) {
    if (c === c1 && v > v1) break;
    if (!note(c, v)) { if (c < c1 && !note(c, v + 1) && !note(c, v + 2)) { c++; v = 0; continue; } missing++; continue; }
    list.push([c, v]);
    if (c === c1 && v === v1) break;
  }
  if (list.length) {
    const det = dv.el("details", "", { container: root, cls: "vp-verses" });
    keepOpen(det, "verses " + day);
    const range = list.length === 1 ? `${c0}.${v0}` : `${c0}.${v0}–${c1 === c0 ? "" : c1 + "."}${v1}`;
    det.createEl("summary", { text: `Today's verses: ${range} (${list.length}${missing ? `; ${missing} verse number${missing > 1 ? "s" : ""} not in the vault` : ""})` });
    const shown = new Map();   // paragraph text (without its "(with …)") -> the verse under which it was shown
    let first = null;
    for (const [c, v] of list) {
      const t = await app.vault.cachedRead(note(c, v));
      const mula = (t.match(/## Mūla\s*\n([\s\S]*?)\s*\^mula/) || [])[1];
      const iast = (t.match(/\^mula\s*\n([\s\S]*?)\s*\^iast/) || [])[1];
      const box = det.createDiv({ cls: "vp-verse", attr: { style: "margin: 0.6em 0 0.9em;" } });
      dv.el("div", `[[${name(c, v)}|${c}.${v}]]`, { container: box, cls: "vp-verse-no" });
      if (mula) dv.el("div", mula.trim().split("\n").join("<br>"), { container: box, cls: "vp-verse-deva", attr: { lang: "sa", style: "font-size: 1.3em; line-height: 1.6;" } });
      if (iast) dv.el("div", "*" + iast.trim().split("\n").join("*<br>*") + "*", { container: box, cls: "vp-verse-iast" });
      const tr = readCallout(t);
      if (!tr) continue;
      if (!first) first = tr;
      const en = box.createDiv({ cls: "vp-verse-en", attr: { style: "margin-top: .4em; padding-left: .7em; border-left: 2px solid var(--background-modifier-border);" } });
      for (const n of tr.notes) dv.el("div", n, { container: en, cls: "vp-verse-en-note", attr: { style: "font-size: .85em; color: var(--text-muted);" } });
      for (const p of tr.paras) {
        const key = p.replace(/ \(with [^)]*\)$/, "");
        const w = (p.match(/ \(with ([^)]*)\)$/) || [])[1];
        if (shown.has(key)) {
          dv.el("div", `↑ ${w ? `(${w}) ` : ""}the same paragraph as under ${shown.get(key)}`, { container: en, cls: "vp-verse-en-same", attr: { style: "font-size: .85em; color: var(--text-muted); margin: .2em 0;" } });
          continue;
        }
        shown.set(key, `${c}.${v}`);
        dv.el("div", p, { container: en, cls: "vp-verse-en-para", attr: { style: "margin: .25em 0;" } });
      }
    }
    // the portion's first page in Dyczkowski's volume: the Markdown copy on every device; the PDF page on the computer only
    if (first) {
      const d2 = dv.el("details", "", { container: root, cls: "vp-translation" });
      d2.createEl("summary", { text: `${first.vol}, ${first.label}: the page${mobile ? "" : " and the PDF"}` });
      let drawn = false;
      d2.addEventListener("toggle", () => {
        if (!d2.open || drawn) return; drawn = true;
        dv.el("div", `[[${first.mdNote}#^pg${first.K}|${first.vol}, ${first.label} (Markdown copy)]]`, { container: d2 });
        if (mobile) dv.el("div", "The PDF is on the computer.", { container: d2, attr: { style: "font-size: .85em; color: var(--text-muted);" } });
        else dv.el("div", `![[${first.pdf}#page=${first.pdfPage}&height=720]]`, { container: d2 });
      });
      keepOpen(d2, "translation " + day);
    }
  }
}
} catch (e) { fail(e); }
