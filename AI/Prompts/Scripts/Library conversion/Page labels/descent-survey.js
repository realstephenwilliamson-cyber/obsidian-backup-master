(async () => {
  // pf620-pagesurvey (3 Nov 2026, audit corrections; read-only). Lists for the SDK page-reading prompt, saved to
  // .work/edits/audcorr-2026-11-03/: (D-05) placeholder suspects: a marker "*[p. K]* ^pgK" (printed number = PDF number) whose
  // neighbours do not continue it (the previous Arabic marker is not K-1 and the next is not K+1); (D-06) printed-number
  // descents among consecutive Arabic markers of a note, each with its neighbours, and "isolated" ones where the markers on both
  // sides fix the expected number exactly (prev + 2 = next). Library/ notes only; Dyczkowski's copy included but flagged.
  const ad = app.vault.adapter, OUT = '.work/edits/audcorr-2026-11-03/';
  const re = /^\*\[(?:p\. ([^\]]+)|PDF (\d+))\]\* \^pg(\d+)\s*$/;
  const sus = [], desc = []; let notes = 0, markers = 0;
  for (const f of app.vault.getMarkdownFiles()) {
    if (!f.path.startsWith('Library/')) continue;
    const lines = (await app.vault.cachedRead(f)).split('\n'); const M = [];
    lines.forEach((l, i) => { const m = l.match(re); if (m) M.push({ line: i + 1, label: m[1] ?? null, pdf: m[2] ? +m[2] : null, K: +m[3] }); });
    if (!M.length) continue; notes++; markers += M.length;
    const num = x => (x.label && /^\d+$/.test(x.label)) ? +x.label : null;
    for (let i = 0; i < M.length; i++) {
      const n = num(M[i]); if (n === null) continue;
      const prev = (() => { for (let j = i - 1; j >= 0; j--) if (num(M[j]) !== null) return M[j]; return null; })();
      const next = (() => { for (let j = i + 1; j < M.length; j++) if (num(M[j]) !== null) return M[j]; return null; })();
      const pn = prev ? num(prev) : null, nn = next ? num(next) : null;
      if (n === M[i].K && !(pn === n - 1 && prev.K === M[i].K - 1) && !(nn === n + 1 && next.K === M[i].K + 1))
        sus.push({ path: f.path, line: M[i].line, K: M[i].K, label: M[i].label, prev: prev && { K: prev.K, label: prev.label }, next: next && { K: next.K, label: next.label }, neighbourLabels: M.slice(Math.max(0, i - 2), i + 3).map(x => [x.K, x.label ?? 'PDF']) });
      if (pn !== null && n < pn) {
        const iso = (nn !== null && nn === pn + 2 && next.K === prev.K + 2 && M[i].K === prev.K + 1) ? { wrong: 'this', expected: pn + 1 } : null;
        desc.push({ path: f.path, line: M[i].line, K: M[i].K, label: M[i].label, prev: { K: prev.K, label: prev.label }, next: next && { K: next.K, label: next.label }, isolated: iso, dyczkowski: f.path.includes('Tantraloka (Dyczkowski)'), neighbourLabels: M.slice(Math.max(0, i - 3), i + 3).map(x => [x.K, x.label ?? 'PDF']) });
      }
    }
  }
  // a misread number that is too HIGH shows as a descent at the NEXT marker: mark those whose previous marker is isolated-high
  for (const d of desc) if (!d.isolated) { const p = d.prev; const pn = +p.label; const n = +d.label; if (d.neighbourLabels.length >= 3) { const before = d.neighbourLabels.filter(x => x[0] < p.K && /^\d+$/.test(x[1])).pop(); if (before && +before[1] + 2 === n && d.K === before[0] + 2 && p.K === before[0] + 1) d.isolated = { wrong: 'previous', K: p.K, label: p.label, expected: n - 1 }; } }
  const mk = async d => { let q = ''; for (const s of d.split('/')) { if (!s) continue; q = q ? q + '/' + s : s; if (!(await ad.exists(q))) await ad.mkdir(q); } };
  await mk(OUT);
  await ad.write(OUT + 'placeholder-suspects.json', JSON.stringify(sus, null, 1));
  await ad.write(OUT + 'descents.json', JSON.stringify(desc, null, 1));
  const iso = desc.filter(d => d.isolated).length, dy = desc.filter(d => d.dyczkowski).length;
  const susNotes = new Set(sus.map(s => s.path)).size;
  return `pf620-pagesurvey: ${notes} Library notes, ${markers} markers; placeholder suspects ${sus.length} in ${susNotes} notes; descents ${desc.length} (isolated misreads fixed by both neighbours ${iso}; in Dyczkowski's copy ${dy}); lists in ${OUT}`;
})()
