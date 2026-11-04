# finn_spec.py (3 Nov 2026): Finn's 13 <sup> remnants, with the footnotes of the same pages that the converter left plain or
# mislabeled, settled from the PDF's text layer (and the page images for the drawings and p. 117). -> finn-spec.json
import json, glob, re
F = '/mnt/user-data/uploads/Obsidian Vault/Library/Trika/The Kulacudamani Tantra and The Vamakesvara Tantra (Finn)/'
P = lambda n: 'Library/Trika/The Kulacudamani Tantra and The Vamakesvara Tantra (Finn)/' + glob.glob(F + 'The Kulacudamani Tantra %s*.md' % n)[0].rsplit('/', 1)[-1]
T = {}
def txt(p):
    if p not in T: T[p] = open('/mnt/user-data/uploads/Obsidian Vault/' + p, encoding='utf-8').read()
    return T[p]
E = []
def ed(i, n, old, new):
    p = P(n); t = txt(p); c = t.count(old); assert c == 1, (i, c, old[:70]); E.append({'id': i, 'path': p, 'old': old, 'new': new})

# 02, p. 65 (PDF 61): the Introduction's notes 38-42, all plain; labels 38-42 are taken in this note, so -p65 (the note's own convention)
ed('f02a', '02', 'samāvesa.38 Kashmir', 'samāvesa.[^38-p65] Kashmir')
ed('f02b', '02', 'Turyãttita. <sup>39</sup>', 'Turyãttita.[^39-p65]')
ed('f02c', '02', 'final attainment.+\\*+°', 'final attainment.[^40-p65]')
ed('f02d', '02', 'comes into play....\\*1', 'comes into play....[^41-p65]')
ed('f02e', '02', 'Śāmbhavopāya."\\*?', 'Śāmbhavopāya."[^42-p65]')
ed('f02f', '02', '38\\. Commentary to VT V:27-33.\n\n39\\. Pandit, Kashmir Satvtsm, pp. 211-12.\n\n40\\. Commentary to VT V:27-33.\n\nt Kgemarãja, Pratyabhijnāhṛdayam, p. 29.\n\nPandey, Abhinavagupta, p. 91.\n',
   '[^38-p65]: Commentary to VT V:27-33.\n[^39-p65]: Pandit, Kashmir Satvtsm, pp. 211-12.\n[^40-p65]: Commentary to VT V:27-33.\n[^41-p65]: Kgemarãja, Pratyabhijnāhṛdayam, p. 29.\n[^42-p65]: Pandey, Abhinavagupta, p. 91.\n')

# 03, pp. 116-117 (PDF 112-113): calls 183-188; the converter had labelled 185 as 183, 186 as 184-p117, 188 as 186
ed('f03a', '03', '^pg112\n\n183,\n\n21\\. And making a rāja yantra <sup>183</sup>whose', '^pg112\n\n21\\. And making a rāja yantra[^183] whose')
ed('f03b', '03', 'the situation (in general).[^184]\n\nS.K. Ramachandra Rao, Tantra Mantra Yantra, p.27.\n\n[^184]:', 'the situation (in general).[^184]\n\n[^183]: S.K. Ramachandra Rao, Tantra Mantra Yantra, p.27.\n[^184]:')
ed('f03c', '03', 'kulas"185 is willingly (produced).[^183]', 'kulas"[^185] is willingly (produced).')
ed('f03d', '03', 'with the (other things),[^184-p117]\' when', 'with the (other things),[^186] when')
ed('f03e', '03', 'Kāmakalā!87 is enclosed', 'Kāmakalā[^187] is enclosed')
ed('f03f', '03', 'he should perform the kula pūjā.[^186] At night', 'he should perform the kula pūjā.[^188] At night')
ed('f03g', '03', 'At night in an empty house, or in a garden or temple,\n\n185\\. I.e., HRIM.\n\n[^183]: "Kulacūdāmani"', 'At night in an empty house, or in a garden or temple,\n\n[^185]: "Kulacūdāmani"')
ed('f03h', '03', '[^184-p117]: See Chapter II Verses 21-22.\n[^186]: The Sanskrit text reads', '[^186]: See Chapter II Verses 21-22.\n[^187]: I.e., HRIM.\n[^188]: The Sanskrit text reads')

