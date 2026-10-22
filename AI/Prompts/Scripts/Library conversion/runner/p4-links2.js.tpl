(async () => {
  // Markdown-first page links, second round (9 Oct 2026; same form as step 7(a)): in the notes under the prefixes below, each link
  // to a page of a converted PDF becomes  [[<chapter note>#^pgK|label]] ([pdf](<the PDF link>))  (wikilink form: ([[x.pdf#page=K|pdf]])).
  // Frontmatter is not touched. Links whose PDF has no Markdown copy, or whose page block is missing, stay as they are.
  // Backups: .work/backup-phase4-links2/. window.DRY !== false -> report only, with a few previews in .work/out/links2-preview/.
  const DRY = window.DRY !== false;
  const PREFIXES = __PREFIXES__;
  const MC = app.metadataCache, V = app.vault, A = app.vault.adapter;
  const range = (s) => { const m = String(s || '').match(/(\d+)\s*[–-]\s*(\d+)/); return m ? [+m[1], +m[2]] : null; };
  const conv = {};
  for (const f of V.getMarkdownFiles()) {
    const fm = MC.getFileCache(f)?.frontmatter; if (!fm || !fm.source_pdf || !fm.converted) continue;
    const r = range(fm.pdf_pages); if (!r) continue;
    (conv[fm.source_pdf] = conv[fm.source_pdf] || []).push({ path: f.path, from: r[0], to: r[1] });
  }
  const mkdirs = async (p) => { let cur = ''; for (const x of p.split('/').slice(0, -1)) { cur = cur ? cur + '/' + x : x; if (!(await A.exists(cur))) await A.mkdir(cur); } };
  const rep = { dry: DRY, notes_seen: 0, notes_changed: 0, links: 0, changed: 0, notConverted: 0, noAnchor: 0, done_before: 0, errors: [], by_prefix: {} };
  const RE = /\[([^\]]*)\]\((?:<([^>]+?\.pdf)#page=(\d+)>|([^)<>\s]+?\.pdf)#page=(\d+))\)|\[\[([^\]|#]+?\.pdf)#page=(\d+)(\\?\|)([^\]]*)\]\]/g;
  let previews = 0;
  const files = V.getMarkdownFiles().filter(f => PREFIXES.some(p => f.path.startsWith(p))).sort((a, b) => a.path.localeCompare(b.path));
  for (const f of files) {
    try {
      const old = await V.read(f); if (!old.includes('#page=')) continue;
      rep.notes_seen++;
      const m0 = old.match(/^---\n[\s\S]*?\n---\n/); const head = m0 ? m0[0] : ''; const body = old.slice(head.length);
      let n = 0;
      const nb = body.split('\n').map(line => {
        const table = line.trimStart().startsWith('|');
        return line.replace(RE, (m, label, pa, Ka, pb, Kb, pw, Kw, sepw, labelw, off, whole) => {
          const pdfPath = pa || pb || pw, K = Ka || Kb || Kw, lab = pw ? labelw : label;
          rep.links++;
          if (lab === 'pdf' && /\]\] \($/.test(whole.slice(Math.max(0, off - 4), off))) { rep.done_before++; return m; }
          const pdf = MC.getFirstLinkpathDest(pdfPath, f.path); const notes = pdf && conv[pdf.path];
          if (!notes) { rep.notConverted++; return m; }
          const c = notes.find(x => +K >= x.from && +K <= x.to);
          if (!c || !(MC.getCache(c.path)?.blocks || {})['pg' + K]) { rep.noAnchor++; return m; }
          rep.changed++; n++;
          const sep = table ? '\\|' : '|';
          const pdfHalf = pw ? `[[${pdfPath}#page=${K}${sep}pdf]]` : `[pdf](<${pdfPath}#page=${K}>)`;
          return `[[${c.path.replace(/\.md$/, '')}#^pg${K}${sep}${lab}]] (${pdfHalf})`;
        });
      }).join('\n');
      if (!n) continue;
      rep.notes_changed++;
      const pre = PREFIXES.find(p => f.path.startsWith(p)); rep.by_prefix[pre] = (rep.by_prefix[pre] || 0) + n;
      if (DRY) { if (previews < 6 && (previews < 2 || Math.random() < 0.002)) { previews++; const pv = '.work/out/links2-preview/' + f.path; await mkdirs(pv); await A.write(pv, head + nb); } continue; }
      const bk = '.work/backup-phase4-links2/' + f.path; await mkdirs(bk);
      if (!(await A.exists(bk))) await A.write(bk, old);
      await V.modify(f, head + nb);
    } catch (e) { rep.errors.push(f.path + ': ' + e.message); }
  }
  await A.write('.work/out/links2-' + (DRY ? 'dry' : 'real') + '-__TAG__.json', JSON.stringify(rep, null, 1));
  return `${DRY ? 'DRY' : 'APPLIED'} notes seen ${rep.notes_seen}, changed ${rep.notes_changed}; links ${rep.links}, changed ${rep.changed}, no Markdown copy ${rep.notConverted}, no page block ${rep.noAnchor}, done before ${rep.done_before}, errors ${rep.errors.length}`;
})()
