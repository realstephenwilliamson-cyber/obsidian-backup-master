# Phase 3 – dry run, batch 3 (Augustine 1-48 and 87)

Question B1 in *Phase 3 - decisions, batch 3*. Nothing here has been applied. The drafter's list comes first; the independent checker's report follows it.


Track 2, Augustine, batch 2 answers A5 ★ and A6 ★. Findings C1 / G20. Drafted 7 Oct 2026 against a copy of the notes as they stood before batch 2's question items (the vault as it will be just before these ops). **Nothing has been applied.** This list is for Stephen to approve; no second agent has re-read it yet.

## Counts

- **`ops.json`: 50 operations in 17 notes**, 23 footnote numbers, 26 pasted pieces of footnote text and 1 running head. 5,083 characters go in all. Every operation only deletes, **except two** (Tractate 38 `703` and Tractate 41 `751`), where the number sat between two words with no space on either side, so it is replaced by one space (see `unsure.md`, item 1).
  - **A5, Tractate 87: 15 operations.** The CCEL page read this time (one request, no refusal). 11 numbers (1451–1461) and 4 pasted pieces, which between them hold all 11 footnotes of the page. 282 characters.
  - **A6, Tractates 38–48: 28 operations in 9 notes.** 6 footnote numbers and 22 pasted pieces. The pieces hold parts of 24 of Innes's longer notes (most the end of a translator's note, "—Tr."); 705 is split over two places, and two places hold the ends of two notes each. 4,778 characters. Tractates 39 and 46 have nothing to remove: their CCEL notes are short (references, Latin words), and none of their text is in the notes.
  - **A6, the 7 strays in 1–37: 7 operations in 7 notes**: 6 footnote numbers (3, 6, 10, 19, 20, 26) and the running head inside "believed" in 11. 23 characters.
- **`extra-ops.json`: 10 more operations, not approved.** The pages for 10 and 11 show 10 more printed running heads ("1–5.") that the survey missed: one at the end of 10, nine in 11. They are the same kind as the approved one in 11 and are drafted the same way, but they are outside the ★ list, so they wait for your yes. They apply after `ops.json`.
- **Not drafted (in `unsure.md`):** the false heading `## §5` in 87 (CCEL has four sections) and the misplaced `## §5` in 11; five running heads "1–11." in 32 and 33 (pages not read).

## How it was checked

- **Pages.** 19 CCEL pages were read with WebFetch, one request each, about 20 seconds apart: 87, 38–48, and 3, 6, 10, 11, 19, 20, 26. None was refused or rate-limited. What each request returned is saved in `ccel/NNN.md`.
- **Numbers.** Each removed number is the number of the CCEL footnote marker at that place: either the tool quoted the marker there, or (87) the footnote is the reference for the quotation the number follows (1451 = 1 Tim. i. 5 after "faith unfeigned", 1459 = Ps. xi. 5 after "hateth his own soul", and so on). Where the marker is glued to the word (`cross,”[47]—He`), only the number goes. In 10 CCEL prints a space before the marker (`judgment; [257]—if`); the number and that space go, giving `judgment;—if`.
- **Pieces.** Each piece was compared with the CCEL footnote text, quotes, italics and Hebrew vowel points set aside: every one is the end (or, for 705, a middle part) of a CCEL footnote, word for word. Allowances, all inside text that is deleted anyway: in 87 the pasted references lack their book number ("Tim." for "1 Tim."); in 47 the pasted copy of 921 lacks the "2" of "Sec. 2", and the Hebrew of 906 is in a different order (the import wrapped each word in right-to-left marks); in 48 the tool did not copy note 947 (`unsure.md`, item 3).
- **Joins.** For every piece but one, the tool quoted CCEL's main text running straight from the words before the piece to the words after it, so nothing of the sermon is removed. The exception is 45 §9 (`unsure.md`, item 2), where the removed text is still word for word the end of note 853.
- **Operations.** `sim.py` on p3e (`notes.json`): 50 of 50 apply, then the 10 extra, 0 refused. Every `find` occurs once at its turn; each `replace` is its `find` with one stretch cut out (the two number→space ops aside); no removed stretch holds `#` or a block id; front matter, H1, callout, every heading line and block id are unchanged. After `ops.json` no 3- or 4-digit number and no "—Tr." is left in these bodies; after both files no running head is left in 10 and 11. No double space, space before punctuation or trailing space results. Track 7's 17 ops on these notes (navigation line under the H1) share no `find` with these and give the same result in either order.
- In the lists below, **bold** in the "before" line is exactly what goes (with a space next to it where the after line shows one gone); ¶ marks a paragraph break. Some Hebrew in 43 and 47 carries invisible right-to-left marks from the import; they go with the piece. The divine name occurs in none of the removed text.

## A5: Tractate 87

### Tractate 87

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.lxxxviii.html>. 11 numbers, 4 pieces; 15 operations.

1. §1, number 1451.
   - Before: …“Out of a pure heart, and a good conscience, and faith unfeigned.”**1451** So love we one another, and so love we God. For it would be with no…
   - After: …“Out of a pure heart, and a good conscience, and faith unfeigned.” So love we one another, and so love we God. For it would be with no…
2. §1, number 1452.
   - Before: …on these two commandments of love hang all the law and the prophets:**1452** this is our fruit. And it is in reference, therefore, to such fruit…
   - After: …on these two commandments of love hang all the law and the prophets: this is our fruit. And it is in reference, therefore, to such fruit…
3. §1, number 1453.
   - Before: …long-suffering, kindness, goodness, faith, meekness, temperance.”**1453** For who can truly rejoice who loves not good as the source of his…
   - After: …long-suffering, kindness, goodness, faith, meekness, temperance.” For who can truly rejoice who loves not good as the source of his…
