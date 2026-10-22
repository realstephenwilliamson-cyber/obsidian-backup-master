---
updated: 2026-10-15
---
# Proposed changes awaiting approval (15 Oct 2026, morning)

**Applied on 15 Oct 2026, 08:33 EDT:** Stephen approved all five groups. The old links below are shown as code so they no longer count as links.

These touch your own notes (concepts, hubs, a journal note, Projects), so nothing below is applied until you approve. Reply "approved", or name the items to leave out. Claude then makes exactly these changes through Obsidian, with backups.

## 1. D15: the two links to the Wallis audiobook companion

Its catalog note goes to `.trash` (your decision D15); these two links then point to the full book, *Ksemaraja - The Recognition Sutras*. The labels stay as you wrote them.

### `Study/Concepts/Pratyabhijna as Johannine Hermeneutic.md`

Now:

> `[[Wallis - The Recognition Sutras|The Recognition Sutras (Wallis tr.)]]`

Proposed:

> [[Ksemaraja - The Recognition Sutras|The Recognition Sutras (Wallis tr.)]]

### `Study/Hubs/Hub - Gospel of John.md`

Now:

> `[[Wallis - The Recognition Sutras|Kṣemarāja — Pratyabhijñāhṛdayam (Recognition Sutras)]]`

Proposed:

> [[Ksemaraja - The Recognition Sutras|Kṣemarāja — Pratyabhijñāhṛdayam (Recognition Sutras)]]

## 2. D26: the hubs in two concepts' `up`

Each concept sits in a hub's matrix that its `up` property does not name.

### `Study/Concepts/Dissolution of the Questioner.md`

Now:

> up:
>   - "[[Hub - Gospel of John]]"

Proposed:

> up:
>   - "[[Hub - Gospel of John]]"
>   - "[[Hub - Tantraloka]]"

### `Study/Concepts/Hobbesian Artificial Man.md`

Now:

> up:
>   - "[[Hub - Technics, memory and the Leviathan]]"

Proposed:

> up:
>   - "[[Hub - Technics, memory and the Leviathan]]"
>   - "[[Hub - The Second Domestication]]"

## 3. D26: first mentions of concepts

Links in the style you already use (line 19 of *The Four Upayas* links Anupāya with "(see …)").

### `Study/Concepts/The Four Upayas of the Trika.md`

Now:

> and the sudden cessation of mental agitation.

Proposed:

> and the sudden cessation of mental agitation (see [[Sambhavopaya - The Divine Path (Ahnika 3)]]).

Now:

> replacing impure thoughts with pure awareness.

Proposed:

> replacing impure thoughts with pure awareness (see [[Saktopaya - The Cognitive Path (Ahnika 4)]]).

Now:

> ritual placement of mantras (*nyāsa*), and external worship.

Proposed:

> ritual placement of mantras (*nyāsa*), and external worship (see [[Anavopaya - The Individual Path (Ahnika 5)]]).

### `Journal/2026/2026-10-03.md`

Now:

> but the exact tertiary retentions through which

Proposed:

> but the exact [[Tertiary Retention|tertiary retentions]] through which

Now:

> **Ritual as the Curative Pharmakon**

Proposed:

> **Ritual as the Curative [[The Pharmakon of Digital Memory|Pharmakon]]**

### `Study/Concepts/How digital tertiary retention alters liturgical memory.md`

Now:

> habits that restore cognitive friction and deliberative latency

Proposed:

> habits that restore [[Engineered Cognitive Friction|cognitive friction]] and deliberative latency

## 4. D17: the `text` property in seven project notes

Seven project index notes use `text:` for a link to the project's text (for example `text: "[[Creed text 2026-09-29]]"`). In the catalog `text` means searchable / scan / print, so Obsidian treats the two as one property. Proposed: rename the key to `text_note:` in these seven notes; the values stay. Nothing in Home, the Bases or the views reads it (checked).

- What I Mean When I Say the Creed
- The Gospel of Recognition
- The Cybernetic Leviathan
- Second Domestication
- Cybernetic Anamnesis
- Let's Just Blame the Sea Peoples
- Artificial Interlocutor

## 5. D21: the Word footnotes in the two Creed AI notes

In `Projects/What I Mean When I Say the Creed/AI/`, *Claude - Read (Creed gloss review) (2026-08-14)* and *Claude - Balancing interpretation and exegetical history (2026-09-07)* keep Word footnote links that open nothing (`[1](#_ftn1)` in the text, `[1](#_ftnref1)` before each note). Proposed: make them Obsidian footnotes. Because the first note quotes three drafts that each number from 1, each draft gets its own letter so the numbers do not collide:

> Now: `> In other words, it is a gloss[1](#_ftn1), a word originally meaning …`
> and: `> [1](#_ftnref1)Greek glōssa, tongue or language; …`
>
> Proposed: `> In other words, it is a gloss[^a1], a word originally meaning …`
> and: `> [^a1]: Greek glōssa, tongue or language; …`

The footnote text itself is not changed. 14 lines in the first note, 2 in the second.
