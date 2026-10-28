(async () => {
  // Sifra di-Tsni'uta (Zohar 5.06), Stephen's yes of 27 Oct 2026: links into Matt's plain copy of the text (block ids ^…)
  // move to the same passage in his annotated copy (^…-c) where that block exists. Only the subpath changes; labels stay.
  // Positions come from Obsidian's link cache and are checked against the text before any change. Backups first.
  const DRY = window.DRY !== false, V = app.vault, mc = app.metadataCache, ad = V.adapter, BK = '.work/backup-illeg-2026-10-27/sifra/', TAG = 'sifra-retarget';
  const src = V.getMarkdownFiles().filter(f => /^Zohar 5\.06\b/.test(f.basename));
  if (src.length !== 1) return `${TAG}: found ${src.length} notes named Zohar 5.06…`;
  const S = src[0], blocks = new Set(Object.keys((mc.getFileCache(S) || {}).blocks || {}));
  const R = { note: S.path, blocks: blocks.size, links: 0, plain: 0, toMove: 0, noTwin: {}, already: 0, toNote: 0, notes: 0, refused: [] };
  const mk = async d => { const segs = d.split('/'); let p = ''; for (const s of segs) { p = p ? p + '/' + s : s; if (!(await ad.exists(p))) await ad.mkdir(p); } };
  for (const f of V.getMarkdownFiles()) {
    const c = mc.getFileCache(f) || {}; const ls = [...(c.links || []), ...(c.embeds || [])];
    const hits = [];
    for (const l of ls) {
      const [p, sub] = l.link.split('#'); if (!p && f !== S) continue;
      const t = p ? mc.getFirstLinkpathDest(p, f.path) : f; if (t !== S) continue;
      R.links++;
      if (!sub) { R.toNote++; continue; }
      if (!sub.startsWith('^')) continue;
      const id = sub.slice(1);
      if (id.endsWith('-c')) { R.already++; continue; }
      R.plain++;
      if (!blocks.has(id + '-c')) { R.noTwin[id] = (R.noTwin[id] || 0) + 1; continue; }
      hits.push({ l, id });
    }
    if (!hits.length) continue;
    const text = await V.read(f); let u = text, ok = true;
    for (const { l, id } of hits.sort((a, b) => b.l.position.start.offset - a.l.position.start.offset)) {
      const s = l.position.start.offset, e = l.position.end.offset, orig = u.slice(s, e);
      if (orig !== l.original || orig.split('#^' + id).length !== 2) { ok = false; R.refused.push(f.basename + ': ' + l.original); break; }
      u = u.slice(0, s) + orig.replace('#^' + id, '#^' + id + '-c') + u.slice(e);
    }
    if (!ok) continue;
    R.toMove += hits.length; R.notes++;
    if (!DRY) { const bp = BK + f.path; await mk(bp.slice(0, bp.lastIndexOf('/'))); if (!(await ad.exists(bp))) await ad.write(bp, text); await V.process(f, t => { if (t !== text) throw new Error('changed under us: ' + f.path); return u; }); }
  }
  await new Promise(r => setTimeout(r, 3000));
  let n = 0, k = 0; for (const o of Object.values(mc.unresolvedLinks)) { const c = Object.values(o).reduce((a, b) => a + b, 0); if (c) { n++; k += c; } }
  await ad.write(`.work/out/${TAG}${DRY ? '-dry' : ''}.json`, JSON.stringify(R, null, 1));
  return `${TAG}${DRY ? ' (dry run)' : ''}: ${S.basename}: ${R.blocks} blocks; links into it ${R.links} (to the note ${R.toNote}, already annotated ${R.already}, plain-copy ${R.plain}); ${DRY ? 'would move' : 'moved'} ${R.toMove} in ${R.notes} notes; no -c twin for ${Object.keys(R.noTwin).length} ids; refused ${R.refused.length}; unresolved ${n}/${k}`;
})()
