(async () => {
  // Phase 4: rename converted notes/folders through Obsidian (links follow, as "Automatically update internal links" is on).
  // Reads .work/p4/rename-list.json: [[oldPath, newPath], ...] (files or folders, applied in order).
  // The dry run lists, for each file, the notes that link to it (so a link inside Stephen's own notes is seen before anything changes).
  // window.DRY !== false -> report only. Writes .work/out/p4-rename-<dry|real>.json
  const DRY = window.DRY !== false;
  const A = app.vault.adapter, V = app.vault, MC = app.metadataCache;
  const list = JSON.parse(await A.read('.work/p4/rename-list.json'));
  const rep = { dry: DRY, renamed: 0, missing: [], exists: [], errors: [], backlinks: {}, outside_library: [] };
  for (const [from, to] of list) {
    const f = V.getAbstractFileByPath(from);
    if (!f) { rep.missing.push(from); continue; }
    if (V.getAbstractFileByPath(to)) { rep.exists.push(to); continue; }
    if (f.extension === 'md') {
      const src = Object.entries(MC.resolvedLinks).filter(([s, m]) => m[from]).map(([s]) => s);
      rep.backlinks[from] = src;
      for (const s of src) if (!s.startsWith('Library/')) rep.outside_library.push([s, from]);
    }
    try { if (!DRY) await app.fileManager.renameFile(f, to); rep.renamed++; }
    catch (e) { rep.errors.push(from + ': ' + e.message); }
  }
  await A.write('.work/out/p4-rename-' + (DRY ? 'dry' : 'real') + '.json', JSON.stringify(rep, null, 1));
  return `${DRY ? 'DRY' : 'APPLIED'} renamed ${rep.renamed}, missing ${rep.missing.length}, target exists ${rep.exists.length}, errors ${rep.errors.length}, links from outside Library ${rep.outside_library.length}`;
})()
