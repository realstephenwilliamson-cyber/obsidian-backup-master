(async () => {
  // Phase 4: create or replace converted-book notes from the bundles in .work/p4/create-list.json.
  // Only replaces a note whose frontmatter says it came from this phase (has source_pdf and converted); anything else is refused.
  // Old versions are copied to .work/backup-phase4-2026-10-07/. window.DRY !== false -> report only.
  const DRY = window.DRY !== false;
  const A = app.vault.adapter, V = app.vault;
  const list = JSON.parse(await A.read('.work/p4/create-list.json'));
  const rep = { dry: DRY, created: 0, replaced: 0, same: 0, refused: [], errors: [] };
  const ensureFolder = async (dir) => { let cur = ''; for (const p of dir.split('/')) { cur = cur ? cur + '/' + p : p; if (!V.getAbstractFileByPath(cur) && !DRY) await V.createFolder(cur); } };
  for (const b of list) {
    const J = JSON.parse(await A.read('.work/p4/bundles/' + b));
    for (const [path, content] of Object.entries(J.notes)) {
      try {
        const f = V.getAbstractFileByPath(path);
        if (!f) { if (!DRY) { await ensureFolder(path.split('/').slice(0, -1).join('/')); await V.create(path, content); } rep.created++; continue; }
        const old = await V.read(f);
        if (old === content) { rep.same++; continue; }
        if (!/^source_pdf: /m.test(old) || !/^converted: /m.test(old)) { rep.refused.push(path); continue; }
        if (!DRY) {
          const bk = '.work/backup-phase4-2026-10-07/' + path; const bd = bk.split('/').slice(0, -1).join('/');
          if (!(await A.exists(bd))) await A.mkdir(bd);
          if (!(await A.exists(bk))) await A.write(bk, old);
          await V.modify(f, content);
        }
        rep.replaced++;
      } catch (e) { rep.errors.push(path + ': ' + e.message); }
    }
  }
  await A.write('.work/out/p4-replace-' + (DRY ? 'dry' : 'real') + '-' + Date.now() + '.json', JSON.stringify(rep, null, 1));
  return `${DRY ? 'DRY' : 'APPLIED'} created ${rep.created}, replaced ${rep.replaced}, same ${rep.same}, refused ${rep.refused.length}, errors ${rep.errors.length}`;
})()
