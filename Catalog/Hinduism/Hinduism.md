---
type: index
cssclasses:
  - wide
---
# Hinduism

*See also: [[Trika|Trika]], [[Sanskrit-Study|Sanskrit Study]].*

Every catalog note tagged with this subject, kept up to date automatically (items marked for deletion are left out). Click a column heading to sort. [[Catalog.base|The library browser]] has more views.

```base
filters:
  and:
    - file.folder.startsWith("Catalog/")
    - subject.contains("Hinduism")
    - status != "delete"
views:
  - type: table
    name: Hinduism
    order:
      - file.name
      - author
    sort:
      - property: file.name
        direction: ASC
    columnSize:
      file.name: 590
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
