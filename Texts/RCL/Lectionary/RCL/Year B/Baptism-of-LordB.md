---
type: rcl-sunday
cycle: "B"
occasion: "Baptism of the Lord"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=e&d=13"
first_reading: "Genesis 1:1-5"
psalm: "Psalm 29"
psalm_bcp: "Psalm 29"
second_reading: "Acts 19:1-7"
gospel: "Mark 1:4-11"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-first-sunday-after-the-epiphany-the-baptism-of-our-lord]]"
cssclasses:
  - lectionary
---

# Baptism of the Lord — Year B

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=e&d=13>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Torah 01 - Bereshit#^1-1\|Genesis 1:1-5]] |
| Psalm | Psalm 29 |
| Second Reading | [[Acts 19#^19-1\|Acts 19:1-7]] |
| Gospel | [[Mark 01#^1-4\|Mark 1:4-11]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Genesis 1:1-5

![[Torah 01 - Bereshit#^1-1]]
![[Torah 01 - Bereshit#^1-2]]
![[Torah 01 - Bereshit#^1-3]]
![[Torah 01 - Bereshit#^1-4]]
![[Torah 01 - Bereshit#^1-5]]

### Psalm · Psalm 29

![[Psalms 029#Chapter 29]]

### Second reading · Acts 19:1-7

![[Acts 19#^19-1]]
![[Acts 19#^19-2]]
![[Acts 19#^19-3]]
![[Acts 19#^19-4]]
![[Acts 19#^19-5]]
![[Acts 19#^19-6]]
![[Acts 19#^19-7]]

### Gospel · Mark 1:4-11

![[Mark 01#^1-4]]
![[Mark 01#^1-5]]
![[Mark 01#^1-6]]
![[Mark 01#^1-7]]
![[Mark 01#^1-8]]
![[Mark 01#^1-9]]
![[Mark 01#^1-10]]
![[Mark 01#^1-11]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
