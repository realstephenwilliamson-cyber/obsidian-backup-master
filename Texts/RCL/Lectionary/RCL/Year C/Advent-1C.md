---
type: rcl-sunday
cycle: "C"
occasion: "First Sunday of Advent"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=a&d=1"
first_reading: "Jeremiah 33:14-16"
psalm: "Psalm 25:1-10"
psalm_bcp: "Psalm 25:1-9"
second_reading: "1 Thessalonians 3:9-13"
gospel: "Luke 21:25-36"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-first-sunday-of-advent]]"
cssclasses:
  - lectionary
---

# First Sunday of Advent — Year C

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=a&d=1>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Jeremiah 33#^33-14\|Jeremiah 33:14-16]] |
| Psalm | [[Psalms 025#^25-1\|Psalm 25:1-10]] |
| Second Reading | [[1 Thessalonians 03#^3-9\|1 Thessalonians 3:9-13]] |
| Gospel | [[Luke 21#^21-25\|Luke 21:25-36]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Jeremiah 33:14-16

![[Jeremiah 33#^33-14]]
![[Jeremiah 33#^33-15]]
![[Jeremiah 33#^33-16]]

### Psalm · Psalm 25:1-10

![[Psalms 025#^25-1]]
![[Psalms 025#^25-2]]
![[Psalms 025#^25-3]]
![[Psalms 025#^25-4]]
![[Psalms 025#^25-5]]
![[Psalms 025#^25-6]]
![[Psalms 025#^25-7]]
![[Psalms 025#^25-8]]
![[Psalms 025#^25-9]]
![[Psalms 025#^25-10]]

### Second reading · 1 Thessalonians 3:9-13

![[1 Thessalonians 03#^3-9]]
![[1 Thessalonians 03#^3-10]]
![[1 Thessalonians 03#^3-11]]
![[1 Thessalonians 03#^3-12]]
![[1 Thessalonians 03#^3-13]]

### Gospel · Luke 21:25-36

![[Luke 21#^21-25]]
![[Luke 21#^21-26]]
![[Luke 21#^21-27]]
![[Luke 21#^21-28]]
![[Luke 21#^21-29]]
![[Luke 21#^21-30]]
![[Luke 21#^21-31]]
![[Luke 21#^21-32]]
![[Luke 21#^21-33]]
![[Luke 21#^21-34]]
![[Luke 21#^21-35]]
![[Luke 21#^21-36]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
