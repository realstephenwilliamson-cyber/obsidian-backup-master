---
type: rcl-sunday
cycle: "A"
occasion: "Second Sunday of Advent"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=a&d=2"
first_reading: "Isaiah 11:1-10"
psalm: "Psalm 72:1-7, 18-19"
psalm_bcp: "Psalm 72:1-7, 18-19"
second_reading: "Romans 15:4-13"
gospel: "Matthew 3:1-12"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-second-sunday-of-advent]]"
cssclasses:
  - lectionary
---

# Second Sunday of Advent — Year A

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=a&d=2>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Isaiah 11#^11-1\|Isaiah 11:1-10]] |
| Psalm | [[Psalms 072#^72-1\|Psalm 72:1-7]], 18-19 |
| Second Reading | [[Romans 15#^15-4\|Romans 15:4-13]] |
| Gospel | [[Matthew 03#^3-1\|Matthew 3:1-12]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Isaiah 11:1-10

![[Isaiah 11#^11-1]]
![[Isaiah 11#^11-2]]
![[Isaiah 11#^11-3]]
![[Isaiah 11#^11-4]]
![[Isaiah 11#^11-5]]
![[Isaiah 11#^11-6]]
![[Isaiah 11#^11-7]]
![[Isaiah 11#^11-8]]
![[Isaiah 11#^11-9]]
![[Isaiah 11#^11-10]]

### Psalm · Psalm 72:1-7, 18-19

![[Psalms 072#^72-1]]
![[Psalms 072#^72-2]]
![[Psalms 072#^72-3]]
![[Psalms 072#^72-4]]
![[Psalms 072#^72-5]]
![[Psalms 072#^72-6]]
![[Psalms 072#^72-7]]
![[Psalms 072#^72-18]]
![[Psalms 072#^72-19]]

### Second reading · Romans 15:4-13

![[Romans 15#^15-4]]
![[Romans 15#^15-5]]
![[Romans 15#^15-6]]
![[Romans 15#^15-7]]
![[Romans 15#^15-8]]
![[Romans 15#^15-9]]
![[Romans 15#^15-10]]
![[Romans 15#^15-11]]
![[Romans 15#^15-12]]
![[Romans 15#^15-13]]

### Gospel · Matthew 3:1-12

![[Matthew 03#^3-1]]
![[Matthew 03#^3-2]]
![[Matthew 03#^3-3]]
![[Matthew 03#^3-4]]
![[Matthew 03#^3-5]]
![[Matthew 03#^3-6]]
![[Matthew 03#^3-7]]
![[Matthew 03#^3-8]]
![[Matthew 03#^3-9]]
![[Matthew 03#^3-10]]
![[Matthew 03#^3-11]]
![[Matthew 03#^3-12]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
