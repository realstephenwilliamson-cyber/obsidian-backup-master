---
type: tool
---
# Devanagari search

Type in Harvard-Kyoto (or paste IAST) and press **Enter**: the vault search opens with the Devanagari spelling, and (unless you untick it) the Roman spelling with or without diacritics. Open this from anywhere with the command **Devanagari search** (Ctrl+P); you can give it a hotkey in Settings → Hotkeys.

```dataviewjs
await dv.view("Templates/Views/devanagari-search")
```

> [!info]- How to type
> Case matters (capital letters are the long vowels, retroflexes and so on).
>
> | Type | Gets | Type | Gets | Type | Gets |
> |---|---|---|---|---|---|
> | a A (or aa) | अ आ | i I (ii) | इ ई | u U (uu) | उ ऊ |
> | R RR | ऋ ॠ | lR | ऌ | e ai o au | ए ऐ ओ औ |
> | M | ं (anusvāra) | H | ः (visarga) | ' | ऽ (avagraha) |
> | k kh g gh G | क ख ग घ ङ | c ch j jh J | च छ ज झ ञ | T Th D Dh N | ट ठ ड ढ ण |
> | t th d dh n | त थ द ध न | p ph b bh m | प फ ब भ म | y r l v | य र ल व |
> | z (or sh) | श | S (or Sh) | ष | s h | स ह |
> | kS (or x) | क्ष | jJ | ज्ञ | L | ळ |
>
> Examples: `tantrAloka` → तन्त्रालोक, `zivasUtra` → शिवसूत्र, `pratyabhijJAhRdayam` → प्रत्यभिज्ञाहृदयम्, `kSemarAja` → क्षेमराज. Pasted IAST (`tantrāloka`) works too. Note that `c` is च and `ch` is छ (Harvard-Kyoto, not ITRANS).
>
> A word ending in a consonant is searched without its final virāma, so `saMvit` also finds संवित्ति and other words that begin संवित. With *allow ṃ/n variants* on, संत and सन्त match each other (also *saṃtāna* and *santāna*).
