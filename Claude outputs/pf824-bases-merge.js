// APPLY
(async () => {
  // pf824-bases-merge (10 Nov 2026): Stephen asked: trash Needs review (Catalog.base's Review view does the same); merge Physical Library,
  // Shelf check and To delete into one Base, Library checks.base, with the three as views (same filters, columns and sorts as before).
  // The four old Bases go to the vault trash (nothing links to them: checked in pf821). Guide and prompt wording follows.
  const JOB = 'pf824-bases-merge', ad = app.vault.adapter, DRY = window.DRY !== false;
  const D = { when: new Date().toISOString(), dry: DRY, log: [], errors: [] };
  const L = s => D.log.push(s), E = s => D.errors.push(s), get = p => app.vault.getAbstractFileByPath(p);
  const done = async () => { await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1)); return `${JOB}${DRY ? ' DRY' : ''}: ${D.log.length} steps, ${D.errors.length} errors${D.errors.length ? ': ' + D.errors.slice(0, 3).join(' | ').slice(0, 300) : ''}`; };
  const base = `filters:
  and:
    - file.folder.startsWith("Catalog/")
    - type != "index"
    - file.folder != "Catalog/Scholars"
views:
  - type: table
    name: Physical Library
    filters:
      and:
        - note.print == true
    groupBy:
      property: subject
      direction: ASC
    order:
      - file.name
      - year
      - publisher
      - subject
    sort:
      - property: title
        direction: ASC
  - type: table
    name: Shelf check
    order:
      - file.name
      - print
      - subject
    sort:
      - property: subject
        direction: ASC
      - property: title
        direction: ASC
    columnSize:
      note.author: 168
      note.subject: 177
  - type: table
    name: To delete
    filters:
      and:
        - status == "delete"
    order:
      - file.name
      - files
    sort:
      - property: file.name
        direction: ASC
`;
  const NEW = 'Catalog/Library checks.base';
  if (get(NEW)) E('exists ' + NEW); else { L('create ' + NEW); if (!DRY) await app.vault.create(NEW, base); }
  for (const n of ['Needs review', 'Physical Library', 'Shelf check', 'To delete']) {
    const f = get(`Catalog/${n}.base`);
    if (!f) { E('missing ' + n); continue; }
    L('trash ' + f.path); if (!DRY) await app.vault.trash(f, false);
  }
  const rep = async (path, from, to, n) => {
    const f = get(path); if (!f) { E('no file ' + path); return; }
    const t = await app.vault.read(f), cnt = t.split(from).length - 1;
    if (cnt !== n) { E(`${path}: expected ${n} of ${from.slice(0, 50)}, found ${cnt}`); return; }
    L(`replace in ${path}: ${from.slice(0, 60)}`); if (!DRY) await app.vault.process(f, s => s.split(from).join(to));
  };
  await rep('Vault Guide.md', 'By author, By subject, Currently reading, Needs review, To delete, Physical Library, Shelf check, Stiegler', 'By author, By subject, Currently reading, Library checks (the views *Physical Library*, *Shelf check* and *To delete*), Stiegler', 1);
  await rep('Vault Guide.md', '(*Needs review* lists them)', '(the *Review* view of *Catalog.base* lists them)', 1);
  await rep('AI/Prompts/Check catalog notes against their files.md', 'notes are waiting in *Needs review* (', 'notes are waiting in the *Review* view of *Catalog.base* (', 1);
  await rep('AI/Prompts/Check catalog notes against their files.md', '*Needs review* in *Catalog.base* (or `Catalog/Needs review.base`) should be shorter', 'The *Review* view in *Catalog.base* should be shorter', 1);
  await rep('AI/Prompts/Prompts - read me.md', 'Settling *Needs review* items', 'Settling *Review* items', 1);
  return await done();
})()
