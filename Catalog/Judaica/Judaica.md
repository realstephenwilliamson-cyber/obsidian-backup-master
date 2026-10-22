---
type: index
cssclasses:
  - wide
---
# Judaica

*See also: [[Christianity|Christianity]], [[Biblical-Studies|Biblical Studies]], [[Philosophy|Philosophy]].*

Every catalog note tagged with this subject, kept up to date automatically (items marked for deletion are left out). Click a column heading to sort. [[Catalog.base|The library browser]] has more views.

```base
filters:
  and:
    - file.folder.startsWith("Catalog/")
    - subject.contains("Judaica")
    - status != "delete"
views:
  - type: table
    name: Judaica
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
