# Track 2 – links: full change list (batch 2)

For the section *Track 2 – links* in "Phase 3 – decisions, batch 2". Built on 7 Oct 2026 from the notes snapshot of 04:08 UTC. Nothing here is applied yet.

## Counts

- **Ready to apply: 398 links in 100 notes.**
  - Tikkunei Zohar → Tanakh and Torah: 372 links in 89 notes. That is the draft's 370 plus the checker's 2 chapter links (`Psalm 121`, `Psalm 118`). Prophets 262, Writings 108, Torah 2. `(Ex. 28)` opens 28:1 by the Guide's Chapters rule (your M7 answer), although the words quoted after it are 28:7.
  - By form: Is. 136, Ez. 81, Song. 72, Ecc. 25, Jon. 23, 1 King. 12, 1 Chron. 6, Ḥab. 3, Naḥ. 2, 2 King. 2, Tzeph. 2, Psalm 2, Rut. 1, Ez (no period) 1, Song, (comma) 1, Ex. 2, 2 Chron. 1.
  - BCP Apocrypha lessons → LXX (Brenton): 26 links in 11 notes (Ecclesiasticus 12, Wisdom 11, Tobit 1, Judith 1, Baruch 1).
- **Ops:** `/home/claude/p3/batch2/t2-ready-ops.json`, 100 `lines` ops. Their `oldSha` is the 04:08 snapshot. No overnight change touched these 100 notes, and none of them links to the renamed Zohar 8.03/8.04, so they apply as built. Apply the BCP ops before track 7's G26 ops (two notes are shared).
- **Checks run on the ready ops (script, against the snapshot):** each `old` occurs once in its line; the line with the new link markup removed equals the original; every target's base name is unique in the vault; every `^c-v` id is in its target note. 0 problems.
- **Edits that depend on your answers:** `/home/claude/p3/batch2/t2-question-edits.json`, listed below by question. The Tikkunei one (L5) is built on the same snapshot and is merged into the ready op for the same note. The BCP ones (L6, L7) are separate ops, applied after the ready BCP ops: L7 (psalms) first, then L6 (Judith and Ecclesiastes). The Tanya and Mei HaShiloach ones (L1–L4) must be rebuilt against the notes as they are now, because those notes gained links overnight; they go in before track 7's nav lines (G19), which touch the same notes.

## Ready: Tikkunei Zohar (372)

