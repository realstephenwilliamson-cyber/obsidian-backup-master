---
type: prompt
updated: 2026-11-09
---
# Import the Mālinīvijayottara (Dyczkowski) as a text

**Use when:** you want Mark Dyczkowski's translation of the *Mālinīvijayottaratantra*, chapters 1–8, in the vault as a primary text in `Texts/`, cited by chapter and verse, like the Tantrāloka. Stephen asked for this on 9 Nov 2026; the three PDFs are in Downloads, *Add to Obsidian*.

**Before you start:** close other AI tools; start the runner (the line is in [[House rules for AI work]] and in project doc 07). An Opus session; size M. Work in stages and check the usage meter between them.

**Copy everything in the box into the task.**

````text
Import Mark Dyczkowski's translation of the Mālinīvijayottaratantra (chapters 1–8) into my Obsidian vault at C:\Vaults\Obsidian Vault as a primary text.

FIRST read in the vault and follow: AI/Prompts/House rules for AI work.md, the "For AIs" section of Vault Guide.md, the top of AI/AI log.md (Open work, next free job number), and AI/Prompts/Add a primary text to Texts.md (its plan, models and checks apply here). Confirm with me that no other AI is working on the vault and that the runner is on (queue a trivial job and read its result).

THE FILES (Downloads\Add to Obsidian; survey of 9 Nov 2026, check it again):
1. "Malinivijayottaratantra chapters 1-5 -- Mark Dyczkowski.pdf" (83 pages, PDF24/Ghostscript, 2024): a general introduction (about pp. 1–14), then chapters 1–5 with the Sanskrit verses in Devanagari and in transliteration and the English translation. The text layer is in broken fonts: in the roman font (ScaGoudy) every character is stored 29 code points too low ("7KH" = "The", the space is \x03); the italic font (ScaGoudyItalic) uses the old CSX-style letters (ä = ā, é = ī, ç = ś, ï = ñ, ù = ḥ, à = ṃ, ò = ḍ, ë = ṇ, ñ = ṣ …: work the table out from the pages, don't assume it); the Devanagari is in a legacy font that does not decode. Decode the roman and the transliteration from the layer (check pages against images); take the Devanagari from a fresh OCR (Tesseract, san) of the page images, or leave it out if the OCR is poor and say so.
2. "Malinivijayottara tantra chapter 6 -- Mark Dyczkowski.pdf" (16 pages; its title says "Malini (Oct–Dec 2023)", made in CorelDRAW): chapter 6, same fonts and encoding as file 1.
3. "Malinivijayottara Tantra chapters 7-8 -- Mark Dyczkowski.pdf" (52 pages, 2025): magazine pages ("Malini", July–September 2024 and other issues; chapter 7 begins "[... continued from Previous Issue]"), two columns, with an OCR text layer of uneven quality; verse references in parentheses ("(6cd-7ab)"). Render the pages and OCR them again if the layer is poor; mark any gap you can't read.
Identify each file from its own pages (title, issue, date); put what you can't establish as status: review with the reason.

WHAT TO BUILD (show me one finished chapter note before doing the rest):
- First ask me which form: one note per verse with Mūla and IAST blocks, like Texts/Tantraloka (the model in "Add a primary text"), or one note per chapter with a block per verse, like Texts/Pseudepigrapha/1 Enoch (9 Nov 2026). Either way: Texts/Malinivijayottara/ with an index note "Malinivijayottara" (the folder note: translator, sources, what each file covers, chapters with links), Dyczkowski's general introduction as its own note, ASCII names (check that none is taken: the library has related material, and Texts/Malinislokavarttika is Abhinavagupta's commentary).
- Each verse with its own block id, ^C-V (a half-verse reference like "6cd-7ab" goes on the verse where it starts; say in the note how the translation's divisions map to verses), with its transliteration (IAST, diacritics kept), the Devanagari if it is good, and the translation; Dyczkowski's notes as footnotes; previous · index · next links at the top and bottom, as in the Tantrāloka and 1 Enoch notes; the printed page as a marker where the source has page numbers.
- A catalog note in Catalog/Trika/ (type: text, files: the index note; the PDFs into Library/Trika/ under ASCII names, with my permission, and listed in files: too). The scripts of the 9 Nov texts import (AI/Prompts/Scripts/Texts import (Nov 2026)/, its README and create-from-bundles.tpl.js) show the bundle-and-runner method.
- Dyczkowski died on 2 February 2025; the translation stops at chapter 8. Say so in the index note.

AFTERWARDS, ask me before doing either: (a) linking the references to the Mālinīvijayottara in the Tantrāloka verse notes, Jayaratha's Viveka and Dyczkowski's Tantrāloka translation (forms like "MV 2.35", "Mālinīvijayottara 2.35") to the new verse blocks, where the verse falls in chapters 1–8; (b) a Texts/Texts.md line and a Vault Guide line.

CHECK: every verse block registered in Obsidian's cache; no unresolved links added; the divine-name rule (house rule 8). Then the AI log entry, Open work, Git commit (the pf808 job in .work/queue/done/ is the latest template), and the session's scratch to .trash.
````
