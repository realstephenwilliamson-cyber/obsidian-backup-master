(async () => {
  // Audit 14 Oct 2026 (read-only): text scans the area agents asked for. (a) letters ů đ ť ľ ő ķ ė ę ų į in converted library notes and
  // Tantraloka verse notes; (b) verse links followed by a lone digit (OCR-split verse numbers); (c) italic-split names (*Ze*ʿ*eir*);
  // (d) iota-subscript counts in the B6 Greek notes, before and after; (e) line diffs for three backup sets too deep to stage.
  // Writes .work/out/audit-1014-textscan.json. Memory guard 300 MB below the limit.
  const ad = app.vault.adapter, MC = app.metadataCache, T0 = Date.now();
  const LIM = performance.memory.jsHeapSizeLimit, heap = () => performance.memory.usedJSHeapSize; let peak = heap();
  const guard = w => { const h = heap(); if (h > peak) peak = h; if (h > LIM - 300e6) throw new Error('memory guard at ' + w + ': ' + Math.round(h / 1e6) + ' MB'); };
  const md = app.vault.getMarkdownFiles();
  const scope = md.filter(f => (f.path.startsWith('Library/') && ((MC.getFileCache(f) || {}).frontmatter || {}).source_pdf) || /^Texts\/Tantraloka\/Ahnika \d+\//.test(f.path) || f.path.startsWith('Texts/Bible/Jewish Annotated New Testament/') || f.path.startsWith('Texts/Aquinas/') || f.path.startsWith('Texts/Fathers/') || f.path.startsWith('Texts/Hobbes/'));
  const R = { when: new Date().toISOString(), scopeNotes: scope.length, letters: { perNote: [], rows: [], totals: {} }, splitVerse: [], italicSplit: {}, iota: [], diffs: {} };
  const LET = /[ůđťľőķėęųįŮĐŤĽŐĶĖĘŲĮ]/g;
  for (let i = 0; i < scope.length; i++) {
    const f = scope[i]; const t = await ad.read(f.path); const lines = t.split('\n');
    // (a)
    const m = t.match(LET); if (m) { const c = {}; for (const ch of m) { c[ch] = (c[ch] || 0) + 1; R.letters.totals[ch] = (R.letters.totals[ch] || 0) + 1; } R.letters.perNote.push([f.path, m.length, c]);
      if (R.letters.rows.length < 3000) lines.forEach((L, j) => { let mm; const re = new RegExp(LET.source, 'g'); while ((mm = re.exec(L)) && R.letters.rows.length < 3000) R.letters.rows.push([f.path, j + 1, mm[0], L.slice(Math.max(0, mm.index - 20), mm.index + 21)]); }); }
    // (b) links whose display ends in a digit and are followed by space + one digit (not a new reference)
    const c = MC.getFileCache(f);
    if (c && c.links && R.splitVerse.length < 3000) for (const l of c.links) { const L = lines[l.position.end.line] || ''; const after = L.slice(l.position.end.col, l.position.end.col + 14); const disp = l.displayText || l.link;
      if (/\d$/.test(disp) && /^ \d(?=$|[,;.)\]]| (?![A-Z1-4]))/.test(after)) R.splitVerse.push([f.path, l.position.end.line + 1, l.original.slice(0, 120), after]); }
    // (c)
    const it = t.match(/\*[^*\n]{1,20}\*[ʿʾ’']\*[^*\n]{1,20}\*/g); if (it) { const book = f.path.split('/').slice(0, 3).join('/'); R.italicSplit[book] = (R.italicSplit[book] || 0) + it.length; }
    if (i % 400 === 0) guard('scan ' + i);
  }
  // (d) iota subscripts
  const iota = s => { let n = 0; for (const ch of s) if (ch.normalize('NFD').includes('ͅ')) n++; return n; };
  const walk = async (p, out) => { const L = await ad.list(p); for (const x of L.files) out.push(x); for (const d of L.folders) await walk(d, out); };
  try { const b6 = []; await walk('.work/backup-phase7-2026-10-13/b6', b6); for (const b of b6) { const cur = b.replace('.work/backup-phase7-2026-10-13/b6/', ''); let after = null; try { after = iota(await ad.read(cur)); } catch (e) {} R.iota.push([cur, iota(await ad.read(b)), after]); } } catch (e) { R.iota = String(e); }
  guard('iota');
  // (e) diffs
  const diffSet = async (prefix, filter) => { const files = []; await walk(prefix.replace(/\/$/, ''), files); const out = [];
    for (const b of files.filter(x => x.endsWith('.md') && (!filter || filter.test(x)))) { const cur = b.slice(prefix.length); let A, B; try { A = (await ad.read(b)).split('\n'); } catch (e) { out.push([cur, 'backup unreadable']); continue; } try { B = (await ad.read(cur)).split('\n'); } catch (e) { out.push([cur, 'current missing']); continue; }
      const pairs = []; if (A.length === B.length) { for (let k = 0; k < A.length && pairs.length < 30; k++) if (A[k] !== B[k]) pairs.push([k + 1, A[k].slice(0, 500), B[k].slice(0, 500)]); }
      else { const sa = new Set(A), sb = new Set(B); const gone = A.filter(x => !sb.has(x)), added = B.filter(x => !sa.has(x)); pairs.push(['lines ' + A.length + ' -> ' + B.length, gone.slice(0, 15).map(x => x.slice(0, 400)), added.slice(0, 15).map(x => x.slice(0, 400))]); }
      out.push([cur, pairs]); }
    return out; };
  for (const [k, p] of [['d13', '.work/backup-phase7-2026-10-13/d13/'], ['late', '.work/backup-phase7-2026-10-13/late/'], ['refs14', '.work/backup-phase8-2026-10-14/refs/']]) { try { R.diffs[k] = await diffSet(p); } catch (e) { R.diffs[k] = String(e); } guard('diff ' + k); }
  R.seconds = Math.round((Date.now() - T0) / 1000); R.peakHeapMB = Math.round(peak / 1e6);
  await ad.write('.work/out/audit-1014-textscan.json', JSON.stringify(R));
  return `read-only textscan: ${scope.length} notes; letters ${JSON.stringify(R.letters.totals)}; split-verse ${R.splitVerse.length}; italic-split books ${Object.keys(R.italicSplit).length}; diffs ${Object.entries(R.diffs).map(([k, v]) => k + ' ' + (Array.isArray(v) ? v.length : v)).join(', ')}; ${R.seconds}s, peak ${R.peakHeapMB} MB`;
})()
