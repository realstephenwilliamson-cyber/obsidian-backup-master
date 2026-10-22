// The phoneme of the day (D18, 13 Oct 2026): one of the Tantrāloka's 108 most frequent conjuncts, in a 108-day cycle that
// keeps the dates of the letter cycle (day 1 = 3 Oct 2026). Shows the conjunct, its letters (linked to their notes, with
// their body places), how often it occurs in the mūla, and words that contain it: from the day's verses in the study plan
// when there are any, otherwise the most frequent words from the whole mūla.
//   await dv.view("Templates/Views/phoneme-card")                       -> today
//   await dv.view("Templates/Views/phoneme-card", {date: "2026-10-20"}) -> that day
//   add {compact: true} for one line and the words (Home)
// Data: Templates/Views/phoneme-card/data.json (the 108 conjuncts, the letter notes' names and body places, and example
// words), written by a runner job from the verse notes; the table in "Conjunct cycle (Tantraloka)" was made from the same count.
const VIEW = "phoneme-card", KEY = VIEW + (input && input.date ? " " + String(input.date).slice(0, 10) : "");
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
const D = JSON.parse(await app.vault.adapter.read("Templates/Views/phoneme-card/data.json"));
const when = input && input.date ? moment(String(input.date).slice(0, 10)) : moment();
const day = when.format("YYYY-MM-DD");
const n = ((when.clone().startOf("day").diff(moment(EPOCH), "days") % 108) + 108) % 108 + 1;
const c = D.clusters[n - 1]; // {cl, count, iast, letters: [devanagari...], words: [[word, count, verse]...]}
const lk = d => { const L = D.letters[d]; return L ? `[[${L.note}|${d}]]` : d; };
// words from the day's verses: the study plan's row for the day names its first and last verse
const re = new RegExp("(?<![क-ह]्)" + c.cl + "(?!्)");
let today = [];
try {
  const dir = "Texts/Tantraloka/Study plan/";
  let cells = null;
  for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith(dir))) {
    const line = (await app.vault.cachedRead(f)).split("\n").find(l => l.startsWith(`| ${day} |`));
    if (line) { cells = line.split(/(?<!\\)\|/).slice(1, -1).map(s => s.trim()); break; }
  }
  const m = cells ? [...cells[3].matchAll(/Tantraloka (\d\d)\.(\d\d\d)/g)] : [];
  if (m.length) {
    const ch = m[0][1], seen = new Map();
    for (let v = +m[0][2]; v <= +m[m.length - 1][2]; v++) {
      const name = `Tantraloka ${ch}.${String(v).padStart(3, "0")}`, f = app.metadataCache.getFirstLinkpathDest(name, "");
      if (!f) continue;
      const mm = (await app.vault.cachedRead(f)).match(/## Mūla\s*\n([\s\S]*?)\s*\^mula/);
      if (!mm) continue;
      for (const w of mm[1].split(/[\s।॥|,.;:!?'"()\[\]0-9०-९-]+/)) if (w && re.test(w) && !seen.has(w)) seen.set(w, `${+ch}.${v}`);
    }
    today = [...seen].slice(0, 6);
  }
} catch (e) { console.error(VIEW, e); }
const big = `<span style="font-size:2.2em; line-height:1.1">${c.cl}</span>`;
const words = today.length
  ? "In today's verses: " + today.map(([w, ref]) => `${w} ([[Tantraloka ${ref.split(".")[0].padStart(2, "0")}.${ref.split(".")[1].padStart(3, "0")}|${ref}]])`).join(" · ")
  : "Often in the mūla: " + c.words.slice(0, 6).map(([w, k, ref]) => `${w} (${k}×)`).join(" · ");
if (input && input.compact) {
  dv.paragraph(`**Phoneme of the day ${n} of 108** · ${big} ${c.iast} · ${c.letters.map(lk).join(" + ")} · ${c.count.toLocaleString("en")} times in the mūla · [[Conjunct cycle (Tantraloka)|cycle]]`, { container: root });
  dv.paragraph(words, { container: root });
} else {
  dv.paragraph(`**Phoneme of the day ${n} of 108** · ${big} ${c.iast}`, { container: root });
  dv.paragraph(`**Letters:** ` + c.letters.map(d => `${lk(d)} ${D.letters[d] ? D.letters[d].iast : ""}` + (D.letters[d] && D.letters[d].nyasa ? ` (body place: ${D.letters[d].nyasa})` : "")).join(" + "), { container: root });
  dv.paragraph(`**In the Tantrāloka mūla:** ${c.count.toLocaleString("en")} times (day ${n} of the 108 most frequent conjuncts)`, { container: root });
  dv.paragraph(words, { container: root });
  dv.paragraph(`[[Conjunct cycle (Tantraloka)|The cycle]] · [[Letters|The fifty letters]]`, { container: root });
}
} catch (e) { fail(e); }
