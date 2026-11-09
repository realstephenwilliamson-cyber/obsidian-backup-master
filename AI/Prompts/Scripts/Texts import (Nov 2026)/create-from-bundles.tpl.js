(async () => {
  // __JOB__ (9 Nov 2026): the Dead Sea Scrolls Study Edition into the vault. Bundles: __BUNDLES__ (in .work/xfer/enoch-2026-11-09/).
  // Dry run: no path or note name taken (all three bundles), the PDF in Downloads and its vault path free, the Texts.md edit found once.
  // APPLY (this job's bundles only): __PDFSTEP__ the notes through app.vault.create; __EDITSTEP__. Writes .work/out/__JOB__.detail.json.
  const JOB = '__JOB__', DIR = '.work/xfer/enoch-2026-11-09/', BK = '.work/backup-enoch-2026-11-09/';
  const ALL = ['dss-bundle-1.json', 'dss-bundle-2.json', 'dss-bundle-3.json'], MINE = __MINE__;
  const DO_PDF = __DO_PDF__, DO_EDIT = __DO_EDIT__;
  const fs = require('fs'), path = require('path'), ad = app.vault.adapter, base = ad.getBasePath();
  const SRC = 'C:\\Users\\welln\\OneDrive\\Documents\\Downloads\\Add to Obsidian\\The Dead Sea Scrolls Study Edition-Two Vol_ Set (Vol 1 & 2) -- Florentino Garcia Martinez, Eibert Tigchelaar -- 1999 -- Brill Academic Publishers.pdf';
  const PDF = 'Library/Judaica/Garcia Martinez, Tigchelaar (eds.) - The Dead Sea Scrolls Study Edition (1999).pdf';
  const EDIT = ['Texts/Texts.md', '- [[1 Enoch]]: R. H. Charles\'s translation (1917), one note per chapter\n\n## Mishnah, Zohar and Chasidut',
    '- [[1 Enoch]]: R. H. Charles\'s translation (1917), one note per chapter\n\n## Dead Sea Scrolls\n\n- [[Qumran]]: the English of García Martínez and Tigchelaar\'s *Study Edition* (1999), one note per manuscript, a block per line, in `Texts/Qumran`\n\n## Mishnah, Zohar and Chasidut'];
  const D = { when: new Date().toISOString(), dry: window.DRY !== false };
  const unres = () => { let f = 0, l = 0; for (const [, t] of Object.entries(app.metadataCache.unresolvedLinks)) { const n = Object.keys(t).length; if (n) { f++; l += n; } } return [f, l]; };
  D.unresolvedBefore = unres();
  const B = {}; for (const b of ALL) B[b] = JSON.parse(await ad.read(DIR + b));
  const names = new Map(); for (const f of app.vault.getFiles()) { const k = f.basename.toLowerCase(); names.set(k, (names.get(k) || []).concat(f.path)); }
  D.exists = []; D.clash = []; const seen = new Set();
  for (const b of (D.dry ? ALL : MINE)) for (const p of Object.keys(B[b])) {
    if (app.vault.getAbstractFileByPath(p)) D.exists.push(p);
    const n = p.split('/').pop().replace(/\.md$/, '').toLowerCase();
    if (names.has(n)) D.clash.push([p, names.get(n)]); if (seen.has(n)) D.clash.push([p, 'twice in bundles']); seen.add(n);
  }
  D.pdfSrc = fs.existsSync(SRC) ? fs.statSync(SRC).size : null; D.pdfDst = fs.existsSync(path.join(base, PDF));
  D.edit = (await ad.read(EDIT[0])).split(EDIT[1]).length - 1;
  const bad = D.exists.length || D.clash.length || (DO_PDF && (!D.pdfSrc || D.pdfDst)) || (DO_EDIT && D.edit !== 1);
  if (bad || D.dry) { await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1)); return `${JOB}${D.dry ? ' DRY' : ' STOP'}: files ${ALL.map(b => Object.keys(B[b]).length).join('+')}; exists ${D.exists.length}; clash ${D.clash.length}; pdf src ${D.pdfSrc} dst ${D.pdfDst}; edit ${D.edit}; unresolved ${D.unresolvedBefore}`; }
  const mk = async (p) => { const parts = p.split('/'); parts.pop(); let cur = ''; for (const x of parts) { cur = cur ? cur + '/' + x : x; if (!app.vault.getAbstractFileByPath(cur)) await app.vault.createFolder(cur); } };
  if (DO_PDF) { await mk(PDF); fs.copyFileSync(SRC, path.join(base, PDF)); await ad.reconcileFile(PDF, PDF); D.pdfCopied = fs.statSync(path.join(base, PDF)).size; }
  D.made = 0; for (const b of MINE) for (const [p, t] of Object.entries(B[b])) { await mk(p); await app.vault.create(p, t); D.made++; }
  if (DO_EDIT) {
    const f = app.vault.getAbstractFileByPath(EDIT[0]); const bp = BK + EDIT[0] + '.before-dss';
    if (!(await ad.exists(bp))) await ad.write(bp, await app.vault.read(f));
    await app.vault.process(f, x => x.replace(EDIT[1], EDIT[2])); D.edited = true;
  }
  await new Promise(r => setTimeout(r, 15000));
  D.unresolvedAfter = unres();
  await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1));
  return `${JOB} APPLY: made ${D.made}; pdf ${D.pdfCopied || '-'}; edit ${D.edited || '-'}; unresolved ${D.unresolvedBefore} -> ${D.unresolvedAfter}`;
})()
