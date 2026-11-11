// APPLY
(async () => {
  // pf830-ai-log-items (10 Nov 2026): AI log entry for the routine items (Other -> Religious-Studies/Philosophy, Bases merge, CIS keys, May's Genocide);
  // next free job number; one Open work line; the answered item is taken off Notes/Discuss next session.md (it says the session deletes answered items).
  const JOB = 'pf830-ai-log-items', ad = app.vault.adapter, get = p => app.vault.getAbstractFileByPath(p);
  const D = { when: new Date().toISOString(), log: [], errors: [] };
  const log = get('AI/AI log.md'), dis = get('Notes/Discuss next session.md');
  if (!log || !dis) return JOB + ': missing file';
  let t = await app.vault.read(log);
  const need = s => { if (t.split(s).length !== 2) { D.errors.push('not exactly once: ' + s.slice(0, 60)); return false; } return true; };
  const A = '**Next free job number: pf821.**', B = '## 10 Nov 2026 (14:36–15:20)', C = "- **Stephen's own:** [[Open items]]";
  if (![A, B, C].every(need)) { await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1)); return JOB + ': ' + D.errors.join(' | '); }
  const entry = `## 10 Nov 2026 (15:20–15:45): the routine items: "Other" subject, Bases, CIS answer keys, May's *Genocide* (Sonnet lead in the cloud)

- **Stephen:** do the routine items on Sonnet; Homer, Borges, Chan and Russell are philosophy; the rest of "Other" is religious studies. Meter at the start: container 64 %, week 24 %, Fable 21 %.
- **"Other" (pf821 survey, pf822 dry, pf823 apply):** the subject is now **Religious-Studies** (hyphenated like Biblical-Studies and Sanskrit-Study, because the subject value is also the folder name): 14 catalog notes; folders \`Catalog/Religious-Studies\` and \`Library/Religious-Studies\` renamed through Obsidian, the index note renamed and rewritten (its view is *Religious Studies*). Homer, Borges, Chan (*Source Book*) and Russell (*History of Western Philosophy*) moved to Philosophy with their PDFs and Markdown copies, subject Philosophy; the Academia.edu *AI Review* PDF and its note, which the Philosophy catalog note *AI Review of Virtual Identity Crisis* pointed to in \`Library/Other\`, moved to \`Library/Philosophy\` too. Also changed: the subject list in \`Templates/Views/quick-capture/view.js\` (the *Add a book you have on paper* form), the Vault Guide (two places), the prompts *Add new files from Downloads* and *Add scholar pages*, the subjects of Timothy Knepper and J.N. Mohanty in \`Catalog/Scholars\`, and \`AI/Smart Connections exclusions.md\`. Knepper, Jones (*Mysticism Examined*) and Chuang Tzu stay in Religious-Studies (not decided separately; say if one should be Philosophy). Unresolved links 24 before and after. pf823's replace changed only the first of two lines in *Scholars.md* (Knepper's line kept "Other"); pf829 corrected it. **Smart Connections:** its real exclusion list is in \`.smart-env/smart_env.json\`, not in the note; the folder *Library/Other/** is now *Library/Religious-Studies/** and the four moved books are in *Library/Philosophy*. Stephen: update *Manage excluded folders* (the note lists the new lines).
- **Bases (pf824):** *Needs review.base* trashed (the *Review* view of *Catalog.base* does the same; nothing linked to it). *Physical Library*, *Shelf check* and *To delete* are now the three views of \`Catalog/Library checks.base\` (same filters, columns and sorts); the three old files trashed. Vault Guide and two prompts reworded.
- **CIS answer keys, Chapters 4–12 (pf825 survey, pf826 dry, pf827 apply):** filed as the keys for Chapters 1–3 are: PDFs \`Library/Sanskrit/Chapter_N.pdf\`, Markdown copies \`Study/Sanskrit/CIS - Answers to Chapter N Exercises (Ruppel).md\` (one note each, page marker and block id), catalog notes in \`Catalog/Sanskrit-Study\` linking the chapter note. The PDFs' Devanagari is garbled in the text layer: rebuilt from the printed transliteration where it stands beside it; Chapter 4's parentheses from the first forms of each list; Chapter 7 item 4 from the roots and meanings; Chapter 10 item 1 and Chapter 12's note on typos read from the page images and kept as printed (Chapter 12's typo note may itself contain a slip in the print); Chapter 11 item 1m prints a missing-glyph box, read as ḷ. Not proof-read word for word. The originals stay in Downloads. Scripts: \`/home/claude/cis\` (cloud, not kept).
- **May, *Genocide: A Normative Account* (pf828 dry, pf829 apply):** PDF \`Library/Philosophy/May - Genocide - A Normative Account (2010).pdf\` (16.8 MB, 304 pages, the Internet Archive's OCR), catalog note in \`Catalog/Philosophy\` (PDF only: no Markdown copy yet), See also both ways with *Limiting Leviathan*, and Larry May queued in *Scholars* (two works). *Limiting Leviathan* is already in the library (273 pages; skipped); the copy in Downloads is a duplicate.
- **Not done:** the four mobile buttons onto the normal Home (Stephen's question stays in *Discuss next session*); the homily mock-up (Fable); Markdown copy of *Genocide*. **Next free job number pf831.**

`;
  t = t.replace(A, '**Next free job number: pf831.**').replace(B, entry + B)
       .replace(C, "- **Larry May, *Genocide: A Normative Account*** (filed 10 Nov 2026): PDF and catalog note only; the Markdown copy (Add new files from Downloads, step 7) is not made.\n" + C);
  await app.vault.modify(log, t);
  let d = await app.vault.read(dis);
  const m = d.match(/^- Can we trash the "Needs Review" base\?.*\n/m);
  if (!m) D.errors.push('Discuss bullet not found'); else await app.vault.modify(dis, d.replace(m[0], ''));
  await ad.write('.work/out/' + JOB + '.detail.json', JSON.stringify(D, null, 1));
  return JOB + ': done, ' + D.errors.length + ' errors ' + D.errors.join('|');
})()
