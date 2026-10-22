(async () => {
  // Phase 4 step 6: for every converted book (an index note, or a one-note article, with `work` and `source_pdf`),
  // add the Markdown note to its catalog note's `files:` (the PDF stays) and put the "Open the PDF" button under the title.
  // Backs up each catalog note before changing it. DRY unless the job starts with "// APPLY".
  const ad = app.vault.adapter, DRYRUN = window.DRY !== false;
  const BK = '.work/backup-phase4-catalog/';
  const BLOCK = '```dataviewjs\nawait dv.view("Templates/Views/open-pdf")\n```';
  const R = { when: new Date().toISOString(), dry: DRYRUN, books: 0, files_added: 0, buttons_added: 0, already: 0, no_catalog: [], changed: [] };
  const books = app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Library/') && !f.path.startsWith('Catalog/')).map(f => [f, app.metadataCache.getFileCache(f)?.frontmatter]).filter(([f, fm]) => fm && fm.work && fm.source_pdf && fm.type !== 'book-chapter');
  for (const [f, fm] of books) {
    R.books++;
    const m = String(fm.work).match(/\[\[([^\]|#]+)/); if (!m) { R.no_catalog.push(f.path); continue; }
    const cat = app.metadataCache.getFirstLinkpathDest(m[1], f.path);
    if (!cat || !cat.path.startsWith('Catalog/')) { R.no_catalog.push(f.path); continue; }
    const cfm = app.metadataCache.getFileCache(cat)?.frontmatter || {};
    const link = `[[${f.path.replace(/\.md$/, '')}]]`;
    const files = [].concat(cfm.files ?? []).map(String);
    // compare by the file each entry opens, not by its spelling (after a rename Obsidian writes the short form "[[Name]]")
    const opens = x => { const m = String(x).match(/\[\[([^\]|#]+)/); const d = m && app.metadataCache.getFirstLinkpathDest(m[1], cat.path); return d ? d.path : null; };
    const needFile = !files.some(x => x.includes(f.path.replace(/\.md$/, '')) || opens(x) === f.path);
    const text = await ad.read(cat.path);
    const needBtn = !text.includes('Templates/Views/open-pdf');
    if (!needFile && !needBtn) { R.already++; continue; }
    R.changed.push(cat.path);
    if (DRYRUN) { if (needFile) R.files_added++; if (needBtn) R.buttons_added++; continue; }
    const bp = BK + cat.path; const dir = bp.substring(0, bp.lastIndexOf('/'));
    if (!(await ad.exists(bp))) { if (!(await ad.exists(dir))) await ad.mkdir(dir); await ad.write(bp, text); }
    if (needFile) { await app.fileManager.processFrontMatter(cat, x => { x.files = [].concat(x.files ?? []).concat([link]); }); R.files_added++; }
    if (needBtn) {
      await app.vault.process(cat, t => {
        const lines = t.split('\n'); let i = 0;
        if (lines[0] === '---') { i = lines.indexOf('---', 1) + 1; }
        let h = lines.findIndex((l, k) => k >= i && /^# /.test(l));
        const at = h >= 0 ? h + 1 : i;
        lines.splice(at, 0, '', BLOCK);
        return lines.join('\n');
      });
      R.buttons_added++;
    }
  }
  R.changed_n = R.changed.length; R.changed = R.changed.slice(0, 20);
  await ad.write('.work/out/p4-catalog-' + (DRYRUN ? 'dry-' : 'real-') + Date.now() + '.json', JSON.stringify(R, null, 1));
  return `${DRYRUN ? 'DRY' : 'APPLIED'} books ${R.books}, catalog notes to change ${R.changed_n}, files added ${R.files_added}, buttons ${R.buttons_added}, already ${R.already}, no catalog ${R.no_catalog.length}`;
})()
