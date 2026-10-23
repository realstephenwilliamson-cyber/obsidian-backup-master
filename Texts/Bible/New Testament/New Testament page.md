---
type: parallel
ref: John 14:1
translation: nrsvue
cssclasses:
  - wide
---
# New Testament page

One section of the [[New Testament]] (a BSB section heading to the next) laid out like a page of a glossed Bible: the verses in the middle, in the BSB or the NRSVue, with the translators' notes and, if you tick *Greek*, the SBLGNT line under each verse with every word linked to its note in the [[Greek NT Lexicon (MorphGNT)|Greek NT lexicon]]; beside them the notes of the [[Jewish Annotated New Testament]]; in the margins the [[Synoptic parallels]] (with a button that opens the row in the [[Synoptic reader]]), the Scripture and the rabbinic texts the JANT notes cite, the Fathers and Aquinas quoted where they cite these verses, the books in the Library that cite them, every other note that links them, and your own `question::`, `claim::` and `connects::` lines. Type a verse in the box (*Matthew 5:3*, *Mt 5*, *1 Cor 13:4*) or use the arrows; the place, the translation and the Greek are kept in this note's properties, and when *ref* is empty the page opens at Matthew 5:1. On a narrow screen the columns stack under the text.

```dataviewjs
await dv.view("Templates/Views/nt-page")
```
