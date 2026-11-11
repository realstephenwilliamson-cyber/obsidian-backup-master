(async () => {
  // pf831-survey-home (10 Nov 2026): read-only. Every mention of "Home (mobile)" and "Phone page" in the vault, and the quick-capture view's size.
  const JOB = 'pf831-survey-home', ad = app.vault.adapter, D = { hits: [] };
  for (const f of app.vault.getFiles().filter(f => /^(md|js|json|base|css)$/.test(f.extension) && !/^(\.work|\.trash|\.git)\//.test(f.path))) {
    let t; try { t = await app.vault.cachedRead(f); } catch (e) { continue; }
    t.split(/\r?\n/).forEach((l, i) => { if (/Home \(mobile\)|Phone page|home-mobile/i.test(l)) D.hits.push(f.path + ':' + (i + 1) + ': ' + l.slice(0, 260)); });
  }
  D.back = Object.entries(app.metadataCache.resolvedLinks).filter(([s, m]) => m['Home (mobile).md']).map(([s]) => s);
  try { const g = JSON.parse(await ad.read('.obsidian/plugins/homepage/data.json')); D.homepage = { value: g.value, kind: g.kind, openOnStartup: g.openOnStartup, mobile: g.mobile, hasMobile: JSON.stringify(g).slice(0, 600) }; } catch (e) { D.homepage = 'none: ' + e.message; }
  try { D.appJson = (await ad.read('.obsidian/app.json')).slice(0, 400); } catch (e) {}
  await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1));
  return JOB + ': ' + D.hits.length + ' hits';
})()
