import sys,os,io,json,re,contextlib,collections
sys.path.insert(0,'scripts')
from assemble import *
from render import *
from prose import prose
TODAY='9 Nov 2026'
CH={1:[('f1',15,25)],2:[('f5',23,36),('f1',26,34)],3:[('f1',35,53)],4:[('f1',54,64)],5:[('f1',65,81)],6:[('f2',1,7),('f4',28,35)],8:[('f3',11,51)]}
ENDS={2:{0:'A Brief Life-Sketch|Moti Lal Pandit'}}
# corrections from the page readers (10 Nov 2026): word divisions the rebuild of letter-spaced lines or a line break got wrong
PATCH_IAST={(1,23):[('mal aikayuktas','malaikayuktas')],(2,21):[('prakal panaiḥ','prakalpanaiḥ')],(3,44):[('keval am','kevalam')],(3,57):[('karmagu ṇādibhiḥ','karmaguṇādibhiḥ')],(3,28):[('t e','te')],
  (5,20):[('ambar āpadāḥ','ambarāpadāḥ')],(5,21):[('chaga lāṇḍakau','chagalāṇḍakau')],(5,29):[('puraḥs arāḥ','puraḥsarāḥ'),('puraƒs arāḥ','puraḥsarāḥ')],(8,95):[('t u','tu'),('svārṇairevāṅgaṣaṭkam','svārṇairevāṅgaṣaṭkam\ue00041:103\ue001')],(8,122):[('śivāgniguruśiṣyāṇāṁ','śivāgniguruśiṣyāṇāṁ\ue00048:137\ue001')],(8,58):[('c a','ca')],(8,130):[('pata nādikam','patanādikam')],(8,37):[('guhyorūpāda gaṁ','guhyorūpādagaṁ')]}
# footnotes that ran together in the text layer: (chapter, number, next number, first words of the next)
FNSPLIT=[(8,'101','102','MV 8/93 quoted'),(8,'86','87','kh:'),(6,'6','7','The reading')]
KEEPCASE={(3,37),(8,28)}     # capitals that stand for long vowels
def patch(D,ch):
    for (c,v),reps in PATCH_IAST.items():
        if c==ch:
            for a,b in reps:
                hit=[i for i,x in enumerate(D['verses'][v]['iast']) if a in x]
                if len(hit)!=1: print('PATCH not applied',c,v,a,D['verses'][v]['iast']); continue
                D['verses'][v]['iast'][hit[0]]=D['verses'][v]['iast'][hit[0]].replace(a,b)
    for c,num,nx,start in FNSPLIT:
        if c!=ch: continue
        for k in list(D['fn']):
            if k[1]==num and start in D['fn'][k] and (k[0],nx) not in D['fn']:
                t=D['fn'][k]; i=t.index(start); head=re.sub(r'[\s'+IO+IC+r']*'+nx+r'['+IO+IC+r'.\s]*$','',t[:i])
                D['fn'][k]=head+(IC if head.count(IO)>head.count(IC) else ''); D['fn'][(k[0],nx)]=(IO if t[i:].count(IC)>t[i:].count(IO) else '')+t[i:]
    for k in list(D['fn']):
        if ch==6: D['fn'][k]=D['fn'][k].replace("' t h i s, t h e intermediate","'this, the intermediate"); D['fn'][k]=re.sub(r'\s*Deposition of the Forces on the Body\s*$',' [A table, Deposition of the Forces on the Body, follows in the print.]',D['fn'][k])
    U=D['units']
    for u in U:
        if ch==5: u['text']=u['text'].replace('Middle O ne','Middle One')
        if ch==8 and any('The Inner Sacrifice' in h for h in u['heads']): u['heads']=['The Inner Sacrifice','The Trika Trident']
    if ch==3:
        for u in U:
            if u['heads']==['(vidyāṅga)'] or u['heads']==['(*vidyāṅga*)']: u['heads']=['The Five Limbs of the Vidyās (vidyāṅga)']
    if ch==5:
        for i,u in enumerate(U):
            m=re.search(r'\s*(?:The )?Worlds in the Remaining Pure\s*Principles\s*$',u['text'].replace('\n',' '))
            if m and u['ref'] and u['ref'][0]==30:
                u['text']=re.sub(r'\s*(?:The )?Worlds in the Remaining Pure\s*Principles\s*$','',u['text']); u['ref']=(30,'',31,'ab'); u.pop('inferred',None); U[i+1]['heads']=['The Worlds in the Remaining Pure Principles']+U[i+1]['heads']
    if ch==4:   # footnote 7 is printed on the next page without a readable number and ran into footnote 6
        for k in list(D['fn']):
            if k[1]=='6' and 'MV 4/6cd. This important line' in D['fn'][k]:
                a,b=D['fn'][k].split('MV 4/6cd. This important line',1); D['fn'][k]=a.rstrip(); D['fn'][(k[0]+1,'7')]='MV 4/6cd. This important line'+b
