# The Talmud's top index note and the six seder notes (run after gen_talmud.py)
import json, collections, os
idx = json.load(open('idx.json'))
SED = ['Seder Zeraim', 'Seder Moed', 'Seder Nashim', 'Seder Nezikin', 'Seder Kodashim', 'Seder Tahorot']
by = collections.defaultdict(list)
for k, v in idx.items():
    s, t = k.split('|'); by[s].append((t, min(v), max(v), len(v)))
toc = json.load(open('/home/claude/sef/toc.json')); names = {t for s in by for t, _, _, _ in by[s]}; order = []
def walk(n):
    if isinstance(n, dict):
        if n.get('title') in names and 'Bavli' in json.dumps(n.get('categories', [])): order.append(n['title'])
        for v in n.values(): walk(v)
    elif isinstance(n, list):
        for v in n: walk(v)
walk(toc); pos = {t: i for i, t in enumerate(order)}
total = sum(x[3] for s in by for x in by[s])
def fm(d):
    out = ['---']
    for k, v in d.items():
        if isinstance(v, list): out.append(f'{k}:'); out += [f'  - {json.dumps(x, ensure_ascii=False)}' for x in v]
        else: out.append(f'{k}: {json.dumps(v, ensure_ascii=False)}')
    out.append('---'); return '\n'.join(out)
J = json.load(open('dl/Berakhot.json'))
L = [fm({'type': 'index', 'work': 'Talmud Bavli', 'translation': J['versionTitle'], 'license': J['license'], 'source': 'https://www.sefaria.org/texts/Talmud/Bavli', 'aliases': ['Talmud index', 'Babylonian Talmud', 'Talmud Bavli', 'Bavli']}),
 '# Talmud (William Davidson edition)', '',
 f'The Babylonian Talmud in English, in the William Davidson edition on Sefaria: {total:,} notes in {len(order)} tractates, one per daf, named as the [[Daf Yomi 2026-2029|Daf Yomi table]] names them (*Berakhot 2*). Each note has the two sides of the daf as headings (*2a*, *2b*) and each of Sefaria\'s lines as a block, so a link can point to a line: `[[Berakhot 2#^2a-1|Berakhot 2a:1]]`. Sefaria describes the version as "English from The William Davidson digital edition of the Koren Noé Talmud, with commentary by Rabbi Adin Even-Israel Steinsaltz": the words in bold translate the Talmud\'s text, and the rest is Rabbi Steinsaltz\'s explanation.',
 '', 'At the top of each side, collapsed boxes rebuild the margins of the printed page from Sefaria\'s links:',
 '- **Torah Or:** the verses quoted, linked to the vault\'s Torah and Tanakh notes, with the lines that quote them;',
 '- **Mesoret HaShas:** parallel passages, linked to their daf notes (the Mishnah, Tosefta and Midrash on Sefaria);',
 '- **Ein Mishpat:** where the codes rule on the passage: the [[Mishneh Torah]] here, Sefer Mitzvot Gadol, the Tur and the Shulchan Arukh on Sefaria;',
 '- **In this vault:** the Hasidic texts, Pirkei Avot, the Kitzur Shulchan Arukh and the Guide for the Perplexed notes that Sefaria links to the passage.',
 '', 'Verse references in the text are links, in the Hebrew numbering the edition prints. Not here: Shekalim (the Daf Yomi reads the Jerusalem Talmud\'s, which has no Davidson English), and Kinnim and Middot (Mishnah only); on those days Home\'s daf line keeps its Sefaria link. Sefaria has no complete English Rashi or Tosafot.',
 '', '## License and attribution', '',
 f'- **Translation:** {J["versionTitle"]}', f'- **License:** {J["license"]}', f'- **Version source:** {J["versionSource"]}', f'- **Print edition:** {J.get("purchaseInformationURL")}',
 '- **Digital text:** [Sefaria](https://www.sefaria.org/), via the [Sefaria-Export](https://github.com/Sefaria/Sefaria-Export) dataset (export of 2026-10-01); the margins from the same export\'s links.']
NOTES = {}
for s in SED:
    items = sorted(by[s], key=lambda x: pos.get(x[0], 99))
    L += ['', f'## {s}', ''] + [f'- [[{t}]] (dapim {a}–{b})' for t, a, b, n in items]
    NOTES[f'Texts/Talmud/{s}/{s}.md'] = '\n'.join([fm({'type': 'index', 'work': 'Talmud Bavli', 'seder': s.replace('Seder ', ''), 'aliases': [f'{s} (Talmud)']}), f'# {s}', '', f'[[Talmud]] · {s}', ''] + [f'- [[{t}]] (dapim {a}–{b}, {n} notes)' for t, a, b, n in items]) + '\n'
NOTES['Texts/Talmud/Talmud.md'] = '\n'.join(L) + '\n'
for k, v in NOTES.items():
    os.makedirs(os.path.dirname('out/' + k), exist_ok=True); open('out/' + k, 'w', encoding='utf-8').write(v)
print(len(order), total, len(NOTES))
