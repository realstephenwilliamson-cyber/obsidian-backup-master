---
type: prompt
updated: 2026-11-07
---
# JANT links (7 Nov 2026)

`jantlinks.py` links references in the Jewish Annotated New Testament notes (annotations and introductions) whose targets are in the vault but which the 13 Oct linker ([[Reference linker]]) left plain. It reads a dump of the JANT notes (`{path: text}`, made by a read-only runner job) and writes `edits.json` (`[{id, path, old, new}]`, one edit per changed line, for the `pf591-audfix-apply.js` template in `.work/edits/sdk-templates-2026-11-03/`) and `proposals.json` (one entry per link, with its category and context). Run: `python3 jantlinks.py jant.json <outdir>`.

| Category | What | Target |
|---|---|---|
| ezra | `*4 Ezra*`, `*5 Ezra*`, `*6 Ezra*`, `2 Esd` with chapter.verse (or a chapter) | NRSVue 2 Esdras (4 Ezra = 2 Esd 3–14, 5 Ezra = 1–2, 6 Ezra = 15–16, same numbering) |
| one | Jude, Philem, 2 Jn, 3 Jn with a verse only | the New Testament note (`Jude 01#^1-9`) |
| avot | `*m. Avot*` C.V | Pirkei Avot, chapters 1–4 and 5.1–19 only; 3.12 left plain (the JANT there numbers as Danby, the vault as Sefaria) |
| note | `C.Vn.`, `v Nn.` (the JANT's own notes) | the JANT annotation whose key covers the verse |
| see | `see` / `cf.` + C.V with no book (the same book) | the New Testament note; left plain when the sentence so far names another work (a link to another book, a siglum with numbers, a plain book abbreviation, Josephus, Philo) |

Skipped: headings, frontmatter, text inside links or code. The apply job checks every new link against the target note's block ids and leaves misprints plain ("Rev 3.30", "Heb 71.29"). Check all links before writing any note: a note just rewritten has no block cache for a moment, so links into it fail (pf781 left 32 good links plain that way; pf784 made them).

Not in the vault, so not linked (counts in the JANT notes, 7 Nov 2026): Pseudepigrapha about 480 (1 Enoch 142, Jubilees 70, 2 Baruch 56, Psalms of Solomon 39), Mishnah other than Avot about 270, Josephus 288, Qumran 261, Philo 204, Midrash Rabbah 162 (Genesis Rabbah 78), other midrash and targum 181, Tosefta 81, Yerushalmi 57. Since 9 Nov 2026 1 Enoch, the Qumran texts and Midrash Rabbah are linked by `jantlinks2.py` (below).

## jantlinks2.py (9 Nov 2026)

The second linker, for the texts added on 9 Nov 2026. `python3 jantlinks2.py jant.json enoch_ids.json dss_ids.json <outdir>`, where `jant.json` is a dump of the JANT notes and the two id files map each note name (`1 Enoch 038`, `DSS 1QS`) to the block ids written in it; it writes `edits.json` for an apply job that checks every new block link before it writes (as pf784 and pf803 do) and `proposals.json`.

| Category | What | Target |
|---|---|---|
| enoch | `*1 En.*` or `*1 Enoch*` C.V, with lists | [[1 Enoch]], `[[1 Enoch 038#^38-2]]` |
| qumran | 1QS, CD (A, B), 1QM, 1QpHab, 1QSa, 1QSb, 11QTemple (11QSTemple, 11QT, 11Q19), 11QMelch, 4QFlor, 11QPsa, 1QapGen, 4QNNN + col.line | `[[DSS 1QS#^3-13]]` when that line is in the note; CD cols 1–16 are CD-A, 19–20 CD-B |
| rabbah | *Gen. Rab.*, *Exod. Rab.*, *Lev. Rab.*, *Num. Rab.*, *Deut. Rab.*, *Song Rab.*, *Ruth Rab.*, *Lam. Rab.*, *Eccl. Rab.*, *Esth. Rab.* + C.S | Sefaria: `Bereshit_Rabbah.C.S` and the other Torah Rabbot to the section; the Megillot Rabbot to the chapter only (Sefaria numbers them by chapter, verse and section) |

Left plain: 1QH and 1QHa (numbering not checked), 2 and 3 Enoch, references without a line number. Run on 9 Nov 2026 over all 362 JANT notes: 551 links in 167 notes (enoch 126, qumran 254, rabbah 171).
