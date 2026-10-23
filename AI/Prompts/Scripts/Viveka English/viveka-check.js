(async () => {
  await new Promise(r => setTimeout(r, 25000));   // let the metadata cache catch up with the patch's writes
  // Read-only: every embed in the verse notes' [!viveka] boxes points to a heading that exists; the vault's unresolved count.
  const mc = app.metadataCache, V = app.vault; const R = { notes: 0, embeds: 0, bad: [], headings: 0, unresolved: null };
  const norm = h => h.replace(/[#^|\[\]]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
  for (const f of V.getMarkdownFiles()) {
    if (!f.path.startsWith('Texts/Tantraloka/Ahnika')) continue;
    const c = mc.getFileCache(f) || {}; const em = (c.embeds || []).filter(e => e.link.includes('Tantraloka Dyczkowski'));
    if (!em.length) continue; R.notes++;
    for (const e of em) {
      R.embeds++; const [p, h] = e.link.split('#'); const t = mc.getFirstLinkpathDest(p, f.path);
      if (!t) { R.bad.push(f.basename + ' → ' + e.link + ' (no note)'); continue; }
      if (!((mc.getFileCache(t) || {}).headings || []).some(x => norm(x.heading) === norm(h))) R.bad.push(f.basename + ' → ' + e.link + ' (no heading)');
    }
  }
  for (const f of V.getMarkdownFiles().filter(f => f.path.startsWith('Library/Trika/Tantraloka (Dyczkowski)/'))) R.headings += ((mc.getFileCache(f) || {}).headings || []).length;
  let n = 0, k = 0; for (const [p, o] of Object.entries(mc.unresolvedLinks)) { const c = Object.values(o).reduce((a, b) => a + b, 0); if (c) { n++; k += c; } }
  R.unresolved = `${n}/${k}`;
  await V.adapter.write('.work/out/viveka-check.json', JSON.stringify(R, null, 1));
  return `viveka-check: ${R.notes} verse notes, ${R.embeds} embeds, ${R.bad.length} broken${R.bad.length ? ': ' + R.bad.slice(0, 5).join(' | ') : ''}; headings in the library copy ${R.headings}; unresolved ${R.unresolved}`;
})()
