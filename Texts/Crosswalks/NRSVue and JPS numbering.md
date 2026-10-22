---
type: "crosswalk"
work: "NRSVue and JPS numbering"
license: "CC BY-SA 4.0"
source:
  - "The NRSVue notes' own text notes of the form \"x.y in Heb\" (Texts/Bible/NRSVue)"
  - "https://github.com/Copenhagen-Alliance/versification-specification/tree/master/versification-mappings/standard-mappings (eng.json)"
aliases:
  - "NRSVue numbering"
---
# NRSVue and JPS numbering

Where the chapter and verse numbers of the NRSVue (English numbering) differ from those of the JPS notes in [[Tanakh]] and [[Torah]] (Hebrew numbering, as in Sefaria). Every chapter not listed here has the same numbers in both. Each Tanakh chapter note and each chapter of a parashah note has a Compare line that links the NRSVue and repeats its row.

Derived from the NRSVue's own notes of the form "x.y in Heb" (58 of them, in 45 chapters): such a note puts its verse at that Hebrew verse, and the following verses keep in step until the two numberings meet again. Checked verse by verse against the Copenhagen Alliance English mapping (`eng.json`, the table the vault's reference linker uses, `AI/Prompts/Scripts/Reference linker/versif-eng.json`); the rows agree except where the Source column says otherwise. Where the NRSVue has no note (the Psalms, Daniel 3–6, 1 Kings 22, 1 Chronicles 12) the rows are Copenhagen's, and the verse counts of the two texts agree with them. The Decalogue rows follow the vault's Torah notes, which divide it as Sefaria does.

