(async () => {
  // Phase 8, step 1 (read-only): render check, third try: the view state is set explicitly to reading mode and the file path is
  // verified before measuring; measures the preview container only. Writes .work/out/s83a-render3.json; closes its tab at the end.
  const sleep = ms => new Promise(r => setTimeout(r, ms)); const MC = app.metadataCache;
  const names = ['Home', 'Home (mobile)', 'Calendar', 'Study', 'Texts', 'Notes', 'AI', 'Catalog/Catalog.base', 'Catalog/By author.base', 'Projects/Homilies/Homily list.base', 'Study/Sanskrit/Ruppel.base', 'Hub - Tantraloka', 'Hub - Gospel of John', 'Hub - Technics, memory and the Leviathan', 'Hub - The Second Domestication', 'Tantraloka study plan', 'Study plan - Practice run 2026', 'Vault Health & Phantom Link Manager', 'Synoptic reader', 'Sanskrit Daily Letter Cycle', 'Monier-Williams Quick Lookup Guide', 'Letters', 'Conjunct cycle (Tantraloka)', 'Devanagari search', 'Devi Mahatmya', 'Homilies', 'Trika', 'Hubs', 'Concepts', 'Journal/2026/2026-10-12.md', 'Tantraloka 31.025'];
  const errs = []; const origErr = console.error; let cur = null;
  console.error = (...a) => { errs.push([cur, a.map(x => { try { return String((x && x.message) || x); } catch (e) { return '?'; } }).join(' ').slice(0, 300)]); try { origErr.apply(console, a); } catch (e) {} };
  const R = []; const prev = app.workspace.activeLeaf; const leaf = app.workspace.getLeaf('tab');
  try {
    for (const n of names) {
      let f = app.vault.getAbstractFileByPath(n) || app.vault.getAbstractFileByPath(n + '.md') || MC.getFirstLinkpathDest(n, '');
      if (!f) { R.push([n, 'missing']); continue; }
      cur = f.path; const n0 = errs.length; const t0 = Date.now();
      try {
        app.workspace.setActiveLeaf(leaf, { focus: true });
        if (f.extension === 'base') await leaf.setViewState({ type: 'bases', state: { file: f.path }, active: true });
        else await leaf.setViewState({ type: 'markdown', state: { file: f.path, mode: 'preview', source: false }, active: true });
        if (leaf.loadIfDeferred) await leaf.loadIfDeferred();
      } catch (e) { R.push([f.path, 'open error: ' + (e && e.message)]); continue; }
      await sleep(f.extension === 'base' ? 7000 : 7000);
      const v = leaf.view; const vf = v && v.file ? v.file.path : null;
      const el = (v && v.previewMode && v.previewMode.containerEl) || (v && v.containerEl);
      const q = s => el ? el.querySelectorAll(s).length : -1;
      const errEls = el ? [...el.querySelectorAll('.dataview-error, .dataview-error-box, .dataviewjs-error, .dataview-error-message, .bases-error, .markdown-embed-error, .callout-error')].filter(x => x.textContent.trim()) : [];
      const txt = el ? el.textContent.replace(/\s+/g, ' ') : '';
      R.push([f.path, { viewType: v && v.getViewType && v.getViewType(), viewFile: vf, sameFile: vf === f.path, mode: v && v.getMode && v.getMode(), dvBlocks: q('.block-language-dataviewjs, .block-language-dataview'), dvTables: q('table.dataview, .dataview.table-view-table, .dataview-list'), errors: errEls.map(x => x.className + ': ' + x.textContent.trim().slice(0, 200)), basesRows: q('.bases-tr, .bases-table-row, .bases-card, [class*="bases-"] tbody tr'), basesCount: (txt.match(/(\d+) (?:results?|items?)/) || [])[0] || null, bodyLen: txt.length, head: txt.slice(0, 200), consoleErrors: errs.slice(n0).map(e => e[1]), ms: Date.now() - t0 }]);
    }
  } finally { console.error = origErr; try { leaf.detach(); } catch (e) {} try { if (prev) app.workspace.setActiveLeaf(prev, { focus: true }); } catch (e) {} }
  await app.vault.adapter.write('.work/out/s83a-render3.json', JSON.stringify({ when: new Date().toISOString(), results: R, consoleErrors: errs }, null, 1));
  const bad = R.filter(r => typeof r[1] === 'string' || !r[1].sameFile || r[1].errors.length || r[1].consoleErrors.length);
  return `render check 3: ${R.length} opened; flagged ${bad.length}: ${JSON.stringify(bad.map(r => [r[0], typeof r[1] === 'string' ? r[1] : { sameFile: r[1].sameFile, errors: r[1].errors.slice(0, 2), console: r[1].consoleErrors.length }])).slice(0, 1800)}`;
})()
