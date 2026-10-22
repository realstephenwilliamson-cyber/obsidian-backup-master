# Phase 2 — Mūla repairs for approval (6 Oct 2026)

**What was checked:** all 5,845 verse notes, at the half-line level (rapidfuzz), against two independent witnesses:

- Jun Takashima's transcription of the KSTS edition: GRETIL for all 37 āhnikas.
  - The DCS text turned out to be the same transcription: 2,529 of 2,726 verses are identical letter for letter, and the rest differ only by GRETIL's lost anusvāras and avagraha signs.
  - So DCS and GRETIL count as one witness. DCS stays in the vault as the word notes; the GRETIL file stays out of the vault.
- The KSTS print itself: all twelve volumes, OCR'd with Tesseract (Sanskrit model) and mapped page by page.

The vault's own Devanagari (the Muktabodha e-text) is the third text.

**How the repairs were made:**

1. A script flagged every verse whose Mūla did not match Takashima half-line for half-line.
2. Fifteen aligner agents (one per āhnika or group) reviewed every flagged verse and proposed the new Mūla. Wherever the vault holds the line, it is copied from the vault's own Devanagari.
3. Nine separate checker agents compared every proposed change with the KSTS page image:
   - 168 confirmed;
   - 7 open items settled from the print;
   - 0 sent back.

## Counts by class and āhnika

| Āhnika | Notes | Correct, unchanged | Half-line missing | Commentary in the mūla | Half-line missing + commentary in the mūla | Partial (split, truncated or e-text marks) | Different text | Changed |
|---|---|---|---|---|---|---|---|---|
| 1 | 332 | 322 | 7 | 1 | 2 |  |  | 10 |
| 2 | 50 | 49 |  | 1 |  |  |  | 1 |
| 3 | 293 | 278 | 8 | 6 |  |  | 1 | 15 |
| 4 | 278 | 267 | 2 | 8 |  | 1 |  | 11 |
| 5 | 158 | 153 | 3 | 2 |  |  |  | 5 |
| 6 | 251 | 243 | 1 | 5 |  |  | 2 | 8 |
| 7 | 71 | 70 | 1 |  |  |  |  | 1 |
| 8 | 452 | 436 | 10 | 1 |  | 4 | 1 | 16 |
| 9 | 314 | 292 | 6 | 7 |  | 8 | 1 | 22 |
| 10 | 309 | 299 | 3 | 3 |  | 4 |  | 10 |
| 11 | 118 | 114 | 1 | 3 |  |  |  | 4 |
| 12 | 26 | 24 |  | 1 | 1 |  |  | 2 |
| 13 | 361 | 352 | 4 | 5 |  |  |  | 9 |
| 14 | 46 | 46 |  |  |  |  |  | 0 |
| 15 | 613 | 600 | 2 | 8 |  | 2 | 1 | 13 |
| 16 | 311 | 304 | 1 | 5 |  | 1 |  | 7 |
| 17 | 122 | 120 |  | 2 |  |  |  | 2 |
| 18 | 11 | 11 |  |  |  |  |  | 0 |
| 19 | 56 | 54 | 1 | 1 |  |  |  | 2 |
| 20 | 15 | 15 |  |  |  |  |  | 0 |
| 21 | 61 | 58 | 3 |  |  |  |  | 3 |
| 22 | 48 | 48 |  |  |  |  |  | 0 |
| 23 | 103 | 101 | 2 |  |  |  |  | 2 |
| 24 | 24 | 23 |  | 1 |  |  |  | 1 |
| 25 | 29 | 27 | 1 | 1 |  |  |  | 2 |
| 26 | 76 | 73 | 2 | 1 |  |  |  | 3 |
| 27 | 59 | 59 |  |  |  |  |  | 0 |
| 28 | 434 | 426 | 3 | 4 |  | 1 |  | 8 |
| 29 | 291 | 280 | 1 | 8 |  | 2 |  | 11 |
| 30 | 123 | 122 |  | 1 |  |  |  | 1 |
| 31 | 163 | 160 |  | 1 |  | 2 |  | 3 |
| 32 | 67 | 66 |  | 1 |  |  |  | 1 |
| 33 | 33 | 32 |  |  |  | 1 |  | 1 |
| 34 | 3 | 3 |  |  |  |  |  | 0 |
| 35 | 44 | 44 |  |  |  |  |  | 0 |
| 36 | 15 | 15 |  |  |  |  |  | 0 |
| 37 | 85 | 85 |  |  |  |  |  | 0 |
| **All** | **5845** | **5671** | **62** | **77** | **3** | **26** | **6** | **174** |

