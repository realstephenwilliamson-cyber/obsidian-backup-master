// Devanagari search: type Harvard-Kyoto or IAST, see the Devanagari, and search the vault for it.
// Used by Notes/Devanagari search.md; the "Devanagari search" command (registered from Home) opens that note.
// Changed 7 Oct 2026 (phase 3): what was typed and the two options survive Dataview's re-render (F4).
// Harvard-Kyoto / IAST (plus a few ITRANS spellings) -> Devanagari and IAST
const V = { a: ['अ', ''], ā: ['आ', 'ा'], i: ['इ', 'ि'], ī: ['ई', 'ी'], u: ['उ', 'ु'], ū: ['ऊ', 'ू'], ṛ: ['ऋ', 'ृ'], ṝ: ['ॠ', 'ॄ'], ḷ: ['ऌ', 'ॢ'], e: ['ए', 'े'], ai: ['ऐ', 'ै'], o: ['ओ', 'ो'], au: ['औ', 'ौ'] };
const C = { k: 'क', kh: 'ख', g: 'ग', gh: 'घ', ṅ: 'ङ', c: 'च', ch: 'छ', j: 'ज', jh: 'झ', ñ: 'ञ', ṭ: 'ट', ṭh: 'ठ', ḍ: 'ड', ḍh: 'ढ', ṇ: 'ण', t: 'त', th: 'थ', d: 'द', dh: 'ध', n: 'न', p: 'प', ph: 'फ', b: 'ब', bh: 'भ', m: 'म', y: 'य', r: 'र', l: 'ल', v: 'व', ś: 'श', ṣ: 'ष', s: 'स', h: 'ह', ḻ: 'ळ' };
const X = { ṃ: 'ं', ḥ: 'ः', "'": 'ऽ' };
// input spelling -> phoneme (longest match first)
const T = { aa: 'ā', A: 'ā', ā: 'ā', ii: 'ī', I: 'ī', ī: 'ī', uu: 'ū', U: 'ū', ū: 'ū', RRI: 'ṝ', 'R^I': 'ṝ', RR: 'ṝ', ṝ: 'ṝ', RRi: 'ṛ', 'R^i': 'ṛ', R: 'ṛ', ṛ: 'ṛ', LLi: 'ḷ', 'L^i': 'ḷ', lR: 'ḷ', ḷ: 'ḷ',
  ai: 'ai', au: 'au', a: 'a', i: 'i', u: 'u', e: 'e', o: 'o', E: 'ai', O: 'au',
  M: 'ṃ', ṃ: 'ṃ', ṁ: 'ṃ', '.m': 'ṃ', '.n': 'ṃ', H: 'ḥ', ḥ: 'ḥ', '.a': "'", "'": "'", 'ʼ': "'",
  kh: 'kh', gh: 'gh', ch: 'ch', jh: 'jh', Th: 'ṭh', ṭh: 'ṭh', Dh: 'ḍh', ḍh: 'ḍh', th: 'th', dh: 'dh', ph: 'ph', bh: 'bh',
  G: 'ṅ', '~N': 'ṅ', ṅ: 'ṅ', J: 'ñ', '~n': 'ñ', ñ: 'ñ', T: 'ṭ', ṭ: 'ṭ', D: 'ḍ', ḍ: 'ḍ', N: 'ṇ', ṇ: 'ṇ', z: 'ś', sh: 'ś', ś: 'ś', S: 'ṣ', Sh: 'ṣ', ṣ: 'ṣ', L: 'ḻ', w: 'v',
  k: 'k', g: 'g', c: 'c', j: 'j', t: 't', d: 'd', n: 'n', p: 'p', b: 'b', m: 'm', y: 'y', r: 'r', l: 'l', v: 'v', s: 's', h: 'h',
  x: ['k', 'ṣ'], kS: ['k', 'ṣ'], kSh: ['k', 'ṣ'], GY: ['j', 'ñ'], 'j~n': ['j', 'ñ'], dny: ['j', 'ñ'] };
const KEYS = Object.keys(T).sort((a, b) => b.length - a.length);
function parse(s) {
  s = s.normalize('NFC'); const out = [];
  for (let i = 0; i < s.length;) {
    const k = KEYS.find(k => s.startsWith(k, i));
    if (k) { [].concat(T[k]).forEach(p => out.push(p)); i += k.length; } else { out.push({ raw: s[i] }); i++; }
  }
  return out;
}
function toDeva(ph) {
  let o = '';
  for (let i = 0; i < ph.length; i++) {
    const p = ph[i], n = ph[i + 1];
    if (typeof p === 'object') { o += p.raw; continue; }
    if (C[p]) { o += C[p]; if (typeof n === 'string' && V[n]) { o += V[n][1]; i++; } else o += '्'; }
    else if (V[p]) o += V[p][0];
    else if (X[p]) o += X[p];
  }
  return o;
}
const toIAST = ph => ph.map(p => typeof p === 'object' ? p.raw : p).join('');


