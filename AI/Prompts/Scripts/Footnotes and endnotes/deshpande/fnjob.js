(async () => {
  // D31c footnotes (18 Oct 2026): write the rewritten notes of one book. Data: .work/footnotes-2026-10-18/__BOOK__.json
  // Refuses if any note changed since it was read (SHA-256). Dry run (no // APPLY line): checks and reports only.
  // Apply: backs up any note not yet in the backup folder, writes through vault.process, then checks frontmatter,
  // page block ids, footnote pairing and unresolved links.
  const ad = app.vault.adapter, MC = app.metadataCache, DRY = window.DRY !== false;
  const J = JSON.parse(await ad.read('.work/footnotes-2026-10-18/__BOOK__.json'));
  const hex = b => Array.from(new Uint8Array(b)).map(x => x.toString(16).padStart(2, '0')).join('');
  const sha = async t => hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t)));
  const pairs = t => {
    const defs = {}, refs = {};
    for (const m of t.matchAll(/^\[\^([^\]\s]+)\]:/gm)) defs[m[1]] = (defs[m[1]] || 0) + 1;
    for (const m of t.matchAll(/\[\^([^\]\s]+)\]/g)) {
      const atDef = (m.index === 0 || t[m.index - 1] === '\n') && t[m.index + m[0].length] === ':';
      if (!atDef) refs[m[1]] = (refs[m[1]] || 0) + 1;
    }
    const ids = new Set([...Object.keys(defs), ...Object.keys(refs)]);
    let bad = 0; for (const k of ids) if (defs[k] !== 1 || refs[k] !== 1) bad++;
    return { defs: Object.values(defs).reduce((a, b) => a + b, 0), refs: Object.values(refs).reduce((a, b) => a + b, 0), bad };
  };
  const unres = () => { let f = 0, l = 0; for (const m of Object.values(MC.unresolvedLinks)) { const n = Object.keys(m).length; if (n) { f++; l += n; } } return [f, l]; };
  const pgBlocks = f => Object.keys((MC.getFileCache(f) || {}).blocks || {}).filter(k => /^pg\d+$/.test(k)).length;
  const bad = [], files = [];
  for (const [n, e] of Object.entries(J.files)) {
    const f = app.vault.getAbstractFileByPath(J.folder + n); if (!f) { bad.push('missing ' + n); continue; }
    if (await sha(await app.vault.read(f)) !== e.sha) { bad.push('changed since read: ' + n); continue; }
    files.push([f, e]);
  }
  if (bad.length) return 'NOT APPLIED: ' + JSON.stringify(bad);
  const [u0f, u0l] = unres();
  const before = new Map(files.map(([f]) => [f.path, pgBlocks(f)]));
  let R = 0, D = 0, B = 0;
  for (const [, e] of files) { const p = pairs(e.new); R += p.refs; D += p.defs; B += p.bad; }
  if (DRY) return `DRY: ${files.length} notes unchanged since read and ready; new text has ${R} footnote references, ${D} definitions, ${B} unpaired ids; page blocks now ${[...before.values()].reduce((a, b) => a + b, 0)}; unresolved now ${u0f} files / ${u0l} links`;
  for (const d of [J.backup, J.backup + J.folder]) if (!(await ad.exists(d))) await ad.mkdir(d);
  for (const [f] of files) { const dst = J.backup + f.path; if (!(await ad.exists(dst))) await ad.write(dst, await ad.read(f.path)); }
  for (const [f, e] of files) await app.vault.process(f, () => e.new);
  // wait until the metadata cache has the new texts
  for (let i = 0; i < 60; i++) {
    await new Promise(r => setTimeout(r, 500));
    if (files.every(([f]) => ((MC.getFileCache(f) || {}).frontmatter || {}).text_source?.includes('18 Oct 2026'))) break;
  }
  await new Promise(r => setTimeout(r, 2000));
  let fm = 0, blk = [], R2 = 0, D2 = 0, B2 = 0;
  for (const [f] of files) {
    const c = MC.getFileCache(f) || {};
    if (!c.frontmatter || !c.frontmatter.type) fm++;
    if (pgBlocks(f) !== before.get(f.path)) blk.push(f.name + ' ' + before.get(f.path) + '->' + pgBlocks(f));
    const p = pairs(await app.vault.read(f)); R2 += p.refs; D2 += p.defs; B2 += p.bad;
  }
  const [u1f, u1l] = unres();
  return `APPLIED: ${files.length} notes written; frontmatter problems ${fm}; page block changes ${blk.length ? JSON.stringify(blk) : 'none'}; footnote references ${R2}, definitions ${D2}, unpaired ids ${B2}; unresolved links ${u0f} files / ${u0l} links before, ${u1f} / ${u1l} after`;
})()
