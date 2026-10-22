---
type: rcl-sunday
cycle: "B"
occasion: "Sixth Sunday of Easter"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=s&d=48"
first_reading: "Acts 10:44-48"
psalm: "Psalm 98"
psalm_bcp: "Psalm 98"
second_reading: "1 John 5:1-6"
gospel: "John 15:9-17"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-sixth-sunday-of-easter]]"
cssclasses:
  - lectionary
---

# Sixth Sunday of Easter — Year B

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=s&d=48>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Acts 10#^10-44\|Acts 10:44-48]] |
| Psalm | Psalm 98 |
| Second Reading | [[1 John 05#^5-1\|1 John 5:1-6]] |
| Gospel | [[John 15#^15-9\|John 15:9-17]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Acts 10:44-48

![[Acts 10#^10-44]]
![[Acts 10#^10-45]]
![[Acts 10#^10-46]]
![[Acts 10#^10-47]]
![[Acts 10#^10-48]]

### Psalm · Psalm 98

![[Psalms 098#Chapter 98]]

### Second reading · 1 John 5:1-6

![[1 John 05#^5-1]]
![[1 John 05#^5-2]]
![[1 John 05#^5-3]]
![[1 John 05#^5-4]]
![[1 John 05#^5-5]]
![[1 John 05#^5-6]]

### Gospel · John 15:9-17

![[John 15#^15-9]]
![[John 15#^15-10]]
![[John 15#^15-11]]
![[John 15#^15-12]]
![[John 15#^15-13]]
![[John 15#^15-14]]
![[John 15#^15-15]]
![[John 15#^15-16]]
![[John 15#^15-17]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
