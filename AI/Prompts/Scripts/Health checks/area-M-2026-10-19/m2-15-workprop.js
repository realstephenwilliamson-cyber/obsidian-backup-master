(async () => {
  // Area M, new check 15 (19 Oct 2026): does every note in Library/ and Texts/ name its work in a frontmatter property?
  // Stephen wants the File properties pane to say what he is reading when a link lands him mid-note. A note counts as
  // naming its work when one of `work`, `book`, `source`, `collection` has a non-empty value. Reported by folder:
  // (1) notes with none of the four; (2) separately, notes with none of the four but a `title` (title is not accepted),
  // with the sub-count whose only property is `title`; (3) notes rescued only by a key that is present but empty.
  // For each folder the most common property-name sets among the notes in (1) and (2), and their `type` values, so that
  // what they do carry (e.g. source_pdf) can be seen. Lists are grouped by parent folder (file names only).
  // Read-only: writes only .work/out/areaM2/workprop.json.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const NAME = 'workprop', OUT = '.work/out/areaM2';
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const R = { job: 'm2-15-workprop', when: new Date().toISOString(), accepted: ['work', 'book', 'source', 'collection'] };
  let line = '';
  try {
    const KEYS = ['work', 'book', 'source', 'collection'];
    const empty = v => v === null || v === undefined || (typeof v === 'string' && !v.trim()) || (Array.isArray(v) && !v.filter(x => x !== null && x !== undefined && String(x).trim()).length);
    const md = app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Library/') || f.path.startsWith('Texts/'));
    const g2 = p => { const s = p.split('/'); return s.slice(0, Math.min(2, s.length - 1)).join('/'); };
    const g3 = p => { const s = p.split('/'); return s.slice(0, Math.min(3, s.length - 1)).join('/'); };
    const parent = p => p.slice(0, p.lastIndexOf('/'));
    const top = {}, mid = {}, lists = { none: {}, titleOnly: {} }, sets = { none: {}, titleOnly: {} }, types = { none: {}, titleOnly: {} };
    const tot = { notes: md.length, named: 0, none: 0, noneWithoutFrontmatter: 0, titleOnly: 0, titleIsTheOnlyProperty: 0, keyPresentButEmpty: 0, byKey: {} };
    let n = 0;
    for (const f of md) {
      const fm = (MC.getFileCache(f) || {}).frontmatter || {};
      const has = KEYS.filter(k => k in fm && !empty(fm[k]));
      const emptyOnly = !has.length && KEYS.some(k => k in fm);
      const cls = has.length ? 'named' : (!empty(fm.title) ? 'titleOnly' : 'none');
      for (const k of has) inc(tot.byKey, k);
      for (const [o, k] of [[top, g2(f.path)], [mid, g3(f.path)]]) { const e = o[k] = o[k] || { notes: 0, named: 0, none: 0, titleOnly: 0 }; e.notes++; e[cls]++; }
      tot[cls]++;
      if (cls !== 'named') {
        if (emptyOnly) tot.keyPresentButEmpty++;
        (lists[cls][parent(f.path)] = lists[cls][parent(f.path)] || []).push(f.basename);
        const g = g3(f.path); sets[cls][g] = sets[cls][g] || {}; inc(sets[cls][g], Object.keys(fm).sort().join(', ') || '(no frontmatter)');
        types[cls][g] = types[cls][g] || {}; inc(types[cls][g], fm.type === undefined ? '(no type)' : String(fm.type));
        if (cls === 'none' && !Object.keys(fm).length) tot.noneWithoutFrontmatter++;
        if (cls === 'titleOnly' && Object.keys(fm).length === 1) tot.titleIsTheOnlyProperty++;
      }
      if (++n % 2000 === 0) { guard('notes ' + n); await new Promise(r => setTimeout(r, 0)); }
    }
    const topSets = o => Object.fromEntries(Object.entries(o).map(([g, s]) => [g, Object.entries(s).sort((a, b) => b[1] - a[1]).slice(0, 5)]));
    R.totals = tot; R.byTopFolder = top;
    R.byWorkFolder = Object.fromEntries(Object.entries(mid).filter(([, e]) => e.none || e.titleOnly).sort((a, b) => (b[1].none + b[1].titleOnly) - (a[1].none + a[1].titleOnly)));
    R.foldersAllNamed = Object.entries(mid).filter(([, e]) => !e.none && !e.titleOnly).length;
    R.propertySets = { none: topSets(sets.none), titleOnly: topSets(sets.titleOnly) }; R.typeValues = types;
    R.listNone = lists.none; R.listTitleOnly = lists.titleOnly;
    const fmt = cls => Object.entries(top).filter(([, e]) => e[cls]).sort((a, b) => b[1][cls] - a[1][cls]).map(([k, e]) => `${k} ${e[cls]}/${e.notes}`).join(', ') || 'none';
    line = `work property: ${md.length} notes in Library/ and Texts/; named by work/book/source/collection ${tot.named} (work ${tot.byKey.work || 0}, book ${tot.byKey.book || 0}, source ${tot.byKey.source || 0}, collection ${tot.byKey.collection || 0}); `
      + `none of the four and no title ${tot.none} (${tot.noneWithoutFrontmatter} without frontmatter): ${fmt('none')}; only title ${tot.titleOnly} (title the only property ${tot.titleIsTheOnlyProperty}): ${fmt('titleOnly')}; `
      + `a key present but empty and nothing else ${tot.keyPresentButEmpty}; work folders with a gap ${Object.keys(R.byWorkFolder).length}, without ${R.foldersAllNamed}`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
