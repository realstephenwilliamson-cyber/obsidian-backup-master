# Finn note 08 (K281-K320: end of VT Chapter I commentary, Chapters II-IV): plain, unnumbered or shifted footnotes, calls as junk,
# label remnants, drawings, settled from the PDF's text layer and the page images (K283-K285, K290, K293, K300, K301, K317).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
D = '*(a drawing in the print)*'
S = Spec('08'); L = S.L
# K282 p.286: junk after 480
S.sub('h01', 282, 'relative (matter).[^480] \\* 80', 'relative (matter).[^480]')
# K283 p.287: calls 470-472 (the first carried no call in the print, the next two were a number high or junk); 470, 475 plain
S.sub('h02', 283, "the letter 's[^471]'\" - the one", "the letter 's'\" - the one")
S.sub('h03', 283, 'the nature of fire[^472] with the fourth vowel and bindu."#71 Again', 'the nature of fire[^%s] with the fourth vowel and bindu.[^471] Again' % L(470, 283))
S.sub('h04', 283, 'form of a triangle!7? that', 'form of a triangle[^472] that')
S.sub('h05', 283, 'of "r" and "1";%75 and', 'of "r" and "1";[^%s] and' % L(475, 283))
S.para('h06', 283, '470\\. "Repha" is synonymous', 1, '470')
S.para('h07', 283, '475\\. "R" and "1" are', 1, '475')
# K284 p.288: Chapter II, notes 1-3 (calls as junk)
l1, l2, l3 = L(1, 284), L(2, 284), L(3, 284)
S.sub('h08', 284, '(of place).! Therefore', '(of place).[^%s] Therefore' % l1)
S.sub('h09', 284, 'the Dvīpa scriptures,? because', 'the Dvīpa scriptures,[^%s] because' % l2)
S.sub('h10', 284, 'BUTTOCKS ARE QUIVERING. 3', 'BUTTOCKS ARE QUIVERING.[^%s]' % l3)
S.para('h11', 284, '1\\. Literally: "witkout regard', 2, l1)
i, j, ls = S.lines(284, 'The Dvīpa scriptures may refer', 2); assert ls[1] == 'to', ls
S.spans.append([i, j, '[^%s]: %s' % (l2, ls[0]), 'h12'])
S.para('h13', 284, '8\\. Literally: "possessed of quivering', 1, l3)
# K285 p.289: 4, 5 (the call 5 had been read as the "S" of "OBSERVANCES")
l4, l5 = L(4, 285), L(5, 285)
S.sub('h14', 285, 'become distracted and what', 'become distracted[^%s] and what' % l4)
S.sub('h15', 285, 'MERITORIOUS OBSERVANCES HAS THUS', 'MERITORIOUS OBSERVANCE[^%s] HAS THUS' % l5)
S.para('h16', 285, 'Literally: "outward faeing"', 1, l4, strip=None)
S.para('h17', 285, 'This meritorious observance has its emphasis', 1, l5, strip=None)
# K288 p.292: 20
l = L(20, 288)
S.sub('h18', 288, 'MAKE THE TILAKA™® WITH', 'MAKE THE TILAKA[^%s] WITH' % l)
S.para('h19', 288, '20\\. A coloured mark made', 1, l)
# K289 p.293: 23 (its call as junk; 24's call carried 23's label), 24 plain
l = L(24, 289)
S.sub('h20', 289, 'ON THE FOREHEAD,?3 HEART', 'ON THE FOREHEAD,[^23] HEART')
S.sub('h21', 289, 'THE GREAT VIDYA[^23]" AND', 'THE GREAT VIDYA[^%s] AND' % l)
S.para('h22', 289, '24\\. I.e., the Mūlavidyā', 1, l)
# K290 p.294: 30 is a drawing
l = L(30, 290)
S.sub('h23', 290, 'draw the image inside it.3°', 'draw the image inside it.[^%s]' % l)
i, j, ls = S.lines(290, '[^29]: The Sanskrit reads', 1)
S.spans.append([j, j, '\n[^%s]: %s' % (l, D), 'h24'])
# K291 p.295: 31, 32
l1, l2 = L(31, 291), L(32, 291)
S.sub('h25', 291, 'BROKEN TO PIECES.3:', 'BROKEN TO PIECES.[^%s]' % l1)
S.sub('h26', 291, 'BRINGS32? THE WHOLE', 'BRINGS[^%s] THE WHOLE' % l2)
S.para('h27', 291, 'ôl. Each of these adjectives', 2, l1, strip=r'^ôl\. ')
S.para('h28', 291, '32\\. Literally: "makes"', 1, l2)
# K292 p.296: junk after 36
S.sub('h29', 292, 'KAMAKALĀ.[^36] >36', 'KAMAKALĀ.[^36]')
# K293 p.297: 38
l = L(38, 293)
S.sub('h30', 293, 'QĀKINĪS, SĀKINĪS,’®', 'QĀKINĪS, SĀKINĪS,[^%s]' % l)
S.para('h31', 293, '38\\. "Săkinis" are', 1, l)
# K294 p.298: a stray label
S.sub('h32', 294, 'Then,\n\n43\\.\n\n', 'Then,\n\n')
# K296 p.300: 43
l = L(43, 296)
S.sub('h33', 296, 'ARISES FROM COOLING. +3', 'ARISES FROM COOLING.[^%s]' % l)
S.para('h34', 296, '43\\. I.e., smallpox.', 1, l)
# K297 p.301: junk after 44
S.sub('h35', 297, "INDRA'S QUARTER,[^44] ”\\*", "INDRA'S QUARTER,[^44]")
# K300 p.304: 48 is a diagram (its labels read as lines)
l = L(48, 300)
S.sub('h36', 300, "ruination of one's enemies.\\*8", "ruination of one's enemies.[^%s]" % l)
i, j, ls = S.lines(300, 'devastation', 5); assert ls[-1] == 'hatred disease', ls
S.spans.append([i, j, '[^%s]: %s' % (l, D), 'h37'])
# K301 p.305: 49-52 (51 and 52 run together)
l9, l0, l1, l2 = L(49, 301), L(50, 301), L(51, 301), L(52, 301)
S.sub('h38', 301, 'AND ENDING\\*9 IN THE', 'AND ENDING[^%s] IN THE' % l9)
S.sub('h39', 301, 'A LIBERATED ONE,5°', 'A LIBERATED ONE,[^%s]' % l0)
S.sub('h40', 301, 'an inner disposition51 bears', 'an inner disposition[^%s] bears' % l1)
S.sub('h41', 301, 'the declared objective? since', 'the declared objective[^%s] since' % l2)
S.para('h42', 301, '49\\. Literally: "as far as”', 1, l9)
S.para('h43', 301, '50\\. "Khecara" or "khecaratvam"', 2, l0)
S.sub('h44', 301, '51\\. The Sanskrit word used here (as below) is "lakga" meaning\n\n"token, sign ete. ", 52. The "declared purpose” (pratijnātārtha) may refer to the\n\ngoal of liberation',
      '[^%s]: The Sanskrit word used here (as below) is "lakga" meaning "token, sign ete. ".\n[^%s]: The "declared purpose” (pratijnātārtha) may refer to the goal of liberation' % (l1, l2))
