---
type: rcl-sunday
cycle: "A"
occasion: "Wednesday of Holy Week"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=h&d=37"
first_reading: "Isaiah 50:4-9a"
psalm: "Psalm 70"
psalm_bcp: "Psalm 70"
second_reading: "Hebrews 12:1-3"
gospel: "John 13:21-32"
cycle_fixed: true
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-wednesday-in-holy-week]]"
cssclasses:
  - lectionary
---

# Wednesday of Holy Week — Year A

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=h&d=37>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Isaiah 50#^50-4\|Isaiah 50:4-9a]] |
| Psalm | Psalm 70 |
| Second Reading | [[Hebrews 12#^12-1\|Hebrews 12:1-3]] |
| Gospel | [[John 13#^13-21\|John 13:21-32]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Isaiah 50:4-9a

![[Isaiah 50#^50-4]]
![[Isaiah 50#^50-5]]
![[Isaiah 50#^50-6]]
![[Isaiah 50#^50-7]]
![[Isaiah 50#^50-8]]
![[Isaiah 50#^50-9]]

### Psalm · Psalm 70

![[Psalms 070#Chapter 70]]

### Second reading · Hebrews 12:1-3

![[Hebrews 12#^12-1]]
![[Hebrews 12#^12-2]]
![[Hebrews 12#^12-3]]

### Gospel · John 13:21-32

![[John 13#^13-21]]
![[John 13#^13-22]]
![[John 13#^13-23]]
![[John 13#^13-24]]
![[John 13#^13-25]]
![[John 13#^13-26]]
![[John 13#^13-27]]
![[John 13#^13-28]]
![[John 13#^13-29]]
![[John 13#^13-30]]
![[John 13#^13-31]]
![[John 13#^13-32]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
