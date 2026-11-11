// APPLY
(async () => {
  // pf832-home-one-page (10 Nov 2026): the four capture buttons onto Home, Home (mobile) trashed, references fixed. Stephen approved the Home.md diff.
  const JOB = 'pf832-home-one-page', ad = app.vault.adapter, DRY = window.DRY !== false;
  const D = { when: new Date().toISOString(), dry: DRY, log: [], errors: [] }, L = s => D.log.push(s), E = s => D.errors.push(s);
  const get = p => app.vault.getAbstractFileByPath(p);
  const unres = () => Object.values(app.metadataCache.unresolvedLinks).reduce((a, m) => a + Object.keys(m).length, 0);
  const before = unres();
  const edit = async (p, fn) => {
    const f = get(p); if (!f) { E('missing ' + p); return; }
    const t = await app.vault.read(f); const r = fn(t);
    if (r === null || r === t) { E('no change ' + p); return; }
    L('edit ' + p); if (!DRY) await app.vault.modify(f, r);
  };
  const rep = (t, a, b, n = 1) => { const parts = t.split(a); if (parts.length - 1 !== n) { E('expected ' + n + ' of "' + a.slice(0, 50) + '" got ' + (parts.length - 1)); return null; } return parts.join(b); };
  const chain = (t, pairs) => { for (const [a, b, n] of pairs) { if (t === null) return null; t = rep(t, a, b, n || 1); } return t; };
  const bt = '`' + '``';
  // Home.md
  await edit('Home.md', t => chain(t, [
    ['## Tasks\n', '## Capture\n\n' + bt + 'dataviewjs\nawait dv.view("Templates/Views/quick-capture")\n' + bt + '\n\n## Tasks\n'],
    [' · [[Home (mobile)|Phone page]]', '']]));
  // Vault Guide
  await edit('Vault Guide.md', t => {
    t = chain(t, [
      ['`Home.md`, `Home (mobile).md`, `Vault Guide.md`', '`Home.md`, `Vault Guide.md`'],
      ['The dashboard, its phone version and this guide', 'The dashboard (the same on every device) and this guide'],
      ['on Home (mobile). The folder', 'on Home. The folder'],
      ['Open [[Home (mobile)]] (on the phone it is the start page; on the laptop it is linked from Home\'s *Go to* row), then *Add a book you have on paper (no PDF)*.', 'Open [[Home]] and press *Add a book you have on paper (no PDF)* in the *Capture* section.'],
      ['so open [[Home (mobile)]] once and leave it in a tab', 'and it is not needed (the same Home serves every device), so open [[Home]] once and leave it in a tab'],
      ['Open Home, or Home (mobile) on the phone:', 'Open Home (on the phone too):']]);
    if (t === null) return null;
    const m = t.match(/^- \*\*On the phone:\*\* \[\[Home \(mobile\)\]\].*$/m);
    if (!m) { E('guide phone bullet not found'); return null; }
    const nb = '- **On the phone:** the same [[Home]] as on the laptop (since 10 Nov 2026 there is no separate phone page). Its *Capture* section has four buttons: *New note*, *New handwritten note* (a note in `Notes/` opened with an Ink writing section; since 21 Oct 2026), *Photograph marked pages*, which files a photo under the date in that book\'s note in `Notes/Marked pages/`, and *Add a book you have on paper*, which catalogs a book that has no PDF (see Adding things). The Homepage plugin is off (it slowed start-up, 16 Oct 2026), so keep *Home* open in a tab: Obsidian reopens the tabs it had when it closed. For the other settings a new phone or tablet needs, see [[#Setting up a new device]].';
    return t.replace(m[0], () => nb);
  });
  await edit('Catalog/Philosophy/Ruiz - Structural Violence.md', t => rep(t, '[[Home (mobile)]]', '[[Home]]'));
  await edit('Templates/Views/today-study/view.js', t => rep(t, 'for Home and Home (mobile)', 'for Home'));
  await edit('Templates/Views/today-items/view.js', t => rep(t, '(Home, Home (mobile))', '(Home)'));
  await edit('Templates/Views/quick-capture/view.js', t => rep(t, '(Home (mobile), and Home)', '(on Home)'));
  await edit('Templates/Catalog Item.md', t => rep(t, 'on Home (mobile)', 'on Home'));
  await edit('AI/Prompts/Scripts/Health checks/render-check.js', t => rep(t, "'Home (mobile)', ", ''));
  await edit('AI/Prompts/Scripts/Health checks/health-report.js', t => chain(t, [["'Home (mobile).md', ", '', 2]]));
  await edit('AI/Prompts/Complete vault audit.md', t => chain(t, [['Home.md, Home (mobile).md,', 'Home.md,'], ['Home, Home (mobile),', 'Home,']]));
  await edit('Notes/Discuss next session.md', t => { const m = t.match(/^- \*\*One Home for every device\*\*.*\n/m); if (!m) { E('discuss bullet missing'); return null; } return t.replace(m[0], ''); });
  // AI log
  await edit('AI/AI log.md', t => {
    t = rep(t, '**Next free job number: pf831.**', '**Next free job number: pf833.**'); if (t === null) return null;
    const h = '## 10 Nov 2026 (15:20–15:45)';
    const entry = '## 10 Nov 2026 (15:49–): one Home for every device (Sonnet lead in the cloud)\n\n- **Stephen:** move the four mobile buttons onto the normal Home and delete *Home (mobile)*; the Homepage plugin proved unnecessary and slow, and the regular Home renders fine on every device. He approved the diff.\n- **Done (pf831 survey, pf832):** *Home.md* has a *Capture* section (the `quick-capture` view: *New note*, *New handwritten note*, *Photograph marked pages*, *Add a book you have on paper*) above *Tasks*, and no "Phone page" link; *Home (mobile).md* is in `.trash`. References reworded in [[Vault Guide]] (six places), the Ruiz catalog note, the comments of three views and *Catalog Item*, the two health-check scripts and *Complete vault audit*; the "One Home for every device" item is out of *Discuss next session*. Older reports, archive notes and the dated area-M scripts still name *Home (mobile)* as history. **Next free job number pf833.**\n\n';
    return rep(t, h, entry + h);
  });
  // trash
  const hm = get('Home (mobile).md');
  if (!hm) E('Home (mobile) missing'); else { L('trash Home (mobile).md'); if (!DRY) await app.vault.trash(hm, false); }
  await new Promise(r => setTimeout(r, DRY ? 0 : 3000));
  D.unresolvedBefore = before; D.unresolvedAfter = unres();
  await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1));
  return JOB + ': ' + (DRY ? 'dry' : 'applied') + ', ' + D.errors.length + ' errors ' + D.errors.join('|') + ' unresolved ' + before + '->' + D.unresolvedAfter;
})()
