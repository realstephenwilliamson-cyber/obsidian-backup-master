__APPLY__(async () => {
  const DRY = window.DRY !== false; const ad = app.vault.adapter, V = app.vault, mc = app.metadataCache;
  const WHICH = __WHICH__; const EDIT = __EDIT__; const E = JSON.parse(await ad.read('.work/pe-big/edits.json'));
  const BK = '.work/backup-sefaria-2026-10-22/big/'; const probs = []; let made = 0, total = 0;
  const names = new Set(V.getMarkdownFiles().map(f => f.basename.toLowerCase()));
  const unres = () => { let uf = 0, ul = 0; for (const o of Object.values(mc.unresolvedLinks)) { const k = Object.keys(o); if (k.length) { uf++; for (const x of k) ul += o[x]; } } return uf + '/' + ul; };
  const u0 = unres();
  for (const i of WHICH) {
    const N = JSON.parse(await ad.read(`.work/pe-big/b${i}.json`)); const paths = Object.keys(N).sort(); total += paths.length;
    for (const p of paths) { if (await ad.exists(p)) probs.push('exists ' + p); else if (names.has(p.split('/').pop().slice(0, -3).toLowerCase())) probs.push('name clash ' + p); }
    if (probs.length || DRY) continue;
    for (const p of paths) {
      const d = p.slice(0, p.lastIndexOf('/'));
      if (!(await ad.exists(d))) { try { await V.createFolder(d); } catch (e) { if (!(await ad.exists(d))) await ad.mkdir(d); } }
      await V.create(p, N[p]); made++;
      if (made % 100 === 0) await new Promise(r => setTimeout(r, 12000));   // let Omnisearch keep up (house lesson of 7 Oct)
    }
  }
  const newText = {};
  if (EDIT) {
    const byFile = {}; for (const [p, a, b] of E.edits) (byFile[p] = byFile[p] || []).push([a, b]);
    for (const [p, list] of Object.entries(byFile)) {
      const f = V.getAbstractFileByPath(p); if (!f) { probs.push('missing ' + p); continue; }
      let t = await V.read(f);
      for (const [a, b] of list) { const n = t.split(a).length - 1; if (n !== 1) probs.push(`anchor x${n} in ${p}: ${a.slice(0, 50)}`); else t = t.replace(a, () => b); }
      newText[p] = t;
    }
    if (!probs.length && !DRY) for (const [p, t] of Object.entries(newText)) { const f = V.getAbstractFileByPath(p); const bp = BK + p; const d = bp.slice(0, bp.lastIndexOf('/')); if (!(await ad.exists(d))) await ad.mkdir(d); await ad.write(bp, await V.read(f)); await V.modify(f, t); }
  }
  if (probs.length) return '__NAME__: ' + (DRY ? 'DRY ' : '') + 'PROBLEMS ' + probs.slice(0, 15).join(' | ') + ' … ' + probs.length;
  if (!DRY) await new Promise(r => setTimeout(r, 8000));
  return `__NAME__: ${DRY ? 'would create' : 'created'} ${DRY ? total : made} notes from bundles ${WHICH.join(',')}` + (EDIT ? `; ${DRY ? 'would edit' : 'edited'} ${Object.keys(newText).length} notes` : '') + `; unresolved ${u0} → ${unres()}`;
})()
