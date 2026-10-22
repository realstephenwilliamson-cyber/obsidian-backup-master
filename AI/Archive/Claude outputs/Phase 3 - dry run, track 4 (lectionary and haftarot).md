# Track 4 – full change list (batch 2)

Companion to `/home/claude/p3/batch2/t4.md`. Nothing here has been applied.

**Files**

- Ready ops: `/home/claude/p3/batch2/t4-ready-ops.json`, 261 ops. They are the six Proper drafts in `drafts/t4/propers-*/ops.json` minus 6 duplicates (§5), then `drafts/t4/c9-repair/ops.json`. Each op keeps its `why` and `source` and names its draft and number in `draft`. Applied in order to the 7 Oct 04:08 snapshot, every `find` occurs once at its turn (re-run for this document). The 78 notes were not touched overnight: tracks 5, 1 and 2 changed LXX, Zohar, Soncino, Tanya and Mei HaShiloach notes and the concordance, and none of the 78 links to the renamed Zohar notes.
- Full list, one row per op: `/home/claude/p3/batch2/t4-changes.tsv` (columns: draft set, op number, note, kind, find, replace, source, why; newlines are written `\n` and backslashes doubled).
- Held for questions: `drafts/t4/propers-C-17-29/ops-C10-Proper-22C.json` (R4), `drafts/t4/template/*.json` (R2, R3). Haftarot: `drafts/t4/haftarot/` (rebuilt before applying, §9).

## 1. Counts by kind

| Kind | Ops | Notes |
|---|---|---|
| Two new properties after `gospel:` | 78 | 78 |
| Two new table rows after the Psalm row | 78 | 78 |
| New `## Complementary track` section before `## Homilies` | 78 | 78 |
| "or" option added to a track-1 property | 7 | 6 |
| "or" option added to a track-1 table cell | 7 | 6 |
| "or" option added to a track-1 section (heading, *or* line, embeds) | 7 | 6 |
| C9 repair: track-1 psalm slot (property, table cell, section) | 6 | 2 |
| **Total** | **261** | **78** |

Added in all: 156 properties, 156 table rows, 78 sections, 1,091 embeds and 142 links (table cells and *or* lines), 14 *or* lines. Of the embeds, 403 are psalm-portion verses (45 portions; every title offset read in the JPS text by a checker) and 50 are LXX verses (Wisdom, Sirach) in 7 notes, which need track 5 (applied 7 Oct, 01:11). 29 existing lines change (§3); everything else is inserted.

## 2. The 78 notes

Source: each note's own Vanderbilt page (`source:`), `https://lectionary.library.vanderbilt.edu/texts/?y=…&z=p&d=…`, with y = 17134 (Year A), 18921 (B), 19342 (C). "Track 1" shows any change to the existing semicontinuous slots.

