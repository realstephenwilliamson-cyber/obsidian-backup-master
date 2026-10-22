(async () => {
  // Area J / Area C (19 Oct 2026): renders the date header (full) and the Daily Office for the Holy Days test dates in temporary
  // notes under Notes/ (made, read in reading mode, text saved to .work/out/holydays-render/<date>.txt, then moved to .trash).
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const dates = ['2026-05-31', '2026-10-18', '2026-10-19', '2026-10-28', '2026-11-01', '2026-11-08', '2026-12-27', '2027-04-25', '2028-08-06', '2029-03-25', '2029-04-09', '2026-12-25', '2026-12-26'];
  await app.vault.adapter.mkdir('.work/out/holydays-render').catch(() => {});
  const errs = []; const origErr = console.error; console.error = (...a) => { errs.push(a.map(x => { try { return String((x && x.message) || x); } catch (e) { return '?'; } }).join(' ').slice(0, 300)); try { origErr.apply(console, a); } catch (e) {} };
  const R = []; const prev = app.workspace.activeLeaf; const leaf = app.workspace.getLeaf('tab');
  try {
    for (const d of dates) {
      const path = `Notes/zz render test ${d}.md`;
      if (app.vault.getAbstractFileByPath(path)) { R.push([d, 'exists already, skipped']); continue; }
      const body = `---\ntype: render-test\n---\n# Render test ${d}\n\n\`\`\`dataviewjs\nawait dv.view("Templates/Views/today-header", {date: "${d}"})\n\`\`\`\n\n## Office\n\n\`\`\`dataviewjs\nawait dv.view("Templates/Views/daily-office", {date: "${d}", open: true})\n\`\`\`\n`;
      const f = await app.vault.create(path, body); const n0 = errs.length;
      try {
        app.workspace.setActiveLeaf(leaf, { focus: true });
        await leaf.setViewState({ type: 'markdown', state: { file: f.path, mode: 'preview', source: false }, active: true });
        if (leaf.loadIfDeferred) await leaf.loadIfDeferred();
        await sleep(6000);
        const v = leaf.view; const el = (v && v.previewMode && v.previewMode.containerEl) || (v && v.containerEl);
        const txt = el ? el.innerText.replace(/\n{3,}/g, '\n\n') : '(no container)';
        const errEls = el ? [...el.querySelectorAll('.dataview-error, .dataview-error-box, .dataviewjs-error, .dataview-error-message')].filter(x => x.textContent.trim()).map(x => x.textContent.trim().slice(0, 200)) : [];
        await app.vault.adapter.write(`.work/out/holydays-render/${d}.txt`, txt);
        R.push([d, { chars: txt.length, errors: errEls, console: errs.slice(n0), head: txt.replace(/\s+/g, ' ').slice(0, 160) }]);
      } finally { await leaf.setViewState({ type: 'empty' }); await app.vault.trash(f, false); }
    }
  } finally { console.error = origErr; try { leaf.detach(); } catch (e) {} try { if (prev) app.workspace.setActiveLeaf(prev, { focus: true }); } catch (e) {} }
  await app.vault.adapter.write('.work/out/holydays-render/index.json', JSON.stringify({ when: new Date().toISOString(), results: R }, null, 1));
  return `holy days render: ${R.length} dates; ${R.map(r => r[0] + ': ' + (typeof r[1] === 'string' ? r[1] : r[1].chars + ' chars' + (r[1].errors.length || r[1].console.length ? ' ERR ' + (r[1].errors[0] || r[1].console[0]) : ''))).join(' | ')}`;
})()
