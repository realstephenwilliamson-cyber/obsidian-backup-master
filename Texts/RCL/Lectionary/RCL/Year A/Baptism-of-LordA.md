---
type: rcl-sunday
cycle: "A"
occasion: "Baptism of the Lord"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=e&d=13"
first_reading: "Isaiah 42:1-9"
psalm: "Psalm 29"
psalm_bcp: "Psalm 29"
second_reading: "Acts 10:34-43"
gospel: "Matthew 3:13-17"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-first-sunday-after-the-epiphany-the-baptism-of-our-lord]]"
cssclasses:
  - lectionary
---

# Baptism of the Lord — Year A

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=e&d=13>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Isaiah 42#^42-1\|Isaiah 42:1-9]] |
| Psalm | Psalm 29 |
| Second Reading | [[Acts 10#^10-34\|Acts 10:34-43]] |
| Gospel | [[Matthew 03#^3-13\|Matthew 3:13-17]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Isaiah 42:1-9

![[Isaiah 42#^42-1]]
![[Isaiah 42#^42-2]]
![[Isaiah 42#^42-3]]
![[Isaiah 42#^42-4]]
![[Isaiah 42#^42-5]]
![[Isaiah 42#^42-6]]
![[Isaiah 42#^42-7]]
![[Isaiah 42#^42-8]]
![[Isaiah 42#^42-9]]

### Psalm · Psalm 29

![[Psalms 029#Chapter 29]]

### Second reading · Acts 10:34-43

![[Acts 10#^10-34]]
![[Acts 10#^10-35]]
![[Acts 10#^10-36]]
![[Acts 10#^10-37]]
![[Acts 10#^10-38]]
![[Acts 10#^10-39]]
![[Acts 10#^10-40]]
![[Acts 10#^10-41]]
![[Acts 10#^10-42]]
![[Acts 10#^10-43]]

### Gospel · Matthew 3:13-17

![[Matthew 03#^3-13]]
![[Matthew 03#^3-14]]
![[Matthew 03#^3-15]]
![[Matthew 03#^3-16]]
![[Matthew 03#^3-17]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
