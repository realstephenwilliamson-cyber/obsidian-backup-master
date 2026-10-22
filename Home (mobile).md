---
cssclasses:
  - home
---
```dataviewjs
await dv.view("Templates/Views/today-header", { compact: true })
```

```dataviewjs
// The three parts are made first, in this order, and each view draws into its own, so the order is fixed (F3)
const holy = dv.container.createDiv(), study = dv.container.createDiv(), verses = dv.container.createDiv(), office = dv.container.createDiv();
await dv.view("Templates/Views/holyday", { container: holy })
await dv.view("Templates/Views/today-study", { container: study })
await dv.view("Templates/Views/today-verses", { container: verses })
await dv.view("Templates/Views/daily-office", { container: office })
```

```dataviewjs
await dv.view("Templates/Views/phoneme-card", { compact: true }); await dv.view("Templates/Views/today-items")
```

```tasks
not done
due before in one week
sort by due
short mode
```

```dataviewjs
await dv.view("Templates/Views/quick-capture")
```

[[Home|Full homepage]] · [[Texts]] · [[Study]] · [[Calendar]] · [[Vault Guide|Guide]]
