(async () => {
  // Area M re-run, check 10 (19 Oct 2026, after Part 1): hard-coded dates and paths in Templates. Changed since 10:30 by
  // the replaced Daily and Weekly note templates and the new view Templates/Views/today-items/view.js.
  // The rules reproduce the 10:30 run exactly (tested outside Obsidian on the 24 files as they were at 10:30: 298 of 298
  // hits, same file, line, kind, value and comment flag): per line (lines over 2,000 characters skipped, i.e. data.json),
  // iso = YYYY-MM-DD; monthName = "D Mon YYYY"; year = 19xx/20xx not touching a digit or hyphen; path = a stretch between
  // two quote characters (" ' `) that starts with a top-level folder and "/" or ends in .md or .pdf; noteLinkLiteral = the
  // text after "[[" up to ] | or # (not in .md templates); comment = the line starts with //.
  // Also: every `EPOCH` constant and every "2026-10-03" in Templates, Study/Sanskrit, Home, Home (mobile) and the .base files.
  // Compared with .work/out/areaM/check10-hardcoded.json. Read-only: writes only .work/out/areaM2/hardcoded.json.
  const ad = app.vault.adapter, T0 = Date.now();
  const NAME = 'hardcoded', OUT = '.work/out/areaM2', CUTOFF = Date.parse('2026-10-19T14:30:00Z');
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const R = { job: 'm2-10-hardcoded', when: new Date().toISOString() };
  let line = '';
  const MONTHS = 'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December';
  const MON_RE = new RegExp('\\b\\d{1,2} (?:' + MONTHS + ')\\.? \\d{4}\\b', 'g');
  const scan = (p, text) => {
    const hits = []; const lines = text.split(/\r?\n/); const isJs = !p.endsWith('.md');
    lines.forEach((L, i) => {
      if (L.length > 2000) return;
      const comment = /^\s*\/\//.test(L);
      const add = (kind, match) => hits.push({ p, line: i + 1, kind, match, comment, text: L.trim().slice(0, 160) });
      for (const m of L.matchAll(/\b\d{4}-\d{2}-\d{2}\b/g)) add('iso', m[0]);
      for (const m of L.matchAll(MON_RE)) add('monthName', m[0]);
      for (const m of L.matchAll(/(?<![\d-])(?:19|20)\d{2}(?![\d-])/g)) add('year', m[0]);
      for (const s of L.split(/["'`]/).slice(1, -1)) if (/^(Texts|Templates|Library|Journal|Study|Projects|Catalog|Notes|Excalidraw|Calendar|AI)\//.test(s) || /\.(md|pdf)$/.test(s)) add('path', s);
      if (isJs) for (const m of L.matchAll(/\[\[([^\]|#]+)/g)) add('noteLinkLiteral', m[1]);
    });
    return { hits, lines: lines.length };
  };
  try {
    const all = app.vault.getFiles();
    const tpl = all.filter(f => f.path.startsWith('Templates/') && ['md', 'js', 'css', 'json'].includes(f.extension)).sort((a, b) => a.path < b.path ? -1 : 1);
    const perFile = [], hits = [];
    for (const f of tpl) {
      const t = await app.vault.cachedRead(f); const s = scan(f.path, t);
      const c = k => s.hits.filter(h => h.kind === k).length;
      perFile.push({ p: f.path, lines: s.lines, bytes: f.stat.size, iso: c('iso'), year: c('year'), monthName: c('monthName'), path: c('path'), noteLinkLiteral: c('noteLinkLiteral'), inComment: s.hits.filter(h => h.comment).length, changedSince1030: f.stat.mtime >= CUTOFF || f.stat.ctime >= CUTOFF });
      hits.push(...s.hits);
    }
    const dv = {}; for (const h of hits) { const k = h.kind + '\u0000' + h.match; const e = dv[k] = dv[k] || { kind: h.kind, match: h.match, n: 0, files: [] }; e.n++; if (!e.files.includes(h.p)) e.files.push(h.p); }
    const distinctValues = Object.values(dv).sort((a, b) => b.n - a.n);
    // EPOCH and the cycle's start date, in and outside Templates
    const ep = [];
    const epFiles = all.filter(f => f.path.startsWith('Templates/') || f.path.startsWith('Study/Sanskrit/') || f.path === 'Home.md' || f.path === 'Home (mobile).md' || f.extension === 'base').filter(f => ['md', 'js', 'base', 'json', 'css'].includes(f.extension));
    for (const f of epFiles) { const t = await app.vault.cachedRead(f); t.split(/\r?\n/).forEach((L, i) => { if (L.length <= 2000 && (/\bEPOCH\s*=/.test(L) || L.includes('2026-10-03'))) ep.push([f.path, i + 1, L.trim().slice(0, 160)]); }); }
    guard('scan');
    // against 10:30: per file, and hits by (file, kind, value, text) so that shifted line numbers do not count
    const old = await readJSON('.work/out/areaM/check10-hardcoded.json'); const cmp = {};
    if (old) {
      const op = Object.fromEntries(old.perFile.map(x => [x.p, x])); const K = ['iso', 'year', 'monthName', 'path', 'noteLinkLiteral', 'inComment'];
      cmp.newFiles = perFile.filter(x => !op[x.p]).map(x => x.p); cmp.goneFiles = old.perFile.filter(x => !perFile.some(y => y.p === x.p)).map(x => x.p);
      cmp.filesWithDifferentCounts = perFile.filter(x => op[x.p] && K.some(k => op[x.p][k] !== x[k])).map(x => ({ p: x.p, changedSince1030: x.changedSince1030, before: Object.fromEntries(K.map(k => [k, op[x.p][k]])), now: Object.fromEntries(K.map(k => [k, x[k]])) }));
      cmp.unchangedFilesWithDifferentCounts = cmp.filesWithDifferentCounts.filter(x => !x.changedSince1030).map(x => x.p);
      const key = h => [h.p, h.kind, h.match, h.text.trim().slice(0, 80)].join('\u0001');
      const cnt = a => { const m = new Map(); for (const h of a) m.set(key(h), (m.get(key(h)) || 0) + 1); return m; };
      const A = cnt(old.hits), B = cnt(hits); const gone = [], added = [];
      for (const [k, n] of A) { const d = n - (B.get(k) || 0); for (let i = 0; i < d; i++) gone.push(k.split('\u0001')); }
      for (const [k, n] of B) { const d = n - (A.get(k) || 0); for (let i = 0; i < d; i++) added.push(k.split('\u0001')); }
      cmp.hitsGone = gone; cmp.hitsAdded = added; cmp.totals1030 = { files: old.perFile.length, hits: old.hits.length };
    } else cmp.error = 'check10-hardcoded.json not readable';
    R.perFile = perFile; R.distinctValues = distinctValues; R.hits = hits; R.epochAndCycleStart = ep; R.against1030 = cmp;
    const tot = k => perFile.reduce((a, x) => a + x[k], 0);
    line = `hard-coded in Templates: ${hits.length} hits in ${perFile.filter(x => x.iso + x.year + x.monthName + x.path + x.noteLinkLiteral).length} of ${perFile.length} files (298 in 22 of 24 at 10:30): iso ${tot('iso')}, year ${tot('year')}, monthName ${tot('monthName')}, path ${tot('path')}, noteLinkLiteral ${tot('noteLinkLiteral')}, on comment lines ${tot('inComment')}; `
      + `new files ${(cmp.newFiles || []).join(', ') || 'none'}; files with different counts ${(cmp.filesWithDifferentCounts || []).map(x => x.p.replace('Templates/', '')).join(', ') || 'none'} (unchanged files among them: ${(cmp.unchangedFilesWithDifferentCounts || []).length}); hits added ${(cmp.hitsAdded || []).length}, gone ${(cmp.hitsGone || []).length}; `
      + `EPOCH / 2026-10-03 lines: ${ep.length} in ${[...new Set(ep.map(x => x[0]))].length} files (${[...new Set(ep.map(x => x[0].split('/').slice(-2).join('/')))].join(', ')})`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
