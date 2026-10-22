---
type: rcl-sunday
cycle: "C"
occasion: "Trinity Sunday"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=p&d=52"
first_reading: "Proverbs 8:1-4, 22-31"
psalm: "Psalm 8"
psalm_bcp: "Psalm 8"
second_reading: "Romans 5:1-5"
gospel: "John 16:12-15"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-first-sunday-after-pentecost-trinity-sunday]]"
cssclasses:
  - lectionary
---

# Trinity Sunday — Year C

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=p&d=52>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Proverbs 08#^8-1\|Proverbs 8:1-4]], 22-31 |
| Psalm | Psalm 8 |
| Second Reading | [[Romans 05#^5-1\|Romans 5:1-5]] |
| Gospel | [[John 16#^16-12\|John 16:12-15]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Proverbs 8:1-4, 22-31

![[Proverbs 08#^8-1]]
![[Proverbs 08#^8-2]]
![[Proverbs 08#^8-3]]
![[Proverbs 08#^8-4]]
![[Proverbs 08#^8-22]]
![[Proverbs 08#^8-23]]
![[Proverbs 08#^8-24]]
![[Proverbs 08#^8-25]]
![[Proverbs 08#^8-26]]
![[Proverbs 08#^8-27]]
![[Proverbs 08#^8-28]]
![[Proverbs 08#^8-29]]
![[Proverbs 08#^8-30]]
![[Proverbs 08#^8-31]]

### Psalm · Psalm 8

![[Psalms 008#Chapter 8]]

### Second reading · Romans 5:1-5

![[Romans 05#^5-1]]
![[Romans 05#^5-2]]
![[Romans 05#^5-3]]
![[Romans 05#^5-4]]
![[Romans 05#^5-5]]

### Gospel · John 16:12-15

![[John 16#^16-12]]
![[John 16#^16-13]]
![[John 16#^16-14]]
![[John 16#^16-15]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
