(async () => {
  // Area M re-run, check 1 (19 Oct 2026, after Part 1): every note's frontmatter parses. Changed since 10:30 by the tags
  // removal (24,156 frontmatter blocks edited as text), the new notes (scholar pages, CIS plan, scratchpad, 108 + 4 card
  // notes) and the `updated:` edits. For every note: the raw block (first line `---` to the next `---` line) against
  // Obsidian's cache (properties present, frontmatterPosition = the raw closing line), Obsidian's own parseYaml when
  // require('obsidian') is available, duplicate top-level keys, tabs, list-item lines after a key with a scalar value.
  // Then, for the 24,156 notes in .work/backup-tags-2026-10-19/removed-tags.json: the shape of what was removed, whether a
  // tags key is still in the raw text, and the risky case `tags:` with no indented items (items written at column 0
  // would have been left behind by the removal, which took only indented `- ` lines).
  // Read-only: writes only .work/out/areaM2/frontmatter.json. Memory guard 300 MB below the heap limit.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const NAME = 'frontmatter', OUT = '.work/out/areaM2', CUTOFF = Date.parse('2026-10-19T14:30:00Z');
  const LIM = performance.memory.jsHeapSizeLimit, GUARD = LIM - 300 * 1024 * 1024; let peak = 0;
  const guard = w => { const h = performance.memory.usedJSHeapSize; if (h > peak) peak = h; if (h > GUARD) throw new Error(`memory guard (${w}): ${Math.round(h / 1048576)} MB of ${Math.round(LIM / 1048576)} MB`); };
  const readJSON = async p => { try { return JSON.parse(await ad.read(p)); } catch (e) { return null; } };
  const fk = p => { const s = p.split('/'); return s.length > 2 ? s[0] + '/' + s[1] : s.length === 2 ? s[0] + '/' : '(top level)'; };
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const readAll = async (list, fn, label) => { for (let i = 0; i < list.length; i += 40) { const ch = list.slice(i, i + 40); const tx = await Promise.all(ch.map(f => app.vault.cachedRead(f).catch(() => null))); for (let j = 0; j < ch.length; j++) fn(ch[j], tx[j]); if (i % 2000 === 0) guard(label + ' ' + i); } };
  const R = { job: 'm2-01-frontmatter', when: new Date().toISOString() };
  let line = '';
  try {
    const md = app.vault.getMarkdownFiles();
    let parseYaml = null; R.parser = 'none: Obsidian cache only (require(\'obsidian\') not available)';
    try { const o = require('obsidian'); if (o && typeof o.parseYaml === 'function') { parseYaml = o.parseYaml; R.parser = "require('obsidian').parseYaml"; } } catch (e) { }
    const rec = await readJSON('.work/backup-tags-2026-10-19/removed-tags.json');
    const removed = (rec && rec.removed) || {};
    const S = { notes: md.length, withBlock: 0, withoutBlock: 0, blockWithoutContent: 0, bom: 0, unreadable: 0 };
    const P = { cacheMissing: [], yamlError: [], notMapping: [], noCachePosition: [], positionMismatch: [], unclosedBlock: [], cacheWithoutRawBlock: [], duplicateKeys: [], tabs: [], listLineAfterScalar: [] };
    const noBlock = [], byFolder = {}, failedPaths = new Set();
    const T = { notes: 0, shapes: {}, tagsKeyStillInRawText: [], keyNoItems: [], keyNoItemsWithColumn0ListLines: [], noFrontmatterNow: [], crlfBodyLfFrontmatter: 0, crlfExamples: [], changedSince1030: 0 };
    const push = (k, p, x) => { failedPaths.add(p); P[k].push(x === undefined ? p : [p, x]); };
    await readAll(md, (f, t0) => {
      if (t0 === null) { S.unreadable++; return; }
      let t = t0; if (t.charCodeAt(0) === 0xFEFF) { S.bom++; t = t.slice(1); }
      const raw = t.split('\n'); const lines = raw.map(l => l.replace(/\r$/, ''));
      const c = MC.getFileCache(f) || {};
      const hasProps = !!(c.frontmatter && Object.keys(c.frontmatter).length);
      const b = byFolder[fk(f.path)] = byFolder[fk(f.path)] || { notes: 0, withBlock: 0, problems: 0 }; b.notes++;
      let end = -1;
      if (lines[0] === '---') { for (let i = 1; i < lines.length; i++) if (lines[i].trimEnd() === '---') { end = i; break; } if (end < 0) push('unclosedBlock', f.path); }
      let block = [];
      if (end < 0) { S.withoutBlock++; noBlock.push(f.path); if (hasProps) push('cacheWithoutRawBlock', f.path); }
      else {
        S.withBlock++; b.withBlock++;
        block = lines.slice(1, end);
        const content = block.filter(l => l.trim() && !/^\s*#/.test(l));
        if (!content.length) S.blockWithoutContent++;
        if (content.length && !hasProps) push('cacheMissing', f.path);
        if (!c.frontmatterPosition) push('noCachePosition', f.path);
        else if (c.frontmatterPosition.end.line !== end) push('positionMismatch', f.path, [c.frontmatterPosition.end.line, end]);
        if (parseYaml && content.length) { try { const y = parseYaml(block.join('\n')); if (y === null || typeof y !== 'object' || Array.isArray(y)) push('notMapping', f.path); } catch (e) { push('yamlError', f.path, String(e && e.message || e).split('\n')[0].slice(0, 160)); } }
        const seen = {}; let scalarKey = null, inBlockScalar = false;
        block.forEach((l, i) => {
          if (/\t/.test(l)) push('tabs', f.path, i + 2);
          const km = l.match(/^([^\s#-][^:]*?):(?:\s+(.*))?$/);
          if (km) { const k = km[1].trim(); if (seen[k]) push('duplicateKeys', f.path, k); seen[k] = 1; const v = (km[2] || '').trim(); inBlockScalar = /^[|>]/.test(v); scalarKey = v && !inBlockScalar ? k : null; return; }
          if (!inBlockScalar && /^\s*-\s/.test(l) && scalarKey) push('listLineAfterScalar', f.path, [i + 2, scalarKey]);
        });
      }
      if (failedPaths.has(f.path)) b.problems++;
      const rm = removed[f.path];
      if (rm) {
        T.notes++; if (f.stat.mtime >= CUTOFF) T.changedSince1030++;
        const shape = rm.length > 1 ? 'key + indented items' : /:\s*$/.test(rm[0]) ? 'key, no items' : 'key with inline value'; inc(T.shapes, shape);
        if (end < 0) T.noFrontmatterNow.push(f.path);
        if (block.some(l => /^(tags?|Tags?)\s*:/.test(l))) T.tagsKeyStillInRawText.push(f.path);
        if (shape === 'key, no items') { if (T.keyNoItems.length < 300) T.keyNoItems.push(f.path); if (block.some(l => /^-\s/.test(l))) T.keyNoItemsWithColumn0ListLines.push(f.path); }
        const fmCR = end >= 0 && raw.slice(0, end + 1).some(l => l.endsWith('\r')), bodyCR = raw.slice(end + 1).some(l => l.endsWith('\r'));
        if (bodyCR && !fmCR) { T.crlfBodyLfFrontmatter++; if (T.crlfExamples.length < 20) T.crlfExamples.push(f.path); }
      }
    }, 'read');
    T.keyNoItemsCount = T.shapes['key, no items'] || 0;
    const problemCounts = Object.fromEntries(Object.entries(P).map(([k, v]) => [k, v.length]));
    R.summary = S; R.problemCounts = problemCounts; R.notesWithAnyProblem = failedPaths.size;
    R.at1030 = { withBlock: 31494, withoutBlock: 43, fail: 0, duplicateKeys: 0, tabs: 0, positionMismatch: 0 };
    R.problems = Object.fromEntries(Object.entries(P).map(([k, v]) => [k, v.slice(0, 500)]));
    R.byFolder = byFolder; R.withoutBlock = noBlock; R.tagsRecordAudit = rec ? T : 'removed-tags.json not found';
    line = `frontmatter: ${md.length} notes, ${S.withBlock} with a block (31,494 at 10:30), ${S.withoutBlock} without (43), ${S.blockWithoutContent} empty blocks, BOM ${S.bom}; `
      + `notes with a problem ${failedPaths.size} (0 at 10:30): ${Object.entries(problemCounts).map(([k, n]) => k + ' ' + n).join(', ')}; parser: ${R.parser}; `
      + (rec ? `tags record: ${T.notes} notes (${Object.entries(T.shapes).map(([k, n]) => k + ' ' + n).join(', ')}), tags key still in raw text ${T.tagsKeyStillInRawText.length}, no frontmatter now ${T.noFrontmatterNow.length}, key-only with column-0 '- ' lines ${T.keyNoItemsWithColumn0ListLines.length}, CRLF body with LF frontmatter ${T.crlfBodyLfFrontmatter}` : 'tags record not found');
  } catch (e) { R.error = String(e && e.stack || e); line = 'ABORTED: ' + R.error.split('\n')[0] + ' | ' + line; }
  peak = Math.max(peak, performance.memory.usedJSHeapSize); R.seconds = Math.round((Date.now() - T0) / 1000); R.peakMB = Math.round(peak / 1048576);
  if (!(await ad.exists(OUT))) await ad.mkdir(OUT);
  await ad.write(OUT + '/' + NAME + '.json', JSON.stringify(R, null, 1));
  return `${line} | ${R.seconds}s, peak ${R.peakMB} MB; detail ${OUT}/${NAME}.json`;
})()