# 05, p. 187 (PDF 183): 156
ed('f05a', '05', 'the method of pūjā <sup>156</sup>by saying:', 'the method of pūjā[^156] by saying:')
ed('f05b', '05', '156\\. The basis for pūjā is the rīcakra with its nine component individual cakras.\n\n[^157]:', '[^156]: The basis for pūjā is the rīcakra with its nine component individual cakras.\n[^157]:')
# 05, pp. 197-198 (PDF 193-194): 188, 191, 193 are drawings in the print
ed('f05c', '05', 'the eight-spoked cakra. <sup>188</sup>', 'the eight-spoked cakra.[^188]')
ed('f05d', '05', '188\\. The third sakti: X >77 1 \\` 7\n\n[^189]:', '[^188]: The third sakti: *(a drawing in the print)*\n[^189]:')
ed('f05e', '05', 'ten-spoked cakra. <sup>191</sup>', 'ten-spoked cakra.[^191]')
ed('f05f', '05', 'The result is the ten-spoked cakra. 193\n\n191\\. Se "7\n\n[^192]:', 'The result is the ten-spoked cakra.[^193]\n\n[^191]: *(a drawing in the print)*\n[^192]:')
ed('f05g', '05', 'is actually the third śakti.\n\n193.\n\n*[p. 199]*', 'is actually the third śakti.\n[^193]: *(a drawing in the print)*\n\n*[p. 199]*')

# 09, p. 345 (PDF 341): 120
ed('f09a', '09', 'contains the Sparsa linga. <sup>12</sup>', 'contains the Sparsa linga.[^120]')
ed('f09b', '09', '"is the desire tṁat is bereft of a head...."[^121]\n\n120\\.\n\n121\\.\n\n120\\. A reference to the Svayambhū tiñga; the liñga most sensitive to "touch" (sparsa)?\n\n[^121]:',
   '"is the desire tṁat is bereft of a head...."[^121]\n\n[^120]: A reference to the Svayambhū tiñga; the liñga most sensitive to "touch" (sparsa)?\n[^121]:')
# 09, p. 350 (PDF 346): 134-138
ed('f09c', '09', '"explain words with words"13% ina circuitous', '"explain words with words"[^134] in a circuitous')
ed('f09d', '09', 'according to the yantra method. <sup>135</sup>', 'according to the yantra method.[^135]')
ed('f09e', '09', 'is in the Kāma(mantra):136', 'is in the Kāma(mantra):[^136]')
ed('f09f', '09', '"h" is called desire. "137', '"h" is called desire."[^137]')
ed('f09g', '09', 'The quotation literally reads: "He has explained words with words".\n\nThe following commentary describes the drawing of a yantra with its five composite blja mantras based on the Kāmamantra of Verses 45 and 46.\n\nThis Line seems to mean that according to the yantra method,\n\nthe sādhya can be any female...\n\nThe letter before "kẹ" is "h"; the letter before "1" is "r";\n\n134\\. , 185.\n\n[^138]: 6. 1837. the letter before "u" is "Z", hence HRĪṆ. I.e., the syllable',
   '[^134]: The quotation literally reads: "He has explained words with words".\n[^135]: The following commentary describes the drawing of a yantra with its five composite blja mantras based on the Kāmamantra of Verses 45 and 46.\n[^136]: This Line seems to mean that according to the yantra method, the sādhya can be any female...\n[^137]: The letter before "kẹ" is "h"; the letter before "1" is "r"; the letter before "u" is "Z", hence HRĪṆ.\n[^138]: I.e., the syllable')
# 09, p. 351 (PDF 347): 143, 144
ed('f09h', '09', 'that which follows \'ç\'."1#3', 'that which follows \'ç\'."[^143]')
ed('f09i', '09', 'And when {(they)1\\#\\* are enfolded', 'And when (they)[^144] are enfolded')
ed('f09j', '09', '(then) in the six\n\n143\\. There are five bhūtas. Joining together the one that precedes anusvāra in the fifth place (i.e. "e") with "a" making "ai"; and the one that follows "p" in the fifth place (i.e., "e") with "a" making another "ai". 144\\. I.e., the mantras HRIY and KLIM are enfolded.\n\n[^139]:',
   '(then) in the six\n\n[^139]:')
