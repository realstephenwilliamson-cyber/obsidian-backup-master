(async () => {
  // Read-only: words with ä/å/Ä/Å in the bodies of converted notes whose text came from OCR (frontmatter text_source mentions OCR
  // or Tesseract), outside [[links]]. Books with Vedic accents are left out (Lanman, Whitney, Macdonell). Writes .work/out/afix-words.json.
  const V = app.vault, MC = app.metadataCache;
  const skip = ['A Sanskrit Reader (Lanman)', 'A Sanskrit Grammar (Whitney)', 'A Vedic Reader for Students (Macdonell)'];
  const words = {}, books = {}; let notes = 0;
  const RX = /\[\[[^\]\n]*\]\]|[\p{L}]*[äåÄÅ][\p{L}]*/gu;
  for (const f of V.getMarkdownFiles()) {
    if (!f.path.startsWith('Library/')) continue;
    if (skip.some(s => f.path.includes('/' + s + '/'))) continue;
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || !fm.source_pdf || !fm.converted) continue;
    if (!/OCR|Tesseract/.test(String(fm.text_source || ''))) continue;
    const t = await V.cachedRead(f); if (!/[äåÄÅ]/.test(t)) continue;
    const body = t.replace(/^---\n[\s\S]*?\n---\n/, '');
    let n = 0;
    for (const m of body.matchAll(RX)) { const w = m[0]; if (w.startsWith('[[')) continue; words[w] = (words[w] || 0) + 1; n++; }
    if (n) { notes++; const b = f.path.split('/').slice(0, 3).join('/'); books[b] = (books[b] || 0) + n; }
  }
  await app.vault.adapter.write('.work/out/afix-words.json', JSON.stringify({ notes, books, words }));
  return `notes ${notes}, books ${Object.keys(books).length}, distinct words ${Object.keys(words).length}`;
})()
