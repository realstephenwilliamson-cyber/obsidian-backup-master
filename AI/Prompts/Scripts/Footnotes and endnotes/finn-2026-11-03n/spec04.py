# Finn note 04 (K121-K160, KCT Chapters VI-VII, VT Chapter I begins): plain or mislabelled footnotes, label remnants, settled from
# the PDF's text layer (images for K134, K139, K154).
import sys; sys.path.insert(0, '/home/claude/finn')
from fnlib import Spec
S = Spec('04'); L = S.L
# K122 p.126: 220 (labelled 222)
S.sub('d01', 122, 'Proceeding to Jãālandhara?2° he', 'Proceeding to Jãālandhara[^220] he')
S.para('d02', 122, '222\\. I.e., the breasts.', 1, L(220, 122))
# K123 p.127: a stray label
S.sub('d03', 123, '228\\.\n\n7\\. There also', '7\\. There also')
# K126 p.130: label remnants in 241
S.sub('d04', 126, '[^241]: 288. 289. The three', '[^241]: The three')
# K129 p.133: 250
S.sub('d05', 129, 'of Mahiṣamardinī. 25°', 'of Mahiṣamardinī.[^250]')
S.para('d06', 129, '250\\. "Three world blja', 1, L(250, 129))
# K131 p.135: 260 (its call was given to 261's place), 261; a stray label
S.sub('d07', 131, '13 & 14.\n\n206\\.\n\n12\\. The deity', '13 & 14.\n\n12\\. The deity')
S.sub('d08', 131, 'TO THE HEARTṬ!"260', 'TO THE HEARTṬ!"[^260]')
S.sub('d09', 131, '(HOMAGE TO THE ELBOWS:)[^260]', '(HOMAGE TO THE ELBOWS:)[^%s]' % L(261, 131))
S.para('d10', 131, '261\\. An amulet is conventionally', 1, '261')
# K134 p.138: the print numbers two notes 272; the second has no call (left plain, with the print's number)
S.sub('d11', 134, '273\\. The image behind this verse', '272\\. The image behind this verse')
# K139 p.143: 276, 277 (unnumbered); label remnants
S.sub('d12', 139, 'peace and welfare,?276 Oh', 'peace and welfare,[^%s] Oh' % L(276, 139))
S.sub('d13', 139, 'called dakgina.?77 And', 'called dakgina.[^%s] And' % L(277, 139))
S.para('d14', 139, 'The "Sāntisvastayana” eeremony.', 1, '276', strip=None)
S.sub('d15', 139, '\n\n276. 277.', '')
S.para('d16', 139, 'According to Goudriaan (Hindu Tantric', 1, '277', strip=None)
# K151 p.155: 11
l = L(11, 151)
S.sub('d17', 151, 'EMBODIMENT OF THE PITHAS. 11', 'EMBODIMENT OF THE PITHAS.[^%s]' % l)
S.para('d18', 151, '11\\. "PIthas" are geographical', 1, l)
# K154 p.158: 24; the OCR had moved "In line" and "state" (with the call) into the quotation above, and "This is" and "classes" out of their sentence
l = L(24, 154)
S.sub('d19', 154, 'In line state?\\* "Were Mahesvara', '"Were Mahesvara')
S.sub('d20', 154, 'with the cogent argument already state, She is in an expanded due to', 'In line with the cogent argument already state, She is in an expanded state[^%s] due to' % l)
S.sub('d21', 154, '\n\nThis is classes\n\n28\\.\n\n', '\n\n')
S.sub('d22', 154, 'an indirect way of saying that the "ganas" are the eight of letters.', 'This is an indirect way of saying that the "ganas" are the eight classes of letters.')
S.para('d23', 154, '24\\. The Sanskrit word used here', 1, l)
# K157 p.161: 41
l = L(41, 157)
S.sub('d24', 157, 'the nature of varṇa;\\*1 mantra', 'the nature of varṇa;[^%s] mantra' % l)
S.para('d25', 157, '41\\. In this context, the word', 1, l)
# K158 p.162: 47
l = L(47, 158)
S.sub('d26', 158, '(to it)."#7', '(to it)."[^%s]' % l)
S.para('d27', 158, '47\\. The meaning seems to be', 1, l)
S.build(); S.save('/home/claude/finn/specs/finn04-spec.json')
