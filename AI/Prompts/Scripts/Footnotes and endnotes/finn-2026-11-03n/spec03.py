# Finn note 03 (K81-K120, KCT Chapters II-V): footnotes left plain, merged, mislabelled, or with label remnants, settled from the
# PDF's text layer (images for K83, K85, K95).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
S = Spec('03'); L = S.L
# K83 p.87: 72's text sat at the end of 71's definition; 73 and 74 were defined as 72 and 73; the call 74 left as junk
S.sub('c01', 83, 'yantra mixture. 7\\*', 'yantra mixture.[^74]')
S.sub('c02', 83, 'for the purpose of sādhana. The name of Svayambhīi is used for vartous plants.\n[^72]: I.e., wine.\n[^73]: I.e., the mixture',
      'for the purpose of sādhana.\n[^72]: The name of Svayambhīi is used for vartous plants.\n[^73]: I.e., wine.\n[^74]: I.e., the mixture')
# K84 p.88: label remnants inside 80
S.sub('c03', 84, 'Verses 30ff 75. 76. 77. 78. 79. 80. describe', 'Verses 30ff describe')
# K85 p.89: 81 (unnumbered), 83 (in 82's definition, with the illustration's caption)
S.sub('c04', 85, 'highest blissë! - as if', 'highest bliss[^81] - as if')
S.sub('c05', 85, '(to her).83', '(to her).[^83]')
S.para('c06', 85, 'Her state of bliss ts produced by the initiation rite.', 1, '81', strip=None)
S.sub('c07', 85, 'see Part III on Symbolism. Illustration to S 81. Verse 833 I.e., the name of the uninitiated woman and the mantra.',
      'see Part III on Symbolism. Illustration to Verse 33: *(a drawing in the print)*\n[^83]: I.e., the name of the uninitiated woman and the mantra.')
# K86 p.90: 84; label remnants inside 89
S.sub('c08', 86, 'the Padminīs8\\* of', 'the Padminīs[^84] of')
S.para('c09', 86, '84\\. The best of the four', 1, '84')
S.sub('c10', 86, 'everlasting life 84. 85. 86. 87. 88. which', 'everlasting life which')
# K90 p.94, K91 p.95: label remnants inside 105, 107, 109
S.sub('c11', 90, 'Of its rituals 101. 102. 108. 104. which', 'Of its rituals which')
S.sub('c12', 91, '[^107]: 10?, The purified', '[^107]: The purified')
S.sub('c13', 91, '[^109]: 109, "Madhuparka”', '[^109]: "Madhuparka”')
# K92 p.96: 112
S.sub('c14', 92, 'grant me the fuil attainment. 112', 'grant me the fuil attainment.[^112]')
S.para('c15', 92, '112. Here, the use', 1, '112', strip=r'^112\. ')
# K93 p.97: 117
S.sub('c16', 93, 'daily pūja,!17', 'daily pūja,[^117]')
S.para('c17', 93, '117\\. There are three types', 1, '117')
# K94 p.98: 118-120 unnumbered at the foot; 118's definition held only label remnants
S.sub('c18', 94, 'sufficiently encouraged.119 And', 'sufficiently encouraged.[^119] And')
S.sub('c19', 94, 'the former,12° the latter', 'the former,[^120] the latter')
S.para('c20', 94, 'According to Maitra the hymm', 1, '118', strip=None)
S.para('c21', 94, 'Reluctant to eat in the presence', 1, '119', strip=None)
S.sub('c22', 94, 'Presumably "former" refers to the purified women of Verse 51.\n\n[^118]: , 119.', '[^120]: Presumably "former" refers to the purified women of Verse 51.')
# K95 p.99: 121 (six lines at the foot); a stray label
S.sub('c23', 95, '121\\.\n\nIf only one woman', 'If only one woman')
S.sub('c24', 95, 'non-kula women.121 In the', 'non-kula women.[^121] In the')
S.para('c25', 95, 'As given in Chapter VII Verses 42-44', 6, '121', strip=None)
# K96 p.100: a line of label remnants that made the next definition part of a paragraph
S.sub('c26', 96, '\n\n122. 128. 124.\n[^124]: I.e., Assam.', '\n\n[^124]: I.e., Assam.')
# K100 p.104: 137, 138
S.sub('c27', 100, 'or to vatukasi37 or bhatravas,!38 then', 'or to vatukas[^137] or bhatravas,[^138] then')
S.para('c28', 100, '137\\. Forms of Śiva', 1, '137')
S.para('c29', 100, '138\\. They are the eight', 1, '138')
# K102 p.106: 141, 145; junk after 144
S.sub('c30', 102, 'Look at my beloved:1\\*1 (I long', 'Look at my beloved:[^141] (I long')
S.sub('c31', 102, 'MANTRA.[^144] 1\\#%', 'MANTRA.[^144]')
S.sub('c32', 102, 'mardin, 1%5', 'mardin,[^145]')
S.para('c33', 102, '141\\. Literally: "friend"', 1, '141')
S.para('c34', 102, '145\\. Presumably the nine', 1, '145')
# K103 p.107: junk after 147
S.sub('c35', 103, 'Kkāmakalā;[^147] 1\\*7', 'Kkāmakalā;[^147]')
# K107 p.111: label remnants inside 171
S.sub('c36', 107, 'not obliged 168. 169. 170. to do so.', 'not obliged to do so.')
# K111 p.115: 181 (at the end of 180's definition); a stray label
S.sub('c37', 111, '181\\.\n\n15\\. (And) he should', '15\\. (And) he should')
S.sub('c38', 111, 'so do they181 produce', 'so do they[^181] produce')
S.sub('c39', 111, 'the zenith and the nadir. I.e., the various malignant', 'the zenith and the nadir.\n[^181]: I.e., the various malignant')
# K113 p.117: two stray labels
S.sub('c40', 113, '34\\.\n\n187\\.\n\n188\\.\n\n', '34\\.\n\n')
# K114 p.118, K115 p.119: label remnants in 190 and 192
S.sub('c41', 114, 'the even more 189. 190. esoterie', 'the even more esoterie')
S.sub('c42', 115, '"If I am your son", 193.', '"If I am your son".')
# K118 p.122: 208; junk after 207
S.sub('c43', 118, 'previously mentioned.[^207] 7', 'previously mentioned.[^207]')
S.sub('c44', 118, 'pī¢ha® 8 on lotuses', 'pī¢ha[^208] on lotuses')
S.para('c45', 118, '208\\. I.e., the KĀIĪ', 1, '208')
S.build(); S.save('/home/claude/finn/specs/finn03-spec.json')