4. §1, footnote text, 1451–1453.
   - Before: …needing to be commended, without which all other good things can **1451 Tim. i. 5. 1452 Matt. xxii. 40. 1453 Gal. v. 22.** be of no avail, and which cannot be possessed without bringing with…
   - After: …needing to be commended, without which all other good things can be of no avail, and which cannot be possessed without bringing with…
5. §2, number 1454.
   - Before: …it is said, “God was in Christ, reconciling the world unto Himself.”**1454** And this also: “The Son of man came not to condemn the world, but…
   - After: …it is said, “God was in Christ, reconciling the world unto Himself.” And this also: “The Son of man came not to condemn the world, but…
6. §2, number 1455.
   - Before: …to condemn the world, but that the world through Him might be saved.”**1455** And John says in his epistle: “We have an advocate with the Father,…
   - After: …to condemn the world, but that the world through Him might be saved.” And John says in his epistle: “We have an advocate with the Father,…
7. §2, number 1456.
   - Before: …and not for ours only, but also [for those] of the whole world.”**1456** The whole world then is the Church, and yet the whole world hateth…
   - After: …and not for ours only, but also [for those] of the whole world.” The whole world then is the Church, and yet the whole world hateth…
8. §3, number 1457.
   - Before: …wrath that are formed out of the same mass and fitted to destruction.**1457** Finally, after saying, “If ye were of the world, the world would…
   - After: …wrath that are formed out of the same mass and fitted to destruction. Finally, after saying, “If ye were of the world, the world would…
9. §3, number 1458.
   - Before: …“then is it no more of works: otherwise grace is no more grace.”**1458** 1454 Cor. v. 19. 1455 John iii. 17. 1456 John ii. 1, 2. 1457 Rom.…
   - After: …“then is it no more of works: otherwise grace is no more grace.” 1454 Cor. v. 19. 1455 John iii. 17. 1456 John ii. 1, 2. 1457 Rom.…
10. §3, footnote text, 1454–1458.
   - Before: …“then is it no more of works: otherwise grace is no more grace.” **1454 Cor. v. 19. 1455 John iii. 17. 1456 John ii. 1, 2. 1457 Rom. ix. 21, 23. 1458 Rom. xi. 5, 6.** ¶ ## §4 ^s4 ¶ But if we are asked about the love which is borne to…
   - After: …“then is it no more of works: otherwise grace is no more grace.” ¶ ## §4 ^s4 ¶ But if we are asked about the love which is borne to…
11. §4, number 1459.
   - Before: …itself truly. For he that loveth wickedness, hateth his own soul.**1459** And yet it is said to love itself, inasmuch as it loves the…
   - After: …itself truly. For he that loveth wickedness, hateth his own soul. And yet it is said to love itself, inasmuch as it loves the…
12. §4, number 1460.
   - Before: …thus, we are forbidden, when it is said to us, “Love not the world;”**1460** and we are commanded, when it is said to us, “Love your…
   - After: …thus, we are forbidden, when it is said to us, “Love not the world;” and we are commanded, when it is said to us, “Love your…
13. §4, number 1461.
   - Before: …and we are commanded, when it is said to us, “Love your enemies.”**1461** These constitute the world that hateth us. And therefore we are…
   - After: …and we are commanded, when it is said to us, “Love your enemies.” These constitute the world that hateth us. And therefore we are…
14. §4, footnote text, 1459 (first part).
   - Before: …it in a right manner, whereas it loves and hates itself perversely. **1459 Ps. xi.** ¶ ## §5 ^s5 ¶ See Tract. LXXXIII. sec. 3, note 4. 1460 John ii. 15.…
   - After: …it in a right manner, whereas it loves and hates itself perversely. ¶ ## §5 ^s5 ¶ See Tract. LXXXIII. sec. 3, note 4. 1460 John ii. 15.…
15. §5, footnote text, 1459 (rest)–1461. The whole text under the false heading §5; the heading stays (see unsure.md).
   - Before: …manner, whereas it loves and hates itself perversely. ¶ ## §5 ^s5 ¶ **See Tract. LXXXIII. sec. 3, note 4. 1460 John ii. 15. 1461 Luke vi. 27.** (end of note)
   - After: …manner, whereas it loves and hates itself perversely. ¶ ## §5 ^s5 (end of note)

## A6: Tractates 38–48

### Tractate 38

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xxxix.html>. 1 number, 3 pieces; 4 operations.

1. §7, footnote text, 694 (end).
   - Before: …they were brought now to despair. But He revived their hope; for He **and its cognate verb mundare. Such plays are frequent in St. Augustin.—Tr.** added, “If ye believe not that I am, ye shall die in your sins.”…
   - After: …they were brought now to despair. But He revived their hope; for He added, “If ye believe not that I am, ye shall die in your sins.”…
2. §11, number 703. Not a pure deletion: the number is replaced by one space. CCEL's copy shows a space before "[the Truth]", as in "Veritas [the Truth]" a line later (unsure.md, item 1).
   - Before: …Truth, and to their question, “Who art thou?” had answered, Veritatem**703**[the Truth]; when to the words, “Who art thou?” He evidently ought to…
   - After: …Truth, and to their question, “Who art thou?” had answered, Veritatem [the Truth]; when to the words, “Who art thou?” He evidently ought to…
3. §11, footnote text, 702 (end) + 705 (middle).
   - Before: …speak to you. But on this subject I have still much to say to you; **primum. So at least it sounded to Chrysostom. But Augustin’s interpretation is favored by Ambrose, Bernard, etc. be able to know and believe Him to be the beginning, the Eternal Alpha. Had He not become man and spoken** may it therefore please your Charity that we reserve what remains,…
   - After: …speak to you. But on this subject I have still much to say to you; may it therefore please your Charity that we reserve what remains,…
