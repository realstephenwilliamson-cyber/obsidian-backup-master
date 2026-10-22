---
type: prompt
date: 2026-10-07
---
# Cloud session prompt: survey of further free texts (estimate only)

A short, cheap job for a Claude Code cloud session (same repository as the phase 7 build). It **builds nothing**: it finds each text's free source, checks the licence, counts the text exactly, and estimates what a full build would make and cost. Expect a few dollars of the credit. Start it the same way as the phase 7 prompt (claude.ai/code → the repository with `tools/` → paste the box). It can run while the phase 7 build is running, in a second session.

````text
Survey only: do not build notes or open a pull request. Work only in this repository; nothing outside GitHub is to be changed.

FIRST read tools/ and the round reports (NT_BUILD_REPORT.md, SKIPPED.md, ROUND6_REPORT.md if present) to see how texts are built here: one note per natural unit, block ids, YAML front matter, ASCII file names.

For each text below:
1. Find the best free source, preferring GitHub copies (this environment reaches them most easily): PerseusDL/canonical-greekLit, eBible.org USFM, OliverHellwig/sanskrit (DCS), Project Gutenberg or its GitHub mirrors, CCEL. If a site refuses automated access, say which and don't work around it.
2. Copy the licence and edition statement from the source itself. For translations, give the translator and the date of first publication from the source, and say whether that makes it public domain in the US (published before 1931) or under an open licence. Mark anything you can't establish as "unverified".
3. Count exactly from the downloaded files: units (chapters, Stephanus pages and sections, verses, homilies), words and characters, and for the DCS texts the verses and tokens analysed (and how many verses of each text the DCS does NOT cover).
4. Propose the note layout (unit per note, naming, block ids), and estimate: number of notes, total Markdown size in MB, hours of session time, and a rough cost range in dollars for building it with checks, scaled from what this repository's earlier rounds produced. Say plainly that the cost is an estimate.

The texts:
- A. Brenton's Septuagint, the Greek text (eBible grcbrent or the best free Brenton Greek), to sit beside the Brenton English already built (1,117 chapter notes, verse ids ^C-V). Report whether its verse division matches the English, book by book.
- B. John Chrysostom, Homilies on the Gospel of John (NPNF series 1, vol. 14), and Origen, Commentary on John (ANF, the "additional volume"), from CCEL or another free copy.
- C. The Digital Corpus of Sanskrit's word analysis for the Śaiva and tantric texts it holds besides the Tantrāloka: at least Tantrasāra, Mṛgendratantra, Spandakārikā, Spandakārikānirṇaya, Bhairavastava, Mahācīnatantra, Mātṛkābhedatantra, Toḍalatantra, Uḍḍāmareśvaratantra; list any other Śaiva or Śākta texts the DCS has.
- D. Plato, complete: every dialogue and letter in the Perseus Burnet Greek, with the Loeb English where it is public domain and Jowett (Gutenberg) where it isn't; list dialogue by dialogue which translation would be used and why.
- E. Thomas Hobbes, De Cive in its English version (Philosophicall Rudiments, 1651), and De Corpore in English (Elements of Philosophy, the First Section, Concerning Body, 1656, e.g. Molesworth's English Works vol. 1).

End with one table: text · source · licence · units · words · notes · MB · hours · cost range · problems. Then a total row. Save the table as tools/SURVEY_ROUND7.md and commit it on a new branch (no pull request needed), and print it in your final message.
````

When it reports, bring the table back to me (or paste it into the phase 4 task) and we'll decide what to build with the rest of the credit. The size column matters for the lag question too.
