# Finn note 07 (K241-K280, VT Chapter I commentary, the vidyas and the nine cakras): plain or unnumbered footnotes, calls as junk or
# a number off, label remnants, settled from the PDF's text layer and the page images (K246, K269, K280).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
S = Spec('07'); L = S.L
# K241 p.245: 335, 336
l5, l6 = L(335, 241), L(336, 241)
S.sub('g01', 241, 'Sõtyabhāmā bhāmā.335 (And)', 'Sõtyabhāmā bhāmā.[^%s] (And)' % l5)
S.sub('g02', 241, "before 'ū',336 and placed", "before 'ū',[^%s] and placed" % l6)
S.para('g03', 241, '835\\. The reference to', 1, l5)
S.para('g04', 241, '536\\. See the chart in footnote 320.', 1, l6)
# K246 p.250: 349 (unnumbered, with the syllable numbers below its mantra); a label remnant in 350
l = L(349, 246)
S.sub('g05', 246, 'MAHĀTRIPURASUNDARĪ.3%9', 'MAHĀTRIPURASUNDARĪ.[^%s]' % l)
S.para('g06', 246, 'The root vidyā, so-called because', 2, l, strip=None)
S.sub('g07', 246, 'which consists of five 849. elements.', 'which consists of five elements.')
# K248 p.252: 357
l = L(357, 248)
S.sub('g08', 248, 'each one with bindu. "357', 'each one with bindu. "[^%s]' % l)
S.para('g09', 248, '357\\. Śiva = "h"', 1, l)
# K253 p.257: 370-372
l0, l1, l2 = L(370, 253), L(371, 253), L(372, 253)
S.sub('g10', 253, 'place of sacrifice,37 - in', 'place of sacrifice,[^%s] - in' % l0)
S.sub('g11', 253, 'HE SHOULD THEN PRESENT?! ĀTMĀSANA', 'HE SHOULD THEN PRESENT[^%s] ĀTMĀSANA' % l1)
S.sub('g12', 253, 'the bulbžł72 and', 'the bulb[^%s] and' % l2)
S.para('g13', 253, '870\\. The "place of sacrifice"', 1, l0)
S.para('g14', 253, '871\\. He should "present"', 2, l1)
S.para('g15', 253, '872\\. The "bulb" is', 1, l2)
# K262 p.266: 404; junk after 402
l = L(404, 262)
S.sub('g16', 262, '(case) ending.[^402] \\* ?', '(case) ending.[^402]')
S.sub('g17', 262, 'is Tripurā.... "4+', 'is Tripurā.... "[^%s]' % l)
S.para('g18', 262, '404\\. The verse actually reads', 1, l)
# K263 p.267, K264 p.268: junk after 408; 409
l = L(409, 264)
S.sub('g19', 263, 'all hopes".[^408] +908', 'all hopes".[^408]')
S.sub('g20', 264, 'MATERIAL BODIES.+99', 'MATERIAL BODIES.[^%s]' % l)
S.para('g21', 264, '409\\. - These sixteen', 2, l, strip=r'^409\\\. - ')
# K266 p.270: two stray labels
S.sub('g22', 266, '\n\n415\\.\n\n416\\.\n\n[^415]:', '\n\n[^415]:')
# K267 p.271: 418, 419
l8, l9 = L(418, 267), L(419, 267)
S.sub('g23', 267, 'one\'s\n\npurposes":#18', 'one\'s\n\npurposes":[^%s]' % l8)
S.sub('g24', 267, 'ALL GOOD FORTUNE.”19', 'ALL GOOD FORTUNE.[^%s]' % l9)
S.para('g25', 267, '418\\. The cakra called', 1, l8)
S.para('g26', 267, '419, Sarvasiddhipradā', 2, l9, strip=r'^419, ')
# K268 p.272: a label remnant in 420
S.sub('g27', 268, 'the worship of every cakra, 421.', 'the worship of every cakra.')
# K269 p.273: 423 (its call carried 425's label), 424, 425 (call as junk); 423 and 424 unnumbered; junk lines
l3, l4 = L(423, 269), L(424, 269)
S.sub('g28', 269, 'letters of the alphabet."[^425]', 'letters of the alphabet."[^%s]' % l3)
S.sub('g29', 269, 'from \'kṣ\'".”24', 'from \'kṣ\'".[^%s]' % l4)
S.sub('g30', 269, 'the fourteen-spoked one.\\*25 The queen', 'the fourteen-spoked one.[^425] The queen')
S.sub('g31', 269, '\n\nzyn\n\n"yāgeśī" is AIM.', '\n\n[^%s]: "yāgeśī" is AIM.' % l3)
S.sub('g32', 269, 'There are fourteen Manus, ten directions', '[^%s]: There are fourteen Manus, ten directions' % l4)
S.sub('g33', 269, 'to the first consonant "k".\n\n423. 424.', 'to the first consonant "k".')
# K271 p.275: 429
l = L(429, 271)
S.sub('g34', 271, 'The nigarbhas?’ deities', 'The nigarbhas[^%s] deities' % l)
S.para('g35', 271, '429\\. The "nigarbha deities"', 1, l)
# K273 p.277: 436
l = L(436, 273)
S.sub('g36', 273, 'by themselves.\\*+36', 'by themselves.[^%s]' % l)
S.para('g37', 273, '436\\. There exist "words”', 2, l)
# K274 p.278: 440
l = L(440, 274)
S.sub('g38', 274, 'the queen of the cakra is arrived at', 'the queen of the cakra[^%s] is arrived at' % l)
S.para('g39', 274, '440\\. Tripurāmbikā/Tripurasundart.', 1, l)
# K275 p.279: junk and label remnants
S.sub('g40', 275, 'tradition![^444] \\#%', 'tradition![^444]')
S.sub('g41', 275, '\n\n442\\.\n\n443\\.\n\n[^442]:', '\n\n[^442]:')
S.sub('g42', 275, 'in the exterior cakra. 444\\. ,', 'in the exterior cakra.')
# K276 p.280: 445 (its call carried 446's label), 446 (call as junk); junk after 448
l = L(445, 276)
S.sub('g43', 276, 'host of mantras[^446] has', 'host of mantras[^%s] has' % l)
S.sub('g44', 276, 'OF THE MUDRĀS\\*\\*6 OF', 'OF THE MUDRĀS[^446] OF')
S.sub('g45', 276, '(AND) OF THE YONI.[^448] \\*\\*8', '(AND) OF THE YONI.[^448]')
S.para('g46', 276, '445\\. I.e., goddesses.', 1, l)
# K277 p.281: 449
l = L(449, 277)
S.sub('g47', 277, 'satisfaction. "%49', 'satisfaction. "[^%s]' % l)
S.para('g48', 277, '449\\. Animā, Laghimā', 1, l)
# K278 p.282: junk after 453
S.sub('g49', 278, 'beings!"[^453] %53', 'beings!"[^453]')
# K279 p.283: 455 plain; calls 455-458 each carried the next label
S.sub('g50', 279, 'DOWNWARD POINTING ONE.[^456]', 'DOWNWARD POINTING ONE.[^%s]' % L(455, 279))
S.sub('g51', 279, 'the parāmarśa[^457] essence of all things composed of the thirty-six substances[^458] and', 'the parāmarśa[^456] essence of all things composed of the thirty-six substances[^457] and')
S.sub('g52', 279, "as 'Siva and Śakti'\".»#58", "as 'Siva and Śakti'\".[^458]")
S.para('g53', 279, '455\\. The Kāmakaąlā configuration', 1, '455')
S.sub('g54', 279, 'in Kashmir Satvism 460.', 'in Kashmir Satvism.')
# K280 p.284: 464
l = L(464, 280)
S.sub('g55', 280, 'in this letter Igi 464', 'in this letter Igi[^%s]' % l)
S.para('g56', 280, '464\\. The letter "s" can convert', 1, l)
S.build(); S.save('/home/claude/finn/specs/finn07-spec.json')