TITLE={1:'The Descent of the Scripture, What is to be Rejected and How',2:'The Seven Perceivers, the Penetrations and the Six Paths',3:'Mantras and the Deities of the Alphabets',
       4:'Śaiva Yoga and the Distribution of the Tattvas',5:'The Path of the Worlds',6:'The Path of the Body',7:'Concerning the Gestures',8:'The Initiation into the Rule (samayadīkṣā)'}
ISSUES={1:'January–June 2022',2:'July–September and October–December 2022',3:'January–March 2023',4:'April–June 2023',5:'July–September 2023',6:'October–December 2023 and January–April 2024',7:'July–September 2024',8:'October–December 2024 and January–April 2025'}
EXTRA_END={5:'The print ends the chapter with two pages of tables of the worlds: [PDF pp. 82–83](<%s#page=82>).'%PDF['f1'],
           6:'The first part of the chapter is followed in the print by an appendix of charts and figures of the depositions on the body: [PDF pp. 8–16](<%s#page=8>).'%PDF['f2']}
def fm(ch,extra=()):
    return ['---','type: "text"','work: "Mālinīvijayottaratantra"','translator: "Mark S. G. Dyczkowski"',f'chapter: {ch}',*extra]
def fnmap(notes):
    fn={};last=None
    for pg in sorted(notes):
        if notes[pg]['cont'] and last: fn[last]+=' '+notes[pg]['cont']
        for num,t in notes[pg]['items']: last=(pg,num); fn[last]=t
    return fn