| Note | d | Complementary first reading | Complementary psalm | Track 1 | Embeds | Links |
|---|---|---|---|---|---|---|
| Proper-4A | 58 | Deuteronomy 11:18-21, 26-28 | Psalm 31:1-5, 19-24 | — | 18 | 2 |
| Proper-5A | 59 | Hosea 5:15-6:6 | Psalm 50:7-15 | — | 16 | 2 |
| Proper-6A | 60 | Exodus 19:2-8a | Psalm 100 | — | 8 | 1 |
| Proper-7A | 61 | Jeremiah 20:7-13 | Psalm 69:7-10, (11-15), 16-18 | — | 19 | 2 |
| Proper-8A | 62 | Jeremiah 28:5-9 | Psalm 89:1-4, 15-18 | — | 13 | 2 |
| Proper-9A | 63 | Zechariah 9:9-12 | Psalm 145:8-14 | psalm: Psalm 45:10-17 → Psalm 45:10-17 or Song of Solomon 2:8-13 | 17 | 4 |
| Proper-10A | 64 | Isaiah 55:10-13 | Psalm 65:(1-8), 9-13 | — | 17 | 1 |
| Proper-11A | 65 | Wisdom of Solomon 12:13, 16-19 or Isaiah 44:6-8 | Psalm 86:11-17 | — | 15 | 3 |
| Proper-12A | 66 | 1 Kings 3:5-12 | Psalm 119:129-136 | psalm: Psalm 105:1-11, 45b → Psalm 105:1-11, 45b or Psalm 128 | 17 | 3 |
| Proper-13A | 67 | Isaiah 55:1-5 | Psalm 145:8-9, 14-21 | — | 15 | 2 |
| Proper-14A | 68 | 1 Kings 19:9-18 | Psalm 85:8-13 | — | 16 | 2 |
| Proper-15A | 69 | Isaiah 56:1, 6-8 | Psalm 67 | — | 5 | 1 |
| Proper-16A | 70 | Isaiah 51:1-6 | Psalm 138 | — | 7 | 1 |
| Proper-17A | 71 | Jeremiah 15:15-21 | Psalm 26:1-8 | — | 15 | 2 |
| Proper-18A | 72 | Ezekiel 33:7-11 | Psalm 119:33-40 | — | 13 | 2 |
| Proper-19A | 75 | Genesis 50:15-21 | Psalm 103:(1-7), 8-13 | psalm: Psalm 114 → Psalm 114 or Exodus 15:1b-11, 20-21 | 33 | 3 |
| Proper-20A | 76 | Jonah 3:10-4:11 | Psalm 145:1-8 | — | 20 | 2 |
| Proper-21A | 77 | Ezekiel 18:1-4, 25-32 | Psalm 25:1-9 | — | 21 | 2 |
| Proper-22A | 78 | Isaiah 5:1-7 | Psalm 80:7-15 | — | 16 | 2 |
| Proper-23A | 79 | Isaiah 25:1-9 | Psalm 23 | — | 10 | 1 |
| Proper-24A | 80 | Isaiah 45:1-7 | Psalm 96:1-9, (10-13) | — | 20 | 2 |
| Proper-25A | 81 | Leviticus 19:1-2, 15-18 | Psalm 1 | — | 7 | 1 |
| Proper-26A | 82 | Micah 3:5-12 | Psalm 43 | — | 9 | 1 |
| Proper-27A | 84 | Wisdom of Solomon 6:12-16 or Amos 5:18-24 | Wisdom of Solomon 6:17-20 or Psalm 70 | — | 17 | 3 |
| Proper-28A | 85 | Zephaniah 1:7, 12-18 | Psalm 90:1-8, (9-11), 12 | — | 20 | 2 |
| Reign-of-ChristA | 86 | Ezekiel 34:11-16, 20-24 | Psalm 95:1-7a | — | 18 | 2 |
| Proper-4B | 58 | Deuteronomy 5:12-15 | Psalm 81:1-10 | — | 14 | 2 |
| Proper-5B | 59 | Genesis 3:8-15 | Psalm 130 | — | 9 | 1 |
| Proper-6B | 60 | Ezekiel 17:22-24 | Psalm 92:1-4, 12-15 | — | 11 | 2 |
| Proper-7B | 61 | Job 38:1-11 | Psalm 107:1-3, 23-32 | first reading: 1 Samuel 17:(1a, 4-11, 19-23), 32-49 → 1 Samuel 17:(1a, 4-11, 19-23), 32-49 or 1 Samuel 17:57-18:5, 18:10-16; psalm: Psalm 9:9-20 → Psalm 9:9-20 or Psalm 133 | 39 | 5 |
| Proper-8B | 62 | Wisdom of Solomon 1:13-15, 2:23-24 or Lamentations 3:22-33 | Psalm 30 | — | 18 | 2 |
| Proper-9B | 63 | Ezekiel 2:1-5 | Psalm 123 | — | 6 | 1 |
| Proper-10B | 64 | Amos 7:7-15 | Psalm 85:8-13 | — | 15 | 2 |
| Proper-11B | 65 | Jeremiah 23:1-6 | Psalm 23 | — | 7 | 1 |
| Proper-12B | 66 | 2 Kings 4:42-44 | Psalm 145:10-18 | — | 12 | 2 |
| Proper-13B | 67 | Exodus 16:2-4, 9-15 | Psalm 78:23-29 | — | 17 | 2 |
| Proper-14B | 68 | 1 Kings 19:4-8 | Psalm 34:1-8 | — | 13 | 2 |
| Proper-15B | 69 | Proverbs 9:1-6 | Psalm 34:9-14 | — | 12 | 2 |
| Proper-16B | 70 | Joshua 24:1-2a, 14-18 | Psalm 34:15-22 | — | 15 | 2 |
| Proper-17B | 71 | Deuteronomy 4:1-2, 6-9 | Psalm 15 | — | 7 | 1 |
| Proper-18B | 72 | Isaiah 35:4-7a | Psalm 146 | — | 5 | 1 |
| Proper-19B | 75 | Isaiah 50:4-9a | Psalm 116:1-9 | psalm: Psalm 19 → Psalm 19 or Wisdom of Solomon 7:26-8:1 | 21 | 3 |
| Proper-20B | 76 | Wisdom of Solomon 1:16-2:1, 12-22 or Jeremiah 11:18-20 | Psalm 54 | — | 17 | 2 |
| Proper-21B | 77 | Numbers 11:4-6, 10-16, 24-29 | Psalm 19:7-14 | — | 24 | 2 |
| Proper-22B | 78 | Genesis 2:18-24 | Psalm 8 | — | 8 | 1 |
| Proper-23B | 79 | Amos 5:6-7, 10-15 | Psalm 90:12-17 | — | 14 | 2 |
| Proper-24B | 80 | Isaiah 53:4-12 | Psalm 91:9-16 | — | 17 | 2 |
| Proper-25B | 81 | Jeremiah 31:7-9 | Psalm 126 | — | 4 | 1 |
| Proper-26B | 82 | Deuteronomy 6:1-9 | Psalm 119:1-8 | — | 17 | 2 |
| Proper-27B | 84 | 1 Kings 17:8-16 | Psalm 146 | — | 10 | 1 |
| Proper-28B | 85 | Daniel 12:1-3 | Psalm 16 | psalm: Psalm 16 → 1 Samuel 2:1-10 | 13 | 2 |
| Reign-of-ChristB | 86 | Daniel 7:9-10, 13-14 | Psalm 93 | — | 5 | 1 |
| Proper-4C | 58 | 1 Kings 8:22-23, 41-43 | Psalm 96:1-9 | — | 14 | 2 |
| Proper-5C | 59 | 1 Kings 17:17-24 | Psalm 30 | — | 9 | 1 |
| Proper-6C | 60 | 2 Samuel 11:26-12:10, 13-15 | Psalm 32 | — | 16 | 1 |
| Proper-7C | 61 | Isaiah 65:1-9 | Psalm 22:19-28 | — | 19 | 2 |
| Proper-8C | 62 | 1 Kings 19:15-16, 19-21 | Psalm 16 | — | 6 | 1 |
| Proper-9C | 63 | Isaiah 66:10-14 | Psalm 66:1-9 | — | 14 | 2 |
| Proper-10C | 64 | Deuteronomy 30:9-14 | Psalm 25:1-10 | — | 16 | 2 |
| Proper-11C | 65 | Genesis 18:1-10a | Psalm 15 | — | 11 | 1 |
| Proper-12C | 66 | Genesis 18:20-32 | Psalm 138 | — | 14 | 1 |
| Proper-13C | 67 | Ecclesiastes 1:2, 12-14; 2:18-23 | Psalm 49:1-12 | — | 22 | 3 |
| Proper-14C | 68 | Genesis 15:1-6 | Psalm 33:12-22 | — | 17 | 2 |
| Proper-15C | 69 | Jeremiah 23:23-29 | Psalm 82 | — | 8 | 1 |
| Proper-16C | 70 | Isaiah 58:9b-14 | Psalm 103:1-8 | — | 14 | 2 |
| Proper-17C | 71 | Sirach 10:12-18 or Proverbs 25:6-7 | Psalm 112 | — | 10 | 2 |
| Proper-18C | 72 | Deuteronomy 30:15-20 | Psalm 1 | — | 7 | 1 |
| Proper-19C | 75 | Exodus 32:7-14 | Psalm 51:1-10 | — | 18 | 2 |
| Proper-20C | 76 | Amos 8:4-7 | Psalm 113 | — | 5 | 1 |
| Proper-21C | 77 | Amos 6:1a, 4-7 | Psalm 146 | — | 6 | 1 |
| Proper-22C | 78 | Habakkuk 1:1-4; 2:1-4 | Psalm 37:1-9 | — | 17 | 3 |
| Proper-23C | 79 | 2 Kings 5:1-3, 7-15c | Psalm 111 | — | 13 | 1 |
| Proper-24C | 80 | Genesis 32:22-31 | Psalm 121 | — | 11 | 1 |
| Proper-25C | 81 | Sirach 35:12-17 or Jeremiah 14:7-10, 19-22 | Psalm 84:1-7 | — | 20 | 3 |
| Proper-26C | 82 | Isaiah 1:10-18 | Psalm 32:1-7 | — | 16 | 2 |
| Proper-27C | 84 | Job 19:23-27a | Psalm 17:1-9 | psalm: Psalm 145:1-5, 17-21 → Psalm 145:1-5, 17-21 or Psalm 98 | 15 | 3 |
| Proper-28C | 85 | Malachi 4:1-2a | Psalm 98 | — | 3 | 1 |
| Reign-of-ChristC | 86 | Jeremiah 23:1-6 | Psalm 46 | psalm: Psalm 46 → Luke 1:68-79 | 18 | 2 |

