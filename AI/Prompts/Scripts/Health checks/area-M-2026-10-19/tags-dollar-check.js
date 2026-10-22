(async () => {
  // J2-11 check (read-only): in the 24,156 notes of the tags record, does any frontmatter contain a "$" (which String.replace could have expanded)?
  const ad = app.vault.adapter; const rec = JSON.parse(await ad.read('.work/backup-tags-2026-10-19/removed-tags.json'));
  const paths = Object.keys(rec.removed || rec.notes || {}); const hits = []; let n = 0, crlf = 0, noFm = 0;
  for (const p of paths) {
    const f = app.vault.getAbstractFileByPath(p); if (!f) { hits.push([p, 'MISSING']); continue; }
    const t = await app.vault.cachedRead(f); n++;
    const m = t.match(/^---\r?\n([\s\S]*?)\r?\n---/); if (!m) { noFm++; continue; }
    if (/\r\n/.test(t)) crlf++;
    if (m[1].includes('$')) hits.push([p, m[1].split('\n').filter(l => l.includes('$')).slice(0, 3)]);
  }
  await ad.write('.work/out/tags-dollar.json', JSON.stringify({ when: new Date().toISOString(), notes: n, noFm, crlf, hits }, null, 1));
  return `tags record ${paths.length} notes, read ${n}, no frontmatter now ${noFm}, CRLF files ${crlf}, frontmatter containing "$": ${hits.length}${hits.length ? ' e.g. ' + JSON.stringify(hits.slice(0, 5)).slice(0, 600) : ''}`;
})()
