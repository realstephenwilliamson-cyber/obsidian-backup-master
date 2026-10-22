(async () => {
  // Step 7(a), approved 8 Oct 2026 ("Markdown first"): in the Tantraloka secondary-literature note and the study plans,
  // each PDF page link whose book is converted becomes  [[<chapter note>#^pgK|label]] ([pdf](<the PDF link>)).
  // Links whose book is not converted yet stay as they are; a later run adds them (a link already followed by its pdf is skipped).
  // Backups: .work/backup-phase4-links/. window.DRY !== false -> report only, with previews in .work/out/p4-links-preview/.
  const DRY = window.DRY !== false;
  const MC = app.metadataCache, V = app.vault, A = app.vault.adapter;
  const TARGETS = ['Texts/Tantraloka/Tantraloka - secondary literature.md',
    ...V.getMarkdownFiles().filter(f => f.path.startsWith('Texts/Tantraloka/Study plan/Study plan - ')).map(f => f.path)];
  const range = (s) => { const m = String(s || '').match(/(\d+)\s*[–-]\s*(\d+)/); return m ? [+m[1], +m[2]] : null; };
  const conv = {};
  for (const f of V.getMarkdownFiles()) {
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || !fm.source_pdf || !fm.converted) continue;
    const r = range(fm.pdf_pages); if (!r) continue;
    (conv[fm.source_pdf] = conv[fm.source_pdf] || []).push({ path: f.path, from: r[0], to: r[1] });
  }
  const mkdirs = async (p) => { let cur = ''; for (const x of p.split('/').slice(0, -1)) { cur = cur ? cur + '/' + x : x; if (!(await A.exists(cur))) await A.mkdir(cur); } };
  const rep = { dry: DRY, files: {}, total: { links: 0, changed: 0, notConverted: 0, noAnchor: 0, skipped: 0, retargeted: 0 } };
  const RE = /\[([^\]]*)\]\((?:<([^>]+?\.pdf)#page=(\d+)>|([^)<>\s]+?\.pdf)#page=(\d+))\)/g;
  for (const path of TARGETS) {
    const f = V.getAbstractFileByPath(path); if (!f) { rep.files[path] = 'not found'; continue; }
    const old = await V.read(f); const st = { links: 0, changed: 0, notConverted: 0, noAnchor: 0, skipped: 0, retargeted: 0 };
    const DONE = /\[\[([^\]|#]+)#\^pg(\d+)(\\?\|)([^\]]*)\]\] \(\[pdf\]\(<([^>]+?\.pdf)#page=(\d+)>\)\)/g;
    const out = old.split('\n').map(line => {
      const table = line.trimStart().startsWith('|');
      // links made before: point them at the chapter note that has the page now (a book converted again may have new chapter notes)
      line = line.replace(DONE, (m, tgt, K1, sep, label, pdfPath, K) => {
        const pdf = MC.getFirstLinkpathDest(pdfPath, path); const notes = pdf && conv[pdf.path];
        const n = notes && notes.find(x => +K >= x.from && +K <= x.to);
        if (!n || n.path.replace(/\.md$/, '') === tgt) return m;
        st.retargeted = (st.retargeted || 0) + 1;
        return `[[${n.path.replace(/\.md$/, '')}#^pg${K}${sep}${label}]] ([pdf](<${pdfPath}#page=${K}>))`;
      });
      return line.replace(RE, (m, label, pa, Ka, pb, Kb, off, whole) => {
        const pdfPath = pa || pb, K = Ka || Kb;
        st.links++;
        if (label === 'pdf' && /\]\] \($/.test(whole.slice(Math.max(0, off - 4), off))) { st.skipped++; return m; }   // done before
        const pdf = MC.getFirstLinkpathDest(pdfPath, path);
        const notes = pdf && conv[pdf.path];
        if (!notes) { st.notConverted++; return m; }
        const n = notes.find(x => +K >= x.from && +K <= x.to);
        if (!n || !(MC.getCache(n.path)?.blocks || {})['pg' + K]) { st.noAnchor++; return m; }
        st.changed++;
        const sep = table ? '\\|' : '|';
        return `[[${n.path.replace(/\.md$/, '')}#^pg${K}${sep}${label}]] ([pdf](<${pdfPath}#page=${K}>))`;
      });
    });
    const neu = out.join('\n');
    rep.files[path] = st; for (const k in st) rep.total[k] += st[k];
    if (neu === old) continue;
    if (DRY) { const pv = '.work/out/p4-links-preview/' + path; await mkdirs(pv); await A.write(pv, neu); continue; }
    const bk = '.work/backup-phase4-links/' + path; await mkdirs(bk);
    if (!(await A.exists(bk))) await A.write(bk, old);
    if ((await A.read(bk)) !== old && !(await A.read(bk)).length) throw new Error('backup failed: ' + path);
    await V.modify(f, neu);
  }
  await A.write('.work/out/p4-links-' + (DRY ? 'dry' : 'real') + '-' + Date.now() + '.json', JSON.stringify(rep, null, 1));
  const t = rep.total;
  return `${DRY ? 'DRY' : 'APPLIED'} ${TARGETS.length} notes: links ${t.links}, changed ${t.changed}, retargeted ${t.retargeted}, book not converted ${t.notConverted}, no anchor ${t.noAnchor}, already done ${t.skipped}`;
})()
