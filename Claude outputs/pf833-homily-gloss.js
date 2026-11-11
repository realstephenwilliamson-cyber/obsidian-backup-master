// APPLY
(async () => {
  // pf833-homily-gloss (10 Nov 2026): installs the glossed homily page (option C: a closed drawer of glosses under each New Testament reading) as
  // Templates/Views/homily-page/view.js and view.css (new files from .work/edits/homily-gloss-2026-11-10/), after a backup of the two old files to
  // .work/backup-homily-gloss-2026-11-10/. It renders four test homilies off screen (as homily-page-render.tpl.js does); on any error in a test
  // page it puts the old files back and says so.
  const JOB = "pf833-homily-gloss", V = app.vault, ad = V.adapter, MC = app.metadataCache, out = [], sleep = ms => new Promise(r => setTimeout(r, ms));
  const DIR = "Templates/Views/homily-page/", NEW = ".work/edits/homily-gloss-2026-11-10/", BK = ".work/backup-homily-gloss-2026-11-10/";
  const files = ["view.js", "view.css"];
  for (const f of files) if (!(await ad.exists(NEW + f))) return JOB + ": missing " + NEW + f;
  if (await ad.exists(BK + "view.js")) return JOB + ": backup folder already holds files";
  if (!(await ad.exists(BK))) await ad.mkdir(BK);
  const old = {};
  for (const f of files) { old[f] = await ad.read(DIR + f); await ad.write(BK + f, old[f]); }
  const unBefore = (() => { let nl = 0; for (const o of Object.values(MC.unresolvedLinks)) nl += Object.values(o).reduce((a, b) => a + b, 0); return nl; })();
  for (const f of files) await ad.write(DIR + f, await ad.read(NEW + f));
  out.push("installed; backups in " + BK);
  const CASES = [
    ["Proper 28A Track 2 (15 Nov)", 'date: 2026-11-15\noccasion: "[[Proper-28A]]"'],
    ["Proper 27A (8 Nov)", 'date: 2026-11-08\noccasion: "[[Proper-27A]]"'],
    ["Saint Thomas (Prayer Book lessons)", 'date: 2026-12-21\noccasion: "[[Holy Days (BCP 1979)]]"\nfeast: "Saint Thomas the Apostle"\npropers: feast'],
    ["Proper 27B with All Saints (both)", 'date: 2027-11-07\noccasion: "[[Proper-27B]]"\nfeast: "All Saints\' Day"\npropers: both'],
  ];
  const dvp = app.plugins.plugins.dataview; if (!dvp?.api?.executeJs) return "Dataview api not available";
  const Component = Object.getPrototypeOf(Object.getPrototypeOf(Object.getPrototypeOf(dvp))).constructor;
  const made = []; let errors = 0;
  for (const [n, fm] of CASES) { const p = `Notes/HP gloss ${n.replace(/[^\w ,-]/g, "")}.md`; if (!V.getAbstractFileByPath(p)) await V.create(p, `---\ntype: test\n${fm}\n---\n# test\n`); made.push(p); }
  await sleep(2500);
  for (const p of made) {
    const comp = new Component(); comp.load();
    const el = document.createElement("div"); el.className = "markdown-preview-view markdown-rendered"; el.style.cssText = "position:absolute;left:-10000px;top:0;width:800px"; document.body.appendChild(el);
    const t0 = Date.now();
    try {
      await dvp.api.executeJs('await dv.view("Templates/Views/homily-page")', el, comp, p);
      let last = -1; for (let i = 0; i < 40; i++) { await sleep(400); const L = el.innerText.length; if (L === last && L > 0) break; last = L; }
      const q = s => [...el.querySelectorAll(s)], errs = q(".hp-error").map(e => e.innerText);
      errors += errs.length;
      out.push(`==== ${p} (${Date.now() - t0} ms incl. ~400 ms settle)\nreadings ${q(".hp-reading").length}; verses ${q(".hp-verse").length}; errors ${errs.join(" || ") || "none"}`);
      for (const b of q(".hp-reading")) {
        const g = b.querySelector(".hp-gl");
        out.push(`  [${b.querySelector(".hp-h3")?.innerText}] ` + (g ? g.querySelector("summary").innerText + ` | open=${g.open}; items JANT ${g.querySelectorAll(".hp-gl-sec:nth-of-type(1) .hp-gl-item").length}` : "no drawer"));
      }
      const g0 = el.querySelector(".hp-gl"); if (g0) { g0.open = true; out.push("  first drawer text: " + g0.innerText.replace(/\s+/g, " ").slice(0, 700)); }
    } catch (e) { errors++; out.push(`${p}: render failed: ${e.message}`); }
    comp.unload(); el.remove();
  }
  for (const p of made) { const f = V.getAbstractFileByPath(p); if (f) await V.trash(f, false); }
  await sleep(1500);
  const unAfter = (() => { let nl = 0; for (const o of Object.values(MC.unresolvedLinks)) nl += Object.values(o).reduce((a, b) => a + b, 0); return nl; })();
  out.push(`unresolved links ${unBefore} -> ${unAfter}`);
  if (errors) { for (const f of files) await ad.write(DIR + f, old[f]); out.push("ERRORS: old view.js and view.css put back"); }
  else out.push("OK: new view installed");
  await ad.write(`.work/out/${JOB}.txt`, out.join("\n"));
  return out.join(" | ").slice(0, 900);
})()