const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const LOOSE = { ā: '[āa]', ī: '[īi]', ū: '[ūu]', ṛ: '(?:ṛ|r̥|ri?)', ṝ: '(?:ṝ|r̥̄|r)', ḷ: '[ḷl]', ṅ: '[ṅn]', ñ: '[ñn]', ṭ: '[ṭt]', ḍ: '[ḍd]', ṇ: '[ṇn]', ś: '(?:ś|sh?)', ṣ: '(?:ṣ|sh?)', ṃ: '[ṃṁmn]', ḥ: '[ḥh]?' };
function query(raw, opt) {
  const ph = parse(raw.trim()); if (!ph.length) return '';
  let dev = toDeva(ph).replace(/्$/, '');               // a final consonant also matches inside compounds
  let devRe = esc(dev);
  if (opt.nasal) devRe = devRe.replace(/(?:ं|[ङञणनम]्)(?=[क-ह])/g, '(?:ं|[ङञणनम]्)');
  const parts = [devRe];
  if (opt.roman) {
    let r = esc(toIAST(ph));
    if (opt.nasal) r = r.replace(/(?:ṃ|[ṅñṇnm])(?=[kgcjṭḍtdpbyrlvśṣsh])/g, 'ṃ');
    r = [...r].map(ch => LOOSE[ch] || ch).join('');
    parts.push(r);
  }
  return '/' + parts.join('|') + '/';
}
// Dataview clears and re-runs this block whenever any note in the vault changes. What was typed and the two options are
// kept on the block's container, so they come back; opened anew, the note starts with an empty box.
const st = dv.container.__vpDeva || (dv.container.__vpDeva = { text: '', roman: true, nasal: true });
const box = dv.container.createDiv({ cls: 'vp-deva' });
const inp = box.createEl('input', { type: 'text', cls: 'vp-deva-input', attr: { placeholder: 'Harvard-Kyoto or IAST, e.g. tantrAloka, zivasUtra, pratyabhijJA', spellcheck: 'false', autocomplete: 'off' } });
inp.style.cssText = 'width:100%;font-size:1.1em;padding:.4em .6em;margin-bottom:.4em';
inp.value = st.text;
const prev = box.createDiv(); prev.style.cssText = 'font-size:1.6em;min-height:1.4em;margin:.2em 0';
const sub = box.createDiv(); sub.style.cssText = 'opacity:.8;min-height:1.2em;margin-bottom:.5em';
const opts = box.createDiv(); opts.style.cssText = 'margin-bottom:.5em;display:flex;gap:1.2em;flex-wrap:wrap';
const chk = (label, on) => { const l = opts.createEl('label'); const c = l.createEl('input', { type: 'checkbox' }); c.checked = on; l.appendText(' ' + label); return c; };
const cRoman = chk('also find the Roman spelling (with or without diacritics)', st.roman), cNasal = chk('allow ṃ/n variants (संत / सन्त)', st.nasal);
const row = box.createDiv(); row.style.cssText = 'display:flex;gap:.5em;flex-wrap:wrap';
const btn = (t, f) => { const b = row.createEl('button', { text: t }); b.onclick = f; return b; };
const opt = () => ({ roman: cRoman.checked, nasal: cNasal.checked });
const update = () => { st.text = inp.value; st.roman = cRoman.checked; st.nasal = cNasal.checked; const ph = parse(inp.value); prev.setText(inp.value.trim() ? toDeva(ph) : ''); sub.setText(inp.value.trim() ? toIAST(ph) + '   ·   ' + query(inp.value, opt()) : ''); };
const search = () => { const q = query(inp.value, opt()); if (!q) return; app.internalPlugins.getPluginById('global-search')?.instance?.openGlobalSearch(q); };
inp.addEventListener('input', update); cRoman.onchange = update; cNasal.onchange = update;
inp.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); search(); } });
btn('Search the vault', search);
const cp = btn('Copy Devanagari', async () => { await navigator.clipboard.writeText(toDeva(parse(inp.value))); cp.setText('Copied'); setTimeout(() => cp.setText('Copy Devanagari'), 1200); });
btn('Clear', () => { inp.value = ''; update(); inp.focus(); });
update();
