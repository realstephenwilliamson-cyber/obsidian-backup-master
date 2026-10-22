---
type: rcl-sunday
cycle: "C"
occasion: "All Saints Day"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=p&d=83"
first_reading: "Daniel 7:1-3, 15-18"
psalm: "Psalm 149"
psalm_bcp: "Psalm 149"
second_reading: "Ephesians 1:11-23"
gospel: "Luke 6:20-31"
cycle_fixed: true
collect:
  - "[[BCP - Collects - Contemporary (Holy Days)#^collect-all-saints-day]]"
cssclasses:
  - lectionary
---

# All Saints Day — Year C

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=p&d=83>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Daniel 07#^7-1\|Daniel 7:1-3]], 15-18 |
| Psalm | Psalm 149 |
| Second Reading | [[Ephesians 01#^1-11\|Ephesians 1:11-23]] |
| Gospel | [[Luke 06#^6-20\|Luke 6:20-31]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Daniel 7:1-3, 15-18

![[Daniel 07#^7-1]]
![[Daniel 07#^7-2]]
![[Daniel 07#^7-3]]
![[Daniel 07#^7-15]]
![[Daniel 07#^7-16]]
![[Daniel 07#^7-17]]
![[Daniel 07#^7-18]]

### Psalm · Psalm 149

![[Psalms 149#Chapter 149]]

### Second reading · Ephesians 1:11-23

![[Ephesians 01#^1-11]]
![[Ephesians 01#^1-12]]
![[Ephesians 01#^1-13]]
![[Ephesians 01#^1-14]]
![[Ephesians 01#^1-15]]
![[Ephesians 01#^1-16]]
![[Ephesians 01#^1-17]]
![[Ephesians 01#^1-18]]
![[Ephesians 01#^1-19]]
![[Ephesians 01#^1-20]]
![[Ephesians 01#^1-21]]
![[Ephesians 01#^1-22]]
![[Ephesians 01#^1-23]]

### Gospel · Luke 6:20-31

![[Luke 06#^6-20]]
![[Luke 06#^6-21]]
![[Luke 06#^6-22]]
![[Luke 06#^6-23]]
![[Luke 06#^6-24]]
![[Luke 06#^6-25]]
![[Luke 06#^6-26]]
![[Luke 06#^6-27]]
![[Luke 06#^6-28]]
![[Luke 06#^6-29]]
![[Luke 06#^6-30]]
![[Luke 06#^6-31]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