# K302 p.306: 58's call as digits; 59's call carried 58's label; 60's call as junk; 59 and 60 plain
l9, l0 = L(59, 302), L(60, 302)
S.sub('h45', 302, 'THE SIDDHA, 58\n\nTHE SIDDHI OF RAW FLESH,[^58] THE MANAHŜILĀ, 6°', 'THE SIDDHA,[^58]\n\nTHE SIDDHI OF RAW FLESH,[^%s] THE MANAHŜILĀ,[^%s]' % (l9, l0))
S.para('h46', 302, '59\\. The "Raw flesh siddhi”', 1, l9)
S.para('h47', 302, '60\\. The Red arsenic siddhi?', 1, l0)
# K303 p.307: 61
l = L(61, 303)
S.sub('h48', 303, 'THE AÑJANA,8!1 THE', 'THE AÑJANA,[^%s] THE' % l)
S.para('h49', 303, '61\\. The "Anjana" or ointment', 1, l)
# K305 p.309: a label remnant in 5
S.sub('h50', 305, '[^5]: 5, The swastika', '[^5]: The swastika')
# K309 p.313: 24, 25 (24's first line read as junk)
l4, l5 = L(24, 309), L(25, 309)
S.sub('h51', 309, 'KĀKINĪS AND HĀKINĪS.?2\\*', 'KĀKINĪS AND HĀKINĪS.[^%s]' % l4)
S.sub('h52', 309, 'USAGE. 25', 'USAGE.[^%s]' % l5)
i, j, ls = S.lines(309, '24\\. -o ; - P', 3)
S.spans.append([i, j, '[^%s]: %s %s' % (l4, ls[1], ls[2]), 'h53'])
S.para('h54', 309, '25\\. I.e., the Samaya mudrā.', 1, l5)
# K311 p.315: 34; junk after 31
l = L(34, 311)
S.sub('h55', 311, 'intoxication",[^31] ž', 'intoxication",[^31]')
S.sub('h56', 311, 'in all the sāstras. "3%', 'in all the sāstras. "[^%s]' % l)
S.para('h57', 311, '34\\. In Kashmir Saivism', 1, l)
# K314 p.318: junk after 3
S.sub('h58', 314, 'mentions[^3-p318] ž\\]', 'mentions[^3-p318]')
# K315 p.319: 4 (unnumbered after its first paragraph), 5
l4, l5 = L(4, 315), L(5, 315)
S.sub('h59', 315, 'human (kinds) of knowledge.\\* Such', 'human (kinds) of knowledge.[^%s] Such' % l4)
S.sub('h60', 315, 'the disiddha5 who', 'the disiddha[^%s] who' % l5)
S.para('h61', 315, '4\\. ALL manifestations', 3, l4)
S.para('h62', 315, '5\\. Ādisiddha means', 2, l5)
# K316 p.320: 11
l = L(11, 316)
S.sub('h63', 316, 'that has been mentioned!t)', 'that has been mentioned[^%s])' % l)
S.para('h64', 316, '11\\. I.e., tn Verse 4', 1, l)
# K317 p.321: 13's call stood after "Tu" (no call in the print) and belongs after "brahman?","; a label remnant in 12
S.sub('h65', 317, 'quiescent brahman?",13 the Lord', 'quiescent brahman?",[^13-p321] the Lord')
S.sub('h66', 317, '"Tu[^13-p321]" has', '"Tu" has')
S.sub('h67', 317, '[^12-p321]: 12, According', '[^12-p321]: According')
# K319 p.323: 23; label remnants in 21, 22, 24
l = L(23, 319)
S.sub('h68', 319, 'its unique pramātp?’ nature', 'its unique pramātp[^%s] nature' % l)
S.para('h69', 319, '23\\. , See Chapter I footnote 46', 1, l, strip=r'^23\\\. , ')
S.sub('h70', 319, '[^21-p323]: 2l, Prakāśa', '[^21-p323]: Prakāśa')
S.sub('h71', 319, '[^22-p323]: 22, "Name"', '[^22-p323]: "Name"')
S.sub('h72', 319, '[^24]: , The Sanskrit', '[^24]: The Sanskrit')
S.build(); S.save('/home/claude/finn/specs/finn08-spec.json')
