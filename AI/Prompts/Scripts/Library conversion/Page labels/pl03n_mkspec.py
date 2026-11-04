# mkspec.py (3 Nov 2026, night): the page-label edits settled by the blind readings of pl-2026-11-03n. Writes spec.json (pf591 form).
import json, re
V='/mnt/user-data/uploads/Obsidian Vault/'
def rom(n):
    out=''
    for v,s in [(100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: out+=s; n-=v
    return out
TT='Library/Philosophy/Technics and Time (Stiegler)/'; RB='Library/Hinduism/The Ritual of Battle (Hiltebeitel)/'
HI='Library/Hinduism/Mudras - Yoga in Your Hands (Hirschi)/'; CY='Library/Christianity/Commentary on John, vol. 1 (Cyril of Alexandria)/'
CC='Library/Philosophy/Cyclonopedia - Complicity with Anonymous Materials (Negarestani)/'
tt5=TT+'Technics and Time 05 - Technics and Time, 2, part 1.md'; tt7=TT+'Technics and Time 07 - Technics and Time, 2, part 3.md'; ttI=TT+'Technics and Time (Stiegler).md'
rb1=RB+'The Ritual of Battle 01 - Part 1.md'; rbI=RB+'The Ritual of Battle (Hiltebeitel).md'
hi11=HI+'Mudras - Yoga in Your Hands 11 - The Mudras of Hatha Yoga and Mudra Exercises.md'; hiI=HI+'Mudras - Yoga in Your Hands (Hirschi).md'
cy2=CY+'Cyril on John I 02 - Contents.md'; cy18=CY+'Cyril on John I 18 - Book VI.md'; cyI=CY+'Commentary on John, vol. 1 (Cyril of Alexandria).md'
cc5=CC+'Cyclonopedia - Complicity 05 - Part 5.md'; ccI=CC+'Cyclonopedia - Complicity with Anonymous Materials (Negarestani).md'
E=[]
def mk(path,k,oldlab,newlab,why):
    o=f'*[{oldlab}]* ^pg{k}'; n=f'*[{newlab}]* ^pg{k}'; E.append(dict(id=f'm{len(E)+1:03d}',path=path,old=o,new=n,why=why))
def ln(path,o,n,why): E.append(dict(id=f'm{len(E)+1:03d}',path=path,old=o,new=n,why=why))
# Technics and Time
mk(tt5,13,'p. i','p. 1','prints 1 (two full-page readers)')
mk(tt5,23,'p. ii','p. 11','prints 11 in old-style figures (two zoom readers; full-page readers 11 / ii)')
ln(tt5,'page_range: 11–36','page_range: "1–36"','first printed page PDF 13 = 1, last PDF 48 = 36 (read)')
ln(ttI,'- [[Technics and Time 05 - Technics and Time, 2, part 1|Technics and Time, 2, part 1]] (pp. 11–36)','- [[Technics and Time 05 - Technics and Time, 2, part 1|Technics and Time, 2, part 1]] (pp. 1–36)','as page_range')
mk(tt7,123,'p. iii','p. 111','prints 111 (two full-page readers)')
# Ritual of Battle
ln(rb1,'page_range: 1–47','page_range: "5–47"','PDF 1 is the cover (no number); PDF 2 = 5 and PDF 40 = 47 (read)')
ln(rbI,'- [[The Ritual of Battle 01 - Part 1|Part 1]] (pp. 1–47)','- [[The Ritual of Battle 01 - Part 1|Part 1]] (pp. 5–47)','as page_range')
# Hirschi 11
for k,lab,why in [(183,'169','read'),(184,'170','read'),(185,'171','folio garbled in the PDF ("VJ\\"); fixed by 170 at PDF 184 and 172 at PDF 186'),(186,'172','read'),(187,'173','read'),
                  (195,'182','read'),(196,'183','read'),(197,'184','read'),(198,'185','read'),(199,'186','read'),(200,'187','no number; fixed by 186 at PDF 199 and 188 at PDF 201'),(201,'188','read')]:
    mk(hi11,k,f'PDF {k}',f'p. {lab}',why)
ln(hi11,'page_range: 166–202','page_range: "166–188"','first PDF 180 = 166 (no number; fixed by 165 at PDF 179 and 168 at PDF 182, PDF 181 garbled "l6j"), last numbered PDF 201 = 188; PDF 188, 189, 202 print no number and stay [PDF]')
ln(hiI,'- [[Mudras - Yoga in Your Hands 11 - The Mudras of Hatha Yoga and Mudra Exercises|The Mudras of Hatha Yoga and Mudra Exercises]] (pp. 166–202)','- [[Mudras - Yoga in Your Hands 11 - The Mudras of Hatha Yoga and Mudra Exercises|The Mudras of Hatha Yoga and Mudra Exercises]] (pp. 166–188)','as page_range')
# Cyril I 02: the preface xvii–lx (placeholders p. 21–64), PDF 65 prints no number
for k in range(21,65):
    mk(cy2,k,f'p. {k}',f'p. {rom(17+k-21)}','read' + (' (zoom readers and OCR lii; full-page readers liii)' if k==56 else ''))
mk(cy2,65,'p. 65','PDF 65','prints no number (Book I title page; lx before, 2 after)')
ln(cy2,'page_range: "2–5"','page_range: "xvii–lx; 2–5"','PDF 21 = xvii … PDF 64 = lx, PDF 65 none, PDF 66–69 = 2–5 (read)')
ln(cyI,'- [[Cyril on John I 02 - Contents|Contents]] (pp. 2–5)','- [[Cyril on John I 02 - Contents|Contents]] (pp. xvii–lx; 2–5)','as page_range')
# Cyril I 18: PDF 749–756 blank leaves, library slip, covers
for k in range(749,757): mk(cy18,k,f'p. {k}',f'PDF {k}','prints no number (blank leaf, date-due slip or cover)')
# Cyclonopedia 05
mk(cc5,170,'p. i','PDF 170','no page number: four readings none / unclear (a single stroke at the page edge); no page near it prints one')
ln(cc5,'page_range: 161–200','page_range: ""','no page of the note prints a number (as parts 2–4)')
ln(ccI,'- [[Cyclonopedia - Complicity 05 - Part 5|Part 5]] (pp. 161–200)','- [[Cyclonopedia - Complicity 05 - Part 5|Part 5]] (PDF 161–200)','as parts 2–4')
# check every old occurs once in the staged copy
bad=0
for e in E:
    t=open(V+e['path'],encoding='utf-8').read()
    lines=t.split('\n'); c=lines.count(e['old'])
    if c!=1 or t.count(e['old'])!=1: print('BAD',e['id'],c,t.count(e['old']),e['old'][:60]); bad+=1
json.dump([{k:e[k] for k in ('id','path','old','new')} for e in E],open('/home/claude/pl/out/spec.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(E,open('/home/claude/pl/out/decided.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
import collections; print(len(E),'edits; bad',bad); print(collections.Counter(e['path'].split('/')[-1][:40] for e in E))
