(async () => {
  // render-holydays-testdates-v2.js (26 Oct 2026, job pf190): Holy Days render test without a workspace tab. The tab-based version drew 0 characters
  // in the tab, so this renders the same two views (today-header, full; daily-office, open) for the 13 test dates through Dataview's
  // own executeJs into a container fixed on the page, and reads its textContent. Writes nothing in the vault except .work/out.
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const dv = app.plugins.plugins.dataview && app.plugins.plugins.dataview.api; if (!dv) return 'dataview not loaded';
  const Plugin = Object.getPrototypeOf(app.plugins.plugins.dataview.constructor), Component = Object.getPrototypeOf(Plugin);
  const dates = ['2026-05-31', '2026-10-18', '2026-10-19', '2026-10-28', '2026-11-01', '2026-11-08', '2026-12-27', '2027-04-25', '2028-08-06', '2029-03-25', '2029-04-09', '2026-12-25', '2026-12-26'];
  await app.vault.adapter.mkdir('.work/out/holydays-render2').catch(() => {});
  const errs = []; const origErr = console.error; console.error = (...a) => { errs.push(a.map(x => { try { return String((x && x.message) || x); } catch (e) { return '?'; } }).join(' ').slice(0, 300)); try { origErr.apply(console, a); } catch (e) {} };
  const R = [];
  try {
    for (const d of dates) {
      const host = document.body.createDiv(); host.setAttr('style', 'position:fixed;left:0;top:0;width:900px;max-height:600px;overflow:auto;opacity:0.02;z-index:-1;pointer-events:none');
      host.addClass('markdown-rendered');
      const comp = new Component(); comp.load(); const n0 = errs.length; const parts = {};
      try {
        for (const [k, code] of [['header', `await dv.view("Templates/Views/today-header", {date: "${d}"})`], ['office', `await dv.view("Templates/Views/daily-office", {date: "${d}", open: true})`]]) {
          const el = host.createDiv(); await dv.executeJs(code, el, comp, 'Notes/zz render test.md');
          let last = -1, txt = ''; for (let i = 0; i < 20; i++) { await sleep(500); txt = el.textContent; if (txt.length && txt.length === last) break; last = txt.length; }
          const errEls = [...el.querySelectorAll('.dataview-error, .dataview-error-box, .dataviewjs-error, .dataview-error-message')].map(x => x.textContent.trim().slice(0, 200)).filter(Boolean);
          const red = [...el.querySelectorAll('[style*="color: red"], [style*="color:red"], .vp-error')].map(x => x.textContent.trim().slice(0, 200)).filter(Boolean);
          parts[k] = { chars: txt.length, errors: errEls.concat(red), text: el.innerText || txt };
        }
        await app.vault.adapter.write(`.work/out/holydays-render2/${d}.txt`, '## header\n' + parts.header.text + '\n\n## office\n' + parts.office.text);
        R.push([d, { header: parts.header.chars, office: parts.office.chars, errors: parts.header.errors.concat(parts.office.errors), console: errs.slice(n0), head: parts.header.text.replace(/\s+/g, ' ').slice(0, 220) }]);
      } finally { comp.unload(); host.remove(); }
    }
  } finally { console.error = origErr; }
  await app.vault.adapter.write('.work/out/holydays-render2/index.json', JSON.stringify({ when: new Date().toISOString(), focus: document.hasFocus(), results: R }, null, 1));
  return `holy days render (executeJs): focus ${document.hasFocus()}; ` + R.map(r => `${r[0]}: ${r[1].header}+${r[1].office} chars${r[1].errors.length || r[1].console.length ? ' ERR ' + (r[1].errors[0] || r[1].console[0]) : ''}`).join(' | ');
})()