Source: `drafts/t2/tik` (row id and the drafter's quotation check); "checker" = the 2 chapter links the checker added.

| Note | Line | Before → after | Source |
|---|---|---|---|
| Tikkunei Zohar 017a | 183 | `Is. 46:10` → `[[Isaiah 46#^46-10\|Is. 46:10]]` | TZ001; read by hand: match |
| Tikkunei Zohar 017b | 109 | `1 Chron. 29:11` → `[[I Chronicles 29#^29-11\|1 Chron. 29:11]]` | TZ002; matches (1.00) |
| Tikkunei Zohar 017b | 122 | `Is. 26:19` → `[[Isaiah 26#^26-19\|Is. 26:19]]` | TZ003; read by hand: match |
| Tikkunei Zohar 017b | 125 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ004; read by hand: match |
| Tikkunei Zohar 017b | 127 | `Is. 26:19` → `[[Isaiah 26#^26-19\|Is. 26:19]]` | TZ005; read by hand: match |
| Tikkunei Zohar 017b | 152 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ006; read by hand: match |
| Tikkunei Zohar 017b | 172 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ007; read by hand: match |
| Tikkunei Zohar 018a | 44 | `Ez. 1:10` → `[[Ezekiel 01#^1-10\|Ez. 1:10]]` | TZ008; matches (0.38) |
| Tikkunei Zohar 018a | 70 | `Song. 8:6` → `[[Song of Songs 8#^8-6\|Song. 8:6]]` | TZ009; matches (0.67) |
| Tikkunei Zohar 018a | 144 | `Naḥ. 1:2` → `[[Nahum 1#^1-2\|Naḥ. 1:2]]` | TZ010; matches (0.50) |
| Tikkunei Zohar 018a | 151 | `Song. 8:6` → `[[Song of Songs 8#^8-6\|Song. 8:6]]` | TZ011; read by hand: match |
| Tikkunei Zohar 018a | 160 | `Song. 8:6` → `[[Song of Songs 8#^8-6\|Song. 8:6]]` | TZ012; matches (0.67) |
| Tikkunei Zohar 018a | 192 | `Is. 33:6` → `[[Isaiah 33#^33-6\|Is. 33:6]]` | TZ013; matches (0.50) |
| Tikkunei Zohar 018b | 91 | `Is. 56:7` → `[[Isaiah 56#^56-7\|Is. 56:7]]` | TZ014; matches (0.75) |
| Tikkunei Zohar 018b | 118 | `Is. 44:13` → `[[Isaiah 44#^44-13\|Is. 44:13]]` | TZ015; matches (0.50) |
| Tikkunei Zohar 018b | 172 | `Is. 27:1` → `[[Isaiah 27#^27-1\|Is. 27:1]]` | TZ016; read by hand: match |
| Tikkunei Zohar 018b | 173 | `Rut. 1:17` → `[[Ruth 1#^1-17\|Rut. 1:17]]` | TZ017; read by hand: match |
| Tikkunei Zohar 019a | 170 | `Is. 9:6` → `[[Isaiah 09#^9-6\|Is. 9:6]]` | TZ018; read by hand: match |
| Tikkunei Zohar 019a | 230 | `Is. 40:12` → `[[Isaiah 40#^40-12\|Is. 40:12]]` | TZ019; matches (0.44) |
| Tikkunei Zohar 019b | 125 | `Ez. 1:22` → `[[Ezekiel 01#^1-22\|Ez. 1:22]]` | TZ020; read by hand: match |
| Tikkunei Zohar 019b | 127 | `Ez. 1:22` → `[[Ezekiel 01#^1-22\|Ez. 1:22]]` | TZ021; matches (0.40) |
| Tikkunei Zohar 019b | 150 | `Ez. 10:20` → `[[Ezekiel 10#^10-20\|Ez. 10:20]]` | TZ022; read by hand: match |
| Tikkunei Zohar 019b | 170 | `Is. 62:3` → `[[Isaiah 62#^62-3\|Is. 62:3]]` | TZ023; read by hand: match |
| Tikkunei Zohar 019b | 264 | `Is. 30:26` → `[[Isaiah 30#^30-26\|Is. 30:26]]` | TZ024; matches (1.00) |
| Tikkunei Zohar 020a | 92 | `Ez. 3:12` → `[[Ezekiel 03#^3-12\|Ez. 3:12]]` | TZ025; matches (0.67) |
| Tikkunei Zohar 020a | 179 | `1 Chron. 29:11` → `[[I Chronicles 29#^29-11\|1 Chron. 29:11]]` | TZ026; read by hand: match |
| Tikkunei Zohar 020a | 191 | `Ecc. 10:20` → `[[Ecclesiastes 10#^10-20\|Ecc. 10:20]]` | TZ027; read by hand: match |
| Tikkunei Zohar 020b | 81 | `Is. 44:6` → `[[Isaiah 44#^44-6\|Is. 44:6]]` | TZ028; matches (0.67) |
| Tikkunei Zohar 020b | 93 | `Ez. 1:16` → `[[Ezekiel 01#^1-16\|Ez. 1:16]]` | TZ029; read by hand: match |
| Tikkunei Zohar 020b | 107 | `Ez. 1:15` → `[[Ezekiel 01#^1-15\|Ez. 1:15]]` | TZ030; read by hand: match |
| Tikkunei Zohar 020b | 224 | `Ez. 1:11` → `[[Ezekiel 01#^1-11\|Ez. 1:11]]` | TZ032; read by hand: match |
| Tikkunei Zohar 020b | 241 | `Ez. 1:22` → `[[Ezekiel 01#^1-22\|Ez. 1:22]]` | TZ033; read by hand: match |
| Tikkunei Zohar 020b | 259 | `Ez. 1:14` → `[[Ezekiel 01#^1-14\|Ez. 1:14]]` | TZ034; read by hand: match |
| Tikkunei Zohar 021a | 35 | `Is. 33:7` → `[[Isaiah 33#^33-7\|Is. 33:7]]` | TZ035; read by hand: match |
| Tikkunei Zohar 021a | 166 | `Naḥ. 1:2` → `[[Nahum 1#^1-2\|Naḥ. 1:2]]` | TZ036; read by hand: match |
| Tikkunei Zohar 021b | 25 | `Ez. 1:6` → `[[Ezekiel 01#^1-6\|Ez. 1:6]]` | TZ037; matches (1.00) |
| Tikkunei Zohar 021b | 175 | `Is. 50:1` → `[[Isaiah 50#^50-1\|Is. 50:1]]` | TZ038; read by hand: match |
| Tikkunei Zohar 021b | 198 | `Is. 42:8` → `[[Isaiah 42#^42-8\|Is. 42:8]]` | TZ039; read by hand: match |
| Tikkunei Zohar 021b | 208 | `Song. 7:6` → `[[Song of Songs 7#^7-6\|Song. 7:6]]` | TZ040; read by hand: match |
| Tikkunei Zohar 021b | 217 | `Ez. 24:17` → `[[Ezekiel 24#^24-17\|Ez. 24:17]]` | TZ041; read by hand: match |
| Tikkunei Zohar 021b | 236 | `Song. 1:13` → `[[Song of Songs 1#^1-13\|Song. 1:13]]` | TZ042; matches (0.83) |
| Tikkunei Zohar 022a | 43 | `Song. 6:1` → `[[Song of Songs 6#^6-1\|Song. 6:1]]` | TZ043; read by hand: match |
| Tikkunei Zohar 022a | 44 | `Song. 8:14` → `[[Song of Songs 8#^8-14\|Song. 8:14]]` | TZ044; read by hand: match |
| Tikkunei Zohar 022a | 45 | `Song. 6:1` → `[[Song of Songs 6#^6-1\|Song. 6:1]]` | TZ045; matches (0.40) |
| Tikkunei Zohar 022a | 68 | `Ez. 46:1` → `[[Ezekiel 46#^46-1\|Ez. 46:1]]` | TZ046; matches (0.78) |
| Tikkunei Zohar 022a | 129 | `Song. 2:9` → `[[Song of Songs 2#^2-9\|Song. 2:9]]` | TZ047; read by hand: match |
| Tikkunei Zohar 022a | 169 | `Song. 2:9` → `[[Song of Songs 2#^2-9\|Song. 2:9]]` | TZ048; read by hand: match |
| Tikkunei Zohar 022a | 178 | `Song. 2:9` → `[[Song of Songs 2#^2-9\|Song. 2:9]]` | TZ049; matches (0.50) |
| Tikkunei Zohar 022a | 195 | `Is. 49:9` → `[[Isaiah 49#^49-9\|Is. 49:9]]` | TZ050; read by hand: match |
| Tikkunei Zohar 022a | 208 | `Is. 56:11` → `[[Isaiah 56#^56-11\|Is. 56:11]]` | TZ051; read by hand: match |
| Tikkunei Zohar 022b | 107 | `Is. 52:8` → `[[Isaiah 52#^52-8\|Is. 52:8]]` | TZ052; matches (0.80) |
| Tikkunei Zohar 023a | 62 | `Is. 4:1` → `[[Isaiah 04#^4-1\|Is. 4:1]]` | TZ053; matches (0.75) |
| Tikkunei Zohar 023a | 141 | `Ez. 1:15` → `[[Ezekiel 01#^1-15\|Ez. 1:15]]` | TZ054; read by hand: match |
| Tikkunei Zohar 023a | 151 | `Ez. 1:5` → `[[Ezekiel 01#^1-5\|Ez. 1:5]]` | TZ055; matches (0.50) |
| Tikkunei Zohar 023a | 248 | `Is. 48:11` → `[[Isaiah 48#^48-11\|Is. 48:11]]` | TZ056; read by hand: match |
| Tikkunei Zohar 023a | 249 | `Ez. 20:14` → `[[Ezekiel 20#^20-14\|Ez. 20:14]]` | TZ057; read by hand: match |
| Tikkunei Zohar 023b | 179 | `Is. 50:1` → `[[Isaiah 50#^50-1\|Is. 50:1]]` | TZ058; matches (0.40) |
| Tikkunei Zohar 024a | 113 | `1 King. 8:32` → `[[I Kings 08#^8-32\|1 King. 8:32]]` | TZ059; matches (1.00) |
| Tikkunei Zohar 024a | 149 | `Is. 24:23` → `[[Isaiah 24#^24-23\|Is. 24:23]]` | TZ060; read by hand: match |
| Tikkunei Zohar 024a | 167 | `Is. 24:23` → `[[Isaiah 24#^24-23\|Is. 24:23]]` | TZ061; matches (0.75) |
| Tikkunei Zohar 024a | 207 | `Is. 30:26` → `[[Isaiah 30#^30-26\|Is. 30:26]]` | TZ062; matches (1.00) |
| Tikkunei Zohar 024a | 216 | `Is. 24:23` → `[[Isaiah 24#^24-23\|Is. 24:23]]` | TZ063; read by hand: match |
| Tikkunei Zohar 024a | 222 | `Is. 51:6` → `[[Isaiah 51#^51-6\|Is. 51:6]]` | TZ064; matches (0.50) |
| Tikkunei Zohar 024b | 101 | `Song. 1:1` → `[[Song of Songs 1#^1-1\|Song. 1:1]]` | TZ065; read by hand: match |
| Tikkunei Zohar 024b | 128 | `1 King. 5:10` → `[[I Kings 05#^5-10\|1 King. 5:10]]` | TZ066; matches (0.38) |
| Tikkunei Zohar 024b | 130 | `Is. 11:9` → `[[Isaiah 11#^11-9\|Is. 11:9]]` | TZ067; read by hand: match |
| Tikkunei Zohar 024b | 184 | `Is. 6:3` → `[[Isaiah 06#^6-3\|Is. 6:3]]` | TZ068; read by hand: match |
| Tikkunei Zohar 024b | 197 | `Ez. 3:12` → `[[Ezekiel 03#^3-12\|Ez. 3:12]]` | TZ069; matches (0.67) |
| Tikkunei Zohar 025a | 39 | `Is. 46:10` → `[[Isaiah 46#^46-10\|Is. 46:10]]` | TZ070; matches (0.67) |
| Tikkunei Zohar 025a | 55 | `Ez. 1:24` → `[[Ezekiel 01#^1-24\|Ez. 1:24]]` | TZ071; matches (0.67) |
| Tikkunei Zohar 025a | 101 | `Ez 1:24` → `[[Ezekiel 01#^1-24\|Ez 1:24]]` | TZ072; read by hand: match |
| Tikkunei Zohar 025a | 234 | `Ez. 1:24` → `[[Ezekiel 01#^1-24\|Ez. 1:24]]` | TZ073; read by hand: match |
| Tikkunei Zohar 025b | 44 | `Song. 1:2` → `[[Song of Songs 1#^1-2\|Song. 1:2]]` | TZ074; read by hand: match |
| Tikkunei Zohar 025b | 48 | `Ez. 1:6` → `[[Ezekiel 01#^1-6\|Ez. 1:6]]` | TZ075; matches (1.00) |
| Tikkunei Zohar 025b | 102 | `Ez. 1:10` → `[[Ezekiel 01#^1-10\|Ez. 1:10]]` | TZ076; matches (0.40) |
| Tikkunei Zohar 025b | 145 | `Ecc. 10:20` → `[[Ecclesiastes 10#^10-20\|Ecc. 10:20]]` | TZ077; read by hand: match |
| Tikkunei Zohar 025b | 185 | `Ez. 1:5` → `[[Ezekiel 01#^1-5\|Ez. 1:5]]` | TZ078; read by hand: match |
| Tikkunei Zohar 025b | 271 | `Is. 16:5` → `[[Isaiah 16#^16-5\|Is. 16:5]]` | TZ079; read by hand: match |
| Tikkunei Zohar 026a | 46 | `Is. 6:2` → `[[Isaiah 06#^6-2\|Is. 6:2]]` | TZ080; matches (0.40) |
| Tikkunei Zohar 026a | 94 | `Ez. 1:24` → `[[Ezekiel 01#^1-24\|Ez. 1:24]]` | TZ081; matches (0.67) |
| Tikkunei Zohar 026b | 64 | `Is. 33:7` → `[[Isaiah 33#^33-7\|Is. 33:7]]` | TZ082; read by hand: match |
| Tikkunei Zohar 026b | 137 | `2 King. 3:15` → `[[II Kings 03#^3-15\|2 King. 3:15]]` | TZ083; matches (1.00) |
| Tikkunei Zohar 026b | 197 | `Is. 57:1` → `[[Isaiah 57#^57-1\|Is. 57:1]]` | TZ084; read by hand: match |
| Tikkunei Zohar 026b | 200 | `Is. 19:5` → `[[Isaiah 19#^19-5\|Is. 19:5]]` | TZ085; read by hand: match |
| Tikkunei Zohar 027a | 179 | `Is. 54:7` → `[[Isaiah 54#^54-7\|Is. 54:7]]` | TZ086; read by hand: match |
| Tikkunei Zohar 027a | 194 | `Is. 6:3` → `[[Isaiah 06#^6-3\|Is. 6:3]]` | TZ087; read by hand: match |
| Tikkunei Zohar 027a | 217 | `Ez. 44:30` → `[[Ezekiel 44#^44-30\|Ez. 44:30]]` | TZ088; matches (0.50) |
| Tikkunei Zohar 027b | 25 | `Song. 7:6` → `[[Song of Songs 7#^7-6\|Song. 7:6]]` | TZ089; matches (0.50) |
| Tikkunei Zohar 027b | 117 | `Psalm 121` → `[[Psalms 121#^121-1\|Psalm 121]]` | checker; checker: Chapters rule |
| Tikkunei Zohar 027b | 134 | `Is. 10:30` → `[[Isaiah 10#^10-30\|Is. 10:30]]` | TZ090; read by hand: match |
| Tikkunei Zohar 027b | 154 | `Song. 5:14` → `[[Song of Songs 5#^5-14\|Song. 5:14]]` | TZ091; read by hand: match |
| Tikkunei Zohar 027b | 157 | `1 King. 10:19` → `[[I Kings 10#^10-19\|1 King. 10:19]]` | TZ092; matches (0.67) |
| Tikkunei Zohar 027b | 171 | `Is. 6:2` → `[[Isaiah 06#^6-2\|Is. 6:2]]` | TZ093; read by hand: match |
| Tikkunei Zohar 027b | 175 | `Ecc. 10:20` → `[[Ecclesiastes 10#^10-20\|Ecc. 10:20]]` | TZ094; matches (0.50) |
| Tikkunei Zohar 027b | 186 | `Song. 2:6` → `[[Song of Songs 2#^2-6\|Song. 2:6]]` | TZ095; matches (0.83) |
| Tikkunei Zohar 027b | 206 | `Song. 5:15` → `[[Song of Songs 5#^5-15\|Song. 5:15]]` | TZ096; matches (0.50) |
| Tikkunei Zohar 028a | 25 | `Song. 3:7` → `[[Song of Songs 3#^3-7\|Song. 3:7]]` | TZ097; matches (0.36) |
| Tikkunei Zohar 028a | 28 | `Song. 6:8` → `[[Song of Songs 6#^6-8\|Song. 6:8]]` | TZ098; matches (1.00) |
| Tikkunei Zohar 028a | 75 | `Ez. 1:10` → `[[Ezekiel 01#^1-10\|Ez. 1:10]]` | TZ099; matches (0.54) |
| Tikkunei Zohar 028a | 99 | `Song. 4:3` → `[[Song of Songs 4#^4-3\|Song. 4:3]]` | TZ100; read by hand: match |
| Tikkunei Zohar 028a | 148 | `Is. 40:25` → `[[Isaiah 40#^40-25\|Is. 40:25]]` | TZ101; read by hand: match |
| Tikkunei Zohar 028a | 182 | `Ez. 1:12` → `[[Ezekiel 01#^1-12\|Ez. 1:12]]` | TZ102; read by hand: match |
| Tikkunei Zohar 028a | 236 | `Is. 53:1` → `[[Isaiah 53#^53-1\|Is. 53:1]]` | TZ103; matches (1.00) |
| Tikkunei Zohar 028a | 244 | `Is. 62:8` → `[[Isaiah 62#^62-8\|Is. 62:8]]` | TZ104; read by hand: match |
| Tikkunei Zohar 028a | 271 | `Is. 63:12` → `[[Isaiah 63#^63-12\|Is. 63:12]]` | TZ105; matches (0.38) |
| Tikkunei Zohar 028b | 28 | `Is. 53:1` → `[[Isaiah 53#^53-1\|Is. 53:1]]` | TZ106; matches (1.00) |
| Tikkunei Zohar 028b | 43 | `2 King. 3:15` → `[[II Kings 03#^3-15\|2 King. 3:15]]` | TZ107; matches (1.00) |
| Tikkunei Zohar 028b | 60 | `Is. 24:19` → `[[Isaiah 24#^24-19\|Is. 24:19]]` | TZ108; read by hand: match |
| Tikkunei Zohar 028b | 120 | `Ecc. 1:9` → `[[Ecclesiastes 01#^1-9\|Ecc. 1:9]]` | TZ109; read by hand: match |
| Tikkunei Zohar 028b | 204 | `Is. 30:26` → `[[Isaiah 30#^30-26\|Is. 30:26]]` | TZ110; matches (1.00) |
| Tikkunei Zohar 028b | 327 | `Is. 58:9` → `[[Isaiah 58#^58-9\|Is. 58:9]]` | TZ111; matches (0.67) |
| Tikkunei Zohar 029a | 185 | `Song. 4:7` → `[[Song of Songs 4#^4-7\|Song. 4:7]]` | TZ112; read by hand: match |
| Tikkunei Zohar 029a | 219 | `1 Chron. 29:11` → `[[I Chronicles 29#^29-11\|1 Chron. 29:11]]` | TZ113; read by hand: match |
| Tikkunei Zohar 029a | 263 | `Song. 7:9` → `[[Song of Songs 7#^7-9\|Song. 7:9]]` | TZ114; read by hand: match |
| Tikkunei Zohar 029b | 50 | `Is. 40:22` → `[[Isaiah 40#^40-22\|Is. 40:22]]` | TZ115; read by hand: match |
| Tikkunei Zohar 029b | 96 | `1 King. 5:12` → `[[I Kings 05#^5-12\|1 King. 5:12]]` | TZ116; read by hand: match |
| Tikkunei Zohar 030a | 90 | `Ez. 44:30` → `[[Ezekiel 44#^44-30\|Ez. 44:30]]` | TZ117; matches (1.00) |
| Tikkunei Zohar 030a | 105 | `Ez. 44:30` → `[[Ezekiel 44#^44-30\|Ez. 44:30]]` | TZ118; matches (1.00) |
| Tikkunei Zohar 030a | 138 | `Song. 4:15` → `[[Song of Songs 4#^4-15\|Song. 4:15]]` | TZ119; read by hand: match |
| Tikkunei Zohar 030b | 66 | `Is. 6:10` → `[[Isaiah 06#^6-10\|Is. 6:10]]` | TZ120; read by hand: match |
| Tikkunei Zohar 030b | 83 | `Ecc. 9:9` → `[[Ecclesiastes 09#^9-9\|Ecc. 9:9]]` | TZ121; read by hand: match |
| Tikkunei Zohar 031a | 129 | `Song. 8:7` → `[[Song of Songs 8#^8-7\|Song. 8:7]]` | TZ122; matches (0.40) |
| Tikkunei Zohar 031b | 53 | `Song. 5:15` → `[[Song of Songs 5#^5-15\|Song. 5:15]]` | TZ123; read by hand: match |
| Tikkunei Zohar 031b | 91 | `1 King. 10:19` → `[[I Kings 10#^10-19\|1 King. 10:19]]` | TZ124; read by hand: match |
| Tikkunei Zohar 031b | 136 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ125; read by hand: match |
| Tikkunei Zohar 032b | 69 | `Song. 7:6` → `[[Song of Songs 7#^7-6\|Song. 7:6]]` | TZ126; matches (0.50) |
| Tikkunei Zohar 032b | 115 | `Ez. 1:10` → `[[Ezekiel 01#^1-10\|Ez. 1:10]]` | TZ127; matches (0.43) |
| Tikkunei Zohar 032b | 142 | `Ecc. 10:20` → `[[Ecclesiastes 10#^10-20\|Ecc. 10:20]]` | TZ128; matches (0.38) |
| Tikkunei Zohar 032b | 162 | `Ez. 1:8` → `[[Ezekiel 01#^1-8\|Ez. 1:8]]` | TZ129; matches (0.50) |
| Tikkunei Zohar 032b | 172 | `Ez. 1:28` → `[[Ezekiel 01#^1-28\|Ez. 1:28]]` | TZ130; read by hand: match |
| Tikkunei Zohar 032b | 179 | `Ez. 1:7` → `[[Ezekiel 01#^1-7\|Ez. 1:7]]` | TZ131; read by hand: match |
| Tikkunei Zohar 033a | 84 | `Ez. 2:1` → `[[Ezekiel 02#^2-1\|Ez. 2:1]]` | TZ132; read by hand: match |
| Tikkunei Zohar 033a | 190 | `1 King. 2:45` → `[[I Kings 02#^2-45\|1 King. 2:45]]` | TZ133; read by hand: match |
| Tikkunei Zohar 033b | 32 | `Ez. 1:8` → `[[Ezekiel 01#^1-8\|Ez. 1:8]]` | TZ134; read by hand: match |
| Tikkunei Zohar 033b | 34 | `Is. 44:13` → `[[Isaiah 44#^44-13\|Is. 44:13]]` | TZ135; matches (0.50) |
| Tikkunei Zohar 033b | 68 | `Song. 2:14` → `[[Song of Songs 2#^2-14\|Song. 2:14]]` | TZ136; matches (0.57) |
| Tikkunei Zohar 033b | 113 | `Is. 1:12` → `[[Isaiah 01#^1-12\|Is. 1:12]]` | TZ137; matches (1.00) |
| Tikkunei Zohar 033b | 228 | `Is. 58:9` → `[[Isaiah 58#^58-9\|Is. 58:9]]` | TZ138; read by hand: match |
| Tikkunei Zohar 034a | 133 | `Song. 7:2` → `[[Song of Songs 7#^7-2\|Song. 7:2]]` | TZ140; read by hand: match |
| Tikkunei Zohar 034a | 156 | `Song. 7:2` → `[[Song of Songs 7#^7-2\|Song. 7:2]]` | TZ141; read by hand: match |
| Tikkunei Zohar 034a | 193 | `Ez. 46:1` → `[[Ezekiel 46#^46-1\|Ez. 46:1]]` | TZ142; matches (0.73) |
| Tikkunei Zohar 034b | 36 | `Is. 6:3` → `[[Isaiah 06#^6-3\|Is. 6:3]]` | TZ143; read by hand: match |
| Tikkunei Zohar 034b | 57 | `Is. 58:9` → `[[Isaiah 58#^58-9\|Is. 58:9]]` | TZ144; read by hand: match |
| Tikkunei Zohar 034b | 145 | `Song. 7:2–6` → `[[Song of Songs 7#^7-2\|Song. 7:2–6]]` | TZ145; matches (0.50) |
| Tikkunei Zohar 034b | 167 | `Song. 5:11–15` → `[[Song of Songs 5#^5-11\|Song. 5:11–15]]` | TZ146; matches (0.47) |
| Tikkunei Zohar 034b | 260 | `Ez. 2:1` → `[[Ezekiel 02#^2-1\|Ez. 2:1]]` | TZ147; matches (0.60) |
| Tikkunei Zohar 034b | 269 | `Ez. 1:7` → `[[Ezekiel 01#^1-7\|Ez. 1:7]]` | TZ148; matches (0.36) |
| Tikkunei Zohar 034b | 274 | `Ez. 1:17` → `[[Ezekiel 01#^1-17\|Ez. 1:17]]` | TZ149; matches (0.67) |
| Tikkunei Zohar 035a | 28 | `Ez. 2:1` → `[[Ezekiel 02#^2-1\|Ez. 2:1]]` | TZ150; matches (0.50) |
| Tikkunei Zohar 035a | 188 | `Is. 62:8` → `[[Isaiah 62#^62-8\|Is. 62:8]]` | TZ151; read by hand: match |
| Tikkunei Zohar 035b | 97 | `Ez. 1:7` → `[[Ezekiel 01#^1-7\|Ez. 1:7]]` | TZ153; read by hand: match |
| Tikkunei Zohar 035b | 101 | `Ez. 1:17` → `[[Ezekiel 01#^1-17\|Ez. 1:17]]` | TZ154; read by hand: match |
| Tikkunei Zohar 035b | 102 | `Ez. 1:14` → `[[Ezekiel 01#^1-14\|Ez. 1:14]]` | TZ155; read by hand: match |
| Tikkunei Zohar 035b | 122 | `Ez. 2:1` → `[[Ezekiel 02#^2-1\|Ez. 2:1]]` | TZ156; matches (0.67) |
| Tikkunei Zohar 035b | 131 | `Ez. 2:2` → `[[Ezekiel 02#^2-2\|Ez. 2:2]]` | TZ157; read by hand: match |
| Tikkunei Zohar 035b | 133 | `Ez. 3:12` → `[[Ezekiel 03#^3-12\|Ez. 3:12]]` | TZ158; read by hand: match |
| Tikkunei Zohar 035b | 136 | `Ez. 3:12` → `[[Ezekiel 03#^3-12\|Ez. 3:12]]` | TZ159; matches (1.00) |
| Tikkunei Zohar 035b | 145 | `Ez. 3:12` → `[[Ezekiel 03#^3-12\|Ez. 3:12]]` | TZ160; read by hand: match |
| Tikkunei Zohar 035b | 147 | `1 King. 19:11` → `[[I Kings 19#^19-11\|1 King. 19:11]]` | TZ161; read by hand: match |
| Tikkunei Zohar 035b | 193 | `Jon. 1:4` → `[[Jonah 1#^1-4\|Jon. 1:4]]` | TZ162; matches (0.50) |
| Tikkunei Zohar 035b | 205 | `Ez. 2:1` → `[[Ezekiel 02#^2-1\|Ez. 2:1]]` | TZ163; read by hand: match |
| Tikkunei Zohar 035b | 223 | `Song. 7:2` → `[[Song of Songs 7#^7-2\|Song. 7:2]]` | TZ164; matches (0.67) |
| Tikkunei Zohar 035b | 249 | `Song. 7:2` → `[[Song of Songs 7#^7-2\|Song. 7:2]]` | TZ165; matches (0.50) |
| Tikkunei Zohar 035b | 269 | `Song. 5:15` → `[[Song of Songs 5#^5-15\|Song. 5:15]]` | TZ166; read by hand: match |
| Tikkunei Zohar 035b | 279 | `1 King. 10:19` → `[[I Kings 10#^10-19\|1 King. 10:19]]` | TZ167; matches (0.50) |
| Tikkunei Zohar 036a | 148 | `Ez. 16:6` → `[[Ezekiel 16#^16-6\|Ez. 16:6]]` | TZ169; matches (1.00) |
| Tikkunei Zohar 036a | 175 | `Ez. 1:28` → `[[Ezekiel 01#^1-28\|Ez. 1:28]]` | TZ170; matches (0.53) |
| Tikkunei Zohar 036a | 204 | `Ez. 1:4` → `[[Ezekiel 01#^1-4\|Ez. 1:4]]` | TZ171; read by hand: match |
| Tikkunei Zohar 036b | 61 | `Ecc. 1:9` → `[[Ecclesiastes 01#^1-9\|Ecc. 1:9]]` | TZ172; read by hand: match |
| Tikkunei Zohar 036b | 81 | `Ez. 1:22` → `[[Ezekiel 01#^1-22\|Ez. 1:22]]` | TZ173; read by hand: match |
| Tikkunei Zohar 036b | 88 | `Song. 7:3` → `[[Song of Songs 7#^7-3\|Song. 7:3]]` | TZ174; read by hand: match |
| Tikkunei Zohar 036b | 216 | `Ez. 36:27` → `[[Ezekiel 36#^36-27\|Ez. 36:27]]` | TZ175; read by hand: match |
| Tikkunei Zohar 036b | 217 | `Ez. 36:26` → `[[Ezekiel 36#^36-26\|Ez. 36:26]]` | TZ176; read by hand: match |
| Tikkunei Zohar 036b | 235 | `Ez. 1:1` → `[[Ezekiel 01#^1-1\|Ez. 1:1]]` | TZ177; matches (1.00) |
| Tikkunei Zohar 037a | 270 | `Ez. 1:8` → `[[Ezekiel 01#^1-8\|Ez. 1:8]]` | TZ178; read by hand: match |
| Tikkunei Zohar 037b | 32 | `Ez. 1:8` → `[[Ezekiel 01#^1-8\|Ez. 1:8]]` | TZ179; read by hand: match |
| Tikkunei Zohar 037b | 48 | `Ecc. 3:13` → `[[Ecclesiastes 03#^3-13\|Ecc. 3:13]]` | TZ180; read by hand: match |
| Tikkunei Zohar 037b | 161 | `Is. 40:12` → `[[Isaiah 40#^40-12\|Is. 40:12]]` | TZ181; matches (0.67) |
| Tikkunei Zohar 037b | 189 | `Ecc. 1:6` → `[[Ecclesiastes 01#^1-6\|Ecc. 1:6]]` | TZ182; read by hand: match |
| Tikkunei Zohar 037b | 286 | `Ez. 1:14` → `[[Ezekiel 01#^1-14\|Ez. 1:14]]` | TZ183; read by hand: match |
| Tikkunei Zohar 038a | 67 | `Is. 40:12` → `[[Isaiah 40#^40-12\|Is. 40:12]]` | TZ184; read by hand: match |
| Tikkunei Zohar 038a | 120 | `Ex. 26: 26–27` → `[[Torah 19 - Terumah#^26-26\|Ex. 26: 26–27]]` | TZ185; matches (0.83) |
| Tikkunei Zohar 038a | 129 | `Ez. 1:22` → `[[Ezekiel 01#^1-22\|Ez. 1:22]]` | TZ186; read by hand: match |
| Tikkunei Zohar 038a | 167 | `Is. 45:18` → `[[Isaiah 45#^45-18\|Is. 45:18]]` | TZ187; read by hand: match |
| Tikkunei Zohar 038a | 200 | `Song. 4:12` → `[[Song of Songs 4#^4-12\|Song. 4:12]]` | TZ188; matches (0.38) |
| Tikkunei Zohar 038a | 209 | `Ez. 46:1` → `[[Ezekiel 46#^46-1\|Ez. 46:1]]` | TZ189; matches (0.88) |
| Tikkunei Zohar 038b | 34 | `Is. 61:11` → `[[Isaiah 61#^61-11\|Is. 61:11]]` | TZ190; read by hand: match |
| Tikkunei Zohar 038b | 49 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ191; matches (0.50) |
| Tikkunei Zohar 038b | 92 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ192; read by hand: match |
| Tikkunei Zohar 038b | 96 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ193; matches (0.50) |
| Tikkunei Zohar 038b | 139 | `Song. 4:12` → `[[Song of Songs 4#^4-12\|Song. 4:12]]` | TZ194; read by hand: match |
| Tikkunei Zohar 038b | 145 | `Ez. 34:31` → `[[Ezekiel 34#^34-31\|Ez. 34:31]]` | TZ195; read by hand: match |
| Tikkunei Zohar 039a | 81 | `Ecc. 11:5` → `[[Ecclesiastes 11#^11-5\|Ecc. 11:5]]` | TZ196; read by hand: match |
| Tikkunei Zohar 039a | 182 | `Song. 4:12` → `[[Song of Songs 4#^4-12\|Song. 4:12]]` | TZ197; read by hand: match |
| Tikkunei Zohar 039a | 192 | `1 King. 5:10` → `[[I Kings 05#^5-10\|1 King. 5:10]]` | TZ198; read by hand: match |
| Tikkunei Zohar 039a | 239 | `Is. 44:6` → `[[Isaiah 44#^44-6\|Is. 44:6]]` | TZ199; matches (1.00) |
| Tikkunei Zohar 039b | 45 | `Ez. 1:22` → `[[Ezekiel 01#^1-22\|Ez. 1:22]]` | TZ200; read by hand: match |
| Tikkunei Zohar 039b | 89 | `Song. 2:5` → `[[Song of Songs 2#^2-5\|Song. 2:5]]` | TZ201; read by hand: match |
| Tikkunei Zohar 039b | 159 | `Song. 2:5` → `[[Song of Songs 2#^2-5\|Song. 2:5]]` | TZ202; matches (0.50) |
| Tikkunei Zohar 039b | 211 | `Ez. 1:14` → `[[Ezekiel 01#^1-14\|Ez. 1:14]]` | TZ203; read by hand: match |
| Tikkunei Zohar 039b | 271 | `Is. 25:1` → `[[Isaiah 25#^25-1\|Is. 25:1]]` | TZ204; read by hand: match |
| Tikkunei Zohar 039b | 279 | `Ḥab. 3:10` → `[[Habakkuk 3#^3-10\|Ḥab. 3:10]]` | TZ205; read by hand: match |
| Tikkunei Zohar 040a | 45 | `Song. 5:14` → `[[Song of Songs 5#^5-14\|Song. 5:14]]` | TZ206; read by hand: match |
| Tikkunei Zohar 040a | 53 | `Is. 25:1` → `[[Isaiah 25#^25-1\|Is. 25:1]]` | TZ207; read by hand: match |
| Tikkunei Zohar 040a | 66 | `Is. 44:13` → `[[Isaiah 44#^44-13\|Is. 44:13]]` | TZ208; read by hand: match |
| Tikkunei Zohar 040a | 69 | `Is. 58:9` → `[[Isaiah 58#^58-9\|Is. 58:9]]` | TZ209; matches (0.67) |
| Tikkunei Zohar 040a | 128 | `Ecc. 1:4` → `[[Ecclesiastes 01#^1-4\|Ecc. 1:4]]` | TZ210; matches (0.83) |
| Tikkunei Zohar 040a | 171 | `Ecc. 3:4` → `[[Ecclesiastes 03#^3-4\|Ecc. 3:4]]` | TZ211; matches (0.67) |
| Tikkunei Zohar 040a | 190 | `Song. 6:1` → `[[Song of Songs 6#^6-1\|Song. 6:1]]` | TZ212; matches (0.35) |
| Tikkunei Zohar 040b | 23 | `1 Chron. 29:11` → `[[I Chronicles 29#^29-11\|1 Chron. 29:11]]` | TZ213; matches (0.67) |
| Tikkunei Zohar 040b | 68 | `Is. 59:17` → `[[Isaiah 59#^59-17\|Is. 59:17]]` | TZ214; read by hand: match |
| Tikkunei Zohar 040b | 138 | `Ecc. 5:7` → `[[Ecclesiastes 05#^5-7\|Ecc. 5:7]]` | TZ215; matches (0.60) |
| Tikkunei Zohar 041a | 34 | `Ex. 28` → `[[Torah 20 - Tetzaveh#^28-1\|Ex. 28]]` | TZ217; Chapters rule (M7): opens 28:1; the words quoted are 28:7 |
| Tikkunei Zohar 041a | 187 | `Is. 40:12` → `[[Isaiah 40#^40-12\|Is. 40:12]]` | TZ218; read by hand: match |
| Tikkunei Zohar 041b | 79 | `Is. 26:4` → `[[Isaiah 26#^26-4\|Is. 26:4]]` | TZ219; read by hand: match |
| Tikkunei Zohar 042a | 45 | `Is. 50:1` → `[[Isaiah 50#^50-1\|Is. 50:1]]` | TZ220; read by hand: match |
| Tikkunei Zohar 042a | 164 | `Is. 44:6` → `[[Isaiah 44#^44-6\|Is. 44:6]]` | TZ221; matches (0.50) |
| Tikkunei Zohar 042a | 219 | `Is. 1:4` → `[[Isaiah 01#^1-4\|Is. 1:4]]` | TZ222; read by hand: match |
| Tikkunei Zohar 042a | 258 | `Is. 42:8` → `[[Isaiah 42#^42-8\|Is. 42:8]]` | TZ223; matches (0.75) |
| Tikkunei Zohar 042b | 29 | `Is. 40:26` → `[[Isaiah 40#^40-26\|Is. 40:26]]` | TZ224; matches (1.00) |
| Tikkunei Zohar 042b | 155 | `Is. 11:6` → `[[Isaiah 11#^11-6\|Is. 11:6]]` | TZ225; read by hand: match |
| Tikkunei Zohar 043a | 155 | `Song. 6:10` → `[[Song of Songs 6#^6-10\|Song. 6:10]]` | TZ226; read by hand: match |
| Tikkunei Zohar 043a | 208 | `1 Chron. 23:17` → `[[I Chronicles 23#^23-17\|1 Chron. 23:17]]` | TZ227; read by hand: match |
| Tikkunei Zohar 043a | 270 | `Is. 53:1` → `[[Isaiah 53#^53-1\|Is. 53:1]]` | TZ228; matches (1.00) |
| Tikkunei Zohar 043b | 54 | `Song. 6:8` → `[[Song of Songs 6#^6-8\|Song. 6:8]]` | TZ229; read by hand: match |
| Tikkunei Zohar 043b | 233 | `Is. 27:5` → `[[Isaiah 27#^27-5\|Is. 27:5]]` | TZ230; read by hand: match |
| Tikkunei Zohar 043b | 239 | `Is. 57:19` → `[[Isaiah 57#^57-19\|Is. 57:19]]` | TZ231; matches (0.67) |
| Tikkunei Zohar 044a | 43 | `Is. 28:10` → `[[Isaiah 28#^28-10\|Is. 28:10]]` | TZ232; read by hand: match |
| Tikkunei Zohar 044b | 208 | `Song. 1:6` → `[[Song of Songs 1#^1-6\|Song. 1:6]]` | TZ233; read by hand: match |
| Tikkunei Zohar 045a | 123 | `Is. 65:24` → `[[Isaiah 65#^65-24\|Is. 65:24]]` | TZ234; matches (0.57) |
| Tikkunei Zohar 045a | 183 | `Is. 58:9` → `[[Isaiah 58#^58-9\|Is. 58:9]]` | TZ235; read by hand: match |
| Tikkunei Zohar 045a | 217 | `Song, 3:6` → `[[Song of Songs 3#^3-6\|Song, 3:6]]` | TZ236; read by hand: match |
| Tikkunei Zohar 045a | 240 | `Song. 1:13` → `[[Song of Songs 1#^1-13\|Song. 1:13]]` | TZ237; read by hand: match |
| Tikkunei Zohar 045a | 245 | `Song. 3:6` → `[[Song of Songs 3#^3-6\|Song. 3:6]]` | TZ238; read by hand: match |
| Tikkunei Zohar 045a | 280 | `Ez. 1:11` → `[[Ezekiel 01#^1-11\|Ez. 1:11]]` | TZ239; matches (1.00) |
| Tikkunei Zohar 045b | 58 | `Is. 50:4` → `[[Isaiah 50#^50-4\|Is. 50:4]]` | TZ240; read by hand: match |
| Tikkunei Zohar 045b | 98 | `Is. 40:22` → `[[Isaiah 40#^40-22\|Is. 40:22]]` | TZ241; matches (0.50) |
| Tikkunei Zohar 045b | 203 | `Is. 27:5` → `[[Isaiah 27#^27-5\|Is. 27:5]]` | TZ242; read by hand: match |
| Tikkunei Zohar 045b | 253 | `Is. 27:5` → `[[Isaiah 27#^27-5\|Is. 27:5]]` | TZ243; read by hand: match |
| Tikkunei Zohar 046a | 98 | `Is. 52:2` → `[[Isaiah 52#^52-2\|Is. 52:2]]` | TZ244; matches (0.67) |
| Tikkunei Zohar 046a | 147 | `Is. 58:9` → `[[Isaiah 58#^58-9\|Is. 58:9]]` | TZ245; matches (1.00) |
| Tikkunei Zohar 046a | 154 | `Is. 40:4` → `[[Isaiah 40#^40-4\|Is. 40:4]]` | TZ246; matches (0.55) |
| Tikkunei Zohar 047a | 25 | `Is. 28:9` → `[[Isaiah 28#^28-9\|Is. 28:9]]` | TZ247; matches (1.00) |
| Tikkunei Zohar 047a | 131 | `Is. 54:12` → `[[Isaiah 54#^54-12\|Is. 54:12]]` | TZ248; read by hand: match |
| Tikkunei Zohar 047b | 28 | `Ez. 1:20` → `[[Ezekiel 01#^1-20\|Ez. 1:20]]` | TZ249; read by hand: match |
| Tikkunei Zohar 048a | 242 | `Ecc. 7:23` → `[[Ecclesiastes 07#^7-23\|Ecc. 7:23]]` | TZ250; read by hand: match |
| Tikkunei Zohar 048b | 161 | `Ez. 1:10` → `[[Ezekiel 01#^1-10\|Ez. 1:10]]` | TZ251; read by hand: match |
| Tikkunei Zohar 048b | 211 | `Is. 42:13` → `[[Isaiah 42#^42-13\|Is. 42:13]]` | TZ252; read by hand: match |
| Tikkunei Zohar 048b | 271 | `Is. 34:11` → `[[Isaiah 34#^34-11\|Is. 34:11]]` | TZ253; read by hand: match |
| Tikkunei Zohar 049b | 22 | `Ecc. 7:6` → `[[Ecclesiastes 07#^7-6\|Ecc. 7:6]]` | TZ254; read by hand: match |
| Tikkunei Zohar 049b | 27 | `Ḥab. 1:13` → `[[Habakkuk 1#^1-13\|Ḥab. 1:13]]` | TZ255; read by hand: match |
| Tikkunei Zohar 049b | 82 | `Ecc. 10:2` → `[[Ecclesiastes 10#^10-2\|Ecc. 10:2]]` | TZ256; matches (0.67) |
| Tikkunei Zohar 049b | 89 | `Ecc. 7:26` → `[[Ecclesiastes 07#^7-26\|Ecc. 7:26]]` | TZ257; matches (0.40) |
| Tikkunei Zohar 049b | 90 | `Ecc. 10:2` → `[[Ecclesiastes 10#^10-2\|Ecc. 10:2]]` | TZ258; read by hand: match |
| Tikkunei Zohar 049b | 97 | `Ez. 44:30` → `[[Ezekiel 44#^44-30\|Ez. 44:30]]` | TZ259; read by hand: match |
| Tikkunei Zohar 049b | 100 | `Ecc. 9:9` → `[[Ecclesiastes 09#^9-9\|Ecc. 9:9]]` | TZ260; matches (0.75) |
| Tikkunei Zohar 049b | 155 | `Song. 1:6` → `[[Song of Songs 1#^1-6\|Song. 1:6]]` | TZ261; read by hand: match |
| Tikkunei Zohar 049b | 157 | `Is. 50:3` → `[[Isaiah 50#^50-3\|Is. 50:3]]` | TZ262; read by hand: match |
| Tikkunei Zohar 049b | 209 | `Song. 1:6` → `[[Song of Songs 1#^1-6\|Song. 1:6]]` | TZ263; read by hand: match |
| Tikkunei Zohar 049b | 324 | `Jon. 2:3` → `[[Jonah 2#^2-3\|Jon. 2:3]]` | TZ264; matches (0.42) |
| Tikkunei Zohar 050a | 110 | `Song. 1:6` → `[[Song of Songs 1#^1-6\|Song. 1:6]]` | TZ265; read by hand: match |
| Tikkunei Zohar 050a | 121 | `Ez. 1:1` → `[[Ezekiel 01#^1-1\|Ez. 1:1]]` | TZ266; read by hand: match |
| Tikkunei Zohar 050a | 126 | `Is. 50:3` → `[[Isaiah 50#^50-3\|Is. 50:3]]` | TZ267; read by hand: match |
| Tikkunei Zohar 050a | 170 | `Ecc. 12:3` → `[[Ecclesiastes 12#^12-3\|Ecc. 12:3]]` | TZ268; read by hand: match |
| Tikkunei Zohar 050a | 172 | `Ecc. 12:2` → `[[Ecclesiastes 12#^12-2\|Ecc. 12:2]]` | TZ269; matches (0.40) |
| Tikkunei Zohar 050a | 223 | `Is. 59:2` → `[[Isaiah 59#^59-2\|Is. 59:2]]` | TZ270; read by hand: match |
| Tikkunei Zohar 050b | 44 | `Is. 30:20` → `[[Isaiah 30#^30-20\|Is. 30:20]]` | TZ271; read by hand: match |
| Tikkunei Zohar 050b | 81 | `Song. 1:6` → `[[Song of Songs 1#^1-6\|Song. 1:6]]` | TZ272; read by hand: match |
| Tikkunei Zohar 050b | 172 | `2 Chron. 7:16` → `[[II Chronicles 07#^7-16\|2 Chron. 7:16]]` | TZ273; matches (0.67) |
| Tikkunei Zohar 050b | 204 | `Is. 63:4` → `[[Isaiah 63#^63-4\|Is. 63:4]]` | TZ274; read by hand: match |
| Tikkunei Zohar 050b | 240 | `Is. 63:4` → `[[Isaiah 63#^63-4\|Is. 63:4]]` | TZ275; matches (0.50) |
| Tikkunei Zohar 050b | 326 | `Is. 30:18` → `[[Isaiah 30#^30-18\|Is. 30:18]]` | TZ276; read by hand: match |
| Tikkunei Zohar 051a | 68 | `Is. 63:4` → `[[Isaiah 63#^63-4\|Is. 63:4]]` | TZ277; read by hand: match |
| Tikkunei Zohar 051a | 119 | `Song. 1:5` → `[[Song of Songs 1#^1-5\|Song. 1:5]]` | TZ278; read by hand: match |
| Tikkunei Zohar 051a | 142 | `Song. 8:7` → `[[Song of Songs 8#^8-7\|Song. 8:7]]` | TZ279; read by hand: match |
| Tikkunei Zohar 051a | 157 | `1 King. 10:19` → `[[I Kings 10#^10-19\|1 King. 10:19]]` | TZ280; matches (0.80) |
| Tikkunei Zohar 051a | 189 | `Is. 42:8` → `[[Isaiah 42#^42-8\|Is. 42:8]]` | TZ281; matches (0.86) |
| Tikkunei Zohar 051a | 209 | `Ez. 46:1` → `[[Ezekiel 46#^46-1\|Ez. 46:1]]` | TZ282; matches (0.71) |
| Tikkunei Zohar 051b | 135 | `Ez. 1:6` → `[[Ezekiel 01#^1-6\|Ez. 1:6]]` | TZ283; matches (0.40) |
| Tikkunei Zohar 051b | 174 | `Song. 5:14` → `[[Song of Songs 5#^5-14\|Song. 5:14]]` | TZ284; matches (0.50) |
| Tikkunei Zohar 051b | 176 | `Song. 5:15` → `[[Song of Songs 5#^5-15\|Song. 5:15]]` | TZ285; read by hand: match |
| Tikkunei Zohar 051b | 183 | `Is. 26:4` → `[[Isaiah 26#^26-4\|Is. 26:4]]` | TZ286; read by hand: match |
| Tikkunei Zohar 051b | 201 | `Is. 6:2` → `[[Isaiah 06#^6-2\|Is. 6:2]]` | TZ287; matches (0.39) |
| Tikkunei Zohar 052a | 23 | `1 King. 19:12` → `[[I Kings 19#^19-12\|1 King. 19:12]]` | TZ288; read by hand: match |
| Tikkunei Zohar 052a | 220 | `Ḥab. 1:13` → `[[Habakkuk 1#^1-13\|Ḥab. 1:13]]` | TZ289; read by hand: match |
| Tikkunei Zohar 052a | 255 | `Is. 1:23` → `[[Isaiah 01#^1-23\|Is. 1:23]]` | TZ290; read by hand: match |
| Tikkunei Zohar 052b | 23 | `Song. 4:7` → `[[Song of Songs 4#^4-7\|Song. 4:7]]` | TZ291; read by hand: match |
| Tikkunei Zohar 052b | 79 | `Song. 4:7` → `[[Song of Songs 4#^4-7\|Song. 4:7]]` | TZ292; read by hand: match |
| Tikkunei Zohar 052b | 91 | `Is. 42:8` → `[[Isaiah 42#^42-8\|Is. 42:8]]` | TZ293; matches (0.50) |
| Tikkunei Zohar 052b | 218 | `Is. 50:3` → `[[Isaiah 50#^50-3\|Is. 50:3]]` | TZ294; read by hand: match |
| Tikkunei Zohar 053a | 73 | `Jon. 1:4` → `[[Jonah 1#^1-4\|Jon. 1:4]]` | TZ295; read by hand: match |
| Tikkunei Zohar 053a | 75 | `Is. 63:14` → `[[Isaiah 63#^63-14\|Is. 63:14]]` | TZ296; read by hand: match |
| Tikkunei Zohar 053a | 133 | `Song. 5:15` → `[[Song of Songs 5#^5-15\|Song. 5:15]]` | TZ297; read by hand: match |
| Tikkunei Zohar 053a | 135 | `Is. 11:2` → `[[Isaiah 11#^11-2\|Is. 11:2]]` | TZ298; matches (0.67) |
| Tikkunei Zohar 053a | 147 | `Ez. 1:12` → `[[Ezekiel 01#^1-12\|Ez. 1:12]]` | TZ299; read by hand: match |
| Tikkunei Zohar 053a | 171 | `Jon. 1:4` → `[[Jonah 1#^1-4\|Jon. 1:4]]` | TZ300; matches (0.36) |
| Tikkunei Zohar 053a | 188 | `Jon. 1:5` → `[[Jonah 1#^1-5\|Jon. 1:5]]` | TZ301; read by hand: match |
| Tikkunei Zohar 053a | 192 | `Jon. 1:5` → `[[Jonah 1#^1-5\|Jon. 1:5]]` | TZ302; read by hand: match |
| Tikkunei Zohar 053a | 230 | `Jon. 1:6` → `[[Jonah 1#^1-6\|Jon. 1:6]]` | TZ303; read by hand: match |
| Tikkunei Zohar 053a | 257 | `Jon. 1:6` → `[[Jonah 1#^1-6\|Jon. 1:6]]` | TZ304; read by hand: match |
| Tikkunei Zohar 053b | 35 | `Jon. 1:6` → `[[Jonah 1#^1-6\|Jon. 1:6]]` | TZ305; read by hand: match |
| Tikkunei Zohar 053b | 62 | `Jon. 1:13` → `[[Jonah 1#^1-13\|Jon. 1:13]]` | TZ306; read by hand: match |
| Tikkunei Zohar 053b | 74 | `Jon. 2:1` → `[[Jonah 2#^2-1\|Jon. 2:1]]` | TZ307; read by hand: match |
| Tikkunei Zohar 053b | 77 | `Jon. 1:5` → `[[Jonah 1#^1-5\|Jon. 1:5]]` | TZ308; read by hand: match |
| Tikkunei Zohar 053b | 96 | `Jon. 2:1` → `[[Jonah 2#^2-1\|Jon. 2:1]]` | TZ309; matches (0.60) |
| Tikkunei Zohar 053b | 110 | `Jon. 2:1` → `[[Jonah 2#^2-1\|Jon. 2:1]]` | TZ310; matches (0.60) |
| Tikkunei Zohar 053b | 128 | `Ez. 29:3` → `[[Ezekiel 29#^29-3\|Ez. 29:3]]` | TZ311; read by hand: match |
| Tikkunei Zohar 053b | 131 | `Jon. 2:2` → `[[Jonah 2#^2-2\|Jon. 2:2]]` | TZ312; matches (0.60) |
| Tikkunei Zohar 053b | 144 | `Jon. 2:1` → `[[Jonah 2#^2-1\|Jon. 2:1]]` | TZ313; read by hand: match |
| Tikkunei Zohar 053b | 151 | `Ecc. 7:6` → `[[Ecclesiastes 07#^7-6\|Ecc. 7:6]]` | TZ314; read by hand: match |
| Tikkunei Zohar 053b | 152 | `Ecc. 7:9` → `[[Ecclesiastes 07#^7-9\|Ecc. 7:9]]` | TZ315; read by hand: match |
| Tikkunei Zohar 053b | 164 | `Jon. 2:1` → `[[Jonah 2#^2-1\|Jon. 2:1]]` | TZ316; matches (0.67) |
| Tikkunei Zohar 053b | 181 | `Jon. 2:1` → `[[Jonah 2#^2-1\|Jon. 2:1]]` | TZ317; matches (0.50) |
| Tikkunei Zohar 053b | 256 | `Jon. 2:1` → `[[Jonah 2#^2-1\|Jon. 2:1]]` | TZ318; read by hand: match |
| Tikkunei Zohar 053b | 261 | `Jon. 2:2` → `[[Jonah 2#^2-2\|Jon. 2:2]]` | TZ319; matches (0.38) |
| Tikkunei Zohar 053b | 277 | `Jon. 2:11` → `[[Jonah 2#^2-11\|Jon. 2:11]]` | TZ320; read by hand: match |
| Tikkunei Zohar 054a | 26 | `Ez. 16:7` → `[[Ezekiel 16#^16-7\|Ez. 16:7]]` | TZ321; matches (1.00) |
| Tikkunei Zohar 054a | 37 | `Jon. 2:11` → `[[Jonah 2#^2-11\|Jon. 2:11]]` | TZ322; matches (0.50) |
| Tikkunei Zohar 054a | 63 | `Jon. 2:11` → `[[Jonah 2#^2-11\|Jon. 2:11]]` | TZ323; matches (0.50) |
| Tikkunei Zohar 054b | 259 | `Is. 53:5` → `[[Isaiah 53#^53-5\|Is. 53:5]]` | TZ324; matches (0.50) |
| Tikkunei Zohar 054b | 264 | `Is. 53:5` → `[[Isaiah 53#^53-5\|Is. 53:5]]` | TZ325; matches (1.00) |
| Tikkunei Zohar 055a | 24 | `Is. 52:2` → `[[Isaiah 52#^52-2\|Is. 52:2]]` | TZ326; matches (1.00) |
| Tikkunei Zohar 055a | 65 | `Is. 63:12` → `[[Isaiah 63#^63-12\|Is. 63:12]]` | TZ327; read by hand: match |
| Tikkunei Zohar 055a | 78 | `Is. 54:7` → `[[Isaiah 54#^54-7\|Is. 54:7]]` | TZ328; read by hand: match |
| Tikkunei Zohar 055a | 148 | `Is. 60:22` → `[[Isaiah 60#^60-22\|Is. 60:22]]` | TZ329; read by hand: match |
| Tikkunei Zohar 055a | 174 | `Is. 1:18` → `[[Isaiah 01#^1-18\|Is. 1:18]]` | TZ330; matches (0.75) |
| Tikkunei Zohar 055a | 195 | `Is. 1:31` → `[[Isaiah 01#^1-31\|Is. 1:31]]` | TZ331; read by hand: match |
| Tikkunei Zohar 055a | 209 | `1 King. 10:19` → `[[I Kings 10#^10-19\|1 King. 10:19]]` | TZ332; read by hand: match |
| Tikkunei Zohar 055a | 251 | `Is. 63:4` → `[[Isaiah 63#^63-4\|Is. 63:4]]` | TZ333; read by hand: match |
| Tikkunei Zohar 055b | 52 | `Song. 3:6` → `[[Song of Songs 3#^3-6\|Song. 3:6]]` | TZ334; read by hand: match |
| Tikkunei Zohar 056a | 79 | `Is. 16:5` → `[[Isaiah 16#^16-5\|Is. 16:5]]` | TZ335; matches (0.67) |
| Tikkunei Zohar 056a | 264 | `Song. 3:11` → `[[Song of Songs 3#^3-11\|Song. 3:11]]` | TZ336; matches (0.50) |
| Tikkunei Zohar 056b | 45 | `Song. 4:7` → `[[Song of Songs 4#^4-7\|Song. 4:7]]` | TZ337; read by hand: match |
| Tikkunei Zohar 056b | 66 | `Is. 54:13` → `[[Isaiah 54#^54-13\|Is. 54:13]]` | TZ338; read by hand: match |
| Tikkunei Zohar 056b | 99 | `Psalm 118` → `[[Psalms 118#^118-1\|Psalm 118]]` | checker; checker: Chapters rule |
| Tikkunei Zohar 057a | 63 | `Ez. 46:1` → `[[Ezekiel 46#^46-1\|Ez. 46:1]]` | TZ339; matches (0.45) |
| Tikkunei Zohar 057a | 192 | `Song. 5:2` → `[[Song of Songs 5#^5-2\|Song. 5:2]]` | TZ340; read by hand: match |
| Tikkunei Zohar 057b | 149 | `Song. 7:2` → `[[Song of Songs 7#^7-2\|Song. 7:2]]` | TZ341; read by hand: match |
| Tikkunei Zohar 057b | 271 | `Is. 42:8` → `[[Isaiah 42#^42-8\|Is. 42:8]]` | TZ342; read by hand: match |
| Tikkunei Zohar 058a | 151 | `Is. 33:7` → `[[Isaiah 33#^33-7\|Is. 33:7]]` | TZ343; read by hand: match |
| Tikkunei Zohar 058b | 183 | `Is. 50:1` → `[[Isaiah 50#^50-1\|Is. 50:1]]` | TZ344; matches (0.40) |
| Tikkunei Zohar 059a | 69 | `Ecc. 3:13` → `[[Ecclesiastes 03#^3-13\|Ecc. 3:13]]` | TZ345; read by hand: match |
| Tikkunei Zohar 059a | 252 | `Is. 26:19` → `[[Isaiah 26#^26-19\|Is. 26:19]]` | TZ347; matches (1.00) |
| Tikkunei Zohar 059b | 140 | `Is. 6:3` → `[[Isaiah 06#^6-3\|Is. 6:3]]` | TZ348; read by hand: match |
| Tikkunei Zohar 059b | 279 | `Is. 3:14` → `[[Isaiah 03#^3-14\|Is. 3:14]]` | TZ349; read by hand: match |
| Tikkunei Zohar 059b | 286 | `Ecc. 9:9` → `[[Ecclesiastes 09#^9-9\|Ecc. 9:9]]` | TZ350; matches (0.75) |
| Tikkunei Zohar 059b | 302 | `Is. 50:1` → `[[Isaiah 50#^50-1\|Is. 50:1]]` | TZ351; matches (0.50) |
| Tikkunei Zohar 060a | 78 | `Is. 50:1` → `[[Isaiah 50#^50-1\|Is. 50:1]]` | TZ352; read by hand: match |
| Tikkunei Zohar 060a | 149 | `Is. 54:11` → `[[Isaiah 54#^54-11\|Is. 54:11]]` | TZ353; read by hand: match |
| Tikkunei Zohar 060a | 162 | `Is. 6:10` → `[[Isaiah 06#^6-10\|Is. 6:10]]` | TZ354; read by hand: match |
| Tikkunei Zohar 060a | 171 | `Is. 45:18` → `[[Isaiah 45#^45-18\|Is. 45:18]]` | TZ355; read by hand: match |
| Tikkunei Zohar 060b | 63 | `Is. 50:3` → `[[Isaiah 50#^50-3\|Is. 50:3]]` | TZ356; read by hand: match |
| Tikkunei Zohar 060b | 144 | `Ez. 1:11` → `[[Ezekiel 01#^1-11\|Ez. 1:11]]` | TZ358; read by hand: match |
| Tikkunei Zohar 060b | 149 | `Ez. 1:14` → `[[Ezekiel 01#^1-14\|Ez. 1:14]]` | TZ359; read by hand: match |
| Tikkunei Zohar 060b | 170 | `Is. 11:9` → `[[Isaiah 11#^11-9\|Is. 11:9]]` | TZ360; matches (0.43) |
| Tikkunei Zohar 060b | 184 | `Tzeph. 3:9` → `[[Zephaniah 3#^3-9\|Tzeph. 3:9]]` | TZ361; matches (0.50) |
| Tikkunei Zohar 060b | 209 | `Is. 60:21` → `[[Isaiah 60#^60-21\|Is. 60:21]]` | TZ362; read by hand: match |
| Tikkunei Zohar 060b | 241 | `Is. 60:20` → `[[Isaiah 60#^60-20\|Is. 60:20]]` | TZ363; read by hand: match |
| Tikkunei Zohar 060b | 284 | `Song. 4:12` → `[[Song of Songs 4#^4-12\|Song. 4:12]]` | TZ364; matches (1.00) |
| Tikkunei Zohar 061a | 82 | `Song. 4:12` → `[[Song of Songs 4#^4-12\|Song. 4:12]]` | TZ365; read by hand: match |
| Tikkunei Zohar 061a | 142 | `Ez. 46:1` → `[[Ezekiel 46#^46-1\|Ez. 46:1]]` | TZ366; matches (0.57) |
| Tikkunei Zohar 061b | 85 | `Is. 66:1` → `[[Isaiah 66#^66-1\|Is. 66:1]]` | TZ367; matches (1.00) |
| Tikkunei Zohar 061b | 127 | `Is. 46:10` → `[[Isaiah 46#^46-10\|Is. 46:10]]` | TZ368; read by hand: match |
| Tikkunei Zohar 061b | 155 | `Ez. 3:12` → `[[Ezekiel 03#^3-12\|Ez. 3:12]]` | TZ369; read by hand: match |
| Tikkunei Zohar 061b | 251 | `Is. 58:9` → `[[Isaiah 58#^58-9\|Is. 58:9]]` | TZ370; matches (0.50) |
| Tikkunei Zohar 062a | 50 | `Is. 63:4` → `[[Isaiah 63#^63-4\|Is. 63:4]]` | TZ371; read by hand: match |
| Tikkunei Zohar 062a | 122 | `Is. 6:3` → `[[Isaiah 06#^6-3\|Is. 6:3]]` | TZ372; read by hand: match |
| Tikkunei Zohar 062a | 154 | `1 Chron. 29:11` → `[[I Chronicles 29#^29-11\|1 Chron. 29:11]]` | TZ373; matches (1.00) |
| Tikkunei Zohar 062a | 194 | `Tzeph. 3:9` → `[[Zephaniah 3#^3-9\|Tzeph. 3:9]]` | TZ374; read by hand: match |
| Tikkunei Zohar 063a | 137 | `Ez. 1:10` → `[[Ezekiel 01#^1-10\|Ez. 1:10]]` | TZ375; matches (0.64) |
| Tikkunei Zohar 063a | 164 | `Ez. 37:7` → `[[Ezekiel 37#^37-7\|Ez. 37:7]]` | TZ376; read by hand: match |
| Tikkunei Zohar 063a | 303 | `Ez. 37:7` → `[[Ezekiel 37#^37-7\|Ez. 37:7]]` | TZ377; read by hand: match |

## Ready: BCP (26)

Source: `drafts/t2/bcp` (E11). Each link wraps `Book c:v-v` only; what follows (`,9`, `,12-24`, `---28:7`) stays outside the link, as the vault's linker does.

| Note | Line | Before → after | Source |
|---|---|---|---|
| BCP - Good Friday | 44 | `Wisdom 2:1` → `[[LXX Wisdom of Solomon 02#^2-1\|Wisdom 2:1]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Burial of the Dead - Rite I | 79 | `Wisdom 3:1-5` → `[[LXX Wisdom of Solomon 03#^3-1\|Wisdom 3:1-5]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Burial of the Dead - Rite II | 108 | `Wisdom 3:1-5` → `[[LXX Wisdom of Solomon 03#^3-1\|Wisdom 3:1-5]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Celebration and Blessing of a Marriage | 97 | `Tobit 8:5b-8` → `[[LXX Tobit 08#^8-5\|Tobit 8:5b-8]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Ordination of a Deacon | 128 | `Ecclesiasticus 39:1-8` → `[[LXX Sirach 39#^39-1\|Ecclesiasticus 39:1-8]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Holy Days | 75 | `Judith 9:1` → `[[LXX Judith 09#^9-1\|Judith 9:1]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Holy Days | 95 | `Ecclesiasticus 38:1-4` → `[[LXX Sirach 38#^38-1\|Ecclesiasticus 38:1-4]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Holy Days | 105 | `Ecclesiasticus 44:1-10` → `[[LXX Sirach 44#^44-1\|Ecclesiasticus 44:1-10]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Holy Days | 107 | `Ecclesiasticus 2:(1-6)7-11` → `[[LXX Sirach 02#^2-1\|Ecclesiasticus 2:(1-6)7-11]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - The Common of Saints | 29 | `Ecclesiasticus 51:1-12` → `[[LXX Sirach 51#^51-1\|Ecclesiasticus 51:1-12]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - The Common of Saints | 45 | `Wisdom 7:7-14` → `[[LXX Wisdom of Solomon 07#^7-7\|Wisdom 7:7-14]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - The Common of Saints | 55 | `Wisdom 3:1-9` → `[[LXX Wisdom of Solomon 03#^3-1\|Wisdom 3:1-9]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - The Common of Saints | 61 | `Ecclesiasticus 2:7-11` → `[[LXX Sirach 02#^2-7\|Ecclesiasticus 2:7-11]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Various Occasions | 47 | `Wisdom 3:1-9` → `[[LXX Wisdom of Solomon 03#^3-1\|Wisdom 3:1-9]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Various Occasions | 93 | `Ecclesiasticus 38:27-32` → `[[LXX Sirach 38#^38-27\|Ecclesiasticus 38:27-32]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Various Occasions | 111 | `Ecclesiasticus 38:27-32` → `[[LXX Sirach 38#^38-27\|Ecclesiasticus 38:27-32]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year A | 81 | `Ecclesiasticus 15:11-20` → `[[LXX Sirach 15#^15-11\|Ecclesiasticus 15:11-20]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year A | 123 | `Wisdom 2:1` → `[[LXX Wisdom of Solomon 02#^2-1\|Wisdom 2:1]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year A | 194 | `Ecclesiasticus 15:11-20` → `[[LXX Sirach 15#^15-11\|Ecclesiasticus 15:11-20]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year A | 222 | `Wisdom 12:13` → `[[LXX Wisdom of Solomon 12#^12-13\|Wisdom 12:13]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year A | 238 | `Ecclesiasticus 27:30` → `[[LXX Sirach 27#^27-30\|Ecclesiasticus 27:30]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year B | 119 | `Wisdom 2:1` → `[[LXX Wisdom of Solomon 02#^2-1\|Wisdom 2:1]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year B | 235 | `Wisdom 1:16` → `[[LXX Wisdom of Solomon 01#^1-16\|Wisdom 1:16]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year C | 40 | `Baruch 5:1-9` → `[[LXX Baruch 05#^5-1\|Baruch 5:1-9]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year C | 116 | `Wisdom 2:1` → `[[LXX Wisdom of Solomon 02#^2-1\|Wisdom 2:1]]` | E11; Brenton verse read by drafter and checker |
| BCP - The Lectionary - Year C | 230 | `Ecclesiasticus 10:(7-11)12-18` → `[[LXX Sirach 10#^10-7\|Ecclesiasticus 10:(7-11)12-18]]` | E11; Brenton verse read by drafter and checker |

## Edits that depend on your answers

### L1 – the 5 held Tanya links (recommended: none of these)

The two `*Tikkun* 7` notes (Likkutei Amarim 39, lines 68 and 71) stay plain under either option: the checker found the drafted links (`[[Tikkunei Zohar 024a#^24a-4\|7]]`, Tikkun 7) wrong, because the teaching cited is at 23a:10–11, in Tikkun 6. The only link option is the three folio items as drafted:

| Note | Line | Option | Before → after |
|---|---|---|---|
| Tanya - Iggeret HaKodesh 08 | 89 | as drafted | `I:128b` → `[[Zohar 10.07 - Parashat Hayyei Sarah#^z1-128b\|I:128b]]` |
| Tanya - Iggeret HaKodesh 08 | 92 | as drafted | `I:128b` → `[[Zohar 10.07 - Parashat Hayyei Sarah#^z1-128b\|I:128b]]` |
| Tanya - Iggeret HaKodesh 18 | 61 | as drafted | `III:145a` → `[[Zohar 12.06 - Piqqudin#^z3-145a\|III:145a]]` |

### L2 – MZ0026 (recommended: link)

| Note | Line | Before → after | Source |
|---|---|---|---|
| Mei HaShiloach I - Emor | 137 | `*Vayikra*, 88b` → `*Vayikra*, [[Zohar 8.04 - Parashat Emor#^z3-88b\|88b]]` | prep `mei_zohar_links.tsv` MZ0026; target renamed from `Zohar 8.04 - Parashat Qedoshim` |

### L3 – "Introduction" rows that quote Patach Eliyahu (recommended: link the 7)

| Row | Note | Line | Before → after | Tanya's words / Tikkunei Zohar 17a |
|---|---|---|---|---|
| TT0023 | Tanya - Likkutei Amarim 46 | 63 | `Introduction.` → `[[Tikkunei Zohar 017a#^17a-16\|Introduction]].` | "the two arms and the body" / 17a:16 "Ḥesed – right arm … Tipheret – body" |
| TT0030 | Tanya - Shaar HaYichud VehaEmunah 06 | 43 | `Introduction.` → `[[Tikkunei Zohar 017a#^17a-12\|Introduction]].` | "You are He who binds [the attributes] together and unites them" / 17a:12 "And You are He that binds them, and unites them" |
| TT0032 | Tanya - Shaar HaYichud VehaEmunah 07 | 109 | `Introduction.` → `[[Tikkunei Zohar 017a#^17a-10\|Introduction]].` | "no thought can grasp You at all" / 17a:10 "no thought apprehends You at all" |
| TT0034 | Tanya - Shaar HaYichud VehaEmunah 10 | 44 | `Introduction.` → `[[Tikkunei Zohar 017a#^17a-11\|Introduction]].` | "You have brought forth ten *tikkunim* … ten *sefirot* … hidden worlds" / 17a:11 "You are He that has produced ten 'constructs' … hidden worlds" |
| TT0035 | Tanya - Shaar HaYichud VehaEmunah 11 | 41 | `Introduction.` → `[[Tikkunei Zohar 017a#^17a-11\|Introduction]].` | "Hidden worlds which are not revealed" / 17a:11 "hidden worlds that are not revealed" |
| TT0037 | Tanya - Iggeret HaTeshuvah 01 | 63 | `Introduction.` → `[[Tikkunei Zohar 017a#^17a-15\|Introduction]].` | "You have made garments for them, from which souls issue forth to man" / 17a:15 "Garments have You fixed for them, from which fly-forth souls for human beings" |
| TT0041 | Tanya - Iggeret HaTeshuvah 10 | 39 | `Introduction.` → `[[Tikkunei Zohar 017a#^17a-16\|Introduction]].` | "kindness is the right arm" / 17a:16 "Ḥesed – right arm" |

### L4 – Raaya Mehemna: the 7 links you could unlink (recommended: keep)

Applied overnight; the checker found the cited passage missing from the vault text at each folio.

| Row | Note | Line | Now → if unlinked |
|---|---|---|---|
| TZ0043 | Tanya - Likkutei Amarim 18 | 53 | `[[Zohar 9.11 - Parashat Pinehas#^z3-252a\|III:252a]]` → `III:252a` |
| TZ0093 | Tanya - Likkutei Amarim 53 | 46 | `[[Zohar 9.11 - Parashat Pinehas#^z3-248a\|III:248a]]` → `III:248a` |
| TZ0179 | Tanya - Iggeret HaKodesh 05 | 92 | `[[Zohar 9.11 - Parashat Pinehas#^z3-248a\|III:248a]]` → `III:248a` |
| TZ0521 | Tanya - Iggeret HaKodesh 26 | 181 | `[[Zohar 9.11 - Parashat Pinehas#^z3-248a\|III:248a]]` → `III:248a` |
| TZ0151 | Tanya - Iggeret HaKodesh 03 | 56 | `[[Zohar 9.11 - Parashat Pinehas#^z3-242a\|III:242a]]` → `III:242a` |
| TZ0345 | Tanya - Iggeret HaKodesh 12 | 73 | `[[Zohar 9.11 - Parashat Pinehas#^z3-248b\|III:248b]]` → `III:248b` |
| TZ0507 | Tanya - Iggeret HaKodesh 26 | 104 | `[[Zohar 3.029a\|III: 29a]]` → `III: 29a` |

### L5 – `(Song. *1:6)` in the Tikkunei (recommended: link the numbers, after a test)

| Note | Line | Option | Before → after |
|---|---|---|---|
| Tikkunei Zohar 060b | 65 | recommended, after a test in Obsidian | `*1:6)` → `*[[Song of Songs 1#^1-6\|1:6]])` |

`(Ex. 28)` (041a, line 34) is no longer a question: it opens 28:1 by the Chapters rule (your M7 answer) and is in the ready list.

### L6 – bare items after a book name (recommended: link)

| Note | Line | Before → after |
|---|---|---|
| BCP - Daily Office - The Season after Pentecost | 1281 | `4:1-15 Su 5:22--6:4, 10-21 Tu 8:9-17; 9:1, 7-10 Th 12:1-20 Su 5:1-21 M 7:1-7, 19-32 W 10:1-23 F 13:1-20` → `[[LXX Judith 04#^4-1\|4:1-15]] Su [[LXX Judith 05#^5-22\|5:22]]--6:4, 10-21 Tu [[LXX Judith 08#^8-9\|8:9-17]]; [[LXX Judith 09#^9-1\|9:1]], 7-10 Th [[LXX Judith 12#^12-1\|12:1-20]] Su [[LXX Judith 05#^5-1\|5:1-21]] M [[LXX Judith 07#^7-1\|7:1-7]], 19-32 W [[LXX Judith 10#^10-1\|10:1-23]] F [[LXX Judith 13#^13-1\|13:1-20]]` |
| BCP - The Lectionary - Year C | 218 | `[[Ecclesiastes 01#^1-12\|Ecclesiastes 1:12-14]]; 2:(1-7,11)18-23` → `[[Ecclesiastes 01#^1-12\|Ecclesiastes 1:12-14]]; [[Ecclesiastes 02#^2-1\|2:(1-7,11)18-23]]` |

The Judith line gets 9 links (one per day item). The Ecclesiastes edit is a `replace` op, so it applies whatever the L7 answer.

### L7 – psalm numbers in the Sunday lectionary tables (recommended: BCP Psalm notes)

529 links in 309 entries of the 6 Sunday lectionary notes; each version is a set of 6 `lines` ops, checked by the BCP checker (309 of 309 edits pass).

- BCP Psalm notes: `/home/claude/p3/drafts/t2/bcp/alt/ops-psalms-bcp.json`
- JPS psalms: `/home/claude/p3/drafts/t2/bcp/alt/ops-psalms-jps.json`; the 100 distinct verse-numbered citations, BCP verse beside JPS verse: `/home/claude/p3/drafts/t2/bcp/alt/psalms-jps-check.md`
- Their `oldSha` is the text after the ready BCP ops (the same as after the draft's `ops.json` for these 6 notes). Apply them after the ready ops, and before the L6 Ecclesiastes edit.

Example, Year C line 90 (Second Sunday in Lent):

```
now:  27 *or* 27:10-18
BCP:  [[BCP Psalm 027#^27-1|27]] *or* [[BCP Psalm 027#^27-10|27:10-18]]
JPS:  [[Psalms 027#^27-1|27]] *or* [[Psalms 027#^27-7|27:10-18]]
```

### Not asked: Tikkunei citations whose numbers don't fit the words (left plain and listed, as your M4/M5 answers)

These 6 stay plain. The edits below are built only in case you want the verse quoted instead; they are under `not_asked_M4_M5` in the JSON.

| Note | Line | Option | Before → after |
|---|---|---|---|
| Tikkunei Zohar 034a | 56 | link to the verse quoted | `Ex. 20:24` → `[[Torah 17 - Yitro#^20-21\|Ex. 20:24]]` |
| Tikkunei Zohar 035a | 305 | link to the verse quoted | `Ex. 20:24` → `[[Torah 17 - Yitro#^20-21\|Ex. 20:24]]` |
| Tikkunei Zohar 036a | 131 | link to the verse quoted | `Ex. 20:24` → `[[Torah 17 - Yitro#^20-21\|Ex. 20:24]]` |
| Tikkunei Zohar 059a | 224 | link to the verse quoted | `Ex. 20:24` → `[[Torah 17 - Yitro#^20-21\|Ex. 20:24]]` |
| Tikkunei Zohar 040b | 190 | link to the verse quoted | `Jer. 19:22–23` → `[[Jeremiah 09#^9-22\|Jer. 19:22–23]]` |
| Tikkunei Zohar 020b | 125 | link to the verse quoted | `Ez. 1:16` → `[[Ezekiel 01#^1-15\|Ez. 1:16]]` |
| Tikkunei Zohar 020b | 125 | Ez. 1:16 as written | `Ez. 1:16` → `[[Ezekiel 01#^1-16\|Ez. 1:16]]` |
