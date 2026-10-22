---
type: rcl-sunday
cycle: "A"
occasion: "Fourth Sunday of Easter"
license: "© 2005 Consultation on Common Texts. Used for non-profit study per CCT terms."
source: "https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=s&d=46"
first_reading: "Acts 2:42-47"
psalm: "Psalm 23"
psalm_bcp: "Psalm 23"
second_reading: "1 Peter 2:19-25"
gospel: "John 10:1-10"
collect:
  - "[[BCP - Collects - Contemporary (Seasons of the Year)#^collect-fourth-sunday-of-easter]]"
cssclasses:
  - lectionary
---

# Fourth Sunday of Easter — Year A

**Source:** <https://lectionary.library.vanderbilt.edu/texts/?y=17134&z=s&d=46>
**License:** Revised Common Lectionary Daily Readings © 2005 Consultation on Common Texts / Augsburg Fortress. Used for non-profit study.

| Reading | Citation |
|---|---|
| First Reading | [[Acts 02#^2-42\|Acts 2:42-47]] |
| Psalm | Psalm 23 |
| Second Reading | [[1 Peter 02#^2-19\|1 Peter 2:19-25]] |
| Gospel | [[John 10#^10-1\|John 10:1-10]] |

## Readings

> [!note]- About these texts
> New Testament: Berean Standard Bible with the SBL Greek New Testament. Old Testament and Psalms: JPS Tanakh (1985), which follows the Hebrew verse numbers; where those differ from English Bibles (most psalm headings, and passages such as [[Isaiah 08#^8-23|Isaiah 9:1–7]] or [[Joel 3#^3-1|Joel 2:28–32]]) the verses shown have been matched to the English citation. Apocrypha: Brenton's Septuagint.

### First reading · Acts 2:42-47

![[Acts 02#^2-42]]
![[Acts 02#^2-43]]
![[Acts 02#^2-44]]
![[Acts 02#^2-45]]
![[Acts 02#^2-46]]
![[Acts 02#^2-47]]

### Psalm · Psalm 23

![[Psalms 023#Chapter 23]]

### Second reading · 1 Peter 2:19-25

![[1 Peter 02#^2-19]]
![[1 Peter 02#^2-20]]
![[1 Peter 02#^2-21]]
![[1 Peter 02#^2-22]]
![[1 Peter 02#^2-23]]
![[1 Peter 02#^2-24]]
![[1 Peter 02#^2-25]]

### Gospel · John 10:1-10

![[John 10#^10-1]]
![[John 10#^10-2]]
![[John 10#^10-3]]
![[John 10#^10-4]]
![[John 10#^10-5]]
![[John 10#^10-6]]
![[John 10#^10-7]]
![[John 10#^10-8]]
![[John 10#^10-9]]
![[John 10#^10-10]]

## Homilies

```dataviewjs
const me = dv.current().file.name;
const HF = app.metadataCache.getFirstLinkpathDest("Homilies", "")?.parent?.path || "Projects/Homilies";
const hs = dv.pages('"' + HF + '"').where(p => p.occasion && String(p.occasion.path ?? p.occasion).split("/").pop().replace(/\.md$/, "") === me).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("No homilies on these readings yet. Start one from Home on the Sunday, or with the Homily template.");
```
