# Finn, notes 01 and 02 (second pass, on the text after pf709 and pf712): footnote text the OCR had dropped, restored where two
# blind Sonnet readers of the page images wrote the same (rd/brief.txt; both agreed on all seven items, 3 Nov 2026, night).
import sys, json; sys.path.insert(0, '/home/claude/finn')
import fnlib
fnlib.ROOT = '/home/claude/finn/md2/'
from fnlib import Spec
R = {"r1_13": "Sanjukta Gupta, Dirk Jan Hoens, and Teun Goudriaan, Hindu Tantrism (Leiden: E.J. Brill, 1979), p. 18.",
     "r2_14": "In the eyes of their devotees Śiva and Viṣṇu each assume a similar metaphysical status.",
     "r3_11": "Ibid., p. 595.", "r4_37end": "(Ibid., p. 130.)",
     "r5_14": "She evolves into the threefold śaktis Icchā, Jñāna and Kriyā.",
     "r5_15": "\"Rasa\" which usually means \"flavour, juice, sentiment or absorbing interest in\" etc., here has the Tantric sense of the joyful union of Śiva and Śakti.",
     "r5_16": "I.e., Śiva. See the \"Introd. to the Philo. of the Texts\"."}
S1 = Spec('01')
# K9 p.13: 13's authors (the OCR kept only the title onwards)
S1.sub('k01', 9, '[^13]: Hindu Tantrism (Leiden: E.J. Brill, 1979), p. 18.', '[^13]: ' + R['r1_13'])
# K10 p.14: 14 (only its last words were in the Markdown, as a stray line; the call as junk)
S1.sub('k02', 10, 'Siva and Viṣṇu1" are no more', 'Siva and Viṣṇu[^14] are no more')
S1.sub('k03', 10, '8. Praise of deities and relation of their exploits\n\nsimilar metaphysical status.', '8. Praise of deities and relation of their exploits\n\n[^14]: ' + R['r2_14'])
S1.build(); S1.save('/home/claude/finn/specs/finn01r-spec.json')
S2 = Spec('02'); L = S2.L
# K51 p.55: 11 (its text was missing)
l = L(11, 51)
S2.sub('k04', 51, 'the "ultimate reality"11 and', 'the "ultimate reality"[^%s] and' % l)
S2.sub('k05', 51, '[^10-p55]: Often the Kula doctrine ts referred to as Kaulism.', '[^10-p55]: Often the Kula doctrine ts referred to as Kaulism.\n[^%s]: %s' % (l, R['r3_11']))
# K59 p.63: the last line of 37
S2.sub('k06', 59, 'Ŝiva Pramātā = Supreme Experiencer.', 'Ŝiva Pramātā = Supreme Experiencer. ' + R['r4_37end'])
# K73 p.77: 14-16 (missing; the calls as junk or lost)
l4, l5, l6 = L(14, 73), L(15, 73), L(16, 73)
S2.sub('k07', 73, 'become threefold,1+', 'become threefold,[^%s]' % l4)
S2.sub('k08', 73, 'comes from union!’ with the Supreme Akula and become', 'comes from union[^%s] with the Supreme Akula[^%s] and become' % (l5, l6))
i, j, ls = S2.lines(73, '[^13]: The Sanskrit reads', 1)
S2.spans.append([j, j, '\n[^%s]: %s\n[^%s]: %s\n[^%s]: %s' % (l4, R['r5_14'], l5, R['r5_15'], l6, R['r5_16']), 'k09'])
S2.build(); S2.save('/home/claude/finn/specs/finn02r-spec.json')
