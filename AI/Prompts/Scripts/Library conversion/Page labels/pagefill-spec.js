(async () => {
  // pf276 (26 Oct 2026, third session): read-only. As pf275, written as an edits-job2 spec (.work/edits/pagefill27.json):
  // (1) a *[PDF K]* marker inside a numbered run takes the counted number (both neighbours printed in the same numbering, numbers differing
  //     by exactly their PDF distance, at most 20 pages apart); (2) each chapter note's page_range = first–last printed marker (empty if none);
  //     (3) its index line's label "(pp. a–b)", or "(PDF a–b)" when the note has no printed page. Notes with a printed marker that is not a
  //     plain number or roman numeral (two-page labels, letters) keep their range and label (listed). Backup .work/backup-corrections-2026-10-26/c-pagefill.
  const MC = app.metadataCache;
  const R2I = s => { const v = { i: 1, v: 5, x: 10, l: 50, c: 100, d: 500, m: 1000 }; let t = 0, p = 0; for (const ch of s.toLowerCase().split('').reverse()) { const n = v[ch]; if (!n) return null; if (n < p) t -= n; else { t += n; p = n; } } return t; };
  const I2R = n => { const t = [[1000, 'm'], [900, 'cm'], [500, 'd'], [400, 'cd'], [100, 'c'], [90, 'xc'], [50, 'l'], [40, 'xl'], [10, 'x'], [9, 'ix'], [5, 'v'], [4, 'iv'], [1, 'i']]; let s = ''; for (const [v, r] of t) while (n >= v) { s += r; n -= v; } return s; };
  const val = N => /^\d+$/.test(N) ? ['a', +N] : (/^[ivxlcdm]+$/.test(N) && R2I(N) && I2R(R2I(N)) === N ? ['r', R2I(N)] : null);
  const files = app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Library/'));
  const byName = new Map(files.map(f => [f.basename, f]));
  const E = {}, add = (p, o, n) => (E[p] = E[p] || []).push([o, n]);
  const rep = { markers: 0, ranges: 0, labels: 0, odd: [], books: 0, skippedEpub: 0 };
  for (const f of files) {
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || fm.type !== 'book') continue;
    const it = await app.vault.cachedRead(f); const lines = it.split('\n');
    const items = []; lines.forEach((l, i) => { const m = /^- \[\[([^\]|#]+)(?:\|[^\]]*)?\]\] \((pp\.|PDF) ([^)]*)\)\s*$/.exec(l); if (m) { const cf = byName.get(m[1].split('/').pop()); if (cf) items.push({ l, cf }); } });
    if (!items.length) continue;
    const all = [];
    for (const x of items) { x.t = await app.vault.cachedRead(x.cf); x.mk = [...x.t.matchAll(/^\*\[(p\.|PDF) ([^\]]+)\]\* \^pg(\d+)\s*$/gm)].map(m => ({ kind: m[1], N: m[2], K: +m[3], line: m[0] })); for (const m of x.mk) all.push({ ...m, x }); }
    const pr0 = all.filter(m => m.kind === 'p.');
    if (pr0.length && pr0.every(m => m.N === String(m.K))) { rep.skippedEpub++; continue; }
    rep.books++;
    all.sort((a, b) => a.K - b.K);
    const printed = all.filter(m => m.kind === 'p.' && val(m.N));
    const newN = new Map();
    for (const m of all) {
      if (m.kind !== 'PDF') continue;
      let prev = null, next = null; for (const p of printed) { if (p.K < m.K) prev = p; else if (p.K > m.K) { next = p; break; } }
      if (!prev || !next || next.K - prev.K > 20) continue;
      const a = val(prev.N), b = val(next.N); if (!a || !b || a[0] !== b[0] || b[1] - a[1] !== next.K - prev.K) continue;
      const n = a[1] + (m.K - prev.K); const N = a[0] === 'a' ? String(n) : I2R(n);
      newN.set(m.x.cf.path + '#' + m.K, N);
      const nl = m.line.replace('*[PDF ' + m.N + ']*', '*[p. ' + N + ']*'); add(m.x.cf.path, m.line, nl); rep.markers++;
    }
    for (const x of items) {
      const vals = x.mk.map(m => m.kind === 'p.' ? m.N : (newN.get(x.cf.path + '#' + m.K) ?? null)).filter(v => v !== null);
      if (vals.some(v => !val(v))) { rep.odd.push([x.cf.path, vals.filter(v => !val(v)).slice(0, 3)]); continue; }
      const newPR = vals.length ? (vals[0] === vals[vals.length - 1] ? vals[0] : vals[0] + '–' + vals[vals.length - 1]) : '';
      const prLine = x.t.split('\n').find(l => /^page_range:/.test(l));
      if (prLine !== undefined) { const cur = prLine.replace(/^page_range:\s*/, '').replace(/^"(.*)"$/, '$1'); if (cur !== newPR) { add(x.cf.path, prLine + '\n', 'page_range: "' + newPR + '"\n'); rep.ranges++; } }
      const ks = x.mk.map(m => m.K); if (!ks.length) continue;
      const lab = newPR ? '(pp. ' + newPR + ')' : '(PDF ' + (ks[0] === ks[ks.length - 1] ? ks[0] : ks[0] + '–' + ks[ks.length - 1]) + ')';
      const newL = x.l.replace(/\((pp\.|PDF) [^)]*\)\s*$/, lab);
      if (newL !== x.l) { add(f.path, x.l, newL); rep.labels++; }
    }
  }
  await app.vault.adapter.write('.work/edits/pagefill27.json', JSON.stringify({ backup: '.work/backup-corrections-2026-10-26/c-pagefill', edits: E }));
  await app.vault.adapter.write('.work/out/pf276-pagefill-spec.json', JSON.stringify(rep, null, 1));
  return `pf276-pagefill-spec: ${rep.books} books; ${rep.markers} markers, ${rep.ranges} page_range, ${rep.labels} labels in ${Object.keys(E).length} notes; odd ${rep.odd.length}; EPUB-like skipped ${rep.skippedEpub}`;
})()
