---
cssclasses:
  - home
type: hub
status: active
aliases: []
---
# Hub - The Second Domestication & Axial Pedagogy

> [!abstract] Thesis & Scope
> Investigating the civilizational hinge between the first Axial Age (the domestication of the inert written word through communal formative disciplines) and the second Axial Age (the challenge of domesticating recursive, per-person, algorithmic machine-speed memory). It frames our contemporary polycrisis as a structural catastrophe of pedagogy: the substitution of engineered cognitive friction with frictionless algorithmic expropriation.

## Core Library
> [!links]
> - **Classical & Philosophical Anchors:** [[Phaedrus 274|Plato — Phaedrus (Thamus & Theuth)]] · [[Pirkei Avot|Pirkei Avot / Rabbinic Dialectic]] · [[Russell - A History of Western Philosophy|Russell — History of Western Philosophy]]
> - **Technological & Pedagogical Critiques:** [[Stiegler - Technics and Time (vols 1-3)|Stiegler — Technics and Time]] · [[Stiegler - Taking Care of Youth and the Generations|Stiegler — Taking Care of Youth]] · [[Heidegger - The Question Concerning Technology and Other Essays|Heidegger — Question Concerning Technology]] · [[Ricoeur - Memory, History, Forgetting|Ricoeur — Memory, History, Forgetting]]

---

## The Conceptual Matrix

> [!philosophy]+ The Two Hinges & Memory Technics
> - [[The First Axial Hinge - The Domestication of the Letter]]
> - [[The Second Axial Hinge - Recursive Retention]]
> - [[The Orphaned Word in the Phaedrus]]
> - [[Inert Writing vs Dynamic Algorithmic Feed]]
> - [[The Scapegoat Reflex - Culprits vs Conditions]]

> [!torah]+ Formation vs Expropriation
> - [[Engineered Cognitive Friction]]
> - [[Frictionless Expropriation]]
> - [[Dialectical Triad - Elenchus, Chavruta, and Koan]]
> - [[The Three Duties - Lectio, Disputatio, Praedicatio]]

> [!navigation]+ Political & Epistemic Implications
> - [[Ready-at-Hand to On-Demand]]
> - [[The Crisis of Curation]]
> - [[Temporal Short-Circuits]]
> - [[Auctoritas vs Circulation]]
> - [[Hobbesian Artificial Man]]

---

## Active Drafting
> [!links]
> - [[Second Domestication]]
> - [[Second Domestication outline 2026-07-07]]
> - [[Let's Just Blame the Sea Peoples]]
> - [[Sea Peoples flowchart 2026-07-24]]
> - [[Artificial Interlocutor]]
> - [[Artificial Interlocutor text 2026-03-25]]

---

## Dynamic Feeds

*The tables of questions and the like collect the `question::`, `claim::` and `connects::` lines in your notes that link this hub, one of its concepts, or a note it links ([[Vault Guide#Fields|Fields]]).*

### Open questions

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "questions"})
```

### Claims

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "claims"})
```

### Connections across traditions

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "connections"})
```

### Populated Concept Notes
```dataview
TABLE status, file.mtime as "Last Worked"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
SORT file.mtime DESC
```

### Concepts shared with the Technics hub

```dataview
TABLE WITHOUT ID file.link AS "Concept", status AS "Status"
FROM "Study/Concepts"
WHERE contains(up, this.file.link) AND contains(up, [[Hub - Technics, memory and the Leviathan]])
SORT file.name ASC
```

### Concepts by status

```dataview
TABLE WITHOUT ID key AS "Status", rows.file.link AS "Concepts", length(rows) AS "N"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
GROUP BY default(status, "no status")
SORT key ASC
```

### Scholars in the library
*Scholars with a page in [[Scholars]] whose works in the library are in philosophy. A name gets a page when [[Add scholar pages|Add scholar pages]] reaches it on the list.*
```dataview
TABLE WITHOUT ID file.link AS "Scholar", affiliation AS "Position", subjects AS "Subjects"
FROM "Catalog/Scholars"
WHERE type = "scholar" AND (econtains(subjects, "Philosophy"))
SORT file.name ASC
```