4. §11, footnote text, 705 (end).
   - Before: …we reserve what remains, and by His gracious aid deliver it tomorrow. **to them, but remained always hidden with the Father, and silent, they could never have had the means of knowing that He personally was the beginning, or believing Him such.—Tr.** (end of note)
   - After: …we reserve what remains, and by His gracious aid deliver it tomorrow. (end of note)

### Tractate 40

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xli.html>. 2 pieces; 2 operations.

1. §5, footnote text, 725 (end).
   - Before: …have smote on his ears, but they have produced no effect on his **illustration in an English version.—Tr.** mind. Why? Because he understood not. But if you have understood,…
   - After: …have smote on his ears, but they have produced no effect on his mind. Why? Because he understood not. But if you have understood,…
2. §10, footnote text, 735 (end).
   - Before: …yet be gathered into Thy barn. Temptations abound in the world, **as Engl. Vers.—Tr.** but greater is He who made the world. Temptations abound, but he…
   - After: …yet be gathered into Thy barn. Temptations abound in the world, but greater is He who made the world. Temptations abound, but he…

### Tractate 41

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xlii.html>. 1 number, 1 piece; 2 operations.

1. §6, number 751. Not a pure deletion: the number is replaced by one space. CCEL has "sins[751] by the law"; a pure deletion would give "sinsby" (unsure.md, item 1).
   - Before: …blood that [true] blood was prefigured, are themselves called sins**751**by the law; and that to such an extent that in certain passages it is…
   - After: …blood that [true] blood was prefigured, are themselves called sins by the law; and that to such an extent that in certain passages it is…
2. §8, footnote text, 751 (end).
   - Before: …from his sin?” He has greatly alarmed us, my brethren, by saying, **signify, the one, both trespass and trespass-offering, and the other, sin and sin-offering; indicating the thoroughness of the substitutionary idea.—Tr.** “The servant abideth not in the house for ever.” But He further adds,…
   - After: …from his sin?” He has greatly alarmed us, my brethren, by saying, “The servant abideth not in the house for ever.” But He further adds,…

### Tractate 42

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xliii.html>. 1 number, 1 piece; 2 operations.

1. §13, footnote text, 784 (end).
   - Before: …a liar, but not the father of the lie. But he, because he got not **Manichæans in support of their heresy, stated in section 10. The words “pater ejus” (ὁ πατὴρ αὐτοῦ), taken by themselves, might of course mean either “his father” or “the father of it” [i.e. of falsehood]. Both the Greek idiom and the context require the latter, but the Manichæans adopted the former, and made the passage run, “for he [i.e. the devil] is a liar, and [so is] his father.” Hence the question they are made to put afterwards, “Who was his [the devil’s] father?” and our author’s exposition of the passage.—Tr.** elsewhere the lie wherewith in serpent-form he slew man as if by…
   - After: …a liar, but not the father of the lie. But he, because he got not elsewhere the lie wherewith in serpent-form he slew man as if by…
2. §15, number 785.
   - Before: …Manicheans are accustomed to say, See, here there are two natures,**785**—the one good and the other bad; the Lord says it. What says the…
   - After: …Manicheans are accustomed to say, See, here there are two natures,—the one good and the other bad; the Lord says it. What says the…

### Tractate 43

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xliv.html>. 3 pieces; 3 operations.

1. §3, footnote text, 787 (end).
   - Before: …ye dishonor me.” That is, I honor not myself, that ye may not think **“Samaritan,” ‫שֹׁמְרֹנִי‬, a keeper, a guardian.—Tr.** me arrogant. I have One to honor; and did ye recognize me, just as I…
   - After: …ye dishonor me.” That is, I honor not myself, that ye may not think me arrogant. I have One to honor; and did ye recognize me, just as I…
2. §6, footnote text, 797 (end).
   - Before: …to know “if you love Him.” Job was unknown to himself, but he was **faciunt.** not unknown to God. He led the tempter into [Job], and brought him to…
   - After: …to know “if you love Him.” Job was unknown to himself, but he was not unknown to God. He led the tempter into [Job], and brought him to…
3. §9, footnote text, 800 (end) + 804 (end). CCEL prints notes 800 and 804 with the same text.
   - Before: …a servant, the difference is great between the glory of Christ and **facts and merits of a case, by sifting the evidence and separating the true from the false. facts and merits of a case, by sifting the evidence and separating the true from the false.** the glory of other men. Of that glory He spoke, when the…
   - After: …a servant, the difference is great between the glory of Christ and the glory of other men. Of that glory He spoke, when the…

### Tractate 44

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xlv.html>. 1 number, 1 piece; 2 operations.

1. §2, footnote text, 822 (end).
   - Before: …Are you a catechumen or a believer? If he reply, A catechumen; he **of church membership.** has been anointed, but not yet washed. But how anointed? Inquire, and…
   - After: …Are you a catechumen or a believer? If he reply, A catechumen; he has been anointed, but not yet washed. But how anointed? Inquire, and…
2. §17, number 843.
   - Before: …“Judge me, O God, and discern my cause against the unholy nation,”**843**—namely, those who say, “We see,” and their sin remaineth. But it was…
   - After: …“Judge me, O God, and discern my cause against the unholy nation,”—namely, those who say, “We see,” and their sin remaineth. But it was…

### Tractate 45

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xlvi.html>. 1 number, 3 pieces; 4 operations.

