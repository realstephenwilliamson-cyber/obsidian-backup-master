(async () => {
  // Area M re-run, check 7 (19 Oct 2026, after Part 1): duplicate file names and file and folder names against the ASCII
  // rule. Changed since 10:30 by the new files (2 scholar pages, CIS plan, scratchpad, Habits.base, Flashcards.base, a 15th
  // view.js, 108 `Card NNN …` notes, 4 `CIS Ch. N cards` notes). Rules as at 10:30 (with m06's corrected copy-ending rule):
  // duplicate = same file name, extension included, ignoring case; bad name = non-ASCII (allowed in Library/Lexicons by the
  // Guide), one of [ ] # ^ | : * ? " < > \, a double space, or a copy ending " (1)", " (2)", " copy" before the extension
  // (a year such as "(2013)" is not one). Bare-name links to a duplicated note name are counted from the cache.
  // Compared with .work/out/areaM/check07-names.json. Read-only: writes only .work/out/areaM2/names.json.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const NAME = 'names', OUT = '.work/out/areaM2', CUTOFF = Date.parse('2026-10-19T14:30:00Z');
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const R = { job: 'm2-07-names', when: new Date().toISOString() };
  let line = '';
  try {
    const files = app.vault.getFiles(), md = app.vault.getMarkdownFiles();
    const folders = app.vault.getAllLoadedFiles().filter(f => f.children && f.path !== '/' && f.path !== '');
    // duplicates
    const byName = {}; for (const f of files) (byName[f.name.toLowerCase()] = byName[f.name.toLowerCase()] || []).push(f);
    const dupMd = [], dupOther = [];
    for (const [n, arr] of Object.entries(byName)) if (arr.length > 1) { const e = { name: n, n: arr.length, md: arr[0].extension === 'md', folders: [...new Set(arr.map(f => f.path.split('/')[0]))], paths: arr.map(f => f.path) }; (e.md ? dupMd : dupOther).push(e); }
    const pairs = {}; for (const e of dupMd) { const k = e.folders.slice().sort().join(' + '); pairs[k] = pairs[k] || { sets: 0, files: 0 }; pairs[k].sets++; pairs[k].files += e.n; }
    const amb = new Set(dupMd.map(e => e.name.replace(/\.md$/, '')));
    const bare = { links: 0, byName: {}, sources: [] };
    for (const f of md) { const c = MC.getFileCache(f); if (!c) continue; for (const l of [...(c.links || []), ...(c.embeds || []), ...(c.frontmatterLinks || [])]) { const p = l.link.split('#')[0].toLowerCase(); if (!p.includes('/') && amb.has(p)) { bare.links++; inc(bare.byName, p); if (bare.sources.length < 50) bare.sources.push([f.path, l.link]); } } }
    guard('dups');
    // names
    const RULES = { nonAscii: n => /[^\x00-\x7F]/.test(n), forbidden: n => /[\[\]#^|:*?"<>\\]/.test(n), doubleSpace: n => /  /.test(n), copyEnding: (n, isFolder) => isFolder ? / \(\d{1,2}\)$| copy( \d+)?$/i.test(n) : / \(\d{1,2}\)\.[^.]+$| copy( \d+)?\.[^.]+$/i.test(n) };
    const bad = [];
    const test = (p, n, isFolder) => { const r = Object.keys(RULES).filter(k => RULES[k](n, isFolder)); if (r.length) bad.push({ p, folder: isFolder, rules: r }); };
    for (const f of files) test(f.path, f.name, false);
    for (const d of folders) test(d.path, d.name, true);
    const lex = p => p.startsWith('Library/Lexicons/');
    const counts = { files: {}, folders: {} }, byFolder = {}, byFolderExLex = {};
    for (const b of bad) { for (const r of b.rules) inc(counts[b.folder ? 'folders' : 'files'], r); const top = b.p.split('/').slice(0, 2).join('/'); inc(byFolder, top); if (!lex(b.p)) inc(byFolderExLex, top); }
    const outside = bad.filter(b => !lex(b.p) || b.rules.some(r => r !== 'nonAscii'));
    const longLib = files.filter(f => f.path.startsWith('Library/') && f.extension === 'pdf' && f.name.length > 100).map(f => [f.path, f.name.length]);
    // created since 10:30: the names
    const created = files.filter(f => f.stat.ctime >= CUTOFF);
    const createdBad = bad.filter(b => created.some(f => f.path === b.p));
    // against 10:30
    const old = await readJSON('.work/out/areaM/check07-names.json');
    const cmp = {};
    if (old) {
      const oldSets = Object.fromEntries([...old.duplicateSets.markdown, ...old.duplicateSets.other].map(e => [e.name, e.n]));
      const newSets = Object.fromEntries([...dupMd, ...dupOther].map(e => [e.name, e.n]));
      cmp.duplicateSetsNew = Object.keys(newSets).filter(k => !(k in oldSets)).map(k => [k, newSets[k]]);
      cmp.duplicateSetsGone = Object.keys(oldSets).filter(k => !(k in newSets));
      cmp.duplicateSetsChangedSize = Object.keys(newSets).filter(k => k in oldSets && oldSets[k] !== newSets[k]).map(k => [k, oldSets[k], newSets[k]]);
      const oldOut = old.badNames.listOutsideLexicons.map(x => x.p), newOut = outside.map(x => x.p);
      cmp.badOutsideLexiconsNew = newOut.filter(p => !oldOut.includes(p)); cmp.badOutsideLexiconsGone = oldOut.filter(p => !newOut.includes(p));
      cmp.counts1030 = old.badNames.counts; cmp.lexiconsNonAscii1030 = old.badNames.lexiconsNonAsciiCount;
    } else cmp.error = 'check07-names.json not readable';
    R.duplicateSets = { markdown: dupMd, other: dupOther }; R.duplicatesByTopFolderPair = pairs; R.bareNameLinksToAmbiguousNames = bare;
    R.badNames = { counts, byFolder, byFolderExcludingLexicons: byFolderExLex, listOutsideLexicons: outside, lexiconsNonAsciiCount: bad.filter(b => lex(b.p) && b.rules.includes('nonAscii')).length };
    R.libraryPdfNamesOver100Chars = longLib; R.createdSince1030 = { files: created.length, withBadNames: createdBad }; R.against1030 = cmp;
    const viewJs = dupOther.find(e => e.name === 'view.js');
    line = `names: ${files.length} files, ${folders.length} folders; duplicate note names ${dupMd.length} set(s) (${dupMd.map(e => e.name + ' ×' + e.n).join('; ') || 'none'}; 1 at 10:30), bare-name links to them ${bare.links} (2); `
      + `other duplicate names ${dupOther.length} (12 at 10:30; view.js ×${viewJs ? viewJs.n : 0}, 14 at 10:30); new sets ${(cmp.duplicateSetsNew || []).map(x => x[0] + ' ×' + x[1]).join('; ') || 'none'}; `
      + `bad names: ${Object.entries(counts.files).map(([k, n]) => k + ' ' + n).join(', ') || 'none'} (files), ${Object.entries(counts.folders).map(([k, n]) => k + ' ' + n).join(', ') || 'none'} (folders); outside Lexicons ${outside.length} (4 at 10:30), new ${(cmp.badOutsideLexiconsNew || []).length}; `
      + `created since 10:30 ${created.length}, with a bad name ${createdBad.length}; Library PDF names over 100 characters ${longLib.length}`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
