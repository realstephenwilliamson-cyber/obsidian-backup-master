---
type: rcl-sunday
cycle: "A"
occasion: "Fourth Sunday of Advent"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=a&d=4"
first_reading: "Isaiah 7:10-16"
psalm: "Psalm 80:1-7, 17-19"
psalm_bcp: "Psalm 80:1-7, 16-18"
second_reading: "Romans 1:1-7"
gospel: "Matthew 1:18-25"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-fourth-sunday-of-advent]]"
cssclasses:
  - lectionary
---

# Fourth Sunday of Advent — Year A

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=a&d=4>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Isaiah 07#^7-10\|Isaiah 7:10-16]] |
| Psalm | [[Psalms 080#^80-2\|Psalm 80:1-7]], 17-19 |
| Second Reading | [[Romans 01#^1-1\|Romans 1:1-7]] |
| Gospel | [[Matthew 01#^1-18\|Matthew 1:18-25]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Isaiah 7:10-16

![[Isaiah 07#^7-10]]
![[Isaiah 07#^7-11]]
![[Isaiah 07#^7-12]]
![[Isaiah 07#^7-13]]
![[Isaiah 07#^7-14]]
![[Isaiah 07#^7-15]]
![[Isaiah 07#^7-16]]

### Psalm · Psalm 80:1-7, 17-19

![[Psalms 080#^80-2]]
![[Psalms 080#^80-3]]
![[Psalms 080#^80-4]]
![[Psalms 080#^80-5]]
![[Psalms 080#^80-6]]
![[Psalms 080#^80-7]]
![[Psalms 080#^80-8]]
![[Psalms 080#^80-18]]
![[Psalms 080#^80-19]]
![[Psalms 080#^80-20]]

### Second reading · Romans 1:1-7

![[Romans 01#^1-1]]
![[Romans 01#^1-2]]
![[Romans 01#^1-3]]
![[Romans 01#^1-4]]
![[Romans 01#^1-5]]
![[Romans 01#^1-6]]
![[Romans 01#^1-7]]

### Gospel · Matthew 1:18-25

![[Matthew 01#^1-18]]
![[Matthew 01#^1-19]]
![[Matthew 01#^1-20]]
![[Matthew 01#^1-21]]
![[Matthew 01#^1-22]]
![[Matthew 01#^1-23]]
![[Matthew 01#^1-24]]
![[Matthew 01#^1-25]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