## 3. Existing lines that change (29)

Each "or" line keeps its old text and gains the option; the old embeds stay first. In the two C9 notes the psalm slot changes and the old psalm moves to the new section.

- **Proper-9A**
  - `psalm: "Psalm 45:10-17"` → `psalm: "Psalm 45:10-17 or Song of Solomon 2:8-13"`
  - `| Psalm | [[Psalms 045#^45-11\|Psalm 45:10-17]] |` → `| Psalm | [[Psalms 045#^45-11\|Psalm 45:10-17]] or [[Song of Songs 2#^2-8\|Song of Solomon 2:8-13]] |`
  - `### Psalm · Psalm 45:10-17` → `### Psalm · Psalm 45:10-17 or Song of Solomon 2:8-13`
- **Proper-12A**
  - `psalm: "Psalm 105:1-11, 45b"` → `psalm: "Psalm 105:1-11, 45b or Psalm 128"`
  - `| Psalm | [[Psalms 105#^105-1\|Psalm 105:1-11]], 45b |` → `| Psalm | [[Psalms 105#^105-1\|Psalm 105:1-11]], 45b or Psalm 128 |`
  - `### Psalm · Psalm 105:1-11, 45b` → `### Psalm · Psalm 105:1-11, 45b or Psalm 128`
- **Proper-19A**
  - `psalm: "Psalm 114"` → `psalm: "Psalm 114 or Exodus 15:1b-11, 20-21"`
  - `| Psalm | Psalm 114 |` → `| Psalm | Psalm 114 or [[Torah 16 - Beshalach#^15-1\|Exodus 15:1b-11]], 20-21 |`
  - `### Psalm · Psalm 114` → `### Psalm · Psalm 114 or Exodus 15:1b-11, 20-21`
- **Proper-7B**
  - `first_reading: "1 Samuel 17:(1a, 4-11, 19-23), 32-49"` → `first_reading: "1 Samuel 17:(1a, 4-11, 19-23), 32-49 or 1 Samuel 17:57-18:5, 18:10-16"`
  - `psalm: "Psalm 9:9-20"` → `psalm: "Psalm 9:9-20 or Psalm 133"`
  - `| First Reading | 1 Samuel 17:(1a, 4-11, 19-23), 32-49 |` → `| First Reading | 1 Samuel 17:(1a, 4-11, 19-23), 32-49 or [[I Samuel 17#^17-57\|1 Samuel 17:57-18:5]], 18:10-16 |`
  - `| Psalm | [[Psalms 009#^9-10\|Psalm 9:9-20]] |` → `| Psalm | [[Psalms 009#^9-10\|Psalm 9:9-20]] or Psalm 133 |`
  - `### First reading · 1 Samuel 17:(1a, 4-11, 19-23), 32-49` → `### First reading · 1 Samuel 17:(1a, 4-11, 19-23), 32-49 or 1 Samuel 17:57-18:5, 18:10-16`
  - `### Psalm · Psalm 9:9-20` → `### Psalm · Psalm 9:9-20 or Psalm 133`
- **Proper-19B**
  - `psalm: "Psalm 19"` → `psalm: "Psalm 19 or Wisdom of Solomon 7:26-8:1"`
  - `| Psalm | Psalm 19 |` → `| Psalm | Psalm 19 or Wisdom of Solomon 7:26-8:1 |`
  - `### Psalm · Psalm 19` → `### Psalm · Psalm 19 or Wisdom of Solomon 7:26-8:1`
- **Proper-27C**
  - `psalm: "Psalm 145:1-5, 17-21"` → `psalm: "Psalm 145:1-5, 17-21 or Psalm 98"`
  - `| Psalm | [[Psalms 145#^145-1\|Psalm 145:1-5]], 17-21 |` → `| Psalm | [[Psalms 145#^145-1\|Psalm 145:1-5]], 17-21 or Psalm 98 |`
  - `### Psalm · Psalm 145:1-5, 17-21` → `### Psalm · Psalm 145:1-5, 17-21 or Psalm 98`
- **Proper-28B**
  - `psalm: "Psalm 16"` → `psalm: "1 Samuel 2:1-10"`
  - `| Psalm | Psalm 16 |` → `| Psalm | [[I Samuel 02#^2-1\|1 Samuel 2:1-10]] |`
  - `### Psalm · Psalm 16` → `### Psalm · 1 Samuel 2:1-10`
  - `![[Psalms 016#Chapter 16]]` → 10 embeds `![[I Samuel 02#^2-1]]` … `![[I Samuel 02#^2-10]]`; `![[Psalms 016#Chapter 16]]` reappears under `### Psalm (complementary) · Psalm 16`
