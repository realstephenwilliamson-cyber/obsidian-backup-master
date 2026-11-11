// APPLY
(async () => {
  // pf835-prompts-docs (10 Nov 2026): the new audit prompt in Prompts - read me, and the AI log (the prompt, the Class note template, next job number).
  const JOB = "pf835-prompts-docs", V = app.vault, D = { errors: [], log: [] };
  const rep = (t, a, b) => { const n = t.split(a).length - 1; if (n !== 1) { D.errors.push(`expected 1 of "${a.slice(0, 50)}" got ${n}`); return null; } return t.split(a).join(b); };
  const edit = async (p, fn) => { const f = V.getAbstractFileByPath(p); if (!f) { D.errors.push("missing " + p); return; } const t = await V.read(f), r = fn(t); if (r === null) return; await V.modify(f, r); D.log.push("edit " + p); };
  await edit("AI/Prompts/Prompts - read me.md", t => {
    const m = t.match(/^\| \[\[Complete vault audit\\\|Complete vault audit\]\].*\n/m);
    if (!m) { D.errors.push("audit row missing"); return null; }
    const row = "| [[Audit of the work since 3 Nov 2026]] | An independent check of the AI sessions' work from 3 Nov 2026: new texts, links, the homily page, Home, subjects and Bases, the Guide and prompts, size and Git; two waves, the cheap one first | Read-only; the report only | AI; Sonnet for wave 1, Fable page readers for wave 2 | M |\n";
    return t.replace(m[0], () => m[0] + row);
  });
  await edit("AI/AI log.md", t => {
    t = rep(t, "**Next free job number: pf835.**", "**Next free job number: pf836.**"); if (t === null) return null;
    return rep(t, "(the Summa notes may link it). **Next free job number pf835.**", "(the Summa notes may link it).\n- **Also (evening):** the prompt [[Audit of the work since 3 Nov 2026]] (read-only; waits for the container's reset and a meter reading; in *Prompts - read me*, pf835); the template [[Class note]] in `Templates/` for the core Slides plugin (a draft, not yet tried: Stephen will try the plugin). *Map new connections* is out of date (default scope 5 Oct, `Texts/New Testament` for `Texts/Bible/New Testament/`, nothing on the Mālinīvijayottara, Enoch, Qumran or the JANT notes, setup lines from the Cowork days); not yet rewritten. **Next free job number pf836.**");
  });
  await V.adapter.write(`.work/out/${JOB}.detail.json`, JSON.stringify(D, null, 1));
  return JOB + ": " + D.errors.length + " errors " + D.errors.join("|") + " " + D.log.join(",");
})()
