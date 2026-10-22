(async () => {
  // Report only: Markdown notes in Library/ whose file name (without folder) is used by more than one note.
  // A bare [[name]] link to such a name can open the wrong note. Writes .work/out/p4-dupnames-<ts>.json
  const A = app.vault.adapter;
  const by = {};
  for (const f of app.vault.getMarkdownFiles()) {
    if (!f.path.startsWith('Library/')) continue;
    (by[f.basename] = by[f.basename] || []).push(f.path);
  }
  const dups = Object.entries(by).filter(([k, v]) => v.length > 1);
  const folders = {};
  for (const [k, v] of dups) for (const p of v) { const d = p.split('/').slice(0, -1).join('/'); folders[d] = (folders[d] || 0) + 1; }
  const rep = { when: new Date().toISOString(), names: dups.length, notes: dups.reduce((s, [k, v]) => s + v.length, 0), folders, sample: dups.slice(0, 60) };
  await A.write('.work/out/p4-dupnames.json', JSON.stringify(rep, null, 1));
  return `duplicate names ${rep.names} (${rep.notes} notes) in ${Object.keys(folders).length} folders`;
})()
