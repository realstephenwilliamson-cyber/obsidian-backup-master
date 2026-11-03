# mktasks.py (2 Nov 2026): TASK.txt for each Chapter Nine reader packet (rd/ID-a/b/c), from reader-task-ch2.txt's text
import json, os
H = '/home/claude/dyfn'; D = '/home/claude/lost/ch09'
PDF = '/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. 06.pdf'
R = json.load(open(f'{D}/ranges.json'))
M = json.load(open(f'{D}/num/ch09-map.json', encoding='utf-8'))
# page-specific points for the readers (from the lead's look at the images)
KNOWN = {
    21: 'PDF 21: 7 was placed by hand (MANUAL).',
    32: 'PDF 32: 40 placed by hand; its "7" is the OCR of ĪP (keep it).',
    54: 'PDF 54: footnote 76 ("ĪP 2/4/10.") has no text in the note: report it, add no definition or call.',
    68: 'PDF 68: 102 placed by hand. The body line "103A bove the triad..." holds call 103 glued to the word: look at the image.',
    71: 'PDF 71: 116 placed by hand; the two lines "> Kala > Vidya ..." are inside 121, not footnotes.',
    75: 'PDF 75: 134 placed by hand.', 80: 'PDF 80: 151 placed by hand.',
    81: 'PDF 81: 156 is "Kiraṇatantra vidyāpāda 3/26cd"; the line beginning "332 (330cd-332ab)" is inside it.',
    84: 'PDF 84: 162 placed by hand.',
    105: 'PDF 105: 205 ("saṁsāra eva aṅkuraḥ.") stands in the note as garbled Devanagari ("५ ऽक सव कोप,"): placed by hand; keep the text.',
    112: 'PDF 112: the first words of 227 ("The question now arises how can Vijñānakala pe...") are missing in the note; the definition begins at "what sense are they so?".',
    118: 'PDF 118: footnote 235 ("BhGī 2/51.") has no text in the note: report it, add no definition or call.',
    140: 'PDF 140: 275 placed by hand.', 169: 'PDF 169: 340 placed by hand.',
    174: 'PDF 174: 349 placed by hand (it begins with \\[illegible\\]); the line beginning "234 n 326" is inside 349.',
    181: 'PDF 181-182: the print seems to skip 374 (373 on PDF 181, 375 on PDF 182): confirm on the images and report.',
    182: 'PDF 181-182: the print seems to skip 374 (373 on PDF 181, 375 on PDF 182): confirm on the images and report.',
    217: 'PDF 217: the asterisk note "* Instead of trividhena kañcukamalena, ..." at the head of the footnotes is not numbered: leave it plain and report it.',
    249: 'PDF 249: 481 placed by hand.', 255: 'PDF 255: 494 placed by hand.', 259: 'PDF 259: 502 placed by hand.',
    261: 'PDF 261-263: PDF 263 repeats PDF 261 (printed p. 244 scanned twice); see addendum point 6: the copy of 507 on PDF 263 becomes 507b.',
    264: 'PDF 264 repeats PDF 262 (printed p. 245 scanned twice): its 508-511 are the copies and keep these labels in this note (addendum point 6); 510 placed by hand.',
    274: 'PDF 274: 526 placed by hand.',
    289: 'PDF 289-295: 561-565 and 568 are already real (made earlier tonight): no op for them unless a call is misplaced. 560 (PDF 289) has no call in the note yet: place it; 566 (PDF 293) and 567 (PDF 294) are new definitions whose calls are garbled (\\*\\* and \\*).',
}
TPL = open('/home/claude/dyfn/scripts/ch2/reader-task-ch2.txt', encoding='utf-8').read()
for nid, rs in R.items():
    pre = json.load(open(f'{H}/work/{nid}/pre.json', encoding='utf-8'))
    lab = {pg: l for pg, l, ml in pre['pages_all']}
    title = 'Tantraloka Dyczkowski %s %s - Chapter Nine, part %d' % (nid[:3], nid[4:], int(nid[4:]) - 2)
    for part, (a, b) in zip('abc', rs):
        nums = sorted(d['n'] for p in pre['pages'] if a <= p['pdf'] <= b for d in p['defs'])
        real = [n for n in nums if n in pre['real_defs_before']]
        known = [v for k, v in sorted(KNOWN.items()) if a <= k <= b]
        exp = ('%d-%d' % (nums[0], nums[-1])) if nums else 'none'
        t = f"""You are a page reader for Stephen's Obsidian vault. First read your brief: /home/claude/dyfn/scripts/reader-brief.txt, then the Chapter Nine points in /home/claude/lost/ch09/reader-addendum.txt (they take precedence where they differ) — follow them exactly.

DIR = /home/claude/dyfn/rd/{nid}-{part}
PDF = {PDF}
Note: {title}. YOUR PAGES: PDF {a}-{b} (printed pp. {lab[a]}-{lab[b]}), the page images in DIR. Chapter Nine's footnotes are numbered through the chapter (1-576); the definitions on your pages are labelled {exp} ({len(nums)} definitions{'; already real: ' + ', '.join(map(str, real)) if real else ''}).
""" + ('Known on your pages:\n' + '\n'.join('- ' + k for k in known) + '\n' if known else '') + """
Practical points:
- Start with DIR/pages.txt, then read note.txt in ranges as you go (Read with offset/limit), and the page images 3 or 4 per turn.
- Save your work as you go: after every 4-5 pages, write DIR/ops.json with all ops so far (same format as the final one), so nothing is lost if you are stopped. The final write replaces it.
- Every footnote whose definition lies on your pages needs exactly one call `[^n]` where the print has its superscript (usually on the same page; a call may be on the page before).
- A footnote the pre-pass missed, or a second footnote still inside a definition: a letter label (e.g. `57b`), never a free number (addendum point 2).
- In per_note, give every footnote of your pages: "n" (its label), "pdf", "printed" (the superscript NUMBER as printed at the footnote's start), "call_line".
- Do not use more than about 300 tool calls; if a page truly cannot be decided, list it in problems and move on.
- Never write the Tetragrammaton (the four-letter divine name) anywhere, in files or in your reply.
- Write nothing outside DIR (no helper scripts left behind). Reply in under 250 words: the numbers covered, the count of each op kind, whether every definition's label equals the printed number (list the ones you changed or added), and the problems.
"""
        open(f'{H}/rd/{nid}-{part}/TASK.txt', 'w', encoding='utf-8').write(t)
        print(nid, part, a, b, lab[a], lab[b], exp, len(nums), 'real', real, 'known', len(known))
