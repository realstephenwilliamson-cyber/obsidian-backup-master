# Finn note 09 (K321-K360, VT Chapter IV commentary): plain or unnumbered footnotes, calls a number off or as junk, label remnants,
# settled from the PDF's text layer and the page images (K335, K349, K350).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
S = Spec('09'); L = S.L
# K322 p.326: 33; stray labels and a line of label remnants (it had made the next definitions part of a paragraph)
l = L(33, 322)
S.sub('i01', 322, 'vāecya and vācaka,łł -i.e.', 'vāecya and vācaka,[^%s] -i.e.' % l)
S.sub('i02', 322, '85\\.\n\n84\\.\n\n8ò.\n\n8\\. ENTERING', '8\\. ENTERING')
S.sub('i03', 322, 'OH SUPREME LADY:\n\n1. 56.\n[^31]:', 'OH SUPREME LADY:\n\n[^31]:')
S.para('i04', 322, '33\\. See Chapter I footnote 21', 1, l)
# K328 p.332: 64
l = L(64, 328)
S.sub('i05', 328, 'impelling speed,ĉ\\* She', 'impelling speed,[^%s] She' % l)
S.para('i06', 328, '64\\. The phrase "ājavañjavibhāvena"', 1, l)
# K329 p.333: 68, 71 (71 run into the end of 70); junk after 70
l8, l1 = L(68, 329), L(71, 329)
S.sub('i07', 329, 'the three sSaktis,ë8 and', 'the three sSaktis,[^%s] and' % l8)
S.sub('i08', 329, 'viga.[^70] ’° Of the varpas (the three are) Vāgbhava, Kāmarāja and akti blja.” And', 'viga.[^70] Of the varpas (the three are) Vāgbhava, Kāmarāja and akti blja.[^%s] And' % l1)
S.para('i09', 329, '68\\. See the commentary to the following', 1, l8)
S.sub('i10', 329, '(Singh, Vijnānabhairava, p.\n\n65.) 71\\. These are', '(Singh, Vijnānabhairava, p. 65.)\n[^%s]: These are' % l1)
# K330 p.334: 74
l = L(74, 330)
S.sub('i11', 330, 'PRAYED T0,7\\* SHE', 'PRAYED T0,[^%s] SHE' % l)
S.para('i12', 330, '74\\. The Sanskrit reads "japtā"', 1, l)
# K335 p.339: 93, 94 plain; the calls 93-96 had carried 95, 96 or been junk
l3, l4 = L(93, 335), L(94, 335)
S.sub('i13', 335, 'GRAMMAR[^95] AND', 'GRAMMAR[^%s] AND' % l3)
S.sub('i14', 335, 'He introduces[^96] the', 'He introduces[^%s] the' % l4)
S.sub('i15', 335, 'SPROUTING DESIRE; 95', 'SPROUTING DESIRE;[^95]')
S.sub('i16', 335, 'MORNING6 SUN;', 'MORNING[^96] SUN;')
S.para('i17', 335, '93\\. A reference to Paṇini', 1, l3)
S.para('i18', 335, '94\\. Literally: "he causes', 1, l4)
# K336 p.340: 100
l = L(100, 336)
S.sub('i19', 336, 'in the heart of Kāminī. "100', 'in the heart of Kāminī. "[^%s]' % l)
S.para('i20', 336, '100\\. "yithout a head"', 1, l)
# K339 p.343: 115
l = L(115, 339)
S.sub('i21', 339, 'the middle saktý¿!115 in', 'the middle saktý[^%s] in' % l)
S.para('i22', 339, '115\\. I.e., Kundalini sakti.', 1, l)
# K342 p.346: stray labels
S.sub('i23', 342, '\n\n122,\n\n128\\.\n\n124\\.\n\n129\\.\n\n126\\.\n\n127\\.\n\n[^123]:', '\n\n[^123]:')
# K349 p.353: 151-153 (calls as digits; 150's definition held 153's text, 150-152 plain)
l1, l2, l3 = L(151, 349), L(152, 349), L(153, 349)
S.sub('i24', 349, "(the mantra's) reigning supremacy.151", "(the mantra's) reigning supremacy.[^%s]" % l1)
S.sub('i25', 349, 'the five desires.152 Here', 'the five desires.[^%s] Here' % l2)
S.sub('i26', 349, 'the eleventh one "p".153', 'the eleventh one "p".[^%s]' % l3)
S.para('i27', 349, '150\\. This, presumably', 1, '150')
S.para('i28', 349, '151\\. The "element in the supporting', 1, l1)
S.sub('i29', 349, '. There are five "desires" because the god of desire Kāma has\n\nfive arrows.\n\n[^150]: . There are eleven Rudras.',
      '[^%s]: There are five "desires" because the god of desire Kāma has five arrows.\n[^%s]: There are eleven Rudras.' % (l2, l3))
# K351 p.355: 159
l = L(159, 351)
S.sub('i30', 351, 'with the goad!53 and', 'with the goad[^%s] and' % l)
S.para('i31', 351, '159\\. - The "goad"', 1, l, strip=r'^159\\\. - ')
S.build(); S.save('/home/claude/finn/specs/finn09-spec.json')
