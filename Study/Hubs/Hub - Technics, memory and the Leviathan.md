---
type: hub
status: active
cssclasses:
  - home
aliases: []
---
# Hub - Technics, Memory and the Leviathan

> [!abstract] Overview
> Exploring the intersection of algorithmic governance, state power, and human memory. This project maps Thomas Hobbes's conception of state sovereignty (the Leviathan) against Bernard Stiegler's framework of tertiary retention, examining how externalized technological memory reshapes political liberty, epistemological trust, and theological ethics.

## Core Library

> [!links]
> - **Primary:** [[Hobbes - Leviathan (parts 1-2)|Leviathan, Parts 1–2 (Hobbes, Bennett's adaptation)]] · [[Stiegler - Technics and Time (vols 1-3)|Technics and Time (Stiegler)]] · [[Stiegler - Symbolic Misery (vols 1-2)|Symbolic Misery (Stiegler)]] · [[Ricoeur - Memory, History, Forgetting|Memory, History, Forgetting (Ricoeur)]]
> - **Secondary:** [[Coeckelbergh - Green Leviathan or the Poetics of Political Liberty|Green Leviathan]] · [[Sreedhar - Hobbes on Resistance|Hobbes on Resistance]] · [[van Bekkum (ed.) - Playing with Leviathan|Playing with Leviathan (Biblical Reception)]] · [[Turner - Returning to Judgment|Returning to Judgment (Ben Turner)]]

## Leviathan in the texts

> [!links]
> - [[Psalms 104#^104-26|Psalm 104:26]] ([[BCP Psalm 104#^104-27|BCP 104:27]]) · [[Job 40#^40-25|Job 40:25–41:26]] (English 41:1–34) · [[Psalms 074#^74-14|Psalm 74:14]] · [[Isaiah 27#^27-1|Isaiah 27:1]] · [[Zohar 4.05 - Parashat Bo#^z2-34a|Zohar 2:34a–35b]] (reading Isaiah 27:1)

---

## The Conceptual Matrix

> [!philosophy]+ The Stieglerian Apparatus
> - [[Tertiary Retention]]
> - [[The Pharmakon of Digital Memory]]
> - [[Mnemotechnics vs Mnemo-technologies]]
> - [[Proletarianization of Knowledge]]
> - [[Epimetheus and the Default of Origin]]

> [!torah]+ Sovereignty and the State
> - [[Hobbesian Artificial Man]]
> - [[Algorithmic Governance as Sovereign]]
> - [[Auctoritas vs Circulation]]
> - [[The State as a Technical System]]
> - [[Paul Ricoeur on State Power and Violence]]
> - [[Theological critiques of absolute sovereignty]]

> [!navigation]+ Hermeneutics & Memory
> - [[The Threefold Frame of Historical Knowledge]]
> - [[Ready-at-Hand to On-Demand]]
> - [[Temporal Short-Circuits]]
> - [[The Crisis of Curation]]
> - [[Crisis of Attestation]]
> - [[Cybernetic Anamnesis (concept)]]

> [!navigation]+ Synthesis & Theology
> - [[How digital tertiary retention alters liturgical memory]]
> - [[Ethical imperatives for algorithmic design]]

---

## Active Drafting

> [!links]
> - [[The Cybernetic Leviathan]]
> - [[Leviathan fragments 2018-2024]]
> - [[Cybernetic Anamnesis]]
> - [[Cybernetic Anamnesis text 2025-11-05]]
> - The Digital Leviathan - Outline
> - [[2026-10-04 Proper 22A]]
> - 2026-11-22 Reign of Christ (A)

---

## Dynamic Feeds

*The tables of questions and the like collect the `question::`, `claim::` and `cites::` lines in your notes that link this hub, one of its concepts, or a note it links ([[Vault Guide#Fields|Fields]]).*

### Open questions

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "questions"})
```

### Claims

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "claims"})
```

### Sources cited

```dataviewjs
await dv.view("Templates/Views/hub-fields", {show: "cites"})
```

### Populated Concept Notes
```dataview
TABLE status, file.mtime as "Last Worked"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
SORT file.mtime DESC
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

### Concepts by status

```dataview
TABLE WITHOUT ID key AS "Status", rows.file.link AS "Concepts", length(rows) AS "N"
FROM "Study/Concepts"
WHERE contains(up, this.file.link)
GROUP BY default(status, "no status")
SORT key ASC
```

### Literature Feed (Philosophy & Politics)
```dataview
TABLE author, year, choice(rank < 99, "core", "") AS "Core"
FROM "Catalog"
FLATTEN default(object(
  "Hobbes - Leviathan (parts 1-2)", 1,
  "Stiegler - Technics and Time (vols 1-3)", 2,
  "Stiegler - Symbolic Misery (vols 1-2)", 3,
  "Ricoeur - Memory, History, Forgetting", 4,
  "Ricoeur - Oneself as Another", 5,
  "Wiener - Cybernetics", 6,
  "Stiegler - The Age of Disruption", 7,
  "Grant - Post-Modernism, Lyotard and Baudrillard", 8,
  "Coeckelbergh - Green Leviathan or the Poetics of Political Liberty", 9,
  "Sreedhar - Hobbes on Resistance", 10,
  "van Bekkum (ed.) - Playing with Leviathan", 11,
  "Turner - Returning to Judgment", 12
)[file.name], 99) AS rank
WHERE rank < 99 OR (contains(subject, "Philosophy") AND (contains(file.name, "Leviathan") OR contains(file.name, "Stiegler") OR contains(file.name, "Ricoeur")))
SORT rank ASC, year DESC, file.name ASC
```

### Scholars in the library
*Scholars with a page in [[Scholars]] whose works in the library are in philosophy. A name gets a page when [[Add scholar pages|Add scholar pages]] reaches it on the list.*
```dataview
TABLE WITHOUT ID file.link AS "Scholar", affiliation AS "Position", subjects AS "Subjects"
FROM "Catalog/Scholars"
WHERE type = "scholar" AND (econtains(subjects, "Philosophy"))
SORT file.name ASC
```
