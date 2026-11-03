# mktask_ch28.py (2 Nov 2026): writes TASK.txt in each Chapter Twenty-Eight reader folder from reader-task-ch28.txt,
# the ranges (ranges.json), the pre-pass map (expected numbers per range) and the lead's notes per range (NOTES below).
import json, os
H = '/home/claude/lost/ch28'
T = open(f'{H}/scripts/reader-task-ch28.txt', encoding='utf-8').read()
M = json.load(open(f'{H}/num/ch28-map.json', encoding='utf-8'))
TITLE = {'v10-02': 'Tantraloka Dyczkowski v10 02 - Chapter Twenty-Eight, opening page', 'v10-03': 'Tantraloka Dyczkowski v10 03 - Chapter Twenty-Eight, part 1',
         'v10-04': 'Tantraloka Dyczkowski v10 04 - Chapter Twenty-Eight, part 2', 'v10-05': 'Tantraloka Dyczkowski v10 05 - Chapter Twenty-Eight, part 3',
         'v10-06': 'Tantraloka Dyczkowski v10 06 - Chapter Twenty-Eight, part 4', 'v10-07': 'Tantraloka Dyczkowski v10 07 - Chapter Twenty-Eight, part 5'}
NOTES = {
 'v10-02-a': 'This note is one page. Footnote 2 runs on over PDF 19-20, which are in the next note (v10-03): leave its definition here as it is and report the carry-over. The call ³ on this page ("one.³ (1)") belongs to footnote 3, which is defined in the next note (PDF 20): add nothing for it, report it.',
 'v10-03-a': 'PDF 19 and the first part of PDF 20\'s footnote zone (above footnote 3) carry the rest of footnote 2, whose definition is in the previous note (v10-02): leave that text where it is and report it (addendum 7). Footnote 3 is defined on PDF 20 but its call is on PDF 18, in the previous note: undo its definition to `3\\. ` and report it. Footnote 9 (PDF 23): its superscript is glued to "The" ("⁹The tradition"); the pre-pass made it from the image, and the note reads `[^9]: TThe`: the first T is the garbled superscript, remove it with a def op. Footnote 21 (PDF 26) was placed by the lead at "\\[illegible\\] Read anyai\\$ for an:" (keep the placeholder); its call and 24\'s are separate (24 is the second "Read anyaiś for anyāś" on PDF 27).',
 'v10-04-c': 'Footnote 196, the last of this note, runs on to PDF 99, which is in the next note: report the carry-over (it cannot be joined).',
 'v10-04-a': 'Footnote 108 (PDF 59): the superscript read as 106 but the sequence gives 108; check it. 122 (PDF 65): Tesseract cut the number off as a line of its own; the definition was made at "Abhinava has said (28/75cd-76ab)". 124 (PDF 66): the print has the number 124 under the rule and NO text at all: there is no definition; find its call in the body if there is one, add nothing, report it. 129 (PDF 67): the OCR lost its superscript; the definition was made by the lead ("Read saptakṛtvakaraṇe").',
 'v10-04-b': 'Footnote 136 (PDF 74, "Dhaniṣṭhā.") was placed by the lead in the footnote line (not in the body, where the same word occurs). Footnotes 145-152 (PDF 79-80) quote verses of the KM and of TĀ 28/114-120: the same verse lines stand in the body transliteration (lines before the footnote zone); 146, 147 and 149 were placed by the lead in the footnote lines; check every definition on these two pages against the image. 161 (PDF 83): made by the lead (the detector missed it).',
 'v10-05-a': 'The top of PDF 99\'s footnote zone (above footnote 197, "means dhātrī, and so stated it twice …") is the rest of footnote 196, defined in the previous note: leave it where it is and report it (addendum 7). Footnote 209 (PDF 101) was placed by the lead in the footnote line, not in the body quotation that begins with the same words.',
 'v10-05-b': 'Footnote 236 (PDF 117, printed "SāṁKā 29.") has no text in the note (the OCR lost it): there is no definition; place nothing, report it (and where its call is).',
 'v10-05-c': 'Footnote 264 (PDF 131): the garble "%t" before "Read, as the context demands" was dropped by the lead.',
 'v10-06-a': 'Footnote 295 (PDF 149): the garble "S" before "Literally ‘made of Siva’" was dropped by the lead.',
 'v10-06-b': 'Footnote 307 (PDF 157): the garble "W" before "Abhinava’s commentary" was dropped by the lead.',
 'v10-06-c': 'Footnote 333 (PDF 172, printed "YSū 4/9."): the converter jumbled 332-334 ("32 See following note. 4/9. 33 ऽ \\[illegible\\] Read dārdhyena…"): there is no definition 333 yet; on the image decide where 333 and 334 begin, make or fix them with def ops (keep every word and placeholder), and report.',
 'v10-07-a': 'Footnote 347 (PDF 179, printed "BhGī 8/6d.") has no text in the note: no definition; place nothing, report it. Footnote 350 (PDF 180): the converter jumbled 349-351 ("\\[illegible\\] Above, 28/326cd. 811 8/6-7ab quoted above as 28/325-326ab. 350 That is 351 kusakā…"): no definition 350 yet; decide on the image, make or fix with def ops (no word changes), report. 374 (PDF 188): its superscript was lost in the OCR; made by the lead at "Instead of".',
 'v10-07-b': 'Footnote 394 (PDF 194): superscript lost in the OCR; made by the lead at "Read vitti- for".',
 'v10-07-c': 'Footnote 424 (PDF 207, printed "BhGī 3/21."): the note reads "81ज 3/21." (the OCR\'s garble of BhGī; keep it); the lead dropped "+\\^" before it. 442 (PDF 214): Tesseract cut the number off; the definition begins "This seems a very odd doctrine". 444 (PDF 215) is the chapter\'s last footnote.',
}
GARB = {27, 42, 64, 68, 99, 184, 227, 402}   # leftover marks: ”, \\^, ¢TM, य (checked 2 Nov 2026)
for nid, p, a, b in json.load(open(f'{H}/ranges.json')):
    part = f'{nid}-{p}'; ns = sorted(r['n'] for r in M if r.get('n') and a <= r['pdf'] <= b)
    exp = 'footnotes %d-%d (%d starts found on the images)' % (ns[0], ns[-1], len(ns)) if ns else 'no footnote start'
    t = (T.replace('__PART__', part).replace('__TITLE__', TITLE[nid]).replace('__ID__', nid).replace('__A__', str(a)).replace('__B__', str(b))
          .replace('__PA__', str(a - 17)).replace('__PB__', str(b - 17)).replace('__EXPECT__', exp).replace('__FLAGS__', NOTES.get(part, '')))
    gl = [n for n in ns if n in GARB]
    if gl: t = t.replace('\n\nPractical points:', ' Definitions that still begin with a garble mark (remove it with a def op): %s.\n\nPractical points:' % ', '.join(map(str, gl)), 1)
    t = t.replace(' \n', '\n')
    open(f'/home/claude/dyfn/rd/{part}/TASK.txt', 'w', encoding='utf-8').write(t)
    print(part, a, b, exp)
