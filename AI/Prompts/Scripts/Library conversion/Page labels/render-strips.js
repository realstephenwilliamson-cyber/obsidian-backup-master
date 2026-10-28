(async () => {
  // pf421 (28 Oct 2026, item 6), read-only for the notes: renders the top and bottom strips of chosen PDF pages (where page numbers print)
  // to PNGs in .work/xfer/pl28/ for blind readers. List: .work/edits/pagelabels-2026-10-28/render-list.json [{id, pdf, K}].
  // Opens one PDF view to load Obsidian's pdf.js, then closes it.
  const sleep = ms => new Promise(r => setTimeout(r, ms)), ad = app.vault.adapter, OUT = '.work/xfer/pl28/';
  const items = JSON.parse(await ad.read('.work/edits/pagelabels-2026-10-28/render-list.json'));
  for (const d of ['.work/xfer', '.work/xfer/pl28']) if (!(await ad.exists(d))) await ad.mkdir(d);
  let leaf = null;
  if (!window.pdfjsLib) { leaf = app.workspace.getLeaf('tab'); await leaf.setViewState({ type: 'pdf', state: { file: items[0].pdf }, active: false }); for (let i = 0; i < 60 && !window.pdfjsLib; i++) await sleep(250); }
  const lib = window.pdfjsLib, R = { ok: 0, err: [] };
  const byPdf = {}; for (const it of items) (byPdf[it.pdf] = byPdf[it.pdf] || []).push(it);
  try {
    for (const [pdf, its] of Object.entries(byPdf)) {
      let doc = null;
      try {
        doc = await lib.getDocument({ data: new Uint8Array(await ad.readBinary(pdf)) }).promise;
        for (const it of its) {
          try {
            const page = await doc.getPage(it.K); const v0 = page.getViewport({ scale: 1 }); const sc = Math.min(2.2, 1100 / v0.width);
            const vp = page.getViewport({ scale: sc }); const c = document.createElement('canvas'); c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
            const ctx = c.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height); await page.render({ canvasContext: ctx, viewport: vp }).promise;
            const h = Math.round(c.height * 0.14), o = document.createElement('canvas'); o.width = c.width; o.height = 2 * h + 12;
            const x = o.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, o.width, o.height); x.drawImage(c, 0, 0, c.width, h, 0, 0, c.width, h);
            x.fillStyle = '#c00'; x.fillRect(0, h + 4, o.width, 4); x.drawImage(c, 0, c.height - h, c.width, h, 0, h + 12, c.width, h);
            const blob = await new Promise(r => o.toBlob(r, 'image/png')); await ad.writeBinary(OUT + it.id + '.png', await blob.arrayBuffer()); R.ok++;
            page.cleanup();
          } catch (e) { R.err.push(it.id + ': ' + (e && e.message)); }
        }
      } catch (e) { R.err.push(pdf + ': ' + (e && e.message)); }
      finally { if (doc) await doc.destroy(); }
    }
  } finally { if (leaf) try { leaf.detach(); } catch (e) {} }
  await ad.write('.work/out/pf421-render.json', JSON.stringify(R, null, 1));
  return `pf421-render: ${R.ok} of ${items.length} pages rendered; errors ${R.err.length}`;
})()
