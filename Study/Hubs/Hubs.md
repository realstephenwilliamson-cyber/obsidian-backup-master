---
type: index
---
# Hubs

Each hub maps one research project: what it is for, its key texts, the writing on it, and the concepts that point up to it. Hubs and concepts together: [[Study]].

```dataview
TABLE WITHOUT ID file.link AS "Hub", file.mtime AS "Last edited"
FROM "Study/Hubs"
WHERE file.path != this.file.path
SORT file.name ASC
```

A new hub: make a note in this folder and fill in what it is for and its key texts. Its concept list fills itself.
