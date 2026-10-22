---
type: rcl-sunday
cycle: "B"
occasion: "All Saints Day"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=p&d=83"
first_reading: "Wisdom of Solomon 3:1-9 or Isaiah 25:6-9"
psalm: "Psalm 24"
psalm_bcp: "Psalm 24"
second_reading: "Revelation 21:1-6a"
gospel: "John 11:32-44"
cycle_fixed: true
collect:
  - "[[BCP - Collects - Contemporary (Holy Days)#^collect-all-saints-day]]"
cssclasses:
  - lectionary
---

# All Saints Day — Year B

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=p&d=83>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | Wisdom of Solomon 3:1-9 or [[Isaiah 25#^25-6\|Isaiah 25:6-9]] |
| Psalm | Psalm 24 |
| Second Reading | [[Revelation 21#^21-1\|Revelation 21:1-6a]] |
| Gospel | [[John 11#^11-32\|John 11:32-44]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Wisdom of Solomon 3:1-9 or Isaiah 25:6-9

![[LXX Wisdom of Solomon 03#^3-1]]
![[LXX Wisdom of Solomon 03#^3-2]]
![[LXX Wisdom of Solomon 03#^3-3]]
![[LXX Wisdom of Solomon 03#^3-4]]
![[LXX Wisdom of Solomon 03#^3-5]]
![[LXX Wisdom of Solomon 03#^3-6]]
![[LXX Wisdom of Solomon 03#^3-7]]
![[LXX Wisdom of Solomon 03#^3-8]]
![[LXX Wisdom of Solomon 03#^3-9]]

*or* **[[Isaiah 25#^25-6|Isaiah 25:6-9]]**

![[Isaiah 25#^25-6]]
![[Isaiah 25#^25-7]]
![[Isaiah 25#^25-8]]
![[Isaiah 25#^25-9]]

### Psalm · Psalm 24

![[Psalms 024#Chapter 24]]

### Second reading · Revelation 21:1-6a

![[Revelation 21#^21-1]]
![[Revelation 21#^21-2]]
![[Revelation 21#^21-3]]
![[Revelation 21#^21-4]]
![[Revelation 21#^21-5]]
![[Revelation 21#^21-6]]

### Gospel · John 11:32-44

![[John 11#^11-32]]
![[John 11#^11-33]]
![[John 11#^11-34]]
![[John 11#^11-35]]
![[John 11#^11-36]]
![[John 11#^11-37]]
![[John 11#^11-38]]
![[John 11#^11-39]]
![[John 11#^11-40]]
![[John 11#^11-41]]
![[John 11#^11-42]]
![[John 11#^11-43]]
![[John 11#^11-44]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
