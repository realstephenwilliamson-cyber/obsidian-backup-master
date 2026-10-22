---
type: index
---
# Concepts

Single ideas in your own words, one per note, each pointing up to its hubs in `up`. By hub: [[Study]].

```dataview
TABLE WITHOUT ID file.link AS "Concept", up AS "Hubs", file.mtime AS "Last edited"
FROM "Study/Concepts"
WHERE file.path != this.file.path
SORT file.name ASC
```
