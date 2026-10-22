<%* /* ================================================================================================================
CONCEPT TEMPLATE — read me (for Stephen; 21 Oct 2026)
What it makes: a concept note in Study/Concepts: the properties (type concept, up, aliases, tags, status draft, created), the
  title, "In a sentence", Notes (claim:: lines), Where it comes from (cites::), Open (question::), Related.
When it runs: Templater fills a NEW, EMPTY note in Study/Concepts — made in the file explorer, or by following a link to a
  concept that does not exist yet. Opening this file does nothing. A note named "Concepts" would be the folder's own note,
  so the guard below gives it a short index instead.
What you may edit: everything after the tag is the note's plain Markdown — the headings, the prompt lines, their order.
  The lines "- claim::", "- cites::" and "- question::" are the fields the hubs collect (Vault Guide, Fields): keep their spelling.
Don't rename: the properties type (concept), up (the hubs this concept belongs to) and status — the Study index and the hubs'
  lists read them.
To test an edit: make a new note in Study/Concepts, look, delete it through Obsidian. The previous version of this file is in
  .work/backup-orient-2026-10-21/Templates/ and in Sync's version history.
================================================================================================================ */
/* Guard (13 Oct 2026, D8): a note named after its own folder is that folder's folder note, so it gets a short folder-note body (a list of the folder's notes) instead of this template. */ if (tp.file.title === tp.file.folder(false)) { tR += "---\ntype: index\n---\n# " + tp.file.title + "\n\n```dataview\nLIST FROM \"" + tp.file.folder(true) + "\" WHERE file.path != this.file.path SORT file.name ASC\n```\n"; } else { -%>
---
type: concept
up: []
aliases: []
tags: []
status: draft
created: <% tp.date.now("YYYY-MM-DD") %>
---
# <% tp.file.title %>

**In a sentence:** 

## Notes

- claim:: 

## Where it comes from

- cites:: 

## Open

- question:: 

## Related

- 
<%* } -%>
