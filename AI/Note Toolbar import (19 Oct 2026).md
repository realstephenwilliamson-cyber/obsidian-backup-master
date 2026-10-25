---
type: prompt
updated: 2026-10-19
---
# Note Toolbar import (19 Oct 2026)

Three toolbars for the Note Toolbar plugin, drafted on 19 October 2026 (the plugin's items not to change are in [[Vault Guide#Plugins|Plugins]]; the import is on the list in [[Open items]]). Nothing here is live: the callouts are kept inside plain-text blocks so that neither Note Toolbar nor Callout Studio renders them.

**How:** Settings → Note Toolbar → *Create toolbar from callout*; paste **one block at a time**, in this order (the Study toolbar's *Reference* item is a menu that points at the *CIS reference* toolbar by name). The importer turns `:LiName:` into the Lucide icon `lucide-name` if Obsidian has it, otherwise it logs *Icon not found* and the icon is set by hand; the `<!-- -->` comments become tooltips. **Visibility and position are not carried** by a callout: afterwards, in each toolbar's settings, set Position to *Top (fixed)* on desktop and *Floating button: right* on mobile, and set the Timeline, Ink and review items to desktop only. Then Settings → Note Toolbar → Rules: *Daily* if property `type` contains `daily`; *Study* if file name is `CIS study plan.md` or property `type` contains `cis-cards` or property `type` contains `flashcard`. Leave *Default toolbar* empty and *Scripting* off. Every file path below exists (checked on the laptop, 19 Oct 2026).

## 1. CIS reference (no rule: used only as a menu)

```text
> [!note-toolbar] CIS reference
> - [[Study/Sanskrit/CIS - Vocabulary (Ruppel).md|Vocabulary]]
> - [[Study/Sanskrit/CIS - Sandhi (Ruppel).md|Sandhi]]
> - [[Study/Sanskrit/CIS - Reference Grammar (Ruppel).md|Grammar]]
> - [[Study/Sanskrit/Conjunct Consonants - Reference List (Ruppel).md|Conjuncts]]
> - [[Study/Sanskrit/Ruppel - Cambridge Introduction to Sanskrit.md|Chapter notes]]
> - [[Library/Sanskrit/Monier-Williams/Monier-Williams Quick Lookup Guide.md|Monier-Williams]]
> - [[Study/Sanskrit/Devanagari search.md|Devanagari search]]
```

## 2. Daily (rule: property `type` contains `daily`)

```text
> [!note-toolbar] Daily
> - [:LiLayers: Cards]()<data data-ntb-command="obsidian-spaced-repetition:srs-review-flashcards"/> <!-- Review flashcards from all notes -->
> - [:LiTimer: Timeline]()<data data-ntb-command="day-planner-og:app:show-timeline"/> <!-- Day Planner OG: Show the timeline -->
> - [[Study/Sanskrit/Sanskrit scratchpad|:LiPenTool: Scratchpad]]
> - [:LiPencil: Ink]()<data data-ntb-command="ink:create-handwritten-section"/> <!-- New handwriting section (Editing view only) -->
> - <hr/>
> - [[Journal/Habits.base|:LiListChecks: Habits]]
> - [[Study/Sanskrit/CIS study plan.md|:LiGraduationCap: CIS]]
> - [[Texts/Tantraloka/Study plan/Tantraloka study plan.md|:LiBookOpen: Plan]]
> - [:LiCalendar: Today]()<data data-ntb-command="daily-notes"/> <!-- Open today's daily note -->
```

## 3. Study (rule: file name is `CIS study plan.md`, or `type` contains `cis-cards` or `flashcard`)

```text
> [!note-toolbar] Study
> - [:LiLayers: Review]()<data data-ntb-command="obsidian-spaced-repetition:srs-review-flashcards"/> <!-- Review flashcards from all notes -->
> - [:LiFileText: This note]()<data data-ntb-command="obsidian-spaced-repetition:srs-review-flashcards-in-note"/> <!-- Review flashcards in this note -->
> - [:LiRepeat: Cram]()<data data-ntb-command="obsidian-spaced-repetition:srs-cram-flashcards"/> <!-- Select a deck to cram -->
> - [[Study/Sanskrit/Sanskrit scratchpad|:LiPenTool: Scratchpad]]
> - <hr/>
> - [:LiBookOpen: Reference]()<data data-ntb-menu="CIS reference"/>
> - [[Study/Sanskrit/CIS study plan.md|:LiGraduationCap: Plan]]
> - [:LiLayoutDashboard: Layout]()<data data-ntb-command="workspaces:load"/> <!-- Load a workspace layout -->
```

**Not included on purpose:** previous/next day and this week (the daily note's first line already links them); Templater *Insert template* (it would duplicate content in a filled note). Lucide icon names other than calendar, pencil, glasses, scroll-text and ship-wheel were not checked against this Obsidian build (unverified).