- **Reign-of-ChristC**
  - `psalm: "Psalm 46"` → `psalm: "Luke 1:68-79"`
  - `| Psalm | Psalm 46 |` → `| Psalm | [[Luke 01#^1-68\|Luke 1:68-79]] |`
  - `### Psalm · Psalm 46` → `### Psalm · Luke 1:68-79`
  - `![[Psalms 046#Chapter 46]]` → 12 embeds `![[Luke 01#^1-68]]` … `![[Luke 01#^1-79]]`; `![[Psalms 046#Chapter 46]]` reappears under `### Psalm (complementary) · Psalm 46`

## 4. Twenty examples of the new section

Each block shows the two new properties, the new section's headings, the first and last embed of each run, and any *or* line. The callout "About the two tracks" (the same in all 78 notes) is left out here; its text is in §5.3 of `drafts/t4/FORMAT.md`.

```
Proper-4A
  first_reading_complementary: "Deuteronomy 11:18-21, 26-28"
  psalm_complementary: "Psalm 31:1-5, 19-24"
  ### First reading (complementary) · Deuteronomy 11:18-21, 26-28
    ![[Torah 46 - Eikev#^11-18]] … ![[Torah 47 - Re'eh#^11-28]]  (7)
  ### Psalm (complementary) · Psalm 31:1-5, 19-24
    ![[Psalms 031#^31-2]] … ![[Psalms 031#^31-25]]  (11)

Proper-9A
  first_reading_complementary: "Zechariah 9:9-12"
  psalm_complementary: "Psalm 145:8-14"
  ### First reading (complementary) · Zechariah 9:9-12
    ![[Zechariah 09#^9-9]] … ![[Zechariah 09#^9-12]]  (4)
  ### Psalm (complementary) · Psalm 145:8-14
    ![[Psalms 145#^145-8]] … ![[Psalms 145#^145-14]]  (7)

Proper-11A
  first_reading_complementary: "Wisdom of Solomon 12:13, 16-19 or Isaiah 44:6-8"
  psalm_complementary: "Psalm 86:11-17"
  ### First reading (complementary) · Wisdom of Solomon 12:13, 16-19 or Isaiah 44:6-8
    ![[LXX Wisdom of Solomon 12#^12-13]] … ![[LXX Wisdom of Solomon 12#^12-19]]  (5)
  *or* **[[Isaiah 44#^44-6|Isaiah 44:6-8]]**
    ![[Isaiah 44#^44-6]] … ![[Isaiah 44#^44-8]]  (3)
  ### Psalm (complementary) · Psalm 86:11-17
    ![[Psalms 086#^86-11]] … ![[Psalms 086#^86-17]]  (7)

Proper-13A
  first_reading_complementary: "Isaiah 55:1-5"
  psalm_complementary: "Psalm 145:8-9, 14-21"
  ### First reading (complementary) · Isaiah 55:1-5
    ![[Isaiah 55#^55-1]] … ![[Isaiah 55#^55-5]]  (5)
  ### Psalm (complementary) · Psalm 145:8-9, 14-21
    ![[Psalms 145#^145-8]] … ![[Psalms 145#^145-21]]  (10)

Proper-19A
  first_reading_complementary: "Genesis 50:15-21"
  psalm_complementary: "Psalm 103:(1-7), 8-13"
  ### First reading (complementary) · Genesis 50:15-21
    ![[Torah 12 - Vayechi#^50-15]] … ![[Torah 12 - Vayechi#^50-21]]  (7)
  ### Psalm (complementary) · Psalm 103:(1-7), 8-13
    ![[Psalms 103#^103-1]] … ![[Psalms 103#^103-13]]  (13)

Proper-24A
  first_reading_complementary: "Isaiah 45:1-7"
  psalm_complementary: "Psalm 96:1-9, (10-13)"
  ### First reading (complementary) · Isaiah 45:1-7
    ![[Isaiah 45#^45-1]] … ![[Isaiah 45#^45-7]]  (7)
  ### Psalm (complementary) · Psalm 96:1-9, (10-13)
    ![[Psalms 096#^96-1]] … ![[Psalms 096#^96-13]]  (13)

Proper-27A
  first_reading_complementary: "Wisdom of Solomon 6:12-16 or Amos 5:18-24"
  psalm_complementary: "Wisdom of Solomon 6:17-20 or Psalm 70"
  ### First reading (complementary) · Wisdom of Solomon 6:12-16 or Amos 5:18-24
    ![[LXX Wisdom of Solomon 06#^6-12]] … ![[LXX Wisdom of Solomon 06#^6-16]]  (5)
  *or* **[[Amos 5#^5-18|Amos 5:18-24]]**
    ![[Amos 5#^5-18]] … ![[Amos 5#^5-24]]  (7)
  ### Psalm (complementary) · Wisdom of Solomon 6:17-20 or Psalm 70
    ![[LXX Wisdom of Solomon 06#^6-17]] … ![[LXX Wisdom of Solomon 06#^6-20]]  (4)
  *or* **[[Psalms 070#^70-1|Psalm 70]]**
    ![[Psalms 070#Chapter 70]]

Reign-of-ChristA
  first_reading_complementary: "Ezekiel 34:11-16, 20-24"
  psalm_complementary: "Psalm 95:1-7a"
  ### First reading (complementary) · Ezekiel 34:11-16, 20-24
    ![[Ezekiel 34#^34-11]] … ![[Ezekiel 34#^34-24]]  (11)
  ### Psalm (complementary) · Psalm 95:1-7a
    ![[Psalms 095#^95-1]] … ![[Psalms 095#^95-7]]  (7)

Proper-4B
  first_reading_complementary: "Deuteronomy 5:12-15"
  psalm_complementary: "Psalm 81:1-10"
  ### First reading (complementary) · Deuteronomy 5:12-15
    ![[Torah 45 - Vaetchanan#^5-12]] … ![[Torah 45 - Vaetchanan#^5-15]]  (4)
  ### Psalm (complementary) · Psalm 81:1-10
    ![[Psalms 081#^81-2]] … ![[Psalms 081#^81-11]]  (10)

Proper-7B
  first_reading_complementary: "Job 38:1-11"
  psalm_complementary: "Psalm 107:1-3, 23-32"
  ### First reading (complementary) · Job 38:1-11
    ![[Job 38#^38-1]] … ![[Job 38#^38-11]]  (11)
  ### Psalm (complementary) · Psalm 107:1-3, 23-32
    ![[Psalms 107#^107-1]] … ![[Psalms 107#^107-32]]  (13)

Proper-8B
  first_reading_complementary: "Wisdom of Solomon 1:13-15, 2:23-24 or Lamentations 3:22-33"
  psalm_complementary: "Psalm 30"
  ### First reading (complementary) · Wisdom of Solomon 1:13-15, 2:23-24 or Lamentations 3:22-33
    ![[LXX Wisdom of Solomon 01#^1-13]] … ![[LXX Wisdom of Solomon 02#^2-24]]  (5)
  *or* **[[Lamentations 3#^3-22|Lamentations 3:22-33]]**
    ![[Lamentations 3#^3-22]] … ![[Lamentations 3#^3-33]]  (12)
  ### Psalm (complementary) · Psalm 30
    ![[Psalms 030#Chapter 30]]

Proper-19B
  first_reading_complementary: "Isaiah 50:4-9a"
  psalm_complementary: "Psalm 116:1-9"
  ### First reading (complementary) · Isaiah 50:4-9a
    ![[Isaiah 50#^50-4]] … ![[Isaiah 50#^50-9]]  (6)
  ### Psalm (complementary) · Psalm 116:1-9
    ![[Psalms 116#^116-1]] … ![[Psalms 116#^116-9]]  (9)

Proper-20B
  first_reading_complementary: "Wisdom of Solomon 1:16-2:1, 12-22 or Jeremiah 11:18-20"
  psalm_complementary: "Psalm 54"
  ### First reading (complementary) · Wisdom of Solomon 1:16-2:1, 12-22 or Jeremiah 11:18-20
    ![[LXX Wisdom of Solomon 01#^1-16]] … ![[LXX Wisdom of Solomon 02#^2-22]]  (13)
  *or* **[[Jeremiah 11#^11-18|Jeremiah 11:18-20]]**
    ![[Jeremiah 11#^11-18]] … ![[Jeremiah 11#^11-20]]  (3)
  ### Psalm (complementary) · Psalm 54
    ![[Psalms 054#Chapter 54]]

Proper-28B
  first_reading_complementary: "Daniel 12:1-3"
  psalm_complementary: "Psalm 16"
  ### First reading (complementary) · Daniel 12:1-3
    ![[Daniel 12#^12-1]] … ![[Daniel 12#^12-3]]  (3)
  ### Psalm (complementary) · Psalm 16
    ![[Psalms 016#Chapter 16]]

Proper-4C
  first_reading_complementary: "1 Kings 8:22-23, 41-43"
  psalm_complementary: "Psalm 96:1-9"
  ### First reading (complementary) · 1 Kings 8:22-23, 41-43
    ![[I Kings 08#^8-22]] … ![[I Kings 08#^8-43]]  (5)
  ### Psalm (complementary) · Psalm 96:1-9
    ![[Psalms 096#^96-1]] … ![[Psalms 096#^96-9]]  (9)

Proper-13C
  first_reading_complementary: "Ecclesiastes 1:2, 12-14; 2:18-23"
  psalm_complementary: "Psalm 49:1-12"
  ### First reading (complementary) · Ecclesiastes 1:2, 12-14; 2:18-23
    ![[Ecclesiastes 01#^1-2]] … ![[Ecclesiastes 02#^2-23]]  (10)
  ### Psalm (complementary) · Psalm 49:1-12
    ![[Psalms 049#^49-2]] … ![[Psalms 049#^49-13]]  (12)

Proper-17C
  first_reading_complementary: "Sirach 10:12-18 or Proverbs 25:6-7"
  psalm_complementary: "Psalm 112"
  ### First reading (complementary) · Sirach 10:12-18 or Proverbs 25:6-7
    ![[LXX Sirach 10#^10-12]] … ![[LXX Sirach 10#^10-18]]  (7)
  *or* **[[Proverbs 25#^25-6|Proverbs 25:6-7]]**
    ![[Proverbs 25#^25-6]] … ![[Proverbs 25#^25-7]]  (2)
  ### Psalm (complementary) · Psalm 112
    ![[Psalms 112#Chapter 112]]

Proper-25C
  first_reading_complementary: "Sirach 35:12-17 or Jeremiah 14:7-10, 19-22"
  psalm_complementary: "Psalm 84:1-7"
  ### First reading (complementary) · Sirach 35:12-17 or Jeremiah 14:7-10, 19-22
    ![[LXX Sirach 32#^32-10]] … ![[LXX Sirach 32#^32-14]]  (5)
  *or* **[[Jeremiah 14#^14-7|Jeremiah 14:7-10, 19-22]]**
    ![[Jeremiah 14#^14-7]] … ![[Jeremiah 14#^14-22]]  (8)
  ### Psalm (complementary) · Psalm 84:1-7
    ![[Psalms 084#^84-2]] … ![[Psalms 084#^84-8]]  (7)

Proper-28C
  first_reading_complementary: "Malachi 4:1-2a"
  psalm_complementary: "Psalm 98"
  ### First reading (complementary) · Malachi 4:1-2a
    ![[Malachi 3#^3-19]] … ![[Malachi 3#^3-20]]  (2)
  ### Psalm (complementary) · Psalm 98
    ![[Psalms 098#Chapter 98]]

Reign-of-ChristC
  first_reading_complementary: "Jeremiah 23:1-6"
  psalm_complementary: "Psalm 46"
  ### First reading (complementary) · Jeremiah 23:1-6
    ![[Jeremiah 23#^23-1]] … ![[Jeremiah 23#^23-6]]  (6)
  ### Psalm (complementary) · Psalm 46
    ![[Psalms 046#Chapter 46]]

```

