(async () => {
  // Area M re-run, check 12 (19 Oct 2026, after Part 1): hidden folders, sizes from the disk. Changed since 10:30 by every
  // job of Part 1 (.work/backup-tags-2026-10-19 with 500 note copies and removed-tags.json, .work/backup-completion-2026-10-19,
  // .work/backup-fable-2026-10-19, .work/queue/done, .work/out, .work/edits). Same tables as at 10:30: .trash, .work,
  // .smart-env, .obsidian with files, folders, bytes, newest date and largest file; their children; the plugin folders;
  // hidden files at the top level. Which .work folders a note names: every .work child whose name has a digit or a hyphen
  // (plus ".work/fx"), as a whole token, in the notes outside Library/ and Texts/ (the 10:30 run searched 84 notes in AI/ and
  // the top level; both scopes are reported). Check 11, not re-run: the .obsidian files modified since 10:30 are listed and
  // every JSON among them is parsed. Compared with .work/out/areaM/check12-hidden-folders.json.
  // Read-only: writes only .work/out/areaM2/hidden.json. Memory guard 300 MB below the heap limit.
  const ad = app.vault.adapter, T0 = Date.now();
  const NAME = 'hidden', OUT = '.work/out/areaM2', CUTOFF = Date.parse('2026-10-19T14:30:00Z');
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const day = t => { if (!t) return null; const d = new Date(t); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  const mb = b => Math.round(b / 1048576 * 10) / 10;
  const R = { job: 'm2-12-hidden', when: new Date().toISOString() };
  let line = '';
  const changedObs = [];
  // one walk per folder; stats in parallel batches
  const tree = async (dir, track) => {
    const r = { files: 0, dirs: 0, bytes: 0, newest: 0, largest: { p: '', b: 0 }, changedSince1030: 0 };
    const walk = async d => {
      let L; try { L = await ad.list(d); } catch (e) { return; }
      for (let i = 0; i < L.files.length; i += 64) {
        const ch = L.files.slice(i, i + 64); const st = await Promise.all(ch.map(p => ad.stat(p).catch(() => null)));
        ch.forEach((p, j) => { const s = st[j]; r.files++; if (!s) return; r.bytes += s.size; if (s.mtime > r.newest) r.newest = s.mtime; if (s.size > r.largest.b) r.largest = { p: p.slice(dir.length + 1), b: s.size }; if (s.mtime >= CUTOFF) { r.changedSince1030++; if (track) changedObs.push([p, s.size, new Date(s.mtime).toISOString()]); } });
      }
      for (const s of L.folders) { r.dirs++; await walk(s); }
    };
    await walk(dir); guard(dir);
    return r;
  };
  const fin = r => ({ files: r.files, dirs: r.dirs, bytes: r.bytes, mb: mb(r.bytes), newest: day(r.newest), largest: r.largest, changedSince1030: r.changedSince1030 });
  const children = async (dir, track) => {
    const out = {}; let L; try { L = await ad.list(dir); } catch (e) { return { out, total: null }; }
    const tot = { files: 0, dirs: L.folders.length, bytes: 0, newest: 0, largest: { p: '', b: 0 }, changedSince1030: 0 };
    for (const d of L.folders.sort()) { const r = await tree(d, track); out[d.slice(dir.length + 1) + '/'] = fin(r); tot.files += r.files; tot.dirs += r.dirs; tot.bytes += r.bytes; tot.changedSince1030 += r.changedSince1030; if (r.newest > tot.newest) tot.newest = r.newest; if (r.largest.b > tot.largest.b) tot.largest = { p: d.slice(dir.length + 1) + '/' + r.largest.p, b: r.largest.b }; }
    const loose = { files: L.files.length, bytes: 0, changedSince1030: 0, names: L.files.map(p => p.slice(dir.length + 1)).slice(0, 60) };
    for (const p of L.files) { const s = await ad.stat(p).catch(() => null); if (!s) continue; loose.bytes += s.size; if (s.mtime >= CUTOFF) { loose.changedSince1030++; if (track) changedObs.push([p, s.size, new Date(s.mtime).toISOString()]); } if (s.mtime > tot.newest) tot.newest = s.mtime; if (s.size > tot.largest.b) tot.largest = { p: p.slice(dir.length + 1), b: s.size }; }
    out['(loose files)'] = loose; tot.files += loose.files; tot.bytes += loose.bytes; tot.changedSince1030 += loose.changedSince1030;
    return { out, total: fin(tot) };
  };
  try {
    let top = { files: [], folders: [] }; try { top = await ad.list('/'); } catch (e) { try { top = await ad.list(''); } catch (e2) { } }
    const hiddenDirs = [...new Set(top.folders.map(p => p.replace(/^\//, '')).filter(p => p.startsWith('.')))];
    for (const k of ['.obsidian', '.trash', '.work', '.smart-env']) if (!hiddenDirs.includes(k) && await ad.exists(k)) hiddenDirs.push(k);
    R.rootHiddenFiles = top.files.map(p => p.replace(/^\//, '')).filter(p => p.startsWith('.'));
    R.hiddenTopLevelFolders = {}; R.children = {};
    for (const h of hiddenDirs.sort()) { const c = await children(h, h === '.obsidian'); R.hiddenTopLevelFolders[h] = c.total; R.children[h] = c.out; }
    R.pluginFolders = (await children('.obsidian/plugins', false)).out;
    // check 11: .obsidian files changed since 10:30; parse every JSON among them
    const obsJsonCount = { all: 0 }; const cntJson = async d => { let L; try { L = await ad.list(d); } catch (e) { return; } obsJsonCount.all += L.files.filter(p => p.endsWith('.json')).length; for (const s of L.folders) await cntJson(s); };
    await cntJson('.obsidian');
    R.check11 = { jsonFilesUnderObsidian: obsJsonCount.all, jsonFiles1030: 53, changedSince1030: changedObs.map(([p, s, t]) => ({ p, size: s, mtime: t })), parsed: [] };
    for (const [p] of changedObs) if (p.endsWith('.json')) { let ok = true, err = null; try { JSON.parse(await ad.read(p)); } catch (e) { ok = false; err = String(e.message || e).slice(0, 160); } R.check11.parsed.push({ p, ok, err }); }
    guard('obsidian');
    // which .work children a note names
    const work = Object.keys(R.children['.work'] || {}).filter(k => k !== '(loose files)').map(k => k.replace(/\/$/, ''));
    const names = work.filter(n => /[\d-]/.test(n)).map(n => [n, n]).concat(work.includes('fx') ? [['fx', '.work/fx']] : []);
    const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const res = names.map(([n, tok]) => [n, new RegExp('(?<![\\w-])' + esc(tok) + '(?![\\w-])')]);
    const md = app.vault.getMarkdownFiles().filter(f => !f.path.startsWith('Library/') && !f.path.startsWith('Texts/'));
    const hits = Object.fromEntries(names.map(([n]) => [n, []]));
    for (let i = 0; i < md.length; i += 40) {
      const ch = md.slice(i, i + 40); const tx = await Promise.all(ch.map(f => app.vault.cachedRead(f).catch(() => '')));
      ch.forEach((f, j) => { const t = tx[j]; if (!t.includes('backup') && !t.includes('.work')) return; for (const [n, re] of res) if (re.test(t)) hits[n].push(f.path); });
      if (i % 2000 === 0) guard('names ' + i);
    }
    const narrow = p => p.startsWith('AI/') || !p.includes('/');
    R.workFoldersNamedInNotes = { notesSearched: md.length, notesSearched1030: 84, perFolder: Object.fromEntries(Object.entries(hits).map(([n, a]) => [n, { notes: a.length, inAIorTopLevel: a.filter(narrow).length, first: a.slice(0, 5) }])),
      namedInNoNote: Object.entries(hits).filter(([, a]) => !a.length).map(([n]) => n), namedOnlyOutsideAIandTopLevel: Object.entries(hits).filter(([, a]) => a.length && !a.some(narrow)).map(([n]) => n) };
    // against 10:30
    const old = await readJSON('.work/out/areaM/check12-hidden-folders.json'); const cmp = {};
    if (old) {
      cmp.topLevel = Object.fromEntries(Object.keys({ ...old.hiddenTopLevelFolders, ...R.hiddenTopLevelFolders }).map(k => { const a = old.hiddenTopLevelFolders[k] || {}, b = R.hiddenTopLevelFolders[k] || {}; return [k, { files: [a.files, b.files], mb: [a.mb, b.mb] }]; }));
      const ow = old.workChildren || {}, nw = R.children['.work'] || {};
      cmp.workNew = Object.keys(nw).filter(k => !(k in ow)).map(k => [k, nw[k].files, nw[k].mb]);
      cmp.workGone = Object.keys(ow).filter(k => !(k in nw));
      cmp.workChanged = Object.keys(nw).filter(k => k in ow && (ow[k].files !== nw[k].files)).map(k => [k, ow[k].files, nw[k].files, ow[k].mb, nw[k].mb]);
      const ot = old.trashChildren || {}, nt = R.children['.trash'] || {};
      cmp.trashNew = Object.keys(nt).filter(k => !(k in ot)); cmp.trashGone = Object.keys(ot).filter(k => !(k in nt));
      cmp.unnamedBackupFolders1030 = ['backup-calendar-2026-10-08', 'backup-phase4-2026-10-07', 'backup-phase4-afix', 'backup-phase4-catalog', 'backup-phase4-catfix', 'backup-phase4-links', 'backup-phase4-nfix', 'backup-phase4-step8', 'backup-phase4-trash', 'backup-phase5-2026-10-09', 'backup-phase5-links-2026-10-12', 'backup-phase5-pass2-2026-10-12', 'backup-plan-2026-10-09', 'backup-scholars-2026-10-15', 'backup-wishlist', 'fx'];
    } else cmp.error = 'check12-hidden-folders.json not readable';
    R.against1030 = cmp;
    const H = R.hiddenTopLevelFolders;
    line = `hidden: ${Object.entries(H).map(([k, v]) => `${k} ${v.files} files ${v.mb} MB (changed since 10:30: ${v.changedSince1030})`).join('; ')}; `
      + `.work new folders ${(cmp.workNew || []).map(x => x[0] + ' ' + x[1] + ' files ' + x[2] + ' MB').join(', ') || 'none'}; grown ${(cmp.workChanged || []).map(x => x[0] + ' ' + x[1] + '→' + x[2]).join(', ') || 'none'}; gone ${(cmp.workGone || []).join(', ') || 'none'}; `
      + `.work folders named in no note (${md.length} notes outside Library/Texts): ${R.workFoldersNamedInNotes.namedInNoNote.length} (${R.workFoldersNamedInNotes.namedInNoNote.join(', ')}); `
      + `check 11: .obsidian files changed since 10:30 ${changedObs.length}, JSON among them ${R.check11.parsed.length}, failing to parse ${R.check11.parsed.filter(x => !x.ok).length}; JSON files ${obsJsonCount.all} (53 at 10:30)`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
