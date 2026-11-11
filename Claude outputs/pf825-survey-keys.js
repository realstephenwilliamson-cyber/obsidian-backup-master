(async () => {
  const JOB = 'pf825-survey-keys', ad = app.vault.adapter, D = { files: {} };
  const all = app.vault.getFiles();
  D.keys = all.filter(f => /^CIS - Answers|^Chapter_\d|Genocide|Normative|Limiting Leviathan/i.test(f.name)).map(f => f.path);
  for (const f of all.filter(f => /^CIS - Answers/.test(f.name) && f.extension === 'md')) D.files[f.path] = (await app.vault.read(f)).slice(0, 3000);
  D.catMay = all.filter(f => /^Catalog\//.test(f.path) && /May|Genocide/.test(f.name)).map(f => f.path);
  await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1));
  return JOB + ': ' + D.keys.length;
})()