## 5. Dropped: 6 duplicate ops

- `drafts/t4/propers-B-17-29/ops.json` ops 37–39 (Proper-28B) and `drafts/t4/propers-C-17-29/ops.json` ops 40–42 (Reign-of-ChristC), numbered from 1. They make the same change as the C9 repair's ops 4–6 and 10–12. Both checkers found that applying both sets gives duplicate properties, two pairs of table rows and two `## Complementary track` sections, and in one order the applier raises no error. The C9 repair is kept because it also fixes the psalm slot.
- `drafts/t4/examples/Proper-13A.example-ops.json` is an illustration only; the same three ops are in the A 4–16 set.

## 6. Order and dependencies

- **Track 5** (LXX blank lines, applied 7 Oct 01:11) had to come first: 50 embeds in Proper-11A, 27A, 8B, 19B, 20B, 17C and 25C, and Proper-19B's *or* link, use LXX verse ids that Obsidian registers only after it. The link check after applying confirms them.
- **Either order, same result** (tested by the checkers): `drafts/t4/template/ops-collect.json`, `ops-collect-keep-ids.json`, `drafts/t7/unassigned/ops-C34.json` (license lines), the Proper-22C ops (R4).
- **`drafts/t4/template/ops-psalm-bcp.json`** (R2): 8 of its ops (9 once R4 changes Proper-22C, under either option) anchor on psalm values that change, so they fail after these ops. If R2 is approved they are rebuilt: the two C9 notes' ops are dropped (the slot then holds a canticle, which that draft does not map), and the others are re-anchored, with a whole-psalm "or" option added (Proper-12A, 7B, 27C).

