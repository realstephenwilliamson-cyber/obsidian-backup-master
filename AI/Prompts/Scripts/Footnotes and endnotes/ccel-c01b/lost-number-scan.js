(async () => {
  // lost-number-scan.js (pf472, read-only, 28 Oct 2026 later session): vault probe; link-target blocks for the C-01(b) restorations;
  // in the two CCEL books, footnote calls <sup>N</sup> whose number N appears nowhere else in the note (footnote text or its number lost).
  const ad = app.vault.adapter;
  const files = app.vault.getFiles(), notes = app.vault.getMarkdownFiles();
  const U = app.metadataCache.unresolvedLinks;
  const uFiles = Object.values(U).filter(o => Object.keys(o).length).length;
  const uLinks = Object.values(U).reduce((s, o) => s + Object.values(o).reduce((a, b) => a + b, 0), 0);
  const need = { 'Matthew 20': ['20-32', '20-33'], 'Matthew 13': ['13-43'], 'Galatians 03': ['3-13'], 'Hebrews 04': ['4-13'], 'Philippians 02': ['2-8'] };
  const blk = {};
  for (const [n, ids] of Object.entries(need)) {
    const f = app.metadataCache.getFirstLinkpathDest(n, '');
    const b = f ? (app.metadataCache.getFileCache(f)?.blocks || {}) : {};
    blk[n] = { file: f ? f.path : null, ids: Object.fromEntries(ids.map(i => [i, !!b[i]])) };
  }
  const dirs = ['Library/Christianity/Sermon on the Mount, Harmony of the Gospels, Homilies (Augustine)/', 'Library/Christianity/Homilies on Matthew (Chrysostom)/'];
  const lost = []; let calls = 0, nNotes = 0;
  for (const f of notes.filter(f => dirs.some(d => f.path.startsWith(d)))) {
    nNotes++;
    const t = await app.vault.cachedRead(f);
    const ns = [...t.matchAll(/<sup>(\d+)<\/sup>/g)].map(m => m[1]);
    const rest = t.replace(/<sup>\d+<\/sup>/g, ' ');
    for (const n of new Set(ns)) {
      calls++;
      const re = new RegExp('(^|[^\\d.,\\-–/#^|])' + n + '(?![\\d])');
      if (!re.test(rest)) lost.push([f.path.split('/').pop(), +n]);
    }
  }
  await ad.write('.work/out/pf472-probe-c01b.detail.json', JSON.stringify({ when: new Date().toISOString(), files: files.length, notes: notes.length, uFiles, uLinks, blk, nNotes, calls, lostN: lost.length, lost }, null, 1));
  return `pf472: ${files.length} files, ${notes.length} notes, unresolved ${uFiles} / ${uLinks}; blocks ${JSON.stringify(blk)}; CCEL notes ${nNotes}, distinct calls ${calls}, calls with no number elsewhere ${lost.length}`;
})()
