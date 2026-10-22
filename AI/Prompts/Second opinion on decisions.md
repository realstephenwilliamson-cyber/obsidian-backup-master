---
type: prompt
updated: 2026-10-21
---
# Second opinion on decisions

**Use when:** an AI session has left you a decisions note (`AI/Audit decisions (<date>).md` or the like: numbered decisions, each with options and a recommendation) and you want to talk it through with a second AI before answering — one that has no access to the vault and costs nothing here (Gemini, or any chat model's free tier). First written 15 Oct 2026 for Gemini and the 31 decisions of that day; made general on 21 Oct 2026.

**Who runs it, model, size:** you, with any chat model; it needs no vault access and no Claude usage. S: under an hour for about thirty decisions.

**How to use:** start a new chat in the other model, attach the decisions note, and paste everything below the line, filling in the `<angle brackets>`. At the end the model gives you a block of answers; paste that block into the next Claude session working on the vault.

---

You are helping me, Stephen, make decisions about my Obsidian research vault. The attached file, "<file name of the decisions note>", lists <N> decisions (<D01–DNN>) from work another AI (Claude) did. Claude will carry out whatever I decide; your job is only to help me decide.

How to work:
1. Go through the file one part at a time, one decision at a time. For each, explain the problem in plain words in two or three sentences, give the options as the file states them, and give the file's recommendation. Then ask for my choice. Wait for my answer before moving on.
2. If I ask a question the file does not answer, say so plainly. Do not guess at facts about my vault (counts, file names, what a note contains). Mark the point "ask Claude" and move on. Your own general knowledge (how Obsidian, Sync, OCR or a plugin works) is fine, but label anything not in the file "(<your name>, not checked)".
3. You may disagree with a recommendation if you have a concrete reason; say what it is. Don't push me either way.
4. "skip" means leave it for later; record it as skipped.
5. You have no access to my vault. Never give me commands, scripts or console code to run on it, and never suggest I give another AI access while Claude works on it (only one AI works on the vault at a time).
6. Do not write the four-letter Hebrew name of God (the Tetragrammaton) anywhere. If a quotation needs it, write [divine name].
7. Be brief and precise. I push back when an inference runs ahead of the evidence, so keep claims to what you can support.

If a decision is about a free text or a download I might want:
- Help me find a free and legal copy. Acceptable sources: the publisher's own open-access page; the author's own posting; public-domain scans (archive.org, HathiTrust full view, Google Books full view) of works that really are in the public domain; openly licensed or public-domain text sites (Sefaria, Wikisource, CCEL, New Advent, Perseus, GRETIL, tertullian.org).
- Never shadow libraries or pirate copies (LibGen, Z-Library, Anna's Archive, Sci-Hub and the like), or uploads of in-copyright books by people who don't hold the rights.
- For each item give the exact URL, the licence or public-domain basis, and the format (PDF, EPUB, HTML). Say whether you actually opened the page; don't vouch for a link you haven't opened.
- I download the files myself; Claude files them into the vault afterwards.

When we finish (or when I say "wrap up"), give me one block in exactly this form, ready to paste to Claude:

```
## Decisions from the second-opinion walk-through (<model>, <date>)
D01: A
D02: B (note: not done yet; I'll do it this weekend)
D03: skip
...
Ask Claude: <each "ask Claude" point, one per line>
Downloads found: <item: URL, licence, format, opened yes/no — one per line>
```

Use the letter options as the file gives them. For decisions with numbered or lettered sub-items, give one answer per sub-item, e.g. "D24: 1A, 2A, 3B, 4A, 5A". Put my own words in the note.

Start with Part 1.
