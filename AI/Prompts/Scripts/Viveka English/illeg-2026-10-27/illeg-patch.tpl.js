// [illegible] fills in the library copy of Dyczkowski's Tantraloka, 27-28 Oct 2026 (OCR-only pass). Data: __SRC__lib-patch.json
(async () => {
  // Per note: the length and FNV-1a hash of the text the patch was made from, line hunks [start, length, new line] in UTF-16 units,
  // and the length and hash after. A note is changed only if it is exactly that text and the result checks. Backups first.
  const DRY = window.DRY !== false, TAG = '__TAG__', V = app.vault, ad = V.adapter, SRC = '__SRC__', BK = '__BK__';
  const fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h >>> 0; };
  const backup = async (p, t) => { const bp = BK + p; const d = bp.slice(0, bp.lastIndexOf('/')); if (!(await ad.exists(d))) await ad.mkdir(d); if (!(await ad.exists(bp))) await ad.write(bp, t); };
  const patch = JSON.parse(await ad.read(SRC + 'lib-patch.json'));
  const R = { ok: 0, already: 0, hunks: 0, refused: [] };
  let n = 0;
  for (const e of patch) {
    const f = V.getAbstractFileByPath(e.path); if (!f) { R.refused.push(e.path + ': missing'); continue; }
    const t = await V.read(f);
    if (t.length === e.len1 && fnv(t) === e.h1) { R.already++; continue; }
    if (t.length !== e.len0 || fnv(t) !== e.h0) { R.refused.push(e.path.split('/').pop() + `: not the expected text (length ${t.length}/${e.len0})`); continue; }
    const hs = e.hunks.slice().sort((a, b) => b[0] - a[0]);
    let u = t; for (const [s, d, ins] of hs) u = u.slice(0, s) + ins + u.slice(s + d);
    if (u.length !== e.len1 || fnv(u) !== e.h1) { R.refused.push(e.path.split('/').pop() + ': result check failed'); continue; }
    if (!DRY) { await backup(e.path, t); await V.modify(f, u); } R.ok++; R.hunks += hs.length;
    if (++n % 20 === 0) await new Promise(r => setTimeout(r, 200));
  }
  let uf = 0, ul = 0; for (const k in app.metadataCache.unresolvedLinks) { const c = Object.values(app.metadataCache.unresolvedLinks[k]).reduce((a, b) => a + b, 0); if (c) { uf++; ul += c; } }
  await ad.write(`.work/out/${TAG}${DRY ? '-dry' : ''}.json`, JSON.stringify(R, null, 1));
  return `${TAG}${DRY ? ' (dry run)' : ''}: ${R.ok} notes ${DRY ? 'would change' : 'changed'} (${R.hunks} lines), ${R.already} already done, refused ${R.refused.length}${R.refused.length ? ': ' + R.refused.slice(0, 4).join(' | ') : ''}; unresolved ${uf} files / ${ul} links`;
})()
