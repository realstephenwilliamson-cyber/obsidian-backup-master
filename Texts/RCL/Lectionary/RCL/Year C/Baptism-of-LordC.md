---
type: rcl-sunday
cycle: "C"
occasion: "Baptism of the Lord"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=e&d=13"
first_reading: "Isaiah 43:1-7"
psalm: "Psalm 29"
psalm_bcp: "Psalm 29"
second_reading: "Acts 8:14-17"
gospel: "Luke 3:15-17, 21-22"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-first-sunday-after-the-epiphany-the-baptism-of-our-lord]]"
cssclasses:
  - lectionary
---

# Baptism of the Lord — Year C

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=e&d=13>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Isaiah 43#^43-1\|Isaiah 43:1-7]] |
| Psalm | Psalm 29 |
| Second Reading | [[Acts 08#^8-14\|Acts 8:14-17]] |
| Gospel | [[Luke 03#^3-15\|Luke 3:15-17]], 21-22 |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Isaiah 43:1-7

![[Isaiah 43#^43-1]]
![[Isaiah 43#^43-2]]
![[Isaiah 43#^43-3]]
![[Isaiah 43#^43-4]]
![[Isaiah 43#^43-5]]
![[Isaiah 43#^43-6]]
![[Isaiah 43#^43-7]]

### Psalm · Psalm 29

![[Psalms 029#Chapter 29]]

### Second reading · Acts 8:14-17

![[Acts 08#^8-14]]
![[Acts 08#^8-15]]
![[Acts 08#^8-16]]
![[Acts 08#^8-17]]

### Gospel · Luke 3:15-17, 21-22

![[Luke 03#^3-15]]
![[Luke 03#^3-16]]
![[Luke 03#^3-17]]
![[Luke 03#^3-21]]
![[Luke 03#^3-22]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
