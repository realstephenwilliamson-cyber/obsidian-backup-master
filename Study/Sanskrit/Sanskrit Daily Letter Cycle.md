---
type: study-plan
status: active
---
# Sanskrit Daily Letter Cycle (108-Day Repeating Wheel)

> [!abstract] The 108-Day Cycle
> This repeating calendar assigns one of the 108 Sanskrit cards to every day of your study. Over the 1,099-day Tantrāloka study course, this cycle repeats approximately **10 times**, ensuring that every letter, vowel sign, and ligature is encountered, written, and contemplated multiple times until recognition is effortless.

> [!note] Since 13 October 2026
> Home, the phone page and new daily notes show the [[Conjunct cycle (Tantraloka)|phoneme of the day]] (a conjunct from the Tantrāloka, decision D18) in place of this card. The card for each day is still here, and each of the fifty letters has its own note ([[Letters]]) with its cards.

## Today's card

```dataviewjs
await dv.view("Templates/Views/sanskrit-card")
```

## How It Works
* **Cycle Day Calculation:**
  $$\text{Card Number} = (\text{Days elapsed since start} \pmod{108}) + 1$$
  Card 1 fell on 3 October 2026.
* **Daily Integration:**
  * `Home.md` shows today's card, front and back, under **Today**.
  * Each new daily note in `Journal/` shows the card for its own date.
  * Handwriting: the day's card is written with Ink — in the daily note's *Letter practice*, under the card note's *Practice* heading, or on the [[Sanskrit scratchpad]] (since 21 Oct 2026; the one-sheet drawing idea was dropped).
* **Where the data lives:** every card's letter, glyph, classification, mouth position and images come from the table in [[Sanskrit 108 Flashcard Register|Sanskrit 108 Flashcard Register]]. Correct a row there and Home, this note and the daily notes all follow. The display code is `Templates/Views/sanskrit-card/view.js`.
* **Body places (*mātṛkā-nyāsa*):** each card shows where its letter goes on the body, from Abhinavagupta's list in [[Tantraloka 15.117|Tantrāloka 15.117–120]] with Jayaratha's commentary. Vowel signs use their vowel's place; syllables, conjuncts and words list each letter's place. The full scheme is in [[Scriptural Anatomical Mapping (Anga-sthana)|Scriptural Anatomical Mapping]].

## The cycle at a glance

```dataviewjs
const epoch = moment((JSON.parse(await app.vault.adapter.read("Templates/Views/paths.json")).letterCycleStart) || "2026-10-03"); // one copy of the cycle start in paths.json since 19 Oct 2026
const n = ((moment().startOf("day").diff(epoch, "days") % 108) + 108) % 108 + 1;
const start = moment().startOf("day").subtract(n - 1, "days");
dv.paragraph(`This round began on ${start.format("ddd D MMM YYYY")} and ends on ${start.clone().add(107, "days").format("ddd D MMM YYYY")}. Today is card ${n}.`);
const rows = [];
for (let k = 0; k < 7; k++) {
  const d = moment().startOf("day").add(k, "days");
  const c = ((d.diff(epoch, "days") % 108) + 108) % 108 + 1;
  rows.push([d.format("ddd D MMM"), c]);
}
dv.table(["Day", "Card"], rows);
```
