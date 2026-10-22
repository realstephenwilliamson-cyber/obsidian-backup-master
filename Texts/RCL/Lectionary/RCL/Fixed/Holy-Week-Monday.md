---
type: rcl-sunday
cycle: "fixed"
occasion: "Monday of Holy Week"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=h&d=35"
first_reading: "Isaiah 42:1-9"
psalm: "Psalm 36:5-11"
psalm_bcp: "Psalm 36:5-11"
second_reading: "Hebrews 9:11-15"
gospel: "John 12:1-11"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-monday-in-holy-week]]"
cssclasses:
  - lectionary
---

# Monday of Holy Week

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=h&d=35>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Isaiah 42#^42-1\|Isaiah 42:1-9]] |
| Psalm | [[Psalms 036#^36-6\|Psalm 36:5-11]] |
| Second Reading | [[Hebrews 09#^9-11\|Hebrews 9:11-15]] |
| Gospel | [[John 12#^12-1\|John 12:1-11]] |

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

### Psalm · Psalm 36:5-11

![[Psalms 036#^36-6]]
![[Psalms 036#^36-7]]
![[Psalms 036#^36-8]]
![[Psalms 036#^36-9]]
![[Psalms 036#^36-10]]
![[Psalms 036#^36-11]]
![[Psalms 036#^36-12]]

### Second reading · Hebrews 9:11-15

![[Hebrews 09#^9-11]]
![[Hebrews 09#^9-12]]
![[Hebrews 09#^9-13]]
![[Hebrews 09#^9-14]]
![[Hebrews 09#^9-15]]

### Gospel · John 12:1-11

![[John 12#^12-1]]
![[John 12#^12-2]]
![[John 12#^12-3]]
![[John 12#^12-4]]
![[John 12#^12-5]]
![[John 12#^12-6]]
![[John 12#^12-7]]
![[John 12#^12-8]]
![[John 12#^12-9]]
![[John 12#^12-10]]
![[John 12#^12-11]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
