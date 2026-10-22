(async () => {
  // Read-only. A line-for-line port of Stephen's Downloads/gemini-code-1792011754459.py (a vault audit written by another LLM)
  // to the Obsidian runner, because the script cannot be run from the cloud workspace and there is no Python shell on the laptop.
  // Same walk (hidden folders skipped), same regexes, same counters, same report sections and formatting.
  // Writes .work/out/vault_audit_report.txt (the script would write vault_audit_report.txt in its working folder).
  const V = app.vault, ad = V.adapter, T0 = Date.now();
  const LIM = performance.memory.jsHeapSizeLimit, heap = () => performance.memory.usedJSHeapSize; const GUARD = LIM - 300e6; let peak = heap();
  const files = V.getFiles();
  const mdFiles = [], otherFiles = [], folderCounts = {}, extSizes = {}, extCounts = {}, noteNames = new Set();
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  // Python Path.name / Path.stem on the link text (the script's own rule: stem = name up to its LAST dot).
  // pname follows Windows pathlib, as the script runs on Stephen's laptop: a trailing backslash or slash is dropped first, so the
  // table link [[X\|label]] (captured as 'X\') gives 'X', not '' (14 Oct 2026, audit L-01).
  const pname = s => { const t = s.replace(/[\\/]+$/, ''); const parts = t.split(/[\\/]/); return parts[parts.length - 1]; };
  const pstem = s => { const i = s.lastIndexOf('.'); return (i > 0 && i < s.length - 1) ? s.slice(0, i) : s; };
  for (const f of files) {
    const folder = f.parent ? (f.parent.path === '/' ? '.' : f.parent.path) : '.';
    inc(folderCounts, folder);
    const ext = f.extension ? '.' + f.extension.toLowerCase() : '(no extension)';
    inc(extCounts, ext); inc(extSizes, ext, f.stat.size);
    if (ext === '.md') { mdFiles.push(f); noteNames.add(f.basename.toLowerCase()); }
    else otherFiles.push(f);
  }
  const wikilink = /\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]/g;
  const tagRe = /(?:^|\s)#([a-zA-Z0-9_\-\/]+)/g;
  const yamlRe = /^---\s*\n([\s\S]*?)\n---\s*\n/;
  const outgoing = new Map(), incoming = {}, allTags = {}, yamlKeys = {}, emptyNotes = [], referenced = new Set();
  let n = 0;
  for (const f of mdFiles) {
    if (f.stat.size === 0) { emptyNotes.push(f.path); continue; }
    let content; try { content = await ad.read(f.path); } catch (e) { continue; }
    if (!content.trim()) emptyNotes.push(f.path);
    const ym = yamlRe.exec(content);
    if (ym) for (const line of ym[1].split('\n')) { if (line.includes(':') && !/^[ \t-]/.test(line)) { const key = line.split(':', 1)[0].trim(); if (key) inc(yamlKeys, key); } }
    const clean = new Set();
    for (const m of content.matchAll(wikilink)) { const target = pname(m[1].trim()).toLowerCase(); clean.add(target); referenced.add(target); inc(incoming, target); inc(incoming, pstem(target)); }
    outgoing.set(f.path, clean);
    for (const m of content.matchAll(tagRe)) inc(allTags, m[1].toLowerCase());
    if (++n % 500 === 0) { const h = heap(); if (h > peak) peak = h; if (h > GUARD) throw new Error('memory guard at ' + n + ' notes: ' + Math.round(h / 1e6) + ' MB'); await new Promise(r => setTimeout(r, 0)); }
  }
  const otherNames = new Set(otherFiles.map(f => f.name.toLowerCase()));
  const orphans = [], broken = {};
  for (const f of mdFiles) {
    const stem = f.basename.toLowerCase(); const out = outgoing.get(f.path) || new Set();
    if (!(incoming[stem] > 0) && out.size === 0) orphans.push(f.path);
    for (const t of out) { const ts = pstem(t).toLowerCase(); if (!noteNames.has(ts) && !otherNames.has(t)) inc(broken, t); }
  }
  const unlinked = otherFiles.filter(f => !referenced.has(f.name.toLowerCase()) && !referenced.has(pstem(f.name).toLowerCase()));
  const totalBytes = Object.values(extSizes).reduce((a, b) => a + b, 0);
  const MB = b => (b / 1048576).toFixed(2), pad = (s, w) => String(s).padStart(w), padR = (s, w) => String(s).padEnd(w);
  const L = [];
  L.push('=== OBSIDIAN VAULT AUDIT REPORT ===');
  L.push(`Total Size: ${(totalBytes / 1073741824).toFixed(2)} GB`);
  L.push(`Markdown Notes: ${mdFiles.length} | Attachments/Other: ${otherFiles.length}`); L.push('');
  L.push('--- STORAGE BY FILE TYPE ---');
  for (const [ext, sz] of Object.entries(extSizes).sort((a, b) => b[1] - a[1]).slice(0, 20)) L.push(`${padR(ext, 12)} : ${pad(extCounts[ext], 6)} files | ${pad(MB(sz), 8)} MB`);
  L.push(''); L.push('--- TOP 30 LARGEST FILES ---');
  for (const f of [...files].sort((a, b) => b.stat.size - a.stat.size).slice(0, 30)) L.push(`${pad(MB(f.stat.size), 8)} MB | ${f.path}`);
  L.push(''); L.push('--- GRAPH HEALTH SUMMARY ---');
  L.push(`Empty Notes: ${emptyNotes.length}`);
  L.push(`Orphaned Notes (0 incoming & 0 outgoing wikilinks): ${orphans.length}`);
  L.push(`Potentially Unlinked Attachments: ${unlinked.length} (${MB(unlinked.reduce((a, f) => a + f.stat.size, 0))} MB)`);
  L.push(''); L.push('--- TOP 30 BROKEN WIKILINKS ---');
  for (const [k, c] of Object.entries(broken).sort((a, b) => b[1] - a[1]).slice(0, 30)) L.push(`[[${k}]] (referenced ${c} times)`);
  L.push(''); L.push('--- TOP 30 YAML FRONTMATTER KEYS ---');
  for (const [k, c] of Object.entries(yamlKeys).sort((a, b) => b[1] - a[1]).slice(0, 30)) L.push(`${k}: ${c} notes`);
  L.push(''); L.push('--- TOP 40 TAGS ---');
  for (const [k, c] of Object.entries(allTags).sort((a, b) => b[1] - a[1]).slice(0, 40)) L.push(`#${k}: ${c}`);
  L.push(''); L.push('--- TOP 40 FOLDERS BY FILE COUNT ---');
  for (const [k, c] of Object.entries(folderCounts).sort((a, b) => b[1] - a[1]).slice(0, 40)) L.push(`${pad(c, 5)} files | ${k}`);
  await ad.write('.work/out/vault_audit_report.txt', L.join('\n') + '\n');
  // Side file for Claude: the full lists behind the counts (not part of the script's report).
  await ad.write('.work/out/s84c-gemini-audit-lists.json', JSON.stringify({ emptyNotes, orphans, broken: Object.entries(broken).sort((a, b) => b[1] - a[1]).slice(0, 400), unlinked: unlinked.map(f => [f.path, f.stat.size]), yamlKeys, allTags, seconds: Math.round((Date.now() - T0) / 1000), peakHeapMB: Math.round(peak / 1e6) }, null, 1));
  return `gemini audit: ${mdFiles.length} notes, ${otherFiles.length} other; empty ${emptyNotes.length}, orphans ${orphans.length}, unlinked ${unlinked.length}, broken targets ${Object.keys(broken).length}; ${Math.round((Date.now() - T0) / 1000)} s, peak ${Math.round(peak / 1e6)} MB`;
})()