| Note | psalm_bcp op as drafted | After the Ready ops |
|---|---|---|
| Proper-12A | `psalm: "Psalm 105:1-11, 45b"` + `psalm_bcp: "Psalm 105:1-11, 45"` | psalm is now `Psalm 105:1-11, 45b or Psalm 128`: re-anchor |
| Proper-19A | `psalm: "Psalm 114"` + `psalm_bcp: "Psalm 114"` | psalm is now `Psalm 114 or Exodus 15:1b-11, 20-21`: re-anchor |
| Proper-9A | `psalm: "Psalm 45:10-17"` + `psalm_bcp: "Psalm 45:11-18"` | psalm is now `Psalm 45:10-17 or Song of Solomon 2:8-13`: re-anchor |
| Proper-19B | `psalm: "Psalm 19"` + `psalm_bcp: "Psalm 19"` | psalm is now `Psalm 19 or Wisdom of Solomon 7:26-8:1`: re-anchor |
| Proper-28B | `psalm: "Psalm 16"` + `psalm_bcp: "Psalm 16"` | psalm is now `1 Samuel 2:1-10`: drop |
| Proper-7B | `psalm: "Psalm 9:9-20"` + `psalm_bcp: "Psalm 9:9-20"` | psalm is now `Psalm 9:9-20 or Psalm 133`: re-anchor |
| Proper-22C | `psalm: "Psalm 137"` + `psalm_bcp: "Psalm 137"` | psalm is now `Lamentations 3:19-26 or Psalm 137` (R4 (a)) or `Psalm 137 or Lamentations 3:19-26` (R4 (b)): re-anchor |
| Proper-27C | `psalm: "Psalm 145:1-5, 17-21"` + `psalm_bcp: "Psalm 145:1-5, 18-22"` | psalm is now `Psalm 145:1-5, 17-21 or Psalm 98`: re-anchor |
| Reign-of-ChristC | `psalm: "Psalm 46"` + `psalm_bcp: "Psalm 46"` | psalm is now `Luke 1:68-79`: drop |

## 7. The template change (R2): exact diffs

From `drafts/t4/template/ops-template.json` applied to the snapshot. Context lines: 1.

### Templates/Homily.md

````diff
--- a/Templates/Homily.md
+++ b/Templates/Homily.md
@@ -3,2 +3,3 @@
 // picks the readings from the study plan (the feast of that day, if it has one); otherwise you choose from a list.
+// It also shows the collect of the day and the psalm as the Prayer Book prints it, when the lectionary note has them.
 const dir = "Texts/Tantraloka/Study plan/";
@@ -38,2 +39,23 @@
 const q = s => `"${String(s).replace(/"/g, '\\"')}"`;
