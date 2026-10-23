__APPLY__(async () => {
  // Talmud references in older notes -> the daf notes (22 Oct 2026). Dry run writes proposals; apply backs up first.
  const DRY = window.DRY !== false; const D = __D__; const V = app.vault, mc = app.metadataCache, ad = app.vault.adapter;
  const SCOPE = ['Texts/Zohar/', 'Texts/Chasidut/', 'Texts/Bible/Torah/', 'Texts/Pirkei Avot/', 'Library/Judaica/', 'Library/Biblical-Studies/', 'Library/Christianity/'];
  const SIDES = new Set(D.sides); const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const full = Object.keys(D.alias).sort((a, b) => b.length - a.length).map(esc).join('|');
  const ab = Object.keys(D.abbr).sort((a, b) => b.length - a.length).map(esc).join('|');
  // 1: full name (optionally italic), 2: SBL abbreviation after 'b.' ; then daf and side
  const RE = new RegExp(`(?<![\\w\\[|#*])(?:(\\*?)(${full})(\\*?)|(?<=\\bb\\.\\s?)(${ab}))(,?\\s+)(\\d{1,3})([ab])(?![\\w\\]])`, 'gu');
  const NOT_BAVLI = /(JT|Y\.|y\.|Yerushalmi|Jerusalem Talmud|Talmud Yerushalmi|PT|j\.|Tosefta|t\.)\s*(\*?)$/;
  const R = { notes: 0, changed: 0, links: 0, skipped_jt: 0, notarget: 0, byFolder: {}, samples: [] }; const BK = '.work/backup-talmudlinks-2026-10-22/';
  for (const f of V.getMarkdownFiles()) {
    if (!SCOPE.some(s => f.path.startsWith(s))) continue; R.notes++;
    const text = await V.read(f); const lines = text.split('\n'); let inFm = lines[0] === '---', inCode = false, n = 0;
    for (let i = 0; i < lines.length; i++) {
      let l = lines[i];
      if (inFm) { if (i > 0 && l === '---') inFm = false; continue; }
      if (/^```/.test(l)) { inCode = !inCode; continue; }
      if (inCode || /^#{1,6} /.test(l)) continue;
      const parts = l.split(/(\[\[[^\]]*\]\]|`[^`]*`|https?:\/\/\S+)/);
      for (let k = 0; k < parts.length; k += 2) {
        parts[k] = parts[k].replace(RE, (m, i1, name, i2, abbr, sp, d, s, off, str) => {
          if (name && Boolean(i1) !== Boolean(i2)) return m;
          if (NOT_BAVLI.test(str.slice(Math.max(0, off - 22), off))) { R.skipped_jt++; return m; }
          const tr = name ? D.alias[name] : D.abbr[abbr];
          if (!SIDES.has(`${tr}|${d}${s}`)) { R.notarget++; return m; }
          n++; R.links++; const out = `[[${tr} ${d}#${d}${s}|${m}]]`;
          if (R.samples.length < 400 && Math.random() < 0.25) R.samples.push({ note: f.path, before: str.slice(Math.max(0, off - 60), off + m.length + 40), link: out });
          return out;
        });
      }
      lines[i] = parts.join('');
    }
    if (n) {
      R.changed++; const top = f.path.split('/').slice(0, 2).join('/'); R.byFolder[top] = (R.byFolder[top] || 0) + n;
      if (!DRY) { const bp = BK + f.path; const dd = bp.slice(0, bp.lastIndexOf('/')); if (!(await ad.exists(dd))) await ad.mkdir(dd); await ad.write(bp, text); await V.modify(f, lines.join('\n')); }
    }
  }
  await ad.write('.work/out/__NAME__.json', JSON.stringify(R, null, 1));
  return `__NAME__: ${R.notes} notes read, ${R.changed} with links, ${R.links} links; JT/Tosefta skipped ${R.skipped_jt}; no daf note ${R.notarget}; by folder ${JSON.stringify(R.byFolder)}`;
})()