(async () => {
  // __TAG__ (27 Oct 2026, Dyczkowski footnotes): read-only check after an apply. For each note in __LIST__ ({p: vault path, old: footnote numbers already real before tonight}), against its
  // backup in __BACKUP__/: the divine-name count (character-class patterns, counts only) equal; Obsidian's footnote cache (footnotes,
  // footnoteRefs, by id) against the [^n] calls and [^n]: definitions in the text, each number once (a number missing from the cache fails only if it was not real before tonight); every ^pg block of the backup still
  // registered; every link or embed in the vault into the note with a heading subpath resolves to a heading; unresolved links.
  const ad = app.vault.adapter, MC = app.metadataCache, BK = '__BACKUP__', LIST = __LIST__;
  const DN = [/י[֑-ׇ]*ה[֑-ׇ]*ו[֑-ׇ]*ה/g, /\b[Yy][Hh][WwVv][Hh]\b/g, /\b[Yy][Aa][Hh][Ww][Ee][Hh]\b/g, /\b[Jj][Ee][Hh][Oo][Vv][Aa][Hh]\b/g];
  const dn = t => DN.reduce((s, r) => s + (t.match(r) || []).length, 0);
  const R = { notes: {}, headLinks: { total: 0, ok: 0, bad: [] }, fail: [] };
  const heads = {};
  for (const e of LIST) {
    const p = e.p, oldReal = new Set(e.old.map(String)); const f = app.vault.getAbstractFileByPath(p); if (!f) { R.fail.push('missing ' + p); continue; }
    const t = await app.vault.read(f), b = await ad.read(BK + '/' + p), c = MC.getFileCache(f) || {};
    const calls = [...t.matchAll(/\[\^(\d+)\](?!:)/g)].map(m => +m[1]), defs = [...t.matchAll(/^\[\^(\d+)\]:/gm)].map(m => +m[1]);
    const pgB = [...b.matchAll(/\^(pg\d+)\s*$/gm)].map(m => m[1]), blocks = c.blocks || {};
    const pgMissing = pgB.filter(id => !blocks[id]);
    heads[p] = new Set((c.headings || []).map(h => h.heading));
    const hb = new Set(((await (async () => b)()).match(/^#{1,6} .*$/gm) || []).map(h => h.replace(/^#+ /, '').trim()));
    const sameCalls = calls.length === new Set(calls).size, sameDefs = defs.length === new Set(defs).size;
    const pairs = calls.length === defs.length && [...new Set(calls)].every(n => defs.includes(n));
    const order = calls.every((n, i) => i === 0 || n > calls[i - 1]);
    const r = { dnBefore: dn(b), dnAfter: dn(t), calls: calls.length, defs: defs.length, cacheFn: (c.footnotes || []).length, cacheRefs: (c.footnoteRefs || []).length,
      once: sameCalls && sameDefs && pairs, order, pgBackup: pgB.length, pgMissing: pgMissing.length, headingsBefore: hb.size, headingsAfter: heads[p].size,
      plainLeft: (t.match(/^\d+\S{0,2}\\\. /gm) || []).length };
    const fnIds = new Set((c.footnotes || []).map(x => String(x.id).replace(/^\[\^|\]:?$/g, ''))), refIds = new Set((c.footnoteRefs || []).map(x => String(x.id).replace(/^\[\^|\]:?$/g, '')));
    r.cacheMissDefs = [...new Set(defs)].map(String).filter(n => !fnIds.has(n)); r.cacheMissCalls = [...new Set(calls)].map(String).filter(n => !refIds.has(n));
    r.cacheMissNew = r.cacheMissDefs.concat(r.cacheMissCalls).filter(n => !oldReal.has(n));
    R.notes[p] = r;
    if (r.dnBefore !== r.dnAfter) R.fail.push('divine-name count ' + p);
    if (!r.once || !r.order) R.fail.push('calls/defs ' + p);
    if (r.cacheMissNew.length) R.fail.push('cache ' + p + ' missing ' + r.cacheMissNew.slice(0, 10).join(','));
    if (r.pgMissing) R.fail.push('pg ' + p + ' ' + r.pgMissing);
  }
  for (const f of app.vault.getMarkdownFiles()) {
    const c = MC.getFileCache(f); if (!c) continue;
    for (const l of (c.links || []).concat(c.embeds || [])) {
      const i = l.link.indexOf('#'); if (i < 0) continue; const sub = l.link.slice(i + 1); if (sub.startsWith('^')) continue;
      const d = MC.getFirstLinkpathDest(l.link.slice(0, i), f.path); if (!d || !heads[d.path]) continue;
      R.headLinks.total++; if (heads[d.path].has(sub.split('#').pop())) R.headLinks.ok++; else { R.headLinks.bad.push([f.path, l.link]); }
    }
  }
  if (R.headLinks.ok !== R.headLinks.total) R.fail.push('heading links ' + (R.headLinks.total - R.headLinks.ok));
  const u = Object.values(MC.unresolvedLinks).filter(o => Object.keys(o).length); R.unresolved = u.length + '/' + u.reduce((s, o) => s + Object.values(o).reduce((a, b) => a + b, 0), 0);
  if (R.unresolved !== '__UNRES__') R.fail.push('unresolved ' + R.unresolved);
  await ad.write('.work/out/__TAG__.json', JSON.stringify(R, null, 1));
  const v = Object.values(R.notes);
  return `__TAG__: ${v.length} notes; calls ${v.reduce((s, n) => s + n.calls, 0)}, defs ${v.reduce((s, n) => s + n.defs, 0)}, cache ${v.reduce((s, n) => s + n.cacheFn, 0)}/${v.reduce((s, n) => s + n.cacheRefs, 0)}; heading links ${R.headLinks.ok}/${R.headLinks.total}; unresolved ${R.unresolved}; FAILURES ${R.fail.length}: ${R.fail.slice(0, 8).join(' | ')}`;
})()
