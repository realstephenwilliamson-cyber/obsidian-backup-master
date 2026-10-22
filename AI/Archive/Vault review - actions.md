---
type: actions
cssclasses:
  - wide
---
# Vault review - actions

From the whole-vault review on 4 October 2026. Everything here waits for you. **Each button does nothing until you click it twice.** Renames go through Obsidian, so links follow. Anything removed goes to the vault's `.trash` folder, so nothing is lost until you empty it. When a button has run, it is replaced by a line saying what it did and when. When everything you want is done, delete this note.

The fixes that needed no decision are already made; they are listed at the end.

## 1. Recommended

### Turn Templater back on
Templater is installed and set up correctly, but it is switched off. Home's buttons ("Start today's note", "Start this week's note", "Start a homily for …") and new notes in Journal, Writing/Homilies, Notes/Concepts and Notes/Hubs depend on it. With it off they are created **empty**: that is why `Writing/Homilies/2026-10-04 Proper 22A` is blank. This button turns Templater on and fills any empty note in those folders from its template.
- [x] Done: 2026-10-04 21:41 — Templater is on; filled from its template: 2026-10-04 Proper 22A

## 2. Redundant notes

### Two empty Stiegler stubs
`Notes/The Future of Work 2017` has only four properties (it repeats the catalog note *Stiegler - Automatic Society 1*), and `Notes/Bernard Stiegler` is empty. This removes both and the "See also" link to the first.
- [x] Done: 2026-10-04 21:41 — 1 link removed; The Future of Work 2017.md moved to .trash; Bernard Stiegler.md moved to .trash

### Duplicate catalog note: Dawning of the Cycles of Consciousness (annotated)
Identical notes exist in `Catalog/Trika` and `Catalog/Other` for the same PDF. This removes the copy in Other; links go to the Trika note.
- [x] Done: 2026-10-04 21:42 — Dyczkowski - Dawning of the Cycles of Consciousness (annotated).md moved to .trash

### Stiegler single-volume notes in Catalog/Other
*Technics and Time 2* and *Symbolic Misery 1* each have a note in `Catalog/Other` (subject "Other", from an early automatic pass) as well as a place in the set notes in `Catalog/Philosophy`, so they are counted twice. This drops them from the "Also in your library" lists, points any other links to the set notes, and removes the two singles.
- [x] Done: 2026-10-04 21:42 — 29 notes updated; Technics and Time, 2 Disorientation (Meridian Crossing Aesthetics).md moved to .trash; Symbolic Misery, Volume One The Hyperindustrial Epoch.md moved to .trash

### Lectionary duplicates: Baptism of the Lord
`Epiphany-BaptismA/B/C` and `Baptism-of-LordA/B/C` are identical. The study plan and homily template use `Baptism-of-Lord`; only the RCL Index row uses the other. This points the index at `Baptism-of-Lord` and removes the three `Epiphany-Baptism` notes.
- [x] Done: 2026-10-04 21:42 — 3 index links re-pointed; Epiphany-BaptismA.md moved to .trash; Epiphany-BaptismB.md moved to .trash; Epiphany-BaptismC.md moved to .trash

### Vault Archival and Stale Files Guide
A note from the crashed session. Most of the files it lists are not in `Writing/_Originals`, and its advice is now in the Vault Guide.
- [x] Done: 2026-10-04 21:43 — Vault Archival and Stale Files Guide.md moved to .trash

### Empty folder Library/Books
- [x] Done: 2026-10-04 21:43 — Books moved to .trash

## 3. Two copies of the same work

Keep one file of each, remove the other from its catalog note and send it to `.trash`.

- **Kubjikā the Erotic Goddess:** keep the 18-page text PDF; remove `Kubjikaa_the_Erotic_Goddess.pdf` (11-page scan, no text, 4.9 MB).
- [x] Done: 2026-10-04 21:43 — Kubjikaa_the_Erotic_Goddess.pdf moved to .trash
- **The Cult of the Goddess Kubjikā:** keep the Nepal Research Centre text PDF; remove `The_Cult_of_the_Goddess_Kubjika2.pdf` (scan, no text, no title pages, 14.8 MB).
- [x] Done: 2026-10-04 21:43 — The_Cult_of_the_Goddess_Kubjika2.pdf moved to .trash
- **Saṃvitprakāśa:** keep the Internet Archive copy (searchable English, 4.5 MB); remove the 26 MB scan without text.
- [x] Done: 2026-10-04 21:43 — Mark Dyczkowski - The Samvit Prakash of Vamanadatta-Sampurnanand Sanskrit University (1990).pdf moved to .trash
- **Russell, *History of Western Philosophy*:** keep the Touchstone 1967 file (5.2 MB); remove the "second copy" from the phone (4.3 MB).
- [x] Done: 2026-10-04 21:43 — Bertrand Russell - A History of Western Philosophy (second copy).pdf moved to .trash

