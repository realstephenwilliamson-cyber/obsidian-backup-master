---
type: prompt
date: 2026-10-07
---
# Cloud session prompt: phase 7's free texts

This job uses the Claude Code cloud credit (it expires on 4 Nov 2026). It builds the three free texts of [[AI/Archive/Claude outputs/7 New texts and gaps|phase 7]] (Plato's *Phaedrus*, Pirkei Avot and the complete 1651 *Leviathan*) in your GitHub repository, the same way rounds 1–5 built the Sefaria, New Testament, LXX and DCS texts (see [[Cloud build reports]]). It never touches the vault. Phase 7 imports the result.

## How to start it (you, about 5 minutes)

1. In a browser, open **claude.ai/code** and sign in (or open Claude Code in the Claude desktop app and choose a cloud session).
2. Pick the repository that holds the earlier build scripts (`tools/build_texts.py`, `tools/build_nt.py` …). If you're not sure which of the two it is, open each on github.com and look for the `tools/` folder.
3. **Network:** if the environment asks, or offers a setting for network access, allow the sites in step 1 of the prompt (or choose full access). If a download is refused, the session will stop and name the site; allow it, then type `Continue`.
4. Paste everything in the box below and start. It works on its own and ends by opening a pull request.
5. When it reports, read its report and merge the pull request on github.com if you're content (rounds 1–2 were merged the same way).

You can start now: it only works in GitHub, so it doesn't break the one-AI-on-the-vault rule. Don't paste it into a Cowork task, since Cowork doesn't use the credit.

````text
Build three public-domain or openly licensed texts as Obsidian Markdown in this repository, the same way the earlier rounds did. Work only in this repository: there is no vault here, and nothing outside GitHub is to be changed.

FIRST read this repository: the build scripts in tools/ and the reports of rounds 1–5 (NT_BUILD_REPORT.md, SKIPPED.md and any other *REPORT*.md). Reuse their conventions and helpers: YAML front matter, ASCII file names (no diacritics and none of [ ] # ^ | : * ? " < > \ /), block ids for anchors, previous · index · next navigation links, the checks (counts, links, file names, path length under 150 characters). Write a new script tools/build_round6.py; a rebuild must give identical output. Cache downloads in .cache/ (git-ignored).

Rules:
- Text only from the named sources, copied exactly. Don't translate, summarise or fill gaps. Where a source has a gap or an error, keep it and say so in the report.
- Record each source's URL, edition, translator, date and licence, copied from the source itself (TEI header, Sefaria version metadata, Gutenberg header). If a value isn't in the source, leave it empty and say so; don't take it from memory.
- The divine name: keep it exactly where a source writes it; never add it to file names, headings, aliases, link labels or front matter. Count occurrences per work in the report.
- If a site refuses automated access or rate-limits you, stop and report which site and URL; don't work around it.

1. Sources, preferring the GitHub copies, which this environment can usually reach:
   - Plato, Phaedrus: the Perseus Digital Library TEI in github.com/PerseusDL/canonical-greekLit (tlg0059.tlg012: Burnet's Greek and the English translation by H. N. Fowler from the Loeb Library), or perseus.tufts.edu. Take the translation's date from its TEI header.
   - Pirkei Avot: from Sefaria (github.com/Sefaria/Sefaria-Export, or sefaria.org's API). List the English versions with their licences; use one whose licence is CC0, CC-BY or public domain (state which, and why that one), and the Hebrew text if its licence allows (state it).
   - Thomas Hobbes, Leviathan (1651), complete: Project Gutenberg (gutenberg.org ebook 3207, or a GitHub mirror of it). Copy the Gutenberg header's statement of what edition it was made from.
2. Layout (folders as they will sit in the vault):
   - Texts/Plato/Phaedrus/: a work note "Phaedrus (Plato)" and one note per Stephanus page, named "Phaedrus 227" … "Phaedrus 279", English (Fowler) with the Greek beside or below if you include it, and a block id at each Stephanus section: ^227a, ^227b … so a link reads [[Phaedrus 274#^274c|Phaedrus 274c]]. Properties: type: text, work: Phaedrus, author: Plato, translator, stephanus: 274 (a number), edition, license.
   - Texts/Pirkei Avot/: a work note "Pirkei Avot" and one note per chapter, "Pirkei Avot 01" … "Pirkei Avot 06", each mishnah with a block id ^1-1, ^1-2 … (chapter-mishnah); English, with the Hebrew under each mishnah if licensed. Properties: type: text, work: Pirkei Avot, chapter (a number), translation, license.
   - Texts/Hobbes/Leviathan (1651)/: a work note "Leviathan (1651)" and one note per chapter, "Leviathan 1651 NN - <chapter title>" (two digits; separate notes for the dedication, the introduction, the parts' openings if they have text, and "A Review and Conclusion"). Keep Hobbes's spelling, italics and marginal notes as the source has them (marginal notes as footnotes or as a quote line beside the paragraph, and say which). Give each paragraph a block id ^p1, ^p2 … within its chapter. Properties: type: text, work: Leviathan (1651), author: Thomas Hobbes, chapter (a number, 0 for front matter), part, edition, license. The vault already has Jonathan Bennett's adaptation of Leviathan, so every note name here contains "1651", to keep links unambiguous.
   - Library/Catalog/Philosophy/ and Library/Catalog/Judaica/: a draft catalog note for each work in this form (fill only what the source states): title, subtitle, author [ ], editor [ ], translator [ ], year, publisher, series, volume, container, subject [Philosophy] or [Judaica], type: book, language [ ], pages (empty), text: searchable, status: review, physical_copy: false, files: ["[[<the work note>]]"], aliases [ ]. Below the properties: a "# Title" line and one sentence on the source and licence with the URL.
3. Check and report:
   - counts against the source's own (Stephanus sections and pages, mishnayot per chapter, Leviathan chapters 1–47 plus front and back matter, paragraphs);
   - every block id unique in its note, every navigation and catalog link resolving inside the build;
   - three units of each work compared word for word with the source, quoted in the report;
   - write tools/ROUND6_REPORT.md in the style of the earlier reports (sources, licences, counts, divine-name counts, what didn't fit the plan), and add a "Round 6" section to the combined build report if the repository keeps one.
4. Commit on a new branch, push, and open a pull request titled "Round 6 - Phaedrus, Pirkei Avot, Leviathan (1651)". Don't merge it. End with a summary: the folders, the note counts, the checks, anything skipped and why.
````

## What phase 7 then does

The Cowork task can't reach GitHub, so it will ask you to download the repository (on github.com: *Code* → *Download ZIP*, then unzip it in Downloads). It then checks the names against the vault, copies the notes in with a script, adds the catalog notes, and relinks the hub links that phase 3 marked "(not in the vault yet)", such as the Second Domestication hub's Phaedrus link to the Theuth and Thamus passage (274c–275b).