1. §7, footnote text, 851 (end).
   - Before: …as not to follow me, even when I give the explanation, yet should he **the Hebrew text. Our English version gives a pretty correct translation of the latter.—Tr.** not despair of himself; but continue in faith, walk on in the way,…
   - After: …as not to follow me, even when I give the explanation, yet should he not despair of himself; but continue in faith, walk on in the way,…
2. §9, footnote text, 853 (end). The join was not confirmed by the tool (it quoted another sentence); the removed text is word for word the end of CCEL note 853.
   - Before: …He came in the flesh, suffered, rose again, ascended into heaven: **The words, “πρὸ ἐμοῦ,” “before me,” of the received text, which are undoubtedly genuine, were wanting in the version here used by Augustin, just as in the Vulgate. It is supposed that the authors of these versions had been tempted to omit them, because of the use made of them by some early heretics to throw discredit on the Old Testament Scriptures.—Tr.** all this, just as you hear verbs of the past tense, we believe to be…
   - After: …He came in the flesh, suffered, rose again, ascended into heaven: all this, just as you hear verbs of the past tense, we believe to be…
3. §9, footnote text, 861 (end).
   - Before: …through the crier, the clerk does not make it, The crier said; but **or assemblies.—Tr.** the judge said. But others there are whom the sheep did not hear, in…
   - After: …through the crier, the clerk does not make it, The crier said; but the judge said. But others there are whom the sheep did not hear, in…
4. §15, number 880.
   - Before: …where they shall be filled who hunger and thirst after righteousness,**880**—such pasture as was found by him to whom it was said, “To-day shalt…
   - After: …where they shall be filled who hunger and thirst after righteousness,—such pasture as was found by him to whom it was said, “To-day shalt…

### Tractate 47

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xlviii.html>. 5 pieces; 5 operations.

1. §3, footnote text, 906 (end).
   - Before: …hath declared Him. In another place also He saith: “No one knoweth **from that of the present Hebrew text, with which our English version pretty closely agrees: “And thou shalt put a knife to thy throat, if thou art a man of appetite” (or perhaps, “if thou hast control over thy appetite,” ‫בעַל‬ ַּ ‫אִם־‬ ‫) נֶפֶשׁ אַתָּה‬. So somewhat similarly the Vulgate, which makes the last clause, “if thou hast power over thy life.”—Tr.** the Son, but the Father; neither knoweth any one the Father, save the…
   - After: …hath declared Him. In another place also He saith: “No one knoweth the Son, but the Father; neither knoweth any one the Father, save the…
2. §5, footnote text, 914 (end).
   - Before: …the corner-stone: all by way of comparison, none of them literally. **of Jerome, in the book on “Hebrew places,” and in Bede, in the names of places in the Acts of the Apostles; as likewise in the sacred history of Sulpitius Severus, Book ii.—Migne. The text is somewhat uncertain, but indicates the existence of “holy places” in Augustin’s day, and certain acts of worship performed in their honor.—Tr.** ¶ ## §6 ^s6 ¶ For I have said so before, and earnestly pressed it on…
   - After: …the corner-stone: all by way of comparison, none of them literally. ¶ ## §6 ^s6 ¶ For I have said so before, and earnestly pressed it on…
3. §7, footnote text, 919 (end).
   - Before: …you there was here a kind of failing in His power, so that, while **does not seem any real cause for such a supposition.—Tr.** He had it in His own power to die, He had it not in His power to rise…
   - After: …you there was here a kind of failing in His power, so that, while He had it in His own power to die, He had it not in His power to rise…
4. §9, footnote text, 921 (end) + 926 (end).
   - Before: …man as being flesh alone: but as man consists of flesh and soul, so, **by Augustin, any more than Prov. xxiii. 1, 2, similarly applied in Sec. of this lecture; and frequently elsewhere. But the accommodation at the will of the writer of all Old Testament Scripture equally to such a purpose was characteristic of the age.—Tr. either “soul” or “life.” The original also is ψύχη.—Tr.** in Christ there is a complete humanity. For He would not have assumed…
   - After: …man as being flesh alone: but as man consists of flesh and soul, so, in Christ there is a complete humanity. For He would not have assumed…
5. §10, footnote text, 927 (end).
   - Before: …and a time, after His assumption of that soul, when He was without **itive, and not a rational soul, and that His divine nature supplied the place of the latter. His doctrines were condemned by the Council of Alexandria, A.D. 362, and he himself was deposed by the Council of Rome, A.D. 378.—Tr.** a soul. I see, indeed, that the Word was once without a human soul,…
   - After: …and a time, after His assumption of that soul, when He was without a soul. I see, indeed, that the Word was once without a human soul,…

### Tractate 48

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xlix.html>. 1 number, 3 pieces; 4 operations.

1. §3, footnote text, 940 (end).
   - Before: …His stand on the human ground, and not on that where along with **after its profanation by Antiochus.—Tr.** the assumption of humanity He also continued Divine, He said to them,…
   - After: …His stand on the human ground, and not on that where along with the assumption of humanity He also continued Divine, He said to them,…
2. §5, footnote text, 946 (end).
   - Before: …We have entered by believing—we go out at death. But as we have **in this present life.—Tr.** entered by the door of faith, so, as believers, we quit the body; for…
   - After: …We have entered by believing—we go out at death. But as we have entered by the door of faith, so, as believers, we quit the body; for…
3. §6, number 949.
   - Before: …He also justified; and whom He justified, them He also glorified;”**949**—there is none of such sheep as these that the wolf seizes, or the…
   - After: …He also justified; and whom He justified, them He also glorified;”—there is none of such sheep as these that the wolf seizes, or the…
