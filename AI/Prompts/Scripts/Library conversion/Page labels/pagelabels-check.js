(async () => {
  // pf431 (28 Oct 2026, item 6): read-only check after pf429/pf430. For every note backed up in .work/backup-pagelabels-2026-10-28/
  // (both specs): frontmatter readable, page_range as written, every *[...]* ^pgK marker line still has its block registered,
  // divine-name count equal to the backup's, and the note differs from its backup only on the edited lines (line count unchanged
  // except Farrer's index, which loses one line break). Unresolved links after.
  await new Promise(r => setTimeout(r, 15000));
  const ad = app.vault.adapter, mc = app.metadataCache, V = app.vault, BK = '.work/backup-pagelabels-2026-10-28';
  const list = async d => { const o = await ad.list(d); let fs = [...o.files]; for (const f of o.folders) fs = fs.concat(await list(f)); return fs; };
  const files = (await list(BK)).filter(p => p.endsWith('.md'));
  const dn = s => (s.match(/[י][ְ-ׇ]*[ה][ְ-ׇ]*[ו][ְ-ׇ]*[ה]|\bY[Hh][VWvw][Hh]\b|\bJ[Ee][Hh][Oo][Vv][Aa][Hh]\b|\bY[Aa][Hh][Ww][Ee][Hh]\b/g) || []).length;
  const R = { backups: files.length, notes: 0, fmBad: [], blocksMissing: [], dnDiff: [], lineDiff: [], changedLines: 0 };
  const seen = new Set();
  for (const b of files) {
    const path = b.replace(/^\.work\/backup-pagelabels-2026-10-28\/(noticed\/)?/, ''); if (seen.has(path + '|' + b)) continue; seen.add(path + '|' + b);
    const f = V.getAbstractFileByPath(path); if (!f) { R.fmBad.push('missing ' + path); continue; }
    const cur = await V.read(f), old = await ad.read(b); R.notes++;
    const fc = mc.getFileCache(f) || {}; if (cur.startsWith('---') && !fc.frontmatter) R.fmBad.push(path);
    const blocks = fc.blocks || {}; for (const m of cur.matchAll(/^\*\[(?:p\.|PDF) [^\]]+\]\* \^(pg\d+)\s*$/gm)) if (!blocks[m[1]]) { R.blocksMissing.push(path + ' ' + m[1]); break; }
    if (dn(cur) !== dn(old)) R.dnDiff.push(path);
    const a = old.split('\n'), c = cur.split('\n');
    if (a.length !== c.length && !path.includes('(Farrer)')) R.lineDiff.push(path); else if (a.length === c.length) for (let i = 0; i < a.length; i++) if (a[i] !== c[i]) R.changedLines++;
  }
  let n = 0, k = 0; for (const o of Object.values(mc.unresolvedLinks)) { const s = Object.values(o).reduce((x, y) => x + y, 0); if (s) { n++; k += s; } }
  await ad.write('.work/out/pf431-pagelabels-check.json', JSON.stringify(R, null, 1));
  return `pf431-pagelabels-check: ${R.notes} notes (${R.backups} backups); frontmatter unreadable ${R.fmBad.length}; marker blocks missing ${R.blocksMissing.length}; divine name differs ${R.dnDiff.length}; line count differs ${R.lineDiff.length}; changed lines ${R.changedLines}; unresolved ${n}/${k}`;
})()
