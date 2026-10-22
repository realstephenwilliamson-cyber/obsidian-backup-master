---
type: prompt
updated: 2026-10-05
---
# Map new connections

**Use when:** you have written new notes, homilies or essays, or added texts and books, and want the references in them linked and related material pointed out. The first linking pass (5 Oct 2026) linked about 55,000 references; new material isn't linked automatically.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder and give it control of Obsidian. Smart Connections should have finished indexing if you want its suggestions used.

**Who runs it, model, size:** an AI session with the runner; Sonnet for the scripted linking (Part A), Opus or Fable if you want the suggestions of Part B weighed. S for a month's new writing, M for a quarter's.

**Tested script:** [[Reference linker]] (`AI/Prompts/Scripts/Reference linker/`) does Part A's scripture, Zohar, Tantrāloka and Avot linking with the numbering rules below; it linked the converted books on 13 Oct 2026.

````text
Map new connections in my Obsidian vault at C:\Vaults\Obsidian Vault: link the references in new material, and suggest related notes, without touching my wording.

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md, especially "Cross-references", "Hubs and concepts" and "Links, names and scripts"
Confirm with me that no other AI tool is working on the vault.

Scope: notes created or changed since <date of the last pass; ask me, or use 5 Oct 2026>. Ask whether to include Projects/ and Journal/; by default include them for linking but never change their wording.

Part A: reference linking (scripted in the Obsidian console, dry run first).

1. Bible references ("John 3:16", "Gen. 1:1-3", "1 Cor 13:4–7", lists like "Isaiah 7:14; 9:6").
   - Link each to the verse note, following the Guide exactly: Tanakh to the JPS notes with Hebrew numbering, Torah verses to the parashah notes (#^c-v block IDs), New Testament to Texts/New Testament.
   - Christian and general sources (lectionaries, the BCP, my writing, notes, the general library) use English numbering. Map those to the Hebrew verse with the standard table: Psalm superscriptions, Joel 2:28–32 → 3:1–5, Joel 3 → 4, Malachi 4 → 3:19–24, Jonah 1:17 → 2:1, Isaiah 9:1 → 8:23 and 9:2–21 → 9:1–20, the Decalogue in Exod 20 and Deut 5, 1 Chr 12, Neh 7, and the other shifted chapters. Show me the table you use.
   - Zohar, Hasidic texts, Rashi and the Judaica already use Hebrew numbering: link as written.
   - The folder does not decide every case. A reference marked LXX, Septuagint or Vulgate ("LXX Ps 81:6") links to its Texts/Bible/LXX note as written; this is the one case where a canonical book goes to the LXX. Psalm verses cited in the BCP link to the BCP Psalm notes (Texts/BCP 1979/09 The Psalter/), which keep the BCP's own verse numbers (BCP Psalm 74:15 is JPS 74:16). The parashah ranges in the crosswalk tables are in Hebrew numbering: link as written. In the dry run, list every shifted link outside Texts/RCL/ and Texts/BCP 1979/ with its sentence, so I can catch a writer who used the Hebrew numbers.
   - In the Church Fathers, link only New Testament references.
2. Zohar folios ("Zohar 1:15a", lists, ranges like "77a–b") link to the Pritzker note containing that folio, otherwise to the Sefaria folio note. The block ID is #^z<part>-<folio>, where part is the 1, 2 or 3 of the citation (Zohar 2:121a → #^z2-121a), not the Pritzker volume number. "ZḤ 36b" links to volumes 10 and 12 (#^zh-36b).
3. Tantrāloka ("TĀ 15.117", "Tantrāloka 4.122", "T.Ā. 3.67") links to the verse note "Tantraloka NN.NNN".
4. Concepts and hubs: in Notes/, Projects/ and the crosswalks, link the first mention of a concept or hub name (or an alias) in each note.
5. Never link inside headings, code, existing links, properties, or the Bible text notes themselves, and leave Templates/, AI/ and Calendar/ out of the pass. Deuterocanonical books (Sirach, Wisdom, Tobit, Maccabees and the rest) link to their Texts/Bible/LXX notes only if the book is there; never send canonical references to the LXX, except a reference marked LXX, Septuagint or Vulgate (rule 1). A chapter named with its book but no verse (John 8) links to the chapter's first verse, as the earlier passes did (`[[John 08#^8-1|John 8]]`); don't link a verse range without a book name, or verses that don't exist (report those as possible misprints). Inside tables, write the pipe as \|.

Show me the dry run: counts by kind and by folder, 20 random samples, and every case the rules could not decide. After I approve, back up the notes to .work/backup-links-<date>/ and apply. Afterwards, check that the new links resolve, that no block-ID link is broken, and that tables still have the same number of columns.

Part B: suggestions (nothing is written without my approval).

6. For each new or changed note in Notes/, Projects/ and Journal/, list up to 5 related notes you can justify: a shared citation, the same text or verse, the same technical term, or the same author. Give the reason for each. Use Smart Connections' results if its index is available (it lives in .smart-env/), but check each suggestion yourself, and drop any that are only vaguely similar.
7. Propose:
   - "See also" lines between catalog notes that are clearly related (two translations of one text, a text and its commentary, volumes of a series);
   - entries for Texts/Crosswalks/Primary to Secondary Literature Matrix.md, Catalog/Scholars/Scholars.md (a name to profile) and the Texts/Crosswalks notes where new material fits them;
   - concepts that should get an up: hub.
   Present all of this as a checklist. Add only what I tick, in my vault's existing formats.

Report: links added by kind, notes changed, unresolved-link count before and after, and the suggestion checklist. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** open a verse note you cite often (say `John 14` or `Tantraloka 15.117`); its backlinks now list the new places that cite it.
