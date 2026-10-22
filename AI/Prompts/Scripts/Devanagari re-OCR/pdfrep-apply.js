// APPLY
(async () => {
  // Decision D09 (15 Oct 2026): replace library PDFs with re-OCR'd copies (same page images, new text layer). For each entry in
  // .work/fx/pdfrep.json: join the parts in .work/d09/ (if split), check size and SHA-256, copy the old PDF to the backup folder,
  // write the new bytes over the old file (Obsidian's modifyBinary, so links stay), remove the parts, and add a dated line to the
  // catalog notes that list the PDF. Dry unless window.DRY === false.
  const ad = app.vault.adapter, MC = app.metadataCache, DRY = window.DRY !== false, BK = '.work/backup-audit-fixes-2026-10-14/d09/';
  const L = JSON.parse(await ad.read('.work/fx/pdfrep.json')); const rep = [];
  const hex = b => Array.from(new Uint8Array(b)).map(x => x.toString(16).padStart(2, '0')).join('');
  for (const e of L) {
    const f = app.vault.getAbstractFileByPath(e.target); if (!f) { rep.push(['missing', e.target]); continue; }
    const bufs = []; let ok = true;
    for (const p of e.parts) { if (!(await ad.exists('.work/d09/' + p))) { ok = false; rep.push(['part missing', p]); break; } bufs.push(new Uint8Array(await ad.readBinary('.work/d09/' + p))); }
    if (!ok) continue;
    const n = bufs.reduce((a, b) => a + b.length, 0); const all = new Uint8Array(n); let o = 0; for (const b of bufs) { all.set(b, o); o += b.length; }
    const sha = hex(await crypto.subtle.digest('SHA-256', all.buffer));
    if (n !== e.size || sha !== e.sha256) { rep.push(['checksum', e.target, n, sha]); continue; }
    const cats = Object.entries(MC.resolvedLinks).filter(([s, m]) => m[e.target] && s.startsWith('Catalog/')).map(([s]) => s);
    if (DRY) { rep.push(['ok (dry)', e.target, n, cats]); continue; }
    const dst = BK + e.target; const dir = dst.slice(0, dst.lastIndexOf('/')); if (!(await ad.exists(dir))) await ad.mkdir(dir);
    if (!(await ad.exists(dst))) await ad.writeBinary(dst, await ad.readBinary(e.target));
    await app.vault.modifyBinary(f, all.buffer);
    const back = hex(await crypto.subtle.digest('SHA-256', await ad.readBinary(e.target)));
    if (back !== e.sha256) { rep.push(['WRITE CHECK FAILED', e.target]); continue; }
    for (const p of e.parts) await ad.remove('.work/d09/' + p);
    for (const c of cats) { const cf = app.vault.getAbstractFileByPath(c); await app.vault.process(cf, t => t.includes(e.line) ? t : t.replace(/\s*$/, '\n\n' + e.line + '\n')); }
    rep.push(['replaced', e.target, n, cats]);
  }
  await ad.write('.work/out/pdfrep-' + (DRY ? 'dry' : 'real') + '-' + Date.now() + '.json', JSON.stringify(rep, null, 1));
  return (DRY ? 'dry run: ' : 'APPLIED: ') + JSON.stringify(rep.map(r => [r[0], r[1].split('/').pop(), r[2]]));
})()