+// The collect of the day and the psalm as the Prayer Book prints it (phase 3 of the October plan), from the lectionary
+// note's `collect` (links to the collects in Library/BCP 1979/03 The Collects) and `psalm_bcp` (the psalm in the Prayer
+// Book's own verse numbers). Without `psalm_bcp` a whole psalm is still shown (it needs no renumbering); part of a psalm gets a link.
+const emb = t => "!" + "[" + "[" + t + "]" + "]"; // an embed, written so that this template shows no unresolved link
+const lnk = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]";
+const collects = [].concat(fm.collect ?? []).filter(Boolean).map(s => String(s).replace(/^!?\[\[|\]\]$/g, "").split("|")[0]);
+const bcpPsalm = n => `BCP Psalm ${String(n).padStart(3, "0")}`;
+const psalmParts = s => String(s ?? "").split(/ or | and /).map(p => p.trim().replace(/^(\d)/, "Psalm $1")).filter(p => /^Psalm \d/.test(p));
+const bcpVerses = c => { // "Psalm 90:1-6, 13-17" or "Psalm 23" -> one embed per verse; a half verse (35b) or an optional part ("(19-22)") shows whole verses
+  const m = c.match(/^Psalm (\d+)(?::(.+))?$/);
+  const f = m ? app.metadataCache.getFirstLinkpathDest(bcpPsalm(+m[1]), "") : null;
+  if (!f) return "";
+  const range = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a + i);
+  const vs = m[2] ? m[2].split(",").flatMap(p => { const r = p.replace(/[\s()]/g, "").match(/^(\d+)[a-c]?(?:-(\d+)[a-c]?)?$/); return r ? range(+r[1], +(r[2] || r[1])) : []; })
+    : range(1, +(app.metadataCache.getFileCache(f)?.frontmatter?.verses || 0));
+  return vs.map(v => emb(`${f.basename}#^${+m[1]}-${v}`)).join("\n");
+};
+const psalmBcp = fm.psalm_bcp ? psalmParts(fm.psalm_bcp) : psalmParts(fm.psalm).every(p => /^Psalm \d+$/.test(p)) ? psalmParts(fm.psalm) : [];
+let psalmOut = psalmBcp.map(p => [p, bcpVerses(p)]).filter(x => x[1]).map(([p, e]) => `### ${p}\n\n${e}\n\n`).join("");
+if (!psalmOut && psalmParts(fm.psalm).length) psalmOut = `The lectionary gives ${fm.psalm} in the verse numbers of English Bibles; the Prayer Book numbers some psalms differently. ` +
+  psalmParts(fm.psalm).map(p => lnk(bcpPsalm(+p.match(/\d+/)[0]), p.replace(/:.*/, "") + " in the Prayer Book")).join(" · ") + "\n\n";
 let out = ["---", "type: homily", `date: ${date || ""}`, `occasion: ${occ ? q(`[[${occ}]]`) : '""'}`, `rcl_year: ${q(fm.cycle ?? year)}`,
@@ -42,3 +64,5 @@
 out += `# ${label}${date ? " · " + moment(date).format("D MMMM YYYY") : ""}\n\n`;
+if (collects.length) out += "## Collect of the day\n\n" + collects.map(emb).join("\n\n*or this*\n\n") + "\n\n";
 if (occ) out += `## Readings\n\n![[${occ}#Readings]]\n\n`;
+if (psalmOut) out += "## Psalm in the Prayer Book\n\n" + psalmOut;
 out += "## Earlier homilies on these readings\n\n```dataviewjs\nconst me = dv.current();\nconst base = l => String(l?.path ?? l ?? \"\").split(\"/\").pop().replace(/\\.md$/, \"\");\nconst hs = dv.pages('\"Writing/Homilies\"').where(p => p.file.path !== me.file.path && p.occasion && base(p.occasion) === base(me.occasion)).sort(p => p.date, \"desc\");\nif (hs.length) dv.table([\"Homily\", \"Date\", \"Stage\"], hs.map(p => [p.file.link, p.date, p.stage]));\nelse dv.paragraph(\"None yet. These readings come round again in three years.\");\n```\n\n";
````

### Templates/Homily (Polyphonic).md

````diff
--- a/Templates/Homily (Polyphonic).md
+++ b/Templates/Homily (Polyphonic).md
@@ -43,2 +43,23 @@
 const wl = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]"; // a wikilink, written so that Obsidian does not list this template's placeholders as unresolved
