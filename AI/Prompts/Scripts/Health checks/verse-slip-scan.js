(async () => {
  // Phase 8 (read-only): sizes the OCR slips in the Dyczkowski translation callouts of the Tantraloka verse notes, for Stephen's
  // decision on a repair pass. Looks only inside the "> [!source] Dyczkowski" callouts. Writes .work/out/s84i-versescan.json.
  const V = app.vault, ad = V.adapter, T0 = Date.now();
  const files = V.getMarkdownFiles().filter(f => /^Texts\/Tantraloka\/Ahnika \d+\/Tantraloka \d+\.\d+\.md$/.test(f.path));
  const R = { notes: files.length, callouts: 0, lines: 0, junk: [], quotes: [], symbols: [], paren: {}, parenLines: 0 };
  const junkRe = /[A-Za-zāīūṛṝḷḹṃṁḥśṣṇṭḍñṅ](ą|ą,|'"|'”|,\?|\.\?|\?,|\?\.)|[,.]\?|\?\)|[a-z]"\)|’"/;
  const symRe = /[A-Za-zāīū]&[A-Za-zāīū]|\(&|~|[A-Za-zāīūṛḷśṣṇṭḍ]\d[A-Za-zāīū]|[A-Za-zāīū]\d\b|\b\d[A-Za-zāīū]+\b|\bfīrtha\b|\bfrika\b/;
  const parenRe = /\(([A-Za-zāīūṛṝḷḹṃṁḥśṣṇṭḍñṅĀĪŪṚŚṢṆṬḌÑṄ-]{3,})\)/g;
  for (const f of files) {
    const t = await ad.read(f.path);
    const L = t.split('\n'); let inCall = false;
    for (let i = 0; i < L.length; i++) {
      const l = L[i];
      if (/^> \[!source\] Dyczkowski/.test(l)) { inCall = true; R.callouts++; continue; }
      if (inCall && !l.startsWith('>')) { inCall = false; continue; }
      if (!inCall || l.trim() === '>' || /^> \[\[/.test(l)) continue;
      R.lines++;
      if (junkRe.test(l) && R.junk.length < 400) R.junk.push([f.basename, i + 1, (l.match(junkRe) || [''])[0], l.slice(Math.max(0, l.search(junkRe) - 40), l.search(junkRe) + 40)]);
      else if (junkRe.test(l)) R.junk.push([f.basename, i + 1]);
      const o = (l.match(/‘/g) || []).length, c = (l.match(/’/g) || []).length;
      if (o !== c && R.quotes.length < 400) R.quotes.push([f.basename, i + 1, o, c]); else if (o !== c) R.quotes.push([f.basename, i + 1]);
      if (symRe.test(l)) { const m = l.match(symRe)[0]; R.symbols.push(R.symbols.length < 400 ? [f.basename, i + 1, m, l.slice(Math.max(0, l.indexOf(m) - 40), l.indexOf(m) + 40)] : [f.basename, i + 1]); }
      let pm; let any = false;
      while ((pm = parenRe.exec(l))) { const w = pm[1]; any = true; const k = w; (R.paren[k] = R.paren[k] || []).length < 6 ? R.paren[k].push(f.basename) : R.paren[k].push(1); }
      if (any) R.parenLines++;
    }
  }
  // compact the paren map: term -> [count, examples]
  const P = {}; for (const [k, v] of Object.entries(R.paren)) P[k] = [v.length, v.filter(x => typeof x === 'string').slice(0, 3)];
  R.paren = P; R.parenTerms = Object.keys(P).length; R.seconds = Math.round((Date.now() - T0) / 1000);
  await ad.write('.work/out/s84i-versescan.json', JSON.stringify(R, null, 1));
  return `versescan: ${R.notes} notes, ${R.callouts} callouts, ${R.lines} lines; junk ${R.junk.length}, unbalanced quotes ${R.quotes.length}, symbols ${R.symbols.length}, paren terms ${R.parenTerms}; ${R.seconds} s`;
})()
