// B3 core (13 Oct 2026): find scripture, Zohar, Tantraloka and Avot references in a line of a converted book.
// Pure functions; the Obsidian jobs wrap them with indexes built from the metadata cache.
// 26 Oct 2026 (audit E-01/E-02): also references with a lower-case Roman chapter ("Matt. xxv. 30", "John iii.31",
// "1 Cor. xv. 3; xvi. 2", "Gen. xlviii. 5, 6"), marked roman: true; they are looked for after everything else,
// so a line without one gives exactly what the 13 Oct version gave.
const B3 = (() => {
  // canonical id -> [names and abbreviations, longest first matters only for the regex]
  const BOOKS = {
    GEN: ['Genesis', 'Gen', 'Gn'], EXO: ['Exodus', 'Exod', 'Ex'], LEV: ['Leviticus', 'Lev', 'Lv'], NUM: ['Numbers', 'Num', 'Nm'],
    DEU: ['Deuteronomy', 'Deut', 'Dt'], JOS: ['Joshua', 'Josh'], JDG: ['Judges', 'Judg', 'Jdg'], RUT: ['Ruth'],
    '1SA': ['1 Samuel', '1 Sam', 'I Samuel', 'I Sam', '1Sam'], '2SA': ['2 Samuel', '2 Sam', 'II Samuel', 'II Sam', '2Sam'],
    '1KI': ['1 Kings', '1 Kgs', 'I Kings', 'I Kgs', '1Kgs'], '2KI': ['2 Kings', '2 Kgs', 'II Kings', 'II Kgs', '2Kgs'],
    '1CH': ['1 Chronicles', '1 Chron', '1 Chr', 'I Chronicles', 'I Chron', 'I Chr'], '2CH': ['2 Chronicles', '2 Chron', '2 Chr', 'II Chronicles', 'II Chron', 'II Chr'],
    EZR: ['Ezra'], NEH: ['Nehemiah', 'Neh'], EST: ['Esther', 'Esth'], JOB: ['Job'], PSA: ['Psalms', 'Psalm', 'Pss', 'Ps'],
    PRO: ['Proverbs', 'Prov', 'Prv'], ECC: ['Ecclesiastes', 'Eccles', 'Eccl', 'Qoheleth', 'Qoh'], SNG: ['Song of Songs', 'Song of Solomon', 'Canticles', 'Cant', 'Song'],
    ISA: ['Isaiah', 'Isa'], JER: ['Jeremiah', 'Jer'], LAM: ['Lamentations', 'Lam'], EZK: ['Ezekiel', 'Ezek'], DAN: ['Daniel', 'Dan'],
    HOS: ['Hosea', 'Hos'], JOL: ['Joel'], AMO: ['Amos'], OBA: ['Obadiah', 'Obad'], JON: ['Jonah'], MIC: ['Micah', 'Mic'],
    NAM: ['Nahum', 'Nah'], HAB: ['Habakkuk', 'Hab'], ZEP: ['Zephaniah', 'Zeph'], HAG: ['Haggai', 'Hag'], ZEC: ['Zechariah', 'Zech'], MAL: ['Malachi', 'Mal'],
    MAT: ['Matthew', 'Matt', 'Mt'], MRK: ['Mark', 'Mk'], LUK: ['Luke', 'Lk'], JHN: ['John', 'Jn'], ACT: ['Acts'],
    ROM: ['Romans', 'Rom'], '1CO': ['1 Corinthians', '1 Cor', 'I Corinthians', 'I Cor', '1Cor'], '2CO': ['2 Corinthians', '2 Cor', 'II Corinthians', 'II Cor', '2Cor'],
    GAL: ['Galatians', 'Gal'], EPH: ['Ephesians', 'Eph'], PHP: ['Philippians', 'Phil'], COL: ['Colossians', 'Col'],
    '1TH': ['1 Thessalonians', '1 Thess', 'I Thessalonians', 'I Thess'], '2TH': ['2 Thessalonians', '2 Thess', 'II Thessalonians', 'II Thess'],
    '1TI': ['1 Timothy', '1 Tim', 'I Timothy', 'I Tim'], '2TI': ['2 Timothy', '2 Tim', 'II Timothy', 'II Tim'], TIT: ['Titus'], PHM: ['Philemon', 'Philem', 'Phlm'],
    HEB: ['Hebrews', 'Heb'], JAS: ['James', 'Jas'], '1PE': ['1 Peter', '1 Pet', 'I Peter', 'I Pet'], '2PE': ['2 Peter', '2 Pet', 'II Peter', 'II Pet'],
    '1JN': ['1 John', '1 Jn', 'I John'], '2JN': ['2 John', '2 Jn', 'II John'], '3JN': ['3 John', '3 Jn', 'III John'], JUD: ['Jude'], REV: ['Revelation', 'Rev', 'Apocalypse'],
    SIR: ['Sirach', 'Sir', 'Ecclesiasticus', 'Ecclus'], WIS: ['Wisdom of Solomon', 'Wisdom', 'Wis'], TOB: ['Tobit', 'Tob'], JDT: ['Judith', 'Jdt'],
    '1MA': ['1 Maccabees', '1 Macc', 'I Maccabees', 'I Macc'], '2MA': ['2 Maccabees', '2 Macc', 'II Maccabees', 'II Macc'],
    '3MA': ['3 Maccabees', '3 Macc'], '4MA': ['4 Maccabees', '4 Macc'], BAR: ['Baruch', 'Bar']
  };
  const TORAH = new Set(['GEN', 'EXO', 'LEV', 'NUM', 'DEU']);
  const NT = new Set(['MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV']);
  const DEUTERO = new Set(['SIR', 'WIS', 'TOB', 'JDT', '1MA', '2MA', '3MA', '4MA', 'BAR']);
  // full names safe for a chapter-only reference ("Isaiah 53"); never abbreviations, never names that are also people or words
  const CHAPTER_OK = new Set(['Genesis', 'Exodus', 'Leviticus', 'Deuteronomy', 'Joshua', 'Judges', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Nehemiah', 'Psalm', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Hosea', 'Obadiah', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Philemon', 'Hebrews', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Sirach', '1 Maccabees', '2 Maccabees']);
  const NAME2ID = new Map(); for (const [id, ns] of Object.entries(BOOKS)) for (const n of ns) NAME2ID.set(n, id);
  const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/ /g, '\\s');
  const names = [...NAME2ID.keys()].sort((a, b) => b.length - a.length).map(esc).join('|');
  // book, optional period, space, chapter, then [:.] verse (optional a/b), optional range; or chapter alone
  const DASH = '[-–—]';
  const BIBLE = new RegExp(`(?<![\\p{L}\\d])(${names})(\\.?)\\s?(\\d{1,3})(?:\\s?([:.])\\s?(\\d{1,3})[abc]?(?:\\s?${DASH}\\s?(\\d{1,3})(?:[:.](\\d{1,3}))?[abc]?)?(?:\\s?ff?\\.?(?![\\p{L}]))?)?(?![\\p{L}\\d]|[.:]\\d)`, 'gu');
  // continuation after a reference: "; 9:6" or ", 9:6" (chapter:verse) or ", 27" (verse in the same chapter)
  const CONT = new RegExp(`^(\\s?[;,]\\s?(?:and\\s)?)(\\d{1,3})(?:([:.])(\\d{1,3}))?[abc]?(?:\\s?${DASH}\\s?(\\d{1,3})(?:[:.](\\d{1,3}))?[abc]?)?(?![\\p{L}\\d]|[:.]\\d)`, 'u');
  const TA = /(?<![\p{L}\d])(T\.\s?[ĀA]\.|T[ĀA]|Tantr[āa]loka)(?![\p{L}])(?:\s?,?\s(?=[IVXL])|\s?,?\s?(?=\d))([IVXL]{1,6}|\d{1,2})\s?([.,:])\s?(\d{1,3})(?:[abcd]{1,2})?(?:\s?[-–]\s?(\d{1,3})(?:[abcd]{1,2})?)?(?![\p{L}\d]|[.,]\d|\s\d{1,3}[abcd]{0,2}\b)/gu;
  const TACONT = /^(\s?[;,]\s?(?:and\s)?)(\d{1,2})\s?[.:]\s?(\d{1,3})(?:[abcd]{1,2})?(?:\s?[-–]\s?(\d{1,3}))?(?![\p{L}\d]|[.,]\d)/u;
  const ZOHAR = /(?<![\p{L}\d])(Zohar(?:\s(?:Ḥadash|Hadash|Chadash))?|ZḤ|ZH)\s?,?\s?(?:(I{1,3}|[123])\s?[:,.]\s?)?(\d{1,3})([a-d])(?:\s?[-–]\s?(\d{1,3})?([a-d]))?(?![\p{L}\d])/gu;
  const AVOT = /(?<![\p{L}\d])((?:m\.\s?|Mishnah\s|Pirkei\s|Pirqe\s|Pirke\s)?(?:Avot|Aboth|Abot|Pirkei Avot))\s?(\d)\s?[:.]\s?(\d{1,2})(?![\p{L}\d]|[.,]\d)/gu;
  const roman = s => { const v = { I: 1, V: 5, X: 10, L: 50 }; let n = 0; for (let i = 0; i < s.length; i++) { const a = v[s[i]], b = v[s[i + 1]] || 0; n += a < b ? -a : a; } return n; };
  // ---- Roman chapters (26 Oct 2026). Abbreviations found before Roman chapters in the Fathers, Hobbes and Brandon that BOOKS lacks;
  // used only here and only with their period ("Is." needs a Roman chapter and a verse after it, so the word "Is" never fires).
  // Left out as ambiguous or OCR: Jos. (Joshua/Josephus), Ez. (Ezra/Ezekiel), Jud. (Judges/Judith/Jude), Marc. (Marcion), Mich., Sol., Ts./Ls./Ie. (OCR for Is.), Mace./Mac.
  const RNAMES = {
    ISA: ['Is', 'Isai'], WIS: ['Wisd'], NUM: ['Numb'], PHP: ['Philip'], MAT: ['Mat', 'Matth'], EPH: ['Ephes'], TIT: ['Tit'], JER: ['Jerem'],
    LEV: ['Levit'], COL: ['Coloss', 'Colos'], HAB: ['Habac'], MAL: ['Malach'], EZK: ['Ezech'], ZEC: ['Zach'], DEU: ['Deuteron'], JHN: ['Joh'], JAS: ['Jam'], REV: ['Apoc'],
    '1CO': ['1 Corinth'], '2CO': ['2 Corinth'], '1TH': ['1 Thes'], '2TH': ['2 Thes']
  };
  const RNAME2ID = new Map(NAME2ID), RDOT = new Set(); for (const [id, ns] of Object.entries(RNAMES)) for (const n of ns) { RNAME2ID.set(n, id); RDOT.add(n); }
  const rnames = [...RNAME2ID.keys()].sort((a, b) => b.length - a.length).map(esc).join('|');
  const RN = '(?=[ivxlc])c?(?:xc|xl|l?x{0,3})(?:ix|iv|v?i{0,3})';   // a well-formed lower-case numeral; its value is checked (1-150) below
  const rval = s => { const v = { i: 1, v: 5, x: 10, l: 50, c: 100 }; let n = 0; for (let i = 0; i < s.length; i++) { const a = v[s[i]], b = v[s[i + 1]] || 0; n += a < b ? -a : a; } return n; };
  const rok = s => { const n = rval(s); return n >= 1 && n <= 150 ? n : 0; };
  // optional "1 S." / "1 St." before the name ("1 St. John i. 1", "1 S. Pet. ii. 8"): the numbered epistle; then name, period and/or space,
  // Roman chapter, period, verse (a/b/c), optional range ("19-22", "6--8", "23-ix. 1"), optional f./ff.
  const RDASH = '[-–—]{1,2}';
  const rbases = [...new Set([...RNAME2ID.keys()].filter(n => /^(?:[1-4]|I{1,3}) \S/.test(n)).map(n => n.replace(/^\S+ /, '')))].sort((a, b) => b.length - a.length).map(esc).join('|');
  const ROMANRE = new RegExp(`(?<![\\p{L}\\d])(?:([1-3]|I{1,3})\\s?St?\\.?\\s(${rbases})|(${rnames}))(?:(\\.)\\s?|\\s)(${RN})\\.\\s?(\\d{1,3})[abc]?(?:\\s?${RDASH}\\s?(?:(${RN})\\.\\s?)?(\\d{1,3})[abc]?)?(?:\\s?ff?\\.?(?![\\p{L}]))?(?![\\p{L}\\d]|[.:]\\d)`, 'gu');
  // continuation: "; xv. 3" or ", xvi. 3" (new chapter, same book), ", 4" (next verse, same chapter), with ranges
  const RCONT = new RegExp(`^(\\s?[;,]\\s?(?:and\\s)?)(?:(${RN})\\.\\s?)?(\\d{1,3})[abc]?(?:\\s?${RDASH}\\s?(?:(${RN})\\.\\s?)?(\\d{1,3})[abc]?)?(?:\\s?ff?\\.?(?![\\p{L}]))?(?![\\p{L}\\d]|[.:]\\d)`, 'u');
  // books with no numbered namesake, so a digit before them is a footnote number ("2 Mark xii. 13-17" in Brandon's notes)
  const NONUM = new Set(Object.keys(BOOKS).filter(id => !/^\d/.test(id) && !['JHN', 'EZR', 'BAR'].includes(id)));
  // spans not to touch: existing links, inline code, URLs, html, footnote refs [^n], page markers, block ids
  const protectedSpans = line => {
    const sp = [];
    for (const re of [/\[\[[^\]]*\]\]/g, /!?\[[^\]]*\]\([^)]*\)/g, /`[^`]*`/g, /https?:\/\/\S+/g, /<[^>]+>/g, /\[\^[^\]]*\]/g, /\*\[p\. [^\]]*\]\*/g, /\s\^[\w-]+$/g]) {
      for (const m of line.matchAll(re)) sp.push([m.index, m.index + m[0].length]);
    }
    return sp;
  };
  const inSpans = (sp, a, b) => sp.some(([x, y]) => a < y && b > x);
  // a stretch in another language: script, or few English function words
  const STOP = new Set('the of and to in a is that for it as with was on be by this which or are from at an his not have but they he were their has its been one all we can these more other also our who so only there into if than when may such any what most will no some them do would should could about between through its into how even very same each first'.split(' '));
  const foreign = s => {
    if (/[\u0900-\u097F\u0590-\u05FF\u0370-\u03FF\u1F00-\u1FFF]/.test(s)) return true;
    const w = s.toLowerCase().match(/[a-zāīūṛṝḷṅñṭḍṇśṣḥṃ']+/g) || [];
    if (w.length < 6) return false;
    const en = w.filter(x => STOP.has(x)).length;
    return en / w.length < 0.2;
  };
  // share of Greek, Hebrew and Devanagari letters among all letters of a line
  const scriptShare = s => { const all = (s.match(/\p{L}/gu) || []).length; if (!all) return 0; const o = (s.match(/[\u0900-\u097F\u0590-\u05FF\u0370-\u03FF\u1F00-\u1FFF]/g) || []).length; return o / all; };
  // the italic span around a position, if any
  const italicAround = (line, pos) => {
    for (const m of line.matchAll(/(?<!\*)\*(?!\*)([^*]+)\*(?!\*)|_([^_]+)_/g)) { if (m.index <= pos && pos < m.index + m[0].length) return m[1] || m[2]; }
    return null;
  };
  // the quotation (curly or straight double quotes) around a position, if any
  const quoteAround = (line, pos) => {
    for (const m of line.matchAll(/“([^”]{0,600})”|"([^"]{0,600})"|«([^»]{0,600})»/g)) { if (m.index <= pos && pos < m.index + m[0].length) return m[1] || m[2] || m[3]; }
    return null;
  };
  const sentenceAround = (line, a, b) => { let s = line.lastIndexOf('. ', a); s = s < 0 ? 0 : s + 2; let e = line.indexOf('. ', b); e = e < 0 ? line.length : e + 1; return line.slice(s, e); };
  // find all references in one line; returns [{kind, a, b, text, ...}]
  const find = (line, opts = {}) => {
    const out = [], sp = protectedSpans(line);
    const push = r => { if (inSpans(sp, r.a, r.b)) return; if (out.some(o => r.a < o.b && r.b > o.a)) return; out.push(r); };
    for (const m of line.matchAll(BIBLE)) {
      const [all, name, dot, ch, sep, v, v2, v3] = m; const id = NAME2ID.get(name.replace(/\s+/g, ' '));
      if (!id) continue;
      const pre = line.slice(Math.max(0, m.index - 40), m.index), post = line.slice(m.index + all.length, m.index + all.length + 14);
      if (/(?:^|[^\p{L}\d])(?:[1-4]|I{1,3}|IV)\\?\.?\s$/u.test(pre.slice(-6))) continue;   // a numbered book we do not know ("I Jn", "2\. Baruch")
      // glued to a preceding abbreviation ("Brd.Clr.Cant.27", "Midr. Rab. Gen. 36.8", "Aug.Ps."), unless it is cf./see/e.g.
      const g = pre.match(/([\p{L}]+)\.$/u); if (g && !/^(?:cf|Cf|see|See|eg|ie|vid|esp|ch|chap|vv?)$/.test(g[1])) continue;
      if (/\b(?:Rab|Rabbah|Midr|Mek|Mekh|Sifre|Sifra|Tanh|Tanḥ|Pesiq|Yalq|Hom|Homil|Comm|Com|Enarr|Tract|Exp|Expos|Quaest|Serm|Lect)\.\s$/.test(pre)) continue;
      if (name.replace(/\s+/g, ' ').length <= 3 && !dot && /^\d/.test(line.slice(m.index + name.length))) continue;   // "Lk2. 334": a siglum
      // persons: "by John 3", "R. Daniel 11.11. Ingalls", "Daniel H."
      if (/^(?:Daniel|John|Mark|Luke|Matthew|Joshua|Isaiah|Amos|Jonah|Micah|Titus|James|Jude|Job|Ruth|Esther|Joel|Ezra|Nahum|Hosea)$/.test(name) && (/(?:\bby|\bed\.|\btr\.|\bR\.|Rabbi|Dr\.|Prof\.)\s$/.test(pre) || /^\.\s[A-Z]/.test(post))) continue;
      const after2 = line.slice(m.index + all.length, m.index + all.length + 8);
      const alt = /^\s?\(\d/.test(after2);   // "Psalm 72 (73)": a second numbering follows
      if (!v) {   // chapter only: full safe names, and not followed by a number-ish continuation
        if (!CHAPTER_OK.has(name.replace(/\s+/g, ' ')) || dot) continue;
        const after = line.slice(m.index + all.length, m.index + all.length + 12);
        if (/^\s?(?:per\s?cent|%|times|vols?\b|pp?\.|years|BCE|CE|AD|BC|n\.|ff?\.)/i.test(after)) continue;
        if (opts.noChapter) continue;
        if (/[-‐]$/.test(pre) || (/\bthe\s$/i.test(pre) && !/(?:Epistle|Letter)\s(?:of\s\w+\s)?to\sthe\s$/i.test(pre))) continue;   // "Self-Revelation 7", "the Hebrews 11"
        if (/^\s?(?:and|&|or|[-–])\s?[1-4]\s/.test(after) || /^\s?[,.]?\s?\d/.test(after) || /^\s?\.{2,}/.test(after)) continue;   // "Romans 1 and 2 Thessalonians"; another number follows
        if (['OBA', 'PHM', '2JN', '3JN', 'JUD'].includes(id)) { push({ kind: 'bible', id, ch: 1, v: +ch, a: m.index, b: m.index + all.length, text: all, range: null, alt, dot: !!dot, name, grp: m.index }); continue; }
        push({ kind: 'chapter', id, ch: +ch, v: 1, a: m.index, b: m.index + all.length, text: all, alt, dot: !!dot, name, grp: m.index });
        continue;
      }
      if (sep === '.' && !dot && name.length <= 3 && /^\d/.test(line.slice(m.index + all.length))) continue;
      const r = { kind: 'bible', id, ch: +ch, v: +v, a: m.index, b: m.index + all.length, text: all, range: v2 ? (v3 ? `${v2}:${v3}` : v2) : null, alt, dot: !!dot, name, grp: m.index };
      push(r);
      if (v3) continue;   // a range across chapters: what follows is ambiguous ("Hos 1:2–2:3, 11")
      // continuations
      let pos = r.b, chap = r.ch, lastV = v2 ? +v2 : +v;
      for (let k = 0; k < 12; k++) {
        const c = line.slice(pos).match(CONT); if (!c) break;
        if (/^\s?nn?\.?\s?\d/.test(line.slice(pos + c[0].length))) break;
        const [ca, lead, n1, s2, n2] = c; const a = pos + lead.length, b = pos + ca.length;
        if (s2) { chap = +n1; lastV = c[5] ? +c[5] : +n2; push({ kind: 'bible-list', id, ch: chap, v: +n2, a, b, text: ca.slice(lead.length), grp: r.grp }); if (c[6]) break; }
        else { if (lead.includes(';') || opts.noVerseCont || +n1 <= lastV) break; lastV = c[5] ? +c[5] : +n1; push({ kind: 'bible-verse', id, ch: chap, v: +n1, a, b, text: ca.slice(lead.length), grp: r.grp }); }
        pos = b;
      }
    }
    for (const m of line.matchAll(TA)) {
      const [all, , c, sep, v] = m; const ch = /\d/.test(c) ? +c : roman(c); if (!ch || ch > 37) continue;
      if (/^V\b/.test(c) && /^T\.?\s?[ĀA]\.?\s?V/.test(all)) continue;   // TĀV / T.A.V. (Jayaratha's Viveka) with a page
      const tail = line.slice(m.index + all.length);
      if (sep === ',' && /^(?:,\s?\d{1,4}){1,}/.test(tail)) continue;   // "TĀ 22, 59, 61": pages
      push({ kind: 'ta', ch, v: +v, a: m.index, b: m.index + all.length, text: all, grp: m.index, sep });
      let pos = m.index + all.length;
      for (let k = 0; k < 12; k++) { const t = line.slice(pos).match(TACONT); if (!t) break; const [ta, lead, c2, v2] = t; const s2 = ta.slice(lead.length).match(/\d\s?([.:])/); if (!s2 || (s2[1] !== sep && sep !== ',')) break; push({ kind: 'ta-list', ch: +c2, v: +v2, a: pos + lead.length, b: pos + ta.length, text: ta.slice(lead.length), grp: m.index }); pos += ta.length; }
    }
    for (const m of line.matchAll(ZOHAR)) {
      const [all, z, part, fol, side] = m; const had = /Ḥ|H|Chadash/.test(z) && z !== 'Zohar';
      if (had) { push({ kind: 'zohar', block: `zh-${fol}${side}`, a: m.index, b: m.index + all.length, text: all }); continue; }
      if (!part) continue;
      const p = /\d/.test(part) ? +part : part.length;
      push({ kind: 'zohar', block: `z${p}-${fol}${side}`, a: m.index, b: m.index + all.length, text: all });
    }
    for (const m of line.matchAll(AVOT)) push({ kind: 'avot', ch: +m[2], v: +m[3], a: m.index, b: m.index + m[0].length, text: m[0] });
    // ---- Roman chapters (26 Oct 2026): looked for last, so they never displace a reference found above
    for (const m of line.matchAll(ROMANRE)) {
      const [all, num, base, nm, dot, rc, v, rc2, v2] = m;
      // "1 St. John", "1 S. Pet.": the numbered book ("I" is read as 1), or nothing
      const name = num ? (/\d/.test(num) ? num : String(num.length)) + ' ' + base.replace(/\s+/g, ' ') : nm.replace(/\s+/g, ' '), nameN = num ? base : name;
      let id = RNAME2ID.get(name); if (!id) continue;
      if (RDOT.has(name) && !dot) continue;   // the added abbreviations only with their period
      const ch = rok(rc); if (!ch) continue;
      const ch2 = rc2 ? rok(rc2) : null; if (rc2 && !ch2) continue;
      const pre = line.slice(Math.max(0, m.index - 40), m.index), tail = line.slice(m.index + all.length);
      // a number split by OCR ("Mark xii. 1 6)", "Rom. xi. 1 3-24", "Eph. i. 2 1 ,"); a digit that starts the next reference ("1 Cor.") is fine
      if (/^\s\d(?!\d)(?!\s[A-Z])/.test(tail)) continue;
      // a chapter cited alone, then the next footnote's number: "19 Gen. xxxvii. 20 Ex. ii. 14"
      const fn = pre.match(/(?:^|[^\d.,:–-])(\d{1,4})\s(?:(?:Cf|cf|Comp|comp|See|see)\.?\s)?$/);
      if (fn && !v2 && +v === +fn[1] + 1 && /^\s/.test(tail) && !new RegExp(`^\\s${+v}(?!\\d)`).test(tail)) continue;
      // "3 John xviii. 3" in a footnote: no such chapter in 1-3 John, so the digit is the footnote's number and the book is John
      let a0 = m.index, text = all;
      if (!num && /^[1-3] John$/.test(name) && ch > (id === '1JN' ? 5 : 1)) { id = 'JHN'; a0 = m.index + 2; text = all.slice(2); }
      // a numbered book we do not know ("2 Esdras", "I Jn"); not when the digit ends the reference before ("John v. 22; i. 3. 1 Cor. i. 24", "Gal. vi. 1, 2. 2 Tim. ii. 24")
      if (!num && !NONUM.has(id) && !/(?:[ivxlc]\.\s?|\d[,;]\s?)[1-4]\\?\.\s$/.test(pre) && /(?:^|[^\p{L}\d])(?:[1-4]|I{1,3}|IV)\\?\.?\s$/u.test(pre.slice(-6))) continue;
      if (/\b(?:First|Second|Third|Fourth|Fifth|1st|2nd|3rd|4th)\s$/i.test(pre)) continue;   // "Fourth Ezra vii. 29"
      const g = pre.match(/([\p{L}]+)\.$/u); if (g && !/^(?:cf|Cf|see|See|eg|ie|vid|esp|ch|chap|vv?)$/.test(g[1])) continue;   // glued to an abbreviation
      if (/\b(?:Rab|Rabbah|Midr|Mek|Mekh|Sifre|Sifra|Tanh|Tanḥ|Pesiq|Yalq|Hom|Homil|Comm|Com|Enarr|Tract|Exp|Expos|Quaest|Serm|Lect)\.\s$/.test(pre)) continue;
      if (/\b(?:Hom|Homil|Comm|Com|Enarr|Tract|Exp|Expos|Serm|Lect|Tom|tom)\.?,?\s(?:in|on|super|ad)\s$/.test(pre)) continue;   // "Hom. in Mat. xxi. 8": a work cited by its title
      if (/\b(?:Hist|Jur|Gr|Aquil|Symm|Theod)\.\s$/.test(pre)) continue;   // "Hist. Eccl. ix. 4", "Jur. Gr. Rom. v. 307", "Aquil. Ps. xliv. 2"
      if (/^(?:Daniel|John|Mark|Luke|Matthew|Joshua|Isaiah|Amos|Jonah|Micah|Titus|James|Jude|Job|Ruth|Esther|Joel|Ezra|Nahum|Hosea)$/.test(nameN) && /(?:\bby|\bed\.|\btr\.|\bR\.|Rabbi|Dr\.|Prof\.)\s$/.test(pre)) continue;
      const after = line.slice(m.index + all.length, m.index + all.length + 12);
      const alt = /^\s?\((?:\d|[ivxlc]+\.\s?\d)/.test(after);   // "Ps. xliv. 3 (xlv. 2, English version)"
      const r = { kind: 'bible', id, ch, v: +v, a: a0, b: m.index + all.length, text, range: v2 ? (ch2 ? `${ch2}:${v2}` : v2) : null, alt, dot: !!dot, name: id === 'JHN' ? 'John' : name, grp: a0, roman: true };
      push(r);
      if (!out.includes(r) || ch2) continue;   // not taken, or a range across chapters: what follows is ambiguous
      let pos = r.b, chap = ch, lastV = v2 ? +v2 : +v;
      for (let k = 0; k < 12; k++) {
        const c = line.slice(pos).match(RCONT); if (!c) break;
        if (/^\s?nn?\.?\s?\d/.test(line.slice(pos + c[0].length))) break;
        const [ca, lead, cr, n1, cr2, n2] = c; const a = pos + lead.length, b = pos + ca.length;
        if (/^\s\d(?!\d)(?!\s[A-Z])/.test(line.slice(b))) break;   // split by OCR
        if (cr) {
          const nc = rok(cr); if (!nc) break; const nc2 = cr2 ? rok(cr2) : null; if (cr2 && !nc2) break;
          chap = nc; lastV = n2 && !cr2 ? +n2 : +n1;
          push({ kind: 'bible-list', id, ch: chap, v: +n1, a, b, text: ca.slice(lead.length), grp: r.grp, roman: true }); if (cr2) break;
        } else {
          if (cr2 || lead.includes(';') || opts.noVerseCont || +n1 <= lastV) break;
          lastV = n2 ? +n2 : +n1; push({ kind: 'bible-verse', id, ch: chap, v: +n1, a, b, text: ca.slice(lead.length), grp: r.grp, roman: true });
        }
        pos = b;
      }
    }
    return out.sort((x, y) => x.a - y.a);
  };
  return { BOOKS, TORAH, NT, DEUTERO, NAME2ID, RNAME2ID, find, foreign, italicAround, quoteAround, sentenceAround, scriptShare, roman, rval };
})();
if (typeof module !== 'undefined') module.exports = B3;
