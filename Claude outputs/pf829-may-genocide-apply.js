// APPLY
(async () => {
  // pf829-may-genocide-apply (10 Nov 2026): files Larry May, Genocide: A Normative Account (Downloads/Add to Obsidian): the PDF to Library/Philosophy/, a catalog note in
  // Catalog/Philosophy/, a "See also" line on May's Limiting Leviathan note, May in Scholars.md (two works), and corrects pf823's miss
  // (Scholars.md: Knepper's line still said Other: String.replace changed only the first of the two). New files only; two small edits.
  const JOB = 'pf829-may-genocide-apply', ad = app.vault.adapter, DRY = window.DRY !== false, fs = require('fs'), path = require('path');
  const D = { when: new Date().toISOString(), dry: DRY, log: [], errors: [] }, L = s => D.log.push(s), E = s => D.errors.push(s);
  const base = ad.getBasePath(), get = p => app.vault.getAbstractFileByPath(p);
  const src = 'C:\\Users\\welln\\OneDrive\\Documents\\Downloads\\Add to Obsidian\\Genocide _ a normative account -- May, Larry -- Cambridge University Press, Cambridge, 2010 -- Cambridge ; New York _ Cambridge University Press.pdf';
  const dst = 'Library/Philosophy/May - Genocide - A Normative Account (2010).pdf';
  const note = 'Catalog/Philosophy/May - Genocide - A Normative Account.md';
  const unresBefore = Object.values(app.metadataCache.unresolvedLinks).reduce((a, m) => a + Object.keys(m).length, 0);
  if (!fs.existsSync(src)) E('no source'); else if (await ad.exists(dst)) E('exists ' + dst); else {
    L('copy PDF ' + fs.statSync(src).size + ' bytes -> ' + dst);
    if (!DRY) { fs.copyFileSync(src, path.join(base, dst)); await ad.reconcileFile?.(dst, dst); }
  }
  const text = `---
title: "Genocide: A Normative Account"
subtitle: ""
author:
  - Larry May
editor: []
translator: []
year: 2010
publisher: Cambridge University Press, Cambridge
series: ""
volume: ""
container: ""
subject:
  - Philosophy
type: book
language:
  - English
pages: 304
text: searchable
print: false
files:
  - "[[May - Genocide - A Normative Account (2010).pdf]]"
aliases:
  - Genocide A Normative Account
---

# Genocide: A Normative Account

\`\`\`dataviewjs
await dv.view("Templates/Views/open-pdf")
\`\`\`

**Checked against the file** on 10 Nov 2026: Title, author, publisher and year (first published 2010) from the title and copyright pages (ISBN 978-0-521-19465-5 hardback, 978-0-521-12296-2 paperback); the page count is the PDF's.

**Text layer:** the Internet Archive's OCR of a scanned library copy (2022). It reads well on the pages sampled, but expect slips; the first pages of the PDF are the Archive's cover notes and blanks.

See also: [[May - Limiting Leviathan - Hobbes on Law and International Affairs]] (the same author).
`;
  if (get(note) || await ad.exists(note)) E('exists ' + note); else { L('create ' + note); if (!DRY) await app.vault.create(note, text); }
  const ll = get('Catalog/Philosophy/May - Limiting Leviathan - Hobbes on Law and International Affairs.md');
  if (!ll) E('no Limiting Leviathan note'); else {
    const t = await app.vault.read(ll);
    if (t.includes('May - Genocide')) L('Limiting Leviathan: link already there'); else { L('append See also to Limiting Leviathan'); if (!DRY) await app.vault.process(ll, s => s.replace(/\s*$/, '\n\nSee also: [[May - Genocide - A Normative Account]] (the same author).\n')); }
  }
  const sc = get('Catalog/Scholars/Scholars.md');
  if (!sc) E('no Scholars.md'); else {
    const t = await app.vault.read(sc);
    const a = '- [[Timothy Knepper]] · Philosophy, Other', b = '- [[Emmanuel Levinas]] · Philosophy, Judaica · added 29 Oct 2026 (two works)';
    if (!t.includes(a)) E('Knepper line not as expected'); else if (!t.includes(b)) E('Levinas line not as expected'); else if (t.includes('Larry May')) E('May already in Scholars.md'); else {
      L('Scholars.md: Knepper line, Larry May line');
      if (!DRY) await app.vault.process(sc, s => s.replace(a, '- [[Timothy Knepper]] · Philosophy, Religious-Studies').replace(b, b + '\n- Larry May · Philosophy · added 10 Nov 2026 (two works)'));
    }
  }
  if (!DRY) { await new Promise(r => setTimeout(r, 4000)); D.unresBefore = unresBefore; D.unresAfter = Object.values(app.metadataCache.unresolvedLinks).reduce((a, m) => a + Object.keys(m).length, 0); const f = get(dst); D.pdfSize = f ? f.stat.size : null; D.noteUnresolved = Object.keys(app.metadataCache.unresolvedLinks[note] || {}); }
  await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1));
  return `${JOB}${DRY ? ' DRY' : ''}: ${D.log.length} steps, ${D.errors.length} errors${D.errors.length ? ': ' + D.errors.join(' | ').slice(0, 300) : ''}${DRY ? '' : '; unresolved ' + D.unresBefore + ' -> ' + D.unresAfter + '; pdf ' + D.pdfSize}`;
})()
