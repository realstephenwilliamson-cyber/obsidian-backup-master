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
views:
  - type: table
    name: Philosophy
    order:
      - file.name
      - author
      - year
      - type
      - text
      - status
    sort:
      - property: file.name
        direction: ASC
    columnSize:
      file.name: 380
  - type: table
    name: Needs review
    filters:
      and:
        - status == "review"
    order:
      - file.name
      - author
      - year
    sort:
      - property: file.name
        direction: ASC

```
