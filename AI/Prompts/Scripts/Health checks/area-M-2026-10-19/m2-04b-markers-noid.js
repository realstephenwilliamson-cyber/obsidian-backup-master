(async () => {
  // Area M, follow-up to check 4 (19 Oct 2026; optional, read-only): page-marker lines WITHOUT a block id. The 10:30 run
  // reported 0 marker lines lacking a ^pg id in Library, but the Paramarthasara (Bansat-Boudon) chapters (414 lines), The
  // Essential Kabbalah (Matt) (102 lines in the staged copies) and single lines in Padoux and Ehrman carry bare "[p. N]"
  // lines. Whole vault: lines that are only a marker, `[p. N]`, `*[p. N]*`, `[PDF n]` or `*[PDF n]*`, with no `^id`
  // (bare), by book folder (first three path segments), with the first line numbers, whether a blank line follows, and
  // the same counts for marker lines that end in a ^pgK id (for comparison with the 114,805 of 10:30). Nothing is changed.
  // Writes only .work/out/areaM2/markers-noid.json. Memory guard 300 MB below the heap limit.
  const ad = app.vault.adapter, T0 = Date.now();
  const NAME = 'markers-noid', OUT = '.work/out/areaM2';
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const g3 = p => { const s = p.split('/'); return s.slice(0, Math.min(3, s.length - 1)).join('/'); };
  const R = { job: 'm2-04b-markers-noid', when: new Date().toISOString() };
  let line = '';
  try {
    const md = app.vault.getMarkdownFiles();
    const BARE = /^\s*\*?\[(?:p\.|PDF) [^\]]+\]\*?\s*$/, WITHID = /^\s*\*?\[(?:p\.|PDF) [^\]]+\]\*? \^pg\d+\s*$/;
    const byBook = {}; let bare = 0, withId = 0, bareNotes = 0, bareNoBlank = 0, withIdNotes = 0;
    for (let i = 0; i < md.length; i += 40) {
      const ch = md.slice(i, i + 40); const tx = await Promise.all(ch.map(f => app.vault.cachedRead(f).catch(() => '')));
      ch.forEach((f, j) => {
        const L = tx[j].split(/\r?\n/); let nb = 0, ni = 0; const first = [];
        L.forEach((l, k) => { if (WITHID.test(l)) ni++; else if (BARE.test(l)) { nb++; if (first.length < 3) first.push(k + 1); if ((L[k + 1] || '').trim() !== '') bareNoBlank++; } });
        if (ni) { withId += ni; withIdNotes++; }
        if (nb) { bare += nb; bareNotes++; const b = byBook[g3(f.path)] = byBook[g3(f.path)] || { notes: 0, bareLines: 0, idLines: 0, examples: [] }; b.notes++; b.bareLines += nb; b.idLines += ni; if (b.examples.length < 3) b.examples.push([f.path, first]); }
      });
      if (i % 2000 === 0) guard('read ' + i);
    }
    R.totals = { notes: md.length, bareMarkerLines: bare, notesWithBare: bareNotes, bareNotFollowedByBlank: bareNoBlank, markerLinesWithPgId: withId, notesWithPgId: withIdNotes, at1030: { markerLines: 114805, notes: 5134, lackingPgIdInLibrary: 0 } };
    R.byBook = Object.fromEntries(Object.entries(byBook).sort((a, b) => b[1].bareLines - a[1].bareLines));
    line = `page markers without a block id: ${bare} lines in ${bareNotes} notes (${Object.keys(byBook).length} folders: ${Object.entries(R.byBook).slice(0, 8).map(([k, v]) => k.split('/').pop() + ' ' + v.bareLines).join(', ')}), not followed by a blank line ${bareNoBlank}; marker lines with ^pgK ${withId} in ${withIdNotes} notes (114,805 / 5,134 at 10:30)`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
