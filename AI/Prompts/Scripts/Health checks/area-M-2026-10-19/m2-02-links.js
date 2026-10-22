(async () => {
  // Area M re-run, check 2 (19 Oct 2026, after Part 1): links and embeds resolve, including #heading and #^block subpaths.
  // Changed since 10:30 by the 91 split-verse edits (39 links re-pointed), the Guide, lists, Scholars, Home, Sanskrit.md and
  // wish-list edits, the replaced prompt and templates, and the new notes (scholar pages, CIS plan and cards, 108 card notes).
  // For every note: every link, embed and frontmatter link in Obsidian's cache, resolved with getFirstLinkpathDest; a
  // `#^id` must be a block id of the target, a `#heading` one of its headings (lower case, spaces collapsed, the last part of
  // A#B; the 11:49 health check's rule); with require('obsidian').resolveSubpath, Obsidian's own result as well. Links into
  // PDFs (#page=) are counted, not checked; a subpath into a .base must name one of the Base's views. A control test checks
  // that 300 real block ids and 300 real headings are found and the same with "zq" appended are not.
  // Read-only: writes only .work/out/areaM2/links.json. Memory guard 300 MB below the heap limit.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const NAME = 'links', OUT = '.work/out/areaM2', CUTOFF = Date.parse('2026-10-19T14:30:00Z');
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const R = { job: 'm2-02-links', when: new Date().toISOString() };
  let line = '';
  try {
    const md = app.vault.getMarkdownFiles();
    let resolveSubpath = null; R.obsidianResolveSubpath = false;
    try { const o = require('obsidian'); if (o && typeof o.resolveSubpath === 'function') { resolveSubpath = o.resolveSubpath; R.obsidianResolveSubpath = true; } } catch (e) { }
    const memo = new Map();
    const dest = (name, src) => { const k = name + '\u0000' + src.slice(0, src.lastIndexOf('/') + 1); if (!memo.has(k)) memo.set(k, MC.getFirstLinkpathDest(name, src)); return memo.get(k); };
    const norm = s => s.toLowerCase().replace(/\s+/g, ' ').trim();
    const hcache = new Map();
    const headSet = t => { if (!hcache.has(t.path)) hcache.set(t.path, new Set(((MC.getFileCache(t) || {}).headings || []).map(h => norm(h.heading)))); return hcache.get(t.path); };
    const blockOk = (t, id) => !!(((MC.getFileCache(t) || {}).blocks || {})[id.toLowerCase()]);
    const headOk = (t, sub) => headSet(t).has(norm(sub.split('#').pop()));
    const C = { links: 0, embeds: 0, frontmatterLinks: 0, withSubpath: 0, block: 0, heading: 0, pdf: 0, selfLinks: 0, base: 0, otherNonMd: 0, unresolved: 0 };
    const bad = [], badObs = [], baseLinks = [], unresolved = [];
    const changedSrc = { files: 0, links: 0, bad: 0, unresolved: 0 };
    const ctl = { block: [], heading: [] };
    let n = 0;
    for (const f of md) {
      const c = MC.getFileCache(f); if (!c) continue;
      const ch = f.stat.mtime >= CUTOFF || f.stat.ctime >= CUTOFF; if (ch) changedSrc.files++;
      for (const [kind, arr] of [['links', c.links], ['embeds', c.embeds], ['frontmatterLinks', c.frontmatterLinks]]) {
        for (const l of arr || []) {
          C[kind]++; if (ch) changedSrc.links++;
          const s = l.link; const i = s.indexOf('#'); const name = i < 0 ? s : s.slice(0, i); const sub = i < 0 ? '' : s.slice(i + 1);
          const t = name ? dest(name, f.path) : f;
          if (!t) { C.unresolved++; unresolved.push([f.path, s, kind]); if (ch) changedSrc.unresolved++; continue; }
          if (!sub) continue;
          C.withSubpath++; if (!name) C.selfLinks++;
          if (t.extension === 'pdf') { C.pdf++; continue; }
          if (t.extension === 'base') { C.base++; baseLinks.push([f.path, s, t.path, sub]); continue; }
          if (t.extension !== 'md') { C.otherNonMd++; continue; }
          let ok;
          if (sub.startsWith('^')) { C.block++; ok = blockOk(t, sub.slice(1)); if (ok && ctl.block.length < 300 && C.block % 97 === 1) ctl.block.push([t, sub.slice(1)]); }
          else { C.heading++; ok = headOk(t, sub); if (ok && ctl.heading.length < 300 && C.heading % 7 === 1) ctl.heading.push([t, sub]); }
          if (!ok) { bad.push([f.path, s, kind, t.path]); if (ch) changedSrc.bad++; }
          if (resolveSubpath) { let r = null; try { r = resolveSubpath(MC.getFileCache(t), '#' + sub); } catch (e) { } if (!r) badObs.push([f.path, s, kind, t.path]); }
        }
      }
      if (++n % 2000 === 0) { guard('links ' + n); await new Promise(r => setTimeout(r, 0)); }
    }
    // .base subpaths: the view must exist
    const baseBad = [], baseViews = {};
    for (const [src, s, bp, sub] of baseLinks) {
      if (!baseViews[bp]) { const bf = app.vault.getAbstractFileByPath(bp); const txt = bf ? await app.vault.cachedRead(bf) : ''; baseViews[bp] = [...txt.matchAll(/^\s*(?:-\s+)?name:\s*["']?(.+?)["']?\s*$/gm)].map(m => m[1]); }
      if (!baseViews[bp].includes(sub)) baseBad.push([src, s, baseViews[bp]]);
    }
    // control test
    const control = {
      block: { tested: ctl.block.length, realFound: ctl.block.filter(([t, id]) => blockOk(t, id)).length, mutatedRejected: ctl.block.filter(([t, id]) => !blockOk(t, id + 'zq')).length },
      heading: { tested: ctl.heading.length, realFound: ctl.heading.filter(([t, h]) => headOk(t, h)).length, mutatedRejected: ctl.heading.filter(([t, h]) => !headOk(t, h + 'zq')).length } };
    // the unresolved-links table (Obsidian's own) against the accepted 14
    const un = Object.entries(MC.unresolvedLinks).filter(([, m]) => Object.keys(m).length);
    const old = await readJSON('.work/out/areaM/check02-links.json');
    R.counts = C; R.at1030 = { links: 440478, embeds: 10469, frontmatterLinks: 13757, withSubpath: 311832, block: 293804, heading: 2428, pdf: 15600, selfLinks: 620, unresolved: 14, badSubpaths: 0 };
    R.unresolvedTable = { files: un.length, links: un.reduce((a, [, m]) => a + Object.values(m).reduce((x, y) => x + y, 0), 0), list: un };
    R.unresolvedFromCache = unresolved.slice(0, 2000);
    R.unresolved1030 = old || 'check02-links.json not readable';
    R.badSubpaths = bad.slice(0, 2000); R.badSubpathsObsidian = resolveSubpath ? { n: badObs.length, list: badObs.slice(0, 2000) } : 'resolveSubpath not available';
    R.baseSubpaths = { n: baseLinks.length, bad: baseBad, views: baseViews };
    R.control = control; R.sourcesChangedSince1030 = changedSrc;
    line = `links: ${C.links} links, ${C.embeds} embeds, ${C.frontmatterLinks} frontmatter links (10:30: 440,478 / 10,469 / 13,757); unresolved ${C.unresolved} (table: ${un.length} files / ${R.unresolvedTable.links} links; 10:30: 10 / 14); `
      + `subpaths ${C.withSubpath} (#^block ${C.block}, #heading ${C.heading}, pdf ${C.pdf}, self ${C.selfLinks}, base ${C.base}, other ${C.otherNonMd}); bad #^block/#heading ${bad.length} (0 at 10:30)`
      + (resolveSubpath ? `, by Obsidian's resolveSubpath ${badObs.length}` : ', resolveSubpath not available') + `; base subpaths bad ${baseBad.length}; `
      + `control: blocks ${control.block.realFound}/${control.block.tested} found, ${control.block.mutatedRejected} mutated rejected; headings ${control.heading.realFound}/${control.heading.tested}, ${control.heading.mutatedRejected}; `
      + `in notes changed since 10:30: ${changedSrc.files} notes, ${changedSrc.links} links, bad ${changedSrc.bad}, unresolved ${changedSrc.unresolved}`;
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
