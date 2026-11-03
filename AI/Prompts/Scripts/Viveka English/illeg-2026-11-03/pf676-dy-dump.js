(async () => {
  // pf676-dy-dump (3 Nov 2026, evening): read-only. Every note of Dyczkowski's Tantraloka library copy that still holds
  // "\[illegible\]", as {path: text}, to .work/xfer/dy-notes.json for the cloud chat (the inner-placeholder reading pass).
  const ad = app.vault.adapter, R = {};
  for (const f of app.vault.getMarkdownFiles()) {
    if (!f.path.startsWith('Library/Trika/Tantraloka (Dyczkowski)/')) continue;
    const t = await app.vault.read(f); if (t.includes('\\[illegible\\]')) R[f.path] = t;
  }
  if (!(await ad.exists('.work/xfer'))) await ad.mkdir('.work/xfer');
  await ad.write('.work/xfer/dy-notes.json', JSON.stringify(R));
  const n = Object.values(R).reduce((s, t) => s + (t.split('\\[illegible\\]').length - 1), 0);
  return `pf676-dy-dump: ${Object.keys(R).length} notes, ${n} placeholders`;
})()
