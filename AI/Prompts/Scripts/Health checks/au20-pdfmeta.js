(async () => {
  // Audit 14 Oct 2026 (read-only): Producer and Creator of every PDF in Library/, read from the first 1 MB and the last 2 MB of each
  // file (Info dictionary or XMP), with flags for OCR or scanning software named there. Opens files read-only with Node's fs.
  // Writes .work/out/audit-1014-pdfmeta.json.
  const T0 = Date.now(); let fs; try { fs = require('fs'); } catch (e) { return 'no fs: ' + e; }
  const base = app.vault.adapter.basePath || (app.vault.adapter.getBasePath && app.vault.adapter.getBasePath());
  const pdfs = app.vault.getFiles().filter(f => f.extension === 'pdf' && f.path.startsWith('Library/'));
  const dec = s => { if (!s) return null; const h = s.match(/^<([0-9A-Fa-f\s]+)>$/); if (h) { const hx = h[1].replace(/\s/g, ''); let out = ''; const be = hx.toUpperCase().startsWith('FEFF'); for (let i = be ? 4 : 0; i < hx.length; i += be ? 4 : 2) out += String.fromCharCode(parseInt(hx.slice(i, i + (be ? 4 : 2)), 16)); return out; } return s.replace(/^\(|\)$/g, '').replace(/^þÿ/, '').replace(/\u0000/g, ''); };
  const R = { when: new Date().toISOString(), pdfs: [] };
  for (const f of pdfs) {
    const p = base + '/' + f.path; let txt = '';
    try { const fd = fs.openSync(p, 'r'); const size = fs.fstatSync(fd).size; const a = Buffer.alloc(Math.min(1e6, size)); fs.readSync(fd, a, 0, a.length, 0); const tl = Math.min(2e6, size); const b = Buffer.alloc(tl); fs.readSync(fd, b, 0, tl, size - tl); fs.closeSync(fd); txt = a.toString('latin1') + '\n' + b.toString('latin1'); }
    catch (e) { R.pdfs.push([f.path, f.stat.size, 'ERROR ' + e.message]); continue; }
    const g = re => { const m = txt.match(re); return m ? dec(m[1]) : null; };
    const producer = g(/\/Producer\s*(\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f\s]+>)/) || g(/<pdf:Producer>([^<]*)</);
    const creator = g(/\/Creator\s*(\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f\s]+>)/) || g(/<xmp:CreatorTool>([^<]*)</);
    const flags = ['ClearScan', 'Paper Capture', 'ABBYY', 'FineReader', 'Tesseract', 'OCRmyPDF', 'ocrmypdf', 'Google', 'Internet Archive', 'pdfTeX', 'InDesign', 'Distiller', 'fpdf', 'Ghostscript', 'ScanSnap', 'Omnipage', 'img2pdf', 'calibre', 'Microsoft', 'LuaTeX', 'XeTeX', 'Quartz'].filter(k => txt.includes(k));
    R.pdfs.push([f.path, f.stat.size, (producer || '').slice(0, 160), (creator || '').slice(0, 160), flags]);
  }
  R.seconds = Math.round((Date.now() - T0) / 1000);
  await app.vault.adapter.write('.work/out/audit-1014-pdfmeta.json', JSON.stringify(R, null, 1));
  return `read-only pdfmeta: ${R.pdfs.length} PDFs, ${R.pdfs.filter(x => typeof x[2] === 'string' && x[2].startsWith('ERROR')).length} errors; ${R.seconds}s`;
})()
