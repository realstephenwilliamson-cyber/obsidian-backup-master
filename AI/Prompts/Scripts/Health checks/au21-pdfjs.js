(async () => {
  // Audit 14 Oct 2026 (read-only): what Obsidian's own pdf.js reads from four Devanagari PDF pages (for finding H-01): the text and the
  // count of Latin-range characters (U+0080–U+024F) right after ि (U+093F). Opens one PDF view to load pdf.js, then closes it.
  // Writes .work/out/audit-1014-pdfjs.json.
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const items = [['Library/Hinduism/Tantra_Kula_Chudamani_Nigama_2.pdf', 85], ['Library/Hinduism/K.P. Leelamma - Devi Mahatmyam with Word to Word Meaning-Sri Ramakrishna Math Thrissur (1998).pdf', 86], ['Library/Hinduism/Taittiriya Upanishad.pdf', 38], ['Library/Sanskrit/Sivadvaita.Nirnaya.by.Appayya.Diksita.pdf', 107]];
  let leaf = null;
  if (!window.pdfjsLib) { leaf = app.workspace.getLeaf('tab'); await leaf.setViewState({ type: 'pdf', state: { file: items[2][0] }, active: false }); for (let i = 0; i < 40 && !window.pdfjsLib; i++) await sleep(250); }
  const lib = window.pdfjsLib; const R = { when: new Date().toISOString(), haveLib: !!lib, results: [] };
  try {
    if (lib) for (const [p, pg] of items) {
      try { const data = new Uint8Array(await app.vault.adapter.readBinary(p)); const doc = await lib.getDocument({ data }).promise; const page = await doc.getPage(pg); const tc = await page.getTextContent(); const text = tc.items.map(x => x.str + (x.hasEOL ? '\n' : '')).join('');
        let junk = 0, i_ = 0; for (let k = 0; k < text.length; k++) if (text[k] === 'ि') { i_++; const n = text.charCodeAt(k + 1); if (n >= 0x80 && n <= 0x24F) junk++; }
        R.results.push([p, pg, { pages: doc.numPages, iSign: i_, junkAfterI: junk, sample: text.slice(0, 700) }]); await doc.destroy(); }
      catch (e) { R.results.push([p, pg, 'ERROR ' + (e && e.message)]); }
    }
  } finally { if (leaf) try { leaf.detach(); } catch (e) {} }
  await app.vault.adapter.write('.work/out/audit-1014-pdfjs.json', JSON.stringify(R, null, 1));
  return `pdfjs check: lib ${!!lib}; ${R.results.length} pages`;
})()
