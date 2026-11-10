import sys,os,io,json,re,contextlib,collections
sys.path.insert(0,'scripts')
from assemble import *
from render import *
from prose import prose
TODAY='9 Nov 2026'
CH={1:[('f1',15,25)],2:[('f5',23,36),('f1',26,34)],3:[('f1',35,53)],4:[('f1',54,64)],5:[('f1',65,81)],6:[('f2',1,7),('f4',28,35)],8:[('f3',11,51)]}
ENDS={2:{0:'Moti Lal Pandit'}}
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
    meta=dict(edition=f"Mark Dyczkowski's text and translation, serialised in the journal Mālinī, {ISSUES[ch]}",
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
    if ch==7: L+=['The print is ten scanned pages with the English and a drawing of each gesture, and no Sanskrit. The English was read from the page images by Claude (9 Nov 2026) and is not yet checked by a second reader; the drawings are in the PDF. In verses 20–21 the print writes the sound with a mark on each S that could not be read at this resolution; it is given here as HSHS. The Sanskrit in the verse notes is the KSTS text.','']
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
        L+=[re.sub(r'\[\^\d+\]','',md(unital(u['text']))),'']
    for c in D['colophon']: L+=['*'+c.replace('ƒ','ḥ').strip(' |')+'* ||','']
    if ch in EXTRA_END: L+=[EXTRA_END[ch],'']
    OUT[f'{ROOT}/Adhikara {ch:02d}/{cname(ch)}.md']='\n'.join(L).rstrip()+'\n'
    st=collections.Counter(s for d in V.values() for s in d.get('devst',[]))
    STATS[ch]=dict(verses=len(vs),differ=sum(1 for d in V.values() if any(x.strip() for x in d['iast']) and min(d['sim'])<0.999),extras=sum(1 for d in V.values() if d['extra']),units=len(D['units']),inferred=[(u['ref'],u.get('printed')) for u in D['units'] if u.get('inferred')],
                   attached=[(u.get('attach'),md(u['text'])[:40]) for u in D['units'] if u['ref'] is None and u.get('attach')],dev=dict(st),fn=len(D['fn']))
if __name__=='__main__':
    json.dump(OUT,open('work/out_main.json','w'),ensure_ascii=False)
    for c,s in STATS.items(): print(c,s)
    print('notes',len(OUT),'report',REPORT)
