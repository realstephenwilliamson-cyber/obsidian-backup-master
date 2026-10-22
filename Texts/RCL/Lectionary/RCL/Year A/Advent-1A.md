---
type: rcl-sunday
cycle: "A"
occasion: "First Sunday of Advent"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=a&d=1"
first_reading: "Isaiah 2:1-5"
psalm: "Psalm 122"
psalm_bcp: "Psalm 122"
second_reading: "Romans 13:11-14"
gospel: "Matthew 24:36-44"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-first-sunday-of-advent]]"
cssclasses:
  - lectionary
---

# First Sunday of Advent — Year A

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=a&d=1>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Isaiah 02#^2-1\|Isaiah 2:1-5]] |
| Psalm | Psalm 122 |
| Second Reading | [[Romans 13#^13-11\|Romans 13:11-14]] |
| Gospel | [[Matthew 24#^24-36\|Matthew 24:36-44]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Isaiah 2:1-5

![[Isaiah 02#^2-1]]
![[Isaiah 02#^2-2]]
![[Isaiah 02#^2-3]]
![[Isaiah 02#^2-4]]
![[Isaiah 02#^2-5]]

### Psalm · Psalm 122

![[Psalms 122#Chapter 122]]

### Second reading · Romans 13:11-14

![[Romans 13#^13-11]]
![[Romans 13#^13-12]]
![[Romans 13#^13-13]]
![[Romans 13#^13-14]]

### Gospel · Matthew 24:36-44

![[Matthew 24#^24-36]]
![[Matthew 24#^24-37]]
![[Matthew 24#^24-38]]
![[Matthew 24#^24-39]]
![[Matthew 24#^24-40]]
![[Matthew 24#^24-41]]
![[Matthew 24#^24-42]]
![[Matthew 24#^24-43]]
![[Matthew 24#^24-44]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
