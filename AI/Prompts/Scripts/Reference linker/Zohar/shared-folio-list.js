(async () => {
  // Item 5 (28 Oct 2026), read-only: links to a Zohar folio side held by two main-text notes (vols. 1-9: one parashah ends
  // and the next begins on it). Lists every link to the five blocks named on 26 Oct (z1-193a, z1-165b, z3-156b, z2-32a, z1-120b),
  // to either holder, with the citing line; counts the same for every other shared block; dumps the citing and holding notes.
  const V = app.vault, mc = app.metadataCache, ad = V.adapter, TAG = 'pf417-shared';
  const FIVE = new Set(['z1-193a', 'z1-165b', 'z3-156b', 'z2-32a', 'z1-120b']);
  const main = V.getMarkdownFiles().filter(f => /^Zohar [1-9]\.\d\d - /.test(f.basename));
  const holders = {};
  for (const f of main) for (const id of Object.keys((mc.getFileCache(f) || {}).blocks || {})) if (/^z[1-3]-\d+[ab]$/.test(id)) (holders[id] = holders[id] || []).push(f);
  const shared = Object.fromEntries(Object.entries(holders).filter(([, v]) => v.length > 1));
  const rows = [], counts = {}, need = new Set();
  for (const f of V.getMarkdownFiles()) {
    const c = mc.getFileCache(f) || {};
    for (const l of [...(c.links || []), ...(c.embeds || [])]) {
      const i = l.link.indexOf('#^'); if (i < 0) continue;
      const id = l.link.slice(i + 2); if (!shared[id]) continue;
      const p = l.link.slice(0, i); const t = p ? mc.getFirstLinkpathDest(p, f.path) : f; if (!t || !shared[id].includes(t)) continue;
      const k = id + ' -> ' + t.basename.slice(6, 10); counts[k] = (counts[k] || 0) + 1;
      if (!FIVE.has(id)) continue;
      rows.push({ path: f.path, line: l.position.start.line + 1, col: l.position.start.col, original: l.original, block: id, target: t.basename, holders: shared[id].map(h => h.basename) });
      need.add(f.path); shared[id].forEach(h => need.add(h.path));
    }
  }
  const dump = {}; for (const p of need) dump[p] = await V.read(V.getAbstractFileByPath(p));
  await ad.write(`.work/out/${TAG}.json`, JSON.stringify({ shared: Object.fromEntries(Object.entries(shared).map(([k, v]) => [k, v.map(h => h.basename)])), counts, rows }, null, 1));
  await ad.write(`.work/out/${TAG}-dump.json`, JSON.stringify(dump));
  return `${TAG}: ${Object.keys(shared).length} shared blocks; links to them ${Object.values(counts).reduce((a, b) => a + b, 0)}; to the five ${rows.length} in ${new Set(rows.map(r => r.path)).size} notes; dumped ${need.size} notes`;
})()
