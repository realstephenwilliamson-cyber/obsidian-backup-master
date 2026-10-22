// APPLY
(async () => {
  // Decision D31c (15 Oct 2026, Stephen: "start Finn too"): Finn's footnotes and verse numbers restored in the 10 converted notes.
  // Refuses if any note changed since it was read (SHA-256). Backups first; writes through vault.process; adds a line to the catalog note.
  const ad = app.vault.adapter, MC = app.metadataCache, BK = '.work/backup-audit-fixes-2026-10-14/d31c-finn/';
  const J = JSON.parse(await ad.read('.work/fx/finnfn.json'));
  const hex = b => Array.from(new Uint8Array(b)).map(x => x.toString(16).padStart(2, '0')).join('');
  const bad = [];
  for (const [n, e] of Object.entries(J.files)) {
    const f = app.vault.getAbstractFileByPath(J.folder + n); if (!f) { bad.push('missing ' + n); continue; }
    const t = await app.vault.read(f); const h = hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t)));
    if (h !== e.sha) bad.push('changed ' + n);
  }
  const cat = MC.getFirstLinkpathDest(J.catalog, '');
  if (!cat) bad.push('catalog note not found');
  if (bad.length) return 'not applied: ' + JSON.stringify(bad);
  for (const d of ['.work/backup-audit-fixes-2026-10-14', BK]) if (!(await ad.exists(d))) await ad.mkdir(d);
  for (const n of Object.keys(J.files)) { const dst = BK + n; if (!(await ad.exists(dst))) await ad.write(dst, await ad.read(J.folder + n)); }
  if (!(await ad.exists(BK + cat.name))) await ad.write(BK + cat.name, await ad.read(cat.path));
  let w = 0;
  for (const [n, e] of Object.entries(J.files)) { await app.vault.process(app.vault.getAbstractFileByPath(J.folder + n), () => e.new); w++; }
  await app.vault.process(cat, t => t.includes(J.line) ? t : t.replace(/\s*$/, '\n\n' + J.line + '\n'));
  await new Promise(r => setTimeout(r, 4000));
  let fm = 0, blocks = 0, refs = 0, defs = 0;
  for (const n of Object.keys(J.files)) {
    const f = app.vault.getAbstractFileByPath(J.folder + n); const c = MC.getFileCache(f) || {};
    if (!c.frontmatter || c.frontmatter.type !== 'book-chapter') fm++;
    blocks += Object.keys(c.blocks || {}).length;
    const t = await app.vault.read(f); defs += (t.match(/^\[\^[\w.-]+\]:/gm) || []).length; refs += (t.match(/\[\^[\w.-]+\]/g) || []).length - (t.match(/^\[\^[\w.-]+\]:/gm) || []).length;
  }
  const un = Object.entries(MC.unresolvedLinks).filter(([, m]) => Object.keys(m).length).length;
  return `APPLIED: notes written ${w}; frontmatter problems ${fm}; page blocks ${blocks}; footnote references ${refs}, definitions ${defs}; catalog ${cat.path}; unresolved files ${un}`;
})()
