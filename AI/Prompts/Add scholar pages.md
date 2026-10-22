---
type: prompt
updated: 2026-10-07
---
# Add scholar pages

**Use when:** names are waiting in [[Scholars]] under *To profile*, after you add a name there, or every few months to recheck the free-source links on existing pages. A batch of about ten names is a good size.

**Before you start:** close other AI tools. In a new Cowork task, connect the vault folder. The task needs web search. Control of Obsidian helps for writing the pages, but isn't required.

**Who runs it, model, size:** an AI session with web search; Sonnet is enough. S–M for ten names: the searching costs more than the writing.

````text
Make scholar pages for my Obsidian vault (C:\Vaults\Obsidian Vault).

FIRST read and follow, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md (Layout, Links, The catalog)
- Catalog/Scholars/Scholars.md (the list of names)
Confirm with me that no other AI tool is working on the vault.

Scope: the first 10 names under "To profile" in Catalog/Scholars/Scholars.md that are not yet links, or the names I give here: <names, or leave as is>.

For each name:
1. Their works in the library: the catalog notes in Catalog/ whose author, editor or translator holds the name in any spelling. Record every spelling the catalog uses; they go in catalog_names.
2. If the scholar has an entry in Texts/Crosswalks/Scholars - library and free sources.md, start from it: move its position line and free-source links to the page, and open each link again. In that note, replace the entry's body with one line: "Now at [[<page>]]." Keep its heading, so links to it still land.
3. Otherwise look them up on the web:
   - their present (or last) position, from an institution's page, their own site or a publisher's author page;
   - where their own work can be read free and legally: an institutional repository or HAL, their own site, an Academia.edu or ResearchGate profile, open-access books or articles from the publisher.
   Never list pirate libraries or third-party uploads of in-copyright books (Internet Archive personal uploads, Scribd, pdfcoffee and the like).
4. Write the page, Catalog/Scholars/<Name in plain ASCII>.md, in the format below. Every statement on it comes from a page you opened, cited with its link. If something can't be found, write "not found" rather than fill it from memory. No adjectives of praise; just what they work on.
5. In Catalog/Scholars/Scholars.md, turn the name into a link to the page, keeping its line otherwise as it is.

Page format (properties, then the body):
---
type: scholar
name: <Name as they publish it, with diacritics>
aliases: [<the ASCII form, and other spellings>]
subjects: [<the vault's subjects of their works in the library: Trika, Hinduism, Sanskrit-Study, Judaica, Christianity, Biblical-Studies, Philosophy, Other>]
affiliation: "<position, institution>"
catalog_names: [<every spelling the catalog uses>]
profiled: <today's date, YYYY-MM-DD>
---
# <Name>

<One or two sentences: position, field, and what they work on, each with its source link.>

## In the library

```dataview
LIST FROM "Catalog"
WHERE any(map(flat(list(author, editor, translator)), (a) => econtains(this.catalog_names, a)))
SORT year ASC
```

## Free online

- [<Site>](<url>): what is there (checked <date>).

## Sources

- <each page used, with its link>

Work in one batch. Before writing anything, show me the list: each name with its one-line description, the number of free-source links, and anything you couldn't settle. Write the pages when I say so, through Obsidian (create, and vault.process for Scholars.md and the old note), with a backup of the two changed notes in .work/backup-scholars-<date>/. Afterwards check that every new page's In the library list shows its works, and that no link is unresolved. At the end, clean up your scratch in .work as the house rules describe (never .work/plan or the backups).
````

**Afterwards:** the pages show in [[Scholars]] under *Profiled*. A hub can list the scholars of its subject with a `dataview` table over `Catalog/Scholars` filtered on `subjects`.
