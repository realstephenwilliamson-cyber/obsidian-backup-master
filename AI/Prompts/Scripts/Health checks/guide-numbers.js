(async () => {
  // Read-only: the numbers the Guide and Welcome state. Writes .work/out/s86j-numbers.json.
  const V = app.vault, MC = app.metadataCache; const out = {};
  const cats = V.getMarkdownFiles().filter(f => f.path.startsWith('Catalog/') && !/\/[^/]+\/[^/]+\.md$/.test(f.path) === false);
  let catalog = 0, withMd = 0, pdfOnly = 0, print = 0, text = 0; const pdfOnlyBySubject = {}, bySubject = {};
  for (const f of V.getMarkdownFiles()) {
    if (!f.path.startsWith('Catalog/')) continue; const fm = (MC.getFileCache(f) || {}).frontmatter; if (!fm || !fm.title) continue;
    const parts = f.path.split('/'); if (parts.length < 3 || parts[2] === parts[1] + '.md') continue;
    catalog++; const subj = Array.isArray(fm.subject) ? fm.subject[0] : fm.subject; bySubject[subj] = (bySubject[subj] || 0) + 1;
    const files = Array.isArray(fm.files) ? fm.files : [];
    const dests = files.map(e => { const m = String(e).match(/\[\[([^\]|#]+)/); return m && MC.getFirstLinkpathDest(m[1], f.path); }).filter(Boolean);
    const md = dests.some(d => d.extension === 'md' && d.path.startsWith('Library/')), lib = dests.some(d => d.extension !== 'md' && d.path.startsWith('Library/'));
    if (fm.type === 'text') text++;
    else if (fm.text === 'print' || !dests.length) print++;
    else if (md) withMd++;
    else if (lib) { pdfOnly++; pdfOnlyBySubject[subj] = (pdfOnlyBySubject[subj] || 0) + 1; }
  }
  out.catalog = { catalog, withMd, pdfOnly, print, text, bySubject, pdfOnlyBySubject };
  const files = V.getFiles(); const sz = {}; let total = 0;
  for (const f of files) { total += f.stat.size; const e = f.extension; sz[e] = (sz[e] || 0) + f.stat.size; }
  out.size = { totalGB: +(total / 1e9).toFixed(2), pdfGB: +((sz.pdf || 0) / 1e9).toFixed(2), pdfFiles: files.filter(f => f.extension === 'pdf').length, pdfOver5MB: files.filter(f => f.extension === 'pdf' && f.stat.size > 5e6).length, txtGB: +((sz.txt || 0) / 1e9).toFixed(2), mdGB: +((sz.md || 0) / 1e9).toFixed(2), imagesMB: Math.round(((sz.jpeg || 0) + (sz.jpg || 0) + (sz.png || 0) + (sz.svg || 0)) / 1e6), djvuMB: Math.round((sz.djvu || 0) / 1e6), tsvMB: Math.round((sz.tsv || 0) / 1e6), docxMB: Math.round(((sz.docx || 0) + (sz.doc || 0) + (sz.pptx || 0)) / 1e6) };
  const noPdf = total - (sz.pdf || 0); const mukta = files.filter(f => f.path.startsWith('Texts/MUKTABODHA-LIBRARY-')).reduce((a, f) => a + f.stat.size, 0); const orig = files.filter(f => f.path.startsWith('Projects/_Originals/')).reduce((a, f) => a + f.stat.size, 0);
  out.sync = { noPdfGB: +(noPdf / 1e9).toFixed(2), muktaGB: +(mukta / 1e9).toFixed(2), originalsMB: Math.round(orig / 1e6), laptopRemoteGB: +((noPdf - mukta) / 1e9).toFixed(2), phoneGB: +((noPdf - mukta - orig) / 1e9).toFixed(2) };
  out.counts = { notes: V.getMarkdownFiles().length, files: files.length, zoharVols: V.getMarkdownFiles().filter(f => /^Texts\/Zohar\/Zohar \d+ - /.test(f.path)).length, convertedNotes: V.getMarkdownFiles().filter(f => { const fm = (MC.getFileCache(f) || {}).frontmatter; return fm && fm.source_pdf; }).length, taVerses: V.getMarkdownFiles().filter(f => /^Texts\/Tantraloka\/Ahnika \d+\/Tantraloka \d+\.\d+\.md$/.test(f.path)).length };
  out.exists = {}; for (const p of ['Notes/Marked pages', 'Notes/Mini Notes', 'Journal/Weeks', 'Excalidraw/Matrika-sarira - 108-day drawing.excalidraw.md', 'Catalog/Scholars', 'AI/AI chats', 'AI/Vault analysis (6 Oct 2026)', 'AI/Archive/Phase 2 changes (6 Oct 2026).md']) out.exists[p] = !!V.getAbstractFileByPath(p);
  out.scholars = V.getMarkdownFiles().filter(f => f.path.startsWith('Catalog/Scholars/')).map(f => f.basename);
  await V.adapter.write('.work/out/s86j-numbers.json', JSON.stringify(out, null, 1));
  return JSON.stringify(out).slice(0, 1500);
})()
