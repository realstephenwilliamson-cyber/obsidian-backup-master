---
type: prompt
updated: 2026-10-05
---
# Add a primary text to Texts

**Use when:** you want a whole primary text in the vault as one note per verse, chapter or section, the way the Tantrāloka, Tanakh, New Testament, LXX, Torah with Rashi, Zohar, Chasidut, Church Fathers, Mārkaṇḍeya Purāṇa and Devī Māhātmya are. For example: another Sanskrit work from the Muktabodha e-texts, a Hasidic book from Sefaria, or a Father.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder (and the source file's folder). The work is scripted, so give it control of Obsidian too. Have a fresh copy of the vault folder.

**Who runs it, model, size:** an AI session with the runner; Opus or Fable for a text whose structure (verses, chapters, commentary layers) is new to the vault, Sonnet for one shaped like those already done. M per text.

````text
Add a primary text to my Obsidian vault (C:\Vaults\Obsidian Vault) under Texts/, in the same form as the texts already there.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md → "A primary text in Texts/", Cross-references, Links, Callouts
- Two models (open a few notes of each):
  Texts/Tantraloka/ (verse notes with ## Mūla, ^mula/^iast blocks, translation callouts, Viveka, previous · chapter · next links)
  and the closest model for the new text (Texts/Chasidut/, Texts/Fathers/, Texts/Markandeya Purana/, Texts/Bible/Torah/).
Confirm with me that no other AI tool is working on the vault.

The text: <name, source file or website, edition>.

1. Source and licence: name the edition and copy its licence from the source itself. For a Muktabodha e-text, take it from the header of that e-text (the Tantrāloka notes say CC BY-NC 4.0 with a credit line); Sefaria gives a licence for each text and version. Ask me before downloading anything. If a site refuses automated access, give me the link instead of working around it.
2. Plan:
   - the folder Texts/<Work>/;
   - the unit (verse, chapter, parashah or section) and the naming "<Work> NN.NNN" (ASCII, zero-padded);
   - the properties (type: "text", work, author, chapter and verse as numbers, edition, license, aliases with diacritics such as "TĀ 31.12");
   - a chapter note per chapter, plus a work note;
   - navigation links on each unit.
   Show me three sample notes before generating the rest.
3. Generate the notes with a script in your workspace, writing new files only (they can be copied in from outside Obsidian). Keep the source text exactly; Devanagari, IAST and Hebrew are fine inside notes. Don't add translations you made up; translations come only from a named source.
4. Link it in:
   - the work note links the chapter notes;
   - add the text to the Vault Guide's Layout row for Texts/ and to any hub it belongs to (ask);
   - if Library has translations of it, add "See also" lines to those catalog notes;
   - offer to run AI/Prompts/Map new connections.md so that existing references to this text become links.
5. Check:
   - unit count against the source's own count;
   - no duplicate names (ambiguous links) with existing notes;
   - every navigation link resolves;
   - three units compared word for word with the source;
   - the vault's unresolved-link count unchanged.

Report the folder, the number of notes, the checks, and what was linked. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** open the work note and step through a few units with the navigation links.
