import sys,json,re,os,collections
sys.path.insert(0,'scripts')
import build_all as B
from build_all import *
from parse import parse_chapter
OUT=B.OUT; ST=B.STATS
# ---- general introduction (f1 pp. 1-14)
items,notes,foots=parse_chapter([('f1',1,14)],1)
for it in items:
    if it['kind'] in('S','K'): it['kind']='E'
D0=dict(fn=fnmap(notes),foots=foots,segs=[('f1',1,14)])
body=prose(items,D0)
G=['---','type: "text"','work: "Mālinīvijayottaratantra"','translator: "Mark S. G. Dyczkowski"','aliases: []','---','[[Malinivijayottara|← Mālinīvijayottara]] · [[Malinivijayottara 01|Chapter 1 →]]','',
   "# Dyczkowski's general introduction to the Mālinīvijayottara",'',
   f"From *Mālinī*, January–June 2022, pp. 25–38: [PDF](<{PDF['f1']}#page=1>). Converted from the PDF's text layer by Claude ({TODAY}); italics, headings and footnotes are kept, the page marks are the journal's page numbers. Check quotations against the PDF.",'',body]
OUT[f'{ROOT}/Malinivijayottara - General introduction (Dyczkowski).md']='\n'.join(G)
# ---- index
tot=sum(s['verses'] for s in ST.values()); dif=sum(s['differ'] for s in ST.values())
I=['---','type: "index"','work: "Mālinīvijayottaratantra"','translator: "Mark S. G. Dyczkowski"','edition: "Mark Dyczkowski\'s text and translation of chapters 1–8, serialised in the journal Mālinī, 2022–2025; KSTS text from Muktabodha M00160"',
   'aliases:','  - "Mālinīvijayottara"','  - "Mālinīvijayottaratantra"','  - "Malinivijayottaratantra"','  - "MVT"','  - "Mālinīvijayottara (Dyczkowski)"','---',
   '# Mālinīvijayottaratantra, chapters 1–8 (Dyczkowski)','',
   f"Mark Dyczkowski's Sanskrit text and English translation of the first eight of the Tantra's 23 chapters, as serialised in the journal *Mālinī* from January 2022 to April 2025. One note per verse ({tot} verses), each with the Devanagari (`^mula`), the transliteration (`^iast`), the translation and his footnotes. Cite a verse as `[[Malinivijayottara 01.001]]`, or by its alias `MVT 1.1`.",'',
   '- [[Malinivijayottara - General introduction (Dyczkowski)|General introduction]] (January–June 2022)','']
I+=['| Chapter | Title | Verses | Issue | Introduction |','|---|---|---|---|---|']
for ch in sorted(ST):
    intro=f'[[{cname(ch)} - Introduction (Dyczkowski)\\|introduction]]' if f'{ROOT}/Adhikara {ch:02d}/{cname(ch)} - Introduction (Dyczkowski).md' in OUT else ''
    I.append(f'| [[{cname(ch)}\\|{ch}]] | {TITLE[ch]} | {ST[ch]["verses"]} | {ISSUES[ch]} | {intro} |')
I+=['','## How the notes were made','',
 f'Made by Claude on {TODAY} from the PDFs in `Library/Trika` (catalog note: [[Dyczkowski (tr.) - Malinivijayottaratantra, chapters 1-8 (Malini 2022-2025)]]). The scripts are in `AI/Prompts/Scripts/Texts import (Nov 2026)/mvt/`.','',
 '- **Verse numbers** are those of the KSTS edition. The print\'s own danda marks and numbers are irregular, so the transliteration was cut into verses by lining it up with the KSTS text (Muktabodha e-text M00160, which is in the vault). His translation paragraphs carry their own references, and a paragraph that covers several verses is repeated in each, ending "(with 1.2–4ab)".',
 '- **Transliteration** is as printed, in lower case, with his word division. The print sometimes has ƒ where ḥ is meant; that is given as ḥ. Other slips of the print are left as they are.',
 f'- **Where the transliteration differs** in its letters from the Muktabodha e-text, the e-text\'s reading follows under it ({dif} verses). These are his emendations and variant choices, slips of the print, and also slips of the e-text; the line does not say which.',
 '- **Devanagari.** The PDFs\' Devanagari is in a legacy font that does not decode and in places does not display correctly. The Devanagari here is written out from the transliteration (or, where the two disagree, from whichever of the transliteration and the KSTS text is closer to an OCR reading of the printed Devanagari). It is a help for reading, not a second witness.',
 '- **Lines not in the KSTS edition** that he adds from manuscripts are given after the verse they follow (1.32).',
 '- **Footnotes** keep their printed numbers. `[n. 37]` marks a call whose note could not be found in the PDF\'s text layer.',
 '- **References supplied.** Where the print gives a paragraph no verse reference, or leaves a verse between two references, the note says so ("the print has …").',
 '- **Chapter 7** is printed as scanned pages with the English and drawings only; its English was read from the page images, and its Sanskrit is the KSTS text.',
 '- **Chapter 8** stops at 8.133; 8.134–135 have the KSTS text and no translation.',
 '- The chapter introductions and the general introduction are converted prose with the journal\'s page numbers; lists and tables in them are rough, and the tables at the end of chapter 5 and the appendix of charts to chapter 6 are linked, not converted.','',
 '## Not checked','',
 'No second reader has compared the notes with the page images. Places to look at first are listed in the AI log entry of this import.','']
