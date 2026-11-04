# Finn note 10 (K361-K408, VT Chapter IV-V commentary to the end): plain or mislabelled footnotes, calls as junk, label remnants,
# settled from the PDF's text layer and the page images (K375, K376, K381, K387).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
S = Spec('10'); L = S.L
# K361 p.365: 195
l = L(195, 361)
S.sub('j01', 361, "ning of 'kh'.\"195", "ning of 'kh'.\"[^%s]" % l)
S.para('j02', 361, '195\\. For this extraction', 2, l)
# K366 p.370: 216
l = L(216, 366)
S.sub('j03', 366, '"1" and "v",.216', '"1" and "v",.[^%s]' % l)
S.para('j04', 366, '216\\. The path is presumably', 1, l)
# K371 p.375: 228; stray labels
l = L(228, 371)
S.sub('j05', 371, 'THE KHECART SIDDHI?28', 'THE KHECART SIDDHI[^%s]' % l)
S.sub('j06', 371, '\n\n227\\.\n\n228\\.\n\n229\\.\n\n228\\. I.e., liberation.', '\n\n[^%s]: I.e., liberation.' % l)
# K375 p.379: 7, 8 (run together), 9 (unnumbered)
l7, l8, l9 = L(7, 375), L(8, 375), L(9, 375)
S.sub('j07', 375, 'PREVIOUSLY DESCRIBED MEDITATION.”', 'PREVIOUSLY DESCRIBED MEDITATION.[^%s]' % l7)
S.sub('j08', 375, 'Cakra means the triple type one also.', 'Cakra means the triple type one also.[^%s]' % l8)
S.sub('j09', 375, 'consider as silently.?', 'consider as silently.[^%s]' % l9)
S.sub('j10', 375, '7\\. Japa may be performed with the cakra internalised. The meditation (dhyāna) for Tripurã is contained in I:113-131. I.e., the cakra abridged',
      '[^%s]: Japa may be performed with the cakra internalised. The meditation (dhyāna) for Tripurã is contained in I:113-131.\n[^%s]: I.e., the cakra abridged' % (l7, l8))
S.para('j11', 375, '"Silently" here means', 1, l9, strip=None)
# K376 p.380: 10; label remnants in 13
l = L(10, 376)
S.sub('j12', 376, 'PUTRAJĪVIKAĄ AND', 'PUTRAJĪVIKA[^%s] AND' % l)
S.para('j13', 376, '10\\. The Rudrāksa seeds', 1, l)
S.sub('j14', 376, '[^13]: 11. 12 Though', '[^13]: Though')
# K378 p.382: 17
l = L(17, 378)
S.sub('j15', 378, 'THE COMPANY OF THE KHECARTS. 17', 'THE COMPANY OF THE KHECARTS.[^%s]' % l)
S.para('j16', 378, '17\\. The "Khecarts" are', 1, l)
# K379 p.383, K380 p.384: junk after 20; 21, 22
l1, l2 = L(21, 380), L(22, 380)
S.sub('j17', 379, 'successive increase.[^20] ??', 'successive increase.[^20]')
S.sub('j18', 380, '„them. ... "21', '„them. ... "[^%s]' % l1)
S.sub('j19', 380, 'IN TEN PARTS...22', 'IN TEN PARTS...[^%s]' % l2)
S.para('j20', 380, '21\\. The ascending order', 2, l1)
S.para('j21', 380, '22\\. The procedure for homa', 1, l2)
# K381 p.385: 31 (defined as 32), 32 (plain, labelled 33)
S.sub('j22', 381, 'the māyā bṛja;žł" placing', 'the māyā bṛja;[^31] placing')
S.sub('j23', 381, '33\\. With which mantra?', '[^32]: With which mantra?')
S.sub('j24', 381, '[^32]: I.e., the mantra HRIM.', '[^31]: I.e., the mantra HRIM.')
# K383 p.387: label remnants
S.sub('j25', 383, '\n\n40. 4l. 42. 48.\n\n[^40]:', '\n\n[^40]:')
# K387 p.391: 59, 60, 62; junk after 61
l9, l0, l2 = L(59, 387), L(60, 387), L(62, 387)
S.sub('j26', 387, 'a state of awareness";59 “the', 'a state of awareness";[^%s] “the' % l9)
S.sub('j27', 387, 'of guru etc."69 Because', 'of guru etc."[^%s] Because' % l0)
S.sub('j28', 387, 'the word nigarbha.[^61] £1', 'the word nigarbha.[^61]')
S.sub('j29', 387, 'widening perception? and action', 'widening perception[^%s] and action' % l2)
S.para('j30', 387, '59\\. "Parāmrsyatām"', 1, l9)
S.para('j31', 387, '60\\. I.e., the pure undivided', 2, l0)
S.para('j32', 387, '862\\. "Dp"', 1, l2)
# K388 p.392: 68
l = L(68, 388)
S.sub('j33', 388, 'and non-existence,68 as well', 'and non-existence,[^%s] as well' % l)
S.para('j34', 388, '68\\. "Kalanā" is a difficult', 1, l)
S.build(); S.save('/home/claude/finn/specs/finn10-spec.json')
