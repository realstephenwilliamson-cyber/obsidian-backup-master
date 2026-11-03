---
type: hub
status: active
cssclasses:
  - home
aliases: []
---
# Hub - Hermeneutics as First Philosophy

> [!abstract] Overview
> Levinas answered the catastrophes of the first half of the twentieth century by making ethics first philosophy. This hub gathers the material for the counter-claim sketched in [[Hermeneutics as First Philosophy]]: that a world of mediated exploitation and algorithmically shaped interpretation needs hermeneutics, the inquiry into meaning as such, as first philosophy. *(Drafted by AI from that note on 29 Oct 2026; rewrite it as you like.)*

## Core Library

> [!links]
> - **Ethics as first philosophy:** [[Levinas - Totality and Infinity|Totality and Infinity]] · [[Levinas - The Levinas Reader|The Levinas Reader]], with "Ethics as First Philosophy" ([[The Levinas Reader 07 - 5. Ethics as First Philosophy|read it in the vault]]) · [[Emmanuel Levinas]]
> - **Hermeneutics:** [[Ricoeur - Hermeneutics (Writings and Lectures Vol 2)|Hermeneutics (Ricoeur)]] · [[Ricoeur - The Model of the Text|The Model of the Text]] · [[Ricoeur - Freud and Philosophy|Freud and Philosophy]] · [[Ricoeur - Lectures on Ideology and Utopia|Lectures on Ideology and Utopia]] · [[Ricoeur - Oneself as Another|Oneself as Another]] · [[Ricoeur - The Course of Recognition|The Course of Recognition]] · [[Ricoeur - Figuring the Sacred|Figuring the Sacred]] · [[Dilthey - The Understanding of Other Persons and Their Expressions of Life|Dilthey on understanding others]] · [[Taylor - The Language Animal|The Language Animal]]
> - **The Other, dialogue, phenomenology:** [[Buber - I and Thou|I and Thou]] · [[Husserl - Ideas Pertaining to a Pure Phenomenology|Ideas (Husserl)]] · [[Merleau-Ponty - Phenomenology of Perception|Phenomenology of Perception]] · [[Stauffer - Ethical Loneliness - The Injustice of Not Being Heard|Ethical Loneliness]] · [[Steinbock - Phenomenology and Mysticism|Phenomenology and Mysticism]]
> - **Mediation and hidden costs:** [[Stiegler - The Age of Disruption|The Age of Disruption]] · [[Stiegler - Symbolic Misery (vols 1-2)|Symbolic Misery]] · [[Horkheimer, Adorno - Dialectic of Enlightenment|Dialectic of Enlightenment]] · [[Adorno - The Culture Industry|The Culture Industry]] · [[Marx - The Fragment on Machines|The Fragment on Machines]] · [[Heidegger - The Question Concerning Technology and Other Essays|The Question Concerning Technology]] · [[Wiener - Cybernetics|Cybernetics]] · [[Lessig - Code Version 2.0|Code 2.0]] · [[Ruiz - Structural Violence|Structural Violence]]
> - **Hermeneutics across traditions:** [[Gregor - Ricoeur's Hermeneutics of Religion|Ricoeur's Hermeneutics of Religion]] · [[Gschwandtner - Reading Religious Ritual with Ricoeur|Reading Religious Ritual with Ricoeur]] · [[Bilimoria and Baindur - Ricoeurian Hermeneutics and Indian Thought|Ricoeurian Hermeneutics and Indian Thought]]

*The groupings are a first sort by title; move or drop anything.*

---

## The Conceptual Matrix

> [!navigation]+ From the ideas note (not concept notes yet)
> - The Face of the Other in proximity, and radically mediated exploitation
> - The upstream and downstream costs hidden behind the curtain of commodities
> - Algorithmically manipulated political hermeneutics and conditioned reflexes
> - "What is hermeneutics?" asked in a radical register
> - Meaning as the architecture of reality at scale: potential crystallizing through relation

> [!navigation]+ Concepts already in the vault that may belong here (their `up:` names other hubs; add this hub there to list them below)
> - [[Pratyabhijna as Johannine Hermeneutic]] · [[Crisis of Attestation]] · [[The Crisis of Curation]] · [[Frictionless Expropriation]] · [[Engineered Cognitive Friction]] · [[The Scapegoat Reflex - Culprits vs Conditions]] · [[Proletarianization of Knowledge]] · [[Paul Ricoeur on State Power and Violence]] · [[The Threefold Frame of Historical Knowledge]]

> [!navigation]+ Related hubs
> - [[Hub - Technics, memory and the Leviathan]] · [[Hub - Tantraloka]] · [[Hub - Gospel of John]] · [[Hub - The Second Domestication]]

---

## Active Drafting

> [!links]
> - [[Hermeneutics as First Philosophy]] (the ideas note, in Notes)

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

### Recent Literature
```dataview
TABLE author, year
FROM "Catalog"
WHERE contains(subject, "Philosophy")
SORT file.ctime DESC
LIMIT 5
```

### Scholars in the library
```dataview
TABLE WITHOUT ID file.link AS "Scholar", affiliation AS "Position", subjects AS "Subjects"
FROM "Catalog/Scholars"
WHERE type = "scholar" AND (econtains(subjects, "Philosophy"))
SORT file.name ASC
```
