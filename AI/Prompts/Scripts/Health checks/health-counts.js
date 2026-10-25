(async () => {
  // Phase 8, step 1: vault health assessment, read-only (AI/Prompts/Vault health assessment.md, areas 1-6, 8-10, plus the
  // Guide/Welcome path check). Writes .work/out/health-<date>b.json (the run's local date). Changes nothing. Memory guard: stops 300 MB below the limit.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now(), R = { when: new Date().toISOString() };
  const LIM = performance.memory.jsHeapSizeLimit, heap = () => performance.memory.usedJSHeapSize;
  const GUARD = LIM - 300e6; let peak = heap();
  const guard = where => { const h = heap(); if (h > peak) peak = h; if (h > GUARD) throw new Error('memory guard at ' + where + ': ' + Math.round(h / 1e6) + ' MB'); };
  const files = app.vault.getFiles(), md = app.vault.getMarkdownFiles();
  const folders = app.vault.getAllLoadedFiles().filter(f => f.children);
  const fmOf = f => ((MC.getFileCache(f) || {}).frontmatter) || {};
  const top = p => p.includes('/') ? p.split('/')[0] : '(top)';
  // 1. counts
  R.counts = { files: files.length, notes: md.length, folders: folders.length };
  const nt = {}; for (const f of md) nt[top(f.path)] = (nt[top(f.path)] || 0) + 1; R.notesByTop = nt;
  // 2. links
  const un = Object.entries(MC.unresolvedLinks).filter(([, m]) => Object.keys(m).length);
  R.unresolved = un.map(([s, m]) => [s, m]);
  const badSub = []; let subLinks = 0;
  for (const f of md) {
    const c = MC.getFileCache(f); if (!c) continue;
    for (const l of [...(c.links || []), ...(c.embeds || [])]) {
      const i = l.link.indexOf('#'); if (i < 0) continue; subLinks++;
      const name = l.link.slice(0, i), sub = l.link.slice(i + 1);
      const t = name ? MC.getFirstLinkpathDest(name, f.path) : f; if (!t || t.extension !== 'md') continue;
      const tc = MC.getFileCache(t) || {};
      if (sub.startsWith('^')) { if (!(tc.blocks || {})[sub.slice(1).toLowerCase()]) badSub.push([f.path, l.link]); }
      else { const h = sub.split('#').pop().toLowerCase().replace(/\s+/g, ' ').trim(); if (!(tc.headings || []).some(x => x.heading.toLowerCase().replace(/\s+/g, ' ').trim() === h)) badSub.push([f.path, l.link]); }
    }
  }
  guard('links');
  R.subpathLinks = subLinks; R.badSubpaths = badSub.slice(0, 500); R.badSubpathCount = badSub.length;
  const byBase = {}; for (const f of md) (byBase[f.basename.toLowerCase()] = byBase[f.basename.toLowerCase()] || []).push(f.path);
  R.ambiguousNames = Object.values(byBase).filter(v => v.length > 1);
  // embeds of missing files (non-md targets) are in unresolvedLinks; list the embed ones separately
  const embMissing = [];
  for (const f of md) { const c = MC.getFileCache(f); if (!c || !c.embeds) continue; for (const e of c.embeds) { const n = e.link.split('#')[0]; if (!n) continue; if (!MC.getFirstLinkpathDest(n, f.path)) embMissing.push([f.path, e.link]); } }
  R.embedsMissing = embMissing.slice(0, 200);
  // 3. catalog
  const SUBJ = ['Trika', 'Judaica', 'Christianity', 'Philosophy', 'Sanskrit-Study', 'Hinduism', 'Biblical-Studies', 'Other'];
  const TYPES = ['book', 'article', 'chapter', 'thesis', 'collection', 'multi-volume-set', 'text', 'other']; // 'text' added 14 Oct 2026 (audit K-08)
  const TEXT = ['searchable', 'scan', 'print'], STATUS = [null, 'reading', 'review', 'delete'];
  const catNotes = md.filter(f => /^Catalog\/[^/]+\/[^/]+\.md$/.test(f.path) && !f.path.startsWith('Catalog/Scholars/') && f.basename !== f.parent.name);
  const linkedBy = {}; const badFileLinks = []; const propProblems = []; const review = [], scan = [], printOnly = [], subjMismatch = [], noFiles = [];
  const isList = v => Array.isArray(v);
  for (const f of catNotes) {
    const fm = fmOf(f); const folderSubj = f.path.split('/')[1];
    const fl = [].concat(fm.files || []).filter(x => x !== null && x !== undefined && x !== '');
    for (const v of fl) { const m = String(v).match(/\[\[([^\]|#]+)/); const name = m ? m[1] : String(v); const t = MC.getFirstLinkpathDest(name, f.path); if (t) (linkedBy[t.path] = linkedBy[t.path] || []).push(f.path); else badFileLinks.push([f.path, String(v)]); }
    const pb = [];
    if (fm.year !== undefined && fm.year !== null && fm.year !== '' && typeof fm.year !== 'number') pb.push('year:' + JSON.stringify(fm.year));
    if (fm.pages !== undefined && fm.pages !== null && fm.pages !== '' && typeof fm.pages !== 'number') pb.push('pages:' + JSON.stringify(fm.pages));
    const sj = [].concat(fm.subject || []); if (!sj.length) pb.push('subject:empty'); if (sj.length && !SUBJ.includes(sj[0])) pb.push('subject:' + JSON.stringify(sj));
    if (fm.subject !== undefined && !isList(fm.subject)) pb.push('subject-not-list');
    if (fm.type !== undefined && !TYPES.includes(fm.type)) pb.push('type:' + JSON.stringify(fm.type));
    if (fm.text !== undefined && !TEXT.includes(fm.text)) pb.push('text:' + JSON.stringify(fm.text));
    if (fm.status !== undefined && !STATUS.includes(fm.status)) pb.push('status:' + JSON.stringify(fm.status));
    if (fm.author !== undefined && fm.author !== null && !isList(fm.author)) pb.push('author-not-list');
    if (fm.language !== undefined && fm.language !== null && !isList(fm.language)) pb.push('language-not-list');
    if (fm.print !== undefined && typeof fm.print !== 'boolean') pb.push('print:' + JSON.stringify(fm.print));
    if (fm.title === undefined || fm.title === null || fm.title === '') pb.push('title:empty');
    if (pb.length) propProblems.push([f.path, pb]);
    if (fm.status === 'review') review.push(f.path);
    if (fm.text === 'scan') scan.push(f.path);
    if (fm.text === 'print') { printOnly.push(f.path); if (fl.length) pb.push('print-with-files'); }
    else if (!fl.length) noFiles.push(f.path);
    if (SUBJ.includes(folderSubj) && !sj.includes(folderSubj)) subjMismatch.push([f.path, sj]);
  }
  guard('catalog');
  const libFiles = files.filter(f => f.path.startsWith('Library/') && ['pdf', 'djvu', 'epub', 'mobi', 'docx', 'doc'].includes(f.extension));
  const libNotLinked = libFiles.filter(f => !linkedBy[f.path]).map(f => f.path);
  const libMulti = libFiles.filter(f => (linkedBy[f.path] || []).length > 1).map(f => [f.path, linkedBy[f.path]]);
  // converted index notes: md in Library/<...>/<X>/<X>.md
  const idxNotes = md.filter(f => f.path.startsWith('Library/') && f.parent && f.basename === f.parent.name && (fmOf(f).type === 'book' || fmOf(f).source_pdf));
  const idxNotLinked = idxNotes.filter(f => !linkedBy[f.path]).map(f => f.path);
  // converted notes whose source_pdf is missing
  const srcMissing = []; const conv = md.filter(f => f.path.startsWith('Library/') && fmOf(f).source_pdf);
  const seenSrc = {}; for (const f of conv) { const s = String(fmOf(f).source_pdf); if (seenSrc[s] !== undefined) continue; seenSrc[s] = !!app.vault.getAbstractFileByPath(s); if (!seenSrc[s]) srcMissing.push([s, f.path]); }
  R.catalog = { notes: catNotes.length, badFileLinks, libraryFiles: libFiles.length, libraryNotLinked: libNotLinked, libraryLinkedTwice: libMulti, convertedIndexNotes: idxNotes.length, convertedIndexNotLinked: idxNotLinked, convertedNotes: conv.length, sourcePdfMissing: srcMissing.slice(0, 100), propertyProblems: propProblems, review, scan: scan.length, scanList: scan, printOnly, noFilesAndNotPrint: noFiles, subjectFolderMismatch: subjMismatch };
  guard('catalog2');
  // 4. names
  const allowNonAscii = p => p.startsWith('Library/Lexicons/');
  R.names = {
    nonAscii: files.filter(f => /[^\x00-\x7F]/.test(f.path) && !allowNonAscii(f.path)).map(f => f.path).slice(0, 300),
    nonAsciiFolders: folders.filter(f => /[^\x00-\x7F]/.test(f.path) && !allowNonAscii(f.path)).map(f => f.path),
    badChars: files.filter(f => /[\[\]#^|:*?"<>\\]/.test(f.name)).map(f => f.path).slice(0, 300),
    endings: files.filter(f => / \(\d\)\.| copy\.| copy \d+\./.test(f.name)).map(f => f.path),
    doubleSpaces: files.filter(f => /  /.test(f.path)).map(f => f.path),
    spaceBeforeExtension: files.filter(f => / \.[a-z0-9]+$/i.test(f.name)).map(f => f.path),
    longPaths: files.filter(f => ('C:/Vaults/Obsidian Vault/' + f.path).length > 240).map(f => [f.path, ('C:/Vaults/Obsidian Vault/' + f.path).length])
  };
  // 5. properties
  const pn = {}; for (const f of md) for (const k of Object.keys(fmOf(f))) { const l = k.toLowerCase(); (pn[l] = pn[l] || {}); pn[l][k] = (pn[l][k] || 0) + 1; }
  R.propertyCaseConflicts = Object.values(pn).filter(s => Object.keys(s).length > 1);
  let types = {}; let props = {};
  try { const M = app.metadataTypeManager; types = Object.assign({}, M.types || {}); props = M.getAllProperties ? M.getAllProperties() : (M.properties || {}); } catch (e) { R.typeManagerError = String(e); }
  R.propertyTypes = Object.fromEntries(Object.entries(props).map(([k, v]) => [k, { type: v.type, count: v.count }]));
  const tc = {};
  for (const f of md) { const fm = fmOf(f); for (const [k, v] of Object.entries(fm)) {
    if (v === null || v === undefined || v === '') continue;
    const t = (types[k.toLowerCase()] || (props[k.toLowerCase()] || {}).type); if (!t) continue;
    let bad = false;
    if (t === 'number') bad = typeof v !== 'number';
    else if (t === 'checkbox') bad = typeof v !== 'boolean';
    else if (t === 'date') bad = !(typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v));
    else if (t === 'datetime') bad = !(typeof v === 'string' && /^\d{4}-\d{2}-\d{2}/.test(v));
    else if (t === 'multitext' || t === 'tags' || t === 'aliases') bad = !Array.isArray(v) && typeof v !== 'string';
    else if (t === 'text') bad = typeof v === 'object';
    if (bad) { (tc[k] = tc[k] || { type: t, count: 0, examples: [] }); tc[k].count++; if (tc[k].examples.length < 5) tc[k].examples.push([f.path, JSON.stringify(v).slice(0, 60)]); }
  } }
  R.propertyTypeConflicts = tc;
  guard('properties');
  // 6. empty notes, empty folders, orphans
  R.emptyNotes = md.filter(f => f.stat.size < 40).map(f => [f.path, f.stat.size]).slice(0, 300);
  R.titleOnlyNotes = md.filter(f => f.stat.size < 400 && !f.path.startsWith('Journal/') && !f.path.startsWith('Library/Lexicons/')).map(f => [f.path, f.stat.size]).slice(0, 300);
  R.emptyFolders = folders.filter(f => f.children.length === 0).map(f => f.path);
  const linked = new Set(); for (const m of Object.values(MC.resolvedLinks)) for (const t of Object.keys(m)) linked.add(t);
  R.orphanFiles = files.filter(f => f.extension !== 'md' && !f.path.startsWith('Library/') && !f.path.startsWith('Templates/') && !f.path.startsWith('Journal/') && !f.path.startsWith('Projects/') && !f.path.startsWith('Texts/MUKTABODHA') && !linked.has(f.path)).map(f => [f.path, f.stat.size]).slice(0, 400);
  R.orphanNotes = md.filter(f => !linked.has(f.path) && !Object.keys(MC.resolvedLinks[f.path] || {}).length && !f.path.startsWith('Library/') && !f.path.startsWith('Texts/') && !f.path.startsWith('Journal/') && !f.path.startsWith('Templates/') && !f.path.startsWith('AI/')).map(f => f.path).slice(0, 200);
  R.topLevel = app.vault.getRoot().children.map(f => f.path + (f.children ? '/' : ''));
  R.testLike = md.filter(f => /\b(test|sample|scratch|untitled|fixture|copy|tmp|temp)\b/i.test(f.basename) || ['test', 'sample', 'fixture'].includes(fmOf(f).type)).map(f => f.path).slice(0, 200);
  R.jsOutsideViews = files.filter(f => f.extension === 'js' && !f.path.startsWith('Templates/Views/') && !f.path.startsWith('AI/Prompts/Scripts/')).map(f => f.path);
  R.claudeOutputFolders = folders.filter(f => /claude outputs|_work|scratch/i.test(f.name)).map(f => f.path);
  R.zipFiles = files.filter(f => ['zip', 'rar', '7z', 'tar', 'gz'].includes(f.extension)).map(f => f.path);
  R.attachmentsFolders = folders.filter(f => /^(Attachments|_images)$/i.test(f.name)).map(f => [f.path, f.children.length]);
  // 8. size
  const ext = {}, tops = {}; let total = 0; const extN = {};
  for (const f of files) { const s = f.stat.size; total += s; const e = (f.extension || '').toLowerCase(); ext[e] = (ext[e] || 0) + s; extN[e] = (extN[e] || 0) + 1; const t = top(f.path); tops[t] = (tops[t] || 0) + s; }
  R.size = { total, byExt: Object.entries(ext).sort((a, b) => b[1] - a[1]).slice(0, 25).map(([e, s]) => [e, s, extN[e]]), byTop: Object.entries(tops).sort((a, b) => b[1] - a[1]) };
  // by top folder without PDFs (for Sync)
  const topsNoPdf = {}; for (const f of files) { if (f.extension === 'pdf') continue; const t = top(f.path); topsNoPdf[t] = (topsNoPdf[t] || 0) + f.stat.size; } R.size.byTopNoPdf = Object.entries(topsNoPdf).sort((a, b) => b[1] - a[1]);
  const sub2 = {}; for (const f of files) { if (f.extension === 'pdf') continue; const parts = f.path.split('/'); const k = parts.length > 2 ? parts[0] + '/' + parts[1] : parts[0]; sub2[k] = (sub2[k] || 0) + f.stat.size; } R.size.bySecondNoPdf = Object.entries(sub2).sort((a, b) => b[1] - a[1]).slice(0, 40);
  R.largest = files.slice().sort((a, b) => b.stat.size - a.stat.size).slice(0, 25).map(f => [f.path, f.stat.size]);
  R.over5MB = files.filter(f => f.stat.size > 5e6).length; R.over5MBnoPdf = files.filter(f => f.stat.size > 5e6 && f.extension !== 'pdf').map(f => [f.path, f.stat.size]); R.over200MB = files.filter(f => f.stat.size > 200e6).map(f => f.path);
  R.largestNotes = md.slice().sort((a, b) => b.stat.size - a.stat.size).slice(0, 20).map(f => [f.path, f.stat.size]);
  const dirSize = async p => { let n = 0, b = 0; try { const L = await ad.list(p); for (const x of L.files) { n++; const s = await ad.stat(x); b += s ? s.size : 0; } for (const d of L.folders) { const r = await dirSize(d); n += r[0]; b += r[1]; } } catch (e) {} return [n, b]; };
  R.hidden = {}; for (const p of ['.trash', '.work', '.smart-env', '.obsidian']) R.hidden[p] = await dirSize(p);
  try { const L = await ad.list('.work'); R.workFolders = []; for (const d of L.folders) R.workFolders.push([d, ...(await dirSize(d))]); } catch (e) {}
  guard('size');
  // 10. bloat: notes per folder (depth 2) and how much they are used (inbound links from outside the folder)
  const grp = {}; for (const f of md) { const parts = f.path.split('/'); const k = parts.length > 2 ? parts[0] + '/' + parts[1] : parts[0]; (grp[k] = grp[k] || { notes: 0, bytes: 0, inbound: 0 }); grp[k].notes++; grp[k].bytes += f.stat.size; }
  for (const [src, m] of Object.entries(MC.resolvedLinks)) { const sp = src.split('/'); const sk = sp.length > 2 ? sp[0] + '/' + sp[1] : sp[0]; for (const [t, n] of Object.entries(m)) { const tp = t.split('/'); const tk = tp.length > 2 ? tp[0] + '/' + tp[1] : tp[0]; if (tk !== sk && grp[tk]) grp[tk].inbound += n; } }
  R.folderUse = Object.entries(grp).sort((a, b) => b[1].notes - a[1].notes).slice(0, 60);
  // tags
  try { R.tags = Object.entries(MC.getTags()).sort((a, b) => b[1] - a[1]).slice(0, 60); } catch (e) { R.tags = String(e); }
  // bases
  R.bases = files.filter(f => f.extension === 'base').map(f => [f.path, f.stat.size, linked.has(f.path)]);
  // templates and views
  R.templates = md.filter(f => f.path.startsWith('Templates/') && !f.path.startsWith('Templates/Views/')).map(f => f.path);
  R.views = folders.filter(f => f.path.startsWith('Templates/Views/') && f.path.split('/').length === 3).map(f => [f.path, f.children.map(c => c.name)]);
  // byte-identical candidates among non-md files > 20 KB
  const bySize = {}; for (const f of files) if (f.extension !== 'md' && f.stat.size > 20000) (bySize[f.stat.size] = bySize[f.stat.size] || []).push(f);
  const dupSets = []; let hashed = 0, stopped = null;
  for (const g of Object.values(bySize)) {
    if (g.length < 2) continue;
    if (g[0].stat.size > 150e6) { dupSets.push({ size: g[0].stat.size, files: g.map(f => f.path), note: 'same size, not hashed (>150 MB)' }); continue; }
    if (heap() > GUARD - 200e6) { stopped = 'memory'; break; }
    const hs = {};
    for (const f of g) { const buf = await ad.readBinary(f.path); const h = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', buf))).slice(0, 12).map(b => b.toString(16).padStart(2, '0')).join(''); (hs[h] = hs[h] || []).push(f.path); hashed++; }
    for (const v of Object.values(hs)) if (v.length > 1) dupSets.push({ size: g[0].stat.size, files: v });
  }
  R.identical = dupSets; R.identicalHashed = hashed; R.identicalStopped = stopped;
  // same-size md notes (> 2 KB) as duplicate candidates
  const mdBySize = {}; for (const f of md) if (f.stat.size > 2000) (mdBySize[f.stat.size] = mdBySize[f.stat.size] || []).push(f.path);
  R.mdSameSize = Object.values(mdBySize).filter(v => v.length > 1).slice(0, 100);
  guard('dups');
  // Guide and Welcome: every backtick path and [[link]] checked
  const gw = {};
  for (const p of ['Vault Guide.md', 'Welcome to the vault.md', 'AI/Prompts/Prompts - read me.md', 'AI/Prompts/House rules for AI work.md']) {
    const t = await ad.read(p); const miss = [];
    for (const m of t.matchAll(/`((?:Texts|Library|Catalog|Study|Projects|Journal|Notes|AI|Templates|Calendar|Excalidraw)\/[^`]*)`/g)) { const q = m[1].replace(/\/$/, '').replace(/\/\*\*$/, ''); if (/[<>*…]/.test(q)) continue; if (!(await ad.exists(q)) && !(await ad.exists(q + '.md'))) miss.push('path: ' + m[1]); }
    for (const m of t.matchAll(/\[\[([^\]|#]+)/g)) { const n = m[1].replace(/\\$/, ''); if (/[<>]/.test(n) || n.length > 120) continue; if (!MC.getFirstLinkpathDest(n, p)) miss.push('link: ' + n); }
    gw[p] = miss;
  }
  R.guideWelcomeMissing = gw;
  R.prompts = md.filter(f => f.path.startsWith('AI/Prompts/') && !f.path.includes('/Scripts/')).map(f => f.path);
  // plugins
  try { R.plugins = { enabled: Object.keys(app.plugins.plugins), manifests: Object.keys(app.plugins.manifests), core: Object.entries(app.internalPlugins.plugins).filter(([k, v]) => v.enabled).map(([k]) => k) }; } catch (e) { R.plugins = String(e); }
  R.seconds = Math.round((Date.now() - T0) / 1000); R.peakHeapMB = Math.round(peak / 1e6); R.heapLimitMB = Math.round(LIM / 1e6);
  await ad.write('.work/out/health-' + new Date().toLocaleDateString('sv') + 'b.json', JSON.stringify(R, null, 1));
  return `read-only: files ${R.counts.files}, notes ${R.counts.notes}, folders ${R.counts.folders}; unresolved files ${un.length}; bad #subpaths ${R.badSubpathCount} of ${subLinks}; ambiguous ${R.ambiguousNames.length}; catalog notes ${catNotes.length}, bad files: links ${badFileLinks.length}, library not linked ${libNotLinked.length}, twice ${libMulti.length}, idx not linked ${idxNotLinked.length}, prop problems ${propProblems.length}, review ${review.length}, scan ${scan.length}; type conflicts ${Object.keys(tc).length}; identical ${dupSets.length} (hashed ${hashed}${stopped ? ' stopped' : ''}); ${R.seconds}s, peak ${R.peakHeapMB} MB`;
})()