+// The collect of the day and the psalm as the Prayer Book prints it (phase 3 of the October plan), from the lectionary
+// note's `collect` (links to the collects in Library/BCP 1979/03 The Collects) and `psalm_bcp` (the psalm in the Prayer
+// Book's own verse numbers). Without `psalm_bcp` a whole psalm is still shown (it needs no renumbering); part of a psalm gets a link.
+const emb = t => "!" + "[" + "[" + t + "]" + "]"; // an embed, written so that this template shows no unresolved link
+const lnk = (t, a) => "[" + "[" + t + (a ? "|" + a : "") + "]" + "]";
+const collects = [].concat(fm.collect ?? []).filter(Boolean).map(s => String(s).replace(/^!?\[\[|\]\]$/g, "").split("|")[0]);
+const bcpPsalm = n => `BCP Psalm ${String(n).padStart(3, "0")}`;
+const psalmParts = s => String(s ?? "").split(/ or | and /).map(p => p.trim().replace(/^(\d)/, "Psalm $1")).filter(p => /^Psalm \d/.test(p));
+const bcpVerses = c => { // "Psalm 90:1-6, 13-17" or "Psalm 23" -> one embed per verse; a half verse (35b) or an optional part ("(19-22)") shows whole verses
+  const m = c.match(/^Psalm (\d+)(?::(.+))?$/);
+  const f = m ? app.metadataCache.getFirstLinkpathDest(bcpPsalm(+m[1]), "") : null;
+  if (!f) return "";
+  const range = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a + i);
+  const vs = m[2] ? m[2].split(",").flatMap(p => { const r = p.replace(/[\s()]/g, "").match(/^(\d+)[a-c]?(?:-(\d+)[a-c]?)?$/); return r ? range(+r[1], +(r[2] || r[1])) : []; })
+    : range(1, +(app.metadataCache.getFileCache(f)?.frontmatter?.verses || 0));
+  return vs.map(v => emb(`${f.basename}#^${+m[1]}-${v}`)).join("\n");
+};
+const psalmBcp = fm.psalm_bcp ? psalmParts(fm.psalm_bcp) : psalmParts(fm.psalm).every(p => /^Psalm \d+$/.test(p)) ? psalmParts(fm.psalm) : [];
+let psalmOut = psalmBcp.map(p => [p, bcpVerses(p)]).filter(x => x[1]).map(([p, e]) => `#### ${p}\n\n${e}\n\n`).join("");
+if (!psalmOut && psalmParts(fm.psalm).length) psalmOut = `The lectionary gives ${fm.psalm} in the verse numbers of English Bibles; the Prayer Book numbers some psalms differently. ` +
+  psalmParts(fm.psalm).map(p => lnk(bcpPsalm(+p.match(/\d+/)[0]), p.replace(/:.*/, "") + " in the Prayer Book")).join(" · ") + "\n\n";
 let out = ["---", "cssclasses:", "  - manuscript", "type: homily", "stage: drafting", `occasion: ${occ ? q(wl(occ)) : '""'}`,
@@ -56,3 +77,5 @@
 out += "> - **Relevant Conceptual Hubs:** [[Notes/Hubs/Hub - Gospel of John|Gospel of John]] · [[Notes/Hubs/Hub - Technics, memory and the Leviathan|Technics & Leviathan]]\n\n---\n\n";
+if (collects.length) out += "## Collect of the Day\n\n" + collects.map(emb).join("\n\n*or this*\n\n") + "\n\n---\n\n";
 out += "## Readings & Exegetical Notes\n\n" + (occ ? "!" + wl(occ + "#Readings") + "\n\n" : "") +
+  (psalmOut ? "### Psalm in the Prayer Book\n\n" + psalmOut : "") +
   "### First Reading (Hebrew Bible / Old Testament)\n\n\n\n### Psalm\n\n\n\n### Second Reading (Epistle)\n\n\n\n### The Holy Gospel\n\n\n\n---\n\n";
````

### Vault Guide.md

````diff
--- a/Vault Guide.md
+++ b/Vault Guide.md
@@ -61,3 +61,3 @@
 - **Polyphonic layout:** run *Templater: Create new note from template* → *Homily (Polyphonic)*. It takes the occasion and the week's parashah from the study plan (or asks), files the note in `Writing/Homilies` as `<date> <occasion> (polyphonic)`, and shows that parashah's Torah, Rashi, Mei HaShiloach and Zohar notes beside the readings.
-- **In the note:** the readings (embedded from the lectionary note), earlier homilies on the same readings, then Notes and Draft. Set `stage` to `idea`, `drafting`, `finished` or `preached`, and `preached_at`. [[Homilies]] and `Bases/Homilies.base` list them.
+- **In the note:** the collect of the day (Contemporary, from the lectionary note's `collect`), the readings (embedded from the lectionary note), the psalm in the Prayer Book's own words and verse numbers (from `psalm_bcp`), earlier homilies on the same readings, then Notes and Draft. Set `stage` to `idea`, `drafting`, `finished` or `preached`, and `preached_at`. [[Homilies]] and `Bases/Homilies.base` list them.
 
````

Other template-draft ops (R2, R3), all in `drafts/t4/template/`: `ops-collect.json` 357 (128 id renames, 6 joins of collects cut by a page marker, 2 Easter Vigil ids, 221 `collect` properties); `ops-psalm-bcp.json` 219 (217 after dropping the two C9 notes); maps `collect-map.tsv` and `psalm-bcp-map.tsv`. If R2 is not approved, the Guide sentence (the last diff) is not applied either.

## 8. Proper 22C (R4), held

As drafted for R4 (a); (b) is the same three ops with the two options swapped.

- `psalm: "Psalm 137"` → `psalm: "Lamentations 3:19-26 or Psalm 137"`
- `| Psalm | Psalm 137 |` → `| Psalm | [[Lamentations 3#^3-19\|Lamentations 3:19-26]] or Psalm 137 |`
- `### Psalm · Psalm 137` → `### Psalm · Lamentations 3:19-26 or Psalm 137`, then 8 Lamentations embeds, an *or* line, and the existing `![[Psalms 137#Chapter 137]]`

Source: `https://lectionary.library.vanderbilt.edu/texts/?y=19342&z=p&d=78`. The checker read the page twice: Lamentations 3:19-26 is the first option, Psalm 137 the second; the Lamentations embeds match the JPS text at both ends.

The five spacing and dash differences (left as the vault writes them under either R4 option); vault value, then the page as WebFetch returned it:

| Note | Slot | Vault | Page (WebFetch) | Page |
|---|---|---|---|---|
| Proper-14A | psalm | `Psalm 105:1-6, 16-22, 45b` | `Psalm 105: 1-6, 16-22, 45b` | y=17134 d=68 |
| Proper-15A | gospel | `Matthew 15:(10-20), 21-28` | `Matthew 15: (10-20), 21-28` | y=17134 d=69 |
| Proper-6B | first reading | `1 Samuel 15:34-16:13` | `1 Samuel 15:34 – 16:13` | y=18921 d=60 |
| Proper-13B | first reading | `2 Samuel 11:26-12:13a` | `2 Samuel 11:26 – 12:13a` | y=18921 d=67 |
| Proper-16B | first reading | `1 Kings 8:(1, 6, 10-11), 22-30, 41-43` | `1 Kings 8:(1,6,10-11), 22-30, 41-43` | y=18921 d=70 |

The new citations follow the vault: `Wisdom of Solomon 7:26-8:1` (Proper-19B), printed "7:26 – 8:1" on the page.

## 9. Haftarot (B25, B31): to be rebuilt before applying

As drafted (`drafts/t4/haftarot/`, against the 04:08 snapshot): 166 ops, 527 links.

- 1 new note, `Texts/Torah/Haftarot.md`: `## Parashot` (62 rows: 54 parashot, 7 doubled portions, Pinchas on or before 17 Tammuz), six short notes, `## Special Shabbatot` (10 rows, Ashkenazi, with the 35 study-plan dates), `## Sources`.
- 108 ops in the 54 parashah notes: the header line gains Mei HaShiloach (54), Zohar (44 as drafted) and `Haftarah: [[#Haftarah]]` (54); a `## Haftarah` section goes after the header line, before the first `## Chapter`.
- 57 ops in the concordance: a Haftarah column (header, alignment row, 54 cells; 13 cells add the Sephardi after `<br>S:`) and one sentence under the table.

Fixes in the rebuild:

- Kedoshim header: `Zohar: [[Zohar 8.04 - Parashat Qedoshim]]` → `Zohar: [[Zohar 8.03 - Parashat Qedoshim]]`. Emor header: `Zohar: [[Zohar 8.03 - Parashat Emor]]` → `Zohar: [[Zohar 8.04 - Parashat Emor]]`. (Haftarot checker: the drafted names no longer exist after last night's swap, and pointed at the wrong text before it.)
- Concordance column: rebuilt against the table as it stands after last night's Kedoshim/Emor cell fix. (The Zohar checker found the drafted column and that fix clashed on the same rows.)
- Ki Teitzei header: add `Zohar: [[Zohar 10.11 - Parashat Ki Tetse]]` once Z9 is in the concordance; the other nine portions get no Zohar item (your Z9 answer).
- The five rows with no reading (Vayakhel, Vayakhel-Pekudei, Metzora, Vayeilech, V'Zot HaBerachah) get "—" in the Sephardi cell, so an empty cell only means "the same reading".
- Dry-run count: 12 sections add the doubled portion's reading; 2 (Vayakhel, Pekudei) say the joint portion is always on Shabbat Parah or HaChodesh.
- Wording for Vayakhel and Metzora read alone as you answer R5.

Full per-note table and three before → after examples (Bereshit, Metzora, Pinchas): `drafts/t4/haftarot/dryrun.md`. Checker report: `drafts/t4/haftarot/check.md`.

