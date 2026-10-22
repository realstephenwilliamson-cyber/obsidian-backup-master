(async () => {
  // Phase 4: notes of a re-converted book that the new conversion no longer has (its chapters came out differently).
  // Moves each to the vault's .trash through Obsidian, only if it is a phase-4 note (source_pdf + converted in its frontmatter),
  // after a copy in .work/backup-phase4-trash/. Reads .work/p4/trash-list.json. window.DRY !== false -> report only.
  const DRY = window.DRY !== false;
  const A = app.vault.adapter, V = app.vault, MC = app.metadataCache;
  const list = JSON.parse(await A.read('.work/p4/trash-list.json'));
  const rep = { dry: DRY, trashed: 0, missing: [], refused: [], errors: [] };
  const mkdirs = async (p) => { let cur = ''; for (const x of p.split('/').slice(0, -1)) { cur = cur ? cur + '/' + x : x; if (!(await A.exists(cur))) await A.mkdir(cur); } };
  for (const path of list) {
    try {
      const f = V.getAbstractFileByPath(path);
      if (!f) { rep.missing.push(path); continue; }
      const fm = MC.getFileCache(f)?.frontmatter || {};
      if (!fm.source_pdf || !fm.converted) { rep.refused.push(path); continue; }
      if (!DRY) {
        const bk = '.work/backup-phase4-trash/' + path; await mkdirs(bk);
        await A.write(bk, await V.read(f));
        await V.trash(f, false);
      }
      rep.trashed++;
    } catch (e) { rep.errors.push(path + ': ' + e.message); }
  }
  await A.write('.work/out/p4-trash-' + (DRY ? 'dry' : 'real') + '-' + Date.now() + '.json', JSON.stringify(rep, null, 1));
  return `${DRY ? 'DRY' : 'APPLIED'} trashed ${rep.trashed}, missing ${rep.missing.length}, refused ${rep.refused.length}, errors ${rep.errors.length}`;
})()
