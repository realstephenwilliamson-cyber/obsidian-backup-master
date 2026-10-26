---
type: parallel
ref: ""
span: 8
cssclasses:
  - wide
---
# Torah View

A passage of the [[Torah]] (or of the Prophets and Writings, [[Tanakh]]) laid out like a page of a Mikraot Gedolot: the verses in the JPS translation in the middle, with the translators' notes and the *Compare* links (NRSVue, LXX, Douay-Rheims); Rashi beside them; in the margins the daf sides of the Talmud whose *Torah Or* names these verses (one line quoted), the *Mishneh Torah* and *Kitzur* chapters that cite them, the Hasidic texts and the Zohar quoted where they cite them, every other note that links them, the haftarah (or, on a page of the Prophets, the parashot that read it as haftarah), the *Guide for the Perplexed*, and your own `question::`, `claim::` and `connects::` lines. Type a verse (*Genesis 1:1*, *Gen 1:1-12*, *Isaiah 53:4*, *Ps 23*) or a parashah (*Noach*) in the box, or use the arrows; the place and the number of verses are kept in this note's properties, and when *ref* is empty the page shows the coming Shabbat's portion. On a narrow screen the columns stack under the text.

```dataviewjs
await dv.view("Templates/Views/torah-page")
```
