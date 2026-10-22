// Quick capture (Home (mobile), and Home): a new blank note, a new handwritten note (a note in the inbox opened with an Ink
// writing section; Excalidraw until 21 Oct 2026), photos of the pages
// you mark in the printed books you are reading, and a form for adding a book you have only on paper.
// Photos go into one "Marked pages" note per book in the marked-pages folder, under a dated heading; the note links back to
// the book's catalog note, so the catalog note's backlinks show it.
// A book added with the form gets a catalog note in <catalog>/<Subject>/ with text: print and an empty files: list
// (Vault Guide -> The catalog), so it shows in the library browser, Currently reading and Physical Library like any other book.
// Changed 12 Oct 2026 (restructure): the catalog and marked-pages folders come from Templates/Views/paths.json.
// Changed 7 Oct 2026 (phase 3): a title or surname with no Latin letters no longer gives an empty file name, and an unused
// heading from an earlier click today is used again instead of repeated (F29 e, f).
// Also changed 7 Oct 2026: the filter and the "Add a book" form keep what was typed when Dataview redraws the block (D6 b, as
// F4 for the lookup boxes), and an error is shown in red instead of leaving the box silently missing (D4, as F3).
// Where it draws (D4): an element of its own in the block, in place of any left by an earlier run of the block.
const VIEW = "quick-capture", KEY = VIEW;
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
const PATHS = await (async () => { try { return JSON.parse(await app.vault.adapter.read("Templates/Views/paths.json")); } catch (e) { return {}; } })();
const CAT = PATHS.catalog || "Library/Catalog", MARKED = PATHS.markedPages || "Notes/Marked pages";
// Dataview clears and re-runs this block whenever any note in the vault changes (on the phone also when Sync brings in a
// file). What was typed in the filter and the form, the ticks, the subject, the last message and which parts were open are
// kept on the block's container, so they come back; opened anew, the note starts with an empty form.
const st = dv.container.__vpCapture || (dv.container.__vpCapture = { filter: "", fields: {}, ticks: {}, subject: "", msg: "", open: {} });
const keepOpen = (el, key) => { el.open = !!st.open[key]; el.addEventListener("toggle", () => { st.open[key] = el.open; }); };
const run = id => app.commands.executeCommandById(id);
const bar = dv.el("div", "", { container: root, cls: "vp-capture" });
bar.createEl("button", { text: "New note" }).onclick = () => run("file-explorer:new-file");
bar.createEl("button", { text: "New handwritten note" }).onclick = async () => { // 21 Oct 2026: Ink, not Excalidraw
  try {
    const name = `Notes/Handwritten ${moment().format("YYYY-MM-DD HH.mm")}.md`;
    const f = app.vault.getAbstractFileByPath(name) || await app.vault.create(name, `# Handwritten note, ${moment().format("D MMM YYYY, HH:mm")}\n\n`);
    const leaf = app.workspace.getLeaf(false); await leaf.openFile(f, { state: { mode: "source" } });
    app.workspace.setActiveLeaf(leaf, { focus: true }); // Ink's command is an editor command: it needs the focused editor
    if (!app.plugins.plugins["ink"]) { new Notice("Ink is not on on this device: the note is open; insert a writing section when it is."); return; }
    setTimeout(() => { // the cursor goes to the end right before the command: the editor restores its own cursor after opening
      const ed = leaf.view && leaf.view.editor; if (ed) { ed.focus(); ed.setCursor({ line: ed.lastLine(), ch: 0 }); }
      run("ink:create-handwritten-section");
    }, 700);
  } catch (e) { fail(e); }
};

// books: the ones you are reading first (status: reading), then the ones you own on paper (physical_copy)
const books = dv.pages(`"${CAT}"`)
  .where(p => p.status === "reading" || p.physical_copy === true)
  .sort(p => (p.status === "reading" ? "0" : "1") + String(p.title || p.file.name).toLowerCase())
  .array();
const det = dv.el("details", "", { container: root, cls: "vp-capture-books" });
keepOpen(det, "books");
const sum = det.createEl("summary");
const setCount = () => sum.setText(`Photograph marked pages (${books.length} books)`);
setCount();
const box = det.createEl("input", { type: "search", attr: { placeholder: "Filter by title or author", style: "width: 100%; margin: 0.4em 0;" } });
box.value = st.filter;
const ul = det.createEl("ul");
det.createEl("div", { text: "Not in the list? Add it with “Add a book you have on paper” below, or mark its catalog note as reading.", attr: { style: "opacity: 0.75; font-size: 0.9em;" } });

