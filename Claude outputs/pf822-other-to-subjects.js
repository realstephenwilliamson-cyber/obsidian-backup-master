(async () => {
  // pf822-other-to-subjects (10 Nov 2026): the subject "Other" becomes "Religious-Studies"; the four works that are not about religion
  // (Homer, Borges, Chan, Russell; Stephen, 10 Nov 2026) and the AI Review file go to Philosophy. Moves and renames through Obsidian
  // (fileManager.renameFile), so links follow. Dry run lists what it would do; // APPLY does it. Writes .work/out/<job>.detail.json.
  const JOB = 'pf822-other-to-subjects', ad = app.vault.adapter, DRY = window.DRY !== false;
  const D = { when: new Date().toISOString(), dry: DRY, log: [], errors: [] };
  const L = s => D.log.push(s), E = s => D.errors.push(s);
  const get = p => app.vault.getAbstractFileByPath(p);
  const done = async () => { await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1)); return `${JOB}${DRY ? ' DRY' : ''}: ${D.log.length} steps, ${D.errors.length} errors${D.errors.length ? ': ' + D.errors.slice(0, 3).join(' | ').slice(0, 300) : ''}`; };
  const before = Object.entries(app.metadataCache.unresolvedLinks).map(([k, v]) => Object.keys(v).length).reduce((a, b) => a + b, 0);
  D.unresolvedBefore = before;
  const mv = async (from, to) => {
    const f = get(from);
    if (!f) { E('missing ' + from); return false; }
    if (get(to) || await ad.exists(to)) { E('target exists ' + to); return false; }
    L('move ' + from + ' -> ' + to);
    if (!DRY) await app.fileManager.renameFile(f, to);
    return true;
  };
  const subjRe = /^subject:\r?\n(?:  - .*\r?\n)+/m;
  const setSubject = async (path, list, mustHave) => {
    const f = DRY ? get(path) : get(path);
    if (!f) { E('no note ' + path); return; }
    const t = await app.vault.read(f), m = t.match(subjRe);
    if (!m || !m[0].includes(mustHave)) { E('subject block not as expected in ' + path); return; }
    L('subject ' + path + ': ' + m[0].replace(/\s+/g, ' ').trim() + ' -> ' + list.join(','));
    if (!DRY) await app.vault.process(f, s => s.replace(subjRe, 'subject:\n' + list.map(x => '  - ' + x).join('\n') + '\n'));
  };
  const rep = async (path, from, to, n) => {
    const f = get(path);
    if (!f) { E('no file ' + path); return; }
    const t = await app.vault.read(f);
    const cnt = typeof from === 'string' ? t.split(from).length - 1 : (t.match(from) || []).length;
    if (cnt !== n) { E(`${path}: expected ${n} of ${from}, found ${cnt}`); return; }
    L(`replace in ${path}: ${n}x ${from}`);
    if (!DRY) await app.vault.process(f, s => s.replace(from, to));
  };

  // A. four works and the AI Review file to Philosophy
  const four = [
    ['Homer - The Odyssey (Lattimore tr.)', ['Library/Other/Homer - The Odyssey of Homer (1965).pdf', 'Library/Other/The Odyssey of Homer (Homer)']],
    ['Borges - On Exactitude in Science', ['Library/Other/On Exactitude in Science.pdf', 'Library/Other/On Exactitude in Science (Borges).md']],
    ['Chan (ed.) - A Source Book in Chinese Philosophy', ['Library/Other/Wing-Tsit Chan - A Source Book in Chinese Philosophy (1969).pdf', 'Library/Other/A Source Book in Chinese Philosophy (Chan)']],
    ['Russell - A History of Western Philosophy', ['Library/Other/Bertrand Russell - A History of Western Philosophy-Touchstone (1967).pdf', 'Library/Other/A History of Western Philosophy (Russell)']],
  ];
  for (const [n, libs] of four) {
    const cat = `Catalog/Other/${n}.md`;
    if (!get(cat)) { E('no catalog note ' + n); continue; }
    for (const l of libs) await mv(l, 'Library/Philosophy/' + l.split('/').pop());
    await mv(cat, `Catalog/Philosophy/${n}.md`);
    await setSubject(DRY ? cat : `Catalog/Philosophy/${n}.md`, ['Philosophy'], 'Other');
  }
  for (const l of ['Library/Other/(67) AI Review - Academia.edu.pdf', 'Library/Other/AI Review of Virtual Identity Crisis.md']) await mv(l, 'Library/Philosophy/' + l.split('/').pop());

  // B. the rest: subject Religious-Studies, folders renamed, index note renamed and rewritten
  const rest = DRY ? app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Catalog/Other/') && f.basename !== 'Other').filter(f => !four.some(x => x[0] === f.basename)) : app.vault.getMarkdownFiles().filter(f => f.path.startsWith('Catalog/Other/') && f.basename !== 'Other');
  D.restCount = rest.length;
  for (const f of rest) await setSubject(f.path, ['Religious-Studies'], 'Other');
  if (D.errors.length) { L('STOPPED before folder renames: errors above'); return await done(); }
  await mv('Library/Other', 'Library/Religious-Studies');
  await mv('Catalog/Other', 'Catalog/Religious-Studies');
  await mv('Catalog/Religious-Studies/Other.md', 'Catalog/Religious-Studies/Religious-Studies.md');
  const idx = DRY ? 'Catalog/Other/Other.md' : 'Catalog/Religious-Studies/Religious-Studies.md';
  await rep(idx, 'subject.contains("Other")', 'subject.contains("Religious-Studies")', 1);
  await rep(idx, '# Other\n', '# Religious Studies\n', 1);
  await rep(idx, '    name: Other\n', '    name: Religious Studies\n', 1);

  // C. places that name the subject
  await rep('Templates/Views/quick-capture/view.js', '"Biblical-Studies", "Other"]', '"Biblical-Studies", "Religious-Studies"]', 1);
  await rep('Vault Guide.md', 'Judaica, Other, Philosophy, Sanskrit, Trika', 'Judaica, Philosophy, Religious-Studies, Sanskrit, Trika', 1);
  await rep('Vault Guide.md', '| Biblical-Studies | Other', '| Biblical-Studies | Religious-Studies', 1);
  await rep('AI/Prompts/Add scholar pages.md', 'Biblical-Studies, Philosophy, Other>', 'Biblical-Studies, Philosophy, Religious-Studies>', 1);
  await rep('AI/Prompts/Add new files from Downloads.md', 'Biblical-Studies | Other.', 'Biblical-Studies | Religious-Studies.', 1);
  await rep('AI/Prompts/Add new files from Downloads.md', '"Other" is for what fits none of these.', 'Religious-Studies is for general and comparative work on religion that fits none of these; what is not about religion goes to Philosophy.', 1);
  await rep('Catalog/Scholars/Timothy Knepper.md', 'subjects: [Philosophy, Other]', 'subjects: [Philosophy, Religious-Studies]', 1);
  await rep('Catalog/Scholars/J.N. Mohanty.md', 'subjects: [Philosophy, Other]', 'subjects: [Philosophy, Religious-Studies]', 1);
  await rep('Catalog/Scholars/Scholars.md', '· Philosophy, Other', '· Philosophy, Religious-Studies', 2);
  await rep('AI/Smart Connections exclusions.md', 'Library/Other/**', 'Library/Religious-Studies/**\nLibrary/Philosophy/The Odyssey of Homer (Homer)/**\nLibrary/Philosophy/On Exactitude in Science (Borges).md\nLibrary/Philosophy/A Source Book in Chinese Philosophy (Chan)/**\nLibrary/Philosophy/A History of Western Philosophy (Russell)/**\nLibrary/Philosophy/AI Review of Virtual Identity Crisis.md', 1);

  if (!DRY) { await new Promise(r => setTimeout(r, 3000)); D.unresolvedAfter = Object.entries(app.metadataCache.unresolvedLinks).map(([k, v]) => Object.keys(v).length).reduce((a, b) => a + b, 0); }
  return await done();
})()
