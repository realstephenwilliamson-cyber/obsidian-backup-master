// APPLY  (without this first line the job is a dry run: it checks and counts, and writes nothing)
(async () => {
  // The English Viveka: a patch to the library copy of Dyczkowski's Tantraloka and the verse notes' [!viveka] boxes (22 Oct 2026).
  // lib-patch.json: per note the length and FNV-1a hash of the text the patch was made from, the edits, and the length and hash
  // after; a note is changed only if it is exactly that text, and the result is checked. callouts.json: per verse note the old box
  // and the new one (old null: add the box under "## Viveka"; new null: take the box out). Backups first. Used as pe53 (second
  // pass: 103 non-verse units folded back, the letter clean-up) and pe57 (third pass: verse headings moved to the verse block).
  const DRY = window.DRY !== false, TAG = 'viveka-patch', V = app.vault, ad = V.adapter, SRC = '.work/pe-viv3/', BK = '.work/backup-viveka3-2026-10-22/', BK1 = '.work/backup-viveka-2026-10-22/';
  const fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h >>> 0; };
  const backup = async (p, t) => { const bp = BK + p; const d = bp.slice(0, bp.lastIndexOf('/')); if (!(await ad.exists(d))) await ad.mkdir(d); if (!(await ad.exists(bp))) await ad.write(bp, t); };
  const patch = JSON.parse(await ad.read(SRC + 'lib-patch.json')), calls = JSON.parse(await ad.read(SRC + 'callouts.json'));
  const R = { lib: { ok: 0, already: 0, refused: [] }, hunks: 0, verse: { replaced: 0, added: 0, removed: 0, already: 0, refused: [] } };
  let n = 0;
  for (const e of patch) {
    const f = V.getAbstractFileByPath(e.path); if (!f) { R.lib.refused.push(e.path + ': missing'); continue; }
    let t = await V.read(f);
    if (t.length === e.len1 && fnv(t) === e.h1) { R.lib.already++; continue; }
    if (t.length !== e.len0 || fnv(t) !== e.h0) { R.lib.refused.push(e.path.split('/').pop() + `: not the expected text (length ${t.length}/${e.len0})`); continue; }
    const hs = e.hunks.slice().sort((a, b) => b[0] - a[0]);
    let u = t; for (const [s, d, ins] of hs) u = u.slice(0, s) + ins + u.slice(s + d);
    if (u.length !== e.len1 || fnv(u) !== e.h1) { R.lib.refused.push(e.path.split('/').pop() + ': result check failed'); continue; }
    if (!DRY) { await backup(e.path, t); await V.modify(f, u); } R.lib.ok++; R.hunks += hs.length;
    if (++n % 20 === 0) await new Promise(r => setTimeout(r, 300));
  }
  n = 0;
  for (const [p, c] of Object.entries(calls)) {
    const f = V.getAbstractFileByPath(p); if (!f) { R.verse.refused.push(p + ': missing'); continue; }
    const t = await V.read(f);
    let u = null;
    if (c.new === null) {
      const k = t.split(c.old).length - 1;
      if (k === 0) { R.verse.already++; continue; }
      if (k !== 1) { R.verse.refused.push(p.split('/').pop() + `: box found ${k} times`); continue; }
      u = t.includes(c.old + '\n\n') ? t.replace(c.old + '\n\n', () => '') : t.replace(c.old, () => '');
      // a "## Viveka" heading the first pass added at the end of a note that had none is taken out again
      if (/\n## Viveka\s*$/.test(u) && (await ad.exists(BK1 + p)) && !(await ad.read(BK1 + p)).includes('\n## Viveka')) u = u.replace(/\s*\n## Viveka\s*$/, '\n');
      R.verse.removed++;
    } else if (t.includes(c.new) && !(c.old && t.includes(c.old))) { R.verse.already++; continue; }
    else if (c.old) {
      const k = t.split(c.old).length - 1;
      if (k !== 1) { R.verse.refused.push(p.split('/').pop() + `: old box found ${k} times`); continue; }
      u = t.replace(c.old, () => c.new); R.verse.replaced++;
    } else {
      if (t.includes('> [!viveka]- Viveka in English')) { R.verse.refused.push(p.split('/').pop() + ': has another box'); continue; }
      const k = t.split('\n## Viveka\n').length - 1;
      if (k === 1) u = t.replace(/\n## Viveka\n\n?/, m => '\n## Viveka\n\n' + c.new + '\n\n');
      else if (k === 0) u = t.replace(/\s*$/, '') + '\n\n## Viveka\n\n' + c.new + '\n';
      else { R.verse.refused.push(p.split('/').pop() + ': two Viveka sections'); continue; }
      R.verse.added++;
    }
    if (!DRY) { await backup(p, t); await V.modify(f, u); }
    if (++n % 50 === 0) await new Promise(r => setTimeout(r, 300));
  }
  await ad.write(`.work/out/${TAG}.json`, JSON.stringify(R, null, 1));
  return `${TAG}${DRY ? ' (dry run)' : ''}: library notes ${R.lib.ok} changed (${R.hunks} edits), ${R.lib.already} already, refused ${R.lib.refused.length}${R.lib.refused.length ? ': ' + R.lib.refused.slice(0, 4).join(' | ') : ''}; verse notes: replaced ${R.verse.replaced}, added ${R.verse.added}, removed ${R.verse.removed}, already ${R.verse.already}, refused ${R.verse.refused.length}${R.verse.refused.length ? ': ' + R.verse.refused.slice(0, 4).join(' | ') : ''}`;
})()
