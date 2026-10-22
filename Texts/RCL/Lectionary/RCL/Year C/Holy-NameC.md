---
type: rcl-sunday
cycle: "C"
occasion: "Holy Name of Jesus"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=c&d=9"
first_reading: "Numbers 6:22-27"
psalm: "Psalm 8"
psalm_bcp: "Psalm 8"
second_reading: "Galatians 4:4-7"
gospel: "Luke 2:15-21"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-the-holy-name]]"
cssclasses:
  - lectionary
---

# Holy Name of Jesus — Year C

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=c&d=9>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Torah 35 - Nasso#^6-22\|Numbers 6:22-27]] |
| Psalm | Psalm 8 |
| Second Reading | [[Galatians 04#^4-4\|Galatians 4:4-7]] |
| Gospel | [[Luke 02#^2-15\|Luke 2:15-21]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Numbers 6:22-27

![[Torah 35 - Nasso#^6-22]]
![[Torah 35 - Nasso#^6-23]]
![[Torah 35 - Nasso#^6-24]]
![[Torah 35 - Nasso#^6-25]]
![[Torah 35 - Nasso#^6-26]]
![[Torah 35 - Nasso#^6-27]]

### Psalm · Psalm 8

![[Psalms 008#Chapter 8]]

### Second reading · Galatians 4:4-7

![[Galatians 04#^4-4]]
![[Galatians 04#^4-5]]
![[Galatians 04#^4-6]]
![[Galatians 04#^4-7]]

### Gospel · Luke 2:15-21

![[Luke 02#^2-15]]
![[Luke 02#^2-16]]
![[Luke 02#^2-17]]
![[Luke 02#^2-18]]
![[Luke 02#^2-19]]
![[Luke 02#^2-20]]
![[Luke 02#^2-21]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