4. §6, footnote text, 947 (end). The tool did not copy note 947; it confirmed that "Far be it from us" runs straight on to "to suppose that the Lord Christ" in the main text.
   - Before: …there was a time when He was, and was not the Son. Far be it from us **our English version: “My Father who gave them me is greater than all.” The latter is certainly the more intelligible and suitable to the context. But the variation of the mss. between the two readings, “ὅ…μεῖζον” and “ὅς…μείζων,” is somewhat remarkable. The far larger number are certainly in favor of the latter, as followed by our English Bibles, but the former is countenanced by some of the more important; while others which have ὅς have at the same time μεῖζον (neut.) and vice versa. Thus the Sinaitic reads ὅ (neut.), and μεῖζων (masc.); while the Alexandrian has ὅς (masc.), and μεῖζον (neut.). The Vulgate, and some of the other early versions, have Augustin’s reading; but the Peshito (Syriac), which is the earliest of them all, supports the other, its literal rendering being, “For my Father, who gave to me, than all greater [is] He.” Modern critics have generally adopted the masc. reading,—Griesbach, Bengel, and others, almost ignoring the other, and Stier dismissing it as wholly inadmissible; while Alford, in a very strange and unsatisfactory way, gives the neuter in his Greek text, and not a syllable of explanation in his notes. It seems to us that the transcriber had first let ὅ creep into the text, perhaps from the previous similar expression in chap. vi. 39; and then μεῖζον was made neuter by some other to agree with it. This is more likely than the reverse; and our English reading is every way more satisfactory than Augustin’s.—Tr.** to suppose that the Lord Christ ever was, and yet was not the Son. Of…
   - After: …there was a time when He was, and was not the Son. Far be it from us to suppose that the Lord Christ ever was, and yet was not the Son. Of…

Tractates 39 and 46: nothing to remove (see Counts).

## A6: the 7 strays in 1–37

| Tractate | § | Removed | Before | After |
|---|---|---|---|---|
| 3 | §3 | `47` | …on of God, let him come down from the cross,”**47**—He, and no other, is our comp… | …on of God, let him come down from the cross,”—He, and no other, is our comp… |
| 6 | §8 | `126` | …e says, “The Lord know eth them that are His”**126**—are endued with different gra… | …e says, “The Lord know eth them that are His”—are endued with different gra… |
| 10 | §12 | `257` | …he four winds when He shall come to judgment; **257**—if, I say, you take these fou… | …he four winds when He shall come to judgment;—if, I say, you take these fou… |
| 11 | §3 | `1–5.` | …o had believed in His name. And why had he be**1–5.** lieved? He goes on, “For no ma… | …o had believed in His name. And why had he believed? He goes on, “For no ma… |
| 19 | §16 | `396` | …e the pure in heart, for they shall see God,”**396**—such a Judge will appear as m… | …e the pure in heart, for they shall see God,”—such a Judge will appear as m… |
| 20 | §2 | `407` | …e made; He commanded, and they were created,”**407**—how could He require rest aft… | …e made; He commanded, and they were created,”—how could He require rest aft… |
| 26 | §4 | `518` | …ay, “Every man is drawn by his own pleasure,”**518**—not necessity, but pleasure; … | …ay, “Every man is drawn by his own pleasure,”—not necessity, but pleasure; … |

CCEL pages: 3 <https://www.ccel.org/ccel/schaff/npnf107.iii.iv.html>, 6 <https://www.ccel.org/ccel/schaff/npnf107.iii.vii.html>, 10 <https://www.ccel.org/ccel/schaff/npnf107.iii.xi.html>, 11 <https://www.ccel.org/ccel/schaff/npnf107.iii.xii.html>, 19 <https://www.ccel.org/ccel/schaff/npnf107.iii.xx.html>, 20 <https://www.ccel.org/ccel/schaff/npnf107.iii.xxi.html>, 26 <https://www.ccel.org/ccel/schaff/npnf107.iii.xxvii.html>.

## Not approved: `extra-ops.json` (10 running heads in 10 and 11)

The survey listed only the running head inside "believed" in 11. Reading the pages for 10 and 11, these ten turned up as well. CCEL prints none of them in the main text: the tool quoted the main text running straight across each place, except item 5 of Tractate 11 below, where it quoted another sentence. They are drafted the same way, as pure deletions, and wait for your yes.

### Tractate 10

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xi.html>. 1 running head; 1 operation.

1. §13, running head. At the very end of the note; CCEL's main text ends at "servant.”".
   - Before: …always, The Lord be magnified, that wish the peace of His servant.” **1–5.** (end of note)
   - After: …always, The Lord be magnified, that wish the peace of His servant.” (end of note)

### Tractate 11

CCEL: <https://www.ccel.org/ccel/schaff/npnf107.iii.xii.html>. 9 running heads; 9 operations.

1. §2, running head.
   - Before: …and fell to the ground.” In this, that in answering them He threw **1–5.** them to the ground, He showed His power; that in His being taken by…
   - After: …and fell to the ground.” In this, that in answering them He threw them to the ground, He showed His power; that in His being taken by…
2. §4, running head. The false heading §5 that follows stays (see unsure.md).
   - Before: …own people, brought over through Himself? By His baptism He brings **1–** ¶ ## §5 ^s5 ¶ over them that believe; all their sins, the enemies as…
   - After: …own people, brought over through Himself? By His baptism He brings ¶ ## §5 ^s5 ¶ over them that believe; all their sins, the enemies as…
3. §5, running head.
   - Before: …thee will He be greater, but thou without Him wilt be less. Grow, **1–5.** therefore, in Him; do not withdraw thyself, that He may, as it were,…
   - After: …thee will He be greater, but thou without Him wilt be less. Grow, therefore, in Him; do not withdraw thyself, that He may, as it were,…