- **Reading fixes:** within these 174 notes, 19 single-word readings are corrected. In each case the checker saw the printed word on the page and GRETIL agrees with the print. Nasal spellings (ङ्क/ंक) and spacing are left as they are.
- **Viveka:** where a half-line stood as running text in a Viveka section, that line is split so the half-line stands on its own `> ` line, as verse quotations do everywhere else. That is 63 Viveka lines in about 60 notes. Nothing is deleted from any Viveka.
- **Commentary lines:** every commentary line removed from a Mūla is already in a Viveka, so no text is lost.
- **Unchanged:** everything else in the notes, including the `^mula`/`^iast` ids. The IAST is regenerated from the new Devanagari, as before.

## Open list (your decision)

| Verse | What the witnesses say | KSTS page | Options |
|---|---|---|---|
| 33.33 | KSTS ends āhnika 33 at verse 32. The vault's note 33.33 holds, as its "Mūla", the e-text's colophon line, which KSTS does not print anywhere (its only colophon is Jayaratha's). | vol. XII p. 351 (PDF 193) | (a) leave the note and add one line saying KSTS has no verse 33.33 (my suggestion for now); (b) retire the note in phase 3 and move its Viveka to the chapter note's Closing (this changes one study-plan day) |
| 37.52 | KSTS prints *siṃtāṃśu*, Dyczkowski reads *sitāṃśu* (the left-over question from phase 1). | vol. XII | keep KSTS as printed (the Mūla follows the edition; my suggestion), or emend to *sitāṃśu* |

**Settled by the print** (no question for you):

- **37.33:** KSTS prints *ṣaḍardhasāraṃ sacchāstram…* after ॥३२॥, as the first half of 33, so it stays in 37.33.
- **8.256** and **19.38ab:** the missing quarter and half are printed in KSTS. 8.256 is rebuilt from the vault's own lines; 19.38a is copied from the page and agrees with GRETIL.
- **3.1:** *atha paraupayikaṃ…* is printed unnumbered at the head of āhnika 3. It is the second half of 2.50 (Jayaratha: "द्वितीयार्धेन"), so it stays in the chapter note, as now.
- **6.53–54:** the vault's two lines swap their subjects; the print agrees with GRETIL.
- **8.110:** KSTS prints *sarveṣām uttaro meruḥ…* as root text, as DCS has it.
- **28.261a** and **31.104:** the half-lines the e-text lost are taken from the page and agree with GRETIL.

## 30 examples (21 āhnikas)

### 1. TĀ 1.134 — half-line missing

KSTS vol. I, p. 174 (PDF p. 184). Check: confirm.

Before:

> सोऽयमात्मानमावृत्य स्थितो जडपदं गतः ॥

After:

> विधिश्च नोक्तः कोऽप्यत्र मन्त्रादि वृत्तिधाम वा ।
> सोऽयमात्मानमावृत्य स्थितो जडपदं गतः ॥

- Moved from: "विधिश्च नोक्तः कोऽप्यत्र मन्त्रादि वृत्तिधाम वा ।" stands in Tantraloka 01.133, Viveka, file line 47, at the start of a running-text line (after the lead-in line 45 "...
- Viveka of 1.133: the half-line «विधिश्च नोक्तः कोऽप्यत्र मन्त्रादि वृत्तिधाम वा ।…» goes on its own `> ` line; the rest of that line stays as it is.

### 2. TĀ 1.330 — half-line missing + commentary in the Mūla

KSTS vol. I, p. 301 (PDF p. 311). Check: confirm.

Before:

> संक्षेपेण एषोऽर्थः प्रकटितः इत्यनेनैव सम्बन्धः ॥

After:

> आत्मा संवित्प्रकाशस्थितिरनवयवा संविदित्यात्तशक्तिव्रातं तस्य स्वरूपं स च निजमहसश्छादनाद् बद्धरूपः ।
> आत्मज्योतिःस्वभावप्रकटनविधिना तस्य मोक्षः स चायं चित्राकारस्य चित्रः प्रकटित इह यत्संग्रहेणार्थ एषः ॥

- Moved from: Both halves of the sragdharā stand together on one running-text line in Tantraloka 01.329, Viveka, file line 47 ("आत्मा संवित्प्रकाशस्थितिरनवयवा ...
- Viveka of 1.329: the half-line «आत्मा संवित्प्रकाशस्थितिरनवयवा संविदित्यात्तशक्तिव्रातं तस्य…» goes on its own `> ` line; the rest of that line stays as it is.
- Viveka of 1.329: the half-line «आत्मज्योतिःस्वभावप्रकटनविधिना तस्य मोक्षः स चायं चित्राकारस्…» goes on its own `> ` line; the rest of that line stays as it is.

### 3. TĀ 1.214 — commentary in the Mūla

KSTS vol. I, p. 236 (PDF p. 246). Check: confirm.

Before:

> परा भट्टारिकारूपा च असौ इच्छाशक्तिः, तदात्मकश्च असौ अंशः
> शाक्तोऽथ भण्यते चेतोधीमनोहंकृतिः स्फुटम् ।
> सविकल्पतया मायामयमिच्छादि वस्तुतः ॥

After:

> शाक्तोऽथ भण्यते चेतोधीमनोहंकृति स्फुटम् ।
> सविकल्पतया मायामयमिच्छादि वस्तुतः ॥

- Reading checked on the page and in GRETIL: चेतोधीमनोहंकृतिः → चेतोधीमनोहंकृति

### 4. TĀ 3.56 — half-line missing

KSTS vol. II, p. 64 (PDF p. 78). Check: confirm.

Before:

> नन्वित्थं प्रतिबिम्बस्य लक्षणं किं तदुच्यते ।
> प्रतिबिम्बमिति प्राहुर्दर्पणे वदनं यथा ॥

After:

> नन्वित्थं प्रतिबिम्बस्य लक्षणं किं तदुच्यते ।
> अन्यव्यामिश्रणायोगात्तद्भेदाशक्यभासनम् ।
> प्रतिबिम्बमिति प्राहुर्दर्पणे वदनं यथा ॥

- Moved from: Tantraloka 03.056 (its own note), Viveka, line 42: "अन्यव्यामिश्रणायोगात्तद्भेदाशक्यभासनम् ॥" on its own line between the two "> " lines, not itself a "> " line.
- Viveka of 3.56: the half-line «अन्यव्यामिश्रणायोगात्तद्भेदाशक्यभासनम् ॥…» goes on its own `> ` line; the rest of that line stays as it is.

### 5. TĀ 3.228 — commentary in the Mūla

KSTS vol. II, p. 217 (PDF p. 231). Check: confirm.

Before:

> भूतभावोद्भवकरो विसर्गः कर्मसंज्ञितः ॥ (गी. ८अ. ३ श्लो.)
> तस्यापि च परं वीर्यं पञ्चभूतकलात्मकम् ।
> भोग्यत्वेनान्नरूपं च शब्दस्पर्शरसात्मकम् ॥

After:

> तस्यापि च परं वीर्यं पञ्चभूतकलात्मकम् ।
> भोग्यत्वेनान्नरूपं च शब्दस्पर्शरसात्मकम् ॥

### 6. TĀ 4.10 — commentary in the Mūla

KSTS vol. III, p. 9 (PDF p. 51). Check: confirm.

Before:

> इत्यादिनोक्तम् । यदभिप्रायेणैव अतो बाह्यैरपि
> ङापनेयमतः किञ्चित्प्रक्षेप्तव्यं न किञ्चन ।
> किं तु दुर्घटकारित्वात्स्वाच्छन्द्यान्निर्मलादसौ ।
> स्वात्मप्रच्छादनक्रीडापण्डितः परमेश्वरः ॥

After:

> किं तु दुर्घटकारित्वात्स्वाच्छन्द्यान्निर्मलादसौ ।
> स्वात्मप्रच्छादनक्रीडापण्डितः परमेश्वरः ॥

### 7. TĀ 4.70 — commentary in the Mūla

KSTS vol. III, p. 75 (PDF p. 117). Check: confirm.

Before:

> गुरोः स शास्त्रंमन्विच्छुस्तदुक्तं क्रममाचरेत् ।
> तदाह येन केनाप्युपायेन गुरुमाराध्य भक्तितः ॥

After:

> गुरोः स शास्त्रंमन्विच्छुस्तदुक्तं क्रममाचरेत् ।
> येन केनाप्युपायेन गुरुमाराध्य भक्तितः ॥

### 8. TĀ 6.53 — different text

KSTS vol. IV, p. 46 (PDF p. 64). Check: resolved.

Before:

> प्रभुशक्तिः क्वचित्कन्दसङ्कोचस्पन्दने यथा ।
> प्राणशक्तिः क्वचिन्मुख्या यथाङ्गमरुदीरणे ॥

After:

> प्रभुशक्तिः क्वचिन्मुख्या यथाङ्गमरुदीरणे ।
> आत्मशक्तिः क्वचित्कन्दसङ्कोचस्पन्दने यथा ॥

- Settled from the KSTS page by the checker: The print settles it. After 'इति ॥ ५२ ॥' and the lead-in 'एवमेषां समानेऽपि यत्नविधायित्वे क्वचित्कस्यचिन्मुख्यत्वम्,—इत्याह', KSTS prints verse 53 in root type. The first half is prabhuśakti with aṅgamarudīraṇa; the second is ātmaśakti with kanda. This agrees with GRETIL/DCS. The vault's lines swap 

### 9. TĀ 6.97 — commentary in the Mūla

KSTS vol. IV, p. 83 (PDF p. 101). Check: confirm.

Before:

> एतदेव प्रकृते योजयति
> एवं कलाः पञ्चदश क्षीयन्ते शशिनः क्रमात् ।
> आप्यायिन्यमृताबूर्पतादात्म्यात्षोडशी न तु ॥

After:

> एवं कलाः पञ्चदश क्षीयन्ते शशिनः क्रमात् ।
> आप्यायिन्यमृताब्रूपतादात्म्यात्षोडशी न तु ॥

- Reading checked on the page and in GRETIL: आप्यायिन्यमृताबूर्पतादात्म्यात् → आप्यायिन्यमृताब्रूपतादात्म्यात्

### 10. TĀ 8.110 — unclear

KSTS vol. V, p. 84 (PDF p. 94). Check: resolved.

Before:

> उदयास्तमयावित्थं सूर्यस्य परिभावयेत् ॥

After:

> सर्वेषामुत्तरो मेरुर्लोकालोकश्च दक्षिणः ।
> उदयास्तमयावित्थं सूर्यस्य परिभावयेत् ॥

- Moved from: Candidate first half stands in Tantraloka 08.109, Viveka line 30: a plain line of its own after '...
- Viveka of 8.109: the half-line «शर्वेषामुत्तरो मेरुर्लोकालोकश्च दक्षिणः…» goes on its own `> ` line; the rest of that line stays as it is.
- Settled from the KSTS page by the checker: Reading B. p.83 (PDF 93) closes '...अयनद्वयमेतदेव कथयन्ति ॥ १०९ ॥'. On p.84, Jayaratha's lead-in ends '...इत्यत्र किं प्रमाणम्? इत्याशङ्क्याह'. KSTS then prints 'सर्वेषामुत्तरो मेरुर्लोकालोकश्च दक्षिणः ।' in root type: large bold type, indented, split over two lines like every root half. The only di

### 11. TĀ 8.256 — partial

KSTS vol. V, p. 175 (PDF p. 185). Check: confirm.

Before:

> कथं सुवीत तत्राद्ये क्षोभे स्यादनवस्थितिः ।
> .................यदि वा तेन ते गुणाः ॥

After:

> कथं सुवीत तत्राद्ये क्षोभे स्यादनवस्थितिः ।
> सांख्यस्य दोष एवायं यदि वा तेन ते गुणाः ॥

### 12. TĀ 8.185 — different text

KSTS vol. V, p. 133 (PDF p. 143). Check: confirm.

Before:

> तेषु क्रमेण ब्रह्माणः संस्युर्द्विगुणजीविताः ।
> क्षीयन्ते क्रमशस्ते च तदन्ते तत्त्वमम्मयम् ++ ॥

After:

> तेषु क्रमेण ब्रह्माणः संस्युर्द्विगुणजीविताः ।
> क्षीयन्ते क्रमशस्ते च तदन्ते तत्त्वमम्मयम् ॥

### 13. TĀ 9.15 — partial

KSTS vol. VI, p. 25 (PDF p. 35). Check: confirm.

Before:

> स तत्स्वभाव इति चेत् ................. ।
> .................टर्हि बीजाङ्कुरा निजे ।
> तावत्येव न विश्रान्तौ तदन्यात्यन्तसंभवात् ॥

After:

> स तत्स्वभाव इति चेत् तर्हि बीजाङ्कुरा निजे ।
> तावत्येव न विश्रान्तौ तदन्यात्यन्तसंभवात् ॥

### 14. TĀ 9.126 — different text

KSTS vol. VI, p. 100 (PDF p. 110). Check: confirm.

Before:

> कृषिकर्म मधौ भोगः शरद्यन्या१ च सा तनुः ।
> अनुसन्धातुरेकस्य संभवस्तु यतस्ततः ॥

After:

> कृषिकर्म मधौ भोगः शरद्यन्या च सा तनुः ।
> अनुसन्धातुरेकस्य संभवस्तु यतस्ततः ॥

### 15. TĀ 10.71 — partial

KSTS vol. VII, p. 57 (PDF p. 70). Check: confirm.

Before:

> अनवस्था.........................
> तथा ह्यन्यैर्नीलाद्यै किन्तु सदृशी न सा ।
> वेद्यता किन्तु धर्मोऽसौ यद्योगात्सर्वधर्मवान् ॥

After:

> अनवस्था तथा ह्यन्यैर्नीलाद्यैः सदृशी न सा ।
> वेद्यता किन्तु धर्मोऽसौ यद्योगात्सर्वधर्मवान् ॥

- Reading checked on the page and in GRETIL: नीलाद्यै किन्तु सदृशी → नीलाद्यैः सदृशी

### 16. TĀ 11.68 — commentary in the Mūla

KSTS vol. VII, p. 54 (PDF p. 275). Check: confirm.

Before:

> सङ्केता यान्ति चेत्तेऽपि यान्त्यसङ्केतवृत्तिताम् ।
> एतदेव व्यतिरेकद्वारेणाप्युपपादयति
> अनया तु विना सर्वे सङ्केता बहुशः कृताः ॥

After:

> सङ्केता यान्ति चेत्तेऽपि यान्त्यसङ्केतवृत्तिताम् ।
> अनया तु विना सर्वे सङ्केता बहुशः कृताः ॥

### 17. TĀ 12.26 — half-line missing + commentary in the Mūla

KSTS vol. VII, p. 108 (PDF p. 328). Check: confirm.

Before:

> दर्शिताभ्युपायमिति दर्शितः स्थानभेदाद्यात्माभ्युपायो यस्य इति शिवम् ॥

After:

> अनुत्तरपदाप्तये तदिदमाणवं दर्शिताभ्युपायमतिविस्तरान्ननु विदांकुरुध्वं बुधाः ॥

- Moved from: The half-verse is in Tantraloka 12.025, Viveka line 56.
- Viveka of 12.25: the half-line «अनुत्तरपदाप्तये तदिदमाणवं दर्शिताभ्युपायमतिविस्तरान्ननु विदा…» goes on its own `> ` line; the rest of that line stays as it is.

### 18. TĀ 13.112 — commentary in the Mūla

KSTS vol. VIII, p. 75 (PDF p. 86). Check: confirm.

Before:

> प्रति भिन्नेन भावेन स्पृहातो लोलिका मलः ।
> इति ॥ ननु भेदवादिवन्मलादीनामीश्वरस्य च
> विशुद्धस्वप्रकाशात्मशिवरूपतया विना ॥

After:

> प्रति भिन्नेन भावेन स्पृहातो लोलिका मलः ।
> विशुद्धस्वप्रकाशात्मशिवरूपतया विना ॥

### 19. TĀ 15.203 — commentary in the Mūla

KSTS vol. IX, p. 101 (PDF p. 105). Check: confirm.

Before:

> दिग्विभागः स्थितो लोके शास्त्रेऽपि च तथोच्यते ।
> तदेवमयं दिग्विभागोऽस्मिन्प्रकाशैकरूपे परानुग्रहपरे परमेश्वरे
> श्वामिनश्चात्मसंस्थस्य भावजातस्य भासनम् ।
> अस्त्येव न विना तस्मादिच्छामर्शः प्रवर्त्तते ॥(रि.प्र. १ ।५ ।१०)
> क्रमात्सदाशिवाधीशः पञ्चमन्त्रतनुर्यतः ॥

After:

> दिग्विभागः स्थितो लोके शास्त्रेऽपि च तथोच्यते ।
> क्रमात्सदाशिवाधीशः पञ्चमन्त्रतनुर्यतः ॥

### 20. TĀ 15.113 — different text

KSTS vol. IX, p. 58 (PDF p. 62). Check: confirm.

Before:

> क्लिश्यन्ते सविकल्पास्तु कल्पोक्तेऽपि कृते सति ।
> ऽऽतदाक्रम्य बलं मन्त्राऽऽ ऽऽअयमेवोदयः स्फुटःऽऽ ॥

After:

> क्लिश्यन्ते सविकल्पास्तु कल्पोक्तेऽपि कृते सति ।
> तदाक्रम्य बलं मन्त्रा अयमेवोदयः स्फुटः ॥

### 21. TĀ 16.1 — half-line missing

KSTS vol. X, p. 1 (PDF p. 5). Check: confirm.

Before:

> यदा तु समयस्थस्य पुत्रकत्वे नियोजनम् ।
> गुरुकत्वे साधकत्वे वा कर्तुमिच्छति दैशिकः ॥

After:

> अथ पुत्रकत्वसिद्ध्यै निरूप्यते शिवनिरूपितोऽत्र विधिः ।
> यदा तु समयस्थस्य पुत्रकत्वे नियोजनम् ।
> गुरुत्वे साधकत्वे वा कर्तुमिच्छति दैशिकः ॥

- Moved from: 16.001, Viveka, Lead-in line (line 1 of the Viveka), as running text after 'द्वितीयार्धेन प्रतिजानीते-- ' and before 'तमेवाह—'.
- Viveka of 16.1: the half-line «अथ पुत्रकत्वसिद्ध्यै निरूप्यते शिवनिरूपितोऽत्र विधिः ।…» goes on its own `> ` line; the rest of that line stays as it is.
- Reading checked on the page and in GRETIL: गुरुकत्वे → गुरुत्वे

### 22. TĀ 19.38 — half-line missing

KSTS vol. X, p. 197 (PDF p. 197). Check: resolved.

Before:

> पर्युदासेन यः श्रोतुमवधारयितुं क्षमः ॥

After:

> हन्त कुड्याग्रतोऽप्यस्य निषेधस्त्वथ कथ्यते ।
> पर्युदासेन यः श्रोतुमवधारयितुं क्षमः ॥

- Settled from the KSTS page by the checker: KSTS prints the missing half in root type after the lead-in 'एवं तर्हि नास्य कदाचिदपि पाठः प्राप्तः, अतः कुड्यादयोऽप्यदीक्षिताः किं न संनिहिता भवेयुरित्याह': 'हन्त कुड्याग्रतोऽप्यस्य / निषेधस्त्वथ कथ्यते ।', then 'पर्युदासेन यः श्रोतु- / मवधारयितुं क्षमः ॥ ३८ ॥'. A full anuṣṭubh; no footnote on the 

### 23. TĀ 21.25 — half-line missing

KSTS vol. X, p. 225 (PDF p. 224). Check: confirm.

Before:

> चित्तमाकृष्य तत्रस्थं कुर्यात्तद्विधिरुच्यते ।
> यावद्धूमाभिरामप्रचिततरशिखाजालकेनाध्वचक्रं संछाद्याभीष्टजीवानयनमिति महाजालनामा प्रयोगः ॥

After:

> चित्तमाकृष्य तत्रस्थं कुर्यात्तद्विधिरुच्यते ।
> मूलाधारादुदेत्य प्रसृतसुविततानन्तनाड्यध्वदण्डं वीर्येणाक्रम्य नासागगनपरिगतं विक्षिपन् व्याप्तुमीष्टे ।
> यावद्धूमाभिरामप्रचिततरशिखाजालकेनाध्वचक्रं संछाद्याभीष्टजीवानयनमिति महाजालनामा प्रयोगः ॥

- Moved from: Tantraloka 21.024, Viveka, line 57: a plain line (running text) after the lead-in "तद्विधिमेव आह -".
- Viveka of 21.24: the half-line «मूलाधारादुदेत्य प्रसृतसुविततानन्तनाड्यध्वदण्डं वीर्येणाक्रम्…» goes on its own `> ` line; the rest of that line stays as it is.

### 24. TĀ 26.64 — half-line missing

KSTS vol. X, p. 350 (PDF p. 346). Check: confirm.

Before:

> आनन्दामृतनिर्भरस्वहृदयानर्घार्घपात्रक्रमात् त्वां देव्या सह देहदेवसदने देवार्चयेऽहर्निशम् ॥

After:

> कृत्वाधारधरां चमत्कृतिरसप्रोक्षाक्षणक्षालिता- मात्तैर्मानसतःस्वभावकुसुमैः स्वामोदसन्दोहिभिः ।
> आनन्दामृतनिर्भरस्वहृदयानर्घार्घपात्रक्रमात् त्वां देव्या सह देहदेवसदने देवार्चयेऽहर्निशम् ॥

- Moved from: First half (padas a-b) stands in Tantraloka 26.063, Viveka, as a running-text line directly after the "> " quote of 26.63 (last line of that Viveka);
- Viveka of 26.63: the half-line «कृत्वाधारधरां चमत्कृतिरसप्रोक्षाक्षणक्षालिता- मात्तैर्मानसतः…» goes on its own `> ` line; the rest of that line stays as it is.

### 25. TĀ 28.261 — half-line missing

KSTS vol. XI, p. 102 (PDF p. 114). Check: resolved.

Before:

> ते तदीशसमीपत्वं यान्ति स्वौचित्ययोगतः ॥

After:

> पशूनामेष वृत्तान्तो ये तु तत्तत्त्वदीक्षिताः ।
> ते तदीशसमीपत्वं यान्ति स्वौचित्ययोगतः ॥

- Settled from the KSTS page by the checker: Left page ('१०२ श्रीतन्त्रालोके ।', no verse number). After '...पुरस्तात्तूपदेक्ष्यते ॥ २६० ॥' comes Jayaratha's lead-in 'नन्वेवं ये न ज्ञानिनः, नापि पशवः, तेषां का वार्तेत्याशङ्क्य आह'. After it, in root type, come 'पशूनामेष वृत्तान्तो/ये तु तत्तत्त्वदीक्षिताः ।' and 'ते तदीशसमीपत्वं/यान्ति स्वौचित

### 26. TĀ 29.176 — partial

KSTS vol. XI, p. 118 (PDF p. 314). Check: confirm.

Before:

> मात्तैर्मानसतः स्वभावकुसुमैः स्वामोदसन्दोहिभिः ।
> आनन्दामृतनिर्भरस्वहृदयानर्घार्घपात्रक्रमात्
> त्वां देव्या सह देहदेवसदने देवार्चयेऽहर्निशम् ॥

After:

> कृत्वाधारधरां चमत्कृतिरसप्रोक्षाक्षणक्षालिता-
> मात्तैर्मानसतः स्वभावकुसुमैः स्वामोदसन्दोहिभिः ।
> आनन्दामृतनिर्भरस्वहृदयानर्घार्घपात्रक्रमात्
> त्वां देव्या सह देहदेवसदने देवार्चयेऽहर्निशम् ॥

- Moved from: Pada a "कृत्वाधारधरां चमत्कृतिरसप्रोक्षाक्षणक्षालिता-" stands in Tantraloka 29.176 (this note), Viveka, at the end of the Lead-in line (note line 38), after "...निजस्तोत्रैकदेशेन संवादयति-- ".
- Viveka of 29.176: the half-line «कृत्वाधारधरां चमत्कृतिरसप्रोक्षाक्षणक्षालिता-…» goes on its own `> ` line; the rest of that line stays as it is.

### 27. TĀ 30.96 — commentary in the Mūla

KSTS vol. XII, p. 212-213 (PDF p. 54). Check: confirm.

Before:

> फ्रेङ्कारः ।
> अग्निमण्डलमध्यस्थभैरवानलतापिताः ।
> वशमायान्ति शाकिन्यः स्थानमेतेन चेद्दहेत् ॥

After:

> अग्निमण्डलमध्यस्थभैरवानलतापिताः ।
> वशमायान्ति शाकिन्यः स्थानमेतेन चेद्दहेत् ॥

### 28. TĀ 31.104 — partial

KSTS vol. XII, p. 273 (PDF p. 115). Check: resolved.

Before:

> दैर्ध्यात्तूच्छ्रयतो वेदांगुला दैर्घ्याद्दशांगुला ॥

After:

> दैर्घ्यात्तूच्छ्रायाच्चोर्ध्वे च चतुरङ्गुलमानतः ।
> ऊर्ध्वेऽप्युच्छ्रायतो वेदाङ्गुला दैर्घ्याद्दशाङ्गुला ॥

- Settled from the KSTS page by the checker: The print settles it. KSTS p.273 prints 104 as two full half-lines in root type, between '...दण्डमूले तु पीठिका ॥१०३॥' and 'शूलमूलगतं पीठीमध्यं खाब्धिसमाङ्गुलम् ।' (105ab). No commentary comes between them, and the page has no footnotes. This matches GRETIL and confirms the aligner's eye-skip diagno

### 29. TĀ 33.27 — partial

KSTS vol. XII, p. 348-349 (PDF p. 190). Check: confirm.

Before:

> इति प्रदर्शितं पूर्वम् ....... ।
> .......ऽर्धमात्रासहत्वतः ।
> स्वरार्धमप्यस्ति यतः स्वरितस्यार्धमात्रकम् ॥

After:

> इति प्रदर्शितं पूर्वम् अर्धमात्रासहत्वतः ।
> स्वरार्धमप्यस्ति यतः स्वरितस्यार्धमात्रकम् ॥

### 30. TĀ 25.16 — commentary in the Mūla

KSTS vol. X, p. 321 (PDF p. 318). Check: confirm.

Before:

> तासां वामादीनां नाडीनां
> यस्य कस्यापि वा श्राद्धे गुरुदेवाग्नितर्पणम् ।
> स चक्रेष्टिः भवेच्छ्रैतो न तु स्यात्पाशवो विधिः ॥

After:

> यस्य कस्यापि वा श्राद्धे गुरुदेवाग्नितर्पणम् ।
> सचक्रेष्टि भवेच्छ्रौतो न तु स्यात्पाशवो विधिः ॥

- Reading checked on the page and in GRETIL: स चक्रेष्टिः → सचक्रेष्टि; भवेच्छ्रैतो → भवेच्छ्रौतो

