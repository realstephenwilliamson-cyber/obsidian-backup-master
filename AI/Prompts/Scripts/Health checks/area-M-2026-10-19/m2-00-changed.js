(async () => {
  // Area M re-run, job 0 (19 Oct 2026, after Part 1): what changed since the 10:30 EDT pre-run, and the evidence that
  // checks 3 (footnotes), 4 (page markers), 5 (catalog), 6 (near-empty notes) and 9 (unlinked attachments) were not
  // changed by Part 1's writes, so they are not re-run.
  //  (a) every vault file created or modified since 10:30 EDT (stat ctime/mtime), matched against the record: the tags
  //      record (.work/backup-tags-2026-10-19/removed-tags.json), the edit specs in .work/edits/ written since 10:30,
  //      the new files of record items 4, 10, 12 and the replaced files; anything else is listed as UNEXPLAINED;
  //  (b) every note backed up by Part 1 (.work/backup-completion-2026-10-19, .work/backup-fable-2026-10-19) compared
  //      with the note now, feature by feature: frontmatter keys and values, links, headings, block ids, footnote
  //      labels, page-marker lines, inline tags, code blocks, attachment links;
  //  (c) the same features counted in the notes created since 10:30;
  //  (d) check 5: Library files by extension against 10:30, the catalog `files:` entries re-resolved;
  //      check 6: the 12 near-empty notes of 10:30 re-measured and every changed note measured;
  //      check 9: attachments outside Library linked by any note (resolved links), against the 21 of 10:30.
  // Read-only: writes only .work/out/areaM2/changed.json. Memory guard 300 MB below the heap limit.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const NAME = 'changed', OUT = '.work/out/areaM2', CUTOFF = Date.parse('2026-10-19T14:30:00Z');
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const iso = t => new Date(t).toISOString();
  const fk = p => { const s = p.split('/'); return s.length > 2 ? s[0] + '/' + s[1] : s.length === 2 ? s[0] + '/' : '(top level)'; };
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const cap = (a, n = 40) => a.length > n ? a.slice(0, n).concat([`… ${a.length - n} more`]) : a;
  const listAll = async dir => { const out = []; const walk = async d => { let L; try { L = await ad.list(d); } catch (e) { return; } out.push(...L.files); for (const s of L.folders) await walk(s); }; if (await ad.exists(dir)) await walk(dir); return out; };
  const R = { job: 'm2-00-changed', when: iso(Date.now()), cutoff: iso(CUTOFF) + ' (10:30 EDT)' };
  let line = '';
  // features of a note's text (fenced code is skipped except for its language)
  const feat = t => {
    const lines = t.replace(/^﻿/, '').split(/\r?\n/);
    const F = { fmKeys: [], fmVals: {}, links: [], headings: [], blocks: [], fnRefs: [], fnDefs: [], markers: [], tags: [], fences: [], attach: [], bodyLen: 0 };
    let end = -1;
    if (lines[0] === '---') for (let i = 1; i < lines.length; i++) if (lines[i].trimEnd() === '---') { end = i; break; }
    let cur = null;
    for (let i = 1; i < end; i++) { const L = lines[i]; const m = L.match(/^([^\s#-][^:]*?):(\s|$)/); if (m) { cur = m[1]; F.fmKeys.push(cur); F.fmVals[cur] = L; } else if (cur) F.fmVals[cur] += '\n' + L; }
    F.bodyLen = lines.slice(end + 1).join('\n').trim().length;
    let fence = null;
    for (let i = end + 1; i < lines.length; i++) {
      const L = lines[i];
      const fo = L.match(/^(?:>\s?)*\s{0,3}(`{3,}|~{3,})\s*([^\s`]*)/);
      if (fo) {
        if (!fence) { fence = fo[1]; F.fences.push(fo[2] || '(none)'); continue; }
        if (fo[1][0] === fence[0] && fo[1].length >= fence.length && !fo[2]) { fence = null; continue; }
      }
      if (fence) continue;
      if (/^#{1,6}\s/.test(L)) F.headings.push(L.trimEnd());
      const bm = L.match(/(?:^|\s)\^([A-Za-z0-9-]+)\s*$/); if (bm) F.blocks.push(bm[1]);
      if (/^\[p\. [^\]]*\] \^pg\d+\s*$/.test(L)) F.markers.push(L.trimEnd() + ((lines[i + 1] || '').trim() === '' ? '' : '  [NOT followed by a blank line]'));
      const nc = L.replace(/`[^`]*`/g, '');
      for (const m of nc.matchAll(/(!?)\[\[([^\]|]+)(?:\|[^\]]*)?\]\]/g)) F.links.push(m[1] + m[2]);
      for (const m of nc.matchAll(/\]\(([^)\s]+)\)/g)) if (!/^[a-z][a-z0-9+.-]*:/i.test(m[1])) F.links.push('md:' + m[1]);
      for (const m of nc.matchAll(/\[\^([^\]\s]+)\](:?)/g)) ((m[2] && m.index === nc.search(/\S/)) ? F.fnDefs : F.fnRefs).push(m[1]);
      for (const m of nc.matchAll(/(?:^|\s)#([^\s#.,;:!?"'`()[\]{}<>|\\*=+~]+)/g)) if (!/^\d+$/.test(m[1])) F.tags.push(m[1]);
    }
    F.attach = F.links.filter(x => /\.(png|jpe?g|gif|svg|webp|pdf|docx?|pptx?|xlsx?|txt|mp3|mp4|m4a|wav|djvu|epub)(#.*)?$/i.test(x.replace(/^!|^md:/, '')));
    return F;
  };
  const msDiff = (a, b) => { const m = new Map(); for (const x of a) m.set(x, (m.get(x) || 0) + 1); for (const x of b) m.set(x, (m.get(x) || 0) - 1); const removed = [], added = []; for (const [k, n] of m) { for (let i = 0; i < n; i++) removed.push(k); for (let i = 0; i < -n; i++) added.push(k); } return { removed, added }; };
  const FEATS = ['fmKeys', 'links', 'headings', 'blocks', 'fnRefs', 'fnDefs', 'markers', 'tags', 'fences', 'attach'];
  const CHECKS = { fmKeys: '1, 8', fmVals: '1, 8', links: '2', headings: '2 (targets)', blocks: '2 (targets)', fnRefs: '3', fnDefs: '3', markers: '4', tags: '14', fences: '13', attach: '9' };
  try {
    const files = app.vault.getFiles(), md = app.vault.getMarkdownFiles();
    const folders = app.vault.getAllLoadedFiles().filter(f => f.children); // as health-counts (root included), for comparison with 984
    R.counts = { now: { files: files.length, notes: md.length, folders: folders.length }, at1030: { files: 34062, notes: 31537, folders: 984 },
      expectedNewFromRecord: { files: 119, notes: 116, folders: 3, note: '2 scholar pages, CIS study plan, scratchpad, 108 card notes, 4 CIS chapter-card notes (notes); today-items/view.js, Habits.base, Flashcards.base; folders Templates/Views/today-items, Study/Sanskrit/Flashcards, Study/Sanskrit/CIS cards' } };
    R.counts.delta = { files: files.length - 34062, notes: md.length - 31537, folders: folders.length - 984 };
    // (a) the record
    const rec = await readJSON('.work/backup-tags-2026-10-19/removed-tags.json');
    const tagNotes = new Set(rec && rec.removed ? Object.keys(rec.removed) : []);
    R.tagsRecord = rec ? { notes: tagNotes.size, when: rec.when, dry: rec.dry, scope: rec.scope, exclude: rec.exclude } : 'removed-tags.json not found';
    const specNotes = {}; R.specs = {};
    let edFiles = []; try { edFiles = (await ad.list('.work/edits')).files.filter(p => p.endsWith('.json')); } catch (e) { R.specs.error = 'no .work/edits'; }
    for (const p of edFiles.sort()) {
      const st = await ad.stat(p); if (!st || st.mtime < CUTOFF) continue;
      const s = await readJSON(p); const nm = p.split('/').pop().replace(/\.json$/, '');
      if (!s || !s.edits) { R.specs[nm] = 'no edits key'; continue; }
      let n = 0; for (const [path, list] of Object.entries(s.edits)) { (specNotes[path] = specNotes[path] || []).push(nm); n += Array.isArray(list) ? list.length : 0; }
      R.specs[nm] = { notes: Object.keys(s.edits).length, editEntries: n, backup: s.backup, written: iso(st.mtime) };
    }
    const NEW_RE = [
      [/^Catalog\/Scholars\/(M\. V\. Patwardhan|Ernst Furlinger)\.md$/, 'scholar page (item 4)'],
      [/^Study\/Sanskrit\/CIS study plan\.md$/, 'CIS study plan (item 10)'],
      [/^Templates\/Views\/today-items\/view\.js$/, 'today-items view (item 10)'],
      [/^Excalidraw\/Sanskrit scratchpad\.excalidraw\.md$/, 'scratchpad (item 10)'],
      [/^Journal\/Habits\.base$/, 'Habits.base (item 10)'],
      [/^Study\/Sanskrit\/Flashcards\/Flashcards\.base$/, 'Flashcards.base (item 10)'],
      [/^Study\/Sanskrit\/Flashcards\/Card \d{3} [^/]+\.md$/, 'card note (item 12)'],
      [/^Study\/Sanskrit\/CIS cards\/CIS Ch\. [0-9a-z]+ cards\.md$/, 'CIS chapter cards (item 12)']];
    const REPLACED = new Set(['Templates/Daily note.md', 'Templates/Weekly note.md', 'AI/Prompts/Completion and final audit (Oct 2026).md', 'AI/AI log.md']);
    const changed = files.filter(f => f.stat.mtime >= CUTOFF || f.stat.ctime >= CUTOFF);
    const why = {}, byFolder = {}, unexplained = [], seenNew = {};
    for (const f of changed) {
      const r = [];
      if (tagNotes.has(f.path)) r.push('tags');
      if (specNotes[f.path]) r.push(...specNotes[f.path]);
      const ne = NEW_RE.find(([re]) => re.test(f.path)); if (ne) { r.push('new'); inc(seenNew, ne[1]); }
      if (REPLACED.has(f.path)) r.push('replaced/log');
      inc(why, r.length ? r.join('+') : 'UNEXPLAINED');
      const b = byFolder[fk(f.path)] = byFolder[fk(f.path)] || { changed: 0, unexplained: 0 }; b.changed++;
      if (!r.length) { b.unexplained++; unexplained.push({ p: f.path, size: f.stat.size, ctime: iso(f.stat.ctime), mtime: iso(f.stat.mtime) }); }
    }
    const notNow = p => { const f = app.vault.getAbstractFileByPath(p); return !f ? 'missing' : f.stat.mtime < CUTOFF ? 'not modified since 10:30' : null; };
    const tagNotChanged = [...tagNotes].map(p => [p, notNow(p)]).filter(x => x[1]);
    const specNotChanged = Object.keys(specNotes).map(p => [p, notNow(p), specNotes[p].join('+')]).filter(x => x[1]);
    R.changed = { files: changed.length, created: changed.filter(f => f.stat.ctime >= CUTOFF).length, byReason: why, byFolder, newFilesFound: seenNew,
      unexplainedCount: unexplained.length, unexplained: unexplained.slice(0, 500), recordedTagNotesNotChanged: { n: tagNotChanged.length, list: cap(tagNotChanged, 100) },
      specNotesNotChanged: { n: specNotChanged.length, list: specNotChanged } };
    guard('changed');
    // (b) backups against the notes now
    const diffs = [], featCount = {}, catalogKeyChanges = [];
    let compared = 0, missingNow = [];
    for (const root of ['.work/backup-completion-2026-10-19', '.work/backup-fable-2026-10-19']) {
      for (const bp of await listAll(root)) {
        if (!bp.endsWith('.md')) continue;
        const rel = bp.slice(root.length + 1); const f = app.vault.getAbstractFileByPath(rel);
        if (!f) { missingNow.push(rel); continue; }
        const A = feat(await ad.read(bp)), B = feat(await app.vault.cachedRead(f)); compared++;
        const d = { p: rel, backup: root.split('/').pop() };
        for (const k of FEATS) { const x = msDiff(A[k], B[k]); if (x.removed.length || x.added.length) { d[k] = { removed: cap(x.removed, 20), added: cap(x.added, 20), nRemoved: x.removed.length, nAdded: x.added.length }; inc(featCount, k); } }
        const vk = Object.keys(B.fmVals).filter(k => k in A.fmVals && A.fmVals[k] !== B.fmVals[k]);
        if (vk.length) { d.fmVals = vk.map(k => ({ key: k, before: A.fmVals[k].slice(0, 200), after: B.fmVals[k].slice(0, 200) })); inc(featCount, 'fmVals'); }
        if (/^Catalog\/(?!Scholars\/)[^/]+\/[^/]+\.md$/.test(rel)) { const ck = ['files', 'status', 'text', 'subject', 'type'].filter(k => (A.fmVals[k] || '') !== (B.fmVals[k] || '')); if (ck.length) catalogKeyChanges.push([rel, ck]); }
        if (Object.keys(d).length > 2) diffs.push(d);
        if (compared % 50 === 0) guard('backups ' + compared);
      }
    }
    R.backups = { notesCompared: compared, missingNow, notesWithAnyFeatureChange: diffs.length, notesByFeatureChanged: featCount, featureToCheck: CHECKS, catalogNotesWithFilesStatusTextSubjectTypeChanged: catalogKeyChanges, diffs };
    guard('backups');
    // (c) notes created since 10:30
    const backedUp = new Set(diffs.map(d => d.p));
    const created = md.filter(f => (f.stat.ctime >= CUTOFF || NEW_RE.some(([re]) => re.test(f.path))) && !backedUp.has(f.path));
    const C = { notes: created.length, byFolder: {}, withFootnoteRefs: [], withFootnoteDefs: [], withMarkers: [], withTags: [], withAttachLinks: [], fences: {}, bodyUnder100: [], fmKeySets: {}, links: 0 };
    for (const f of created) {
      const F = feat(await app.vault.cachedRead(f)); inc(C.byFolder, fk(f.path));
      if (F.fnRefs.length) C.withFootnoteRefs.push([f.path, F.fnRefs.length]);
      if (F.fnDefs.length) C.withFootnoteDefs.push([f.path, F.fnDefs.length]);
      if (F.markers.length) C.withMarkers.push([f.path, F.markers.length]);
      if (F.tags.length) C.withTags.push([f.path, F.tags.slice(0, 10)]);
      if (F.attach.length) C.withAttachLinks.push([f.path, F.attach.slice(0, 10)]);
      for (const x of F.fences) inc(C.fences, x);
      if (F.bodyLen < 100) C.bodyUnder100.push([f.path, F.bodyLen]);
      inc(C.fmKeySets, F.fmKeys.join(', ') || '(no frontmatter)'); C.links += F.links.length;
    }
    R.createdNotes = C;
    guard('created');
    // (d) check 5
    const c05 = await readJSON('.work/out/areaM/check05-catalog.json');
    const libExt = {}; for (const f of files) if (f.path.startsWith('Library/')) inc(libExt, f.extension);
    const cat = md.filter(f => /^Catalog\/[^/]+\/[^/]+\.md$/.test(f.path) && !f.path.startsWith('Catalog/Scholars/'));
    let withFiles = 0, entries = 0; const missing = [];
    for (const f of cat) {
      const fm = (MC.getFileCache(f) || {}).frontmatter || {}; if (!('files' in fm)) continue; withFiles++;
      for (const v of [].concat(fm.files || []).filter(x => x !== null && x !== undefined && x !== '')) { entries++; const m = String(v).match(/\[\[([^\]|#]+)/); const t = MC.getFirstLinkpathDest(m ? m[1] : String(v), f.path); if (!t) missing.push([f.path, String(v)]); }
    }
    R.check5 = { libraryByExtNow: libExt, libraryByExt1030: c05 ? c05.libraryVaultExt : 'check05-catalog.json not found',
      libraryNonMdChangedSince1030: changed.filter(f => f.path.startsWith('Library/') && f.extension !== 'md').map(f => f.path),
      catalogNotes: cat.length, catalogNotes1030: c05 ? c05.catalogNotes : null, withFilesKey: withFiles, withFilesKey1030: c05 ? c05.withFilesKey : null,
      entries, entries1030: c05 ? c05.entries : null, entriesMissing: missing };
    // check 6
    const c06 = await readJSON('.work/out/areaM/check06-nearempty.json');
    const bodyLen = t => { const s = t.replace(/^﻿/, ''); const m = s.match(/^---\r?\n[\s\S]*?\r?\n---[ \t]*(\r?\n|$)/); return (m ? s.slice(m[0].length) : s).trim().length; };
    const old6 = [];
    for (const [p, n] of (c06 && c06.notes) || []) { const f = app.vault.getAbstractFileByPath(p); old6.push([p, n, f ? bodyLen(await app.vault.cachedRead(f)) : 'missing']); }
    const cand = changed.filter(f => f.extension === 'md' && f.stat.size < 3 * (((MC.getFileCache(f) || {}).frontmatterPosition || { end: { offset: 0 } }).end.offset) + 400);
    const new6 = [];
    for (const f of cand) { const n = bodyLen(await app.vault.cachedRead(f)); if (n < 100) new6.push([f.path, n]); }
    R.check6 = { nearEmpty1030Now: old6, changedNotesMeasured: cand.length, changedNotesUnder100: new6 };
    guard('check6');
    // check 9
    const c09 = await readJSON('.work/out/areaM/check09-unlinked-attachments.json');
    const EXCL = new Set(['md', 'base', 'canvas', 'js', 'json', 'css', 'py', 'sh', 'diff', 'tpl', 'tsv']);
    const linked = new Set(); for (const m of Object.values(MC.resolvedLinks)) for (const t of Object.keys(m)) linked.add(t);
    const scope9 = files.filter(f => !EXCL.has(f.extension) && !f.path.startsWith('Library/'));
    const unl = scope9.filter(f => !linked.has(f.path)).map(f => f.path);
    const old9 = c09 ? [...c09.listNotLinkedNotMentioned, ...c09.listNotLinkedButMentioned].map(x => x.p) : [];
    R.check9 = { inScope: scope9.length, inScope1030: c09 ? c09.attachmentsInScope : null, notLinked: unl.length, notLinked1030: c09 ? c09.notLinked.n : null,
      newlyUnlinked: unl.filter(p => !old9.includes(p)), nowLinkedOrGone: old9.filter(p => !unl.includes(p)), createdInScope: scope9.filter(f => f.stat.ctime >= CUTOFF).map(f => f.path) };
    line = `changed since 10:30: ${changed.length} files (${Object.entries(why).sort((a, b) => b[1] - a[1]).map(([k, n]) => k + ' ' + n).join(', ')}); `
      + `now ${files.length} files (${R.counts.delta.files >= 0 ? '+' : ''}${R.counts.delta.files}), ${md.length} notes (${R.counts.delta.notes >= 0 ? '+' : ''}${R.counts.delta.notes}), ${folders.length} folders (${R.counts.delta.folders >= 0 ? '+' : ''}${R.counts.delta.folders}); `
      + `tags record ${tagNotes.size} (not changed ${tagNotChanged.length}); backups compared ${compared}: changed ${Object.entries(featCount).map(([k, n]) => k + ' ' + n).join(', ') || 'nothing'}; catalog files/status/text/subject/type changed ${catalogKeyChanges.length}; `
      + `created notes ${created.length}: footnotes ${C.withFootnoteRefs.length + C.withFootnoteDefs.length}, markers ${C.withMarkers.length}, tags ${C.withTags.length}, attachment links ${C.withAttachLinks.length}, body<100 ${C.bodyUnder100.length}; `
      + `check 5: Library pdf ${libExt.pdf || 0}, md ${libExt.md || 0}, catalog entries ${entries} missing ${missing.length}; check 6: changed notes under 100 ${new6.length}; check 9: unlinked ${unl.length} (21 at 10:30), new ${R.check9.newlyUnlinked.length}`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