async function addScan(p) {
  const dir = MARKED, path = `${dir}/${p.file.name} - marked pages.md`, title = String(p.title || p.file.name); // "- marked pages" suffix since 19 Oct 2026 (audit G-02): no note shares a name with its catalog note
  if (!app.vault.getAbstractFileByPath(dir)) await app.vault.createFolder(dir);
  let f = app.vault.getAbstractFileByPath(path);
  if (!f) f = await app.vault.create(path,
    `---\ntype: marked-pages\nbook: "[[${p.file.path.replace(/\.md$/, "")}|${title.replace(/"/g, "'")}]]"\n---\n` +
    `# Marked pages: ${title}\n\nPhotos of the pages marked in the printed book, oldest first. Put the page number after each date.\n`);
  const leaf = app.workspace.getLeaf(false);
  await leaf.openFile(f, { state: { mode: "source" } });
  const ed = leaf.view?.editor; if (!ed) return;
  const last = ed.lastLine(), head = `### ${moment().format("D MMM YYYY")}, p. `;
  // a heading left by an earlier click today, with nothing under it yet, is used again rather than repeated
  let k = last; while (k > 0 && !ed.getLine(k).trim()) k--;
  if (ed.getLine(k).trim() !== head.trim()) ed.replaceRange(`\n${head}\n\n`, { line: last, ch: ed.getLine(last).length });
  else if (k === last) ed.replaceRange("\n\n", { line: last, ch: ed.getLine(last).length });
  ed.setCursor({ line: ed.lastLine(), ch: 0 }); ed.focus();
  setTimeout(() => run("editor:attach-file"), 400);   // on a phone this offers the camera or the photo library
}
function render(q) {
  ul.empty(); q = (q || "").toLowerCase();
  for (const p of books) {
    const label = `${p.title || p.file.name}${p.author && [].concat(p.author).length ? " · " + [].concat(p.author).join(", ") : ""}`;
    if (q && !label.toLowerCase().includes(q)) continue;
    const li = ul.createEl("li");
    const a = li.createEl("a", { text: label, href: "#" });
    a.onclick = e => { e.preventDefault(); addScan(p); };
    if (p.status === "reading") li.appendText(" (reading)");
  }
}
box.oninput = () => { st.filter = box.value; render(box.value); };
render(box.value);

// ---- Add a book you have on paper (no PDF) ----
const SUBJECTS = ["Philosophy", "Christianity", "Judaica", "Trika", "Hinduism", "Sanskrit-Study", "Biblical-Studies", "Other"];
const add = dv.el("details", "", { container: root, cls: "vp-capture-addbook" });
keepOpen(add, "add");
add.createEl("summary", { text: "Add a book you have on paper (no PDF)" });
const form = add.createEl("div", { attr: { style: "display: grid; gap: 0.35em; margin: 0.4em 0;" } });
const fieldStyle = "width: 100%;";
const mk = (key, ph, type = "text") => {
  const el = form.createEl("input", { type, attr: { placeholder: ph, style: fieldStyle } });
  el.value = st.fields[key] || "";
  el.addEventListener("input", () => { st.fields[key] = el.value; });
  return el;
};
const fTitle = mk("title", "Title (with diacritics if it has them)");
const fSub = mk("subtitle", "Subtitle (optional)");
const fAuth = mk("author", "Author(s), comma between names");
const fYear = mk("year", "Year", "number");
const fPub = mk("publisher", "Publisher (optional)");
const fSubj = form.createEl("select", { attr: { style: fieldStyle } });
for (const s of SUBJECTS) fSubj.createEl("option", { text: s, value: s });
if (SUBJECTS.includes(st.subject)) fSubj.value = st.subject;
fSubj.addEventListener("change", () => { st.subject = fSubj.value; });
const fLink = mk("link", "Where the details came from: a link (Google Books, publisher) (optional)", "url");
const ticks = form.createEl("div");
const tick = (key, label, on) => {
  const l = ticks.createEl("label", { attr: { style: "margin-right: 1.2em; white-space: nowrap;" } }); const c = l.createEl("input", { type: "checkbox" });
  c.checked = st.ticks[key] ?? on; c.addEventListener("change", () => { st.ticks[key] = c.checked; });
  l.appendText(" " + label); return c;
};
const fReading = tick("reading", "Reading now", true);
const fOwn = tick("own", "I own it on paper", true);
const btns = form.createEl("div");
const bAdd = btns.createEl("button", { text: "Add book" });
const bAddScan = btns.createEl("button", { text: "Add book and photograph pages" });
const msg = form.createEl("div", { attr: { style: "opacity: 0.85;" } });
msg.setText(st.msg);
const say = s => { st.msg = s; msg.setText(s); };

