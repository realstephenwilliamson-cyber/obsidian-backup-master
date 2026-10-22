---
type: rcl-sunday
cycle: "B"
occasion: "Second Sunday of Easter"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=s&d=44"
first_reading: "Acts 4:32-35"
psalm: "Psalm 133"
psalm_bcp: "Psalm 133"
second_reading: "1 John 1:1-2:2"
gospel: "John 20:19-31"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-second-sunday-of-easter]]"
cssclasses:
  - lectionary
---

# Second Sunday of Easter — Year B

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=s&d=44>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Acts 04#^4-32\|Acts 4:32-35]] |
| Psalm | Psalm 133 |
| Second Reading | [[1 John 01#^1-1\|1 John 1:1-2:2]] |
| Gospel | [[John 20#^20-19\|John 20:19-31]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Acts 4:32-35

![[Acts 04#^4-32]]
![[Acts 04#^4-33]]
![[Acts 04#^4-34]]
![[Acts 04#^4-35]]

### Psalm · Psalm 133

![[Psalms 133#Chapter 133]]

### Second reading · 1 John 1:1-2:2

![[1 John 01#^1-1]]
![[1 John 01#^1-2]]
![[1 John 01#^1-3]]
![[1 John 01#^1-4]]
![[1 John 01#^1-5]]
![[1 John 01#^1-6]]
![[1 John 01#^1-7]]
![[1 John 01#^1-8]]
![[1 John 01#^1-9]]
![[1 John 01#^1-10]]
![[1 John 02#^2-1]]
![[1 John 02#^2-2]]

### Gospel · John 20:19-31

![[John 20#^20-19]]
![[John 20#^20-20]]
![[John 20#^20-21]]
![[John 20#^20-22]]
![[John 20#^20-23]]
![[John 20#^20-24]]
![[John 20#^20-25]]
![[John 20#^20-26]]
![[John 20#^20-27]]
![[John 20#^20-28]]
![[John 20#^20-29]]
![[John 20#^20-30]]
![[John 20#^20-31]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
