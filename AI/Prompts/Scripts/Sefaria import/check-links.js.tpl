(async () => {
  // Read-only: in the given folders, every link resolves, every #^block and #heading exists, every note has frontmatter
  const SCOPE = __SCOPE__; const mc = app.metadataCache, V = app.vault; const R = { notes: 0, links: 0, bad: [], nofm: [], sub: 0 };
  const norm = h => h.replace(/[#^|\[\]]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
  for (const f of V.getMarkdownFiles()) {
    if (!SCOPE.some(s => f.path.startsWith(s))) continue; R.notes++;
    const c = mc.getFileCache(f) || {}; if (!c.frontmatter) R.nofm.push(f.path);
    for (const l of (c.links || []).concat(c.frontmatterLinks || [])) {
      R.links++; const [p, sub] = l.link.split('#'); const t = p ? mc.getFirstLinkpathDest(p, f.path) : f;
      if (!t) { R.bad.push(f.basename + ' → ' + l.link); continue; }
      if (sub === undefined) continue; R.sub++;
      const tc = mc.getFileCache(t) || {};
      if (sub.startsWith('^')) { if (!(tc.blocks || {})[sub.slice(1).toLowerCase()] && !(tc.blocks || {})[sub.slice(1)]) R.bad.push(f.basename + ' → ' + l.link + ' (no block)'); }
      else if (!(tc.headings || []).some(h => norm(h.heading) === norm(sub))) R.bad.push(f.basename + ' → ' + l.link + ' (no heading)');
    }
  }
  await app.vault.adapter.write('.work/out/__NAME__.json', JSON.stringify(R, null, 1));
  return `__NAME__: ${R.notes} notes, ${R.links} links (${R.sub} to a block or heading), ${R.bad.length} broken, ${R.nofm.length} without frontmatter; first: ${R.bad.slice(0, 8).join(' | ')}`;
})()
