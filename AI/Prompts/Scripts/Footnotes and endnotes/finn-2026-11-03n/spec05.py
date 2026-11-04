# Finn note 05 (K161-K200, VT Chapter I commentary): plain, merged or mislabelled footnotes, label remnants, drawings, settled from
# the PDF's text layer and the page images (K167, K185, K187, K192, K195-K199).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
D = '*(a drawing in the print)*'
S = Spec('05'); L = S.L
# K162 p.166: 63; label remnants
l = L(63, 162)
S.sub('e01', 162, 'Mokṣa and Rasa. "63', 'Mokṣa and Rasa. "[^%s]' % l)
S.sub('e02', 162, '\n\n64. 85. 66.\n\n63\\. Siddhis are', '\n\n[^%s]: Siddhis are' % l)
# K167 p.171: 89-91 (unnumbered at the foot); label remnants
l89, l90, l91 = L(89, 167), L(90, 167), L(91, 167)
S.sub('e03', 167, 'countless gākinīs,89 malignant', 'countless gākinīs,[^%s] malignant' % l89)
S.sub('e04', 167, 'host of yoginīs."% (3:19)', 'host of yoginīs."[^%s] (3:19)' % l90)
S.sub('e05', 167, 'And also,\n\n89\\.\n\n"The Lord Hari', 'And also,\n\n"The Lord Hari')
S.sub('e06', 167, 'mohint. "91 (4:67)', 'mohint. "[^%s] (4:67)' % l91)
S.para('e07', 167, '"Dākints are semi-divine', 1, l89, strip=None)
S.para('e08', 167, 'See footnote 10 for a deftnitton', 1, l90, strip=None)
S.sub('e09', 167, 'A "vidyā" is a feminine mantra.', '[^%s]: A "vidyā" is a feminine mantra.' % l91)
S.sub('e10', 167, 'such is the Tantric explanation.\n\n90. 91.', 'such is the Tantric explanation.')
# K178 p.182: 139-143 (calls as junk, labels standing alone, definitions unnumbered)
ls = [L(n, 178) for n in (139, 140, 141, 142, 143)]
S.sub('e11', 178, 'NATURE IS "AHAM"139 AND', 'NATURE IS "AHAM"[^%s] AND' % ls[0])
S.sub('e12', 178, 'CONJUNCT OF LETTERS;1%° WHO', 'CONJUNCT OF LETTERS;[^%s] WHO' % ls[1])
S.sub('e13', 178, 'KULA KALAS"! AND', 'KULA KALAS"[^%s] AND' % ls[2])
S.sub('e14', 178, 'TURMOIL. 1%#2', 'TURMOIL.[^%s]' % ls[3])
S.sub('e15', 178, 'the four variants1#3 relating', 'the four variants[^%s] relating' % ls[4])
S.sub('e16', 178, '\n\n1839\\.\n\n140\\.\n\n141\\.\n\n142\\.\n\nThe word "ahan" means', '\n\n[^%s]: The word "ahan" means' % ls[0])
S.para('e17', 178, 'The Goddess ís of the nature of "ahaṇ"', 2, ls[1], strip=None)
S.para('e18', 178, 'See Part II and the "Introd.', 1, ls[2], strip=None)
S.para('e19', 178, '"Olija" is the churning', 2, ls[3], strip=None)
S.para('e20', 178, '"Vikalpa" usually means', 1, ls[4], strip=None)
# K185 p.189: 163
l = L(163, 185)
S.sub('e21', 185, 'siddha yoginīs.153 It is said', 'siddha yoginīs.[^%s] It is said' % l)
S.para('e22', 185, '163\\. The Goddess is a treasure house', 1, l)
# K186 p.190: label remnants in 170
S.sub('e23', 186, 'footnote 1 of the 166. 167. 168. 169. Sanskrit text.', 'footnote 1 of the Sanskrit text.')
# K187 p.191: 171; 172's second line stood above its first
l = L(171, 187)
S.sub('e24', 187, 'SIXTEEN VIDYĀS?71 WHICH', 'SIXTEEN VIDYĀS[^%s] WHICH' % l)
S.para('e25', 187, '171\\. The word vidyā has', 1, l)
S.sub('e26', 187, 'kārṇava" part of the Vāmakeśvarimatam or Vāmakeśvara Tantra.\n\n[^172]: This verse marks the actual „beginning of the "Nityāṣodaği-',
      '[^172]: This verse marks the actual „beginning of the "Nityāṣodağikārṇava" part of the Vāmakeśvarimatam or Vāmakeśvara Tantra.')