4. §7, running head.
   - Before: …the flood,—he in whom, and in his sons, the Church was prefigured? **1–5.** Borne by wood, they escaped the flood. Then afterwards great men whom…
   - After: …the flood,—he in whom, and in his sons, the Church was prefigured? Borne by wood, they escaped the flood. Then afterwards great men whom…
5. §8, running head. The tool did not confirm this join (it quoted another sentence).
   - Before: …there are four sorts. Either of the good are born good, or **1–5.** of the evil, are born evil; or of the good are born evil, or of the…
   - After: …there are four sorts. Either of the good are born good, or of the evil, are born evil; or of the good are born evil, or of the…
6. §10, running head.
   - Before: …Thou hast the Scripture openly declaring by the voice of God, “Jacob **1–5.** have I loved, but Esau have I hated.” Rebecca bare those two, Jacob…
   - After: …Thou hast the Scripture openly declaring by the voice of God, “Jacob have I loved, but Esau have I hated.” Rebecca bare those two, Jacob…
7. §11, running head.
   - Before: …neck, and wished to seduce his brother while he was playing with him. **1–5.** ¶ ## §12 ^s12 ¶ A great mystery is there. They were playing together,…
   - After: …neck, and wished to seduce his brother while he was playing with him. ¶ ## §12 ^s12 ¶ A great mystery is there. They were playing together,…
8. §13, running head.
   - Before: …bodily suffering, not the suffering of spiritual deception. Hear and **1–5.** see in the very facts of Old Testament history all the signs and…
   - After: …bodily suffering, not the suffering of spiritual deception. Hear and see in the very facts of Old Testament history all the signs and…
9. §14, running head.
   - Before: …by whom not three children, but the whole world, with these **1–5.** very kings, is delivered from the fire of hell! For those three…
   - After: …by whom not three children, but the whole world, with these very kings, is delivered from the fire of hell! For those three…



---

## Independent check


Folder: `aug-a6`. Checked 7 Oct 2026 against `notes.json`. For the 125 tractate notes, p3f has the same text as p3e.

### Result

- **Checked: 60 ops** (50 in `ops.json`, 10 in `extra-ops.json`). **Wrong: 0.** No corrected files were written.
- **sim.py on p3f:** all 50 ops in `ops.json` apply in order with none refused, and all 10 in `extra-ops.json` apply after them (they also apply alone). 5,083 characters are removed by `ops.json`. Front matter, H1, callout, `**John:**` line, every heading line and every block id are unchanged. No double space, space before punctuation or trailing space is added.
- **Each `replace` is its `find` with one stretch cut out.** The two exceptions are 38 `703` and 41 `751`, where the number becomes one space.
- **Track 7:** 17 of its ops touch these notes (both `t7-final-ops.json` and `batch2/t7-ready-ops.json`). None shares a `find` with these ops, all apply after them, and the result is the same in either order.

### Pages re-read

- **Re-read with WebFetch, one request each, 20 seconds apart (7 pages):** 87, 38, 40, 41, 42, 43, 44.
- **8th request, Tractate 45: refused.** The WebFetch model declined to copy the text, calling it copyrighted. I stopped fetching at that point and used no other route.
- **So these were checked only against the drafter's saved copies (`ccel/NNN.md`):** 45 (ops 31–34), 47 (35–39), 48 (40–43), the 7 strays in 3, 6, 10, 11, 19, 20, 26 (44–50), and all 10 extra ops. That is 20 of the 50 ops and all 10 extras. The other 30 ops (87, 38, 40–44) were checked against my own reading as well.
- **Note on 87:** the A5 ★ allowed one request for that page. Mine was a second request, made because the lead's task asked me to re-read every page. It was not refused or rate-limited.

### Points for the lead (none makes an op wrong)

1. **45 §9 (op 32): the join is still not confirmed on CCEL.** The drafter's reading quoted a different sentence, and mine was refused. What the evidence does show:
   - The removed piece is word for word the end of note 853 in the saved copy, from a sentence start ("The words, "πρὸ ἐμοῦ,"…") to "—Tr.". So no sermon text is removed.
   - The remaining sentence reads straight on: `…rose again, ascended into heaven: all this, just as you hear verbs of the past tense, we believe to be already fulfilled.` The next sentence repeats the same list in the future tense (`would suffer, would rise again, would ascend into heaven`).
   - What is unconfirmed is whether CCEL's wording at this join is exactly what remains. The op cannot change that wording, since it only deletes footnote text.
