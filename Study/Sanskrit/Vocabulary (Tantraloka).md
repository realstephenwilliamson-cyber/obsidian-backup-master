---
type: index
cssclasses:
  - wide
---
# Vocabulary (Tantraloka)

Words you note in the **Words** section of each day's note (`- word:: ātman: the self`) collect here, with the day you met them. Add as many `word::` lines as you like.

```dataview
TABLE WITHOUT ID W AS "Word", file.link AS "Day", tantraloka_day AS "Plan day"
FROM "Journal"
FLATTEN word AS W
WHERE W
SORT W ASC
```

For looking words up: [[Tantraloka words (DCS)]] · [[README - Monier-Williams|Monier-Williams]] · [[Brunner (ed.) - Tantrikabhidhanakosa]]
