---
type: index
tags:
  - index
  - architecture
status: active
aliases:
  - Concepts and hubs
---
# Study

> [!abstract] The Vault Knowledge Graph
> An index of the main conceptual hubs, primary project maps, and atomic concept notes in the vault. 
> 
> * **Hubs** map entire research domains, linking texts, drafts, and dynamic feeds.
> * **Concepts** are single ideas formulated in your own words, pointing up to one or more Hubs via their `up` property.

**Hubs** map a whole project: what it's for, its key texts, your writing on it. **Concepts** are single ideas in your own words, one per note, each pointing up to the hubs it belongs to. A concept that shows up in more than one hub is where your projects meet.

**Sanskrit:** [[Sanskrit]] (the Ruppel course, the daily card, vocabulary and the look-up tools).

---

## Active Hubs

> [!links]
> - [[Hub - Technics, memory and the Leviathan|Hub — Technics, Memory and the Leviathan]]
> - [[Hub - Gospel of John|Hub — Gospel of John]]
> - [[Hub - Tantraloka|Hub — Tantrāloka]]
> - [[Hub - The Second Domestication|Hub — The Second Domestication & Axial Pedagogy]]

### All hubs

```dataview
LIST FROM "Study/Hubs"
WHERE file.path != "Study/Hubs/Hubs.md"
SORT file.name ASC
```

---

## Conceptual Matrices by Research Stream

### 1. Technics, Memory & Sovereign Power
```dataview
TABLE up as "Parent Hubs", status as "Status"
FROM "Study/Concepts"
WHERE contains(up, [[Hub - Technics, memory and the Leviathan]])
SORT file.name ASC
```

### 2. Johannine Commentary & Mystical Non-Duality
```dataview
TABLE up as "Parent Hubs", status as "Status"
FROM "Study/Concepts"
WHERE contains(up, [[Hub - Gospel of John]])
SORT file.name ASC
```

### 3. The Second Domestication & Axial Pedagogy
```dataview
TABLE up as "Parent Hubs", status as "Status"
FROM "Study/Concepts"
WHERE contains(up, [[Hub - The Second Domestication]])
SORT file.name ASC
```

### 4. Trika Shaivism & Sanskrit Metaphysics
```dataview
TABLE up as "Parent Hubs", status as "Status"
FROM "Study/Concepts"
WHERE contains(up, [[Hub - Tantraloka]])
SORT file.name ASC
```

---

## All Concepts

```dataview
TABLE WITHOUT ID file.link AS "Concept", up AS "Hubs", file.mtime AS "Last edited"
FROM "Study/Concepts"
WHERE file.path != "Study/Concepts/Concepts.md"
SORT file.name ASC
```

## Open questions

*Every `question::` line in your notes that has no `answer::` under it, newest note first ([[Vault Guide#Fields|Fields]]).*

```dataview
TABLE WITHOUT ID L.question AS "Question", L.section AS "Where"
FROM "Journal" or "Notes" or "Projects" or "Study"
FLATTEN file.lists AS L
WHERE L.question AND !L.task AND !startswith(file.path, "Projects/_Originals/") AND !any(map(L.children, (c) => c.answer))
SORT file.mtime DESC
LIMIT 40
```

## Adding one

- **Concept:** make a new note in `Study/Concepts`. It starts from the concept template; put one or more hubs in `up` (for example `[[Hub - Tantraloka]]`) and it appears on those hubs automatically.
- **Hub:** make a new note in `Study/Hubs` and fill in what it's for and its key texts. Its concept list fills itself.
