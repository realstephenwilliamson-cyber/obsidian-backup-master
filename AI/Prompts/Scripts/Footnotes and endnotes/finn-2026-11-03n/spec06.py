# Finn note 06 (K201-K240, VT Chapter I commentary, the cakra and its vidyas): plain or unnumbered footnotes, calls as junk, label
# remnants, drawings, settled from the PDF's text layer and the page images (K201, K216, K220, K225, K232).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
D = '*(a drawing in the print)*'
S = Spec('06'); L = S.L
# K201 p.205: 211 is a drawing (OCR junk in 210's definition, which also ends with a drawing)
l = L(211, 201)
S.sub('f01', 201, 'and four fires.211', 'and four fires.[^%s]' % l)
S.sub('f02', 201, 'to the top of the whole cakra. 211\\. 8 SANV KAS DORO VANVZAYA', 'to the top of the whole cakra. %s\n[^%s]: %s' % (D, l, D))
# K214 p.218: 264; label remnants in it
l = L(264, 214)
S.sub('f03', 214, 'inscribed with the cakra. ?26\\* Half', 'inscribed with the cakra.[^%s] Half' % l)
S.sub('f04', 214, '264\\. I.e., the "pericarp" with the five Saktis and the four fires will 262. 263. cover', '[^%s]: I.e., the "pericarp" with the five Saktis and the four fires will cover' % l)
# K215 p.219: 265, 266
l5, l6 = L(265, 215), L(266, 215)
S.sub('f05', 215, 'the eight and the one.?255 One becomes', 'the eight and the one.[^%s] One becomes' % l5)
S.sub('f06', 215, 'creation and dissolution. ?56 On the outside', 'creation and dissolution.[^%s] On the outside' % l6)
S.para('f07', 215, '265\\. These lines have been quoted', 1, l5)
S.para('f08', 215, '266\\. Although the Saktis basically', 2, l6)
# K216 p.220: 268's table read as junk; label remnants before 269
S.sub('f09', 216, 'The result ts: Maṇdala p— ji = Portals a 7 w a | Lotuses i n Pericarp y w . 3 a- w z L B L | 1 hand 2 hand 3 hand', 'The result ts: ' + D)
S.sub('f10', 216, '[^269]: 53 a 269. There are', '[^269]: There are')
# K217 p.221: 270
l = L(270, 217)
S.sub('f11', 217, 'cakra.)?7° Suspecting', 'cakra.)[^%s] Suspecting' % l)
S.para('f12', 217, '270\\. The fourth thread is only', 1, l)
# K220 p.224: 276-278 (unnumbered, among the drawing's labels)
l6, l7, l8 = L(276, 220), L(277, 220), L(278, 220)
S.sub('f13', 220, 'three-part feature,?76 and', 'three-part feature,[^%s] and' % l6)
S.sub('f14', 220, 'perimeter of the square.)?77 By', 'perimeter of the square.)[^%s] By' % l7)
S.sub('f15', 220, 'respect to the circle;278 by', 'respect to the circle;[^%s] by' % l8)
i, j, ls = S.lines(220, '277\\.', 9)
assert ls[3].startswith('The "middle part"') and ls[4].startswith('The reference points') and ls[8].startswith('The text reads'), ls
S.spans.append([i, j, '[^%s]: %s\n[^%s]: %s %s\n[^%s]: %s' % (l6, ls[3], l7, ls[4], D, l8, ls[8]), 'f16'])
# K225 p.229: 296 is a drawing
l = L(296, 225)
S.sub('f17', 225, 'This is the cakra.?96 The', 'This is the cakra.[^%s] The' % l)
S.sub('f18', 225, '\n\n296\\.', '\n\n[^%s]: %s' % (l, D))
# K226 p.230: 298
l = L(298, 226)
S.sub('f19', 226, 'yellow gorocana??8 pigment', 'yellow gorocana[^%s] pigment' % l)
S.para('f20', 226, '298\\. Gorocanā is a yellow', 1, l)
# K227 p.231: 299
l = L(299, 227)
S.sub('f21', 227, 'BELOW IṬ299', 'BELOW IṬ[^%s]' % l)
S.para('f22', 227, '299, Here and elsewhere', 1, l, strip=r'^299, ')
# K228 p.232: 300, 301
l0, l1 = L(300, 228), L(301, 228)
S.sub('f23', 228, 'at its endž°° is', 'at its end[^%s] is' % l0)
S.sub('f24', 228, 'which is in earth301 is', 'which is in earth[^%s] is' % l1)
S.para('f25', 228, '300\\. I.e., coming after it', 1, l0)
S.para('f26', 228, '301\\. The letter "L" stands', 2, l1)
# K229 p.233: label remnant in 305
S.sub('f27', 229, '[^305]: 305, "Raised above"', '[^305]: "Raised above"')
# K231 p.235: 307, 308
l7, l8 = L(307, 231), L(308, 231)
S.sub('f28', 231, 'daŝarathī Ramah" 3°7', 'daŝarathī Ramah"[^%s]' % l7)
S.sub('f29', 231, 'SECOND; 3098 THE ONE', 'SECOND;[^%s] THE ONE' % l8)
S.para('f30', 231, '507\\. The significance of the', 2, l7)
S.para('f31', 231, '3508, The Yāgbhava = AIM', 1, l8, strip=r'^3508, ')
# K232 p.236: 310's call stood after 'S' (no call in the print); it belongs after "vahnivesma"
S.sub('f32', 232, "after 'S[^310]' joined", "after 'S' joined")
S.sub('f33', 232, 'vahnivesma,. "319', 'vahnivesma,. "[^310]')
# K233 p.237: 316; label remnant
l = L(316, 233)
S.sub('f34', 233, 'relating to Purapdaraž16 and', 'relating to Purapdara[^%s] and' % l)
S.sub('f35', 233, '316\\. "Puraṇdara" is an epithet of Indra, hence the letter "I". 8317.', '[^%s]: "Puraṇdara" is an epithet of Indra, hence the letter "I".' % l)
# K235 p.239: label remnants in 324
S.sub('f36', 235, 'for complete diagram. 821. 322. 828. 324. NE East SE South', 'for complete diagram.')
# K237 p.241: 328
l = L(328, 237)
S.sub('f37', 237, 'THE KULA VIDYĀ328 WHICH', 'THE KULA VIDYĀ[^%s] WHICH' % l)
S.para('f38', 237, '828\\. "Kulavidyā" suggests', 2, l)
# K238 p.242: 330
l = L(330, 238)
S.sub('f39', 238, 'Thus HRĪM. >30', 'Thus HRĪM.[^%s]' % l)
S.para('f40', 238, '380\\. One must consult the triangle', 1, l)
# K239 p.243: 331, 332
l1, l2 = L(331, 239), L(332, 239)
S.sub('f41', 239, 'Rājānakalyāṇa. 331 We do', 'Rājānakalyāṇa.[^%s] We do' % l1)
S.sub('f42', 239, 'So,33? whatever', 'So,[^%s] whatever' % l2)
S.para('f43', 239, '531\\. I.e., as both these gurus', 1, l1)
S.para('f44', 239, '332\\. The text reads "tanah"', 1, l2)
S.build(); S.save('/home/claude/finn/specs/finn06-spec.json')
