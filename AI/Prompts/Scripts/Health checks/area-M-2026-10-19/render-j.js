(async () => {
  // Area J render check (19 Oct 2026, read-only): opens each note or Base in reading mode in a temporary tab, measures the
  // preview, records Dataview/Bases errors and console errors; writes .work/out/render-j.json; closes the tab.
  const sleep = ms => new Promise(r => setTimeout(r, ms)); const MC = app.metadataCache; const files = app.vault.getMarkdownFiles();
  const byFrag = (folder, frag) => { const l = files.filter(f => f.path.startsWith(folder) && f.basename.includes(frag)); return l.length ? l.map(f => f.path) : [folder + '?' + frag]; };
  const names = ['Home', 'Home (mobile)', 'Calendar', 'Vault Guide', 'Welcome', 'Study', 'Journal/Habits.base', 'Study/Sanskrit/Flashcards/Flashcards.base', 'Catalog/Catalog.base',
    'Study/Sanskrit/CIS study plan.md', 'Study/Sanskrit/Sanskrit.md', 'Study/Sanskrit/Flashcards/Card 017 vocalic l sign.md', 'Study/Sanskrit/Flashcards/Card 094 subscript ra.md', 'Study/Sanskrit/CIS cards/CIS Ch. 3 cards.md',
    'Sanskrit Daily Letter Cycle', 'Calendar/Holy Days (BCP 1979).md', 'Hub - Tantraloka', 'Templates/Daily note.md',
    ...byFrag('Catalog/', 'Lambdin'), ...byFrag('Catalog/', 'Constas'), ...byFrag('Catalog/', 'Dyczkowski (tr.) - Tantraloka'), ...byFrag('Catalog/', 'Dyczkowski - Tantraloka'), ...byFrag('Catalog/', 'Watson'), ...byFrag('Catalog/Trika/', 'Vasugupta'), ...byFrag('Catalog/', 'Radhakrishnan')];
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
      await sleep(7000);
      const v = leaf.view; const vf = v && v.file ? v.file.path : null;
      const el = (v && v.previewMode && v.previewMode.containerEl) || (v && v.containerEl);
      const q = s => el ? el.querySelectorAll(s).length : -1;
      const errEls = el ? [...el.querySelectorAll('.dataview-error, .dataview-error-box, .dataviewjs-error, .dataview-error-message, .bases-error, .markdown-embed-error, .callout-error')].filter(x => x.textContent.trim()) : [];
      const txt = el ? el.textContent.replace(/\s+/g, ' ') : '';
      const buttons = el ? [...el.querySelectorAll('button')].map(b => b.textContent.trim()).filter(Boolean).slice(0, 12) : [];
      R.push([f.path, { viewType: v && v.getViewType && v.getViewType(), viewFile: vf, sameFile: vf === f.path, dvBlocks: q('.block-language-dataviewjs, .block-language-dataview'), dvTables: q('table.dataview, .dataview.table-view-table, .dataview-list'), errors: errEls.map(x => x.className + ': ' + x.textContent.trim().slice(0, 200)), basesRows: q('.bases-tr, .bases-table-row, .bases-card, [class*="bases-"] tbody tr'), basesCount: (txt.match(/(\d+) (?:results?|items?)/) || [])[0] || null, buttons, bodyLen: txt.length, head: txt.slice(0, 600), consoleErrors: errs.slice(n0).map(e => e[1]), ms: Date.now() - t0 }]);
    }
  } finally { console.error = origErr; try { leaf.detach(); } catch (e) {} try { if (prev) app.workspace.setActiveLeaf(prev, { focus: true }); } catch (e) {} }
  await app.vault.adapter.write('.work/out/render-j.json', JSON.stringify({ when: new Date().toISOString(), results: R, consoleErrors: errs }, null, 1));
  const bad = R.filter(r => typeof r[1] === 'string' || !r[1].sameFile || r[1].errors.length || r[1].consoleErrors.length);
  return `render J: ${R.length} opened; flagged ${bad.length}: ${JSON.stringify(bad.map(r => [r[0], typeof r[1] === 'string' ? r[1] : { sameFile: r[1].sameFile, errors: r[1].errors.slice(0, 2), console: r[1].consoleErrors.slice(0, 2) }])).slice(0, 1800)}`;
})()
