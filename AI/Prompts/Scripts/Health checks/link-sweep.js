(async () => {
  // Phase 8, step 4 prep (read-only): the two sweeps the B3 sample check suggested: (a) a link that follows an escaped bracket
  // (`\[[[…`), which Obsidian reads as `[[[`; (b) chapter-only links in English-numbered books into chapters whose first verse
  // differs between Hebrew and English numbering, anchored at the Hebrew verse 1 (one verse off). Writes .work/out/s84a-sweep.json.
  const MC = app.metadataCache; const SHIFT = {"GEN": {"32": [32, 2]}, "EXO": {"8": [7, 26], "22": [21, 37]}, "LEV": {"6": [5, 20]}, "NUM": {"17": [17, 16], "30": [30, 2]}, "DEU": {"13": [13, 2], "23": [23, 2], "29": [28, 69]}, "1SA": {"21": [21, 2], "24": [24, 2]}, "2SA": {"19": [19, 2]}, "1KI": {"5": [5, 15]}, "2KI": {"12": [12, 2]}, "1CH": {"6": [5, 27]}, "2CH": {"2": [1, 18], "14": [13, 23]}, "NEH": {"4": [3, 33], "10": [10, 2]}, "JOB": {"41": [40, 25]}, "PSA": {"51": [51, 3], "52": [52, 3], "54": [54, 3], "60": [60, 3]}, "ECC": {"5": [4, 17]}, "SNG": {"7": [7, 2]}, "ISA": {"9": [8, 23]}, "JER": {"9": [8, 23]}, "EZK": {"21": [21, 6]}, "DAN": {"4": [3, 31], "6": [6, 2]}, "HOS": {"2": [2, 3], "12": [12, 2], "14": [14, 2]}, "JOL": {"3": [4, 1]}, "JON": {"2": [2, 2]}, "MIC": {"5": [4, 14]}, "NAM": {"2": [2, 2]}, "ZEC": {"2": [2, 5]}, "MAL": {"4": [3, 19]}}; const NAMES = {"GEN": ["Genesis", "Gen", "Gn"], "EXO": ["Exodus", "Exod", "Ex"], "LEV": ["Leviticus", "Lev", "Lv"], "NUM": ["Numbers", "Num", "Nm"], "DEU": ["Deuteronomy", "Deut", "Dt"], "1SA": ["1 Samuel", "1 Sam", "I Samuel", "1Sam"], "2SA": ["2 Samuel", "2 Sam", "II Samuel", "2Sam"], "1KI": ["1 Kings", "1 Kgs", "I Kings", "1Kgs"], "2KI": ["2 Kings", "2 Kgs", "II Kings", "2Kgs"], "1CH": ["1 Chronicles", "1 Chron", "1 Chr", "I Chronicles"], "2CH": ["2 Chronicles", "2 Chron", "2 Chr", "II Chronicles"], "NEH": ["Nehemiah", "Neh"], "JOB": ["Job"], "PSA": ["Psalms", "Psalm", "Pss", "Ps"], "ECC": ["Ecclesiastes", "Eccl", "Qoh", "Qoheleth", "Eccles"], "SNG": ["Song of Songs", "Song", "Cant", "Canticles", "Song of Solomon"], "ISA": ["Isaiah", "Isa", "Is"], "JER": ["Jeremiah", "Jer"], "EZK": ["Ezekiel", "Ezek", "Ez"], "DAN": ["Daniel", "Dan"], "HOS": ["Hosea", "Hos"], "JOL": ["Joel"], "JON": ["Jonah", "Jon"], "MIC": ["Micah", "Mic"], "NAM": ["Nahum", "Nah"], "ZEC": ["Zechariah", "Zech"], "MAL": ["Malachi", "Mal"]};
  const nameToBook = {}; for (const [b, ns] of Object.entries(NAMES)) for (const n of ns) nameToBook[n.toLowerCase().replace(/\.$/, '')] = b;
  const files = app.vault.getMarkdownFiles().filter(f => (f.path.startsWith('Library/') && ((MC.getFileCache(f) || {}).frontmatter || {}).source_pdf) || /^Texts\/(Hobbes|Aquinas|Fathers|Bible\/Jewish Annotated New Testament)\//.test(f.path));
  const esc = [], chap = []; let scanned = 0;
  const LIM = performance.memory.jsHeapSizeLimit;
  for (const f of files) {
    if (performance.memory.usedJSHeapSize > LIM - 300e6) { esc.push(['MEMORY GUARD', f.path]); break; }
    const t = await app.vault.cachedRead(f); scanned++;
    const lines = t.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const l = lines[i];
      if (l.includes('\\[[[')) esc.push([f.path, i + 1, l.slice(Math.max(0, l.indexOf('\\[[[') - 60), l.indexOf('\\[[[') + 120)]);
      for (const m of l.matchAll(/\[\[([^\]|#]+)#\^(\d+)-1\\?\|([^\]]+)\]\]/g)) {
        const label = m[3].trim(); if (/[\d][:.]\s*\d|\bv\.?\s*\d|^\d+:\d/.test(label)) continue; // has a verse
        const lm = label.match(/^((?:[123I]{1,3}\s*)?[A-Za-z][A-Za-z .]*?)\.?\s+(\d+)\s*$/); if (!lm) continue;
        const book = nameToBook[lm[1].toLowerCase().replace(/\.$/, '').replace(/\s+/g, ' ')]; const ch = +lm[2];
        if (!book || !SHIFT[book] || !SHIFT[book][ch] || +m[2] !== ch) continue;
        const [hc, hv] = SHIFT[book][ch];
        chap.push({ path: f.path, line: i + 1, link: m[0], target: m[1], label, book, chapter: ch, heb: hc + ':' + hv, ctx: l.slice(Math.max(0, m.index - 80), m.index + m[0].length + 60) });
      }
    }
  }
  await app.vault.adapter.write('.work/out/s84a-sweep.json', JSON.stringify({ scanned, escaped: esc, chapterLinks: chap }, null, 1));
  return `sweep: scanned ${scanned} notes; escaped-bracket links ${esc.length}; chapter-only links into shifted chapters ${chap.length}`;
})()