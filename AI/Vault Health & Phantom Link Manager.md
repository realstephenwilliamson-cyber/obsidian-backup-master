---
type: dashboard
tags:
  - vault-health
  - maintenance
  - bases
status: active
---
# Vault Health & Phantom Link Manager

> [!abstract] Graph Hygiene & Health Metrics
> This dashboard monitors the connectivity, metadata completeness, and conceptual growth of your Obsidian vault. It surfaces "phantom" concepts (concepts linked on Hubs that have not yet been written), catalog review backlogs, and physical book inventory.

---

## 1. Hub Concept Implementation Tracker

```dataview
TABLE status, up, file.folder as "Location"
FROM "Study/Concepts"
SORT file.name ASC
```

---

## 2. Unwritten / Phantom Links Detector

This query lists the unresolved links (wikilinks pointing to notes that don't yet exist) in your four Hubs and in the Concept notes, with the note each one is in:

```dataviewjs
const roots = ["Study/Hubs/", "Study/Concepts/"];
const unresolved = app.metadataCache.unresolvedLinks;
const rows = [];
for (const src of Object.keys(unresolved).sort()) {
  if (!roots.some((r) => src.startsWith(r))) continue;
  for (const target of Object.keys(unresolved[src]).sort()) rows.push([dv.fileLink(src), target]);
}
if (rows.length) dv.table(["Note", "Missing target"], rows);
else dv.paragraph("No unresolved links in Study/Hubs or Study/Concepts.");
```

---

## 3. Physical Books Inventory (`physical_copy: true`)

Tracks all catalog items where you own a physical copy on your shelves:

```dataview
TABLE author, year, publisher, subject
FROM "Catalog"
WHERE physical_copy = true
SORT author ASC
```

---

## 4. Library Metadata Review Backlog (`status: review`)

Tracks items that need manual check against the original physical book or PDF:

```dataview
TABLE author, year, files
FROM "Catalog"
WHERE status = "review"
SORT file.name ASC
```
