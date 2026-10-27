(async () => {
  // pf269 (26 Oct 2026, third session): read-only. Soft hyphens: Brown's PDF stored every hyphen as U+00AD, which the converter drops.
  // For every converted book whose index note says its text came from the PDF's own text layer (born-digital), sample up to 14 pages
  // with Obsidian's pdf.js and count: U+00AD inside a line (followed by a letter or digit in the same text item), U+00AD at item end,
  // ASCII hyphens, en and em dashes. Brown is the control. Writes .work/out/pf269-softhyph.json.
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const MC = app.metadataCache, ad = app.vault.adapter;
  const books = [];
  for (const f of app.vault.getMarkdownFiles()) {
    if (!f.path.startsWith('Library/')) continue;
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || fm.type !== 'book') continue;
    const src = String(fm.source_pdf || ''), ts = String(fm.text_source || '');
    if (!/\.pdf$/i.test(src)) continue;
    if (!/text layer/i.test(ts) || /OCR|Tesseract|ocrmypdf/i.test(ts)) continue;
    books.push([f.path, src, ts]);
  }
  let leaf = null;
  if (!window.pdfjsLib) { const anyPdf = books[0] && books[0][1]; leaf = app.workspace.getLeaf('tab'); await leaf.setViewState({ type: 'pdf', state: { file: anyPdf }, active: false }); for (let i = 0; i < 60 && !window.pdfjsLib; i++) await sleep(250); }
  const lib = window.pdfjsLib; const R = { when: new Date().toISOString(), haveLib: !!lib, n: books.length, results: [] };
  const t0 = Date.now();
  try {
    if (lib) for (const [note, src, ts] of books) {
      try {
        const st = await ad.stat(src); if (!st) { R.results.push([note, src, 'NO FILE']); continue; }
        if (st.size > 120e6) { R.results.push([note, src, 'SKIP size ' + st.size]); continue; }
        const data = new Uint8Array(await ad.readBinary(src)); const doc = await lib.getDocument({ data }).promise;
        const N = doc.numPages, picks = [...new Set(Array.from({ length: Math.min(14, N) }, (_, i) => 1 + Math.floor((i + 0.5) * N / Math.min(14, N))))];
        let shyIn = 0, shyEnd = 0, hy = 0, en = 0, em = 0, chars = 0; const ex = [];
        for (const pg of picks) {
          const page = await doc.getPage(pg); const tc = await page.getTextContent();
          for (const it of tc.items) { const s = it.str || ''; chars += s.length;
            for (let k = 0; k < s.length; k++) { const c = s[k];
              if (c === '­') { if (k < s.length - 1 && /[\p{L}\p{N}]/u.test(s[k + 1])) { shyIn++; if (ex.length < 4) ex.push(s.slice(Math.max(0, k - 12), k + 12)); } else shyEnd++; }
              else if (c === '-') hy++; else if (c === '–') en++; else if (c === '—') em++; } }
          page.cleanup();
        }
        await doc.destroy();
        R.results.push([note, src, { pages: N, sampled: picks.length, chars, shyIn, shyEnd, hy, en, em, ex }]);
      } catch (e) { R.results.push([note, src, 'ERROR ' + (e && e.message)]); }
      if (R.results.length % 20 === 0) await ad.write('.work/out/pf269-softhyph.json', JSON.stringify(R));
    }
  } finally { if (leaf) try { leaf.detach(); } catch (e) {} }
  R.secs = Math.round((Date.now() - t0) / 1000);
  await ad.write('.work/out/pf269-softhyph.json', JSON.stringify(R, null, 1));
  const flag = R.results.filter(r => typeof r[2] === 'object' && r[2].shyIn > 0);
  return `pf269-softhyph: lib ${!!lib}; ${books.length} born-digital books, ${R.results.length} read in ${R.secs}s; with soft hyphens inside lines: ${flag.length}; ${flag.slice(0, 6).map(r => r[0].split('/').pop() + ' ' + r[2].shyIn + '/' + r[2].hy).join(' | ')}`;
})()
