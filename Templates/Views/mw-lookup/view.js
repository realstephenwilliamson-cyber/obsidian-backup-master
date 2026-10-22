// Monier-Williams lookup box (Library/Sanskrit/Monier-Williams/monier-williams.tsv, 286,525 records of the 1899 dictionary,
// Cologne digitization). Type a headword in IAST (prakāśa) or plain letters (prakasa) and press Enter.
// The dictionary file (30 MB) is read on the first search and kept in memory until Obsidian restarts.
// Changed 7 Oct 2026 (phase 3): a dictionary file that cannot be read is reported instead of 'Loading…' for ever, and the
// headword column is found by its name in the header (F29 d); what was typed and found survives Dataview's re-render (F4).
const TSV = "Library/Sanskrit/Monier-Williams/monier-williams.tsv";
const plain = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z]/g, "");
// Dataview clears and re-runs this block whenever any note in the vault changes. The text typed, the last search and the
// entries opened are kept on the block's container, so they come back; opened anew, the note starts with an empty box.
const st = dv.container.__vpMw || (dv.container.__vpMw = { typed: "", q: "", open: new Map() });
const box = dv.el("div", "", { cls: "vp-mw" });
const field = box.createEl("input", { type: "search", attr: { placeholder: "Headword: prakāśa or prakasa, then Enter", style: "width: 100%; font-size: 1.1em; padding: 0.3em;" } });
field.value = st.typed;
const info = box.createEl("div", { attr: { style: "margin: 0.4em 0; opacity: 0.8;" } });
const out = box.createEl("div");
// the n-th tab-separated field of a line (0 = first), without splitting the whole line
const nth = (s, n) => { let a = 0; for (let k = 0; k < n; k++) { a = s.indexOf("\t", a) + 1; if (!a) return ""; } const b = s.indexOf("\t", a); return b < 0 ? s.slice(a) : s.slice(a, b); };
async function load() {
  if (window.__mw) return window.__mw;
  info.setText("Loading the dictionary (first search only)…");
  let raw;
  try { raw = await app.vault.adapter.read(TSV); }
  catch (e) { info.setText(`Could not read ${TSV}: ${e && e.message ? e.message : e}`); return null; }
  const lines = raw.split("\n"); const head = lines.shift().split("\t");
  const col = n => head.indexOf(n);
  const ci = { page: col("page_col"), hw: col("headword"), hp: col("headword_print"), hom: col("homonym"), text: col("text") };
  if (ci.hw < 0 || ci.text < 0) { info.setText(`${TSV} has no "headword" or "text" column in its first line.`); return null; }
  const keys = new Array(lines.length);
  for (let i = 0; i < lines.length; i++) keys[i] = plain(nth(lines[i], ci.hw));
  window.__mw = { lines, keys, ci };
  return window.__mw;
}
async function search(q) {
  if (q !== st.q) st.open.clear();
  st.q = q;
  const k = plain(q); out.empty(); if (!k) { info.setText(""); return; }
  const mw = await load(); if (!mw) return;
  const exact = [], prefix = [];
  for (let i = 0; i < mw.keys.length; i++) {
    if (mw.keys[i] === k) exact.push(i);
    else if (prefix.length < 40 && mw.keys[i].startsWith(k)) prefix.push(i);
  }
  const hits = exact.concat(prefix).slice(0, 40);
  info.setText(hits.length ? `${exact.length} exact match${exact.length === 1 ? "" : "es"}${prefix.length ? `, then words beginning with “${q}”` : ""} (showing ${hits.length})` : `No headword “${q}”. Try fewer letters.`);
  for (const i of hits) {
    const c = mw.lines[i].split("\t");
    const d = out.createEl("details", { attr: { style: "margin: 0.25em 0;" } });
    d.open = st.open.has(i) ? st.open.get(i) : exact.includes(i) && exact.length <= 6;
    d.addEventListener("toggle", () => st.open.set(i, d.open));
    const s = d.createEl("summary");
    s.createEl("b", { text: c[mw.ci.hp] || c[mw.ci.hw] });
    s.appendText(`${c[mw.ci.hom] ? " (" + c[mw.ci.hom] + ")" : ""} · p. ${String(c[mw.ci.page]).replace(",", ", col. ")}`);
    d.createEl("div", { text: c[mw.ci.text], attr: { style: "margin: 0.3em 0 0.6em 1.2em; white-space: pre-wrap;" } });
  }
}
field.addEventListener("input", () => { st.typed = field.value; });
field.addEventListener("keydown", e => { if (e.key === "Enter") search(field.value.trim()); });
if (st.q) search(st.q);
