(async () => {
  // health-report.js — the vault's monthly check-up without an AI (21 Oct 2026, for the maintenance mode from November 2026).
  // Run: copy this file into .work/queue/ while the runner is on (the house-rules line starts the runner after an Obsidian restart).
  // It reads the vault, renders the dashboards in temporary tabs, and writes ONE new note, AI/Health reports/Health report <date>.md, plus the full
  // figures in .work/out/health-report-<date>.json. It changes nothing else. The note's frontmatter carries the numbers, and the next
  // run reads the latest earlier report to show what moved. Each section is guarded: if one check fails, the report says so and goes on.
  const t0 = Date.now();
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const ad = app.vault.adapter, MC = app.metadataCache;
  const today = moment().format('YYYY-MM-DD');
  const R = { date: today, numbers: {}, fine: [], attention: [], notes: [], errors: [] };
  const sec = async (name, fn) => { try { await fn(); } catch (e) { R.errors.push(name + ': ' + (e && e.message || e)); } };
  const mb = b => Math.round(b / 1048576);
  const files = app.vault.getFiles(), notes = app.vault.getMarkdownFiles();

  // the previous report
  let prev = null, prevDate = null;
  await sec('previous report', async () => {
    const reps = notes.filter(f => /^AI\/Health reports\/Health report \d{4}-\d{2}-\d{2}\.md$/.test(f.path) && !f.path.endsWith(today + '.md')).sort((a, b) => b.path.localeCompare(a.path));
    if (reps.length) { prev = (MC.getFileCache(reps[0]) || {}).frontmatter || null; prevDate = reps[0].basename.slice(-10); }
  });
  const since = prev && prev.date ? moment(prev.date, 'YYYY-MM-DD').valueOf() : moment().subtract(31, 'days').valueOf();

  // 1. counts and links
  await sec('counts', async () => {
    R.numbers.files = files.length; R.numbers.notes = notes.length;
    const folders = new Set(files.map(f => f.parent && f.parent.path)); R.numbers.folders = folders.size;
    let uf = 0, ul = 0; const unres = [];
    for (const [p, m] of Object.entries(MC.unresolvedLinks)) { const ks = Object.keys(m); if (ks.length) { uf++; ul += ks.length; unres.push([p, ks]); } }
    R.numbers.unresolved_links = ul; R.numbers.unresolved_notes = uf;
    const journalOnly = unres.every(([p, ks]) => p.startsWith('Journal/') || p.startsWith('Templates/') || p === 'Projects/Projects.md');
    const list = unres.filter(([p]) => !p.startsWith('Journal/') && !p.startsWith('Templates/')).map(([p, ks]) => `${p} → ${ks.slice(0, 3).join(', ')}${ks.length > 3 ? ' …' : ''}`);
    if (journalOnly) R.fine.push(`Unresolved links: ${ul} in ${uf} notes, all of them day links to days without a note, template placeholders or the known Projects line.`);
    else R.attention.push({ what: `Unresolved links outside the Journal and the templates: ${list.length} notes`, paths: list.slice(0, 15), run: 'look at them yourself; for many at once, *Map new connections* or a short AI session' });
  });

  // 2. the catalog
  await sec('catalog', async () => {
    const lib = files.filter(f => f.path.startsWith('Library/') && /^(pdf|djvu)$/i.test(f.extension));
    const linkedBy = {}; let badLinks = [], review = 0, scan = 0, print = 0, catalogNotes = 0;
    for (const n of notes) {
      if (!n.path.startsWith('Catalog/')) continue;
      const fm = (MC.getFileCache(n) || {}).frontmatter; if (!fm || !('files' in fm)) continue;
      catalogNotes++;
      if (fm.status === 'review') review++; if (fm.text === 'scan') scan++; if (fm.text === 'print') print++;
      for (const raw of [].concat(fm.files || [])) {
        const link = String(raw).replace(/^\[\[|\]\]$/g, '').split('|')[0].split('#')[0];
        const dest = MC.getFirstLinkpathDest(link, n.path);
        if (!dest) badLinks.push(`${n.path}: ${link}`); else (linkedBy[dest.path] = linkedBy[dest.path] || []).push(n.path);
      }
    }
    const unlinked = lib.filter(f => !linkedBy[f.path]).map(f => f.path);
    const twice = Object.entries(linkedBy).filter(([p, a]) => a.length > 1 && /\.(pdf|djvu)$/i.test(p)).map(([p, a]) => `${p} ← ${a.join(' + ')}`);
    Object.assign(R.numbers, { catalog_notes: catalogNotes, library_files: lib.length, library_files_unlinked: unlinked.length, catalog_bad_links: badLinks.length, catalog_review: review, catalog_scan: scan, catalog_print: print });
    if (!unlinked.length && !badLinks.length && !twice.length) R.fine.push(`Catalog: ${catalogNotes} notes; every one of the ${lib.length} library PDFs and DjVus has its catalog note and every files: link resolves.`);
    if (unlinked.length) R.attention.push({ what: `Library files without a catalog note: ${unlinked.length}`, paths: unlinked.slice(0, 15), run: 'Add new files from Downloads (for a file you meant to file) or Redundancy sweep' });
    if (badLinks.length) R.attention.push({ what: `Catalog files: links that do not resolve: ${badLinks.length}`, paths: badLinks.slice(0, 15), run: 'fix by hand in the catalog note, or Check catalog notes against their files' });
    if (twice.length) R.attention.push({ what: `Library files listed by two catalog notes: ${twice.length}`, paths: twice.slice(0, 10), run: 'Redundancy sweep' });
    if (review) R.notes.push(`${review} catalog notes are in status: review (Catalog.base → Review); *Check catalog notes against their files* settles them.`);
    if (scan) R.notes.push(`${scan} catalog notes are text: scan (*Scans without text*); *Make scans searchable (OCR)* when you want their PDFs searchable.`);
  });

  // 3. names, empties, strays
  await sec('names', async () => {
    // Stephen's originals keep their own names (Projects/_Originals/, 21 Oct 2026); the Greek lexicon and the Ink attachments are the Guide's exceptions
    const named = files.filter(f => !f.path.startsWith('Projects/_Originals/') && !f.path.startsWith('Library/Lexicons/') && !f.path.startsWith('Study/Sanskrit/Flashcards/Attachments/'));
    const nonAscii = named.filter(f => /[^\x00-\x7F]/.test(f.path)).map(f => f.path);
    const badChars = named.filter(f => /[\[\]#^|:*?"<>\\]/.test(f.name) || / \(\d\)\./.test(f.name) || / copy\./i.test(f.name) || /  /.test(f.name)).map(f => f.path);
    const empties = notes.filter(f => f.stat.size < 12 && !f.path.startsWith('Journal/')).map(f => f.path);
    const top = files.filter(f => !f.path.includes('/') && !['Home.md', 'Home (mobile).md', 'Welcome to the vault.md', 'Vault Guide.md', 'Plugins.md'].includes(f.path)).map(f => f.path);
    const strayJs = files.filter(f => f.extension === 'js' && !f.path.startsWith('Templates/Views/') && !f.path.startsWith('AI/Prompts/Scripts/') && !f.path.startsWith('AI/Archive/')).map(f => f.path);
    Object.assign(R.numbers, { names_non_ascii: nonAscii.length, names_bad: badChars.length, empty_notes: empties.length, top_level_strays: top.length, stray_scripts: strayJs.length });
    if (!nonAscii.length && !badChars.length) R.fine.push('File names: all plain ASCII outside the Greek lexicon and Stephen\'s originals, no forbidden characters, no " (1)" or " copy" endings.');
    if (nonAscii.length) R.attention.push({ what: `Names with non-ASCII characters: ${nonAscii.length}`, paths: nonAscii.slice(0, 10), run: 'rename through Obsidian (diacritics belong in the title property)' });
    if (badChars.length) R.attention.push({ what: `Names with forbidden characters or " (1)"/" copy" endings: ${badChars.length}`, paths: badChars.slice(0, 10), run: 'rename through Obsidian' });
    if (empties.length) R.attention.push({ what: `Empty notes outside the Journal: ${empties.length}`, paths: empties.slice(0, 10), run: 'open each: fill it, or delete it through Obsidian' });
    if (top.length) R.attention.push({ what: `Files at the vault's top level that are not the five known notes: ${top.length}`, paths: top, run: 'move them into a folder through Obsidian' });
    if (strayJs.length) R.attention.push({ what: `Scripts outside Templates/Views and AI/Prompts/Scripts: ${strayJs.length}`, paths: strayJs.slice(0, 10), run: 'an AI left them; trash through Obsidian if no note calls them' });
  });

  // 4. calendar, plan, today's note
  await sec('calendar', async () => {
    const y = moment().year(), nextYear = moment().add(12, 'months').year();
    const panch = [y, nextYear].map(yy => [yy, !!app.vault.getAbstractFileByPath(`Calendar/Panchang ${yy} (Hickory).md`)]);
    const shab = notes.find(f => f.path.startsWith('Calendar/') && /Shabbat/i.test(f.basename));
    let shabLast = null; if (shab) { const m = (await app.vault.read(shab)).match(/\| (\d{4}-\d{2}-\d{2}) \|/g); if (m) shabLast = m[m.length - 1].slice(2, 12); }
    let planRow = false; for (const f of notes.filter(f => f.path.startsWith('Texts/Tantraloka/Study plan/'))) { if ((await app.vault.read(f)).includes(`| ${today} |`)) { planRow = true; break; } }
    const todayNote = !!app.vault.getAbstractFileByPath(`Journal/${today.slice(0, 4)}/${today}.md`);
    Object.assign(R.numbers, { panchang_this_year: panch[0][1], panchang_next_year: panch[1][1], shabbat_table_ends: shabLast, plan_has_today: planRow, today_note_exists: todayNote });
    const ok = panch.every(p => p[1]) && shabLast && moment(shabLast).diff(moment(), 'months') >= 12;
    if (ok) R.fine.push(`Calendar tables cover the next 12 months (panchang ${panch.map(p => p[0]).join(' and ')} present; Shabbat table to ${shabLast}).`);
    else R.attention.push({ what: `Calendar tables: panchang ${panch.map(p => p[0] + (p[1] ? ' ok' : ' MISSING')).join(', ')}; Shabbat table ends ${shabLast}`, paths: [], run: 'Extend the calendar tables' });
    if (planRow) R.fine.push('The study plan has a row for today.'); else R.attention.push({ what: 'No study-plan row for today', paths: [], run: 'look at Texts/Tantraloka/Study plan; after Advent 2029 the plan is over' });
    if (!todayNote) R.notes.push("Today's daily note does not exist yet (Home's button, the Calendar, or the startup setting makes it).");
  });

  // 5. dashboards: render in the tab that already shows the note (Vertical Tabs deduplicates a second one) or a fresh tab
  await sec('render', async () => {
    const errs = []; const origErr = console.error;
    console.error = (...a) => { errs.push(a.map(x => { try { return String((x && x.message) || x); } catch (e) { return '?'; } }).join(' ').slice(0, 200)); try { origErr.apply(console, a); } catch (e) {} };
    const prevLeaf = app.workspace.activeLeaf; const out = [];
    try {
      for (const p of ['Home.md', 'Home (mobile).md', 'Calendar/Calendar.md', 'Journal/Habits.base', 'Catalog/Catalog.base', `Journal/${today.slice(0, 4)}/${today}.md`]) {
        const f = app.vault.getAbstractFileByPath(p); if (!f) { out.push([p, 'absent']); continue; }
        const n0 = errs.length; let el = null, made = null;
        const open = app.workspace.getLeavesOfType(f.extension === 'base' ? 'bases' : 'markdown').find(l => l.view && l.view.file && l.view.file.path === p);
        if (open) { const v = open.view; el = (v.getMode && v.getMode() === 'preview' && v.previewMode) ? v.previewMode.containerEl : v.containerEl; }
        else {
          try { made = app.workspace.getLeaf('tab'); } catch (e) { made = app.workspace.createLeafInParent(app.workspace.rootSplit, 0); }
          if (f.extension === 'base') await made.setViewState({ type: 'bases', state: { file: p }, active: true });
          else await made.setViewState({ type: 'markdown', state: { file: p, mode: 'preview', source: false }, active: true });
          await sleep(6500);
          const v = made.view; el = (v && v.previewMode && v.previewMode.containerEl) || (v && v.containerEl);
        }
        const txt = el ? el.textContent.replace(/\s+/g, ' ') : '';
        const errEls = el ? [...el.querySelectorAll('.dataview-error, .dataview-error-box, .dataviewjs-error, .dataview-error-message, .bases-error, .markdown-embed-error, .mod-error')].filter(x => x.textContent.trim()).map(x => x.textContent.trim().slice(0, 120)) : [];
        out.push([p, { chars: txt.length, errors: errEls, console: errs.slice(n0).slice(0, 3) }]);
        if (made) { try { made.detach(); } catch (e) {} }
      }
    } finally { console.error = origErr; try { if (prevLeaf) app.workspace.setActiveLeaf(prevLeaf, { focus: true }); } catch (e) {} }
    R.render = out;
    const bad = out.filter(o => typeof o[1] !== 'string' && (o[1].errors.length || o[1].console.length || o[1].chars < 200));
    if (!bad.length) R.fine.push(`Dashboards render without errors: ${out.filter(o => typeof o[1] !== 'string').map(o => o[0]).join(', ')}.`);
    else R.attention.push({ what: `Dashboards with errors or no content: ${bad.length}`, paths: bad.map(o => `${o[0]}: ${o[1].errors.concat(o[1].console).join(' | ') || 'empty'}`), run: 'open the note and read the red box; if a view is missing, check Sync all other types; else a short AI session' });
  });

  // 6. sizes, hidden folders, growth
  await sec('sizes', async () => {
    const byKind = { pdf: 0, md: 0, txt: 0, images: 0, other: 0 }; let total = 0;
    for (const f of files) { const s = f.stat.size; total += s; const e = f.extension.toLowerCase(); if (e === 'pdf') byKind.pdf += s; else if (e === 'md') byKind.md += s; else if (e === 'txt') byKind.txt += s; else if (/^(png|jpe?g|gif|svg|webp)$/.test(e)) byKind.images += s; else byKind.other += s; }
    const hidden = {}; const walk = async (dir, acc) => { const l = await ad.list(dir); for (const fp of l.files) { try { const st = await ad.stat(fp); acc.bytes += st ? st.size : 0; acc.files++; } catch (e) {} } for (const d of l.folders) if (acc.files < 60000) await walk(d, acc); };
    for (const d of ['.trash', '.work', '.smart-env']) { const acc = { bytes: 0, files: 0 }; if (await ad.exists(d)) await walk(d, acc); hidden[d] = acc; }
    const big = files.filter(f => f.stat.size > 50 * 1048576 && f.stat.mtime > since).map(f => `${f.path} (${mb(f.stat.size)} MB)`);
    Object.assign(R.numbers, { vault_mb: mb(total), pdf_mb: mb(byKind.pdf), notes_mb: mb(byKind.md), txt_mb: mb(byKind.txt), images_mb: mb(byKind.images), other_mb: mb(byKind.other), trash_mb: mb(hidden['.trash'].bytes), work_mb: mb(hidden['.work'].bytes), smart_env_mb: mb(hidden['.smart-env'].bytes), remote_estimate_mb: mb(total - byKind.pdf - byKind.txt) });
    R.fine.push(`Size: ${mb(total)} MB in the vault (PDFs ${mb(byKind.pdf)}, notes ${mb(byKind.md)}, e-texts ${mb(byKind.txt)}, images ${mb(byKind.images)}); about ${mb(total - byKind.pdf - byKind.txt)} MB would be in the remote vault with PDFs and the e-texts off. Hidden: .trash ${mb(hidden['.trash'].bytes)} MB, .work ${mb(hidden['.work'].bytes)} MB, .smart-env ${mb(hidden['.smart-env'].bytes)} MB.`);
    if (hidden['.trash'].bytes > 500 * 1048576) R.attention.push({ what: `.trash holds ${mb(hidden['.trash'].bytes)} MB`, paths: [], run: 'empty it in Windows Explorer when you are sure (the one deletion outside Obsidian that is fine)' });
    if (hidden['.work'].bytes > 1500 * 1048576) R.notes.push(`.work holds ${mb(hidden['.work'].bytes)} MB (backups and scratch); the backup folders are yours to clear when the work they guard is settled.`);
    R.bigFiles = big;
    if (big.length) R.notes.push(`Files over 50 MB written since ${prevDate || moment(since).format('D MMM YYYY')} (new or replaced, as after an OCR pass): ${big.slice(0, 8).join('; ')}${big.length > 8 ? `; and ${big.length - 8} more (the JSON lists them)` : ''}.`);
    if (prev && prev.vault_mb) R.notes.push(`Growth since ${prevDate}: ${mb(total) - prev.vault_mb} MB; notes ${notes.length - (prev.notes || 0)}; files ${files.length - (prev.files || 0)}.`);
  });

  // 7. new writing with references that are not links (a rough count, by pattern)
  await sec('references', async () => {
    const books = '(?:Gen(?:esis)?|Exod(?:us)?|Lev(?:iticus)?|Num(?:bers)?|Deut(?:eronomy)?|Josh(?:ua)?|Judg(?:es)?|Ruth|1 ?Sam(?:uel)?|2 ?Sam(?:uel)?|1 ?Kgs|2 ?Kgs|1 ?Kings|2 ?Kings|Isa(?:iah)?|Jer(?:emiah)?|Ezek(?:iel)?|Hos(?:ea)?|Joel|Amos|Obad(?:iah)?|Jon(?:ah)?|Mic(?:ah)?|Nah(?:um)?|Hab(?:akkuk)?|Zeph(?:aniah)?|Hag(?:gai)?|Zech(?:ariah)?|Mal(?:achi)?|Ps(?:alms?)?|Prov(?:erbs)?|Job|Song|Eccl(?:esiastes)?|Lam(?:entations)?|Dan(?:iel)?|Ezra|Neh(?:emiah)?|1 ?Chr(?:onicles)?|2 ?Chr(?:onicles)?|Matt(?:hew)?|Mark|Luke|John|Acts|Rom(?:ans)?|1 ?Cor(?:inthians)?|2 ?Cor(?:inthians)?|Gal(?:atians)?|Eph(?:esians)?|Phil(?:ippians)?|Col(?:ossians)?|1 ?Thess(?:alonians)?|2 ?Thess(?:alonians)?|1 ?Tim(?:othy)?|2 ?Tim(?:othy)?|Titus|Philem(?:on)?|Heb(?:rews)?|Jas|James|1 ?Pet(?:er)?|2 ?Pet(?:er)?|1 ?John|2 ?John|3 ?John|Jude|Rev(?:elation)?)';
    const re = new RegExp(`\\b${books}\\.? \\d+:\\d+|\\bZohar \\d:\\d+[ab]|\\bT\\.?Ā\\.? \\d+\\.\\d+|\\bTantrāloka \\d+\\.\\d+`, 'g');
    const hits = [];
    for (const f of notes.filter(f => /^(Notes|Projects|Journal)\//.test(f.path) && f.stat.mtime > since)) {
      const t = (await app.vault.read(f)).replace(/\[\[[^\]]*\]\]/g, '').replace(/```[\s\S]*?```/g, '');
      const n = (t.match(re) || []).length; if (n) hits.push([f.path, n]);
    }
    R.numbers.unlinked_reference_notes = hits.length;
    if (hits.length) R.notes.push(`Notes changed since ${prevDate || 'last month'} with scripture, Zohar or Tantrāloka references that are not links (a rough count): ${hits.slice(0, 8).map(h => `${h[0]} (${h[1]})`).join('; ')}${hits.length > 8 ? ' …' : ''}. *Map new connections* links them in one pass.`);
    else R.fine.push(`No new writing since ${prevDate || 'last month'} carries unlinked scripture, Zohar or Tantrāloka references (by pattern).`);
  });

  // 8. plugins and settings
  await sec('plugins', async () => {
    const P = app.plugins; const loaded = Object.keys(P.plugins).length; const enabled = [...P.enabledPlugins];
    const stale = enabled.filter(id => !P.manifests[id]);
    let types = {}; try { types = JSON.parse(await ad.read('.obsidian/types.json')).types || {}; } catch (e) {}
    const habitKeys = ['date', 'office', 'tantraloka', 'letter', 'reading_min', 'cis', 'exercise', 'calls', 'puja', 'church'];
    const untyped = habitKeys.filter(k => !types[k]);
    Object.assign(R.numbers, { plugins_loaded: loaded, plugins_enabled_ids: enabled.length, stale_plugin_ids: stale.length, untyped_habit_properties: untyped.length });
    R.fine.push(`Plugins: ${loaded} loaded; ${enabled.length} ids on the on-list${stale.length ? ` (${stale.length} stale: ${stale.join(', ')} — the C3 item)` : ''}.`);
    if (untyped.length) R.notes.push(`Property types not set on this device: ${untyped.join(', ')} (the properties pane: icon left of the name → Property type).`);
    const tpl = P.plugins['templater-obsidian']; if (!tpl) R.attention.push({ what: 'Templater is not loaded', paths: [], run: 'Settings → Community plugins' });
    const dv = P.plugins['dataview']; if (dv && dv.settings && dv.settings.enableDataviewJs === false) R.attention.push({ what: 'Dataview JavaScript queries are off', paths: [], run: 'Settings → Dataview → Enable JavaScript queries' });
  });

  // the report
  const fmt = v => (v === null || v === undefined) ? '—' : String(v);
  const rows = Object.keys(R.numbers).map(k => `| ${k} | ${fmt(R.numbers[k])} | ${prev ? fmt(prev[k]) : '—'} |`).join('\n');
  const att = R.attention.length ? R.attention.map(a => `- **${a.what}.** Run: ${a.run}.${a.paths.length ? '\n' + a.paths.map(p => `    - \`${p}\``).join('\n') : ''}`).join('\n') : '- Nothing.';
  const note = ['---', 'type: health-report', `date: ${today}`, ...Object.entries(R.numbers).map(([k, v]) => `${k}: ${typeof v === 'string' ? JSON.stringify(v) : v}`), '---',
    `# Health report ${today}`, '',
    `Written by \`AI/Prompts/Scripts/Health checks/health-report.js\` through the runner on ${moment().format('D MMMM YYYY, HH:mm')} (${Math.round((Date.now() - t0) / 1000)} s). No AI was involved and nothing else was changed. Previous report: ${prevDate ? `[[Health report ${prevDate}]]` : 'none'}. Full figures: \`.work/out/health-report-${today}.json\`.`, '',
    '## Needs attention', '', att, '',
    '## Worth knowing', '', R.notes.length ? R.notes.map(n => `- ${n}`).join('\n') : '- Nothing.', '',
    '## Fine', '', R.fine.map(n => `- ${n}`).join('\n'), '',
    '## Numbers', '', `| Measure | ${today} | ${prevDate || 'previous'} |`, '|---|---|---|', rows, '',
    '## Checks that failed to run', '', R.errors.length ? R.errors.map(e => `- ${e}`).join('\n') : '- None.', '',
    '## What this report does not see', '', '- Sync\'s own settings and the remote vault\'s real size (Settings → Sync shows them); the phone and tablet; the Downloads folder; the correctness of any text. For those, and for anything red above, the prompts in [[Prompts - read me]] say which short AI session to run.', ''].join('\n');
  const path = `AI/Health reports/Health report ${today}.md`;
  if (!app.vault.getAbstractFileByPath('AI/Health reports')) await app.vault.createFolder('AI/Health reports');
  const existing = app.vault.getAbstractFileByPath(path);
  if (existing) await app.vault.modify(existing, note); else await app.vault.create(path, note);
  await ad.write(`.work/out/health-report-${today}.json`, JSON.stringify(R, null, 1));
  return `health-report: ${path} written (${note.length} chars); attention ${R.attention.length}, notes ${R.notes.length}, fine ${R.fine.length}, failed checks ${R.errors.length} ${JSON.stringify(R.errors)}; ${Math.round((Date.now() - t0) / 1000)} s`;
})()
