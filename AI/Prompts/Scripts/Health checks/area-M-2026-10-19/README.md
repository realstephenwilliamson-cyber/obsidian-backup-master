# Area M re-run jobs and the render checks of 19 Oct 2026

Runner jobs (`(async () => { … })()`, read-only; copy into `.work/queue/` to run; results `.work/out/<name>.result.txt`, details `.work/out/areaM2/<name>.json`). Written by the audit agent `audit-M` for the complete vault audit of 19 Oct 2026 (project docs `claude/audit-2026-10-19/`), filed here so that the end-of-session clean-up of `.work/queue/done` does not lose them (Area L finding L-06).

| File | Check | Measures |
|---|---|---|
| `m2-00-changed.js` | — | every file changed since a cutoff, matched to the record of writes; backups compared with the notes now, feature by feature |
| `m2-01-frontmatter.js` | 1 | frontmatter parses, position, duplicate keys, tabs; the tags record |
| `m2-02-links.js` | 2 | links, embeds, frontmatter links, `#^block`/`#heading` sub-paths, unresolved |
| `m2-04b-markers-noid.js` | 4b | page-marker lines without a `^pgK` id, by folder |
| `m2-07-names.js` | 7 | duplicate note names, non-ASCII names, names over 100 characters |
| `m2-08-properties.js` | 8 | property vocabularies, counts, value types, the catalog notes |
| `m2-10-hardcoded.js` | 10 | hard-coded dates, paths and links in Templates/; the `EPOCH` lines |
| `m2-12-hidden.js` | 12 | sizes of `.obsidian`, `.smart-env`, `.trash`, `.work`; backup folders named in no note |
| `m2-13-dataview.js` | 13 | dataview/dataviewjs blocks, view calls, `.base` files |
| `m2-14-tags.js` | 14 | tags from the cache and `getTags()`; what relies on a tag |
| `m2-15-workprop.js` | 15 | Library/Texts notes without `work`/`book`/`source`/`collection` |
| `render-j.js` | — | opens notes and Bases in reading mode and records Dataview/console errors and button labels (note: opening a `.base` makes Obsidian re-save it) |
| `render-holydays-testdates.js` | — | renders the date header and the Daily Office for test dates in temporary notes (made and trashed) — add `// APPLY` as the first line to run |
| `cards-after.js` | — | the 108 card notes: count, numbers, card lines, links |
| `tags-dollar-check.js` | — | `$` in the frontmatter of the tags record's notes (J2-11) |

Baseline values of 19 Oct 2026, 14:26 EDT: see the merged report, section 7.
