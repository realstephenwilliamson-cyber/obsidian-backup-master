---
type: rcl-sunday
cycle: "B"
occasion: "Thanksgiving Day"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=p&d=87"
first_reading: "Joel 2:21-27"
psalm: "Psalm 126"
psalm_bcp: "Psalm 126"
second_reading: "1 Timothy 2:1-7"
gospel: "Matthew 6:25-33"
cycle_fixed: true
collect:
  - "[[BCP - Collects - Contemporary (Holy Days)#^collect-thanksgiving-day]]"
cssclasses:
  - lectionary
---

# Thanksgiving Day — Year B

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=18921&z=p&d=87>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Joel 2#^2-21\|Joel 2:21-27]] |
| Psalm | Psalm 126 |
| Second Reading | [[1 Timothy 02#^2-1\|1 Timothy 2:1-7]] |
| Gospel | [[Matthew 06#^6-25\|Matthew 6:25-33]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Joel 2:21-27

![[Joel 2#^2-21]]
![[Joel 2#^2-22]]
![[Joel 2#^2-23]]
![[Joel 2#^2-24]]
![[Joel 2#^2-25]]
![[Joel 2#^2-26]]
![[Joel 2#^2-27]]

### Psalm · Psalm 126

![[Psalms 126#Chapter 126]]

### Second reading · 1 Timothy 2:1-7

![[1 Timothy 02#^2-1]]
![[1 Timothy 02#^2-2]]
![[1 Timothy 02#^2-3]]
![[1 Timothy 02#^2-4]]
![[1 Timothy 02#^2-5]]
![[1 Timothy 02#^2-6]]
![[1 Timothy 02#^2-7]]

### Gospel · Matthew 6:25-33

![[Matthew 06#^6-25]]
![[Matthew 06#^6-26]]
![[Matthew 06#^6-27]]
![[Matthew 06#^6-28]]
![[Matthew 06#^6-29]]
![[Matthew 06#^6-30]]
![[Matthew 06#^6-31]]
![[Matthew 06#^6-32]]
![[Matthew 06#^6-33]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
