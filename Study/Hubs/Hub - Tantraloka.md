---
type: hub
created: 2026-10-02
status: active
cssclasses:
  - wide
  - home
aliases:
  - "Tantraloka Hub"
---
# Hub - Tantrāloka

> [!abstract] Scope & Synthesis
> The primary research and practice hub for the systematic study of Abhinavagupta’s *Tantrāloka* (Light on the Tantras) across its 37 Āhnikas, integrating the root Sanskrit text, Jayaratha’s *Viveka* commentary, Mark Dyczkowski’s 11-volume translation, lexical analysis via the Digital Corpus of Sanskrit (DCS) and Monier-Williams, and the daily liturgical reading cycle.

## What this is for

The three-year reading of Abhinavagupta's Tantrāloka with Jayaratha's commentary: the plan, the text, the tools for reading it, and what you write along the way.

## Core Library

> [!links]
> - **Primary Corpora:** [[Tantraloka 01 - Vijnanabhedaprakasana|Tantrāloka (Reading Copy)]] (each āhnika has an overview note and one note per verse) · [[Tantraloka|Tantrāloka (Muktabodha E-Text)]] · [[Library/Sanskrit/KSTS/Trika/KSTS - Tantraloka Sanskrit (vols I-XII)/KSTS volumes|KSTS Sanskrit Edition (vols I-XII)]] and the [[Tantraloka verse-page map]]
> - **Translations & Commentaries:** [[Dyczkowski - Tantraloka (tr., vols I-XI)|Dyczkowski Translation (vols I-XI)]] (the translation the plan follows) · [[Chakravarty, Marjanovic (tr.) - Tantrasara of Abhinavagupta|Tantrasāra (Chakravarty & Marjanovic)]] · [[Rastogi - Introduction to the Tantraloka|Rastogi — Introduction to the Tantrāloka]]
> - **Lexicons & Grammars:** [[Library/Sanskrit/Monier-Williams/README - Monier-Williams|Monier-Williams Database]] · [[Library/Sanskrit/Tantraloka words/Tantraloka words (DCS)|Tantrāloka Words (DCS)]] · [[Brunner (ed.) - Tantrikabhidhanakosa]] · [[Vocabulary (Tantraloka)|Master Vocabulary Register]] · [[Ruppel - Cambridge Introduction to Sanskrit|Ruppel Sanskrit Grammar]]

## Study Plans & Liturgical Pacing

> [!links]
> - Master Overview: [[Texts/Tantraloka/Study plan/Tantraloka study plan|Tantrāloka Study Plan (1,099 Portions)]]
> - Active Cycle: [[Texts/Tantraloka/Study plan/Study plan - Practice run 2026|Practice Run 2026 (Āhnikas 31–37)]]
> - Upcoming Triennial Cycles:
>   - [[Texts/Tantraloka/Study plan/Study plan - Year 1 (2026-27)|Year 1 (2026–2027)]]
>   - [[Texts/Tantraloka/Study plan/Study plan - Year 2 (2027-28)|Year 2 (2027–2028)]]
>   - [[Texts/Tantraloka/Study plan/Study plan - Year 3 (2028-29)|Year 3 (2028–2029)]]
> - [[Home]] has today's portion and the button for today's note.
> - [[Vocabulary (Tantraloka)|Words collected so far]]

## Around the text

> [!links]
> - [[Malinislokavarttika]]: Abhinavagupta on the Mālinīvijayottara
> - [[Abhinavagupta - An Introduction to Tantric Philosophy]] · [[Chakravarty, Marjanovic (tr.) - Tantrasara of Abhinavagupta|Tantrasāra of Abhinavagupta]]
> - [[Tantraloka - secondary literature]] · [[Scholars - library and free sources]]
> - [[Trika|Trika catalog]]

---

## The Conceptual Matrix

> [!mula]+ Fundamental Ontology & Non-Duality
> - [[Prakasa and Vimarsa]]
> - [[The Four Upayas of the Trika]]
> - [[Matrika - The Phonic Emanation of Reality]]
> - [[Scriptural Anatomical Mapping (Anga-sthana)|Scriptural Anatomical Mapping (Aṅga-sthāna)]]

> [!viveka]+ The Upāya Framework (Āhnikas 1–5)
> - [[Anupaya - The Direct Path (Ahnika 2)]]
> - [[Sambhavopaya - The Divine Path (Ahnika 3)]]
> - [[Saktopaya - The Cognitive Path (Ahnika 4)]]
> - [[Anavopaya - The Individual Path (Ahnika 5)]]

> [!philosophy]+ Cycles & Esoteric Ritual (Āhnikas 6–29)
> - [[Krama and the Twelve Kalis]]
> - [[Pratyabhijna as Johannine Hermeneutic]]
> - [[Dissolution of the Questioner]]

---

## Dynamic Feeds

*The tables of questions and the like collect the `question::` and `connects::` lines in your notes that link this hub, one of its concepts, a note it links, or one of its texts ([[Vault Guide#Fields|Fields]]).*

### Recent days

```dataview
TABLE WITHOUT ID file.link AS "Day", tantraloka_day AS "Plan day", length(verses_read) AS "Verses", length(filter(file.lists, (L) => L.word)) AS "Words", length(filter(file.lists, (L) => L.question OR L.claim OR L.connects)) AS "Reflection lines"
FROM "Journal"
WHERE type = "daily"
SORT date DESC
LIMIT 10
```

### Open questions on the Tantrāloka

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "questions", folders: ["Texts/Tantraloka"]})
```

### Connections across traditions

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "connections", folders: ["Texts/Tantraloka"]})
```

### Active Concept Notes
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

### Works your concepts cite

```dataview
TABLE WITHOUT ID key AS "Work", rows.file.link AS "Cited by", length(rows) AS "N"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
FLATTEN file.outlinks AS W
WHERE startswith(meta(W).path, "Catalog/")
GROUP BY W
SORT length(rows) DESC
```

### Trika & Tantric Literature Feed
```dataview
TABLE author, year
FROM "Catalog/Trika"
SORT file.ctime DESC
LIMIT 10
```

### Scholars in the library
*Scholars with a page in [[Scholars]] whose works in the library are in Trika or Hinduism. A name gets a page when [[Add scholar pages|Add scholar pages]] reaches it on the list.*
```dataview
TABLE WITHOUT ID file.link AS "Scholar", affiliation AS "Position", subjects AS "Subjects"
FROM "Catalog/Scholars"
WHERE type = "scholar" AND (econtains(subjects, "Trika") OR econtains(subjects, "Hinduism"))
SORT file.name ASC
```
