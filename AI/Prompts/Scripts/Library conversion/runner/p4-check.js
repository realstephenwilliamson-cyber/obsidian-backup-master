(async () => {
  // Phase 4 check: for each book folder in .work/p4/check-list.json ({folder: expectedPageAnchors}),
  // count the ^pgK blocks Obsidian registered, frontmatter validity, and the vault's unresolved links.
  const A = app.vault.adapter, V = app.vault, MC = app.metadataCache;
  const want = JSON.parse(await A.read('.work/p4/check-list.json'));
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  await sleep(1500);
  const rep = { when: new Date().toISOString(), books: {}, notes: V.getMarkdownFiles().length };
  for (const [folder, exp] of Object.entries(want)) {
    const files = V.getMarkdownFiles().filter(f => f.path === folder || f.path.startsWith(folder + '/'));
    let blocks = 0, badfm = 0, nofm = 0; const ids = new Set();
    for (const f of files) {
      const c = MC.getFileCache(f);
      if (!c) { nofm++; continue; }
      if (!c.frontmatter) nofm++;
      for (const k of Object.keys(c.blocks || {})) if (/^pg\d+$/.test(k)) { blocks++; ids.add(k); }
    }
    const missing = [];
    for (let k = 1; k <= exp; k++) if (!ids.has('pg' + k)) missing.push(k);
    rep.books[folder] = { notes: files.length, page_blocks: blocks, expected: exp, missing: missing.slice(0, 20), missing_n: missing.length, no_frontmatter: nofm };
  }
  let ul = 0, up = 0; const un = MC.unresolvedLinks; const notesWith = new Set();
  for (const [src, m] of Object.entries(un)) for (const [t, n] of Object.entries(m)) { ul += n; up++; notesWith.add(src); }
  rep.unresolved = { links: ul, pairs: up, notes: notesWith.size };
  rep.unresolved_in_books = Object.keys(un).filter(s => Object.keys(want).some(f => s === f || s.startsWith(f + '/')) && Object.keys(un[s]).length).map(s => [s, Object.keys(un[s])]);
  await A.write('.work/out/p4-check-' + Date.now() + '.json', JSON.stringify(rep, null, 1));
  return JSON.stringify({ notes: rep.notes, unresolved: rep.unresolved, books: Object.fromEntries(Object.entries(rep.books).map(([k, v]) => [k.split('/').pop(), `${v.page_blocks}/${v.expected} missing ${v.missing_n}`])) });
})()