ed('f09k', '09', 'from "ā" is "Ù".\n\n*[p. 352]*', 'from "ā" is "Ù".\n[^143]: There are five bhūtas. Joining together the one that precedes anusvāra in the fifth place (i.e. "e") with "a" making "ai"; and the one that follows "p" in the fifth place (i.e., "e") with "a" making another "ai".\n[^144]: I.e., the mantras HRIY and KLIM are enfolded.\n\n*[p. 352]*')
# 09, p. 352 (PDF 348): 145-148 (the converter had put 145 at 146's place and 146 at a place with no call)
ed('f09l', '09', 'called Kandarpa: 145', 'called Kandarpa:[^145]')
ed('f09m', '09', "before 'kṣ' and 'h[^145]’", "before 'kṣ' and 'h’[^146]")
ed('f09n', '09', "precede 'h',[^146] tth', '1' and tu’, <sup>147</sup>", "precede 'h', tth', '1' and tu’,[^147]")
ed('f09o', '09', 'what has been cast into the womb.1+\\#s', 'what has been cast into the womb.[^148]')
ed('f09p', '09', '147\\. The letter preceding "h" in the alphabet', '[^147]: The letter preceding "h" in the alphabet')
ed('f09q', '09', 'Hence STRĪṆ.\n\n148\\. I.e., one completes', 'Hence STRĪṆ.\n[^148]: I.e., one completes')
ed('f09r', '09', 'the two interlocking triangles.\n\n[^145]: The third desire', 'the two interlocking triangles.\n[^145]: The third desire')

# 10, p. 372 (PDF 368): 221 (labelled 222) and 222
ed('f10a', '10', 'the part before Indra.[^222] The second', 'the part before Indra.[^221] The second')
ed('f10b', '10', 'BAM. <sup>222</sup>', 'BAM.[^222]')
ed('f10c', '10', '221\\. "Jambha" is an epithet for Indra whieh stands for the letter\n\n"1"? However, the commentary that follows does not make elear\n\nwhat this first goad is.... Probably KROM.\n\n[^222]:',
   '[^221]: "Jambha" is an epithet for Indra whieh stands for the letter "1"? However, the commentary that follows does not make elear what this first goad is.... Probably KROM.\n[^222]:')
# 10, p. 394 (PDF 390): 73
ed('f10d', '10', 'the vidyās and pTthas. <sup>13</sup>', 'the vidyās and pTthas.[^73]')
ed('f10e', '10', 'the six of them,\n\n73\\. Although the vidyās', 'the six of them,\n\n[^73]: Although the vidyās')
ed('f10f', '10', 'realisation.\n\n[^72]: "Pindasiddhidah"', 'realisation.\n[^72]: "Pindasiddhidah"')
# 10, p. 399 (PDF 394, a plate the OCR read as junk): the two tags only
ed('f10g', '10', '<sup>९3</sup>', '९3')
ed('f10h', '10', '<sup>40</sup>२।१९।', '40२।१९।')
# 10, p. 413 (PDF 404), the bibliography: the 7 is not in the print; three entries the OCR ran together
ed('f10i', '10', 'Manohar, 1977). <sup>7</sup> M. Biardeau,', 'Manohar, 1977).\n\nM. Biardeau,')
ed('f10j', '10', 'Sciences Sociales, 1982). D.N. Bose and Hiralal', 'Sciences Sociales, 1982).\n\nD.N. Bose and Hiralal')
json.dump(E, open('finn-spec.json', 'w'), ensure_ascii=False, indent=0)
# simulate and check
out = dict(T)
for e in E: out[e['path']] = out[e['path']].replace(e['old'], e['new'])
for p, t in out.items():
    calls = re.findall(r'\[\^([^\]]+)\](?!:)', t); defs = re.findall(r'(?m)^\[\^([^\]]+)\]:', t)
    cs, ds = set(calls), set(defs)
    print(p.rsplit('/', 1)[-1], 'sup', len(re.findall('<sup', t)), 'calls', len(calls), 'defs', len(defs), 'no def', sorted(cs - ds)[:5], 'no call', sorted(ds - cs)[:5],
          'dup calls', sorted({c for c in calls if calls.count(c) > 1})[:5], 'dup defs', sorted({d for d in defs if defs.count(d) > 1})[:5])
    for m in re.finditer(r'(?m)^\[\^[^\]]+\]:', t):   # a definition run must follow a blank line
        k = m.start()
        if k >= 2 and t[k - 1] == '\n' and t[k - 2] != '\n':
            prev = t[t.rfind('\n', 0, k - 1) + 1:k - 1]
            if not prev.startswith('[^'): print('   def after a text line:', repr(prev[-60:]), repr(t[k:k + 30]))
print(len(E), 'edits')