OUT[f'{ROOT}/Malinivijayottara.md']='\n'.join(I)
# ---- catalog note
C=['---','title: "Mālinīvijayottaratantra, chapters 1–8: text and translation"','subtitle: "serialised in Mālinī, 2022–2025"','author: []','editor: []','translator:','  - "Mark S. G. Dyczkowski"','year: 2022','publisher: "Ishwar Ashram Trust"','series: ""','volume: ""','container: "Mālinī"','subject:','  - "Trika"','type: text','language:','  - "English"','  - "Sanskrit"','pages: 150','text: searchable','print: false','files:',
   *[f'  - "[[{PDF[k]}]]"' for k in ('f1','f2','f3','f5','f4')],'  - "[[Texts/Malinivijayottara/Malinivijayottara]]"','aliases: []','---',
   '# Mālinīvijayottaratantra, chapters 1–8: text and translation','','```dataviewjs','await dv.view("Templates/Views/open-pdf")','```','',
   'Mark Dyczkowski\'s text and translation of the first eight chapters, with introductions, as printed in the journal *Mālinī* between January 2022 and April 2025. Three files are the article pages alone (chapters 1–5, 83 pp.; chapter 6, 16 pp.; chapters 7–8, 51 pp.). They lack two parts, which are in the two whole issues kept with them: the introduction and verses 1–24 of chapter 2 (July–September 2022, PDF pp. 23–36) and the second half of chapter 6 (January–April 2024, PDF pp. 28–35). Chapter 7 is scanned pages; the rest have a text layer in legacy fonts.','',
   'Kept as notes: [[Texts/Malinivijayottara/Malinivijayottara|Malinivijayottara]] in `Texts/Malinivijayottara`, one note per verse.','',
   f'Catalogued by Claude on {TODAY} from the files themselves (headings and page footers). The publisher is taken from the issues\' own pages. The subject was assigned by Claude; change it if the item belongs elsewhere.','']
OUT['Catalog/Trika/Dyczkowski (tr.) - Malinivijayottaratantra, chapters 1-8 (Malini 2022-2025).md']='\n'.join(C)
# ---- checks on the output, bundles
bad=[p for p,t in OUT.items() if re.search('[\ue000-\ue005\ufffd]',t)]
tet=[p for p,t in OUT.items() if re.search(r'\bYHWH\b|\bYahweh\b|\bJehovah\b|יהוה',t)]
links=set(); names={p.split('/')[-1][:-3] for p in OUT}
miss=collections.Counter()
for p,t in OUT.items():
    for m in re.finditer(r'\[\[([^\]|#\\]+)',t):
        n=m.group(1).split('/')[-1]
        if n not in names and not m.group(1).startswith('Library/'): miss[m.group(1)]+=1
print('notes',len(OUT),'bytes',sum(len(t.encode()) for t in OUT.values()),'| internal marks left:',len(bad),bad[:5],'| divine name:',tet,'| links not to bundle notes:',dict(miss))
long=[p for p in OUT if len('C:/Vaults/Obsidian Vault/'+p)>200]; print('long paths',long)
os.makedirs('/mnt/user-data/outputs/mvt',exist_ok=True)
keys=sorted(OUT); half=len(keys)//2
for i,ks in enumerate((keys[:half],keys[half:]),1):
    json.dump({k:OUT[k] for k in ks},open(f'/mnt/user-data/outputs/mvt/mvt-bundle-{i}c.json','w'),ensure_ascii=False)
    print('bundle',i,len(ks),os.path.getsize(f'/mnt/user-data/outputs/mvt/mvt-bundle-{i}c.json'))
json.dump(B.REPORT,open('work/report.json','w'),ensure_ascii=False); json.dump(ST,open('work/stats.json','w'),ensure_ascii=False,default=str)
