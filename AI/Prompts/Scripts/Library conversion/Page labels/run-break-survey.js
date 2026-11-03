(async () => {
  // pf624-runsurvey (3 Nov 2026, audit corrections, D-06; read-only). A wider net than pf620: a Library marker "*[p. L]* ^pgK" (L Arabic)
  // whose offset L-K differs from the offset shared by at least two Arabic markers on EACH side within four markers (same note), i.e. a
  // number that breaks a run fixed on both sides; expected = K + that offset. Catches runs of two or more misreads that pf620's
  // descent test missed (dropped digits "17" for 77, four-digit numbers in the Apostolic Fathers). Writes
  // .work/edits/audcorr-2026-11-03/run-breaks.json.
  const ad = app.vault.adapter, re = /^\*\[(?:p\. ([^\]]+)|PDF (\d+))\]\* \^pg(\d+)\s*$/, out = [];
  for (const f of app.vault.getMarkdownFiles()) {
    if (!f.path.startsWith('Library/')) continue;
    const M = []; (await app.vault.cachedRead(f)).split('\n').forEach((l, i) => { const m = l.match(re); if (m && m[1] && /^\d+$/.test(m[1])) M.push({ line: i + 1, L: +m[1], K: +m[3] }); });
    for (let i = 0; i < M.length; i++) {
      const before = M.slice(Math.max(0, i - 4), i).map(x => x.L - x.K), after = M.slice(i + 1, i + 5).map(x => x.L - x.K);
      const cand = {}; for (const o of before.concat(after)) cand[o] = (cand[o] || 0) + 1;
      for (const [o, c] of Object.entries(cand)) {
        const ob = before.filter(x => x == o).length, oa = after.filter(x => x == o).length;
        if (ob >= 2 && oa >= 2 && M[i].L - M[i].K != o && M[i].K + +o > 0) { out.push({ path: f.path, line: M[i].line, K: M[i].K, label: String(M[i].L), expected: String(M[i].K + +o), dyczkowski: f.path.includes('Tantraloka (Dyczkowski)') }); break; }
      }
    }
  }
  await ad.write('.work/edits/audcorr-2026-11-03/run-breaks.json', JSON.stringify(out, null, 1));
  const notes = new Set(out.map(x => x.path)).size;
  return `pf624-runsurvey: ${out.length} markers break a run fixed on both sides, in ${notes} notes (Dyczkowski ${out.filter(x => x.dyczkowski).length}); list .work/edits/audcorr-2026-11-03/run-breaks.json`;
})()
