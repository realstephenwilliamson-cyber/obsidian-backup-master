<%*
// ================================================================================================================
// CATALOG ITEM TEMPLATE — read me (for Stephen; 21 Oct 2026)
// What it makes: the property block of a catalog note (Vault Guide, The catalog) and the title line, with cursor stops at
//   the title, the subject, the file link and the heading (Templater's "Jump to next cursor location" moves between them).
// When it runs: make the note yourself in Catalog/<Subject>/, named "Author - Short title", then run "Templater: Insert
//   template" → Catalog Item; no folder applies it on its own. On the phone, "Add a book you have on paper" on Home (mobile)
//   makes a catalog note without this template. Opening this file does nothing.
// What you may edit: the default values (type book, language English, text searchable, print false; status stays empty).
// Don't rename the properties or change the shape of their values — subject, type, text, status, print, files,
//   pages, year keep the forms in the Guide's block: the catalog Bases and the subject indexes sort and filter on them.
// To test an edit: insert the template into a scratch note in Notes/, look, delete it through Obsidian. The previous version
//   of this file is in .work/backup-orient-2026-10-21/Templates/ and in Sync's version history.
// ================================================================================================================
-%>
---
title: "<% tp.file.cursor(1) %>"
subtitle: ""
author: []
editor: []
translator: []
year: 
publisher: ""
series: ""
volume: ""
container: ""
subject:
  - <% tp.file.cursor(2) %>
type: book
language:
  - English
pages: 
text: searchable
status:
print: false
files:
  - "[[<% tp.file.cursor(3) %>]]"
aliases: []
---

# <% tp.file.cursor(4) %>
