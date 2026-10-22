(async () => {
  // Area M re-run, check 14 (19 Oct 2026, after Part 1): tags. Changed since 10:30 by the removal of the frontmatter `tags`
  // key from 24,156 machine-made notes (Texts/ except MUKTABODHA, Library/, Calendar/, Study/Sanskrit/, Catalog/).
  // Per tag, from Obsidian's cache (frontmatter tags/tag and inline tags): notes, uses, inline, frontmatter, notes in
  // Stephen's writing (Projects/, Journal/, Study/Concepts/, Study/Hubs/) and in machine-made notes, folders; Obsidian's own
  // getTags() totals; what is left in the removal's scope (frontmatter and inline, by folder); and whether any template,
  // view, Base, maintenance script or dataview/dataviewjs/tasks block relies on tags (lines that use a tags API or field,
  // and `#tag` tokens of every tag that exists now or existed at 10:30; every hit is listed so that false hits can be seen).
  // Compared with .work/out/areaM/check14-tags.json (whose per-tag numbers were counted from the text, so a small
  // difference in a tag that the removal did not touch is a difference of method).
  // Read-only: writes only .work/out/areaM2/tags.json. Memory guard 300 MB below the heap limit.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const NAME = 'tags', OUT = '.work/out/areaM2';
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const fk = p => { const s = p.split('/'); return s.length > 2 ? s[0] + '/' + s[1] : s.length === 2 ? s[0] + '/' : '(top level)'; };
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const R = { job: 'm2-14-tags', when: new Date().toISOString() };
  let line = '';
  try {
    const all = app.vault.getFiles(), md = app.vault.getMarkdownFiles();
    const writing = p => /^(Projects|Journal)\//.test(p) || /^Study\/(Concepts|Hubs)\//.test(p);
    const rec = await readJSON('.work/backup-tags-2026-10-19/removed-tags.json');
    const SCOPE = (rec && rec.scope) || ['Texts/', 'Library/', 'Calendar/', 'Study/Sanskrit/', 'Catalog/'], EXCL = (rec && rec.exclude) || ['Texts/MUKTABODHA'];
    const inScope = p => SCOPE.some(s => p.startsWith(s)) && !EXCL.some(s => p.startsWith(s));
    const T = {}; let usesFm = 0, usesInl = 0, notesWithTags = 0;
    const scopeLeft = { notes: 0, frontmatterNotes: [], inlineNotes: 0, inlineUses: 0, inlineByFolder: {}, inlineByTag: {}, inlineExamples: [] };
    let n = 0;
    for (const f of md) {
      const c = MC.getFileCache(f) || {}; const fm = c.frontmatter || {};
      const fmT = [];
      for (const k of ['tags', 'tag', 'Tags', 'Tag']) { const v = fm[k]; if (v === null || v === undefined) continue; for (const x of (Array.isArray(v) ? v : String(v).split(/[,\s]+/))) { const s = String(x === null || x === undefined ? '' : x).trim().replace(/^#/, ''); if (s) fmT.push(s); } }
      const inl = (c.tags || []).map(t => t.tag.replace(/^#/, ''));
      if (fmT.length || inl.length) notesWithTags++;
      const seen = new Set();
      for (const [arr, kind] of [[fmT, 'frontmatter'], [inl, 'inline']]) for (const t of arr) {
        const e = T[t] = T[t] || { tag: t, files: 0, uses: 0, inline: 0, frontmatter: 0, writingFiles: 0, machineFiles: 0, folders: {} };
        e.uses++; e[kind]++; if (kind === 'inline') usesInl++; else usesFm++;
        if (!seen.has(t)) { seen.add(t); e.files++; if (writing(f.path)) e.writingFiles++; else e.machineFiles++; inc(e.folders, fk(f.path)); }
      }
      if (inScope(f.path)) {
        scopeLeft.notes++;
        if (fmT.length) scopeLeft.frontmatterNotes.push([f.path, fmT.slice(0, 5)]);
        if (inl.length) { scopeLeft.inlineNotes++; scopeLeft.inlineUses += inl.length; inc(scopeLeft.inlineByFolder, fk(f.path)); for (const t of inl) inc(scopeLeft.inlineByTag, t); if (scopeLeft.inlineExamples.length < 30) scopeLeft.inlineExamples.push([f.path, inl.slice(0, 5)]); }
      }
      if (++n % 2000 === 0) { guard('tags ' + n); await new Promise(r => setTimeout(r, 0)); }
    }
    let gt = {}; try { gt = MC.getTags(); } catch (e) { gt = { error: String(e) }; }
    const list = Object.values(T).sort((a, b) => b.files - a.files);
    const caseGroups = {}; for (const e of list) (caseGroups[e.tag.toLowerCase()] = caseGroups[e.tag.toLowerCase()] || []).push(e.tag);
    const inWriting = list.filter(e => e.writingFiles), inMachine = list.filter(e => e.machineFiles);
    // what relies on tags: templates, views, Bases, scripts, and the query blocks in notes
    const sources = [];
    for (const f of all) {
      if ((f.path.startsWith('Templates/') && ['md', 'js', 'css', 'json'].includes(f.extension)) || f.extension === 'base') sources.push([f.path, f.path.startsWith('Templates/') ? 'template/view' : 'base', await app.vault.cachedRead(f)]);
      else if (f.path.startsWith('AI/Prompts/Scripts/') && ['js', 'py'].includes(f.extension)) sources.push([f.path, 'maintenance script', await app.vault.cachedRead(f)]);
    }
    const blockSeen = new Set(); let blockNotes = 0;
    for (const f of md) {
      const c = MC.getFileCache(f); if (!c || !(c.sections || []).some(s => s.type === 'code')) continue;
      blockNotes++; const t = await app.vault.cachedRead(f);
      for (const m of t.matchAll(/^(?:>\s?)*\s{0,3}(`{3,}|~{3,})\s*(dataview|dataviewjs|tasks|base)\s*\r?\n([\s\S]*?)\r?\n(?:>\s?)*\s{0,3}\1\s*$/gim)) { const k = m[2].toLowerCase() + '\u0000' + m[3].trim(); if (blockSeen.has(k)) continue; blockSeen.add(k); sources.push([f.path, m[2].toLowerCase() + ' block', m[3]]); }
      if (blockNotes % 500 === 0) guard('blocks ' + blockNotes);
    }
    const API = /\bfile\.e?tags\b|\.tags\b|\btags?\s*(?:==|!=|\.includes|\.contains|\)|,)|\bcontains\(\s*(?:file\.)?tags|\btaggedWith\b|\bhasTag\b|getAllTags|getTags\s*\(|^\s*(?:tags?|tag)\s+(?:include|includes|do not include|does not include)\b|\bFROM\s+#/i;
    const apiHits = [];
    const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const old = await readJSON('.work/out/areaM/check14-tags.json');
    const tagUnion = [...new Set([...list.map(e => e.tag), ...((old && old.all) || []).map(e => e.tag)])];
    const tagRes = tagUnion.map(t => [t, new RegExp('(?<![\\w#/&])#' + esc(t) + '(?![\\w/-])')]);
    const tagHits = {};
    for (const [p, kind, t] of sources) {
      t.split(/\r?\n/).forEach((L, i) => { if (L.length <= 2000 && API.test(L) && apiHits.length < 400) apiHits.push([p, kind, i + 1, L.trim().slice(0, 160)]); });
      for (const [tag, re] of tagRes) { if (re.test(t)) (tagHits[tag] = tagHits[tag] || []).push([p, kind]); }
    }
    guard('sources');
    // against 10:30
    const cmp = {};
    if (old) {
      const oa = Object.fromEntries((old.all || []).map(e => [e.tag, e]));
      cmp.totals1030 = old.totals;
      cmp.gone = (old.all || []).filter(e => !T[e.tag]).map(e => [e.tag, e.files, e.frontmatter, e.inline]);
      cmp.new = list.filter(e => !oa[e.tag]).map(e => [e.tag, e.files, e.frontmatter, e.inline]);
      cmp.changed = list.filter(e => oa[e.tag] && (oa[e.tag].files !== e.files || oa[e.tag].frontmatter !== e.frontmatter || oa[e.tag].inline !== e.inline)).map(e => ({ tag: e.tag, files: [oa[e.tag].files, e.files], frontmatter: [oa[e.tag].frontmatter, e.frontmatter], inline: [oa[e.tag].inline, e.inline] }));
      const ow = (old.tagsInMyWriting || []).map(e => e.tag); cmp.writingTags1030 = ow.length; cmp.writingTagsGone = ow.filter(t => !inWriting.some(e => e.tag === t)); cmp.writingTagsNew = inWriting.map(e => e.tag).filter(t => !ow.includes(t));
    } else cmp.error = 'check14-tags.json not readable';
    R.totals = { distinctTags: list.length, distinctIgnoringCase: Object.keys(caseGroups).length, uses: usesFm + usesInl, frontmatterUses: usesFm, inlineUses: usesInl, notesWithTags,
      obsidianGetTagsDistinct: Object.keys(gt).length, obsidianGetTagsUses: Object.values(gt).reduce((a, b) => a + (typeof b === 'number' ? b : 0), 0) };
    R.caseVariants = Object.values(caseGroups).filter(a => a.length > 1);
    R.tagsInMyWriting = inWriting; R.tagsInMachineMadeNotes = inMachine; R.onlyInMyWriting = inWriting.filter(e => !e.machineFiles).map(e => e.tag); R.onlyInMachineNotes = inMachine.filter(e => !e.writingFiles).map(e => e.tag);
    R.removalScopeNow = { ...scopeLeft, frontmatterNotesCount: scopeLeft.frontmatterNotes.length, frontmatterNotes: scopeLeft.frontmatterNotes.slice(0, 200) };
    R.usedBy = { sourcesSearched: sources.length, byKind: sources.reduce((o, s) => (inc(o, s[1]), o), {}), tagApiLines: apiHits, tagsOfNowOr1030NamedInSources: tagHits };
    R.all = list; R.against1030 = cmp;
    line = `tags: ${list.length} distinct (${Object.keys(caseGroups).length} ignoring case; 229/220 at 10:30, counted from the text), ${usesFm + usesInl} uses (frontmatter ${usesFm}, inline ${usesInl}) in ${notesWithTags} notes; Obsidian getTags ${R.totals.obsidianGetTagsDistinct} / ${R.totals.obsidianGetTagsUses} (218 / 69,382 at 10:30); `
      + `writing ${inWriting.length} tags (59), machine-made ${inMachine.length} (179); gone ${(cmp.gone || []).length}, new ${(cmp.new || []).length} (${(cmp.new || []).slice(0, 8).map(x => x[0]).join(', ')}); `
      + `removal scope now: ${scopeLeft.notes} notes, frontmatter tags in ${scopeLeft.frontmatterNotes.length}, inline tags in ${scopeLeft.inlineNotes} (${scopeLeft.inlineUses} uses; ${Object.entries(scopeLeft.inlineByFolder).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => k + ' ' + v).join(', ')}); `
      + `relying on tags: ${sources.length} sources searched, ${apiHits.length} tag-API lines, ${Object.keys(tagHits).length} tags (now or 10:30) named as #tag (${Object.keys(tagHits).slice(0, 8).join(', ')})`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
