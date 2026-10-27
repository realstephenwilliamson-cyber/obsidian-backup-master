(async () => {
  // long-paths.js (26 Oct 2026): read-only. Lists the vault files whose full Windows path (the vault folder, a backslash, the path inside
  // the vault) is 240 characters or more. House rule 7 keeps every path at 240 or less; Windows and the Git backup stop at 259
  // (on 26 Oct 2026 two notes at 261 and 262 stopped a Git commit). Run it after renames, or before a Git commit that fails with
  // "Filename too long". Writes .work/out/long-paths.json. Changes nothing.
  const base = app.vault.adapter.getBasePath(), full = p => base.length + 1 + p.length;
  const rows = app.vault.getFiles().map(f => ({ len: full(f.path), path: f.path })).filter(x => x.len >= 240).sort((a, b) => b.len - a.len);
  const over = rows.filter(x => x.len > 259).length;
  await app.vault.adapter.write('.work/out/long-paths.json', JSON.stringify({ when: new Date().toISOString(), base, over259: over, rows }, null, 1));
  return `long-paths: ${rows.length} files at 240 or more (${over} over 259); longest ${rows.length ? rows[0].len : '-'}; list in .work/out/long-paths.json`;
})()
