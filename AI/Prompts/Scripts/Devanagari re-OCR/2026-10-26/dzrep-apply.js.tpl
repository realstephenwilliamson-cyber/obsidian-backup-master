(async () => {
  // __TAG__ (26 Oct 2026, decision 7): replace Dyczkowski's Tantraloka volumes with the re-OCR'd copies (same page images, new text layer on
  // the pages that had a stray glyph after ि). For each entry in .work/xfer/dzrep.json: check the old file is the one that was re-OCR'd
  // (size + SHA-256), join the parts in .work/xfer/dzn/, check size and SHA-256, copy the old PDF to the backup folder, write the new
  // bytes with modifyBinary (links stay), read back, remove the parts, add the dated line to the Catalog notes that link the PDF.
  // Adapted from AI/Prompts/Scripts/Devanagari re-OCR/pdfrep-apply.js. Dry unless the first line is // APPLY.
  const ad = app.vault.adapter, MC = app.metadataCache, DRY = window.DRY !== false, BK = '.work/backup-corrections-2026-10-26/s8-dyczkowski/', PD = '.work/xfer/dzn/';
  const L = JSON.parse(await ad.read('.work/xfer/dzrep.json')); const rep = [];
  const hex = b => Array.from(new Uint8Array(b)).map(x => x.toString(16).padStart(2, '0')).join('');
  for (const e of L) {
    const f = app.vault.getAbstractFileByPath(e.target); if (!f) { rep.push(['missing', e.target]); continue; }
    const old = await ad.readBinary(e.target); const osha = hex(await crypto.subtle.digest('SHA-256', old));
    if (old.byteLength !== e.old_size || osha !== e.old_sha256) { rep.push(['old file differs', e.target, old.byteLength]); continue; }
    const bufs = []; let ok = true;
    for (const p of e.parts) { if (!(await ad.exists(PD + p))) { ok = false; rep.push(['part missing', e.target, p]); break; } bufs.push(new Uint8Array(await ad.readBinary(PD + p))); }
    if (!ok) continue;
    const n = bufs.reduce((a, b) => a + b.length, 0); const all = new Uint8Array(n); let o = 0; for (const b of bufs) { all.set(b, o); o += b.length; }
    const sha = hex(await crypto.subtle.digest('SHA-256', all.buffer));
    if (n !== e.size || sha !== e.sha256) { rep.push(['checksum', e.target, n, sha]); continue; }
    const cats = Object.entries(MC.resolvedLinks).filter(([s, m]) => m[e.target] && s.includes('Catalog/')).map(([s]) => s);
    if (DRY) { rep.push(['ok (dry)', e.target, n, cats]); continue; }
    const dst = BK + e.target.split('/').pop(); if (!(await ad.exists(BK))) await ad.mkdir(BK.slice(0, -1));
    if (!(await ad.exists(dst))) await ad.writeBinary(dst, old);
    const bk = hex(await crypto.subtle.digest('SHA-256', await ad.readBinary(dst))); if (bk !== (e.orig_sha256 || e.old_sha256)) { rep.push(['BACKUP CHECK FAILED', e.target]); continue; }  // a second pass keeps the original as the backup
    await app.vault.modifyBinary(f, all.buffer);
    const back = hex(await crypto.subtle.digest('SHA-256', await ad.readBinary(e.target)));
    if (back !== e.sha256) { rep.push(['WRITE CHECK FAILED', e.target]); continue; }
    for (const p of e.parts) await ad.remove(PD + p);
    // catalog line: one paragraph for all eleven volumes, written by a separate edits job after the last volume
    rep.push(['replaced', e.target, n, cats]);
  }
  await ad.write('.work/out/__TAG__.detail.json', JSON.stringify(rep, null, 1));
  return (DRY ? 'DRY __TAG__: ' : 'APPLIED __TAG__: ') + JSON.stringify(rep.map(r => [r[0], r[1].split('/').pop(), r[2], r[3]]));
})()
