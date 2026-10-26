(async () => {
  // Phase 8, step 1 (read-only, part 2): property types from .obsidian/types.json, calendar and study-plan coverage, views and templates
  // (parse check and where they are used), plugin states, and a few single notes the first run flagged. Writes .work/out/health-<date>c.json (the run's local date).
  // 14 Oct 2026 (audit K-09, LEAD-01): Smart Connections read from .smart-env/smart_env.json; Obsidian's inferred property types tested too.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now(), R = { when: new Date().toISOString() };
  const LIM = performance.memory.jsHeapSizeLimit, heap = () => performance.memory.usedJSHeapSize; let peak = heap();
  const guard = w => { const h = heap(); if (h > peak) peak = h; if (h > LIM - 300e6) throw new Error('memory guard at ' + w); };
  const md = app.vault.getMarkdownFiles(), files = app.vault.getFiles();
  const fmOf = f => ((MC.getFileCache(f) || {}).frontmatter) || {};
  const readJ = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return { _error: String(e) }; } };
  // property types
  const typesJ = await readJ('.obsidian/types.json'); const types = (typesJ && typesJ.types) || {};
  R.types = types; R.typesError = typesJ._error;
  let mtm = {}; try { const M = app.metadataTypeManager; mtm = { keys: Object.keys(M), sampleProp: M.getPropertyInfo ? M.getPropertyInfo('year') : null, propertiesSample: M.properties ? Object.entries(M.properties).slice(0, 3) : null }; } catch (e) { mtm = String(e); }
  R.mtm = mtm;
  const tc = {}; const propCount = {};
  for (const f of md) { const fm = fmOf(f); for (const [k, v] of Object.entries(fm)) {
    propCount[k] = (propCount[k] || 0) + 1;
    if (v === null || v === undefined || v === '') continue;
    const t = types[k]; if (!t) continue;
    let bad = false;
    if (t === 'number') bad = typeof v !== 'number';
    else if (t === 'checkbox') bad = typeof v !== 'boolean';
    else if (t === 'date') bad = !(typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v));
    else if (t === 'datetime') bad = !(typeof v === 'string' && /^\d{4}-\d{2}-\d{2}/.test(v));
    else if (t === 'multitext' || t === 'tags' || t === 'aliases') bad = !Array.isArray(v) && typeof v !== 'string';
    else if (t === 'text') bad = typeof v === 'object';
    if (bad) { (tc[k] = tc[k] || { type: t, count: 0, examples: [] }); tc[k].count++; if (tc[k].examples.length < 8) tc[k].examples.push([f.path, JSON.stringify(v).slice(0, 80)]); }
  } }
  R.propertyTypeConflicts = tc; R.propertyCounts = Object.entries(propCount).sort((a, b) => b[1] - a[1]);
  // Obsidian's own type for each property that types.json does not list (inferred from the values, or set in Settings → Properties):
  // a value that does not fit is shown with a warning in the properties pane (e.g. "887–904" in `pages`, inferred as a number).
  const inf = {}; try { const M = app.metadataTypeManager;
    for (const k of Object.keys(propCount)) { if (types[k]) continue; let info = null;
      try { info = (M.getTypeInfo && M.getTypeInfo(k)) || (M.getPropertyInfo && M.getPropertyInfo(k)) || (M.properties && M.properties[k]) || null; } catch (e) {}
      const w = info && (info.expected ? info.expected.type : (info.inferred ? info.inferred.type : info.type || info.widget)) || null;
      if (w) inf[k] = { type: w, notes: propCount[k], count: 0, examples: [] }; }
    for (const f of md) { const fm = fmOf(f); for (const [k, v] of Object.entries(fm)) { const e = inf[k]; if (!e || v === null || v === undefined || v === '') continue; const t = e.type;
      const bad = t === 'number' ? typeof v !== 'number' : t === 'checkbox' ? typeof v !== 'boolean' : t === 'date' ? !(typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)) : t === 'datetime' ? !(typeof v === 'string' && /^\d{4}-\d{2}-\d{2}/.test(v)) : (t === 'multitext' || t === 'tags' || t === 'aliases') ? !Array.isArray(v) && typeof v !== 'string' : t === 'text' ? typeof v === 'object' : false;
      if (bad) { e.count++; if (e.examples.length < 8) e.examples.push([f.path, JSON.stringify(v).slice(0, 80)]); } } }
  } catch (e) { inf._error = String(e); }
  R.inferredTypeConflicts = Object.fromEntries(Object.entries(inf).filter(([k, e]) => k === '_error' || e.count));
  // catalog type and status values
  const catNotes = md.filter(f => /^Catalog\/[^/]+\/[^/]+\.md$/.test(f.path) && !f.path.startsWith('Catalog/Scholars/') && f.basename !== f.parent.name);
  const cnt = k => { const c = {}; for (const f of catNotes) { const v = fmOf(f)[k]; const s = JSON.stringify(v); c[s] = (c[s] || 0) + 1; } return c; };
  R.catalogValues = { type: cnt('type'), status: cnt('status'), text: cnt('text'), subjectFirst: (() => { const c = {}; for (const f of catNotes) { const v = [].concat(fmOf(f).subject || [])[0]; c[v] = (c[v] || 0) + 1; } return c; })() };
  // review notes: the sentence that says why (first body line with 'review' or 'Note')
  R.reviewWhy = [];
  for (const f of catNotes.filter(f => fmOf(f).status === 'review')) { const t = await app.vault.cachedRead(f); const body = t.replace(/^---[\s\S]*?---\s*/, ''); const lines = body.split('\n').filter(l => /review|unverified|not (yet )?checked|Note|check/i.test(l)).slice(0, 2); R.reviewWhy.push([f.path, lines.map(l => l.slice(0, 220))]); }
  guard('review');
  // calendar tables: date coverage
  R.calendar = [];
  for (const f of md.filter(f => f.path.startsWith('Calendar/') && f.path.split('/').length === 2)) { const t = await app.vault.cachedRead(f); const ds = [...t.matchAll(/\b(20\d\d-\d\d-\d\d)\b/g)].map(m => m[1]); if (ds.length < 20) continue; ds.sort(); R.calendar.push([f.path, ds.length, ds[0], ds[ds.length - 1]]); }
  // study plan: a row for today
  const today = new Date(); const iso = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0'); R.today = iso;
  R.studyPlan = [];
  for (const f of md.filter(f => f.path.startsWith('Texts/Tantraloka/Study plan/'))) { const t = await app.vault.cachedRead(f); const rows = t.split('\n').filter(l => l.includes(iso)); const ds = [...t.matchAll(/\b(20\d\d-\d\d-\d\d)\b/g)].map(m => m[1]).sort(); R.studyPlan.push([f.path, rows.length, rows[0] ? rows[0].slice(0, 300) : null, ds[0], ds[ds.length - 1]]); }
  // views: parse check
  R.views = [];
  for (const f of files.filter(f => f.path.startsWith('Templates/Views/') && f.extension === 'js')) { const code = await ad.read(f.path); let ok = true, err = null; try { new Function('dv', 'input', 'app', 'moment', 'return (async () => {\n' + code + '\n})'); } catch (e) { ok = false; err = String(e); } R.views.push([f.path, code.length, ok, err]); }
  // where views and templates are used: scan notes outside Library/Texts/Journal plus the templates and Home
  const used = {}; const tplUsed = {}; const scanSet = md.filter(f => !f.path.startsWith('Library/') && !f.path.startsWith('Texts/') && !f.path.startsWith('Journal/') && !f.path.startsWith('Calendar/Great') && !f.path.startsWith('Catalog/') && !f.path.startsWith('AI/Archive/'));
  const viewNames = files.filter(f => f.path.startsWith('Templates/Views/') && f.name === 'view.js').map(f => f.path.split('/')[2]);
  const tplNames = md.filter(f => f.path.startsWith('Templates/') && !f.path.startsWith('Templates/Views/')).map(f => f.basename);
  const viewCode = {}; for (const f of files.filter(f => f.path.startsWith('Templates/Views/') && f.extension === 'js')) viewCode[f.path] = await ad.read(f.path);
  const texts = [];
  for (const f of scanSet) texts.push([f.path, await app.vault.cachedRead(f)]);
  for (const [p, c] of Object.entries(viewCode)) texts.push([p, c]);
  for (const [p, t] of texts) {
    for (const v of viewNames) if (t.includes('Templates/Views/' + v)) (used[v] = used[v] || []).push(p);
    for (const n of tplNames) if (t.includes('"' + n + '"') || t.includes("'" + n + "'") || t.includes('[[' + n) || t.includes('Templates/' + n)) (tplUsed[n] = tplUsed[n] || []).push(p);
  }
  R.viewsUsed = Object.fromEntries(viewNames.map(v => [v, (used[v] || []).filter(p => !p.startsWith('Templates/Views/' + v))]));
  R.templatesUsed = Object.fromEntries(tplNames.map(n => [n, tplUsed[n] || []]));
  guard('scan');
  // Templater and other settings (read only)
  const tpl = await readJ('.obsidian/plugins/templater-obsidian/data.json');
  R.templater = tpl && { folder_templates: tpl.folder_templates, trigger_on_file_creation: tpl.trigger_on_file_creation, templates_folder: tpl.templates_folder, user_scripts_folder: tpl.user_scripts_folder, enable_folder_templates: tpl.enable_folder_templates, _error: tpl._error };
  R.communityPlugins = await readJ('.obsidian/community-plugins.json');
  R.appJson = await readJ('.obsidian/app.json');
  R.homepage = (p => p && { value: p.value, mobileValue: p.mobileValue, separateMobile: p.separateMobile, hasMobile: p.hasMobile, openOnStartup: p.openOnStartup, _error: p._error })(await readJ('.obsidian/plugins/homepage/data.json'));
  R.folderNotes = (p => p && { excludeFolders: p.excludeFolders, folderNoteName: p.folderNoteName, _error: p._error })(await readJ('.obsidian/plugins/folder-notes/data.json'));
  R.smartEnv = (p => { if (!p || p._error) return p; const s = p.smart_sources || {}; const fl = s.folder_exclusions_list; const list = Array.isArray(fl) ? fl : typeof fl === 'string' ? fl.split(',').map(x => x.trim()).filter(Boolean) : [];
    return { folderExclusions: list.length, folders: list, fileExclusions: s.file_exclusions || null }; })(await readJ('.smart-env/smart_env.json'));
  R.omnisearch = (p => p && { useCache: p.useCache, PDFIndexing: p.PDFIndexing, downrankedFoldersFilters: p.downrankedFoldersFilters, _error: p._error })(await readJ('.obsidian/plugins/omnisearch/data.json'));
  R.snippets = (await readJ('.obsidian/appearance.json'));
  R.workspacesJson = (p => p && { names: Object.keys(p.workspaces || {}), active: p.active, _error: p._error })(await readJ('.obsidian/workspaces.json'));
  try { R.syncState = { enabled: !!app.internalPlugins.plugins.sync?.enabled, instance: (i => i && { vaultName: i.vaultName, vaultId: i.vaultId ? 'set' : 'none', syncStatus: i.syncStatus, paused: i.pause, allowTypes: i.allowTypes, allowSpecialFiles: i.allowSpecialFiles, ignoreFolders: i.ignoreFolders, syncAppearance: i.syncAppearance })(app.internalPlugins.plugins.sync?.instance) }; } catch (e) { R.syncState = String(e); }
  // single notes flagged
  const one = async p => { const f = app.vault.getAbstractFileByPath(p); return f ? (await app.vault.cachedRead(f)).slice(0, 1500) : null; };
  R.notes = {};
  for (const p of ['Journal/2026/2026-10-04.md', 'Journal/2026/2026-10-11.md', 'Catalog/Philosophy/Plato - Timaeus.md', 'Catalog/Philosophy/Hobbes - Leviathan (1651).md', 'Catalog/Biblical-Studies/NRSV Updated Edition (2021).md', 'Catalog/Trika/Rastogi - Metaphysics and Tantric Esotericism of Krama.md', 'Catalog/Sanskrit-Study/108 Sanskrit Flash Cards.md', 'Synoptic View.md', 'Study/Concepts/Concepts.md', 'Texts/Chasidut/Chasidut.md']) R.notes[p] = await one(p);
  R.goudriaanFolder = (app.vault.getAbstractFileByPath('Library/Trika/Ritual and Speculation in Early Tantrism (Goudriaan)') || { children: [] }).children.map(c => c.name);
  R.excalidraw = (app.vault.getAbstractFileByPath('Excalidraw') || { children: [] }).children.map(c => c.name);
  R.journal = (app.vault.getAbstractFileByPath('Journal') || { children: [] }).children.map(c => c.path);
  R.notesFolder = (app.vault.getAbstractFileByPath('Notes') || { children: [] }).children.map(c => c.path);
  R.scholars = (app.vault.getAbstractFileByPath('Catalog/Scholars') || { children: [] }).children.length;
  R.aiArchive = (app.vault.getAbstractFileByPath('AI/Archive') || { children: [] }).children.map(c => c.path);
  R.seconds = Math.round((Date.now() - T0) / 1000); R.peakHeapMB = Math.round(peak / 1e6);
  await ad.write('.work/out/health-' + new Date().toLocaleDateString('sv') + 'c.json', JSON.stringify(R, null, 1));
  return `read-only: types ${Object.keys(types).length}; type conflicts ${Object.keys(tc).length}; inferred-type conflicts ${Object.keys(R.inferredTypeConflicts).length}; Smart Connections folder exclusions ${R.smartEnv && R.smartEnv.folderExclusions}; calendar tables ${R.calendar.length}; study plan files ${R.studyPlan.length}; views ${R.views.length} (${R.views.filter(v => !v[2]).length} fail to parse); scanned ${texts.length}; ${R.seconds}s, peak ${R.peakHeapMB} MB`;
})()
