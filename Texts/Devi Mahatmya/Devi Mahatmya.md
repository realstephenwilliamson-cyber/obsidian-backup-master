---
type: devi-mahatmya-index
title: "Devī Māhātmya"
---

# Devī Māhātmya

The *Devī Māhātmya* (“Glory of the Goddess”), also known as the *Durgā Saptaśatī* or *Caṇḍī*, is the section of the [[Markandeya Purana|Mārkaṇḍeya Purāṇa]] comprising chapters 78–90 (13 chapters, ~590 ślokas — see the footnote at the start of [[Markandeya Purana 078]]). The English translation of each chapter already lives in the Mārkaṇḍeya Purāṇa notes; the 13 notes below are the Devī Māhātmya-specific companions — for the Sanskrit text — and link back to that translation.

The recitation audio (29 tracks: 13 chapters and 16 opening, closing and rahasya texts) was taken out of the vault on 6 Oct 2026; it is kept in OneDrive.

## The thirteen chapters

| # | Chapter | Episode (caritra) | Mārkaṇḍeya Purāṇa |
|---|---|---|---|
| 1 | [[Devi Mahatmya 01]] | Prathama Charitra (First Episode) | [[Markandeya Purana 078\|MP 078]] |
| 2 | [[Devi Mahatmya 02]] | Madhyama Charitra (Middle Episode) | [[Markandeya Purana 079\|MP 079]] |
| 3 | [[Devi Mahatmya 03]] | Madhyama Charitra (Middle Episode) | [[Markandeya Purana 080\|MP 080]] |
| 4 | [[Devi Mahatmya 04]] | Madhyama Charitra (Middle Episode) | [[Markandeya Purana 081\|MP 081]] |
| 5 | [[Devi Mahatmya 05]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 082\|MP 082]] |
| 6 | [[Devi Mahatmya 06]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 083\|MP 083]] |
| 7 | [[Devi Mahatmya 07]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 084\|MP 084]] |
| 8 | [[Devi Mahatmya 08]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 085\|MP 085]] |
| 9 | [[Devi Mahatmya 09]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 086\|MP 086]] |
| 10 | [[Devi Mahatmya 10]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 087\|MP 087]] |
| 11 | [[Devi Mahatmya 11]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 088\|MP 088]] |
| 12 | [[Devi Mahatmya 12]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 089\|MP 089]] |
| 13 | [[Devi Mahatmya 13]] | Uttara Charitra (Final Episode) | [[Markandeya Purana 090\|MP 090]] |

## Opening recitation texts

Recited, in approximately this order, before beginning the thirteen chapters:

- [[Devi Mahatmya - Saptasati Parayana Sankalpam|Saptaśatī Pārāyaṇa Saṅkalpam]]
- [[Devi Mahatmya - Sapoddhara Mantram|Śāpoddhāra Mantram]]
- [[Devi Mahatmya - Utkilana Mantram|Utkīlana Mantram]]
- [[Devi Mahatmya - Devi Kavacham|Devī Kavacham]]
- [[Devi Mahatmya - Argala Stotram|Argalā Stotram]]
- [[Devi Mahatmya - Kilakam|Kīlakam]]
- [[Devi Mahatmya - Vaidika Ratri Suktam|Vaidika Rātri Sūktam]]
- [[Devi Mahatmya - Tantrika Ratri Suktam|Tāntrika Rātri Sūktam]]

## Closing recitation texts

Recited after completing the thirteen chapters:

- [[Devi Mahatmya - Devi Atharva Sirsam|Devī Atharva Śīrṣam]]
- [[Devi Mahatmya - Durga Saptasloki|Durgā Saptaślokī]]
- [[Devi Mahatmya - Durga Suktam|Durgā Sūktam]]
- [[Devi Mahatmya - Ksama Prarthana Stotram|Kṣamā Prārthanā Stotram]]
- [[Devi Mahatmya - Rgvedoktam Devisuktam|Ṛgvedoktaṃ Devīsūktam]]

## Rahasya Trayam (the three secret appendices)

- [[Devi Mahatmya - Rahasya Trayam - Murti Rahasyam|Rahasya Trayam — Mūrti Rahasyam]]
- [[Devi Mahatmya - Rahasya Trayam - Pradhanika Rahasyam|Rahasya Trayam — Prādhānika Rahasyam]]
- [[Devi Mahatmya - Rahasya Trayam - Vaikrtika Rahasyam|Rahasya Trayam — Vaikṛtika Rahasyam]]

## In the library

The catalog notes that name this work (`work: "[[Devi Mahatmya]]"`) and say how they relate to it (`role`): versions of the text, the texts recited with it, studies of it, and related goddess literature.

```base
filters:
  and:
    - file.folder.startsWith("Catalog/")
    - file.hasProperty("role")
    - file.hasLink(this.file)
views:
  - type: table
    name: By role
    groupBy:
      property: note.role
      direction: ASC
    order:
      - file.name
      - role
      - year
      - text
    sort:
      - property: role
        direction: ASC
      - property: file.name
        direction: ASC
```

## Status

All 29 companion notes are stubs: the 13 chapter notes link to the existing English translation, and all have headings left ready for the Sanskrit text and translation to be added later.