Licence: the rows taken from the Copenhagen Alliance versification specification (`eng.json`, CC BY-SA 4.0) are adapted here (JSON turned into this table, merged with the NRSVue's notes); this note is shared under the same licence.

**Reading a row.** "Heb 9:1–20 = NRSVue 9:2–21" means the JPS verses 9:1–20 are the NRSVue verses 9:2–21. "NRSVue 9:1 = Heb 8:23" names a verse of the NRSVue chapter that belongs to another Hebrew chapter. "Verses" gives the number of verses in the JPS chapter and in the NRSVue chapter of the same number.

## Torah, Prophets, Writings

| Book | Hebrew (JPS) | Verses JPS / NRSVue | Hebrew = NRSVue | Source |
|---|---|---|---|---|
| Genesis | [[Torah 07 - Vayetzei#Chapter 31\|Genesis 31]] | 54 / 55 | NRSVue 31:55 = Heb 32:1 | NRSVue note at 31:55. Copenhagen agrees |
| Genesis | [[Torah 07 - Vayetzei#Chapter 32\|Genesis 32]] | 33 / 32 | Heb 32:1 = NRSVue 31:55; Heb 32:2–33 = NRSVue 32:1–32 | NRSVue note at 31:55, carried on into NRSVue 32 (no note there). Copenhagen agrees |
| Exodus | [[Torah 14 - Vaera#Chapter 7\|Exodus 7]] | 29 / 25 | Heb 7:26–29 = NRSVue 8:1–4 | NRSVue note at 8:1. Copenhagen agrees |
| Exodus | [[Torah 14 - Vaera#Chapter 8\|Exodus 8]] | 28 / 32 | Heb 8:1–28 = NRSVue 8:5–32; NRSVue 8:1–4 = Heb 7:26–29 | NRSVue notes at 8:1, 8:5. Copenhagen agrees |
| Exodus | [[Torah 17 - Yitro#Chapter 20\|Exodus 20]] | 23 / 26 | Heb 20:13 = NRSVue 20:13–16; Heb 20:14–23 = NRSVue 20:17–26 | The vault's Torah notes divide the Decalogue as Sefaria does (23 verses); neither the NRSVue notes nor Copenhagen (BHS) cover it |
| Exodus | [[Torah 18 - Mishpatim#Chapter 21\|Exodus 21]] | 37 / 36 | Heb 21:37 = NRSVue 22:1 | NRSVue note at 22:1. Copenhagen agrees |
| Exodus | [[Torah 18 - Mishpatim#Chapter 22\|Exodus 22]] | 30 / 31 | Heb 22:1–30 = NRSVue 22:2–31; NRSVue 22:1 = Heb 21:37 | NRSVue notes at 22:1, 22:2. Copenhagen agrees |
| Leviticus | [[Torah 24 - Vayikra#Chapter 5\|Leviticus 5]] | 26 / 19 | Heb 5:20–26 = NRSVue 6:1–7 | NRSVue note at 6:1. Copenhagen agrees |
| Leviticus | [[Torah 25 - Tzav#Chapter 6\|Leviticus 6]] | 23 / 30 | Heb 6:1–23 = NRSVue 6:8–30; NRSVue 6:1–7 = Heb 5:20–26 | NRSVue notes at 6:1, 6:8. Copenhagen agrees |
| Numbers | [[Torah 38 - Korach#Chapter 16\|Numbers 16]] | 35 / 50 | NRSVue 16:36–50 = Heb 17:1–15 | NRSVue note at 16:36. Copenhagen agrees |
| Numbers | [[Torah 38 - Korach#Chapter 17\|Numbers 17]] | 28 / 13 | Heb 17:1–15 = NRSVue 16:36–50; Heb 17:16–28 = NRSVue 17:1–13 | NRSVue notes at 16:36, 17:1. Copenhagen agrees |
| Numbers | [[Torah 41 - Pinchas#Chapter 29\|Numbers 29]] | 39 / 40 | NRSVue 29:40 = Heb 30:1 | NRSVue note at 29:40. Copenhagen agrees |
| Numbers | [[Torah 41 - Pinchas#Chapter 30\|Numbers 30]] | 17 / 16 | Heb 30:1 = NRSVue 29:40; Heb 30:2–17 = NRSVue 30:1–16 | NRSVue note at 29:40, carried on into NRSVue 30 (no note there). Copenhagen agrees |
| Deuteronomy | [[Torah 45 - Vaetchanan#Chapter 5\|Deuteronomy 5]] | 30 / 33 | Heb 5:17 = NRSVue 5:17–20; Heb 5:18–30 = NRSVue 5:21–33 | The vault's Torah notes divide the Decalogue as Sefaria does (30 verses); neither the NRSVue notes nor Copenhagen (BHS) cover it |
| Deuteronomy | [[Torah 47 - Re'eh#Chapter 12\|Deuteronomy 12]] | 31 / 32 | NRSVue 12:32 = Heb 13:1 | NRSVue note at 12:32. Copenhagen agrees |
| Deuteronomy | [[Torah 47 - Re'eh#Chapter 13\|Deuteronomy 13]] | 19 / 18 | Heb 13:1 = NRSVue 12:32; Heb 13:2–19 = NRSVue 13:1–18 | NRSVue notes at 12:32, 13:1. Copenhagen agrees |
| Deuteronomy | [[Torah 49 - Ki Teitzei#Chapter 22\|Deuteronomy 22]] | 29 / 30 | NRSVue 22:30 = Heb 23:1 | NRSVue note at 22:30. Copenhagen agrees |
| Deuteronomy | [[Torah 49 - Ki Teitzei#Chapter 23\|Deuteronomy 23]] | 26 / 25 | Heb 23:1 = NRSVue 22:30; Heb 23:2–26 = NRSVue 23:1–25 | NRSVue note at 22:30, carried on into NRSVue 23 (no note there). Copenhagen agrees |
| Deuteronomy | [[Torah 50 - Ki Tavo#Chapter 28\|Deuteronomy 28]] | 69 / 68 | Heb 28:69 = NRSVue 29:1 | NRSVue note at 29:1. Copenhagen agrees |
| Deuteronomy | [[Torah 50 - Ki Tavo#Chapter 29\|Deuteronomy 29]] | 28 / 29 | Heb 29:1–28 = NRSVue 29:2–29; NRSVue 29:1 = Heb 28:69 | NRSVue notes at 29:1, 29:2. Copenhagen agrees |
| I Samuel | [[I Samuel 20\|I Samuel 20]] | 42 / 42 | Heb 20:42–21:1 = NRSVue 20:42 | NRSVue note at 20:42 ("This sentence is 21.1 in Heb"). Copenhagen maps all of 20:42 to Heb 21:1; the counts (42 / 42) agree with the NRSVue |
| I Samuel | [[I Samuel 21\|I Samuel 21]] | 16 / 15 | Heb 20:42–21:1 = NRSVue 20:42; Heb 21:2–16 = NRSVue 21:1–15 | NRSVue notes at 20:42 ("This sentence is 21.1 in Heb") and 21:1. Copenhagen maps all of 20:42 to Heb 21:1 |
| I Samuel | [[I Samuel 23\|I Samuel 23]] | 28 / 29 | NRSVue 23:29 = Heb 24:1 | NRSVue note at 23:29. Copenhagen agrees |
| I Samuel | [[I Samuel 24\|I Samuel 24]] | 23 / 22 | Heb 24:1 = NRSVue 23:29; Heb 24:2–23 = NRSVue 24:1–22 | NRSVue note at 23:29, carried on into NRSVue 24 (no note there). Copenhagen agrees |
| II Samuel | [[II Samuel 18\|II Samuel 18]] | 32 / 33 | NRSVue 18:33 = Heb 19:1 | NRSVue note at 18:33. Copenhagen agrees |
| II Samuel | [[II Samuel 19\|II Samuel 19]] | 44 / 43 | Heb 19:1 = NRSVue 18:33; Heb 19:2–44 = NRSVue 19:1–43 | NRSVue note at 18:33, carried on into NRSVue 19 (no note there). Copenhagen agrees |
| I Kings | [[I Kings 04\|I Kings 4]] | 20 / 34 | NRSVue 4:21–34 = Heb 5:1–14 | NRSVue note at 4:21. Copenhagen agrees |
| I Kings | [[I Kings 05\|I Kings 5]] | 32 / 18 | Heb 5:1–14 = NRSVue 4:21–34; Heb 5:15–32 = NRSVue 5:1–18 | NRSVue notes at 4:21, 5:1. Copenhagen agrees |
| I Kings | [[I Kings 22\|I Kings 22]] | 54 / 53 | Heb 22:43–44 = NRSVue 22:43; Heb 22:45–54 = NRSVue 22:44–53 | No NRSVue note. Copenhagen (22:43–53 = Heb 22:44–54) and the counts (54 / 53): Heb 22:43–44 are one NRSVue verse |
| II Kings | [[II Kings 11\|II Kings 11]] | 20 / 21 | NRSVue 11:21 = Heb 12:1 | NRSVue note at 11:21. Copenhagen agrees |
| II Kings | [[II Kings 12\|II Kings 12]] | 22 / 21 | Heb 12:1 = NRSVue 11:21; Heb 12:2–22 = NRSVue 12:1–21 | NRSVue note at 11:21, carried on into NRSVue 12 (no note there). Copenhagen agrees |
| I Chronicles | [[I Chronicles 05\|I Chronicles 5]] | 41 / 26 | Heb 5:27–41 = NRSVue 6:1–15 | NRSVue note at 6:1. Copenhagen agrees |
| I Chronicles | [[I Chronicles 06\|I Chronicles 6]] | 66 / 81 | Heb 6:1–66 = NRSVue 6:16–81; NRSVue 6:1–15 = Heb 5:27–41 | NRSVue notes at 6:1, 6:16. Copenhagen agrees |
| I Chronicles | [[I Chronicles 12\|I Chronicles 12]] | 41 / 40 | Heb 12:4–5 = NRSVue 12:4; Heb 12:6–41 = NRSVue 12:5–40 | No NRSVue note. Copenhagen (12:4–40 = Heb 12:5–41) and the counts (41 / 40): Heb 12:4–5 are one NRSVue verse |
| II Chronicles | [[II Chronicles 01\|II Chronicles 1]] | 18 / 17 | Heb 1:18 = NRSVue 2:1 | NRSVue note at 2:1. Copenhagen agrees |
| II Chronicles | [[II Chronicles 02\|II Chronicles 2]] | 17 / 18 | Heb 2:1–17 = NRSVue 2:2–18; NRSVue 2:1 = Heb 1:18 | NRSVue notes at 2:1, 2:2. Copenhagen agrees |
| II Chronicles | [[II Chronicles 13\|II Chronicles 13]] | 23 / 22 | Heb 13:23 = NRSVue 14:1 | NRSVue note at 14:1. Copenhagen agrees |
| II Chronicles | [[II Chronicles 14\|II Chronicles 14]] | 14 / 15 | Heb 14:1–14 = NRSVue 14:2–15; NRSVue 14:1 = Heb 13:23 | NRSVue notes at 14:1, 14:2. Copenhagen agrees |
| Nehemiah | [[Nehemiah 03\|Nehemiah 3]] | 38 / 32 | Heb 3:33–38 = NRSVue 4:1–6 | NRSVue note at 4:1. Copenhagen agrees |
| Nehemiah | [[Nehemiah 04\|Nehemiah 4]] | 17 / 23 | Heb 4:1–17 = NRSVue 4:7–23; NRSVue 4:1–6 = Heb 3:33–38 | NRSVue notes at 4:1, 4:7. Copenhagen agrees |
| Nehemiah | [[Nehemiah 07\|Nehemiah 7]] | 72 / 73 | Heb 7:68–72 = NRSVue 7:69–73; NRSVue 7:68 not in Heb | NRSVue note at 7:69 (= Heb 7:68), so NRSVue 7:68 has no Hebrew number. The NRSVue's own note at 7:68 says the MT lacks it; the JPS supplies it in brackets inside its 7:68 (footnote: missing in some mss., cf. Ezra 2.66). Copenhagen leaves 7:68 = Heb 7:68 |
| Nehemiah | [[Nehemiah 09\|Nehemiah 9]] | 37 / 38 | NRSVue 9:38 = Heb 10:1 | NRSVue note at 9:38. Copenhagen agrees |
| Nehemiah | [[Nehemiah 10\|Nehemiah 10]] | 40 / 39 | Heb 10:1 = NRSVue 9:38; Heb 10:2–40 = NRSVue 10:1–39 | NRSVue notes at 9:38, 10:1. Copenhagen agrees |
| Job | [[Job 40\|Job 40]] | 32 / 24 | Heb 40:25–32 = NRSVue 41:1–8 | NRSVue note at 41:1. Copenhagen agrees |
| Job | [[Job 41\|Job 41]] | 26 / 34 | Heb 41:1–26 = NRSVue 41:9–34; NRSVue 41:1–8 = Heb 40:25–32 | NRSVue notes at 41:1, 41:9. Copenhagen agrees |
| Ecclesiastes | [[Ecclesiastes 04\|Ecclesiastes 4]] | 17 / 16 | Heb 4:17 = NRSVue 5:1 | NRSVue note at 5:1. Copenhagen agrees |
| Ecclesiastes | [[Ecclesiastes 05\|Ecclesiastes 5]] | 19 / 20 | Heb 5:1–19 = NRSVue 5:2–20; NRSVue 5:1 = Heb 4:17 | NRSVue notes at 5:1, 5:2. Copenhagen agrees |
| Song of Songs | [[Song of Songs 6\|Song of Songs 6]] | 12 / 13 | NRSVue 6:13 = Heb 7:1 | NRSVue note at 6:13. Copenhagen agrees |
| Song of Songs | [[Song of Songs 7\|Song of Songs 7]] | 14 / 13 | Heb 7:1 = NRSVue 6:13; Heb 7:2–14 = NRSVue 7:1–13 | NRSVue note at 6:13, carried on into NRSVue 7 (no note there). Copenhagen agrees |
| Isaiah | [[Isaiah 08\|Isaiah 8]] | 23 / 22 | Heb 8:23 = NRSVue 9:1 | NRSVue note at 9:1. Copenhagen agrees |
| Isaiah | [[Isaiah 09\|Isaiah 9]] | 20 / 21 | Heb 9:1–20 = NRSVue 9:2–21; NRSVue 9:1 = Heb 8:23 | NRSVue notes at 9:1, 9:2. Copenhagen agrees |
| Isaiah | [[Isaiah 63\|Isaiah 63]] | 19 / 19 | Heb 63:19 = NRSVue 63:19–64:1 | NRSVue note at 64:2 (= Heb 64:1), so NRSVue 64:1 has no Hebrew number; it is the second half of Heb 63:19 (the JPS 63:19 ends "If You would but tear open the heavens and come down"). Copenhagen leaves 64:1 = Heb 64:1 |
| Isaiah | [[Isaiah 64\|Isaiah 64]] | 11 / 12 | Heb 64:1–11 = NRSVue 64:2–12; Heb 63:19 = NRSVue 63:19–64:1 | NRSVue note at 64:2 (= Heb 64:1), so NRSVue 64:1 has no Hebrew number; it is the second half of Heb 63:19 (the JPS 63:19 ends "If You would but tear open the heavens and come down"). Copenhagen leaves 64:1 = Heb 64:1 |
| Jeremiah | [[Jeremiah 08\|Jeremiah 8]] | 23 / 22 | Heb 8:23 = NRSVue 9:1 | NRSVue note at 9:1. Copenhagen agrees |
| Jeremiah | [[Jeremiah 09\|Jeremiah 9]] | 25 / 26 | Heb 9:1–25 = NRSVue 9:2–26; NRSVue 9:1 = Heb 8:23 | NRSVue notes at 9:1, 9:2. Copenhagen agrees |
| Ezekiel | [[Ezekiel 20\|Ezekiel 20]] | 44 / 49 | NRSVue 20:45–49 = Heb 21:1–5 | NRSVue note at 20:45. Copenhagen agrees |
| Ezekiel | [[Ezekiel 21\|Ezekiel 21]] | 37 / 32 | Heb 21:1–5 = NRSVue 20:45–49; Heb 21:6–37 = NRSVue 21:1–32 | NRSVue notes at 20:45, 21:1. Copenhagen agrees |
| Daniel | [[Daniel 03\|Daniel 3]] | 33 / 30 | Heb 3:31–33 = NRSVue 4:1–3 | No NRSVue note. Copenhagen, confirmed by the counts |
| Daniel | [[Daniel 04\|Daniel 4]] | 34 / 37 | Heb 4:1–34 = NRSVue 4:4–37; NRSVue 4:1–3 = Heb 3:31–33 | No NRSVue note. Copenhagen, confirmed by the counts |
| Daniel | [[Daniel 05\|Daniel 5]] | 30 / 31 | NRSVue 5:31 = Heb 6:1 | No NRSVue note. Copenhagen, confirmed by the counts |
| Daniel | [[Daniel 06\|Daniel 6]] | 29 / 28 | Heb 6:1 = NRSVue 5:31; Heb 6:2–29 = NRSVue 6:1–28 | No NRSVue note. Copenhagen, confirmed by the counts |
| Hosea | [[Hosea 01\|Hosea 1]] | 9 / 11 | NRSVue 1:10–11 = Heb 2:1–2 | NRSVue note at 1:10. Copenhagen agrees |
| Hosea | [[Hosea 02\|Hosea 2]] | 25 / 23 | Heb 2:1–2 = NRSVue 1:10–11; Heb 2:3–25 = NRSVue 2:1–23 | NRSVue notes at 1:10, 2:1. Copenhagen agrees |
| Hosea | [[Hosea 11\|Hosea 11]] | 11 / 12 | NRSVue 11:12 = Heb 12:1 | NRSVue note at 11:12. Copenhagen agrees |
| Hosea | [[Hosea 12\|Hosea 12]] | 15 / 14 | Heb 12:1 = NRSVue 11:12; Heb 12:2–15 = NRSVue 12:1–14 | NRSVue note at 11:12, carried on into NRSVue 12 (no note there). Copenhagen agrees |
| Hosea | [[Hosea 13\|Hosea 13]] | 15 / 16 | NRSVue 13:16 = Heb 14:1 | NRSVue note at 13:16. Copenhagen agrees |
| Hosea | [[Hosea 14\|Hosea 14]] | 10 / 9 | Heb 14:1 = NRSVue 13:16; Heb 14:2–10 = NRSVue 14:1–9 | NRSVue note at 13:16, carried on into NRSVue 14 (no note there). Copenhagen agrees |
| Joel | [[Joel 2\|Joel 2]] | 27 / 32 | NRSVue 2:28–32 = Heb 3:1–5 | NRSVue note at 2:28. Copenhagen agrees |
| Joel | [[Joel 3\|Joel 3]] | 5 / 21 | Heb 3:1–5 = NRSVue 2:28–32 | NRSVue note at 2:28. Copenhagen agrees |
| Joel | [[Joel 4\|Joel 4]] | 21 / – | Heb 4:1–21 = NRSVue 3:1–21 | NRSVue note at 3:1. Copenhagen agrees |
| Jonah | [[Jonah 1\|Jonah 1]] | 16 / 17 | NRSVue 1:17 = Heb 2:1 | NRSVue note at 1:17. Copenhagen agrees |
| Jonah | [[Jonah 2\|Jonah 2]] | 11 / 10 | Heb 2:1 = NRSVue 1:17; Heb 2:2–11 = NRSVue 2:1–10 | NRSVue note at 1:17, carried on into NRSVue 2 (no note there). Copenhagen agrees |
| Micah | [[Micah 4\|Micah 4]] | 14 / 13 | Heb 4:14 = NRSVue 5:1 | NRSVue note at 5:1. Copenhagen agrees |
| Micah | [[Micah 5\|Micah 5]] | 14 / 15 | Heb 5:1–14 = NRSVue 5:2–15; NRSVue 5:1 = Heb 4:14 | NRSVue notes at 5:1, 5:2. Copenhagen agrees |
| Nahum | [[Nahum 1\|Nahum 1]] | 14 / 15 | NRSVue 1:15 = Heb 2:1 | NRSVue note at 1:15. Copenhagen agrees |
| Nahum | [[Nahum 2\|Nahum 2]] | 14 / 13 | Heb 2:1 = NRSVue 1:15; Heb 2:2–14 = NRSVue 2:1–13 | NRSVue note at 1:15, carried on into NRSVue 2 (no note there). Copenhagen agrees |
| Zechariah | [[Zechariah 01\|Zechariah 1]] | 17 / 21 | NRSVue 1:18–21 = Heb 2:1–4 | NRSVue note at 1:18. Copenhagen agrees |
| Zechariah | [[Zechariah 02\|Zechariah 2]] | 17 / 13 | Heb 2:1–4 = NRSVue 1:18–21; Heb 2:5–17 = NRSVue 2:1–13 | NRSVue notes at 1:18, 2:1. Copenhagen agrees |
| Malachi | [[Malachi 3\|Malachi 3]] | 24 / 18 | Heb 3:19–24 = NRSVue 4:1–6 | NRSVue note at 4:1. Copenhagen agrees |

## Psalms

The NRSVue sets each superscription in italics, unnumbered, before verse 1, and has no "in Heb" notes in the Psalms. The JPS counts a superscription as a verse. Where the superscription is a verse of its own in the Hebrew (one verse; two in Psalms 51, 52, 54 and 60), every NRSVue verse number is one (two) lower than the JPS number. Where the superscription is only the start of the Hebrew verse 1 (for example Psalm 23, "A psalm of David. The LORD is my shepherd"), and in psalms without one, the numbers are the same. Psalm 13 is the one exception to the rule of the counts: both texts have six verses, but NRSVue 13:5–6 are the one Hebrew verse 13:6. The rows are Copenhagen's; the counts agree with them in every psalm.

| Psalm | Superscription (Heb) | Hebrew = NRSVue | Verses JPS / NRSVue |
|---|---|---|---|
| [[Psalms 003\|Psalm 3]] | 3:1 | Heb 3:2–9 = NRSVue 3:1–8 | 9 / 8 |
| [[Psalms 004\|Psalm 4]] | 4:1 | Heb 4:2–9 = NRSVue 4:1–8 | 9 / 8 |
| [[Psalms 005\|Psalm 5]] | 5:1 | Heb 5:2–13 = NRSVue 5:1–12 | 13 / 12 |
| [[Psalms 006\|Psalm 6]] | 6:1 | Heb 6:2–11 = NRSVue 6:1–10 | 11 / 10 |
| [[Psalms 007\|Psalm 7]] | 7:1 | Heb 7:2–18 = NRSVue 7:1–17 | 18 / 17 |
| [[Psalms 008\|Psalm 8]] | 8:1 | Heb 8:2–10 = NRSVue 8:1–9 | 10 / 9 |
| [[Psalms 009\|Psalm 9]] | 9:1 | Heb 9:2–21 = NRSVue 9:1–20 | 21 / 20 |
| [[Psalms 012\|Psalm 12]] | 12:1 | Heb 12:2–9 = NRSVue 12:1–8 | 9 / 8 |
| [[Psalms 013\|Psalm 13]] | 13:1 | Heb 13:2–5 = NRSVue 13:1–4; Heb 13:6 = NRSVue 13:5–6 | 6 / 6 |
| [[Psalms 018\|Psalm 18]] | 18:1 | Heb 18:2–51 = NRSVue 18:1–50 | 51 / 50 |
| [[Psalms 019\|Psalm 19]] | 19:1 | Heb 19:2–15 = NRSVue 19:1–14 | 15 / 14 |
| [[Psalms 020\|Psalm 20]] | 20:1 | Heb 20:2–10 = NRSVue 20:1–9 | 10 / 9 |
| [[Psalms 021\|Psalm 21]] | 21:1 | Heb 21:2–14 = NRSVue 21:1–13 | 14 / 13 |
| [[Psalms 022\|Psalm 22]] | 22:1 | Heb 22:2–32 = NRSVue 22:1–31 | 32 / 31 |
| [[Psalms 030\|Psalm 30]] | 30:1 | Heb 30:2–13 = NRSVue 30:1–12 | 13 / 12 |
| [[Psalms 031\|Psalm 31]] | 31:1 | Heb 31:2–25 = NRSVue 31:1–24 | 25 / 24 |
| [[Psalms 034\|Psalm 34]] | 34:1 | Heb 34:2–23 = NRSVue 34:1–22 | 23 / 22 |
| [[Psalms 036\|Psalm 36]] | 36:1 | Heb 36:2–13 = NRSVue 36:1–12 | 13 / 12 |
| [[Psalms 038\|Psalm 38]] | 38:1 | Heb 38:2–23 = NRSVue 38:1–22 | 23 / 22 |
| [[Psalms 039\|Psalm 39]] | 39:1 | Heb 39:2–14 = NRSVue 39:1–13 | 14 / 13 |
| [[Psalms 040\|Psalm 40]] | 40:1 | Heb 40:2–18 = NRSVue 40:1–17 | 18 / 17 |
| [[Psalms 041\|Psalm 41]] | 41:1 | Heb 41:2–14 = NRSVue 41:1–13 | 14 / 13 |
| [[Psalms 042\|Psalm 42]] | 42:1 | Heb 42:2–12 = NRSVue 42:1–11 | 12 / 11 |
| [[Psalms 044\|Psalm 44]] | 44:1 | Heb 44:2–27 = NRSVue 44:1–26 | 27 / 26 |
| [[Psalms 045\|Psalm 45]] | 45:1 | Heb 45:2–18 = NRSVue 45:1–17 | 18 / 17 |
| [[Psalms 046\|Psalm 46]] | 46:1 | Heb 46:2–12 = NRSVue 46:1–11 | 12 / 11 |
| [[Psalms 047\|Psalm 47]] | 47:1 | Heb 47:2–10 = NRSVue 47:1–9 | 10 / 9 |
| [[Psalms 048\|Psalm 48]] | 48:1 | Heb 48:2–15 = NRSVue 48:1–14 | 15 / 14 |
| [[Psalms 049\|Psalm 49]] | 49:1 | Heb 49:2–21 = NRSVue 49:1–20 | 21 / 20 |
| [[Psalms 051\|Psalm 51]] | 51:1–2 | Heb 51:3–21 = NRSVue 51:1–19 | 21 / 19 |
| [[Psalms 052\|Psalm 52]] | 52:1–2 | Heb 52:3–11 = NRSVue 52:1–9 | 11 / 9 |
| [[Psalms 053\|Psalm 53]] | 53:1 | Heb 53:2–7 = NRSVue 53:1–6 | 7 / 6 |
| [[Psalms 054\|Psalm 54]] | 54:1–2 | Heb 54:3–9 = NRSVue 54:1–7 | 9 / 7 |
| [[Psalms 055\|Psalm 55]] | 55:1 | Heb 55:2–24 = NRSVue 55:1–23 | 24 / 23 |
| [[Psalms 056\|Psalm 56]] | 56:1 | Heb 56:2–14 = NRSVue 56:1–13 | 14 / 13 |
| [[Psalms 057\|Psalm 57]] | 57:1 | Heb 57:2–12 = NRSVue 57:1–11 | 12 / 11 |
| [[Psalms 058\|Psalm 58]] | 58:1 | Heb 58:2–12 = NRSVue 58:1–11 | 12 / 11 |
| [[Psalms 059\|Psalm 59]] | 59:1 | Heb 59:2–18 = NRSVue 59:1–17 | 18 / 17 |
| [[Psalms 060\|Psalm 60]] | 60:1–2 | Heb 60:3–14 = NRSVue 60:1–12 | 14 / 12 |
| [[Psalms 061\|Psalm 61]] | 61:1 | Heb 61:2–9 = NRSVue 61:1–8 | 9 / 8 |
| [[Psalms 062\|Psalm 62]] | 62:1 | Heb 62:2–13 = NRSVue 62:1–12 | 13 / 12 |
| [[Psalms 063\|Psalm 63]] | 63:1 | Heb 63:2–12 = NRSVue 63:1–11 | 12 / 11 |
| [[Psalms 064\|Psalm 64]] | 64:1 | Heb 64:2–11 = NRSVue 64:1–10 | 11 / 10 |
| [[Psalms 065\|Psalm 65]] | 65:1 | Heb 65:2–14 = NRSVue 65:1–13 | 14 / 13 |
| [[Psalms 067\|Psalm 67]] | 67:1 | Heb 67:2–8 = NRSVue 67:1–7 | 8 / 7 |
| [[Psalms 068\|Psalm 68]] | 68:1 | Heb 68:2–36 = NRSVue 68:1–35 | 36 / 35 |
| [[Psalms 069\|Psalm 69]] | 69:1 | Heb 69:2–37 = NRSVue 69:1–36 | 37 / 36 |
| [[Psalms 070\|Psalm 70]] | 70:1 | Heb 70:2–6 = NRSVue 70:1–5 | 6 / 5 |
| [[Psalms 075\|Psalm 75]] | 75:1 | Heb 75:2–11 = NRSVue 75:1–10 | 11 / 10 |
| [[Psalms 076\|Psalm 76]] | 76:1 | Heb 76:2–13 = NRSVue 76:1–12 | 13 / 12 |
| [[Psalms 077\|Psalm 77]] | 77:1 | Heb 77:2–21 = NRSVue 77:1–20 | 21 / 20 |
| [[Psalms 080\|Psalm 80]] | 80:1 | Heb 80:2–20 = NRSVue 80:1–19 | 20 / 19 |
| [[Psalms 081\|Psalm 81]] | 81:1 | Heb 81:2–17 = NRSVue 81:1–16 | 17 / 16 |
| [[Psalms 083\|Psalm 83]] | 83:1 | Heb 83:2–19 = NRSVue 83:1–18 | 19 / 18 |
| [[Psalms 084\|Psalm 84]] | 84:1 | Heb 84:2–13 = NRSVue 84:1–12 | 13 / 12 |
| [[Psalms 085\|Psalm 85]] | 85:1 | Heb 85:2–14 = NRSVue 85:1–13 | 14 / 13 |
| [[Psalms 088\|Psalm 88]] | 88:1 | Heb 88:2–19 = NRSVue 88:1–18 | 19 / 18 |
| [[Psalms 089\|Psalm 89]] | 89:1 | Heb 89:2–53 = NRSVue 89:1–52 | 53 / 52 |
| [[Psalms 092\|Psalm 92]] | 92:1 | Heb 92:2–16 = NRSVue 92:1–15 | 16 / 15 |
| [[Psalms 102\|Psalm 102]] | 102:1 | Heb 102:2–29 = NRSVue 102:1–28 | 29 / 28 |
| [[Psalms 108\|Psalm 108]] | 108:1 | Heb 108:2–14 = NRSVue 108:1–13 | 14 / 13 |
| [[Psalms 140\|Psalm 140]] | 140:1 | Heb 140:2–14 = NRSVue 140:1–13 | 14 / 13 |
| [[Psalms 142\|Psalm 142]] | 142:1 | Heb 142:2–8 = NRSVue 142:1–7 | 8 / 7 |