OUT={};REPORT=[];STATS={}
CH[7]=[('f3',1,10)]
chs=sorted(CH)
import ch7
for ch in chs:
    D=ch7.data() if ch==7 else build(CH[ch],ch,ends=ENDS.get(ch))
    patch(D,ch)
    meta=dict(keepcase={v for c,v in KEEPCASE if c==ch},edition=f"Mark Dyczkowski's text and translation, serialised in the journal Mālinī, {ISSUES[ch]}",
              title_lines=[],noiast="Dyczkowski's transliteration and translation stop at 8.133. The print gives only the Devanagari of this verse; the text here is that of the KSTS edition (Muktabodha M00160).",
              mula_from_ksts=('Dyczkowski prints no Sanskrit for this chapter; the text is that of the KSTS edition (Muktabodha M00160).' if ch==7 else None),
              notrans='No translation of this verse is printed: the serial stops at 8.133.' if ch==8 else 'No translation of this verse is printed in the source.')
    title_bits=set(re.split(r'\s*,\s*',TITLE[ch]))|{TITLE[ch],'Maaliniivijottara Tantra','Mālinīvijayottara',f'Chapter {["","One","Two","Three","Four","Five","Six","Seven","Eight"][ch]}',f'Chapter {["","One","Two","Three","Four","Five","Six","Seven","Eight"][ch]} of the'}
    for u in D['units']:
        hs=' '.join(u['heads']); 
        u['heads']=[h for h in u['heads'] if h.strip(' ,') not in title_bits and not any(h.strip(' ,')==b.strip(' ,') for b in title_bits)]
        # drop pieces of the chapter title printed at the head of the text
        u['heads']=[h for h in u['heads'] if not (u is D['units'][0] and (h.rstrip(',') in TITLE[ch] or TITLE[ch].startswith(h.rstrip(',')) or h in ('The Seven Perceivers, the','Penetrations and the Six Paths')))]
    prev=ch-1 if ch>1 else None; nxt=ch+1 if ch<8 else None
    out,rep,x=render_chapter(D,meta,prev,nxt)
    OUT.update(out); REPORT+=rep
    V=D['verses']; vs=sorted(V)
    # ---- chapter note
    L=fm(ch,['aliases:',f'  - "MVT {ch}"',f'  - "MV {ch}"',f'  - "Mālinīvijayottara {ch}"','---'])
    L.append((f'[[{cname(prev)}|← Chapter {prev}]]' if prev else '[[Malinivijayottara|← Mālinīvijayottara]]')+' · [[Malinivijayottara|Mālinīvijayottara]] · '+(f'[[{cname(nxt)}|Chapter {nxt} →]]' if nxt else '[[Malinivijayottara|Mālinīvijayottara →]]'))
    L+=['',f'# Mālinīvijayottara, chapter {ch}: {TITLE[ch]}','']
    files=' · '.join(f'[PDF pp. {a}–{b}](<{PDF[n]}#page={a}>)' for n,a,b in CH[ch])
    L+=[f'{len(vs)} verses, {vs[0]}–{vs[-1]}. '+('Translation' if ch==7 else 'Text and translation')+f' by Mark Dyczkowski, from *Mālinī*, {ISSUES[ch]}: {files}.','']
    if ch==7: L+=['The print is ten scanned pages with the English and a drawing of each gesture, and no Sanskrit. The English was read from the page images by Claude (9 Nov 2026) ; the drawings are in the PDF. A second reader compared it with the page images on 10 Nov 2026. The Sanskrit in the verse notes is the KSTS text.','']
    if ch==8: L+=['The serial stops at 8.133: the last page prints the Devanagari of 8.134–135 with no transliteration or translation.','']
    if D['intro']:
        iname=f'{cname(ch)} - Introduction (Dyczkowski)'
        L+=[f'Dyczkowski\'s introduction to the chapter: [[{iname}]].','']
        body=prose(D['intro'],D,skip_heads=())
        I=fm(ch,['aliases: []','---'])+[f'[[{cname(ch)}|← Chapter {ch}]] · [[Malinivijayottara|Mālinīvijayottara]]','',f'# Dyczkowski\'s introduction to chapter {ch} of the Mālinīvijayottara','',
           f'From *Mālinī*, {ISSUES[ch]}: [PDF](<{PDF[CH[ch][0][0]]}#page={CH[ch][0][1]}>). Converted from the PDF\'s text layer by Claude ({TODAY}); italics, headings and footnotes are kept, the page marks are the journal\'s page numbers. Check quotations against the PDF.','',body]
        OUT[f'{ROOT}/Adhikara {ch:02d}/{iname}.md']='\n'.join(I)
    for u in x['open']:
        t=md(unital(u['text'])) 
        if len(t)>40: L+=[re.sub(r'\[\^\d+\]','',t),'']
    L+=['## Verses','']
    firstunit={}
    for u in D['units']:
        if u['ref'] and u['heads'] and u['ref'][0] not in firstunit: firstunit[u['ref'][0]]=' '.join(u['heads'])
    for v in vs:
        if v in firstunit: L+=['',f'### {firstunit[v]}','']
        d=V[v]; first=re.sub(CO+r'[\d:]+'+CC,'',(d['iast'][0].strip() or d['ks'][0])).lower().replace('ƒ','ḥ')
        L.append(f'- [[{vname(ch,v)}|{ch}.{v}]] {first}')
    L+=['','## Closing','']
    for u in x['close']:
        ct=re.sub(r'\[\^\d+\]','',md(unital(u['text'])))
        m=re.search(r'\s*(?:—\s*|-\s*)?Dr\.? ?M(?:ark)?\b.*$',ct,re.S)
        if m: L+=[ct[:m.start()].rstrip(),'','*The journal adds:* '+ct[m.start():].strip(),'']
        else: L+=[ct,'']
    for c in D['colophon']: L+=['*'+c.replace('ƒ','ḥ').strip(' |')+'* ||','']
    if ch in EXTRA_END: L+=[EXTRA_END[ch],'']
    usedn=set()
    for p,t in list(out.items())+[(k,v) for k,v in OUT.items() if f'/Adhikara {ch:02d}/' in k]:
        usedn.update(re.findall(r'(?m)^\[\^(\d+)',t))
    orphan=[(k,t) for k,t in sorted(D['fn'].items()) if k[1] not in usedn and k[1].isdigit()]
    if orphan:
        L+=['## Footnotes printed without a call','','These notes stand at the foot of the page in the print, but no call for them is printed in the text.','']
        for (pg,num),t in orphan:
            iss,pp=issue_of(D['foots'],pg); L.append(f'- {num} (p. {pp}): '+md(re.sub(CO+r'[\d:]+'+CC,'',t)))
        L.append('')
    OUT[f'{ROOT}/Adhikara {ch:02d}/{cname(ch)}.md']='\n'.join(L).rstrip()+'\n'
    st=collections.Counter(s for d in V.values() for s in d.get('devst',[]))
    STATS[ch]=dict(verses=len(vs),differ=sum(1 for d in V.values() if any(x.strip() for x in d['iast']) and min(d['sim'])<0.999),extras=sum(1 for d in V.values() if d['extra']),units=len(D['units']),inferred=[(u['ref'],u.get('printed')) for u in D['units'] if u.get('inferred')],
                   attached=[(u.get('attach'),md(u['text'])[:40]) for u in D['units'] if u['ref'] is None and u.get('attach')],dev=dict(st),fn=len(D['fn']))
if __name__=='__main__':
    json.dump(OUT,open('work/out_main.json','w'),ensure_ascii=False)
    for c,s in STATS.items(): print(c,s)
    print('notes',len(OUT),'report',REPORT)
