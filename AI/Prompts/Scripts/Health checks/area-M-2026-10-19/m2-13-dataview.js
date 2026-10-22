(async () => {
  // Area M re-run, check 13 (19 Oct 2026, after Part 1): Dataview dependence. Changed since 10:30 by the new view
  // Templates/Views/today-items (called from Home and Home (mobile), and written by the new Daily note template), the two
  // scholar pages (a Scholars LIST block each), the two new Bases (Journal/Habits.base, Study/Sanskrit/Flashcards/
  // Flashcards.base) and the replaced templates. Every note's fenced code blocks by language (``` and ~~~, also inside
  // callouts), inline queries (`= …`, `$= …`), dv.view calls by view, distinct dataview/dataviewjs blocks with their counts,
  // and for every folder in Templates/Views: size, dv.* and app.* calls, input, other views it names, and how many notes call
  // it. Compared with .work/out/areaM/check13-dataview-raw.json (per note: a difference in a note not modified since 10:30
  // is a difference of method, reported apart). Read-only: writes only .work/out/areaM2/dataview.json.
  const ad = app.vault.adapter, T0 = Date.now();
  const NAME = 'dataview', OUT = '.work/out/areaM2', CUTOFF = Date.parse('2026-10-19T14:30:00Z');
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const fk = p => { const s = p.split('/'); return s.length > 2 ? s[0] + '/' + s[1] : s.length === 2 ? s[0] + '/' : '(top level)'; };
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const R = { job: 'm2-13-dataview', when: new Date().toISOString() };
  let line = '';
  try {
    const all = app.vault.getFiles(), md = app.vault.getMarkdownFiles();
    const langs = {}, byFolder = {}, perFile = {}, byTemplate = {}, viewCalls = {}, distinct = {};
    const chg = new Set(all.filter(f => f.stat.mtime >= CUTOFF || f.stat.ctime >= CUTOFF).map(f => f.path));
    const blocksOf = t => {
      const lines = t.split(/\r?\n/); const out = []; let open = null, buf = [], lang = '', inline = 0;
      let i0 = 0; if (lines[0] === '---') { for (let i = 1; i < lines.length; i++) if (lines[i].trimEnd() === '---') { i0 = i + 1; break; } }
      for (let i = i0; i < lines.length; i++) {
        const L = lines[i]; const body = L.replace(/^(?:>\s?)*/, '');
        const fo = body.match(/^\s{0,3}(`{3,}|~{3,})\s*([^\s`]*)(.*)$/);
        if (!open && fo) { open = fo[1]; lang = (fo[2] || '').toLowerCase(); buf = []; continue; }
        if (open && fo && fo[1][0] === open[0] && fo[1].length >= open.length && !fo[2]) { out.push({ lang: lang || '(none)', text: buf.join('\n') }); open = null; continue; }
        if (open) { buf.push(body); continue; }
        inline += (L.match(/`=\s*[^`]+`/g) || []).length + (L.match(/`\$=[^`]+`/g) || []).length;
      }
      if (open) out.push({ lang: lang || '(none)', text: buf.join('\n'), unclosed: true });
      return { blocks: out, inline };
    };
    for (let i = 0; i < md.length; i += 40) {
      const ch = md.slice(i, i + 40); const tx = await Promise.all(ch.map(f => app.vault.cachedRead(f).catch(() => '')));
      ch.forEach((f, j) => {
        const { blocks, inline } = blocksOf(tx[j]);
        const c = { dataview: 0, dataviewjs: 0, tasks: 0, inline, base: 0 };
        for (const b of blocks) {
          inc(langs, b.lang);
          if (b.lang in c && b.lang !== 'inline') c[b.lang]++;
          if (b.lang === 'dataview' || b.lang === 'dataviewjs') {
            const kind = b.lang === 'dataview' ? 'dataview:' + ((b.text.trim().match(/^\w+/) || ['?'])[0].toUpperCase()) : 'dataviewjs';
            const k = kind + '\u0000' + b.text.trim(); const e = distinct[k] = distinct[k] || { kind, text: b.text.trim().slice(0, 600), len: b.text.trim().length, count: 0, folders: {}, sample: [] }; e.count++; inc(e.folders, fk(f.path)); if (e.sample.length < 3) e.sample.push(f.path);
          }
          if (b.lang === 'dataviewjs') for (const m of b.text.matchAll(/dv\.view\(\s*["'`]([^"'`]+)["'`]/g)) inc(viewCalls, m[1].replace(/\/view(\.js)?$/, ''));
        }
        if (c.dataview + c.dataviewjs + c.tasks + c.inline + c.base) {
          perFile[f.path] = c; const b = byFolder[fk(f.path)] = byFolder[fk(f.path)] || { files: 0, dataview: 0, dataviewjs: 0, tasks: 0, inline: 0, base: 0 }; b.files++; for (const k of Object.keys(c)) b[k] += c[k];
          if (f.path.startsWith('Templates/')) byTemplate[f.path] = c;
        }
      });
      if (i % 2000 === 0) guard('read ' + i);
    }
    // views
    const viewDirs = [...new Set(all.filter(f => /^Templates\/Views\/[^/]+\//.test(f.path)).map(f => f.path.split('/').slice(0, 3).join('/')))].sort();
    const views = {};
    for (const v of viewDirs) {
      const fl = all.filter(f => f.path.startsWith(v + '/')); const js = fl.find(f => f.name === 'view.js'); const e = { files: fl.map(f => f.name) };
      if (js) { const t = await app.vault.cachedRead(js); const dvApi = {}, appApi = {}; for (const m of t.matchAll(/\bdv\.(\w+)/g)) inc(dvApi, m[1]); for (const m of t.matchAll(/\bapp\.(\w+)/g)) inc(appApi, m[1]);
        Object.assign(e, { bytes: js.stat.size, lines: t.split('\n').length, dvApi, dvApiTotal: Object.values(dvApi).reduce((a, b) => a + b, 0), appApi, usesInput: /\binput\b/.test(t), callsOtherViews: [...new Set([...t.matchAll(/Templates\/Views\/([\w-]+)/g)].map(m => m[1]))].filter(x => 'Templates/Views/' + x !== v), changedSince1030: chg.has(js.path) }); }
      e.calledByNotes = viewCalls[v] || 0; views[v.split('/').pop()] = e;
    }
    const namedByViews = new Set(Object.values(views).flatMap(e => e.callsOtherViews || []));
    const tplText = (await Promise.all(all.filter(f => f.path.startsWith('Templates/') && f.extension === 'md').map(f => app.vault.cachedRead(f)))).join('\n');
    const uncalled = Object.keys(views).filter(v => !views[v].calledByNotes && !namedByViews.has(v) && !tplText.includes('Templates/Views/' + v));
    const bases = all.filter(f => f.extension === 'base').map(f => [f.path, f.stat.size, chg.has(f.path)]);
    guard('views');
    // against 10:30
    const old = await readJSON('.work/out/areaM/check13-dataview-raw.json'); const cmp = {};
    if (old) {
      cmp.fenceLangs = Object.fromEntries([...new Set([...Object.keys(old.fenceLangs), ...Object.keys(langs)])].filter(k => (old.fenceLangs[k] || 0) !== (langs[k] || 0)).map(k => [k, [old.fenceLangs[k] || 0, langs[k] || 0]]));
      const of = old.files || {}; const K = ['dataview', 'dataviewjs', 'tasks', 'inline', 'base'];
      const diffs = [...new Set([...Object.keys(of), ...Object.keys(perFile)])].filter(p => K.some(k => ((of[p] || {})[k] || 0) !== ((perFile[p] || {})[k] || 0))).map(p => ({ p, before: of[p] || null, now: perFile[p] || null, changedSince1030: chg.has(p), exists: !!app.vault.getAbstractFileByPath(p) }));
      cmp.notesWithDifferentCounts = diffs.filter(d => d.changedSince1030 && d.exists); cmp.notesGone = diffs.filter(d => !d.exists).map(d => d.p); cmp.methodDifferences = diffs.filter(d => !d.changedSince1030 && d.exists);
      cmp.viewCalls = Object.fromEntries([...new Set([...Object.keys(old.dvJsViewCalls || {}), ...Object.keys(viewCalls)])].filter(k => ((old.dvJsViewCalls || {})[k] || 0) !== (viewCalls[k] || 0)).map(k => [k, [(old.dvJsViewCalls || {})[k] || 0, viewCalls[k] || 0]]));
      const od = Object.fromEntries((old.distinctBlocks || []).map(e => [e.kind + '\u0000' + e.text.trim(), e.count]));
      cmp.distinctBlocksChanged = Object.values(distinct).filter(e => (od[e.kind + '\u0000' + e.text] || 0) !== e.count && e.len <= 600).map(e => ({ kind: e.kind, text: e.text.slice(0, 160), before: od[e.kind + '\u0000' + e.text] || 0, now: e.count }));
    } else cmp.error = 'check13-dataview-raw.json not readable';
    const tot = k => Object.values(perFile).reduce((a, c) => a + c[k], 0);
    R.fenceLangs = langs; R.byFolder = byFolder; R.byTemplate = byTemplate; R.files = perFile; R.dvJsViewCalls = viewCalls;
    R.distinctBlocks = Object.values(distinct).sort((a, b) => b.count - a.count); R.views = views; R.viewsCalledByNothing = uncalled; R.bases = bases; R.against1030 = cmp;
    line = `Dataview: ${tot('dataviewjs')} dataviewjs, ${tot('dataview')} dataview, ${tot('inline')} inline, ${tot('tasks')} tasks, ${tot('base')} base blocks in ${Object.keys(perFile).length} notes (10:30: 986 / 114 / 0 / 4 / 9 in 1,048); `
      + `distinct blocks ${Object.keys(distinct).length}; views ${Object.keys(views).length} (14 at 10:30; ${Object.entries(views).map(([k, e]) => k + ' ' + e.calledByNotes).join(', ')}); called by nothing: ${uncalled.join(', ') || 'none'}; .base files ${bases.length} (13); `
      + `changed vs 10:30: fence languages ${JSON.stringify(cmp.fenceLangs || {})}; notes with different counts ${(cmp.notesWithDifferentCounts || []).length} (${(cmp.notesWithDifferentCounts || []).slice(0, 6).map(d => d.p.split('/').pop()).join('; ')}); notes gone ${(cmp.notesGone || []).length}; method differences in unchanged notes ${(cmp.methodDifferences || []).length}; view calls ${JSON.stringify(cmp.viewCalls || {})}`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
