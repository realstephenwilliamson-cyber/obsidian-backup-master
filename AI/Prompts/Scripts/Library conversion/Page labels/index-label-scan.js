(async () => {
  // pf270 (26 Oct 2026, third session): read-only. Index lines whose page label may mix numberings. For every converted book's index note
  // (type: book, under Library/), each contents line "[[note|label]] (pp. a–b)" or "(PDF a–b)" is compared with the chapter note:
  // its page_range, its first and last markers (*[p. N]* or *[PDF K]* with ^pgK). Flags: label differs from page_range; the first page of
  // the label equals the PDF number K of a [PDF K] marker; page_range empty but label "pp.". Writes .work/out/pf270-rangescan.json.
  const MC = app.metadataCache, R = [];
  const notes = app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Library/'));
  const byName = new Map(notes.map(f => [f.basename, f]));
  for (const f of notes) {
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || fm.type !== 'book') continue;
    const t = await app.vault.cachedRead(f);
    for (const line of t.split('\n')) {
      const m = /^- \[\[([^\]|#]+)(?:\|[^\]]*)?\]\] \((pp\.|PDF) ([^)]*)\)\s*$/.exec(line); if (!m) continue;
      const cf = byName.get(m[1].split('/').pop()); if (!cf) { R.push([f.path, line, 'no note']); continue; }
      const ct = await app.vault.cachedRead(cf); const cfm = MC.getFileCache(cf)?.frontmatter || {};
      const mk = [...ct.matchAll(/^\*\[(p\.|PDF) ([^\]]+)\]\* \^pg(\d+)/gm)].map(x => [x[1], x[2], +x[3]]);
      if (!mk.length) continue;
      const pr = String(cfm.page_range ?? ''), lab = m[3], kind = m[2];
      const first = mk[0], firstP = mk.find(x => x[0] === 'p.'), lastP = [...mk].reverse().find(x => x[0] === 'p.');
      const flags = [];
      if (kind === 'pp.' && pr && lab !== pr) flags.push('label≠page_range');
      if (kind === 'pp.' && !pr) flags.push('pp. but empty page_range');
      if (kind === 'pp.' && first[0] === 'PDF' && lab.split(/[–-]/)[0] === String(first[2])) flags.push('label starts with a PDF number');
      if (kind === 'pp.' && firstP && lab.split(/[–-]/)[0] !== firstP[1]) flags.push('label start≠first printed marker ' + firstP[1]);
      if (kind === 'pp.' && lastP && lab.split(/[–-]/).pop() !== lastP[1]) flags.push('label end≠last printed marker ' + lastP[1]);
      if (flags.length) R.push([f.path.split('/').slice(-2, -1)[0], cf.basename, lab, pr, first, firstP && firstP.slice(0, 2), lastP && lastP.slice(0, 2), flags]);
    }
  }
  await app.vault.adapter.write('.work/out/pf270-rangescan.json', JSON.stringify(R, null, 1));
  return `pf270-rangescan: ${R.length} index lines flagged`;
})()
