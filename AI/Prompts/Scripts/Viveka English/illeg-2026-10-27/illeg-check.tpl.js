// Read-only check after the [illegible] fills (27-28 Oct 2026): every patched note is the intended text; its divine-name count,
// footnote calls and definitions, ^pg blocks and headings equal the backup's; every Viveka embed resolves; unresolved links.
(async () => {
  await new Promise(r => setTimeout(r, 20000));
  const V = app.vault, ad = V.adapter, mc = app.metadataCache, SRC = '__SRC__', BK = '__BK__', TAG = '__TAG__';
  const fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h >>> 0; };
  const DN = new RegExp('[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה', 'g');
  const cnt = (t, re) => (t.match(re) || []).length;
  const patch = JSON.parse(await ad.read(SRC + 'lib-patch.json'));
  const R = { notes: 0, intended: 0, notIntended: [], dn: [0, 0], calls: [0, 0], defs: [0, 0], pg: [0, 0], heads: [0, 0], illeg: [0, 0], cacheFootnotes: 0, embeds: 0, badEmbeds: [], unresolved: '' };
  for (const e of patch) {
    const f = V.getAbstractFileByPath(e.path); R.notes++;
    const t = await V.read(f); if (t.length === e.len1 && fnv(t) === e.h1) R.intended++; else R.notIntended.push(e.path.split('/').pop());
    const bp = BK + e.path; if (!(await ad.exists(bp))) continue; const b = await ad.read(bp);
    R.dn[0] += cnt(b, DN); R.dn[1] += cnt(t, DN);
    R.calls[0] += cnt(b, /\[\^[^\]]+\](?!:)/g); R.calls[1] += cnt(t, /\[\^[^\]]+\](?!:)/g);
    R.defs[0] += cnt(b, /^\[\^[^\]]+\]:/gm); R.defs[1] += cnt(t, /^\[\^[^\]]+\]:/gm);
    R.pg[0] += cnt(b, /\^pg\d+/g); R.pg[1] += Object.keys((mc.getFileCache(f) || {}).blocks || {}).filter(k => /^pg\d+$/.test(k)).length;
    R.heads[0] += cnt(b, /^#{1,6} /gm); R.heads[1] += ((mc.getFileCache(f) || {}).headings || []).length;
    R.illeg[0] += cnt(b, /\\\[illegible\\\]/g); R.illeg[1] += cnt(t, /\\\[illegible\\\]/g);
    R.cacheFootnotes += ((mc.getFileCache(f) || {}).footnotes || []).length;
  }
  const norm = h => h.replace(/[#^|\[\]]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
  for (const f of V.getMarkdownFiles()) {
    if (!f.path.startsWith('Texts/Tantraloka/')) continue;
    const em = ((mc.getFileCache(f) || {}).embeds || []).filter(e => e.link.includes('Tantraloka Dyczkowski'));
    for (const e of em) { R.embeds++; const [p, h] = e.link.split('#'); const tg = mc.getFirstLinkpathDest(p, f.path);
      if (!tg || !((mc.getFileCache(tg) || {}).headings || []).some(x => norm(x.heading) === norm(h || ''))) R.badEmbeds.push(f.basename + ' → ' + e.link); }
  }
  let n = 0, k = 0; for (const o of Object.values(mc.unresolvedLinks)) { const c = Object.values(o).reduce((a, b) => a + b, 0); if (c) { n++; k += c; } } R.unresolved = `${n}/${k}`;
  await ad.write(`.work/out/${TAG}.json`, JSON.stringify(R, null, 1));
  return `${TAG}: ${R.intended}/${R.notes} notes as intended; divine name ${R.dn.join('→')}; calls ${R.calls.join('→')}; definitions ${R.defs.join('→')}; ^pg ${R.pg.join('→')} (cache); headings ${R.heads.join('→')}; [illegible] ${R.illeg.join('→')}; cache footnotes ${R.cacheFootnotes}; embeds ${R.embeds}, ${R.badEmbeds.length} broken; unresolved ${R.unresolved}`;
})()
