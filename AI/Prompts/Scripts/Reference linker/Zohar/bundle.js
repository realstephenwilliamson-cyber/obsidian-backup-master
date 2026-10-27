(async () => {
  // pf258 (26 Oct 2026, third session): read-only. Bundle for the Zohar linking (the 1,789 plain main-Zohar references and S2's leftovers):
  // every note under Texts/Zohar except the Soncino folio notes, plus every other note (Journal/ and Projects/ left out) whose text has
  // "[[Zohar " or a Zohar folio reference (Zohar ... N:NNNa). With each Zohar note's block ids and the folio note list. ~9 MB parts in .work/xfer/zb27/.
  const fs = require('fs'), path = require('path'), base = app.vault.adapter.basePath, dst = path.join(base, '.work', 'xfer', 'zb27');
  fs.mkdirSync(dst, { recursive: true });
  const MC = app.metadataCache, folio = /^Zohar \d\.\d{2,3}[a-d]$/, ref = /Zohar[^\n]{0,60}?\b[1-3]:\d{1,3}[a-d]\b/;
  const notes = {}, blocks = {}, folioNotes = [];
  for (const f of app.vault.getMarkdownFiles()) {
    if (folio.test(f.basename)) { folioNotes.push(f.path); continue; }
    const inZ = f.path.startsWith('Texts/Zohar/');
    if (!inZ && (f.path.startsWith('Journal/') || f.path.startsWith('Projects/'))) continue;
    const t = await app.vault.cachedRead(f);
    if (inZ || t.includes('[[Zohar ') || ref.test(t)) { notes[f.path] = t; if (inZ) blocks[f.path] = Object.keys(MC.getFileCache(f)?.blocks || {}); }
  }
  const keys = Object.keys(notes).sort(); let part = [], size = 0, n = 0; const parts = [];
  const flush = () => { if (!part.length) return; n++; const o = {}; for (const k of part) o[k] = notes[k]; const fn = `part${String(n).padStart(2, '0')}.json`; fs.writeFileSync(path.join(dst, fn), JSON.stringify(o)); parts.push(fn); part = []; size = 0; };
  for (const k of keys) { const s = Buffer.byteLength(notes[k]) + k.length + 10; if (size + s > 9_000_000) flush(); part.push(k); size += s; }
  flush();
  fs.writeFileSync(path.join(dst, 'meta.json'), JSON.stringify({ when: new Date().toISOString(), parts, notes: keys.length, blocks, folioNotes }));
  return `pf258: ${keys.length} notes (${keys.filter(k => k.startsWith('Texts/Zohar/')).length} in Texts/Zohar), ${folioNotes.length} folio notes left out, ${parts.length} parts, ${Math.round(keys.reduce((s, k) => s + Buffer.byteLength(notes[k]), 0) / 1e6)} MB`;
})()
