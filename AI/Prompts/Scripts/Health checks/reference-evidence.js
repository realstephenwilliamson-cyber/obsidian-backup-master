(async () => {
  // Phase 8, step 4 (read-only): evidence for the references in AI/Bible references to decide later.md (sections 1 and 2).
  // For each row: the full line, the reference as the linker parses it, and the candidate targets with their verse text:
  // H = the number as printed read as Hebrew numbering, E = read as English numbering (converted to the Hebrew note),
  // L = the LXX note as printed, N = the NRSVue verse at the printed number (English numbering). Writes .work/out/s85a-decide-prep.json.
  const V = app.vault, ad = V.adapter, MC = app.metadataCache, files = V.getMarkdownFiles();
  const src = await ad.read('AI/Prompts/Scripts/Reference linker/b3core.js');
  const B3 = eval(src.replace(/if \(typeof module[^\n]*\n?/, '') + '\n;B3');
  const VERSIF = JSON.parse(await ad.read('AI/Prompts/Scripts/Reference linker/versif-eng.json'));
  const blocksOf = f => ((MC.getFileCache(f) || {}).blocks) || {};
  const NTX = new Map(), TNX = new Map(), TOR = new Map(), LXX = new Map(), NRS = new Map(), DRB = new Map(); const torahMax = {};
  for (const f of files) {
    const p = f.path;
    if (p.startsWith('Texts/Bible/New Testament/')) { const m = f.basename.match(/^(.+) (\d+)$/); const id = m && B3.NAME2ID.get(m[1]); if (id) NTX.set(id + '|' + (+m[2]), f); }
    else if (p.startsWith('Texts/Bible/Tanakh/')) { const m = f.basename.match(/^(.+) (\d+)$/); const id = m && B3.NAME2ID.get(m[1]); if (id) TNX.set(id + '|' + (+m[2]), f); }
    else if (p.startsWith('Texts/Bible/Torah/')) { const bm = p.split('/')[3].match(/^\d+ (.+)$/); const id = bm && B3.NAME2ID.get(bm[1]); if (!id) continue; for (const b of Object.keys(blocksOf(f))) { const m = b.match(/^(\d+)-(\d+)$/); if (!m) continue; TOR.set(id + '|' + (+m[1]) + '|' + (+m[2]), f); const k = id + '|' + (+m[1]); torahMax[k] = Math.max(torahMax[k] || 0, +m[2]); } }
    else if (p.startsWith('Texts/Bible/LXX/')) { const fm = p.split('/')[3].match(/^\d+ (.+)$/); const nm = fm && fm[1].replace(/ \(Greek\)$/, ''); const id = nm && B3.NAME2ID.get(nm); const m = f.basename.match(/(\d+)$/); if (id && m) LXX.set(id + '|' + (+m[1]), f); }
    else if (p.startsWith('Texts/Bible/NRSVue/')) { const m = f.basename.match(/^NRSVue (.+) (\d+)$/); const id = m && B3.NAME2ID.get(m[1]); if (id) NRS.set(id + '|' + (+m[2]), f); }
    else if (p.startsWith('Texts/Bible/Douay-Rheims/')) { const fm = (p.split('/')[3] || '').match(/^\d+ (.+)$/); const id = fm && B3.NAME2ID.get(fm[1]); const m = f.basename.match(/(\d+)$/); if (id && m) DRB.set(id + '|' + (+m[1]), f); }
  }
  const DECA = [];
  if (torahMax['EXO|20'] === 23) DECA.push(['EXO', 20, 14, 16, 20, 13, 'all'], ['EXO', 20, 17, 17, 20, 14], ['EXO', 20, 18, 26, 20, 15]);
  if (torahMax['DEU|5'] === 30) DECA.push(['DEU', 5, 18, 20, 5, 17, 'all'], ['DEU', 5, 21, 21, 5, 18], ['DEU', 5, 22, 33, 5, 19]);
  const mapBy = (rows, id, c, v) => { for (const r of rows) if (r[0] === id && r[1] === c && v >= r[2] && v <= r[3]) return r[6] === 'all' ? [r[4], r[5]] : [r[4], r[5] + (v - r[2])]; return null; };
  const toHeb = (id, c, v) => mapBy(VERSIF, id, c, v) || mapBy(DECA, id, c, v) || [c, v];
  const textCache = {};
  const blockText = async (f, b) => { if (!f) return null; const bl = blocksOf(f)[b]; if (!bl) return null; const t = textCache[f.path] ?? (textCache[f.path] = await ad.read(f.path)); return t.slice(bl.position.start.offset, bl.position.end.offset).replace(/\s*\^[\w-]+\s*$/, '').replace(/\s+/g, ' ').slice(0, 360); };
  const target = async (kind, id, c, v) => {
    let f = null;
    if (kind === 'heb') f = B3.TORAH.has(id) ? TOR.get(id + '|' + c + '|' + v) : TNX.get(id + '|' + c);
    else if (kind === 'lxx') f = LXX.get(id + '|' + c);
    else if (kind === 'nrs') f = NRS.get(id + '|' + c);
    else if (kind === 'nt') f = NTX.get(id + '|' + c);
    else if (kind === 'drb') f = DRB.get(id + '|' + c);
    if (!f) return null; const b = c + '-' + v; const txt = await blockText(f, b); if (txt === null) return { target: f.basename + '#^' + b, missing: true };
    return { target: f.basename + '#^' + b, text: txt };
  };
  // rows of the decide-later note
  const note = (await ad.read('AI/Bible references to decide later.md')).split('\n'); let sec = null; const rows = [];
  for (const l of note) {
    if (l.startsWith('## ')) sec = l.slice(3, 4);
    const m = l.match(/^\| \[\[([^\]|]+)\\\|[^\]]*\]\] \| (\d+) \| (.*?) \| (.*?) \| (.*) \|$/);
    if (m && (sec === '1' || sec === '2')) rows.push({ sec, path: m[1] + '.md', line: +m[2], ref: m[3], why: m[4], ctx: m[5] });
  }
  const lineCache = {}; const items = []; let id = 0; const problems = [];
  for (const r of rows) {
    id++;
    const L = lineCache[r.path] ?? (lineCache[r.path] = (await ad.exists(r.path)) ? (await ad.read(r.path)).split('\n') : null);
    if (!L) { problems.push([id, r.path, 'no file']); continue; }
    const line = L[r.line]; if (line === undefined) { problems.push([id, r.path, 'no line ' + r.line]); continue; }
    const it = { id, sec: r.sec, path: r.path, line: r.line, ref: r.ref, why: r.why, ctx: r.ctx, lineText: line };
    // unlink the line so that continuations after an already linked head ("Ps 47:2, 6, 7") are parsed too; remember the links
    const links = []; let un = ''; const lre = /\[\[([^\]|]+?)(?:\\?\|([^\]]*))?\]\]/g; let lm, last = 0;
    while ((lm = lre.exec(line))) { const label = lm[2] !== undefined ? lm[2] : lm[1]; un += line.slice(last, lm.index); links.push({ a: un.length, b: un.length + label.length, target: lm[1], label }); un += label; last = lm.index + lm[0].length; }
    un += line.slice(last); it.unlinked = un;
    let found = [];
    try { found = B3.find(un, {}); } catch (e) { it.parseError = String(e.message); }
    const same = found.filter(x => x.text === r.ref && (x.kind === 'bible' || x.kind === 'bible-list' || x.kind === 'bible-verse' || x.kind === 'chapter' || x.kind === 'ta' || x.kind === 'ta-list'));
    let pick = same[0];
    if (same.length > 1) { const key = r.ctx.replace(/\\\|/g, '|').trim(); let at = un.indexOf(key.slice(0, 40)); if (at < 0) at = un.indexOf(key.slice(-40)); if (at < 0) at = 0; const center = at + Math.min(key.length, 160) / 2; pick = same.reduce((best, x) => (Math.abs(x.a - center) < Math.abs(best.a - center) ? x : best), same[0]); it.ambiguousText = same.length; }
    if (!pick) { it.unparsed = found.map(x => x.text).slice(0, 12); items.push(it); continue; }
    it.parsed = { kind: pick.kind, id: pick.id, ch: pick.ch, v: pick.v, range: pick.range || null, text: pick.text, at: pick.a };
    const selfLink = links.find(l => l.a <= pick.a && l.b >= pick.b); if (selfLink) it.alreadyLinked = selfLink.target;
    const head = found.find(x => x.grp === pick.grp && x.kind !== 'bible-list' && x.kind !== 'bible-verse');
    if (head && head !== pick) { const hl = links.find(l => l.a <= head.a && l.b >= head.b); let numbering = null; if (hl) { const mm = hl.target.match(/#\^(\d+)-(\d+)$/); if (mm) numbering = (+mm[1] === head.ch && +mm[2] === head.v) ? 'unshifted' : 'eng'; } it.head = { text: head.text, id: head.id, ch: head.ch, v: head.v, link: hl ? hl.target : null, numbering }; }
    // other linked references on the line whose anchor differs from the printed number: evidence of English numbering in this line
    it.lineShifted = links.filter(l => { const mm = l.target.match(/#\^(\d+)-(\d+)$/); const fm = l.label.match(/(\d+)[:.](\d+)/); return mm && fm && (+mm[1] !== +fm[1] || +mm[2] !== +fm[2]); }).map(l => l.label + '→' + l.target.split('#^')[1]).slice(0, 6);
    if (pick.kind === 'ta' || pick.kind === 'ta-list') { const n = `Tantraloka ${String(pick.ch).padStart(2, '0')}.${String(pick.v).padStart(3, '0')}`; it.cands = { TA: { target: n, exists: !!MC.getFirstLinkpathDest(n, '') } }; const mx = files.filter(f => f.basename.startsWith(`Tantraloka ${String(pick.ch).padStart(2, '0')}.`) && /^Tantraloka \d\d\.\d\d\d$/.test(f.basename)).length; it.cands.chapterVerses = mx; items.push(it); continue; }
    const bid = pick.id, c = pick.ch, v = pick.v;
    const cands = {};
    if (B3.NT.has(bid)) { cands.NT = await target('nt', bid, c, v); cands.N = await target('nrs', bid, c, v); }
    else if (B3.DEUTERO.has(bid)) { cands.L = await target('lxx', bid, c, v); cands.N = await target('nrs', bid, c, v); }
    else {
      cands.H = await target('heb', bid, c, v);
      const heb = toHeb(bid, c, v); cands.E = (heb[0] === c && heb[1] === v) ? 'same as H' : Object.assign({ heb }, await target('heb', bid, heb[0], heb[1]) || { target: null, missing: true });
      cands.L = await target('lxx', bid, c, v);
      cands.N = await target('nrs', bid, c, v);
      cands.D = await target('drb', bid, c, v);
    }
    it.cands = cands; items.push(it);
  }
  await ad.write('.work/out/s85a2-decide-prep.json', JSON.stringify({ when: new Date().toISOString(), rows: rows.length, items, problems }, null, 1));
  const unparsed = items.filter(x => !x.parsed).length;
  return `decide-prep: rows ${rows.length}, items ${items.length}, unparsed ${unparsed}, problems ${problems.length}; indexes nt ${NTX.size} tanakh ${TNX.size} torah ${TOR.size} lxx ${LXX.size} nrsvue ${NRS.size} drb ${DRB.size}`;
})()
