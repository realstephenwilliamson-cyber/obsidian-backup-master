---
type: reference
updated: 2026-10-19
---
# Smart Connections exclusions

Smart Connections keeps its excluded folders in `.smart-env/smart_env.json`, a hidden folder that Obsidian Sync does not carry, so a new device starts with no exclusions and would index the whole vault (with the whole vault it crashed Obsidian on this computer, 13 Oct 2026). Before the first index on a device: Settings → Smart Connections → *Manage excluded folders*, and enter the folders below. On a phone or tablet the plugin loads only when you ask it to. See [[Vault Guide#Setting up a new device]].

Copied from this computer's settings on 14 Oct 2026: 106 entries (files named `Untitled` are excluded too); three added on 19 Oct 2026 — the AI prompts folder and the two Sanskrit card folders, whose Devanāgarī an English embedding model is unlikely to match well — 109 in all.

```
Library/Lexicons/**
Library/Sanskrit/Tantraloka words/**
Library/Sanskrit/Monier-Williams/**
Templates/**
Excalidraw/**
Projects/_Originals/**
Calendar/**
Library/Biblical-Studies/**
Library/Other/**
Library/Trika/**
Library/Christianity/**
Library/Hinduism/**
Library/Judaica/**
Library/Sanskrit/**
AI/Archive/**
Texts/Aquinas/**
Texts/BCP 1979/**
Texts/Chasidut/**
Texts/DCS/**
Texts/Devi Mahatmya/**
Texts/Bible/Douay-Rheims/**
Texts/Fathers/**
Texts/Bible/LXX/**
Texts/Malinislokavarttika/**
Texts/Markandeya Purana/**
Texts/Muktabodha/**
Texts/MUKTABODHA-LIBRARY-DEVANAGARI/**
Texts/MUKTABODHA-LIBRARY-IAST_2026_02_20/**
Texts/Pirkei Avot/**
Texts/RCL/**
Texts/Tantraloka/**
Texts/Zohar/**
Library/Philosophy/A History of Time in the Samkhya Tradition (Ratie)/**
Library/Philosophy/Aesthetics, Digital Studies and Bernard Stiegler (Fitzpatrick)/**
Library/Philosophy/Bernard Stiegler (Buseyne)/**
Library/Philosophy/Critical Essays on Bernard Stiegler (Bradley)/**
Library/Philosophy/Cybernetics - Or Control and Communication in the Animal (Wiener)/**
Library/Philosophy/Cyclonopedia - Complicity with Anonymous Materials (Negarestani)/**
Library/Philosophy/Dialectic of Enlightenment (Horkheimer)/**
Library/Philosophy/Dialogue and Universalism 28, no. 4 (Brudzinska)/**
Library/Philosophy/Echographies of Television (Derrida)/**
Library/Philosophy/Eichmann in Jerusalem (Arendt)/**
Library/Philosophy/Ethical Loneliness (Stauffer)/**
Library/Philosophy/Figuring the Sacred (Ricoeur)/**
Library/Philosophy/Freud and Philosophy (Ricoeur)/**
Library/Philosophy/Green Leviathan or the Poetics of Political Liberty (Coeckelbergh)/**
Library/Philosophy/Hermeneutics - Writings and Lectures, Volume 2 (Ricoeur)/**
Library/Philosophy/Hobbes on Resistance (Sreedhar)/**
Library/Philosophy/Hobbes, Bramhall and the Politics of Liberty and Necessity (Jackson)/**
Library/Philosophy/Hobbes, Locke, and Confusion's Masterpiece (Harrison)/**
Library/Philosophy/Humanism and Terror (Merleau-Ponty)/**
Library/Philosophy/I and Thou (Buber)/**
Library/Philosophy/Ideas Pertaining to a Pure Phenomenology (Husserl)/**
Library/Philosophy/In Search of Meaning (Arnswald)/**
Library/Philosophy/Invisible Leviathan (Smith)/**
Library/Philosophy/Lectures 1949-1968, Volume 2 (Adorno)/**
Library/Philosophy/Lectures on Ideology and Utopia (Ricoeur)/**
Library/Philosophy/Leviathan After 350 Years (Sorell)/**
Library/Philosophy/Liberty, Rationality, and Agency in Hobbes's Leviathan (van Mill)/**
Library/Philosophy/Limiting Leviathan (May)/**
Library/Philosophy/Memory, History, Forgetting (Ricoeur)/**
Library/Philosophy/Minima Moralia - Reflections on a Damaged Life (Adorno)/**
Library/Philosophy/Morality in the Philosophy of Thomas Hobbes (Lloyd)/**
Library/Philosophy/Narrative and Technology Ethics (Reijers)/**
Library/Philosophy/Narrative Identity, Autonomy, and Mortality (Davenport)/**
Library/Philosophy/Negative Dialectics (Adorno)/**
Library/Philosophy/On Bernard Stiegler (Nancy)/**
Library/Philosophy/On Psychoanalysis - Writings and Lectures, Volume 1 (Ricoeur)/**
Library/Philosophy/Oneself as Another (Ricoeur)/**
Library/Philosophy/Phantasy, Image Consciousness, and Memory (Husserl)/**
Library/Philosophy/Phenomenology and Mysticism (Steinbock)/**
Library/Philosophy/Phenomenology and the Human Sciences (Mohanty)/**
Library/Philosophy/Phenomenology of Perception (Merleau-Ponty)/**
Library/Philosophy/Play as Symbol of the World (Fink)/**
Library/Philosophy/Politics, Economy, and Society (Ricoeur)/**
Library/Philosophy/Problems of Moral Philosophy (Adorno)/**
Library/Philosophy/Psychosynthesis (Firman)/**
Library/Philosophy/Reading Religious Ritual with Ricoeur (Gschwandtner)/**
Library/Philosophy/Returning to Judgment (Turner)/**
Library/Philosophy/Ricoeur's Hermeneutics of Religion (Gregor)/**
Library/Philosophy/Routledge Philosophy GuideBook to Merleau-Ponty (Romdenh-Romluc)/**
Library/Philosophy/Society Must Be Defended (Foucault)/**
Library/Philosophy/Stiegler and Technics (Howells)/**
Library/Philosophy/Taming the Leviathan (Parkin)/**
Library/Philosophy/The Cambridge Companion to Adorno (Huhn)/**
Library/Philosophy/The Cambridge Introduction to Walter Benjamin (Ferris)/**
Library/Philosophy/The Complete Correspondence, 1928-1940 (Adorno)/**
Library/Philosophy/The Course of Recognition (Ricoeur)/**
Library/Philosophy/The Culture Industry (Adorno)/**
Library/Philosophy/The Language Animal (Taylor)/**
Library/Philosophy/The Limits of Leviathan (Scott)/**
Library/Philosophy/The Natural History of Religion (Hume)/**
Library/Philosophy/The New Leviathan (Collingwood)/**
Library/Philosophy/The Platonian Leviathan (Craig)/**
Library/Philosophy/The Possibility of Transcendental Philosophy (Mohanty)/**
Library/Philosophy/The Prophetic Faith (Buber)/**
Library/Philosophy/The Psychological Technique of Martin Luther Thomas' Radio (Adorno)/**
Library/Philosophy/The Question Concerning Technology and Other Essays (Heidegger)/**
Library/Philosophy/The Stars Down to Earth and Other Essays on the Irrational (Adorno)/**
Library/Philosophy/The Thought of Bernard Stiegler (Abbinnett)/**
Library/Philosophy/The Time of the Image (Azizov)/**
Library/Philosophy/The Visible and the Invisible (Merleau-Ponty)/**
Library/Philosophy/Theological-Political Treatise (de Spinoza)/**
Library/Philosophy/Two Types of Faith (Buber)/**
Texts/Bible/NRSVue/**
Texts/Bible/Jewish Annotated New Testament/**
AI/Prompts/**
Study/Sanskrit/Flashcards/**
Study/Sanskrit/CIS cards/**
```
