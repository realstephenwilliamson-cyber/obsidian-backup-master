---
type: prompt
updated: 2026-10-26
---
# Zohar linker

Scripts that turn plain Zohar folio references in the vault's notes into links to the Pritzker notes, following the rule Stephen set on 26 Oct 2026 (the composition named after the reference decides the target; see below). Written on 26 Oct 2026 (third session of the corrections week) to replace the script of session S2 (26 Oct, first session), whose code was not kept; validated against S2's 6,888 new links (`validation.md` in `.work/edits/zohar-open-2026-10-26/`). Kept here under the house rule *Keep what a later session will use*; the general linker for scripture, Tantrāloka and Avot references is [[Reference linker]]. Python 3, standard library only, nothing to install.

## Files

| file | what it does |
|---|---|
| `zoharlink.py` | the linker as a library and command line: parses references, resolves the target note and block from `meta.json`, emits line changes. Everything else imports it. |
| `run_cur.py` | runs the linker over a `{path: text}` dump of the vault and writes the proposal batch (`proposals.json`, `links.json`, `undecided.json`, `noblock.json`, `stephen.json`, `counts.json`). |
| `validate_s2.py` | runs the linker over the pre-S2 text and compares its links with the links S2 made from plain text; writes `validation.md`. Rerun it after any change to the rules. |
| `mkpatch.py` | turns `proposals.json` into the spec of a `linepatch2` job (`.work/edits/linepatch2.tpl.js`): whole-note length and hash before and after, lines that hold the divine name as character offsets only; refuses to write if any line differs from the note, a new link does not resolve, or the plain text would change. |
| `linkitems.py` | links chosen references to a decided target (a note and block, a note's top, or a Sefaria folio note) from a list of items (`[{path, line, block, label, note, block_target}]`) and writes a `linepatch2` spec with the same refusals as `mkpatch.py`; used for Stephen's decisions of 26 Oct 21:20 (the items are in `.work/edits/zohar-open-2026-10-26/`). |
| `decide_packet.py` | lays out references the rule leaves undecided (rows of `undecided.json` or `noblock.json`) beside each candidate passage, for a reader to decide; the decisions then go through `linkitems.py`. |
| `shared-folio-list.js` | (pf417, read-only job) lists every link to the folio sides held by two parashah notes (vols. 1–9), counts them by block and target, and dumps the citing and holding notes for the packet script. Written 28 Oct 2026 for the five blocks of 26 Oct; widen `FIVE` for others (11 shared blocks, 355 links in all on 28 Oct). |
| `shared_folio_packets.py` | builds a reading packet per block: both candidate passages once, then each citing link with its context and the link masked as ⟦label⟧, so the reader does not see the current target; writes `key.json`. |
| `shared-folio-brief.txt` | the readers' brief for those packets (choices A, B, both, neither, unclear; no divine name in the reasons). |
| `zfolio-retarget.tpl.js` | the label-preserving retarget job: moves chosen links from one holder to the other by line and column from Obsidian's link cache, backup first, with its own check (each note differs from its backup only by the moved names; every `#^` link resolves; divine-name count unchanged). Placeholders `__DATA__`, `__BACKUP__`, `__TAG__`. |
| `bundle.js` | the read-only job (pf258) that writes the notes dump and `meta.json` to `.work/xfer/zb27/`: every note under `Texts/Zohar/` except the folio notes, plus every other note (Journal/ and Projects/ left out) with a Zohar reference or link. Rename its output folder for a new run. |
| `selfcheck.py` | draws a seeded random sample of proposed links and lays out, for each, the citing line, the composition named, whether the block exists and the folio's own text in the target note, for a checker to judge. |

## Inputs

- **`meta.json`** (written by `bundle.js`): `"blocks": {note path: [block ids]}` is the authority for which note holds which folio. Ids: `z1-156a` = Zohar vol. 1 folio 156a, `zh-46a` = Zohar Hadash 46a. Other ids (`t1-…`, `v206-…`, `pg…`, `z2-176b-c`) are ignored.
- **a notes dump** `{vault path: full note text}` — every note that may hold a reference (the vault's own index notes are skipped by name, see `SKIP_NOTES`).

## Commands (from the folder that holds `meta.json`, `cur.json`)

```
python3 -I linker/run_cur.py META.json cur.json out/
python3 -I linker/validate_s2.py META.json pre.json s2-patch-1.json out/validation.md out/validation.json
python3 -I linker/selfcheck.py META.json cur.json out/links.json 40 20261027 out/selfcheck-raw.md
python3 -I linker/zoharlink.py parse META.json '*Zohar* 1:76b, 97a (both *ST*); 2:3b'     # try one line
python3 -I linker/zoharlink.py run META.json notes.json out/                                # plain run, no sets
python3 -I linker/mkpatch.py out/proposals.json fresh.json META.json edits/NAME/            # the job spec, from a fresh read of the notes
```

To apply: copy `edits/NAME/` to `.work/edits/NAME/`, make the jobs with `mkjob.py .work/edits/linepatch2.tpl.js NAME pfNNN-NAME-dry.js --backup .work/backup-<topic>-<date>/<name>` (and `--apply` for the second), queue the dry run, read its result, then queue the apply. Before building the spec, read the notes again (a bundle of just the notes in `proposals.json`) and re-run `run_cur.py` with any note that changed since the first bundle.

`-I` keeps Python from importing stray modules from the data folders.

## Outputs of `run_cur.py`

- `proposals.json`: `{path: {"changes": [[line, oldLine, newLine], …], "changes_by_offset": [{line, oldLen, oldSha1, edits: [[start, end, replacement], …]}, …]}}`. Lines are 1-based on the text split on `\n`; `oldLine` is the note's line exactly; every link in `newLine` resolves (target note exists in `meta.json` with that block). A line that holds the divine name is never copied: it is given by number, length and SHA-1, with its edits as character offsets (`replacement` is the full `[[…|label]]`, and `oldLine[start:end]` is the label). To apply, replace `line[start:end]` by `replacement` from the last edit to the first, after checking the hash.
- `links.json`: one row per new link — `path, line, set, label, target, block, composition, rule`. Sets: `A-outside-11` (main-Zohar references outside the 14 vol. 11 notes), `B-vol11-left` (main-Zohar references in the vol. 11 notes), `B-zh-left` (Zohar Hadash references anywhere).
- `undecided.json`: references the rule does not decide (a folio shared by two notes and no composition named; a parenthesis naming two compositions), with `why`.
- `noblock.json`: references no note holds a block for, or whose named composition the vault lacks (RM, TZ, Tiq, Tosafot) or whose named composition's note has no block for that folio; `sole_holder` names the one note that does hold the folio when there is one, so such cases can be approved in bulk.
- `stephen.json`: links that would fall in Stephen's own notes (`Study/Concepts/`, `Study/Hubs/`, `Notes/`), listed, never proposed.
- `counts.json`: the counts, the notes skipped, and any proposal that failed the self-check (should be none).

Nothing is applied by these scripts; the batch is reviewed and applied by the job runner as usual. The data of the 26 Oct run (the links made, the references left undecided or without a block, the run report, the validation) are in `.work/edits/zohar-open-2026-10-26/`.

## The rule as implemented

1. **What is a reference.** Only text introduced by "Zohar" (italic or not: `*Zohar* 1:15a`, `Zohar* 1:46b` inside a longer italic, `Zohar 1:15a`, `Zohar I, 15a`, `Zohar 1.15a`, `*Zohar* III:28a`) or by "ZH"/"Zohar Hadash" (`*ZḤ* 47d`, `ZH 42a`, `*Zohar Ḥadash* 56d–58d`), and the items that continue such a list: separated by `, ` `; ` ` and ` or (for dropped commas in the source) a space, each item a folio `NNNa`/`NNNb` (a–d for ZH), optionally with a volume `1:` `I:` `1.` and a range `–b` / `–16a` (en dash or hyphen). A bare folio takes the last volume given earlier in the list. Half-verses (`Genesis 1:3b`) never match because they are not introduced by Zohar. "Nitsotsei Zohar", "Tiqqunei Zohar", "ha-Zohar", "the *Tiqqunim* of Zohar Hadash" are not introducers. Items already inside links, inline code, headings, frontmatter and code blocks are left alone (an existing link's label still supplies the volume for the items after it).
2. **Composition.** The parenthesis right after the item (`(*ST*)`, `(*MhN, Rut*)`, `(*ST*, standard edition)`), or a group parenthesis covering earlier items (`(both *ST*)`, `(last two *Heikh*)`, `(last three all *MhN, Rut*)`, `(all *Tos*)`; "all" reaches back to the introducer but stops at an item that has its own composition), or, for a glossary line, the entry's bold headword (`***Qav ha-Middah*** … *Zohar Ḥadash* 56d–58d`), or a full name written right before the introducer (`the Idra Rabba (Zohar 3:127b–145a`, `*Idra Zuta, Zohar 3:292b*`). The abbreviations are those of the Pritzker abbreviation lists (ST, Tos, Mat, MhN with Rut/Eikhah/ShS, ShS, Heikh, Piq, RR, SO, QhM, IR, IZ, SdTs, and the full names); a parenthesis naming two compositions is undecided unless it says which is meant ("labeled as *Tos*, but in fact *MhN*"). Non-deciding: *Hash* (Hashmatot, a location), SA (*Sefarim aherim*, variant readings; not Sava de-Mishpatim), "standard edition", "Vol. 5, n. 22", "Nitsotsei Zohar, n. 2". Absent from the vault: *RM*, *TZ*, *Tiq* (Tiqqunim in Zohar Hadash), *Tosafot*.
3. **Target.** Composition named → the note(s) of that composition (table `COMPOSITIONS`) that hold the block; none → noblock; several → the one holding the range's last folio too, else undecided. No composition → the sole holder of the block; if several hold it, the main-text note (volumes 1–9); if two main-text notes hold it (a folio side on which one parashah ends and the next begins), the one that also holds the range's last folio, else undecided. Tos goes to 11.08 or to 12.12 (Passages (Mis)Labeled as Tosefta) according to which holds the folio.
4. **Form.** `[[Zohar 2.06 - Parashat Va-Yetse#^z1-156a|1:156a]]`: the label is the printed text of the item (`1:161a–b`, `2:176b–179a`, `III:28a`, `3.233a`); a range links the first folio's block; the italic `*Zohar*`/`*ZḤ*` stays outside. In a note (or book) whose existing links carry the word in the label (`[[…|Zohar 2:176b]]`, `[[…|Zohar III, 137b]]`) a non-italic introducer is taken into the label of the first item. In a table row the pipe is written `\|`. Nothing else on the line changes.

## Changing the rules

- A new composition note: add its number to `COMPOSITIONS` and its tokens to `COMP_TOKENS` / `NAME_TOKENS` in `zoharlink.py`.
- To link a reference to the sole holder of its folio even when the named composition has no block there (the S2 fallback for "(all *IR*)"), filter `noblock.json` on `sole_holder` rather than changing the rule.
- After any change rerun `validate_s2.py`; the M1/J1-02 agreement should stay at 6,068/6,071 and 799/817 or improve, and every difference must be explained.

## The run of 26 Oct 2026

- Stephen's go-ahead (26 Oct, 18:07): link the plain main-Zohar references outside vol. 11, by the same rule as S2.
- Bundle pf258 (625 notes), fresh read pf283 (the 118 notes concerned; 6 had changed since, one proposal line with them, re-run), spec by `mkpatch.py`, dry run pf284, apply pf285: **1,536 new links in 116 notes (488 lines)**; plain text unchanged; unresolved links 16 files / 30 links before and after. Backups: `.work/backup-corrections-2026-10-26/c-zlink/`.
- By set: 1,526 main-Zohar references outside vol. 11, 8 left in the vol. 11 notes, 2 Zohar Hadash. By rule: sole holder 1,113; main text 121; composition named 294; range tie-break 8.
- Left: 37 undecided (`undecided.json`) and 1,363 without a block (`noblock.json`; 189 of them have a `sole_holder`, for a bulk decision). See the run report for S2's six lost range endings and the folios missing in 11.09 and 11.04.

## Stephen's decisions of 26 Oct 2026, 21:20

- References whose named composition's note lacks the folio (104, after the 84 RM/Tiq/TZ/Tosafot references and 5.05's `2:5a (*Piq*)` were set aside): each target read by an agent (`fallback-decisions.json`, checked on 17: `fallback-check17.json`); 86 linked with `linkitems.py` (pf309–pf310), 18 plain.
- Folios no Pritzker note marks: the 44 with a Sefaria folio note linked to it (pf302, pf304); the other 708 have no note to link to and stay plain.

## Stephen's answers of 26 Oct 2026, 23:13

- The 37 undecided (a folio side shared by two parashot, no composition named) and the seven `1:108a (*ST*)` references (11.09 lacks the folio): `decide_packet.py` laid out each citing note beside both candidate passages; an agent decided them (`undecided-decisions.json`), a second agent decided them again without the answers (`undecided-check44.json`, 44 of 44 the same); `linkitems.py` linked 43 (pf339–pf340); 11.08's "On this stone, cf. 1:193a" stays plain. The seven *ST* references go to 11.08 Tosefta at `^z1-108a`, whose text is the passage cited.
- S2's six lost range endings restored on the same links (pf333–pf334).
- Done 28 Oct 2026: the links to the five shared folio sides named on 26 Oct (`^z1-193a`, `^z1-165b`, `^z3-156b`, `^z2-32a`, `^z1-120b`): 193 links, 178 decided (the folio index and the five Sefaria folio notes name their parashah and were left out) by two readers blind, who agreed on all; the 103 they both placed in the other note were moved (pf419–pf423); 14 left (`listed.json`). Data in `.work/edits/zfolio-2026-10-28/`. Seen: 8.04 Emor carries a `**[2:32a]**` marker between 3:93b and 3:94a, and the text after it is the Ishmael passage; not checked against the print.

