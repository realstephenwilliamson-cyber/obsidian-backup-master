(async () => {
  // zfolio-retarget (28 Oct 2026, item 5): move chosen links to a Zohar folio side shared by two parashah notes from one holder
  // to the other. Data: [{path, line, col, original, block, from, to}] (from/to = note basenames). Only the note name inside the
  // link changes; block id and label stay. Each link is found in Obsidian's link cache by line and column and checked against
  // the text (same original, resolving to `from`, block present in `to`) before any change. Backups first. Then a check:
  // each changed note differs from its backup only by the moved names; every #^ link in it resolves; divine-name count unchanged.
  const DRY = window.DRY !== false, V = app.vault, mc = app.metadataCache, ad = V.adapter;
  const DATA = '__DATA__', BK = '__BACKUP__', TAG = '__TAG__';
  const items = JSON.parse(await ad.read(DATA));
  const byName = n => V.getMarkdownFiles().find(f => f.basename === n);
  const mk = async d => { let p = ''; for (const s of d.split('/')) { p = p ? p + '/' + s : s; if (!(await ad.exists(p))) await ad.mkdir(p); } };
  const R = { items: items.length, moved: 0, notes: 0, refused: [], perPair: {} };
  const byPath = {}; for (const it of items) (byPath[it.path] = byPath[it.path] || []).push(it);
  const changed = [];
  for (const [path, its] of Object.entries(byPath)) {
    const f = V.getAbstractFileByPath(path); if (!f) { R.refused.push(path + ': note missing'); continue; }
    const c = mc.getFileCache(f) || {}; const ls = [...(c.links || []), ...(c.embeds || [])];
    const text = await V.read(f); let u = text; const ops = [];
    for (const it of its) {
      const l = ls.find(x => x.position.start.line + 1 === it.line && x.position.start.col === it.col);
      const from = byName(it.from), to = byName(it.to);
      const why = !l ? 'no link at line/col' : l.original !== it.original ? 'original differs' : !from || !to ? 'note missing'
        : mc.getFirstLinkpathDest(l.link.split('#')[0], path) !== from ? 'does not resolve to from' : l.link.split('#')[1] !== '^' + it.block ? 'block differs'
        : !((mc.getFileCache(to) || {}).blocks || {})[it.block] ? 'block absent in to' : text.slice(l.position.start.offset, l.position.end.offset) !== it.original ? 'text differs' : '';
      if (why) { R.refused.push(`${path} ${it.line}: ${why}`); continue; }
      const linkpath = l.link.split('#')[0]; const nw = it.original.replace('[[' + linkpath + '#', '[[' + it.to + '#');
      if (nw === it.original) { R.refused.push(`${path} ${it.line}: no change made`); continue; }
      ops.push({ s: l.position.start.offset, e: l.position.end.offset, nw, it });
    }
    if (!ops.length) continue;
    for (const o of ops.sort((a, b) => b.s - a.s)) u = u.slice(0, o.s) + o.nw + u.slice(o.e);
    R.moved += ops.length; R.notes++; ops.forEach(o => { const k = o.it.block + ': ' + o.it.from.slice(6, 10) + ' -> ' + o.it.to.slice(6, 10); R.perPair[k] = (R.perPair[k] || 0) + 1; });
    changed.push({ f, text, u, ops });
    if (!DRY) { const bp = BK + path; await mk(bp.slice(0, bp.lastIndexOf('/'))); if (!(await ad.exists(bp))) await ad.write(bp, text); await V.process(f, t => { if (t !== text) throw new Error('changed under us: ' + path); return u; }); }
  }
  // check
  if (!DRY) await new Promise(r => setTimeout(r, 15000));
  const dn = s => (s.match(/[י][ְ-ׇ]*[ה][ְ-ׇ]*[ו][ְ-ׇ]*[ה]|\bY[Hh][VWvw][Hh]\b|\bJ[Ee][Hh][Oo][Vv][Aa][Hh]\b|\bY[Aa][Hh][Ww][Ee][Hh]\b/g) || []).length;
  const C = { notes: 0, onlyNames: 0, bad: [], dnSame: 0, dnDiff: [], unresolvedSub: 0 };
  for (const ch of changed) {
    const cur = DRY ? ch.u : await V.read(ch.f); C.notes++;
    let back = cur, d = 0; const asc = [...ch.ops].sort((a, b) => a.s - b.s), pos = asc.map(o => { const s = o.s + d; d += o.nw.length - (o.e - o.s); return s; });
    for (let i = asc.length - 1; i >= 0; i--) { const o = asc[i]; if (back.slice(pos[i], pos[i] + o.nw.length) !== o.nw) { back = null; break; } back = back.slice(0, pos[i]) + o.it.original + back.slice(pos[i] + o.nw.length); }
    if (back === ch.text) C.onlyNames++; else C.bad.push(ch.f.path);
    if (dn(cur) === dn(ch.text)) C.dnSame++; else C.dnDiff.push(ch.f.path);
    if (!DRY) for (const l of [...((mc.getFileCache(ch.f) || {}).links || []), ...((mc.getFileCache(ch.f) || {}).embeds || [])]) {
      const [p, sub] = l.link.split('#'); if (!sub || !sub.startsWith('^')) continue;
      const t = p ? mc.getFirstLinkpathDest(p, ch.f.path) : ch.f; if (!t || !((mc.getFileCache(t) || {}).blocks || {})[sub.slice(1)]) C.unresolvedSub++;
    }
  }
  let n = 0, k = 0; for (const o of Object.values(mc.unresolvedLinks)) { const c = Object.values(o).reduce((a, b) => a + b, 0); if (c) { n++; k += c; } }
  await ad.write(`.work/out/${TAG}${DRY ? '-dry' : ''}.json`, JSON.stringify({ R, C }, null, 1));
  return `${TAG}${DRY ? ' (dry run)' : ''}: ${DRY ? 'would move' : 'moved'} ${R.moved} of ${R.items} links in ${R.notes} notes; refused ${R.refused.length}; check: ${C.onlyNames}/${C.notes} differ only by the names, divine name same in ${C.dnSame}/${C.notes}${DRY ? '' : `, #^ links not resolving ${C.unresolvedSub}`}; unresolved ${n}/${k}`;
})()
