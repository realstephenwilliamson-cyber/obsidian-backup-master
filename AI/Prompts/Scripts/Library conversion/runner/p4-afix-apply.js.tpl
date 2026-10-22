(async () => {
  // Phase 4 repair (9 Oct 2026): ä/å/Ä/Å that Tesseract's Latin model read for ā/Ā in OCR'd converted notes.
  // The replacement for each word comes from .work/p4/afix-map.json (made in the cloud by tools/afix.py from the words this
  // vault's notes contain: German words such as Universität, Bäumer kept; 'anå' -> 'and', 'shoulä' -> 'should'; else ä/å -> ā).
  // Only the body is changed, never the frontmatter or the target of a [[link]]. Books with Vedic accents are left out.
  // Backs up each changed note to .work/backup-phase4-afix/. window.DRY !== false -> report only.
  const DRY = window.DRY !== false;
  const ONLY = __ONLY__;   // null = all books, or a list of book paths (Library/<subject>/<book>)
  const A = app.vault.adapter, V = app.vault, MC = app.metadataCache;
  const BK = '.work/backup-phase4-afix/';
  const skip = ['A Sanskrit Reader (Lanman)', 'A Sanskrit Grammar (Whitney)', 'A Vedic Reader for Students (Macdonell)'];
  const MAP = JSON.parse(await A.read('.work/p4/afix-map.json'));
  const rep = { dry: DRY, notes_changed: 0, replacements: 0, books: {}, unmapped: {}, errors: [] };
  const mkdirs = async (p) => { let cur = ''; for (const x of p.split('/').slice(0, -1)) { cur = cur ? cur + '/' + x : x; if (!(await A.exists(cur))) await A.mkdir(cur); } };
  const RX = /\[\[[^\]\n]*\]\]|[\p{L}]*[äåÄÅ][\p{L}]*/gu;
  for (const f of V.getMarkdownFiles()) {
    if (!f.path.startsWith('Library/')) continue;
    if (skip.some(s => f.path.includes('/' + s + '/'))) continue;
    const book = f.path.split('/').slice(0, 3).join('/');
    if (ONLY && !ONLY.includes(book)) continue;
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || !fm.source_pdf || !fm.converted) continue;
    if (!/OCR|Tesseract/.test(String(fm.text_source || ''))) continue;
    try {
      const t = await V.read(f); if (!/[äåÄÅ]/.test(t)) continue;
      const m = t.match(/^---\n[\s\S]*?\n---\n/); const head = m ? m[0] : ''; const body = t.slice(head.length);
      let n = 0;
      const body2 = body.replace(RX, w => {
        if (w.startsWith('[[')) return w;
        if (Object.prototype.hasOwnProperty.call(MAP, w)) { n++; return MAP[w]; }
        rep.unmapped[w] = (rep.unmapped[w] || 0) + 1; return w;
      });
      if (!n) continue;
      rep.notes_changed++; rep.replacements += n;
      const b = rep.books[book] || (rep.books[book] = { notes: 0, words: 0 }); b.notes++; b.words += n;
      if (DRY) continue;
      const bp = BK + f.path; if (!(await A.exists(bp))) { await mkdirs(bp); await A.write(bp, t); }
      await V.modify(f, head + body2);
    } catch (e) { rep.errors.push(f.path + ': ' + e.message); }
  }
  await A.write('.work/out/p4-afix-' + (DRY ? 'dry' : 'real') + '__TAG__.json', JSON.stringify(rep, null, 1));
  return `${DRY ? 'DRY' : 'APPLIED'} notes ${rep.notes_changed}, replacements ${rep.replacements}, books ${Object.keys(rep.books).length}, unmapped kinds ${Object.keys(rep.unmapped).length}, errors ${rep.errors.length}`;
})()
