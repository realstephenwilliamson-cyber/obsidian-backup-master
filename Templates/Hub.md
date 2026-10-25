<%* /* ================================================================================================================
HUB TEMPLATE — read me (for Stephen; 21 Oct 2026)
What it makes: a hub note in Study/Hubs (type hub, status active, the Home page's style): a thesis box, Core Library, the
  Conceptual Matrix, Active Drafting, and three Dataview lists — the concepts whose up: names this hub, recent catalog items
  on the hub's subjects, and the scholars on those subjects. The feeds of question::, claim::, connects:: and cites:: lines
  on the existing hubs come from blocks that call the view Templates/Views/hub-fields; this template does not add them —
  copy such a block from an existing hub (Hub - Tantraloka, under Dynamic Feeds) if a new hub should have them.
When it runs: Templater fills a NEW, EMPTY note in Study/Hubs. Opening this file does nothing. A note named "Hubs" would be
  the folder's own note, so the guard below gives it a short index instead.
What you may edit: everything after the tag is plain Markdown and three Dataview queries — the placeholder texts, the
  headings, and the subjects in the WHERE lines ("Subject 1", "Subject 2").
Don't rename: the properties type (hub) and status (the Study index reads them), and the up: convention — a concept names
  the hub in its up property, which is how the first list here finds it.
To test an edit: make a new note in Study/Hubs, look, delete it through Obsidian. The previous version of this file is in
  .work/backup-orient-2026-10-21/Templates/ and in Sync's version history.
================================================================================================================ */
/* Guard (13 Oct 2026, D8): a note named after its own folder is that folder's folder note, so it gets a short folder-note body (a list of the folder's notes) instead of this template. */ if (tp.file.title === tp.file.folder(false)) { tR += "---\ntype: index\n---\n# " + tp.file.title + "\n\n```dataview\nLIST FROM \"" + tp.file.folder(true) + "\" WHERE file.path != this.file.path SORT file.name ASC\n```\n"; } else { -%>
---
cssclasses:
  - home
type: hub
status: active
---
# Hub: [Project or Synthesis Name]

> [!abstract] Thesis / Overview
> A short, 2-3 sentence anchor describing the exact scope of this project. What problem is this hub trying to solve? What two disparate ideas is it trying to connect?

## Core Library
*Primary and secondary source texts anchoring this research.*
- **Primary:** *Link to Text 1* · *Link to Text 2*
- **Secondary:** *Link to Commentary* · *Link to Scholar*

---

## The Conceptual Matrix
*Atomic ideas and arguments. Gray links are "phantom" concepts that need to be written; blue links are populated.*

> [!navigation]+ Foundational Concepts
> - *Concept 1*
> - *Concept 2 (Phantom)*
> - *Concept 3 (Phantom)*

> [!navigation]+ Synthesis & Arguments
> - *Argument A connecting Concept 1 and 2*
> - *Drafting Idea B*

---

## Active Drafting
*Homilies, papers, or essays flowing from this hub.*
- *Projects/Homilies/YYYY-MM-DD Sunday*
- *Projects/Term Paper - Outline*

---

## Dynamic Feeds (Dataview)

### Populated Concept Notes
*Automatically pulls any atomic note in the vault that points up to this Hub.*
```dataview
TABLE status, file.mtime as "Last Worked"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
SORT file.mtime DESC
```

### Recent Literature
*Automatically pulls recent catalog items tagged with relevant subjects.*
```dataview
TABLE author, year
FROM "Catalog"
WHERE contains(subject, "Subject 1") OR contains(subject, "Subject 2")
SORT file.ctime DESC
LIMIT 5
```

### Scholars in the library
*Scholars with a page in Catalog/Scholars whose works in the library are on this hub's subjects. Put the subjects in the WHERE line.*
```dataview
TABLE WITHOUT ID file.link AS "Scholar", affiliation AS "Position", subjects AS "Subjects"
FROM "Catalog/Scholars"
WHERE type = "scholar" AND (econtains(subjects, "Subject 1") OR econtains(subjects, "Subject 2"))
SORT file.name ASC
```
<%* } -%>
