---
type: index
cssclasses:
  - wide
---
# Religious Studies

Every catalog note tagged with this subject, kept up to date automatically (items marked for deletion are left out). Click a column heading to sort. [[Catalog.base|The library browser]] has more views.

```base
filters:
  and:
    - file.folder.startsWith("Catalog/")
    - subject.contains("Religious-Studies")
    - status != "delete"
formulas:
  Read: files.filter(value.asFile().ext == "md").map(link(value, "Read"))
views:
  - type: table
    name: Religious Studies
    order:
      - formula.Read
      - title
      - author
      - type
      - year
      - status
      - note.print
      - file.tags
    sort:
      - property: file.name
        direction: ASC
    columnSize:
      note.title: 517
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
