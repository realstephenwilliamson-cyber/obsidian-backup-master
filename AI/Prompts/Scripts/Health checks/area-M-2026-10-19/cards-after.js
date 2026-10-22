(async () => {
  // Read-only after-check for the 108 card notes and the 4 CIS card notes (19 Oct 2026, completion chat).
  const mc = app.metadataCache, files = app.vault.getMarkdownFiles();
  const cards = files.filter(f => f.path.startsWith('Study/Sanskrit/Flashcards/Card ')).sort((a, b) => a.path.localeCompare(b.path));
  const cis = files.filter(f => f.path.startsWith('Study/Sanskrit/CIS cards/'));
  const unres = Object.entries(mc.unresolvedLinks).filter(([, o]) => Object.keys(o).length);
  const newUnres = unres.filter(([p]) => p.startsWith('Study/Sanskrit/Flashcards/') || p.startsWith('Study/Sanskrit/CIS cards/')).map(([p, o]) => p + ': ' + Object.keys(o).join(', '));
  const nums = new Set(), bad = [];
  for (const f of cards) {
    const fm = mc.getFileCache(f)?.frontmatter || {};
    if (fm.type !== 'flashcard') bad.push(f.path + ' type=' + fm.type);
    if (typeof fm.card !== 'number' || nums.has(fm.card)) bad.push(f.path + ' card=' + fm.card); nums.add(fm.card);
    if (fm.tags) bad.push(f.path + ' has tags');
    const t = await app.vault.cachedRead(f);
    const q = t.split('\n').filter(l => /::/.test(l) && !/^\s*(-|%%)/.test(l)).length;
    if (q !== 2) bad.push(f.path + ' card lines=' + q);
  }
  const base = app.vault.getAbstractFileByPath('Study/Sanskrit/Flashcards/Flashcards.base');
  const habits = app.vault.getAbstractFileByPath('Journal/Habits.base');
  const sizes = {};
  for (const p of ['Study/Sanskrit/Flashcards/Flashcards.base', 'Journal/Habits.base', 'Study/Sanskrit/CIS study plan.md', 'Templates/Daily note.md']) { const f = app.vault.getAbstractFileByPath(p); sizes[p] = f ? f.stat.size : 'MISSING'; }
  const out = { when: new Date().toISOString(), cards: cards.length, cis: cis.length, cardNumbers: nums.size, unresolvedFiles: unres.length, unresolvedLinks: unres.reduce((n, [, o]) => n + Object.values(o).reduce((a, b) => a + b, 0), 0), newUnresolved: newUnres, problems: bad, sizes };
  await app.vault.adapter.write('.work/out/cards-after.json', JSON.stringify(out, null, 1));
  return `cards ${cards.length} (numbers ${nums.size}), CIS notes ${cis.length}; unresolved ${unres.length} files / ${out.unresolvedLinks} links; new unresolved in the card folders: ${newUnres.length ? newUnres.join(' | ') : 'none'}; problems: ${bad.length ? bad.slice(0, 6).join(' | ') : 'none'}; sizes ${JSON.stringify(sizes)}`;
})()
