---
type: rcl-sunday
cycle: "A"
occasion: "Holy Saturday"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=h&d=40"
first_reading: "Job 14:1-14"
psalm: "Psalm 31:1-4, 15-16"
psalm_bcp: "Psalm 31:1-4, 15-16"
second_reading: "1 Peter 4:1-8"
gospel: "Matthew 27:57-66"
cycle_fixed: true
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-holy-saturday]]"
cssclasses:
  - lectionary
---

# Holy Saturday — Year A

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=h&d=40>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Job 14#^14-1\|Job 14:1-14]] |
| Psalm | [[Psalms 031#^31-2\|Psalm 31:1-4]], 15-16 |
| Second Reading | [[1 Peter 04#^4-1\|1 Peter 4:1-8]] |
| Gospel | [[Matthew 27#^27-57\|Matthew 27:57-66]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Job 14:1-14

![[Job 14#^14-1]]
![[Job 14#^14-2]]
![[Job 14#^14-3]]
![[Job 14#^14-4]]
![[Job 14#^14-5]]
![[Job 14#^14-6]]
![[Job 14#^14-7]]
![[Job 14#^14-8]]
![[Job 14#^14-9]]
![[Job 14#^14-10]]
![[Job 14#^14-11]]
![[Job 14#^14-12]]
![[Job 14#^14-13]]
![[Job 14#^14-14]]

### Psalm · Psalm 31:1-4, 15-16

![[Psalms 031#^31-2]]
![[Psalms 031#^31-3]]
![[Psalms 031#^31-4]]
![[Psalms 031#^31-5]]
![[Psalms 031#^31-16]]
![[Psalms 031#^31-17]]

### Second reading · 1 Peter 4:1-8

![[1 Peter 04#^4-1]]
![[1 Peter 04#^4-2]]
![[1 Peter 04#^4-3]]
![[1 Peter 04#^4-4]]
![[1 Peter 04#^4-5]]
![[1 Peter 04#^4-6]]
![[1 Peter 04#^4-7]]
![[1 Peter 04#^4-8]]

### Gospel · Matthew 27:57-66

![[Matthew 27#^27-57]]
![[Matthew 27#^27-58]]
![[Matthew 27#^27-59]]
![[Matthew 27#^27-60]]
![[Matthew 27#^27-61]]
![[Matthew 27#^27-62]]
![[Matthew 27#^27-63]]
![[Matthew 27#^27-64]]
![[Matthew 27#^27-65]]
![[Matthew 27#^27-66]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
