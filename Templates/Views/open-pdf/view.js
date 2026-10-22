// Catalog box (the open-pdf view), revised Oct 2026: "Read in the vault" for each Markdown copy, then "Open the PDF".
// Reads the note's `files:` list. A Markdown copy opens in Obsidian (Ctrl/Cmd-click: new tab); it is on every device.
// A PDF opens in the computer's default PDF app, outside Obsidian, so large PDFs do not slow the vault.
// On a phone or tablet the PDF is not synced, so the box says it is on the computer (decided by what the note lists,
// not by what resolves). A listed PDF that is missing on the computer is named, not skipped.
const page = dv.current();
const box = dv.el("div", "", { cls: "open-pdf-view" });
const raw = [].concat(page?.file?.frontmatter?.files ?? []);
const reads = [], pdfs = [], missingPdfs = [];
let pdfListed = 0;
for (const v of raw) {
  const m = String(v).match(/\[\[([^\]|#]+)/);
  if (!m) continue;
  const target = m[1].trim();
  const low = target.toLowerCase();
  if (low.endsWith(".pdf")) {
    pdfListed++;
    const f = app.metadataCache.getFirstLinkpathDest(target, page.file.path);
    if (f) pdfs.push(f); else missingPdfs.push(target.split("/").pop());
  } else if (!/\.(djvu|txt|epub|docx?|tsv)$/.test(low)) {
    const f = app.metadataCache.getFirstLinkpathDest(target, page.file.path);
    if (f && f.extension === "md" && f.path !== page.file.path && !reads.some(r => r.path === f.path)) reads.push(f);
  }
}
// Several copies: by name, numbers in order (vol 2 before vol 10).
if (reads.length > 1) reads.sort((a, b) => a.basename.localeCompare(b.basename, undefined, { numeric: true }));
// Notes in a book: when the copy's first note is its folder's folder note, count the folder's notes.
const notesIn = f => {
  const dir = f.parent;
  if (!dir || dir.name !== f.basename) return 1;
  let n = 0;
  const walk = d => { for (const c of d.children) { if (c.children) walk(c); else if (c.extension === "md") n++; } };
  walk(dir);
  return n;
};
for (const f of reads) {
  const row = box.createDiv({ cls: "open-pdf-row" });
  const b = row.createEl("button", { text: reads.length > 1 ? `Read in the vault: ${f.basename}` : "Read in the vault", cls: "mod-cta" });
  b.style.marginRight = "0.5em";
  b.onclick = evt => app.workspace.openLinkText(f.path, page.file.path, evt.ctrlKey || evt.metaKey);
  const n = notesIn(f);
  row.createSpan({ text: n > 1 ? `contents and ${n - 1} more notes` : "one note", cls: "open-pdf-hint" });
}
if (pdfListed) {
  const row = box.createDiv({ cls: "open-pdf-row" });
  if (app.isMobile) {
    row.createEl("p", { text: pdfListed > 1 ? "The PDFs are on the computer." : "The PDF is on the computer." });
  } else {
    for (const f of pdfs) {
      const b = row.createEl("button", { text: pdfs.length > 1 ? `Open the PDF: ${f.basename}` : "Open the PDF" });
      b.style.marginRight = "0.5em";
      b.onclick = () => app.openWithDefaultApp(f.path);
    }
    for (const name of missingPdfs) row.createEl("p", { text: `PDF listed but not found: ${name}` });
  }
}
if (!reads.length && !pdfListed) box.createEl("p", { text: "No PDF or Markdown copy in this note's files." });
