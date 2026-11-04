# Finn note 01 (Introduction, K1-K40): footnotes left plain or mislabelled, settled from the PDF's text layer (images for K11, K31, K36).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
S = Spec('01')
# K11 p.15: the print has calls 15, 16 (after "Vamakesvara Tantra."), 17 (after "material"); none after "tantra"; 18 has no call
S.sub('a01', 11, 'the word "tantra[^16]" is', 'the word "tantra" is')
S.sub('a02', 11, 'Vamakeś5-vara Tantra.[^17] Similarly', 'Vamakeś5-vara Tantra.[^16] Similarly')
S.sub('a03', 11, 'textual material[^18] to which', 'textual material[^17] to which')
S.sub('a04', 11, 'p. 11.\n[^18]: Texts which go by', 'p. 11.\n\n18\\. Texts which go by')
# K14 p.18: 25 and 26 (both labelled 26)
S.sub('a05', 14, 'sandhyãābhāgṣa?5 when', 'sandhyãābhāgṣa[^25] when')
S.sub('a06', 14, 'AD 1500.26 This', 'AD 1500.[^26] This')
S.para('a07', 14, '26\\. Sandhyã bhāga', 1, '25')
S.para('a08', 14, '26\\. Sir John Woodroffe', 2, '26')
# K15 p.19: 29
S.sub('a09', 15, 'AD 80029 - can', 'AD 800[^29] - can')
S.para('a10', 15, '29\\. Goudriaan, Tantrie', 1, '29')
# K19 p.23: 47, 48
S.sub('a11', 19, 'their religion.\\*?', 'their religion.[^47]')
S.sub('a12', 19, 'Table One!t8 demonstrates', 'Table One[^48] demonstrates')
S.para('a13', 19, '47\\. Corpus Inscriptionum', 2, '47')
S.para('a14', 19, '48\\. See the Appendix.', 1, '48')
# K25 p.29: 66
S.sub('a15', 25, 'NĪ1ā66 is supposedly', 'NĪ1ā[^66] is supposedly')
S.para('a16', 25, '66\\. Ibid., p. 212.', 1, '66')
# K30 p.34: 81
S.sub('a17', 30, '“is flawless”"81 and', '“is flawless”"[^81] and')
S.para('a18', 30, '81\\. A familiarity', 1, '81')
# K31 p.35: 87, 90, 91; 89 has no call in the print ("can be judged from footnote eighty-nine"): its two lines joined, left plain
S.sub('a19', 31, 'makāras,ë7 whereas', 'makāras,[^87] whereas')
S.sub('a20', 31, 'five sacrifices"?0 - implying', 'five sacrifices"[^90] - implying')
S.sub('a21', 31, 'are rare91 and', 'are rare[^91] and')
S.para('a22', 31, '87\\. I.e., wine', 1, '87')
S.para('a23', 31, '89\\. Bharati says', 2, 'plain:89')
S.para('a24', 31, '90\\. Lalitã-Sahasranãman', 2, '90')
S.para('a25', 31, '91\\. "The left current', 1, '91')
# K32 p.36: 93
S.sub('a26', 32, 'uttarāmāya"9ž and', 'uttarāmāya"[^93] and')
S.para('a27', 32, '93\\. Rastogi, Krama', 1, '93')
# K33 p.37: 96 (labelled 36), 97
S.sub('a28', 33, 'in Chapter IV.98 In the edition', 'in Chapter IV.[^96] In the edition')
S.sub('a29', 33, 'Ānandāśama Series,97 the', 'Ānandāśama Series,[^97] the')
S.para('a30', 33, '36\\. Verse 58 has been', 1, '96')
S.para('a31', 33, '97\\. The \\_"Nityā', 3, '97')
# K34 p.38: 98
S.sub('a32', 34, 'Vidyānanda?8 that', 'Vidyānanda[^98] that')
S.para('a33', 34, '98\\. The Nityāgodasikārnava', 3, '98')
# K36 p.40: 109's second line stood above its first
S.sub('a34', 36, 'ikā listed by Pandey as a work of Kgemarāja. (Ibíid., p. 2586.)\n\n[^109]: One presumes that it is the same text as the Utpala Stotrāvali',
      '[^109]: One presumes that it is the same text as the Utpala Stotrāvali ikā listed by Pandey as a work of Kgemarāja. (Ibíid., p. 2586.)')
# K39 p.43: 116-118
S.sub('a35', 39, 'The assertion!15 is', 'The assertion[^116] is')
S.sub('a36', 39, "Jayaratha's commentaryt17 which", "Jayaratha's commentary[^117] which")
S.sub('a37', 39, 'the text...,118 something', 'the text...,[^118] something')
S.para('a38', 39, '116\\. Goudriaan, Hindu', 1, '116')
S.para('a39', 39, '117\\. Cormentary to VT', 1, '117')
S.para('a40', 39, '118\\. It is Goudriaan', 1, '118')
S.build(); S.save('/home/claude/finn/specs/finn01-spec.json')
