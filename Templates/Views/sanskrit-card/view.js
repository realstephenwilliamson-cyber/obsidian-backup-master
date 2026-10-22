// Daily Sanskrit card for the 108-day cycle (card 1 = 2026-10-03).
// Used by Home, the Daily Letter Cycle note and daily notes:
//   await dv.view("Templates/Views/sanskrit-card")                 -> today's card
//   await dv.view("Templates/Views/sanskrit-card", {date: "2026-10-05"}) -> that day's card
// All card data comes from the Flashcard Register table, so fixing a row there fixes it everywhere.
// Changed 7 Oct 2026 (D4, as F3 for the Today block): the card draws into an element of its own in the block, in place of any
// left by an earlier run of the block (same date), so a re-render that starts while that run is still reading the register
// cannot show the card twice; an error is shown in red instead of leaving the card silently missing.
const VIEW = "sanskrit-card", KEY = VIEW + (input && input.date ? " " + String(input.date).slice(0, 10) : "");
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
try { // (the body is not indented, to keep the change small)
const EPOCH = await (async () => { try { return JSON.parse(await app.vault.adapter.read("Templates/Views/paths.json")).letterCycleStart || "2026-10-03"; } catch (e) { return "2026-10-03"; } })(); // one copy in paths.json since 19 Oct 2026
// 12 Oct 2026 (restructure): the register and the notes linked below are found by name, so their folder can move.
const REGISTER = app.metadataCache.getFirstLinkpathDest("Sanskrit 108 Flashcard Register", "")?.path || "Sanskrit 108 Flashcard Register.md";
const DRAWING = "Excalidraw/Matrika-sarira - 108-day drawing.excalidraw";
const when = input && input.date ? moment(String(input.date).slice(0, 10)) : moment();
const n = ((when.clone().startOf("day").diff(moment(EPOCH), "days") % 108) + 108) % 108 + 1;
const file = app.vault.getAbstractFileByPath(REGISTER);
if (!file) {
  dv.paragraph("Flashcard Register not found at " + REGISTER, { container: root });
} else {
  const text = await app.vault.cachedRead(file);
  const split = l => {
    const out = []; let cur = "", depth = 0;
    for (let i = 0; i < l.length; i++) {
      if (l.startsWith("[[", i)) { depth++; cur += "[["; i++; continue; }
      if (l.startsWith("]]", i)) { depth--; cur += "]]"; i++; continue; }
      const c = l[i];
      if (c === "|" && depth === 0 && l[i - 1] !== "\\") { out.push(cur); cur = ""; } else cur += c;
    }
    out.push(cur);
    return out.slice(1, -1).map(s => s.trim());
  };
  const row = text.split("\n").find(l => new RegExp("^\\|\\s*" + n + "\\s*\\|").test(l));
  if (!row) {
    dv.paragraph("Card " + n + " is not in the register.", { container: root });
  } else {
    const c = split(row);
    const plain = s => s.replace(/<[^>]+>/g, "").replace(/\*\*/g, "").trim();
    const img = s => (s.match(/!\[\[([^\]|\\]+)/) || [])[1];
    dv.paragraph(`**Sanskrit card ${n} of 108** · ${plain(c[1])} ${plain(c[2])} · ${plain(c[3])} · ${plain(c[4])}`, { container: root });
    const box = dv.el("div", "", { container: root, cls: "vp-card-row", attr: { style: "display:flex;flex-wrap:wrap;gap:1em;margin:.4em 0;" } });
    for (const p of [img(c[5]), img(c[6])]) {
      const f = p && (app.vault.getAbstractFileByPath(p) || app.metadataCache.getFirstLinkpathDest(p, REGISTER));
      if (f) box.createEl("img", { attr: { src: app.vault.getResourcePath(f), alt: p.split("/").pop(),
        style: "width:46%;max-width:300px;height:auto;border-radius:6px;border:1px solid var(--background-modifier-border);" } });
    }
    const placement = c.length > 8 ? plain(c[8]) : "";
    if (placement && placement !== "—") dv.paragraph(`**Body place** ([[Scriptural Anatomical Mapping (Anga-sthana)|TĀ 15.117–120]]): ${placement}`, { container: root });
    dv.paragraph(`[[Sanskrit 108 Flashcard Register|Register]] · [[Sanskrit Daily Letter Cycle|About the cycle]]`, { container: root });
  }
}
} catch (e) { fail(e); }
