---
type: index
---
# Notes

The inbox. New notes land here; when one finds its place, move it to Study, Projects or the Catalog.

## Newest

```dataview
TABLE WITHOUT ID file.link AS "Note", file.folder AS "Folder", file.ctime AS "Created"
FROM "Notes"
WHERE file.path != this.file.path
SORT file.ctime DESC
LIMIT 25
```

## Not linked yet

Notes here with no links in or out:

```dataview
LIST
FROM "Notes"
WHERE file.path != this.file.path AND length(file.inlinks) = 0 AND length(file.outlinks) = 0
SORT file.ctime DESC
```
