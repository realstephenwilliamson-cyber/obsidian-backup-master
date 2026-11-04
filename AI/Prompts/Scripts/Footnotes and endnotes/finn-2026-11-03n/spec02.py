# Finn note 02 (K41-K80: Introduction to the Philosophy of the Texts, then the KCT translation, Chapter I): footnotes left plain,
# run together or mislabelled, settled from the PDF's text layer (images for K51, K52, K55, K57, K59, K70, K73, K77, K78).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
S = Spec('02'); L = S.L
# K43 p.47: note 1 (no number in the Markdown)
l = L(1, 43); S.sub('b01', 43, 'like himself.1! It seems', 'like himself.[^%s] It seems' % l)
S.para('b02', 43, 'Pandit, Kashmir Satvism, p. 94. The expression', 1, l, strip=None)
# K45 p.49: note 3 (labelled 5)
l = L(3, 45); S.sub('b03', 45, 'sexual intercourse? as part', 'sexual intercourse[^%s] as part' % l)
S.para('b04', 45, '5\\. Madya, Mapsa', 1, l)
# K47 p.51: note 7
l = L(7, 47); S.sub('b05', 47, 'the Supreme Being? into which', 'the Supreme Being[^%s] into which' % l)
S.para('b06', 47, '7\\. Expressed in Kashmir', 2, l)
# K51 p.55: notes 8-10 run together in one paragraph (11's text is missing: a restoration, later); the call 8 left no trace
l8, l9, l10 = L(8, 51), L(9, 51), L(10, 51)
S.sub('b07', 51, 'the meaning of it". Bhattacarya implies', 'the meaning of it".[^%s] Bhattacarya implies' % l8)
S.sub('b08', 51, 'at least a dozen.?', 'at least a dozen.[^%s]' % l9)
S.sub('b09', 51, 'these texts subscribe,!° or', 'these texts subscribe,[^%s] or' % l10)
S.sub('b10', 51, '8\\. B. Bhattacarya, Buddhist Esoterism, p. 81. 3. . Pandey, Abhinavagupta, pp. 594-97. 10. Often the Kula doctrine ts referred to as Kaulism.',
      '[^%s]: B. Bhattacarya, Buddhist Esoterism, p. 81.\n[^%s]: Pandey, Abhinavagupta, pp. 594-97.\n[^%s]: Often the Kula doctrine ts referred to as Kaulism.' % (l8, l9, l10))
# K52 p.56: 12
l = L(12, 52); S.sub('b11', 52, 'Sakti".12 These', 'Sakti".[^%s] These' % l)
S.para('b12', 52, '12\\. Ibid., p. 595.', 1, l)
# K53 p.57: 18, 19
l18, l19 = L(18, 53), L(19, 53)
S.sub('b13', 53, 'sugumnā".18 N.', 'sugumnā".[^%s] N.' % l18)
S.sub('b14', 53, 'to Sakti,19 but', 'to Sakti,[^%s] but' % l19)
S.para('b15', 53, '18\\. Lalitã-Sahasranãman, p. 3.', 1, l18)
S.para('b16', 53, '19, N. Bhattacharyya', 1, l19, strip=r'^19, ')
# K55 p.59: 26-28
l26, l27, l28 = L(26, 55), L(27, 55), L(28, 55)
S.sub('b17', 55, 'kula kalās"?6 suggests', 'kula kalās"[^%s] suggests' % l26)
S.sub('b18', 55, 'and that Speech?” is abstract and eternal.?8 Speech', 'and that Speech[^%s] is abstract and eternal.[^%s] Speech' % (l27, l28))
S.sub('b19', 55, '26\\. NSA 1:10.\n\n27\\. Capitalised to indicate that it ts speech not in the vocal\n\narticulated sense, but Speech in the most abstract form. 28. .\n\n8 One of the Sanskrit words',
      '[^%s]: NSA 1:10.\n[^%s]: Capitalised to indicate that it ts speech not in the vocal articulated sense, but Speech in the most abstract form.\n[^%s]: One of the Sanskrit words' % (l26, l27, l28))
# K57 p.61: 30-33
l30, l31, l32, l33 = L(30, 57), L(31, 57), L(32, 57), L(33, 57)
S.sub('b20', 57, 'action in succession".30', 'action in succession".[^%s]' % l30)
S.sub('b21', 57, 'simply a power. 31', 'simply a power.[^%s]' % l31)
S.sub('b22', 57, 'is called vimarśa. ž?', 'is called vimarśa.[^%s]' % l32)
S.sub('b23', 57, 'of the personality.ž3', 'of the personality.[^%s]' % l33)
S.sub('b24', 57, '30\\. Pandey, Abhinavagupta, p. 327.\n\n31\\. Ibid., p. 329.\n\n82\\. Pandit, Kashmir Saivism, p. 205.\n\n53\\. Pandey, Abhinavagupta, p. 325.',
      '[^%s]: Pandey, Abhinavagupta, p. 327.\n[^%s]: Ibid., p. 329.\n[^%s]: Pandit, Kashmir Saivism, p. 205.\n[^%s]: Pandey, Abhinavagupta, p. 325.' % (l30, l31, l32, l33))
