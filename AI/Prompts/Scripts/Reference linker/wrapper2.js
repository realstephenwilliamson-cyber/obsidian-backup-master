
  // ---- Reference linker (first used 13 Oct 2026 as B3). DRY: report only. With window.B3APPLY = true: write the links (backups first).
  const APPLY = window.B3APPLY === true;
  const MC = app.metadataCache, ad = app.vault.adapter, files = app.vault.getMarkdownFiles();
  const T0 = Date.now(), R = { apply: APPLY, counts: {}, bySubject: {}, byBook: {}, notes: 0, notesWithLinks: 0, skipped: { foreign: 0, heading: 0, skippedNotes: 0, listHeld: 0, excluded: 0 }, missing: [], shifted: [], undecided: [], foreignSample: [], survey: {}, checks: {}, numbering: {} };
  const P = [];   // proposals
  const inc = (o, k, n = 1) => { o[k] = (o[k] || 0) + n; };
  const blocksOf = f => new Set(Object.keys(((MC.getFileCache(f) || {}).blocks) || {}));
  // ---- indexes
  const NTX = new Map(), TNX = new Map(), TOR = new Map(), LXX = new Map(), ZOH = new Map(), TAX = new Set(), TAMAX = {}, AVX = new Map();
  const torahMax = {};
  const ZSUB = /Tosefta|Sitrei|Ra'aya|Raaya|Piqqudin|Midrash ha-Ne|Passages|Matnitin|Heikhalot|Idra|Sava|Yanuqa|Raza/;
  for (const f of files) {
    const p = f.path;
    if (p.startsWith('Texts/Bible/New Testament/')) { const m = f.basename.match(/^(.+) (\d+)$/); const id = m && B3.NAME2ID.get(m[1]); if (id) NTX.set(id + '|' + (+m[2]), { name: f.basename, blocks: blocksOf(f) }); }
    else if (p.startsWith('Texts/Bible/Tanakh/')) { const m = f.basename.match(/^(.+) (\d+)$/); const id = m && B3.NAME2ID.get(m[1]); if (id) TNX.set(id + '|' + (+m[2]), { name: f.basename, blocks: blocksOf(f) }); }
    else if (p.startsWith('Texts/Bible/Torah/')) {
      const bm = p.split('/')[3].match(/^\d+ (.+)$/); const id = bm && B3.NAME2ID.get(bm[1]); if (!id) continue;
      for (const b of blocksOf(f)) { const m = b.match(/^(\d+)-(\d+)$/); if (!m) continue; TOR.set(id + '|' + (+m[1]) + '|' + (+m[2]), f.basename); const k = id + '|' + (+m[1]); torahMax[k] = Math.max(torahMax[k] || 0, +m[2]); }
    }
    else if (p.startsWith('Texts/Bible/LXX/')) { const fm = p.split('/')[3].match(/^\d+ (.+)$/); const nm = fm && fm[1].replace(/ \(Greek\)$/, ''); const id = nm && B3.NAME2ID.get(nm); const m = f.basename.match(/(\d+)$/); if (id && m) LXX.set(id + '|' + (+m[1]), { name: f.basename, blocks: blocksOf(f) }); }
    else if (p.startsWith('Texts/Zohar/')) {
      const sef = p.includes('/Sefaria/'), sub = ZSUB.test(f.basename), rank = sef ? 2 : sub ? 1 : 0;
      for (const b of blocksOf(f)) { if (!/^z(?:[123]|h)-\d+[a-d]$/.test(b)) continue; const all = ZOH.get(b) || []; all.push({ name: f.basename, rank }); ZOH.set(b, all); }
    }
    else if (p.startsWith('Texts/Tantraloka/') && /^Tantraloka \d\d\.\d\d\d$/.test(f.basename)) { TAX.add(f.basename); const c = +f.basename.slice(11, 13), v = +f.basename.slice(14); TAMAX[c] = Math.max(TAMAX[c] || 0, v); }
    else if (p.startsWith('Texts/Pirkei Avot/')) { const m = f.basename.match(/^Pirkei Avot (\d+)$/); if (m) AVX.set(+m[1], { name: f.basename, blocks: blocksOf(f) }); }
  }
  for (const v of ZOH.values()) v.sort((a, b) => a.rank - b.rank);
  R.checks.index = { nt: NTX.size, tanakh: TNX.size, torahVerses: TOR.size, lxx: LXX.size, zoharBlocks: ZOH.size, ta: TAX.size, avot: AVX.size, exo20max: torahMax['EXO|20'], deu5max: torahMax['DEU|5'] };
  // ---- numbering: English -> Hebrew (Copenhagen Alliance eng.json, CC BY-SA 4.0); the vault's Torah notes divide the
  // Decalogue as Sefaria does (Exod 20:13, Deut 5:17 hold four commandments), English Bibles and the BHS do not
  const DECA = [];
  if (torahMax['EXO|20'] === 23) DECA.push(['EXO', 20, 14, 16, 20, 13, 'all'], ['EXO', 20, 17, 17, 20, 14], ['EXO', 20, 18, 26, 20, 15]);
  if (torahMax['DEU|5'] === 30) DECA.push(['DEU', 5, 18, 20, 5, 17, 'all'], ['DEU', 5, 21, 21, 5, 18], ['DEU', 5, 22, 33, 5, 19]);
  R.checks.decalogue = DECA.length ? 'Sefaria division in the Torah notes: Exod 20 and Deut 5 mapped' : 'no Decalogue mapping';
  const mapBy = (rows, id, c, v) => { for (const r of rows) if (r[0] === id && r[1] === c && v >= r[2] && v <= r[3]) return r[6] === 'all' ? [r[4], r[5]] : [r[4], r[5] + (v - r[2])]; return null; };
  const toHeb = (id, c, v) => mapBy(VERSIF, id, c, v) || mapBy(DECA, id, c, v) || [c, v];
  const decaOnly = (id, c, v) => mapBy(DECA, id, c, v) || [c, v];
  const inDeca = (id, c, v) => (id === 'EXO' && c === 20 && v >= 14) || (id === 'DEU' && c === 5 && v >= 18);
  const BOOK = p => { const s = p.split('/'); return s.length > 3 ? s.slice(0, 3).join('/') : p; };
  const SKIPNOTE = /(?:^|[^\p{L}])(?:index|indices|indexes|register|contents|front matter|acknowledg\w*|abbreviations|list of contributors|about the author|title pages?)(?:[^\p{L}]|$)/iu;
  const FATHERS = /Maximus|Constas|Berthold|Sherwood|Thalassios|Ambigua|Catena|Apostolic Fathers/;
  const FATHERCTX = /Augustine|Jerome|Vulgate|Vulg\.|Septuagint|LXX|Bernard|Aquinas|Origen|Cassian|Chrysostom|Ambrose|Cassiodorus|Athanasius|Jerusalem Bible|Douay/;
  const VERSTALK = /\b(?:NJPS|JPS|Hebrew (?:printings?|text|numbering|Bible)|Masoretic|MT|English (?:numbering|versions?|Bibles?|translations?)|in (?:the )?(?:RSV|NRSV|KJV|AV|NAB|NJB|JB))\b/;
  const RABBINIC = /Mekhilta|Mekilta|Sifre|Midrash|Rashi|Targum|Rabbah|Lauterbach|JPS|NJPS|Talmud/;
  // reviewers' decisions (13 Oct 2026), by book: 'heb' = already Hebrew numbers, 'eng' = English, 'mixed' = shifted refs left for Stephen
  const OVERRIDE = {
    'Legal Revision and Religious Renewal in Ancient Israel (Levinson)': 'heb', 'Phenomenology and Mysticism (Steinbock)': 'heb', 'Memory, History, Forgetting (Ricoeur)': 'heb',
    'The Aryeh Kaplan Anthology (Kaplan)': 'heb', 'Deity and Divine Agency in the Hebrew Bible (McClellan)': 'heb',
    'Daily Prayers (Katz)': 'mixed', 'Theological-Political Treatise (de Spinoza)': 'mixed', 'Text and Tradition (Ehrman).md': 'mixed', 'The Orthodox Corruption of Scripture (Ehrman)': 'mixed',
    'An Introduction to the New Testament Manuscripts (Parker)': 'mixed', 'A Handbook of Ancient Religions (Hinnells)': 'mixed', 'Religion and Time (Balslev)': 'mixed', 'Incarnation in Hinduism and Christianity (Bassuk)': 'mixed',
    'Playing with Leviathan (van Bekkum)': 'mixed', "Jesus Our Priest (O'Collins)": 'mixed', 'Magnifica Humanitas (Leo XIV)': 'mixed', 'Mysticism in Shaivism and Christianity (Baumer)': 'mixed', 'Samarasya (Das)': 'mixed',
    'Ancient Israel in Sinai (Hoffmeier)': 'mixed', 'The Use of the Old Testament in the New Testament (McClellan).md': 'mixed',
    'Book of Common Prayer 1928 (text)': 'eng', 'A History of Anglican Liturgy (Cuming)': 'eng'
  };
  // single references the reviewers found wrong that no rule catches: [book folder, text as printed]
  const EXCLUDE = [['Playing with Leviathan (van Bekkum)', 'Ps 44:9–26'], ['The Collection of the Words of the Lord (Frank)', 'Zohar 1.37a']];
  const hebValid = (id, c, v) => B3.TORAH.has(id) ? TOR.has(id + '|' + c + '|' + v) : !!(TNX.get(id + '|' + c) && TNX.get(id + '|' + c).blocks.has(c + '-' + v));
  const engValid = (id, c, v) => v >= 1 && !!(ENGMAX[id] && c <= ENGMAX[id].length && v <= ENGMAX[id][c - 1]);
  // scope: by default the converted books; window.B3SCOPE = ['Texts/Plato/', ...] to run over other folders instead
  const conv = window.B3SCOPE ? files.filter(f => window.B3SCOPE.some(s => f.path.startsWith(s))) : files.filter(f => f.path.startsWith('Library/') && ((MC.getFileCache(f) || {}).frontmatter || {}).source_pdf);
  let seed = 7; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  const optsFor = f => { const subj = f.path.split('/')[1]; return { noChapter: !['Biblical-Studies', 'Judaica', 'Christianity'].includes(subj) }; };
  // ---- pass 1: evidence per book (numbering, Tantraloka sanity)
  const EV = {};
  for (const f of conv) {
    if (SKIPNOTE.test(f.basename)) continue;
    const bk = BOOK(f.path); const e = EV[bk] = EV[bk] || { heb: 0, eng: 0, hebEx: [], engEx: [], ta: 0, taOut: 0 };
    const fathers = FATHERS.test(f.path);
    const lines = (await ad.read(f.path)).split('\n'); let inFm = lines[0] === '---', inCode = false;
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (inFm) { if (i > 0 && line === '---') inFm = false; continue; }
      if (/^\s*```/.test(line)) { inCode = !inCode; continue; }
      if (inCode || /^#{1,6}\s/.test(line) || B3.scriptShare(line) > 0.3) continue;
      for (const r of B3.find(line, optsFor(f))) {
        if (r.kind === 'ta') { e.ta++; if (!TAX.has(`Tantraloka ${String(r.ch).padStart(2, '0')}.${String(r.v).padStart(3, '0')}`)) e.taOut++; continue; }
        if (fathers || r.kind !== 'bible' || !r.id || B3.NT.has(r.id) || B3.DEUTERO.has(r.id) || !ENGMAX[r.id]) continue;
        const after = line.slice(r.b, r.b + 16);
        if (/^\s?(?:\(|\\?\[)\s?(?:Eng(?:lish)?|ET|EVV?|RSV|NRSV|KJV)\b/i.test(after)) { e.heb += 5; if (e.hebEx.length < 4) e.hebEx.push(r.text + ' [Eng…]'); continue; }
        if (/^\s?(?:\(|\\?\[)\s?(?:Heb(?:rew)?|MT)\b/i.test(after)) { e.eng += 5; if (e.engEx.length < 4) e.engEx.push(r.text + ' [Heb…]'); continue; }
        if (inDeca(r.id, r.ch, r.v) || (r.id === 'EXO' && r.ch === 20) || (r.id === 'DEU' && r.ch === 5)) continue;
        const ends = [[r.ch, r.v]]; if (r.range && !String(r.range).includes(':')) ends.push([r.ch, +r.range]);
        for (const [c, v] of ends) {
          const h = hebValid(r.id, c, v), en = engValid(r.id, c, v);
          if (h && !en) { e.heb++; if (e.hebEx.length < 4) e.hebEx.push(r.text); }
          if (en && !h) { e.eng++; if (e.engEx.length < 4) e.engEx.push(r.text); }
        }
      }
    }
  }
  const NUMB = {}, TABAD = new Set();
  for (const [bk, e] of Object.entries(EV)) {
    const name = bk.split('/').slice(2).join('/'); const def = bk.split('/')[1] === 'Judaica' ? 'heb' : 'none';
    let d = def, why = 'default';
    if (!e.heb && e.eng >= (def === 'heb' ? 2 : 1)) { d = 'eng'; why = 'evidence'; }
    else if (!e.eng && e.heb >= 2) { d = 'heb'; why = 'evidence'; }
    else if (e.heb && e.eng) { d = e.heb >= 3 * e.eng + 2 ? 'heb' : e.eng >= 3 * e.heb + 2 ? 'eng' : 'mixed'; why = 'evidence'; }
    if (FATHERS.test(bk)) { d = 'mixed'; why = 'Church Father translation'; }
    if (OVERRIDE[name]) { d = OVERRIDE[name]; why = 'reviewed'; }
    NUMB[bk] = d;
    if (e.heb || e.eng || why !== 'default') R.numbering[bk] = { decided: d, why, hebOnly: e.heb, engOnly: e.eng, hebEx: e.hebEx, engEx: e.engEx };
    if (e.ta >= 4 && e.taOut / e.ta > 0.25) { TABAD.add(bk); R.numbering[bk] = Object.assign(R.numbering[bk] || {}, { ta: e.ta, taOutOfRange: e.taOut, taDecision: 'volume/page citations: not linked' }); }
  }
  // ---- resolving one reference
  const zoharTarget = (block, before) => {
    const all = ZOH.get(block); if (!all) return null;
    const named = before.match(ZSUB); if (named) { const x = all.find(z => z.name.includes(named[0])); if (x) return x.name; }
    return all[0].name;
  };
  const linkFor = (r, subj, line, bk) => {
    const before = line.slice(Math.max(0, r.a - 30), r.a), after = line.slice(r.b, r.b + 16);
    if (r.kind === 'ta' || r.kind === 'ta-list') {
      if (TABAD.has(bk)) return { undecided: 'this book cites the Tantrāloka by volume and page' };
      const n = `Tantraloka ${String(r.ch).padStart(2, '0')}.${String(r.v).padStart(3, '0')}`;
      if (!TAX.has(n)) return { miss: n };
      if (TAMAX[r.ch] && r.v > TAMAX[r.ch] - 3) return { undecided: 'within 3 verses of the chapter end (the KSTS count may differ)' };
      return { target: n };
    }
    if (r.kind === 'zohar') { const z = zoharTarget(r.block, before); return z ? { target: z + '#^' + r.block } : { miss: r.block }; }
    if (r.kind === 'avot') { if ((r.ch === 5 && r.v >= 20) || r.ch === 6) return { undecided: 'Avot 5:20 on and chapter 6 are numbered differently in editions' }; const a = AVX.get(r.ch); return a && a.blocks.has(r.ch + '-' + r.v) ? { target: a.name + '#^' + r.ch + '-' + r.v } : { miss: 'Avot ' + r.ch + ':' + r.v }; }
    const id = r.id;
    if (['Hinduism', 'Sanskrit', 'Trika'].includes(subj) && /^(?:Song|Ex)$/.test(r.name || '')) return { skip: true };
    if (/(LXX|Septuagint|Vulg\.?|Vulgate)\s?$/.test(before.slice(-14))) { const x = LXX.get(id + '|' + r.ch); if (x && x.blocks.has(r.ch + '-' + r.v)) return { target: x.name + '#^' + r.ch + '-' + r.v, lxx: true }; return { undecided: 'LXX reference with no LXX note for it' }; }
    if (/^\s?\(?\s?(?:Sept|LXX|Vulg|Vulgate)\b/.test(after)) return { undecided: 'marked as Septuagint or Vulgate numbering' };
    if (r.alt && !/^\s?\(\d{4}/.test(after)) return { undecided: 'a second number follows in brackets (another numbering?)' };
    if (id === 'HEB' && r.dot && /\(\s?$/.test(before) && r.prevEnd != null && r.a - r.prevEnd < 30) return { undecided: '"(Heb." right after another reference: probably the Hebrew numbering' };
    if (/^\s?(?:\(|\\?\[)\s?(?:Eng(?:lish)?|ET|EVV?|Heb(?:rew)?|MT|LXX|English|Hebrew|RSV|NRSV|KJV)\b/i.test(after) || /(?:\(|\\?\[)\s?(?:Eng|Heb|MT|English|Hebrew|RSV|NRSV|KJV)\.?,?\s?$/.test(before)) return { undecided: 'a second numbering is given beside it' };
    if (B3.NT.has(id)) { const x = NTX.get(id + '|' + r.ch); if (x && x.blocks.has(r.ch + '-' + r.v)) return { target: x.name + '#^' + r.ch + '-' + r.v }; return { miss: id + ' ' + r.ch + ':' + r.v }; }
    if (B3.DEUTERO.has(id)) { const x = LXX.get(id + '|' + r.ch); if (x && x.blocks.has(r.ch + '-' + r.v)) return { target: x.name + '#^' + r.ch + '-' + r.v }; return { miss: id + ' ' + r.ch + ':' + r.v + ' (LXX)' }; }
    const fathers = FATHERS.test(r.path);
    if (fathers && (id === 'PSA' || ['1SA', '2SA', '1KI', '2KI'].includes(id) || (id === 'DAN' && [3, 13, 14].includes(r.ch)))) return { undecided: 'Church Father translation: LXX book names or numbering possible' };
    if (id === 'PSA' && FATHERCTX.test(line.slice(Math.max(0, r.a - 300), r.b + 300))) return { undecided: 'Psalm near a Latin or Greek Father, Vulgate or LXX: numbering unsure' };
    const nb = NUMB[BOOK(r.path)] || (subj === 'Judaica' ? 'heb' : 'none');
    let heb = nb === 'heb' ? (subj === 'Judaica' ? [r.ch, r.v] : decaOnly(id, r.ch, r.v)) : toHeb(id, r.ch, r.v);
    if (subj === 'Judaica' && nb === 'heb' && inDeca(id, r.ch, r.v) && !hebValid(id, r.ch, r.v)) heb = decaOnly(id, r.ch, r.v);
    if (r.kind === 'chapter' && heb[0] === r.ch) heb = [r.ch, 1];
    const shifted = heb[0] !== r.ch || heb[1] !== r.v;
    if (shifted && inDeca(id, r.ch, r.v) && RABBINIC.test(line.slice(Math.max(0, r.a - 80), r.b + 80))) return { undecided: 'Decalogue verse near a rabbinic source (JPS numbering?)' };
    if (shifted && nb !== 'eng' && !(nb === 'heb' && subj !== 'Judaica')) return { undecided: nb === 'mixed' ? 'the book mixes Hebrew and English numbering' : 'English numbering assumed but not shown in this book', heb };
    if (shifted && VERSTALK.test(B3.sentenceAround(line, r.a, r.b))) return { undecided: 'the sentence discusses verse numbering', heb };
    if (B3.TORAH.has(id)) { const n = TOR.get(id + '|' + heb[0] + '|' + heb[1]); return n ? { target: n + '#^' + heb[0] + '-' + heb[1], shifted, heb } : { miss: id + ' ' + heb[0] + ':' + heb[1] }; }
    const x = TNX.get(id + '|' + heb[0]); if (x && x.blocks.has(heb[0] + '-' + heb[1])) return { target: x.name + '#^' + heb[0] + '-' + heb[1], shifted, heb };
    return { miss: id + ' ' + heb[0] + ':' + heb[1] };
  };
  // ---- pass 2: proposals (and, with APPLY, the edits)
  const BK = (window.B3BACKUP || '.work/backup-links-' + new Date().toISOString().slice(0, 10)).replace(/\/$/, '') + '/', changedNotes = [];
  const ensureAd = async p => { let c = ''; for (const x of p.split('/').slice(0, -1)) { c = c ? c + '/' + x : x; if (!(await ad.exists(c))) await ad.mkdir(c); } };
  const unres = () => { let fl = 0, l = 0; for (const m of Object.values(MC.unresolvedLinks)) { const k = Object.keys(m); if (k.length) { fl++; for (const x of k) l += m[x]; } } return { files: fl, links: l }; };
  if (APPLY) R.unresolvedBefore = unres();
  for (const f of conv) {
    R.notes++;
    if (SKIPNOTE.test(f.basename)) { R.skipped.skippedNotes++; continue; }
    const subj = f.path.split('/')[1], bk = BOOK(f.path); const t = await ad.read(f.path); const lines = t.split('\n');
    const excl = EXCLUDE.filter(([b]) => f.path.includes(b)).map(x => x[1]);
    let inFm = lines[0] === '---', inCode = false, nlinks = 0; const edits = new Map();
    for (const ch of ['Š', 'š', '˚', 'ň']) { const n = t.split(ch).length - 1; if (n) { R.survey[bk] = R.survey[bk] || {}; inc(R.survey[bk], ch, n); } }
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (inFm) { if (i > 0 && line === '---') inFm = false; continue; }
      if (/^\s*```/.test(line)) { inCode = !inCode; continue; }
      if (inCode || !line.trim()) continue;
      if (/^#{1,6}\s/.test(line)) { if (B3.find(line).length) R.skipped.heading++; continue; }
      const refs = B3.find(line, optsFor(f)); if (!refs.length) continue;
      const table = line.trim().startsWith('|'), lineForeign = B3.scriptShare(line) > 0.3;
      const quoteLine = line.startsWith('>') && B3.foreign(line.replace(/^>\s?/, ''));
      const res = []; let prevEnd = null;
      for (const r of refs) {
        r.prevEnd = prevEnd; prevEnd = r.b; r.path = f.path;
        const it = B3.italicAround(line, r.a), qu = B3.quoteAround(line, r.a);
        const near = line.slice(Math.max(0, r.a - 40), r.b + 40);
        const isTa = r.kind === 'ta' || r.kind === 'ta-list';
        if (isTa ? (B3.scriptShare(near) > 0.5 && !/[॥।]|\|\|/.test(near)) : (lineForeign || quoteLine || (it && B3.foreign(it)) || (qu && B3.foreign(qu)))) {
          R.skipped.foreign++; if (R.foreignSample.length < 30 && rnd() < 0.2) R.foreignSample.push({ path: f.path, text: r.text, ctx: line.slice(Math.max(0, r.a - 100), r.b + 60) }); res.push({ r, drop: 'foreign' }); continue;
        }
        if (excl.includes(r.text)) { R.skipped.excluded++; res.push({ r, drop: 'excluded' }); continue; }
        res.push({ r, x: linkFor(r, subj, line, bk) });
      }
      // a list whose head or any member fails is held back whole ("John 18:151, 18:152, 19:17" in the Mandaean Book of John)
      const badGrp = new Set(res.filter(o => o.x && (o.x.miss || o.x.undecided)).map(o => o.r.grp).filter(g => g != null));
      for (const o of res) {
        const { r, x } = o; if (!x) continue;
        if (x.skip) continue;
        if (x.undecided) { R.undecided.push({ path: f.path, line: i, text: r.text, why: x.undecided, heb: x.heb ? x.heb.join(':') : undefined, ctx: line.slice(Math.max(0, r.a - 120), r.b + 80) }); continue; }
        if (x.miss) { inc(R.counts, 'missing'); if (R.missing.length < 600) R.missing.push({ path: f.path, text: r.text, target: x.miss, ctx: line.slice(Math.max(0, r.a - 80), r.b + 40) }); continue; }
        if (r.grp != null && badGrp.has(r.grp)) { R.skipped.listHeld++; continue; }
        const kind = r.id ? (B3.NT.has(r.id) ? 'NT' : B3.DEUTERO.has(r.id) ? 'deutero' : B3.TORAH.has(r.id) ? 'Torah' : 'Tanakh') + (r.kind === 'chapter' ? ' chapter' : r.kind === 'bible-verse' ? ' verse-list' : '') + (x.lxx ? ' (LXX)' : '') : r.kind.replace('-list', '');
        inc(R.counts, kind); inc(R.bySubject, subj); if (r.id) inc(R.byBook, r.id); nlinks++;
        P.push([f.path, i, r.a, r.b, r.text, x.target, kind, x.shifted ? 1 : 0, table ? 1 : 0, line.slice(Math.max(0, r.a - 160), r.b + 100)]);
        if (x.shifted && R.shifted.length < 3000) R.shifted.push({ path: f.path, text: r.text, heb: x.heb.join(':'), target: x.target, sentence: B3.sentenceAround(line, r.a, r.b).slice(0, 400) });
        if (APPLY) { const e = edits.get(i) || []; e.push([r.a, r.b, `[[${x.target}${table ? '\\|' : '|'}${r.text}]]`]); edits.set(i, e); }
      }
    }
    if (nlinks) R.notesWithLinks++;
    if (APPLY && edits.size) {
      const nl = lines.slice();
      for (const [i, e] of edits) {
        let s = nl[i]; for (const [a, b, rep] of e.sort((p, q) => q[0] - p[0])) s = s.slice(0, a) + rep + s.slice(b);
        if (nl[i].trim().startsWith('|') && (s.match(/(?<!\\)\|/g) || []).length !== (nl[i].match(/(?<!\\)\|/g) || []).length) { R.tableProblems = (R.tableProblems || 0) + 1; continue; }
        nl[i] = s;
      }
      const nu = nl.join('\n');
      if (nu !== t) {
        await ensureAd(BK + f.path); if (!(await ad.exists(BK + f.path))) await ad.write(BK + f.path, t);
        await app.vault.process(f, cur => { if (cur !== t) throw new Error('changed during the edit: ' + f.path); return nu; });
        changedNotes.push(f.path);
      }
    }
  }
  R.total = P.length; R.seconds = Math.round((Date.now() - T0) / 1000);
  if (APPLY) { await new Promise(r => setTimeout(r, 5000)); R.unresolvedAfter = unres(); R.changedNotes = changedNotes.length; }
  const tag = APPLY ? OUTTAG + '-real' : OUTTAG;
  await ad.write(`.work/out/${tag}-proposals.json`, JSON.stringify(P));
  await ad.write(`.work/out/${tag}.json`, JSON.stringify(R, null, 1));
  return `${APPLY ? 'APPLIED' : 'DRY'} notes ${R.notes}, with links ${R.notesWithLinks}; proposals ${R.total} ${JSON.stringify(R.counts)}; undecided ${R.undecided.length}; skipped ${JSON.stringify(R.skipped)}; ${R.seconds}s` + (APPLY ? `; changed ${changedNotes.length}; unresolved ${JSON.stringify(R.unresolvedBefore)} -> ${JSON.stringify(R.unresolvedAfter)}` : '');
})()