2. **Extra op x6 (11 §8, `born good, or 1–5. of the evil`): the join is not confirmed.** The saved reading quoted another sentence. "1–5." is the running head (11's passage is John 2:23–25; 3:1–5), so it is not Augustine's text in any case.
3. **38 `703` and 41 `751` (number → space): confirmed.**
   - My copies show a space after the marker: `*Veritatem*[703](…) [the Truth]` and `*sins*[751](…)[751](…) by the law`.
   - The tool's own comment said "no space" both times, so its copy and its comment disagree. I followed the copy.
   - English also needs the space in 41 (`sinsby`), and 38 has `Veritas [the Truth]` a line later.
4. **10 §12 `257` (op 46): this is a choice about one space.**
   - CCEL prints `judgment; [257]—if`. Taking out only the marker would give `judgment; —if`.
   - The op also removes the space before the marker, giving `judgment;—if`. That matches the other dashes in these ops (`cross,"—He`). The drafter flagged this (unsure item 7).
   - Not counted wrong. If you want CCEL's spacing exactly, change the op's `replace` to `when He shall come to judgment; —if, I say`.
5. **87: two marker places are loose in both readings.**
   - My reading put 1451 before the quotation (`explains to be,[1451] Out of a pure heart`) and 1458 before "For He who chose". It also ended §3 at "what He should choose:", which leaves out the quotation that follows.
   - The ops are still right: all 11 numbers in the note are on the page's footnote list (1451–1461). Each one in the vault follows the quotation its reference names (1451 1 Tim. i. 5 after "faith unfeigned", 1458 Rom. xi. 5, 6 after "grace is no more grace"). The ops remove only the digits.
   - Confirmed in my reading: `can be of no avail`; §4 begins "But if we are asked about the love"; the main text ends "hates itself perversely."; CCEL has 4 sections and no §5.
6. **42 §15 `785`:** my reading copied `two natures[785] —the one` without the comma, while the drafter's had `natures,`. The op removes only the digits and leaves the vault's comma. That is outside this op.
7. **48 note 947 (op 43): still not copied by any reading.**
   - The removed piece is the translator's matter by its content. It speaks of "Augustin's reading", "our English Bibles", the Sinaitic and Alexandrian manuscripts, and Griesbach, Bengel, Stier and Alford, and it ends "—Tr.".
   - The drafter's reading confirmed that the main text runs `Far be it from us to suppose that the Lord Christ ever was`.
   - That it is footnote matter is established. That it is note 947 in particular is not.
8. **Leftovers I agree should stay out of these ops (drafter's unsure items 4–6):** the empty `## §5 ^s5` at the end of 87, the misplaced `## §5` in 11, and five "1–11." running heads in 32 and 33.
9. **Not in the drafter's list (vault only, pages not read, unverified):** running heads printed `1-11.` (hyphen) remain after the earlier 49–124 cleanup:
   - 121, at the end: `…on the topics that remain. 1-11.`
   - 122, five places: `rose 1-11. again`, `receive 1-11. the wages`, `went up, 1-11. and drew`, `the good 1-11. alone`, `Let 1-11. the spirit`. 122's passage is John 20:30–31; 21:1–11.
   - A scan of all 124 notes after both op files finds no other "—Tr." or footnote number. The bare numbers left are verse citations in the text such as `(ver. 25)`.

### Every op

"Footnote matter" says what the removed piece is and how that is known. "Join" says what shows that the words on each side run on as CCEL's main text has them. "(mine)" is my own reading; "saved" is the drafter's copy. In "Removed", `¶` is a line break and long pieces are shortened with "…".

### `ops.json`

| # | Tr. | Removed | Footnote matter | Join | Checked against | Verdict |
|---|---|---|---|---|---|---|
| 1 | 87 | `1451` | marker 1451 (1 Tim. i. 5) | reading loose on place; number is on page list | re-read | right |
| 2 | 87 | `1452` | marker 1452 | `prophets:[1452] this is our fruit` (mine) | re-read | right |
| 3 | 87 | `1453` | marker 1453 | `temperance."[1453] For who can truly` (mine) | re-read | right |
| 4 | 87 | `1451 Tim. i. 5. 1452 Matt. xxii. 40. 1453 Gal. v. 22.` | text of notes 1451–1453 | `good things can be of no avail` (mine) | re-read | right |
| 5 | 87 | `1454` | marker 1454 | `unto Himself."[1454] And this also` (mine) | re-read | right |
| 6 | 87 | `1455` | marker 1455 | `be saved."[1455] And John says` (mine) | re-read | right |
| 7 | 87 | `1456` | marker 1456 | `whole world."[1456] The whole world` (mine) | re-read | right |
| 8 | 87 | `1457` | marker 1457 | `destruction.[1457] Finally, after saying` (mine) | re-read | right |
| 9 | 87 | `1458` | marker 1458 (Rom. xi. 5, 6) | reading loose on place; follows the Rom. xi. 6 quotation | re-read | right |
| 10 | 87 | `1454 Cor. v. 19. 1455 John i … 1, 23. 1458 Rom. xi. 5, 6.` | text of notes 1454–1458 | §4 begins "But if we are asked" (mine); §3 end as drafter | re-read | right |
| 11 | 87 | `1459` | marker 1459 | `own soul.[1459]` (mine) | re-read | right |
| 12 | 87 | `1460` | marker 1460 | `the world;"[1460] and we are commanded` (mine) | re-read | right |
| 13 | 87 | `1461` | marker 1461 | `your enemies."[1461] These constitute` (mine) | re-read | right |
| 14 | 87 | `1459 Ps. xi.` | text of note 1459, first part | main text ends "hates itself perversely." (mine) | re-read | right |
| 15 | 87 | `See Tract. LXXXIII. sec. 3,  …  ii. 15. 1461 Luke vi. 27.` | text of notes 1459 (rest)–1461 | 4 sections, no §5 (mine); empty heading stays | re-read | right |
| 16 | 38 | `nd its cognate verb mundare. … ent in St. Augustin.—Tr. a` | end of note 694 (mine) | `for He added, "If ye believe not` (mine) | re-read | right |
| 17 | 38 | `703` → space | marker 703 → space | `Veritatem[703] [the Truth]` (mine, see point 3) | re-read | right |
| 18 | 38 | `primum. So at least it sound …  not become man and spoken` | end of 702 + middle of 705 (mine) | `much to say to you; may it therefore please` (mine) | re-read | right |
| 19 | 38 | `to them, but remained always … or believing Him such.—Tr.` | end of note 705 (mine) | main text ends "deliver it tomorrow." (mine) | re-read | right |
| 20 | 40 | `illustration in an English version.—Tr.` | end of note 725 (mine) | `effect on his mind. Why?` (mine) | re-read | right |
| 21 | 40 | `as Engl. Vers.—Tr.` | end of note 735 (mine) | `in the world, but greater is He` (mine) | re-read | right |
| 22 | 41 | `751` → space | marker 751 → space | `sins[751] by the law` (mine, see point 3) | re-read | right |
| 23 | 41 | `signify, the one, both tresp …  substitutionary idea.—Tr.` | end of note 751 (mine) | `by saying, "The servant abideth` (mine) | re-read | right |
| 24 | 42 | `Manichæans in support of the … sition of the passage.—Tr.` | end of note 784 (mine) | `got not elsewhere the lie` (mine) | re-read | right |
| 25 | 42 | `785` | marker 785 | `natures[785] —the one good` (mine; comma, point 6) | re-read | right |
| 26 | 43 | `“Samaritan,” ‫שֹׁמְרֹנִי‬, a keeper, a guardian.—Tr.` | end of note 787 (mine) | `not think me arrogant` (mine) | re-read | right |
| 27 | 43 | `faciunt.` | end of note 797 (mine) | `but he was not unknown to God` (mine) | re-read | right |
| 28 | 43 | `facts and merits of a case,  … g the true from the false.` | ends of notes 800 + 804 (mine; same text) | `glory of Christ and the glory of other men` (mine) | re-read | right |
| 29 | 44 | `of church membership.` | end of note 822 (mine) | `A catechumen; he has been anointed` (mine) | re-read | right |
| 30 | 44 | `843` | marker 843 | `nation,"[843] —namely` (mine) | re-read | right |
| 31 | 45 | `the Hebrew text. Our English … slation of the latter.—Tr.` | end of note 851 (saved) | saved join confirmed | saved only | right |
| 32 | 45 | `The words, “πρὸ ἐμοῦ,” “befo …  Testament Scriptures.—Tr.` | end of note 853 (saved) | NOT CONFIRMED in either reading (point 1) | saved only | right; join unconfirmed |
| 33 | 45 | `or assemblies.—Tr.` | end of note 861 (saved) | saved join confirmed | saved only | right |
| 34 | 45 | `880` | marker 880 | saved `righteousness,[880]—such pasture` | saved only | right |
| 35 | 47 | `from that of the present Heb …  power over thy life.”—Tr.` | end of note 906 (saved; Hebrew order differs) | saved join confirmed | saved only | right |
| 36 | 47 | `of Jerome, in the book on “H … formed in their honor.—Tr.` | end of note 914 (saved) | saved: §5 ends "literally." | saved only | right |
| 37 | 47 | `does not seem any real cause for such a supposition.—Tr.` | end of note 919 (saved) | saved join confirmed | saved only | right |
| 38 | 47 | `by Augustin, any more than P … original also is ψύχη.—Tr.` | ends of notes 921 + 926 (saved; "Sec." lacks "2") | saved join confirmed | saved only | right |
| 39 | 47 | `itive, and not a rational so … cil of Rome, A.D. 378.—Tr.` | end of note 927 (saved; "itive" = tail of "sensitive") | saved join confirmed | saved only | right |
| 40 | 48 | `after its profanation by Antiochus.—Tr.` | end of note 940 (saved) | saved join confirmed | saved only | right |
| 41 | 48 | `in this present life.—Tr.` | end of note 946 (saved) | saved join confirmed | saved only | right |
| 42 | 48 | `949` | marker 949 | saved `glorified;"[949]—there is none` | saved only | right |
| 43 | 48 | `our English version: “My Fat … ctory than Augustin’s.—Tr.` | note 947 not copied; translator's matter by content (point 7) | saved join confirmed | saved only | right; note number unconfirmed |
| 44 | 3 | `47` | marker 47 | saved: marker after `cross,"`; words after not shown | saved only | right |
| 45 | 6 | `126` | marker 126 | saved `His"[126] … —are endued` | saved only | right |
| 46 | 10 | `257` | marker 257 + space before it | saved `judgment; [257]—if` (point 4) | saved only | right |
| 47 | 11 | `1–5.` | running head "1–5." (John 3:1–5) | saved `why had he believed? He goes on` | saved only | right |
| 48 | 19 | `396` | marker 396 | saved `God,"[396] —such a Judge` | saved only | right |
| 49 | 20 | `407` | marker 407 | saved `created,"[407] —how could He` | saved only | right |
| 50 | 26 | `518` | marker 518 | saved `pleasure,"[518] … —not necessity` | saved only | right |

### `extra-ops.json` (not approved; apply after `ops.json`)

| # | Tr. | Removed | Footnote matter | Join | Checked against | Verdict |
|---|---|---|---|---|---|---|
| x1 | 10 | `1–5.` | running head "1–5." | saved: main text ends `servant."` | saved only | right |
| x2 | 11 | `1–5.` | running head "1–5." | saved join b | saved only | right |
| x3 | 11 | `1–` | running head "1–5." | saved join c | saved only | right |
| x4 | 11 | `1–5.` | running head "1–5." | saved join d | saved only | right |
| x5 | 11 | `1–5.` | running head "1–5." | saved join e | saved only | right |
| x6 | 11 | `1–5.` | running head "1–5." | NOT CONFIRMED (saved f quoted another sentence) | saved only | right; join unconfirmed |
| x7 | 11 | `1–5.` | running head "1–5." | saved join g | saved only | right |
| x8 | 11 | `1–5.` | running head "1–5." | saved: §11 ends "playing with him." | saved only | right |
| x9 | 11 | `1–5.` | running head "1–5." | saved join h | saved only | right |
| x10 | 11 | `1–5.` | running head "1–5." | saved join i | saved only | right |