## 4. Names

### Tidy 85 file names
Shortens the 33 files whose full path is over 220 characters (four are at or over Windows' 260-character limit, which can trip backups, sync and copying), drops leftover " (1)" and " copy" endings where no other copy exists, and removes double spaces and stray publisher tails from catalog note names. The new names follow the library pattern `Author - Short title (year)`. Catalog links follow automatically.
- [x] Done: 2026-10-04 21:44 — 85 renamed

> [!info]- The 85 renames (old → new)
> | Now | Becomes |
> |---|---|
> | `(SUNY series in Shaiva traditions of Kashmir) Vasugupta._ Mark S G Dyczkowski - The Stanzas on vibration _ the Spandakarika with four commentaries _ the spandasamdoha by Ksemaraja, the Spandavrtti .pdf` | `Dyczkowski (tr.) - The Stanzas on Vibration, the Spandakarika with Four Commentaries.pdf` |
> | `(SUNY series in Tantric studies) Debabrata Sen Sharma - The philosophy of sadhana _ with special reference to the Trika philosophy of Kashmir-State University of New York Press (1990) (1).pdf` | `Sen Sharma - The Philosophy of Sadhana (SUNY 1990).pdf` |
> | `Abhinavagupta, Rajanaka._ Baumer, Bettina - Abhinavagupta's hermeneutics of the absolute Anuttaraprakriya _ an interpretation of his Paratrisika Vivarana-D.K. Printworld, Indian Institute of Advanced .pdf` | `Baumer - Abhinavagupta's Hermeneutics of the Absolute, Anuttaraprakriya.pdf` |
> | `Ksemaraja_Wallis, Christopher D - The Recognition Sutras_ a complete translation and explanation of the 1,000-year-old spiritual masterpiece the Pratyabhijna-hrdaya by Rajanaka Ksemaraja-Mattamayura.pdf` | `Wallis - The Recognition Sutras (Pratyabhijna-hrdaya of Ksemaraja).pdf` |
> | `Paratrisika-vivarana_ The Secret Of Tantric Mysticism Secret -- Abhinavagupta; English translation, with notes and running -- New Ed edition, December -- 9788120804623 -- 7f053dc8915ef221a202a90f00a22aba -- Anna's .pdf` | `Singh (tr.) - Paratrisika-vivarana, The Secret of Tantric Mysticism.pdf` |
> | `Swami Lakshmanjoo, John Howard Hughes - The Mystery of Vibrationless-Vibration in Kashmir Shaivism_ Vasugupta's Spanda Karika & Kshemaraja's Spanda Sandoha-Universal Shaiva Fellowship (2016).pdf` | `Lakshmanjoo, Hughes - The Mystery of Vibrationless-Vibration in Kashmir Shaivism (2016).pdf` |
> | `Rediscovering God with Transcendental Argument _ A -- David Peter Lawrence; Paul J_ Griffiths; Laurie L_ Patton -- State University of New York Press, -- 9780585090900 -- f375afcf6cdb510698666c915ce1d154 -- Anna's .pdf` | `Lawrence - Rediscovering God with Transcendental Argument (SUNY 1999).pdf` |
> | `(Suny Series in the Shaiva Traditions of Kashmir) Mark S. G. Dyczkowsk - Canon of the Saivagama and the Kubjika Tantras of the Western Kaula Tradition-State University of New York (1988).pdf` | `Dyczkowski - The Canon of the Saivagama and the Kubjika Tantras (SUNY 1988).pdf` |
> | `(Suny Series in the Shaiva Traditions of Kashmir) Lilian Silburn - Kundalini_ The Energy of the Depths_ A Comprehensive Study Based on the Scriptures of Nondualistic Kasmir Saivism-State University of.pdf` | `Silburn - Kundalini, The Energy of the Depths (SUNY).pdf` |
> | `(SUNY Series in the Shaiva Traditions of Kashmir) Andre Padoux, Jacques Gontier (Translator) - Vac_ The Concept of the Word in Selected Hindu Tantras-State University of New York Press (1990).pdf` | `Padoux - Vac, The Concept of the Word in Selected Hindu Tantras (SUNY 1990).pdf` |
> | `(Suny series in tantric studies) Teun Goudriaan (Editor) - Ritual and Speculation in Early Tantrism_ Studies in Honor of Andre Padoux-State  University  of  New  York  Press (1992).pdf` | `Goudriaan (ed.) - Ritual and Speculation in Early Tantrism (1992).pdf` |
> | `(Serie Orientale Roma LXXI) Raffaelle Torella - The Ishvarapratyabhijnakarika of Utpaladeva with the Author's Vrtti_ Critical edition and annotated translation-Istituto Italiano Per Il Medio Ed Estrem.pdf` | `Torella - The Isvarapratyabhijnakarika of Utpaladeva with the Author's Vrtti (SOR 71).pdf` |
> | `(Nepal Research Centre publications, 23) Mark S G Dyczkowski - The Cult of the Goddess Kubjika, A Preliminary Comparative Textual and Anthropological Survey of a Secret Newar Goddess-Franz Steiner Ver.pdf` | `Dyczkowski - The Cult of the Goddess Kubjika (Nepal Research Centre 23).pdf` |
> | `(Nepal Research Centre Publications, 22.) Mark S G Dyczkowski - Kubjika, Kali, Tripura, and Trika-Franz Steiner Verlag (2000) (1).pdf` | `Dyczkowski - Kubjika, Kali, Tripura and Trika (Nepal Research Centre 22, 2000).pdf` |
> | `(Routledge studies in tantric traditions) Bansat-Boudon, Lyne_Tripathi, Kamalesha Datta - The Paramarthasara of Abhinavagupta and its commentary by Yogaraja-Routledge (2014).pdf` | `Abhinavagupta, Yogaraja - An Introduction to Tantric Philosophy (2011).pdf` |
> | `(Suny Series in Tantric Studies) Mark S. G. Dyczkowski - The Aphorisms of Siva_ The Sivasutra With Bhaskara's Commentary, the Varttika-State University of New York Press (1992).pdf` | `Dyczkowski (tr.) - The Aphorisms of Siva, the Sivasutra with Bhaskara's Varttika (SUNY 1992).pdf` |
> | `Manthanabhairavatantram _ Kumarikakhandah _ the section concerning the virgin goddess of the Tant...{Mark S. G. Dyczkowski}(2009, D.K. Printworld Pvt. Ltd.){113995016} libgen.li.pdf` | `Dyczkowski (ed. and tr.) - The Kumarikakhanda of the Manthanabhairavatantra (2009).pdf` |
> | `John R. Dupuche - Abhinavagupta_ The Kula Ritual as Elaborated in Chapter 29 of the Tantraloka  -Motilal Banarsidass (2003).pdf` | `Dupuche - Abhinavagupta, The Kula Ritual as Elaborated in Chapter 29 of the Tantraloka (2003).pdf` |
> | `The Kubjikamatatantra  Kulalikamnaya version by by T. Goudriaan and J.A. Schoterman. (z-lib.org).pdf` | `Goudriaan, Schoterman (eds.) - The Kubjikamatatantra (1988).pdf` |
> | `The Satsahasra samhita  chapters 1-5.pdf` | `The Satsahasra Samhita, chapters 1-5.pdf` |
> | `own_being .pdf` | `Wilberg - Absolute Awareness or Absolute Egoity.pdf` |
> | `Daniel Odier, Clare Frock - Yoga Spandakarika_ the sacred texts at the origins of Tantra  -Inner Traditions (2005).pdf` | `Odier, Frock - Yoga Spandakarika, the Sacred Texts at the Origins of Tantra (2005).pdf` |
> | `An early Upanisadic reader _ with notes, glossary and an -- Henrich Hans Hock -- Bilingual, PS, 2006 -- Motilal Banarasidass, Delhi -- 9788120832138 -- 014c93f96a07131357e3d7dbe73e0af6 -- Anna's Archive.pdf` | `Hock - An Early Upanisadic Reader (2006).pdf` |
> | `A Vedic reader for students _ containing thirty hymns of the -- Macdonell, Arthur Anthony, 1854-1930 -- New Ed edition, 1992 -- Delhi _ Motilal -- 9788120810174 -- d39f429d1f8e05e249bac6e07aa6703e -- Anna's Archive.pdf` | `Macdonell - A Vedic Reader for Students (1992 reprint).pdf` |
> | `Jan Gonda_ Gordon B. Ford (Translator) - A Concise Elementary Grammar of the Sanskrit Language_ With Exercises, Reading Selections, and a Glossary_ With Exercises, Reading Selections and Glossary  -Br.pdf` | `Gonda, Ford (tr.) - A Concise Elementary Grammar of the Sanskrit Language.pdf` |
> | `The Complete Correspondence, 1928-1940 -- Theodor W Adorno; Walter Benjamin; Henri Lonitz -- 2_ printing, Cambridge, Mass, 2000 -- Harvard University, -- 9780674006898 -- 441516fa4a660233a06056f211cf0c4e -- Anna's .pdf` | `Adorno, Benjamin - The Complete Correspondence 1928-1940 (2000).pdf` |
> | `Thomas Hobbes, Deborah Baumgold (ed.) - Three-Text Edition of Thomas Hobbes's Political Theory_ The Elements of Law, De Cive and Leviathan-Cambridge University Press (2017).pdf` | `Hobbes, Baumgold (ed.) - Three-Text Edition of Thomas Hobbes's Political Theory (2017).pdf` |
> | `Jean-Luc Nancy - On Bernard Stiegler_ Philosopher of Friendship-Bloomsbury Academic (2024) (1).pdf` | `Nancy - On Bernard Stiegler, Philosopher of Friendship (2024).pdf` |
> | `1717442d89c422f478b4ddaab223f535 (1).PDF` | `Somers-Hall - Deleuze and Merleau-Ponty.pdf` |
> | `societies-02-00357-v2 (1).pdf` | `de Ville - Deconstructing the Leviathan (2012).pdf` |
> | `Robin George Collingwood - The new Leviathan_ or, Man, society, civilization and barbarism  -Clarendon Press (1944).pdf` | `Collingwood - The New Leviathan (1944).pdf` |
> | `Daniel W. Graham (editor and translator) - The Texts of Early Greek Philosophy The Complete Fragments and Selected Testimonies of the Major Presocratics. 2-Cambridge (2010).pdf` | `Graham (tr.) - The Texts of Early Greek Philosophy (2010).pdf` |
> | `Buber, Martin - Prophetic Faith (Harper & Row, 1960) copy.pdf` | `Buber - Prophetic Faith (1960).pdf` |
> | `Bernard Stiegler_ Daniel Ross, Suzanne Arnold (transl.) - The Decadence of  Industrial Democracies. Disbelief and Discredit, Volume 1 1(2011, Polity) - libgen.lc.pdf` | `Stiegler - The Decadence of Industrial Democracies, Disbelief and Discredit 1 (2011).pdf` |
> | `Bart Buseyne, Georgios Tsagdis, Paul Willemarck - Bernard Stiegler_ Memories of the Future-Bloomsbury Academic (2024) (1).pdf` | `Buseyne, Tsagdis, Willemarck (eds.) - Bernard Stiegler, Memories of the Future (2024).pdf` |
> | `(Routledge Studies in Contemporary Philosophy) Mark Coeckelbergh - Green Leviathan or the Poetics of Political Liberty_ Navigating Freedom in the Age of Climate Change and Artificial Intelligence-Rout.pdf` | `Coeckelbergh - Green Leviathan or the Poetics of Political Liberty.pdf` |
> | `(Routledge Studies in Contemporary Philosophy) John J. Davenport - Narrative Identity, Autonomy, and Mortality_ From Frankfurt and MacIntyre to Kierkegaard-Routledge (2012) (1).pdf` | `Davenport - Narrative Identity, Autonomy, and Mortality (2012).pdf` |
> | `(Media, Culture and Critique_ Future Imperfect) Ross Abbinnett - The Thought of Bernard Stiegler_ Capitalism, Technology and the Politics of Spirit-Routledge (2017) (1).pdf` | `Abbinnett - The Thought of Bernard Stiegler (2017).pdf` |
> | `(Publications of the de Nobili Research Library) Alex Watson - The Self's Awareness of Itself_ Bhatta Ramakantha's Arguments Against the Buddhist Doctrine of No-Self-Institut fur Sudasien-, Tibet- und.pdf` | `Watson - The Self's Awareness of Itself, Bhatta Ramakantha against the Buddhist No-Self.pdf` |
> | `NumberSystems4 (1).pdf` | `NumberSystems4.pdf` |
> | `(Routledge Studies in Religion) Richard G. Marks - Jewish Approaches to Hinduism_ A History of Ideas from Judah Ha-Levi to Jacob Sapir (12th-19th centuries)-Routledge (2021).pdf` | `Marks - Jewish Approaches to Hinduism (2021).pdf` |
> | `(Texts and Studies in Ancient Judaism _ Texte und Studien zum Antiken Judentum volume 143) Ed. by Peter Schafer, Michael Meerson and Yaacov Deutsch - Toledot Yeshu (''The Life Story of Jesus'') Revisi.pdf` | `Schafer, Meerson, Deutsch (eds.) - Toledot Yeshu Revisited (TSAJ 143).pdf` |
> | `Shimon Bar Yohai, Moses de Leon, ed. Michael Berg - The Zohar_ Volumes 1-23  -Kabbalah Publishing (2003).pdf` | `Berg (ed.) - The Zohar, Volumes 1-23 (Kabbalah Publishing 2003).pdf` |
> | `Ben Sonship and Jewish Mysticism (Robert  Arlene Kogod Library Judaic Studies) by Moshe Idel (z-lib.org).pdf` | `Idel - Ben, Sonship and Jewish Mysticism (2007).pdf` |
> | `(Themes in Biblical Narrative Jewish and Christian Traditions) Koert van Bekkum_ Jaap Dekker_ Henk van de Kamp_ Eric Peels - Playing with Leviathan_ Interpretation and Reception of Monsters from the B.pdf` | `van Bekkum et al. (eds.) - Playing with Leviathan.pdf` |
> | `(Princeton library of Asian translations) Velcheru Narayana Rao, Gene Henry Roghair - Siva's warriors_ The _Basava Purana_ of Palkuriki Somanatha-Princeton University Press (1990).pdf` | `Rao, Roghair (tr.) - Siva's Warriors, The Basava Purana of Palkuriki Somanatha (1990).pdf` |
> | `(Sri Garib Das oriental series no. 85.) Chakraborty, Uma_ Ksemendra, active 11th century - Ksemendra, the eleventh century Kashmiri poet _ a study of his life and works-Sri Satguru Publications (1991.pdf` | `Chakraborty - Ksemendra, the Eleventh Century Kashmiri Poet (1991).pdf` |
> | `(SUNY series in Hindu Studies) Ute Husken (editor), Vasudha Narayanan (editor), Astrid Zotter (editor) - Nine Nights of Power_ Durga, Dolls, and Darbars-SUNY Press (2021).pdf` | `Husken, Narayanan, Zotter (eds.) - Nine Nights of Power (SUNY 2021).pdf` |
> | `(SUNY series in Hindu studies) Vidyacakravartin._ Lawrence, David Peter_ Virupaksanathapada., Virupaksanathapada - The teachings of the odd-eyed one _ a study and translation of the Virupaksapanca.pdf` | `Lawrence - The Teachings of the Odd-Eyed One, Virupaksapancasika (SUNY).pdf` |
> | `Bhavani-nama-sahasra-stutih = The thousand names of Bhavani  a page from Rudrayamala Tantra by Jankinath Kaul Kamal. (English Translation with interpreation) (z-lib.org).pdf` | `Kaul (tr.) - Bhavani-nama-sahasra-stutih, The Thousand Names of Bhavani (1991).pdf` |
> | `David Gordon White - Kiss of the Yogini_ _Tantric Sex_ in its South Asian Contexts  -University Of Chicago Press.djvu` | `White - Kiss of the Yogini.djvu` |
> | `Tracy Pintchman, Rita D. Sherma - Woman and Goddess in Hinduism_ Reinterpretations and Re-envisionings  -Palgrave Macmillan (2011).pdf` | `Pintchman, Sherma (eds.) - Woman and Goddess in Hinduism (2011).pdf` |
> | `Sri Amritananda Natha Saraswati_ Michael M. Bowden - Gifts from the Goddess Selected Works of Sri Amritananda Natha Saraswati Original writings of Sri Amritananda Natha Saraswati-45th Parallel Press (.pdf` | `Bowden - Gifts from the Goddess, Selected Works of Sri Amritananda Natha Saraswati.pdf` |
> | `Padma, Sree(Editor)_Beck, Brenda(Contributor)_Srinivasan, Perundevi(Contributor)_Pintchman, Tracy(Contributor) - Inventing and Reinventing the Goddess_ Contemporary Iterations of Hindu Deities on the .pdf` | `Padma (ed.) - Inventing and Reinventing the Goddess.pdf` |
> | `Dorman, Eric Robert - A study of the letters of the Sanskrit alphabet and their metaphysical role in the emanation of manifest reality as described in select Hindu Tantras (2009).pdf` | `Dorman - A Study of the Letters of the Sanskrit Alphabet (2009).pdf` |
> | `Devi Mahatmyam English Transliteration (1).pdf` | `Devi Mahatmyam English Transliteration.pdf` |
> | `A_12th_Century_Varaasimahatmya_and_Its (1).pdf` | `Bisschop - A 12th-Century Varanasimahatmya (2016).pdf` |
> | `Atharvavedins_in_Tantric_Territory_In_Th (1).pdf` | `Sanderson - Atharvavedins in Tantric Territory (2007).pdf` |
> | `Anant Pai - Tales of Durga (Mythology, 1)  -Amar Chitra Katha (2009).pdf` | `Pai - Tales of Durga (Amar Chitra Katha 2009).pdf` |
> | `(S U N Y Series in Hindu Studies) C. MacKenzie Brown - The Triumph of the Goddess_ The Canonical Models and Theological Visions of the Devi-Bhagavata Purana-State Univ of New York Pr (1990).pdf` | `Brown - The Triumph of the Goddess, the Devi-Bhagavata Purana (SUNY 1990).pdf` |
> | `(Routledge South Asian religion series, 4) Esther Bloch_ Marianne Keppens_ Rajaram Hegde - Rethinking religion in India _ the colonial construction of Hinduism-Routledge (2010).pdf` | `Bloch, Keppens, Hegde (eds.) - Rethinking Religion in India (2010).pdf` |
> | `Pelikan, Jaroslav - The Shape of Death_ Life, Death and Immortality in the Early Fathers-MacMillan & Co Ltd (1962) (1).pdf` | `Pelikan - The Shape of Death (1962).pdf` |
> | `being-human-in-a-technological-age-rethinking-theological-anthropology-christian-perspectives-on-leadership-and-social-ethics-9789042941816-9789042941823-9042941812_compress.pdf` | `Being Human in a Technological Age (2020).pdf` |
> | `Bart D. Ehrman - The Orthodox Corruption of Scripture_ The Effect of Early Christological Controversies on the Text of the New Testament-Oxford University Press, USA (1996).pdf` | `Ehrman - The Orthodox Corruption of Scripture (1996).pdf` |
> | `(Mcgill Studies in the History of Religions, a Series Devoted to International Scholarship) Hillary Rodrigues - Ritual Worship of the Great Goddess_ The Liturgy of the Durga Puja With Interpretations-.pdf` | `Rodrigues - Ritual Worship of the Great Goddess, The Liturgy of the Durga Puja.pdf` |
> | `03 03 SHAAPODDHAARA MANTRAM - To  remove curse from mantra.mp3` | `03 03 SHAAPODDHAARA MANTRAM - To remove curse from mantra.mp3` |
> | `Abhinavagupta The Kula Ritual as Elaborated in Chapter 29 of the Tantraloka  -Motilal Banarsidass.md` | `Abhinavagupta The Kula Ritual as Elaborated in Chapter 29 of the Tantraloka.md` |
> | `The philosophy of sadhana  with special reference to the Trika philosophy of Kashmir.md` | `The philosophy of sadhana, with special reference to the Trika philosophy of Kashmir.md` |
> | `The Stanzas on vibration  the Spandakarika with four commentaries  the spandasamdoha by Ksemaraja, the Spandavrtti.md` | `The Stanzas on vibration, the Spandakarika with four commentaries, the spandasamdoha by Ksemaraja, the Spandavrtti.md` |
> | `Yoga Spandakarika the sacred texts at the origins of Tantra  -Inner Traditions.md` | `Yoga Spandakarika the sacred texts at the origins of Tantra.md` |
> | `Introduction to the Tantraloka  A Study in Structure.md` | `Introduction to the Tantraloka, A Study in Structure.md` |
> | `Abhinavagupta's hermeneutics of the absolute Anuttaraprakriya  an interpretation of his Paratrisika Vivarana.md` | `Abhinavagupta's hermeneutics of the absolute Anuttaraprakriya, an interpretation of his Paratrisika Vivarana.md` |
> | `The new Leviathan or, Man, society, civilization and barbarism  -Clarendon Press.md` | `The new Leviathan or, Man, society, civilization and barbarism.md` |
> | `Sabbatai Zevi  Testimonies to a Fallen Messiah.md` | `Sabbatai Zevi, Testimonies to a Fallen Messiah.md` |
> | `Ksemendra, the eleventh century Kashmiri poet  a study of his life and works.md` | `Ksemendra, the eleventh century Kashmiri poet, a study of his life and works.md` |
> | `Loving Ganesa  Hinduism's endearing elephant-faced God Premavan Ganesah  sanatanadharmavallabho Gajananamahadevah.md` | `Loving Ganesa, Hinduism's endearing elephant-faced God.md` |
> | `Oh terrifying mother  sexuality, violence, and worship of the goddess Kali.md` | `Oh terrifying mother, sexuality, violence, and worship of the goddess Kali.md` |
> | `The teachings of the odd-eyed one  a study and translation of the Virupaksapanca.md` | `The teachings of the odd-eyed one, a study and translation of the Virupaksapanca.md` |
> | `Trilogy of tantra  Sivasutrani, Bhavanopanisat, Kaulopanisat tantra.md` | `Trilogy of tantra, Sivasutrani, Bhavanopanisat, Kaulopanisat tantra.md` |
> | `Siva in the forest of pines  an essay on sorcery and self-knowledge.md` | `Siva in the forest of pines, an essay on sorcery and self-knowledge.md` |
> | `Woman and Goddess in Hinduism Reinterpretations and Re-envisionings  -Palgrave Macmillan.md` | `Woman and Goddess in Hinduism Reinterpretations and Re-envisionings.md` |
> | `Tales of Durga (Mythology, 1)  -Amar Chitra Katha.md` | `Tales of Durga (Mythology, 1).md` |
> | `Rethinking religion in India  the colonial construction of Hinduism.md` | `Rethinking religion in India, the colonial construction of Hinduism.md` |
> | `Kiss of the Yogini _Tantric Sex in its South Asian Contexts  -University Of Chicago Press.md` | `Kiss of the Yogini Tantric Sex in its South Asian Contexts.md` |
> | `Early Tantric medicine  snakebite, mantras, and healing in the Garuda Tantras.md` | `Early Tantric medicine, snakebite, mantras, and healing in the Garuda Tantras.md` |

### Cybernetic Anamnesis: one name for two notes
Your essay (`Writing/Cybernetic Anamnesis/Cybernetic Anamnesis`) and the concept note (`Notes/Concepts/Cybernetic Anamnesis`) share a name, so a plain `[[Cybernetic Anamnesis]]` can land on the wrong one. This renames the concept note to `Cybernetic Anamnesis (concept)` and keeps the old name as an alias.
- [x] Done: 2026-10-04 21:45 — renamed to Cybernetic Anamnesis (concept)

## 5. Optional settings

- **PDF++** (installed, off): highlights and annotations inside PDFs, linked back to notes. Useful for the tablet.
- [x] Done: 2026-10-04 21:45 — PDF++ is on
- **Text Extractor** (installed, off): lets Omnisearch search inside PDFs and images. With ~690 PDFs the first pass can take hours and a lot of CPU. After turning it on, switch on *PDF indexing* in Settings → Omnisearch.
- [x] Done: 2026-10-04 21:45 — Text Extractor is on; now turn on "PDF indexing" in Settings → Omnisearch
- **Where new notes go:** new notes now land in the vault root. This sends them to `Notes/` instead.
- [x] Done: 2026-10-04 21:45 — new notes now go to Notes/
- **Deleted files:** deletions you make now go to the Windows Recycle Bin. This sends them to the vault's `.trash` instead, like these buttons do.
- [x] Done: 2026-10-04 21:46 — deleted files now go to the vault .trash

## 6. For you to look at (no button)

- **Leviathan notes:** `The Cybernetic Leviathan` and `Leviathan fragments 2018-2024` link 12 `.docx` names that are not in `Writing/_Originals` (e.g. `Chapter1.docx`, `cyberLevi2.docx`, `Thoughts.docx`). The folder has `CyberLevi.docx`, `CyberLevi (2).docx`, `CyberLevi3.pdf`, `The Cybernetic Leviathan.docx`, `The Cybernetic Leviathan 1.docx` and `New folder/Thoughts on the Cybernetic Leviathan.docx`, which may be the same drafts under other names. `The Gospel of Recognition` links `gospel_recognition_v3.docx`; the folder has `gospel_recognition_v3_1.docx`.
- **Lincoln Times** and **From Moral Injury to Moral Repair (part 2)** point at images from the OneNote import that are not in the vault.
- **Kubjikāmatatantra:** two different files and two catalog notes for the Goudriaan and Schoterman edition (`The Kubjikamatatantra` and `Goudriaan and Schoterman - The Kubjikamatatantra (Kaulika-Amnya)`). I could not tell which file is better, so neither is touched.
- **Exodus essay:** two different drafts; both kept.
- **Stiegler, *Decadence of Industrial Democracies*:** has its own note and is also volume 1 of *Disbelief and Discredit*. Both are in Philosophy, so I left them.
- **Gospel of Thomas:** the catalog note mentions a second translation "kept in Library/Christianity" that is no longer there.
- **Planned notes not yet written:** `Scholars - library and free sources` (linked from Home, the [[Hub - Tantraloka|Tantraloka]] hub and 8 catalog notes), and several hub links.
- **Two drawings** from 2 October in `Excalidraw/` are not linked anywhere. Keep or delete as you like.
- **Plugins you have installed but switched off** (Editing Toolbar, Pane Relief, Importer): if you no longer use them, uninstall them in Settings → Community plugins.

## 7. Redundancy sweep (5 Oct 2026, evening)

No byte-identical files were found. The 13 out-of-place items you approved are in `.trash`, and 11 misfiled works were moved to the right subject. Fourteen catalog notes named after a person or a publisher were renamed "Author - Short title", and the links followed.

These four pairs are the same book in two files. Each catalog note says which copy is better and why. The buttons take the weaker copy out of the catalog note and move it to `.trash`.

### Tantrasāra: the 200 dpi colour scan
Keeps the 283-page 600 dpi Rudra Press scan.
```dataviewjs
await dv.view("Templates/Views/sweep-actions", {id: "tantrasara2", label: "Remove the 200 dpi copy"})
```

### Kubjikāmatatantra: the Scribd copy
Its hidden text is Japanese OCR that Obsidian can't search. Keeps the z-lib copy.
```dataviewjs
await dv.view("Templates/Views/sweep-actions", {id: "kubscribd", label: "Remove the Scribd copy"})
```

### Vīṇāśikhatantra: the low-resolution two-page spreads
Keeps the Internet Archive single-page scan in Library/Hinduism.
```dataviewjs
await dv.view("Templates/Views/sweep-actions", {id: "vinaspreads", label: "Remove the spreads copy"})
```

### Rig Veda: the partial file (introduction and notes only, 75 MB)
Keeps the complete 699-page HOS 50 scan.
```dataviewjs
await dv.view("Templates/Views/sweep-actions", {id: "rigpartial", label: "Remove the partial file"})
```

### Kept on purpose (no button)

- **Macdonell, *A Vedic Reader*:** the 1992 reprint is your reading copy; the other file is the older full scan.
- **Dyczkowski, *Dawning of the Cycles of Consciousness*:** the annotated version stops at verse 146, so the full text stays too.
- **Wallis, *The Recognition Sutras*:** the second, 27-page file is the audiobook's companion PDF, not a copy of the book.
- **Devī Māhātmya:** nine PDFs (translations, editions, selections) besides the verse notes in `Texts/Devi Mahatmya` and the recitation audio. They are different translations, so nothing was removed; thin them out if you like.
- **Two links now point at removed items, inside your own writing** (left as you wrote them): `Writing/Cybernetic Anamnesis/Cybernetic Anamnesis.md` links the 2025 Ricoeur call for papers, and `Notes/Concepts/The Scapegoat Reflex - Culprits vs Conditions.md` links *1967*.


## 8. Recitation audio (6 Oct 2026)

The 29 Devī Māhātmya recitation tracks in `Audio/DeviMahatmyamRecitationAudio/` take about 250 MB, and you keep them in OneDrive for your media player anyway. The button takes the audio links out of the Devī Māhātmya notes (the `audio` property and the "Audio recitation: ▶ play" line in each chapter note, and the sentence in [[Texts/Devi Mahatmya/Devi Mahatmya|Devi Mahatmya]] that says where the tracks are), then moves the MP3s and the empty `Audio` folders to the vault's `.trash`.

```dataviewjs
await dv.view("Templates/Views/remove-audio")
```

## Already fixed (no action needed)

- Five Bases did not open at all ("groupBy must be an object", a format change in Obsidian 1.13): `Physical Library`, `Needs review`, `By subject`, `By author`, `Muktabodha`. Rewritten in the new format.
- `hide-layers` was hiding three folders that no longer exist; it now hides `Library/Lexicons`, `Library/Sanskrit/Monier-Williams` and `Library/Sanskrit/KSTS`.
- The Vault Guide is rewritten for the vault as it is now, with step-by-step instructions for adding things.
- **New:** a date box at the top of Home (Home date box): today's date, the Hebrew date (turning at sunset), the day's Sanskrit letter, the panchang for Hickory, and Shabbat/Yom Tov times for Hickory and New York. Its tables are in `Library/Calendars/` and run to the end of 2029.
