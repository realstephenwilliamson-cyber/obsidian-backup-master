(async () => {
  // The English Viveka (22 Oct 2026, Stephen's option b): headings in the library copy of Dyczkowski's Tantraloka at each unit
  // ("### TĀ 1.1" before the verse, "#### Viveka on 1.1" before the commentary), and in each verse note, under "## Viveka", a folded
  // [!viveka] callout that embeds those sections. Nothing in the text is changed. Dry run checks every anchor; apply backs up first.
  const DRY = __DRY__, TAG = '__TAG__';
  const V = app.vault, ad = V.adapter, SRC = '.work/pe-viv/', BK = '.work/backup-viveka-2026-10-22/';
  const lib = JSON.parse(await ad.read(SRC + 'lib-inserts.json')), calls = JSON.parse(await ad.read(SRC + 'verse-callouts.json'));
  const R = { lib_ok: 0, lib_bad: [], headings: 0, verse: { once: 0, none: 0, many: 0, already: 0, missing: 0 }, verse_written: 0 };
  const backup = async (p, t) => { const bp = BK + p; const d = bp.slice(0, bp.lastIndexOf('/')); if (!(await ad.exists(d))) await ad.mkdir(d); if (!(await ad.exists(bp))) await ad.write(bp, t); };
  for (const e of lib) {
    const f = V.getAbstractFileByPath(e.path); if (!f) { R.lib_bad.push(e.path + ': missing'); continue; }
    let t = await V.read(f);
    if (t.length !== e.len) { R.lib_bad.push(e.path + `: length ${t.length} ≠ ${e.len}`); continue; }
    const badAt = e.ins.find(([o, h, pre]) => t.substr(o, pre.length) !== pre || t.substr(o - 2, 2) !== '\n\n');
    if (badAt) { R.lib_bad.push(e.path + ': anchor ' + badAt[0]); continue; }
    R.lib_ok++; R.headings += e.ins.length;
    if (!DRY) {
      await backup(e.path, t);
      for (let i = e.ins.length - 1; i >= 0; i--) { const [o, h] = e.ins[i]; t = t.slice(0, o) + h + '\n\n' + t.slice(o); }
      await V.modify(f, t);
      if (R.lib_ok % 20 === 0) await new Promise(r => setTimeout(r, 300));
    }
  }
  let n = 0;
  for (const [p, c] of Object.entries(calls)) {
    const f = V.getAbstractFileByPath(p); if (!f) { R.verse.missing++; continue; }
    const t = await V.read(f);
    if (t.includes('> [!viveka]- Viveka in English')) { R.verse.already++; continue; }
    const k = t.split('\n## Viveka\n').length - 1;
    let u;
    if (k === 1) { R.verse.once++; u = t.replace(/\n## Viveka\n\n?/, m => '\n## Viveka\n\n' + c + '\n\n'); }
    else if (k === 0) { R.verse.none++; u = t.replace(/\s*$/, '') + '\n\n## Viveka\n\n' + c + '\n'; }
    else { R.verse.many++; continue; }
    if (!DRY) { await backup(p, t); await V.modify(f, u); R.verse_written++; if (++n % 200 === 0) await new Promise(r => setTimeout(r, 400)); }
  }
  await ad.write(`.work/out/${TAG}.json`, JSON.stringify(R, null, 1));
  return `${TAG}: library notes ${R.lib_ok}/${lib.length} (${R.headings} headings), refused ${R.lib_bad.length}${R.lib_bad.length ? ': ' + R.lib_bad.slice(0, 5).join(' | ') : ''}; verse notes ${JSON.stringify(R.verse)}, written ${R.verse_written}`;
})()
