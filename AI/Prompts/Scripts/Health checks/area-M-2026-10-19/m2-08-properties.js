(async () => {
  // Area M re-run, check 8 (19 Oct 2026, after Part 1): properties against the Guide's vocabularies. Changed since 10:30
  // by the tags removal (the `tags` property on 24,156 notes) and the new notes' properties (type flashcard, cis-cards,
  // scholar, study-plan; card, card_label, alpha, category, cis_chapter, cis_start, cis_mwf, cis_tth, …).
  // Same tables as at 10:30: the vocabularies (type, subject, status, text, stage, propers) by scope (top folder;
  // Catalog/Scholars apart; top-level notes = "other"); values outside them; property counts; JS value types per property
  // and properties that mix them; types.json against the values; capitals in names; the forms of year, date,
  // physical_copy and pages; the catalog notes (Catalog/<subject>/<note>.md with `files:`) against the vocabularies; and
  // the type Obsidian assigns each property (types.json or inferred) against the values. Compared with
  // .work/out/areaM/check08-properties.json. Read-only: writes only .work/out/areaM2/properties.json.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const NAME = 'properties', OUT = '.work/out/areaM2';
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const R = { job: 'm2-08-properties', when: new Date().toISOString() };
  let line = '';
  try {
    const md = app.vault.getMarkdownFiles();
    const VOCAB = { type: ['book', 'article', 'chapter', 'thesis', 'collection', 'multi-volume-set', 'text', 'other'], subject: ['Trika', 'Judaica', 'Christianity', 'Philosophy', 'Sanskrit-Study', 'Hinduism', 'Biblical-Studies', 'Other'], status: ['keep', 'reading', 'review', 'delete'], text: ['searchable', 'scan', 'print'], stage: ['idea', 'drafting', 'finished', 'preached'], propers: ['sunday', 'feast', 'both'] };
    const SUBJ = VOCAB.subject;
    const scopeOf = p => p.startsWith('Catalog/Scholars/') ? 'Catalog/Scholars' : p.includes('/') ? p.split('/')[0] : 'other';
    const kind = v => v === null || v === undefined || v === '' || (Array.isArray(v) && !v.length) ? 'empty' : Array.isArray(v) ? 'array' : typeof v;
    const vals = v => (Array.isArray(v) ? v : [v]).filter(x => x !== null && x !== undefined && x !== '').map(x => typeof x === 'string' ? x : JSON.stringify(x));
    const tables = {}, counts = {}, jsTypes = {}, samples = {}, upper = {};
    const forms = { year: [], date: [], physical_copy: [], pages: [] };
    let withFm = 0, n = 0;
    for (const f of md) {
      const fm = (MC.getFileCache(f) || {}).frontmatter; if (!fm) continue; withFm++; const sc = scopeOf(f.path);
      for (const [k, v] of Object.entries(fm)) {
        inc(counts, k); const kd = kind(v); jsTypes[k] = jsTypes[k] || {}; inc(jsTypes[k], kd); samples[k] = samples[k] || {}; if (!samples[k][kd]) samples[k][kd] = f.path;
        if (/[A-Z]/.test(k)) inc(upper, k);
        if (VOCAB[k]) for (const x of vals(v)) { const t = tables[k] = tables[k] || {}; const e = t[x] = t[x] || { _files: [] }; inc(e, sc); if (e._files.length < 8) e._files.push(f.path); }
      }
      if (kind(fm.year) !== 'empty' && typeof fm.year !== 'number') forms.year.push([f.path, kind(fm.year), fm.year]);
      if (kind(fm.date) !== 'empty' && !(typeof fm.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(fm.date))) forms.date.push([f.path, kind(fm.date), String(fm.date).slice(0, 40)]);
      if (kind(fm.physical_copy) !== 'empty' && typeof fm.physical_copy !== 'boolean') forms.physical_copy.push([f.path, kind(fm.physical_copy), fm.physical_copy]);
      if (typeof fm.pages === 'string' && fm.pages !== '') forms.pages.push([f.path, 'string', fm.pages]);
      if (++n % 2000 === 0) { guard('props ' + n); await new Promise(r => setTimeout(r, 0)); }
    }
    const outside = {};
    for (const k of Object.keys(VOCAB)) outside[k] = Object.entries(tables[k] || {}).filter(([v]) => !VOCAB[k].includes(v)).map(([v, e]) => { const byScope = Object.fromEntries(Object.entries(e).filter(([s]) => s !== '_files')); return { value: v, byScope, total: Object.values(byScope).reduce((a, b) => a + b, 0), sampleFiles: e._files }; }).sort((a, b) => b.total - a.total);
    const mixed = Object.entries(jsTypes).filter(([, t]) => Object.keys(t).filter(x => x !== 'empty').length > 1).map(([k, t]) => ({ prop: k, types: t, samples: Object.values(samples[k]) }));
    // types.json and Obsidian's assigned types
    const tj = await readJSON('.obsidian/types.json'); const declared = (tj && (tj.types || tj)) || {};
    const fits = (t, v) => t === 'number' ? typeof v === 'number' : t === 'checkbox' ? typeof v === 'boolean' : t === 'date' ? typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v) : t === 'datetime' ? typeof v === 'string' && /^\d{4}-\d{2}-\d{2}/.test(v) : (t === 'multitext' || t === 'tags' || t === 'aliases') ? Array.isArray(v) || typeof v === 'string' : t === 'text' ? typeof v !== 'object' : true;
    let props = {}; try { const M = app.metadataTypeManager; props = (M.getAllProperties ? M.getAllProperties() : M.properties) || {}; } catch (e) { R.typeManagerError = String(e); }
    const assigned = k => declared[k] || declared[k.toLowerCase()] || (props[k.toLowerCase()] || props[k] || {}).type;
    const declMismatch = {}, assignedConflicts = {};
    for (const f of md) {
      const fm = (MC.getFileCache(f) || {}).frontmatter; if (!fm) continue;
      for (const [k, v] of Object.entries(fm)) {
        if (kind(v) === 'empty') continue;
        if (declared[k] && !fits(declared[k], v)) { const e = declMismatch[k] = declMismatch[k] || { type: declared[k], count: 0, examples: [] }; e.count++; if (e.examples.length < 5) e.examples.push([f.path, JSON.stringify(v).slice(0, 60)]); }
        const t = assigned(k); if (t && !fits(t, v)) { const e = assignedConflicts[k] = assignedConflicts[k] || { type: t, count: 0, examples: [] }; e.count++; if (e.examples.length < 5) e.examples.push([f.path, JSON.stringify(v).slice(0, 60)]); }
      }
    }
    guard('types');
    // catalog notes
    const cat = md.filter(f => /^Catalog\/[^/]+\/[^/]+\.md$/.test(f.path) && !f.path.startsWith('Catalog/Scholars/') && 'files' in (((MC.getFileCache(f) || {}).frontmatter) || {}));
    const CK = { notes: cat.length, typeOutside: [], statusOutside: [], textOutside: [], noValidSubject: [], narrowerAfterValid: {}, twoOrMoreSubjects: 0, twoOrMoreValidSubjects: 0, folderNotInSubject: [] };
    for (const f of cat) {
      const fm = MC.getFileCache(f).frontmatter; const folder = f.path.split('/')[1];
      if (fm.type !== undefined && fm.type !== null && !VOCAB.type.includes(fm.type)) CK.typeOutside.push([f.path, fm.type]);
      if (fm.status !== undefined && fm.status !== null && !VOCAB.status.includes(fm.status)) CK.statusOutside.push([f.path, fm.status]);
      if (fm.text !== undefined && fm.text !== null && !VOCAB.text.includes(fm.text)) CK.textOutside.push([f.path, fm.text]);
      const sj = vals(fm.subject); if (!sj.length || !SUBJ.includes(sj[0])) CK.noValidSubject.push([f.path, sj]);
      for (const s of sj.slice(1)) if (!SUBJ.includes(s)) inc(CK.narrowerAfterValid, s);
      if (sj.length > 1) CK.twoOrMoreSubjects++; if (sj.filter(s => SUBJ.includes(s)).length > 1) CK.twoOrMoreValidSubjects++;
      if (SUBJ.includes(folder) && !sj.includes(folder)) CK.folderNotInSubject.push([f.path, sj]);
    }
    const hom = md.filter(f => ((MC.getFileCache(f) || {}).frontmatter || {}).type === 'homily');
    const HM = { notes: hom.length, stage: {}, propers: {} }; for (const f of hom) { const fm = MC.getFileCache(f).frontmatter; for (const s of vals(fm.stage)) inc(HM.stage, s); for (const s of vals(fm.propers)) inc(HM.propers, s); }
    // against 10:30
    const old = await readJSON('.work/out/areaM/check08-properties.json'); const cmp = {};
    if (old) {
      const oc = old.propertyCounts || {};
      cmp.newKeys = Object.keys(counts).filter(k => !(k in oc)).map(k => [k, counts[k]]);
      cmp.goneKeys = Object.keys(oc).filter(k => !(k in counts)).map(k => [k, oc[k]]);
      cmp.changedCounts = Object.keys(counts).filter(k => k in oc && oc[k] !== counts[k]).map(k => [k, oc[k], counts[k]]).sort((a, b) => Math.abs(b[2] - b[1]) - Math.abs(a[2] - a[1]));
      cmp.outsideVocabulary = {};
      for (const k of Object.keys(VOCAB)) { const o = Object.fromEntries(((old.outsideVocabulary || {})[k] || []).map(e => [e.value, e.total])); const nw = Object.fromEntries(outside[k].map(e => [e.value, e.total])); const d = [...new Set([...Object.keys(o), ...Object.keys(nw)])].filter(v => (o[v] || 0) !== (nw[v] || 0)).map(v => [v, o[v] || 0, nw[v] || 0]); if (d.length) cmp.outsideVocabulary[k] = d; }
      const om = (old.mixedTypeProperties || []).map(e => e.prop); cmp.mixedNew = mixed.map(e => e.prop).filter(p => !om.includes(p)); cmp.mixedGone = om.filter(p => !mixed.some(e => e.prop === p));
      cmp.pagesAsText1030 = ((old.explicitForms || {}).pages || []).length;
    } else cmp.error = 'check08-properties.json not readable';
    R.notesWithFrontmatter = withFm; R.vocabulary = VOCAB; R.valueTablesByScope = tables; R.outsideVocabulary = outside; R.propertyCounts = counts; R.propertyJsTypes = jsTypes;
    R.mixedTypeProperties = mixed; R.declaredTypesFile = declared; R.declaredVsActualMismatch = declMismatch; R.assignedTypeConflicts = assignedConflicts; R.namesWithUppercase = upper;
    R.explicitForms = forms; R.catalog = CK; R.homilies = HM; R.against1030 = cmp;
    line = `properties: ${withFm} notes with frontmatter, ${Object.keys(counts).length} property names (136 at 10:30): new ${(cmp.newKeys || []).map(x => x[0] + ' ' + x[1]).join(', ') || 'none'}; gone ${(cmp.goneKeys || []).map(x => x[0]).join(', ') || 'none'}; tags ${counts.tags || 0} (24,219 at 10:30); `
      + `catalog ${CK.notes} with files: (718): type outside ${CK.typeOutside.length}, status ${CK.statusOutside.length}, text ${CK.textOutside.length}, no valid subject ${CK.noValidSubject.length}, subject not folder ${CK.folderNotInSubject.length}; `
      + `outside the vocabularies (all notes): ${Object.entries(outside).map(([k, a]) => k + ' ' + a.length + ' values/' + a.reduce((x, e) => x + e.total, 0) + ' uses').join(', ')}; type values changed: ${((cmp.outsideVocabulary || {}).type || []).map(([v, a, b]) => v + ' ' + a + '→' + b).join(', ') || 'none'}; `
      + `mixed-type properties ${mixed.length} (11 at 10:30; new ${(cmp.mixedNew || []).join(', ') || 'none'}); pages as text ${forms.pages.length} (153); year ${forms.year.length}, date ${forms.date.length}, physical_copy ${forms.physical_copy.length} wrong; capitals ${Object.keys(upper).length}; `
      + `types.json mismatches ${Object.keys(declMismatch).length}; assigned-type conflicts ${Object.entries(assignedConflicts).map(([k, e]) => k + ' (' + e.type + ') ' + e.count).join(', ') || 'none'}`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
