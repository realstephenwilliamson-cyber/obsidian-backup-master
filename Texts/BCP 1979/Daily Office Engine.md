---
type: liturgical-tool
status: active
---
# BCP 1979 Daily Office — today's readings

> [!abstract] Purpose
> Shows the Psalms and Lessons appointed for today in the Daily Office Lectionary of the 1979 Book of Common Prayer (pp. 934–1001), read live from the lectionary notes in `Texts/BCP 1979/15 Daily Office Lectionary/`. The view works out the lectionary year, the season and week, Holy Days and their transfers, and the Eves; nothing is typed in by hand.

## Use it

In any note (the Journal daily-note template is the natural place), add a DataviewJS block:

````markdown
```dataviewjs
await dv.view("Templates/Views/daily-office")
```
````

Options, all optional:

````markdown
```dataviewjs
await dv.view("Templates/Views/daily-office", { date: "2026-12-25", open: true })
```
````

- `date` — any `YYYY-MM-DD`; defaults to today. Use it to look ahead or to check a past day.
- `open: true` — render the block expanded instead of collapsed.
- `thanksgiving: false` — do not treat the fourth Thursday of November as Thanksgiving Day (the BCP names the feast but gives no date; the date comes from U.S. law).

The block's summary line reads, for example, `Daily Office · Year Two · Proper 22 · Tuesday`, or the Holy Day's name. Inside: Morning and Evening psalms (each linked to its Psalter note), the three Lessons as links into the Bible notes, the lectionary's footnotes for that day, an Evening Prayer block when the evening is an Eve, a note when a Holy Day replaces the weekday, and a link to the BCP page.

## What it follows

| Rule | BCP |
|---|---|
| Two-year cycle. Year One begins on the First Sunday of Advent before an odd-numbered year, Year Two before an even-numbered year. | p. 934 |
| Advent is the four Sundays before Christmas Day; Easter Day sets Ash Wednesday, Holy Week, Ascension (Thursday, forty days after Easter), Pentecost and Trinity Sunday. | p. 15; tables pp. 880–885 |
| Principal Feasts take precedence of any other day. Only the Holy Name, the Presentation and the Transfiguration take precedence of a Sunday; other Major Feasts on a Sunday are transferred to the first open day in the week. | pp. 15–16 |
| Fixed feasts are not kept in Holy Week or Easter Week (they move to the week after the Second Sunday of Easter, in order) and do not displace Ash Wednesday. | p. 17 |
| A Holy Day's Psalms and Lessons replace the weekday's. | pp. 16–17, 996–1000 |
| The dated days after the Epiphany are used only until the following Saturday evening. | p. 942 |
| Each week after Pentecost uses the Proper whose date is closest to its Sunday; the weekdays after Pentecost and after Trinity Sunday use the Proper closest to those Sundays. | pp. 158, 884–885, 964 |
| Eves (Christmas Eve, Eve of Holy Name, of the Epiphany, of 1 Epiphany, of Ascension, of Pentecost, of Trinity Sunday, and the seven Eves in the Holy Days table) are shown for Evening Prayer the day before. | pp. 938–964, 996–1000 |

Where the Prayer Book leaves a choice, the view shows both options rather than deciding: an Eve that falls on a Sunday appears beside the Sunday's entry; bracketed psalms and parenthesised verses are kept as printed (p. 935). Since 19 Oct 2026 the view also follows your choice on a Sunday that a Holy Day may take (the feast's Psalms and Lessons in place of the Sunday's: BCP p. 16 "when desired", and All Saints on the Sunday following November 1, p. 15); the choice is a row in [[Holy Days - my choices]], set by the button on Home, and the Holy Days are in [[Holy Days (BCP 1979)]]. It does not show other optional observances (Eves of Apostles, patronal and dedication feasts, Ember and Rogation days, Lesser Feasts).

## Files

- View: `Templates/Views/daily-office/view.js`. The calendar and parsing logic sits in a marked `CORE` block so it can be run outside Obsidian.
- Lectionary notes read by the view: [[BCP - Daily Office - Advent|Advent]] · [[BCP - Daily Office - Christmas|Christmas]] · [[BCP - Daily Office - Epiphany|Epiphany]] · [[BCP - Daily Office - Lent|Lent]] · [[BCP - Daily Office - Easter|Easter]] · [[BCP - Daily Office - The Season after Pentecost|Season after Pentecost]] · [[BCP - Daily Office - Holy Days|Holy Days]]. The [[BCP - Daily Office - Special Occasions|Special Occasions]] table is for use by hand.
- Rules: [[BCP - Concerning the Daily Office Lectionary|Concerning the Daily Office Lectionary]] (p. 934), [[BCP - The Calendar of the Church Year|The Calendar of the Church Year]] (pp. 15–33), [[BCP - Concerning the Proper of the Church Year|Concerning the Proper of the Church Year]] (p. 158), [[BCP - Tables|Tables for finding Easter and the movable feasts]] (pp. 880–885).
- Offices: [[BCP - Morning Prayer - Rite Two|Morning Prayer (Rite II)]] · [[BCP - Evening Prayer - Rite Two|Evening Prayer (Rite II)]] · [[BCP - An Order for Compline|Compline]]

## Checks made

Every day from 1 October 2026 to 31 December 2029 resolves to an entry. The Easter computation matches the Prayer Book's own table for every year 1900–2089. Readings were compared with Mission St. Clare and My Daily Office for Sept–Oct 2026 and Dec 2025, the calendar with The Lectionary Page's 2026 and 2027 calendars, and the Advent text with Ken Collins' transcription; details are in the build report in the Claude project (vault-rescue notes, doc 04).

> [!note] Known gaps
> The lectionary notes contain a few OCR slips (`Heb, 1:1-12`, `Matt. 12-14-21`, `ACts 16:16-24`, `2 tim. 1:1-14`) which the view shows as written; correcting the notes corrects the view. Thanksgiving's date is a civil rule, not a Prayer Book one. Transfers follow the Prayer Book's "first open day" literally; a parish may keep a transferred feast on another open day of the week.

## Credits

Text: *The Book of Common Prayer* (1979), The Episcopal Church — public domain; the lectionary notes were made from the bcponline source files. View and tests built with Claude, October 2026, for Stephen's vault; the previous month-based engine (which guessed the season from the calendar month) is retired.