# K59 p.63: junk before call 37; a stray "36\." line (36 has its definition)
S.sub('b25', 59, 'Mantramaheśvaražł[^37]', 'Mantramaheśvara[^37]')
S.sub('b26', 59, '\n\n36\\.\n\n[^35]:', '\n\n[^35]:')
# K70 p.74: the print has no call after Vaisnava; 2 after "Tantras", 3 after "Mahasarasvata Tantra,", 4 after "Yoginijalasambara Tantra,"
S.sub('b27', 70, 'Vaiṣṇava,[^2-p74] the', 'Vaiṣṇava, the')
S.sub('b28', 70, 'excellent Tantras[^3] of the Mothers: the Mahāsārasvata Tantra,[^4-p74]’ the Yoginījālasambara Tantra, \\*',
      'excellent Tantras[^2-p74] of the Mothers: the Mahāsārasvata Tantra,[^3] the Yoginījālasambara Tantra,[^4-p74]')
# K71 p.75: 5-8, the four paragraphs at the foot
l5, l6, l7, l8 = L(5, 71), L(6, 71), L(7, 71), L(8, 71)
S.sub('b29', 71, 'called Bhairavāṣṭaka,>’', 'called Bhairavāṣṭaka,[^%s]' % l5)
S.sub('b30', 71, 'Yāmalaṣṭaka\n\nTantras, 6', 'Yāmalaṣṭaka\n\nTantras,[^%s]' % l6)
S.sub('b31', 71, 'Kalāsāra Tantra,” and', 'Kalāsāra Tantra,[^%s] and' % l7)
S.sub('b32', 71, 'Trogdalottara Tantras ,¿\' Pancāmṛta', 'Trogdalottara Tantras ,[^%s] Pancāmṛta' % l8)
S.para('b33', 71, '"Bhairavāgṭaka" refers', 1, l5, strip=None)
S.para('b34', 71, 'Following footnote 18 of this Sanskrit text the Bahurüpāṣṭaka', 1, l6, strip=None)
S.para('b35', 71, 'In the VT, the Kalāpaka Tantra', 1, l7, strip=None)
S.para('b36', 71, 'The VT gives this sequence', 1, l8, strip=None)
# K76 p.80: 34 (call junk; a line of label remnants)
l = L(34, 76); S.sub('b37', 76, 'the sādhaka,ž"\n\n80. 81. 82. 35.\n\n34\\. The "sãdhaka" is', 'the sādhaka,[^%s]\n\n[^%s]: The "sãdhaka" is' % (l, l))
# K77 p.81: 37; 40, 41, 42 run together in 40's definition; label remnants
l37 = L(37, 77)
S.sub('b38', 77, '85\\.\n\n34\\. first meditating', '34\\. first meditating')
S.sub('b39', 77, 'on the kula?ł7 up above.', 'on the kula[^%s] up above.' % l37)
S.sub('b40', 77, 'the kula disciple. %1', 'the kula disciple.[^41]')
S.sub('b41', 77, 'the; kula mother+?\n\n86. 87. 88. 39. 40. 41.\n\n37\\. I.e., Kundalini.', 'the; kula mother[^42]\n\n[^%s]: I.e., Kundalini.' % l37)
S.sub('b42', 77, '[^40]: I.e., the Kundalint. The second half of Verse 36 and Verse 37 deseribe the "dhyāna" or the way in which one should visualize the gurus in : meditation. I.e., the Kundalini.',
      '[^40]: I.e., the Kundalint.\n[^41]: The second half of Verse 36 and Verse 37 deseribe the "dhyāna" or the way in which one should visualize the gurus in : meditation.\n[^42]: I.e., the Kundalini.')
# K78 p.82: 45 (defined as 46), 46 (as 47), 47 (plain, labelled 48), 48 (as 49), 49 (plain, labelled 50); calls 45 and 48 junk
S.sub('b43', 78, 'paśu\\*#5 it', 'paśu[^45] it')
S.sub('b44', 78, 'kulíina\\*#8 is', 'kulíina[^48] is')
S.sub('b45', 78, '48\\. "Initiation" does not', '[^47]: "Initiation" does not')
S.sub('b46', 78, '50\\. The guru is the aspirant\'s most powerful guide on the spiritual path. 43\\. , 44. 45. 46. 47. 48.', '[^49]: The guru is the aspirant\'s most powerful guide on the spiritual path.')
S.sub('b47', 78, '[^46]: "Pagu" literally', '[^45]: "Pagu" literally')
S.sub('b48', 78, '[^47]: I.e., the guru.\n[^49]: I.e., the guru.', '[^46]: I.e., the guru.\n[^48]: I.e., the guru.')
# K80 p.84: label remnants inside 60
S.sub('b49', 80, 'offering of Bhairava to Bhairava. 57. 58. 59. 60. The same idea', 'offering of Bhairava to Bhairava. The same idea')
S.build(); S.save('/home/claude/finn/specs/finn02-spec.json')
