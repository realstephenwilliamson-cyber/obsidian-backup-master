---
cssclasses:
  - home
---
```dataviewjs
await dv.view("Templates/Views/today-header", { compact: true })
```

## Today

```dataviewjs
// The three parts are made first, in this order, and each view draws into its own, so the order is fixed (F3)
const holy = dv.container.createDiv(), study = dv.container.createDiv(), verses = dv.container.createDiv(), office = dv.container.createDiv();
await dv.view("Templates/Views/holyday", { container: holy })
await dv.view("Templates/Views/today-study", { container: study })
await dv.view("Templates/Views/today-verses", { container: verses })
await dv.view("Templates/Views/daily-office", { container: office })
```

[[Tantraloka study plan|Study plan]] · [[Study plan - Year 1 (2026-27)|Year 1 (2026–27)]] · [[Study plan - Year 2 (2027-28)|Year 2 (2027–28)]] · [[Study plan - Year 3 (2028-29)|Year 3 (2028–29)]] · [[Homilies]] · [[Vocabulary (Tantraloka)|Words]] · [[Sanskrit]]

### Phoneme of the day · CIS · Letter

```dataviewjs
await dv.view("Templates/Views/phoneme-card", { compact: true }); await dv.view("Templates/Views/today-items")
```

[[Conjunct cycle (Tantraloka)|The cycle]] · [[Letters|The fifty letters]] · [[Sanskrit Daily Letter Cycle|Today's flashcard]]

CIS minutes: M/W/F `INPUT[inlineSelect(option(5), option(10), option(15), option(20), option(25), option(30), option(35), option(40), option(45)):CIS study plan#cis_mwf]` · T/Th `INPUT[inlineSelect(option(5), option(10), option(15), option(20), option(25), option(30), option(35), option(40), option(45)):CIS study plan#cis_tth]`

## Tasks

Due today or overdue:

```tasks
not done
due before tomorrow
sort by due
short mode
```

Coming up in the next two weeks:

```tasks
not done
due after today
due before in two weeks
sort by due
short mode
```

Open, with no date (Journal, Notes, Projects, Study):

```tasks
not done
no due date
path regex matches /^(Journal|Notes|Projects|Study)\//
heading does not include Day Planner
path does not include CIS study plan
group by filename
short mode
```

## Go to

[[Catalog.base|Catalog]] · [[Texts]] · [[Study]] · [[Projects]] · [[Notes]] · [[Calendar]] · [[Vault Guide|Guide]] · [[Vault Guide|Tour]] · [[Home (mobile)|Phone page]]
