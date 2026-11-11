(async () => {
  // pf821-survey-other (10 Nov 2026): read-only. Where is the subject "Other" named; who links to the four Bases; the Other notes' files.
  const JOB = 'pf821-survey-other', ad = app.vault.adapter, D = { when: new Date().toISOString() };
  const files = app.vault.getFiles().filter(f => /^(md|base|js|json)$/.test(f.extension) && !/^(\.work|\.trash|\.git)\//.test(f.path));
  const pats = [/Catalog\/Other/, /Library\/Other/, /Biblical-Studies\s*\|\s*Other/, /\bOther\b.{0,40}(Trika|Judaica|Philosophy)|(Trika|Judaica|Philosophy).{0,40}\bOther\b/, /Needs review|Physical Library|Shelf check|To delete/];
  D.hits = [];
  for (const f of files) {
    let t; try { t = await app.vault.cachedRead(f); } catch (e) { continue; }
    const lines = t.split(/\r?\n/);
    lines.forEach((l, i) => { if (pats.some(p => p.test(l))) D.hits.push(f.path + ':' + (i + 1) + ': ' + l.slice(0, 220)); });
  }
  D.hits = D.hits.filter(h => !/^(Texts|Study\/Sanskrit|Library)\//.test(h));
  // backlinks to the four bases
  const names = ['Needs review.base', 'Physical Library.base', 'Shelf check.base', 'To delete.base'];
  D.backlinks = {};
  for (const n of names) {
    const tf = app.vault.getAbstractFileByPath('Catalog/' + n); D.backlinks[n] = [];
    for (const [src, m] of Object.entries(app.metadataCache.resolvedLinks)) if (m['Catalog/' + n]) D.backlinks[n].push(src);
  }
  // Other notes
  D.other = [];
  for (const f of app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Catalog/Other/') && f.basename !== 'Other')) {
    const fm = app.metadataCache.getFileCache(f)?.frontmatter || {};
    D.other.push({ n: f.basename, subject: fm.subject, status: fm.status, files: fm.files, print: fm.print });
  }
  D.libOther = (await ad.list('Library/Other')).folders.concat((await ad.list('Library/Other')).files);
  const tf = app.vault.getAbstractFileByPath('Catalog/Philosophy'); D.philFolder = !!tf;
  await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1));
  return `${JOB}: ${D.hits.length} hits, ${D.other.length} other notes`;
})()
