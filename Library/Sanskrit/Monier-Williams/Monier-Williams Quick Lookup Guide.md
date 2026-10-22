---
prakasa: reference
status: active
---
# Monier-Williams lookup

Type a headword and press Enter. IAST (`prakāśa`) and plain letters (`prakasa`) both work. Exact headwords come first, then words that begin with what you typed, up to 40; click an entry to open or close it. The first search after Obsidian starts reads the whole dictionary (30 MB), so it takes a few seconds, longer on the phone.

```dataviewjs
await dv.view("Templates/Views/mw-lookup")
```

## About the data

The dictionary is the 1899 edition as digitized by the Cologne Digital Sanskrit Dictionaries: 286,525 records in one tab-separated file, `Library/Sanskrit/Monier-Williams/monier-williams.tsv`. Its columns are the record number, page and column of the print, the headword (IAST), the headword as printed, the homonym number, Monier-Williams' line, and the entry text with Sanskrit in IAST. There is no Devanagari column. Source, licence (non-commercial, share-alike) and credits are in [[Library/Sanskrit/Monier-Williams/README - Monier-Williams|README - Monier-Williams]].

## Words from your daily notes

In a daily note, write each new word under *Words* as an inline field, for example `- word:: prakāśa: light, manifestation`. [[Vocabulary (Tantraloka)]] gathers them all with the day you met them; look each one up here.

*Rewritten 5 Oct 2026. The earlier version of this note, from the crashed session, gave a wrong path for the dictionary, wrong columns and a lookup script that never existed.*
