---
type: chores
updated: 2026-10-21
---
# Chores

The weekly chore schedule. One line per chore, in this exact shape: the list bullet (`- `), the chore, **a space, a dash, a space**, then the days. The dash may be an em dash (—), an en dash (–) or a plain hyphen (-) — what the template looks for is the space on each side of it: `Cat litter — daily` and `Cat litter - daily` are read; `Cat litter--daily` and `Cat litter-daily` are not. The days: `daily`, `weekdays`, `weekend`, or day names (`Sun`, `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`), separated by commas. When a daily note is made, its **Chores** section lists that weekday's chores as tasks dated that day, so they show on [[Home]] under *Due today or overdue* until ticked; the weekly note lists the week's chores by day. A change here shows from the next daily note on. Lines that do not fit the pattern are ignored.

Drag this note's tab into the right sidebar to keep the lists below in view.

## Today

Unticked chores due today or earlier. They live in the daily notes; a tick here is written there.

```tasks
not done
heading includes Chores
due before tomorrow
sort by due
short mode
```

## This week

The week's chores, ticked or not, by day.

```tasks
heading includes Chores
due after yesterday
due before in one week
group by due
sort by due
short mode
```

## The schedule

- Dishes — daily
- Bins out — Tue
- Cat litter — daily
- Self-Care — daily
- P.M.C.S. — Mon
