(async () => {
  // pf275 (26 Oct 2026, third session): read-only. Unnumbered pages inside a numbered run, and the labels built on them.
  // For every converted book (index note type: book under Library/, its contents lines "- [[note|label]] (pp. …)" / "(PDF …)"):
  // all page markers of its chapter notes, sorted by the PDF page K. A *[PDF K]* marker between two printed markers of the same numbering
  // (both arabic or both roman) whose numbers differ by exactly their PDF distance (at most 20 pages apart) takes the counted number
  // ("inside a numbered run", the Guide's rule). Then each chapter note's page_range (first–last printed) and its index label are recomputed.
  // Writes .work/out/pf275-pagefill.json: {markers: [[path, K, newN]], ranges: [[path, old, new]], labels: [[indexPath, oldLine, newLine]]}.
  const MC = app.metadataCache;
  const R2I = s => { const v = { i: 1, v: 5, x: 10, l: 50, c: 100, d: 500, m: 1000 }; let t = 0, p = 0; for (const ch of s.toLowerCase().split('').reverse()) { const n = v[ch]; if (!n) return null; if (n < p) t -= n; else { t += n; p = n; } } return t; };
  const I2R = n => { const t = [[1000, 'm'], [900, 'cm'], [500, 'd'], [400, 'cd'], [100, 'c'], [90, 'xc'], [50, 'l'], [40, 'xl'], [10, 'x'], [9, 'ix'], [5, 'v'], [4, 'iv'], [1, 'i']]; let s = ''; for (const [v, r] of t) while (n >= v) { s += r; n -= v; } return s; };
  const val = N => /^\d+$/.test(N) ? ['a', +N] : (/^[ivxlcdm]+$/i.test(N) && R2I(N) ? ['r', R2I(N)] : null);
  const files = app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Library/'));
  const byName = new Map(files.map(f => [f.basename, f]));
  const out = { markers: [], ranges: [], labels: [], skipped: [] };
  for (const f of files) {
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || fm.type !== 'book') continue;
    const it = await app.vault.cachedRead(f); const lines = it.split('\n');
    const items = []; lines.forEach((l, i) => { const m = /^- \[\[([^\]|#]+)(?:\|[^\]]*)?\]\] \((pp\.|PDF) ([^)]*)\)\s*$/.exec(l); if (m) { const cf = byName.get(m[1].split('/').pop()); if (cf) items.push({ i, l, cf }); } });
    if (!items.length) continue;
    const all = [];
    for (const x of items) { x.t = await app.vault.cachedRead(x.cf); x.mk = [...x.t.matchAll(/^\*\[(p\.|PDF) ([^\]]+)\]\* \^pg(\d+)\s*$/gm)].map(m => ({ kind: m[1], N: m[2], K: +m[3] })); for (const m of x.mk) all.push({ ...m, x }); }
    if (all.some(m => m.kind === 'p.' && m.N === String(m.K)) && all.filter(m => m.kind === 'p.').every(m => m.N === String(m.K))) { out.skipped.push([f.path, 'all printed = K (EPUB-like)']); continue; }
    all.sort((a, b) => a.K - b.K);
    const printed = all.filter(m => m.kind === 'p.' && val(m.N));
    for (const m of all) {
      if (m.kind !== 'PDF') continue;
      let prev = null, next = null; for (const p of printed) { if (p.K < m.K) prev = p; else if (p.K > m.K) { next = p; break; } }
      if (!prev || !next || next.K - prev.K > 20) continue;
      const a = val(prev.N), b = val(next.N); if (!a || !b || a[0] !== b[0]) continue;
      if (b[1] - a[1] !== next.K - prev.K) continue;
      const n = a[1] + (m.K - prev.K); const N = a[0] === 'a' ? String(n) : I2R(n);
      out.markers.push([m.x.cf.path, m.K, N]); m.newN = N;
    }
    for (const x of items) {
      const pr = x.mk.map(m => m.kind === 'p.' ? m.N : (all.find(a => a.x === x && a.K === m.K)?.newN ?? null)).filter(Boolean);
      const cfm = MC.getFileCache(x.cf)?.frontmatter || {}; const oldPR = cfm.page_range == null ? '' : String(cfm.page_range);
      const newPR = pr.length ? (pr[0] === pr[pr.length - 1] ? pr[0] : pr[0] + '–' + pr[pr.length - 1]) : '';
      if (newPR !== oldPR) out.ranges.push([x.cf.path, oldPR, newPR]);
      const ks = x.mk.map(m => m.K); const lab = newPR ? '(pp. ' + newPR + ')' : '(PDF ' + (ks[0] === ks[ks.length - 1] ? ks[0] : ks[0] + '–' + ks[ks.length - 1]) + ')';
      const newL = x.l.replace(/\((pp\.|PDF) [^)]*\)\s*$/, lab);
      if (newL !== x.l) out.labels.push([f.path, x.l, newL]);
    }
  }
  await app.vault.adapter.write('.work/out/pf275-pagefill.json', JSON.stringify(out));
  return `pf275-pagefill: ${out.markers.length} markers to number, ${out.ranges.length} page_range changes, ${out.labels.length} index labels; skipped ${out.skipped.length}`;
})()
