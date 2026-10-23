---
type: prompt
updated: 2026-10-22
---
# Sefaria import scripts

The scripts that built the 22 Oct 2026 imports from Sefaria's export: *Kedushat Levi*, *Likutei Moharan* and *Mei HaShiloach* vol. II (`Texts/Chasidut`), the Babylonian Talmud (`Texts/Talmud`), Maimonides' *Mishneh Torah*, *Guide for the Perplexed*, *Eight Chapters* and Introduction to the Mishnah (`Texts/Maimonides`), and the *Kitzur Shulchan Arukh* (`Texts/Kitzur Shulchan Arukh`). They are in `AI/Prompts/Scripts/Sefaria import/`. [[Add a primary text to Texts]] is the prompt to use with them; the record is the AI log, 22 Oct 2026 (afternoon), and the project doc *Sefaria imports (22 Oct 2026) - record*.

They were written for a cloud workspace with the work in `/home/claude/sef/` (the three Hasidic works and `common.py`), `/home/claude/tal/` (the Talmud) and `/home/claude/ram/` (Maimonides and the Kitzur). Copy them there, or change the paths at the top of each script.

## Getting the data

- Sefaria's export is on Google Cloud Storage, bucket `sefaria-export` (the AI's network must allow `storage.googleapis.com`: claude.ai → Settings → Capabilities). List a folder with `https://storage.googleapis.com/storage/v1/b/sefaria-export/o?prefix=json/Chasidut/` and fetch a file with `https://storage.googleapis.com/sefaria-export/<path, URL-encoded>`. `last_export.txt` gives the export's date.
- Texts: `json/<category>/…/<Work>/English/<version title>.json`, one file per version; the licence is in each file (`license`). Use one version and add another only where the first has no text, saying so where it appears.
- Links: `links/links0.csv` … `links16.csv` (about 680 MB together). Stream them through `grep` for the works wanted (`curl … | grep -E 'Kedushat Levi|…' > l0.csv`); the columns are *Citation 1, Citation 2, Connection type, Text 1, Text 2, Category 1, Category 2*.
- The runner jobs `pe17-torahmap` and `pe18-blocks` (in `.work/out`, 22 Oct) listed the Torah and Tanakh notes with their verse blocks; `common.py` reads them to know which verse links exist.

## The scripts

| File | What it does |
|---|---|
| `common.py` | HTML to Markdown (bold, italics, line breaks, footnotes with nested italics, editorial ‹angle brackets› kept visible); verse links (`link_refs`: linked where Sefaria links the same verse to the passage, or as printed with `as_written=True`, for the Talmud and Maimonides); Talmud links (`link_talmud`: *Shabbat* 31a, Berachot 3a → the side of the daf note); footnote blocks; frontmatter; the divine-name count (counts only) |
| `gen.py` | *Kedushat Levi* (Munk; community passages marked), *Likutei Moharan* (Mykoff), *Mei HaShiloach* vol. II (community) |
| `gen_talmud.py`, `tal_index.py` | The Talmud (William Davidson edition): one note per daf named as the Daf Yomi table names it, a block per line (`^2a-1`), and the margins (Torah Or, Mesoret HaShas, Ein Mishpat, In this vault) from the links; then the Talmud and seder index notes |
| `gen_mt.py` | *Mishneh Torah* (Touger, one note per chapter, a block per halakhah, *In the Talmud* and *Verses* boxes), the *Guide* (Friedländer), *Eight Chapters* (Gorfinkle), the Introduction to the Mishnah (Nataf), the *Kitzur* (Davis) |
| `import-bundles.js.tpl` | Runner job: creates the notes of JSON bundles (about 18 MB each) in `.work/pe-big/`, pausing every 100 notes, refuses if a note or name exists, then makes the edits in `edits.json` (each anchor found exactly once, notes backed up first) |
| `check-links.js.tpl` | Runner job: in the given folders, every link resolves and every `#^block` and `#heading` exists |
| `talmud-links.js.tpl` | Runner job: links Talmud references (*BT Ḥagigah 13a*, *b. Šabb. 31a*, *Shabbat 31a*) in older notes to the daf notes, skipping the Jerusalem Talmud and the Tosefta |
| `talmud-links-2.js` | The second pass as it ran (22 Oct 2026, with its data): every note in `Texts/` and `Library/` outside the Talmud, Maimonides and Kitzur folders, adding the Jewish Annotated New Testament's *b. Shabb*. 30b and *b. Ber.* 64a forms; the first line `// APPLY` makes it an apply |

## Checks used

- Every segment of the source appears in the notes (plain text compared, bold and links stripped).
- Every link and anchor resolves (`check-links`), and the vault's unresolved-link count is unchanged.
- Verses linked as printed were tested against Sefaria's links where both exist: of 7,322 references in the Talmud with a Sefaria link to the same chapter, 60 named another verse, all of them ranges.

## Fixed after the first run (22 Oct 2026)

- `gen_talmud.py` wrote the label of a Mesoret HaShas link from the text after the first word, which doubled a two-word name (*Bava Kamma Kamma 46a:6*); it now drops the tractate's whole name. The 4,215 labels in 1,661 daf notes were corrected in the vault (job `pe36-fix-talmud`).
- A link to one line of a daf now checks that Sefaria has English for that line (some segments are empty and get no block); otherwise it points to the side's heading (`common.py` keeps `TAL_BLOCKS`; `gen_talmud.py` has `seg_ok`). Eleven such links were corrected in the vault.
- After an import, run the reference linker (*Reference linker*, B3) over the new folders with `B3OVERRIDE` set to `heb` for the Jewish texts. Friedländer's *Guide* mixes the two numberings (Deut. 5:24 is the Hebrew verse, Exod. 20:24 and Deut. 5:31 the English); it was run with `eng`, which moved only those two, whose numbers exist only in the English numbering, to the Hebrew verse. B3 leaves Pirkei Avot 5:20 to the end and chapter 6 undecided, because editions number them differently: check what the passage quotes against the vault's [[Pirkei Avot]] before linking (in *Likutei Moharan* 11 matched; I 088 "5:20" quotes 5:17 and I 102 "6:1" quotes 6:11).