const ascii = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[‘’]/g, "'").replace(/[“”]/g, "")
  .replace(/[^\x20-\x7e]/g, "").replace(/[\\/:*?"<>|#^\[\]]/g, " ").replace(/\s+/g, " ").trim();
const q = s => JSON.stringify(s);   // a YAML double-quoted string
async function addBook(thenScan) {
  const title = fTitle.value.trim();
  if (!title) { say("A title is needed."); return; }
  const authors = fAuth.value.split(",").map(s => s.trim()).filter(Boolean);
  const year = parseInt(fYear.value, 10);
  const subject = fSubj.value;
  const surname = authors.length ? ascii(authors[0].split(/\s+/).pop()) : "";
  // a title in Devanagari or Hebrew script has no Latin letters for the file name: use a placeholder to rename later
  const short0 = ascii(title).slice(0, 80).trim(), short = short0 || `Untitled ${moment().format("YYYY-MM-DD HHmm")}`;
  const name = (surname ? `${surname} - ${short}` : short).trim();
  const dir = `${CAT}/${subject}`, path = `${dir}/${name}.md`;
  if (app.vault.getAbstractFileByPath(path)) { say(`There is already a catalog note “${name}”. Open it from the catalog, or change the title.`); return; }
  if (!app.vault.getAbstractFileByPath(dir)) await app.vault.createFolder(dir);
  const link = fLink.value.trim();
  const today = moment().format("D MMM YYYY");
  const fm = [
    "---",
    `title: ${q(title)}`,
    `subtitle: ${q(fSub.value.trim())}`,
    authors.length ? "author:\n" + authors.map(a => `  - ${q(a)}`).join("\n") : "author: []",
    "editor: []",
    "translator: []",
    `year: ${Number.isFinite(year) ? year : ""}`,
    `publisher: ${q(fPub.value.trim())}`,
    'series: ""',
    'volume: ""',
    'container: ""',
    `subject:\n  - ${subject}`,
    "type: book",
    "language:\n  - English",
    "pages: ",
    "text: print",
    `status: ${fReading.checked ? "reading" : "keep"}`,
    `physical_copy: ${fOwn.checked}`,
    "files: []",
    "aliases: []",
    "---",
  ].join("\n");
  const full = fSub.value.trim() ? `${title}: ${fSub.value.trim()}` : title;
  const body = `\n\n# ${full}\n\n**On paper only:** there is no digital copy in the vault (text: print). ` +
    (link ? `Details from [this page](${link}), added on ${today}.` : `Details typed in on ${today}; check them against the title page when you can.`) +
    `\n\nPages you photograph with *Photograph marked pages* on Home go to ${MARKED}/ and show in this note's backlinks.\n`;
  const f = await app.vault.create(path, fm + body);
  const p = { file: { name, path: f.path }, title, author: authors, status: fReading.checked ? "reading" : "keep" };
  books.unshift(p); setCount(); render(box.value);
  say(`Added “${name}” to ${CAT}/${subject}.` + (short0 ? "" : " The title has no Latin letters, so the file name is a placeholder: rename the note in Obsidian."));
  if (window.Notice) new Notice(`Added “${name}” to ${CAT}/${subject}`);
  for (const el of [fTitle, fSub, fAuth, fYear, fPub, fLink]) el.value = "";
  st.fields = {};
  if (thenScan) await addScan(p);
}
bAdd.onclick = () => addBook(false);
bAddScan.onclick = () => addBook(true);
} catch (e) { fail(e); }
