---
type: index
cssclasses:
  - wide
---
# Philosophy

*See also: [[Judaica|Judaica]], [[Christianity|Christianity]].*

Every catalog note tagged with this subject, kept up to date automatically (items marked for deletion are left out). Click a column heading to sort. [[Catalog.base|The library browser]] has more views.

```base
filters:
  and:
    - file.folder.startsWith("Catalog/")
    - subject.contains("Philosophy")
    - status != "delete"
formulas:
  Read: files.filter(value.asFile().ext == "md").map(link(value, "Read"))
views:
  - type: table
    name: Philosophy
    order:
      - formula.Read
      - title
      - author
      - type
      - year
      - note.print
    sort:
      - property: file.name
        direction: ASC
    columnSize:
      formula.Read: 73
      note.title: 392
      note.author: 173
      note.type: 90
      note.year: 62
  - type: table
    name: Needs review
    filters:
      and:
        - status == "review"
    order:
      - formula.Read
      - file.name
      - author
      - type
      - year
    sort:
      - property: file.name
        direction: ASC

```
