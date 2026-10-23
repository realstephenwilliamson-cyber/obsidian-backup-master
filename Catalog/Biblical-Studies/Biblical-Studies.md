---
type: index
cssclasses:
  - wide
---
# Biblical Studies

*See also: [[Judaica|Judaica]], [[Christianity|Christianity]].*

Every catalog note tagged with this subject, kept up to date automatically (items marked for deletion are left out). Click a column heading to sort. [[Catalog.base|The library browser]] has more views.

```base
filters:
  and:
    - file.folder.startsWith("Catalog/")
    - subject.contains("Biblical-Studies")
    - status != "delete"
formulas:
  Read: files.filter(value.asFile().ext == "md").map(link(value, "Read"))
views:
  - type: table
    name: Biblical Studies
    order:
      - formula.Read
      - file.name
      - author
      - type
      - year
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
      - formula.Read
      - file.name
      - author
      - type
      - year
    sort:
      - property: file.name
        direction: ASC
```
