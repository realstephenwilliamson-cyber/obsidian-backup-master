---
type: hub
created: 2026-10-02
status: active
cssclasses:
  - wide
  - home
aliases: []
---
# Hub - Gospel of John

> [!abstract] Thesis & Scope
> A theological, phenomenological, and mystical commentary on the Fourth Gospel. This project reads the Johannine text at the intersection of early Christian mystical theology (Gregory of Nyssa, Maximus the Confessor), non-dual recognition philosophy (*Pratyabhijñā* in Abhinavagupta), and radical Hasidic thought (the Ishbitzer Rebbe / Mei HaShiloach). It critiques exclusionary institutional readings of [[John 14#^14-6|John 14:6]] (*"No one comes to the Father except through me"*) and restores it as an apophatic threshold of egoic dissolution and divine recognition.

## What this is for

Everything around your commentary on John: the draft, the text, the patristic commentators, and the Sundays when John is read.

## Core Library

> [!links]
> - **Primary Texts:** [[John 01|Gospel of John (BSB + SBLGNT)]] (Greek and English, one note per chapter) · [[Augustine - Tractates on John|Augustine — Tractates on John]] · [[Catena Aurea on John - page map|Catena Aurea on John]]
> - **Textual & Exegetical:** [[Library/Lexicons/Greek NT/Greek NT Lexicon (MorphGNT)|Greek NT Lexicon (MorphGNT)]] · [[Ehrman - Text and Tradition, Clark Lectures|Ehrman — Text and Tradition]] · [[Ehrman - Text and Transmission, Clark Lecture 2 (2000)|Ehrman, Clark lecture 2]] · [[Parker - An Introduction to the New Testament Manuscripts and Their Texts|Parker — NT Manuscripts and Their Texts]]
> - **Theological & Mystical Convergences:** [[Ricoeur - The Course of Recognition|Ricoeur — The Course of Recognition]] · [[Tollefsen - The Christocentric Cosmology of St Maximus the Confessor|Tollefsen — Christocentric Cosmology of Maximus]] · [[Ksemaraja - The Recognition Sutras|Kṣemarāja — Pratyabhijñāhṛdayam (Recognition Sutras)]] · [[Mei HaShiloach|Mei HaShiloach (Ishbitzer Rebbe)]]

## Your writing

> [!links]
> - [[The Gospel of Recognition|The Gospel of Recognition]] (the work note, with versions and AI conversations)
> - [[Gospel of Recognition text 2026-08-05]]
> - [[Gospel Differences - Comparative Passages]]
> - [[What I Mean When I Say the Creed]]
> - [[Homilies]]

---

## The Conceptual Matrix

> [!torah]+ The Whirlwind & The Threshold
> - [[The Velvet Rope and the Velvet Noose]]
> - [[Dissolution of the Questioner]]
> - [[Oudeis as Ontological Negation]]

> [!philosophy]+ Recognition & Non-Dual Christology
> - [[Pratyabhijna as Johannine Hermeneutic]]
> - [[Apophatic Light in Gregory of Nyssa]]
> - [[Logos and Microcosm in Maximus the Confessor]]
> - [[Garments of the Absolute in Mei HaShiloach]]

> [!navigation]+ Exegetical Problems & Homiletics
> - [[The Johannine Parentheticals]]
> - [[The Divine Pedagogy in Job and John]]
> - [[Prakasa and Vimarsa]]

---

## Sundays with a reading from John

```dataviewjs
const ps = dv.pages('"Texts/RCL/Lectionary/RCL"').where(p => /^John /.test(String(p.gospel ?? ""))).sort(p => p.file.path);
if (ps.length) dv.table(["Sunday or feast", "Gospel"], ps.map(p => [p.file.link, p.gospel]));
else dv.paragraph("No lectionary notes with a reading from John found.");
```

## Homilies on John

```dataviewjs
const hs = dv.pages('"Projects/Homilies"').where(p => p.type === "homily" && [].concat(p.readings ?? []).some(r => /^John /.test(String(r)))).sort(p => p.date, "desc");
if (hs.length) dv.table(["Homily", "Date", "Stage"], hs.map(p => [p.file.link, p.date, p.stage]));
else dv.paragraph("None yet.");
```

## Dynamic Feeds

*The tables of questions and the like collect the `question::`, `claim::` and `connects::` lines in your notes that link this hub, one of its concepts, a note it links, or one of its texts ([[Vault Guide#Fields|Fields]]).*

### Days when the coming Sunday's gospel is John

```dataview
TABLE WITHOUT ID file.link AS "Day", sunday AS "Sunday", sunday.gospel AS "Gospel"
FROM "Journal"
WHERE type = "daily" AND typeof(sunday) = "link"
WHERE startswith(sunday.gospel, "John")
SORT date DESC
LIMIT 12
```

### Open questions on John

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "questions", folders: ["Texts/Bible/New Testament/04 John", "Texts/Bible/Douay-Rheims/50 John", "Texts/Bible/NRSVue/61 John", "Texts/Bible/Jewish Annotated New Testament/Annotations/04 John", "Texts/Fathers/Augustine - Tractates on John", "Texts/Fathers/Chrysostom - Homilies on John", "Texts/Fathers/Origen - Commentary on John"]})
```

### Claims

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "claims", folders: ["Texts/Bible/New Testament/04 John", "Texts/Bible/Douay-Rheims/50 John", "Texts/Bible/NRSVue/61 John", "Texts/Bible/Jewish Annotated New Testament/Annotations/04 John", "Texts/Fathers/Augustine - Tractates on John", "Texts/Fathers/Chrysostom - Homilies on John", "Texts/Fathers/Origen - Commentary on John"]})
```

### Connections across traditions

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "connections", folders: ["Texts/Bible/New Testament/04 John", "Texts/Bible/Douay-Rheims/50 John", "Texts/Bible/NRSVue/61 John", "Texts/Bible/Jewish Annotated New Testament/Annotations/04 John", "Texts/Fathers/Augustine - Tractates on John", "Texts/Fathers/Chrysostom - Homilies on John", "Texts/Fathers/Origen - Commentary on John"]})
```

### Populated Concept Notes
```dataview
TABLE status, file.mtime as "Last Worked"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
SORT file.mtime DESC
```

### Concepts by status

```dataview
TABLE WITHOUT ID key AS "Status", rows.file.link AS "Concepts", length(rows) AS "N"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
GROUP BY default(status, "no status")
SORT key ASC
```

### Johannine, Patristic & Biblical Literature
```dataview
TABLE author, year
FROM "Catalog"
WHERE contains(subject, "Christianity") OR contains(subject, "Biblical-Studies")
WHERE contains(file.name, "John") OR contains(file.name, "Augustine") OR contains(file.name, "Maximus") OR contains(file.name, "Gospel")
SORT file.ctime DESC
LIMIT 10
```

### Scholars in the library
*Scholars with a page in [[Scholars]] whose works in the library are in Christianity or biblical studies. A name gets a page when [[Add scholar pages|Add scholar pages]] reaches it on the list.*
```dataview
TABLE WITHOUT ID file.link AS "Scholar", affiliation AS "Position", subjects AS "Subjects"
FROM "Catalog/Scholars"
WHERE type = "scholar" AND (econtains(subjects, "Christianity") OR econtains(subjects, "Biblical-Studies"))
SORT file.name ASC
```