# K191 p.195: 183, 184 (run together)
l183, l184 = L(183, 191), L(184, 191)
S.sub('e27', 191, 'seven times seven yonis,"183', 'seven times seven yonis,"[^%s]' % l183)
S.sub('e28', 191, 'no sense at allḷ:18%', 'no sense at allḷ:[^%s]' % l184)
S.sub('e29', 191, '183\\. See footnote 182. 184\\. Jayaratha has been', '[^%s]: See footnote 182.\n[^%s]: Jayaratha has been' % (l183, l184))
# K192 p.196: 185 is a drawing (the OCR read it as junk lines)
l = L(185, 192)
S.sub('e30', 192, '"root" triangle.185', '"root" triangle.[^%s]' % l)
i, j, _ = S.lines(192, '? 2 3', 5); S.spans.append([i, j, '[^%s]: %s' % (l, D), 'e31'])
# K195 p.199: 194 (its call carried 196's label), 196 (call as digits); 195's drawing
l = L(194, 195)
S.sub('e32', 195, 'above all the others[^196] and', 'above all the others[^%s] and' % l)
S.sub('e33', 195, 'within the third śaktýí196 that', 'within the third śaktýí[^196] that')
S.para('e34', 195, '194\\. I.e., above all other', 1, l)
S.sub('e35', 195, 'ten-spoked cakras.  The fourth sakti:', 'ten-spoked cakras. The fourth sakti: ' + D)
# K196 p.200: no call after "FIRST SAKTI,"; 198 and 199 as junk; 197 and 198 drawings
l = L(198, 196)
S.sub('e36', 196, 'THE FIRST AKTI,[^199] ONE', 'THE FIRST AKTI, ONE')
S.sub('e37', 196, 'the three upper angles.198', 'the three upper angles.[^%s]' % l)
S.sub('e38', 196, 'THE FIRST?:99 FIRE.', 'THE FIRST[^199] FIRE.')
S.sub('e39', 196, '[^197]: The third fire: AI 190.. KRZ /X ANIA', '[^197]: The third fire: %s\n[^%s]: %s' % (D, l, D))
# K197 p.201: 201 (a drawing) inside 200's definition; 202's drawing
l = L(201, 197)
S.sub('e40', 197, 'ten-spoked cakras.??1', 'ten-spoked cakras.[^%s]' % l)
S.sub('e41', 197, '[^200]: See footnote 199. (A s, 7 RANN 201\\. ZYY JANANA: nÉ = V -naa 2 (£9) t', '[^200]: See footnote 199.\n[^%s]: %s' % (l, D))
S.sub('e42', 197, '[^202]: The fifth śakti: sT ATANAN T7 yavan ay, SANNA A N ZY', '[^202]: The fifth śakti: ' + D)
# K198 p.202: junk from 204's drawing at the end of 203; 204's drawing
S.sub('e43', 198, 'which deseends lowest. 1N 2 VV/NV \\` VOAS VEER NSA ANVIAN', 'which deseends lowest.')
S.sub('e44', 198, '[^204]: The fourth fire:', '[^204]: The fourth fire: ' + D)
# K199 p.203: 205, 206 (drawings; calls as junk)
l205, l206 = L(205, 199), L(206, 199)
S.sub('e45', 199, 'angles of the cakra.??\\*', 'angles of the cakra.[^%s]' % l205)
S.sub('e46', 199, 'fourteen-spoked cakra. °°’', 'fourteen-spoked cakra.[^%s]' % l206)
i, j, _ = S.lines(199, 'K -', 6); S.spans.append([i, j, '[^%s]: %s\n[^%s]: %s' % (l205, D, l206, D), 'e47'])
S.build(); S.save('/home/claude/finn/specs/finn05-spec.json')
