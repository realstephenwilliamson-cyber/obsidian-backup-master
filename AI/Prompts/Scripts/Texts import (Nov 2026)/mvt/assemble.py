"""Chapter data for the Malinivijayottara import: verses (print transliteration cut by the KSTS verse boundaries,
Devanagari checked against OCR of the print), translation units with their references, headings, footnotes."""
import json,re,sys,subprocess,os
sys.path.insert(0,'scripts')
from parse import *
from align import cut
from deva import to_deva,dnorm
import pymupdf
JUNK=re.compile(r'^(§|\d+|\d*L+\d*L*/?|_)$')
XO,XC='',''
def clean_s(lines):
    out=''
    for t in lines:
        t=t.replace(IO,'').replace(IC,'')
        t=re.sub(r'[/|_।॥]+',' § ',t)
        toks=[x for x in t.split() if not JUNK.match(x)]
        out2=[];run=[]          # letter-spaced words: a run of single letters is one word
        for x in toks+['§§']:
            if len(x)<=2 and x.isalpha() and x!='ca' and x!='sa' and x!='na' and x!='tu' and x!='vā' and x!='hi' and x!='yā' and x!='sā' and x!='te' and x!='me': run.append(x); continue
            if len(run)>=4: out2.append(''.join(run))
            else: out2+=run
            run=[]
            if x!='§§': out2.append(x)
        t=' '.join(out2)
        if not t: continue
        if re.search(r'\s?-$',out) and not out.endswith(XC+'-'): out=re.sub(r'\s?-$','',out)+t
        else: out=(out+' '+t) if out else t
    return re.sub(r'\s+',' ',out).strip()
def ocr_line(l,docs={}):
    n=l['n']
    if n not in docs: docs[n]=pymupdf.open(f'src/{n}.pdf')
    doc=docs[n]
    key=f"{n}-{l['rp']}-{l['x0']}-{l['y']}"
    os.makedirs('work/ocr',exist_ok=True); fn=f'work/ocr/{key}.txt'
    if os.path.exists(fn): return open(fn,encoding='utf-8').read()
    p=doc[l['rp']-1]; r=pymupdf.Rect(l['x0']-4,l['y']-3,l['x1']+4,l['y1']+3)
    png=f'/tmp/ocr_{os.getpid()}.png'; p.get_pixmap(dpi=400,clip=r).save(png)
    o=subprocess.run(['tesseract',png,'-','--tessdata-dir','/home/claude/tess','-l','san','--psm','7'],capture_output=True,text=True).stdout.strip()
    open(fn,'w',encoding='utf-8').write(o); return o
def dch(c): return '' if re.match(r'[\s।॥|0-9०-९‌‍.,/:;\'"‌-]',c) else c
def parse_ref(m):
    v1=int(m.group(1)); p1=m.group(2) or ''; v2=int(m.group(3)) if m.group(3) else v1; p2=m.group(4) or ''
    if m.group(3) is None or m.group(3)=='' : v2=v1; p2=''
    return v1,p1,v2,p2
def build(segs,ch,bold_is_head=False,do_ocr=True,starts=None,ends=None):
    items,notes,foots=parse_chapter(segs,ch,bold_is_head,starts,ends)
    # the chapter's text begins with the headings just before its first Devanagari line; what precedes is the introduction
    fk=next((i for i,it in enumerate(items) if it['kind']=='K'),0); j=fk
    def headish(it): return it['kind']=='H' or (it['kind']=='E' and all(x[0][0] in 'BO' for x in it['line']['segs'] if x[1].strip() and x[0]!='S') and len(plain(it['line']))<70)
    while j>0 and headish(items[j-1]): j-=1
    intro=items[:j]; items=items[j:]
    for it in intro:
        if it['kind'] in('S','K'): it['kind']='E'
    n=segs[0][0]
    mk=MK[str(ch)]
    refs=[]; refid=[]
    for v,h in mk['verses']:
        for i,x in enumerate(h): refs.append(x); refid.append((v,i))
    if mk['rest'].strip():
        last=mk['verses'][-1][0]
        for i,x in enumerate([y.strip() for y in mk['rest'].split('|') if y.strip()]): refs.append(x); refid.append((last+1,i))
    # --- transliteration stream; passages not in the KSTS text are lifted out and remembered by a marker
    S=[];extras=[];run=[];colophon=[]
    for it in items+[dict(kind='END',extra=False)]:
        if it['kind']=='S' and it['extra']:
            run.append(linetext(it['line'],italics=False)); continue
        if run:
            txt=clean_s([re.sub(r'[/|_।॥]+\s*\d*\s*[/|_L।॥]*',' ¦ ',x) for x in run]).replace('¦','|')
            if re.match(r'iti śrī',txt): colophon.append(txt)
            else: extras.append(txt); S.append(f'{XO}{len(extras)-1}{XC}')
            run=[]
        if it['kind']=='S': S.append(linetext(it['line'],italics=False))
    raw=clean_s(S)
    pieces,sims=cut(raw,refs,norm)
    for i in range(1,len(pieces)):          # a scrap cut off the end of the previous half goes back to it
        if sims[i]<0.25 and pieces[i] and len(norm(pieces[i]))<0.34*len(norm(refs[i])):
            pieces[i-1]=(pieces[i-1]+' '+pieces[i]).strip(); pieces[i]=''; sims[i]=0.0
            sims[i-1]=__import__('difflib').SequenceMatcher(None,norm(pieces[i-1]),norm(refs[i-1]),autojunk=False).ratio()
    verses={}
    firstpage={}
    for (v,i),p,s,r in zip(refid,pieces,sims,refs):
        d=verses.setdefault(v,dict(iast=[],sim=[],ks=[],extra=[]))
        for m in re.finditer(XO+r'(\d+)'+XC,p): d['extra'].append(extras[int(m.group(1))])
        p=re.sub(XO+r'\d+'+XC,' ',p); p=re.sub(r'\s+',' ',p).strip()
        d['iast'].append(p); d['sim'].append(round(s,3)); d['ks'].append(r)
    # --- Devanagari: OCR of the print's lines, cut the same way, used to confirm the reading
    K=[it for it in items if it['kind']=='K']
    if do_ocr and K:
        ocr=' '.join(re.sub(r'[|।॥]+',' ',ocr_line(it['line'])) for it in K)
        ocr=re.sub(r'[0-9०-९]+',' ',ocr); ocr=re.sub(r'\s+',' ',ocr)
        kd=[to_deva(r) for r in refs]
        opieces,osims=cut(ocr,kd,dch)
        for (v,i),o,ks in zip(refid,opieces,kd):
            d=verses[v]; gd=to_deva(re.sub(CO+r'[\d:]+'+CC,'',d['iast'][i]).replace('ƒ','ḥ'))
            d.setdefault('dev',[]);d.setdefault('devst',[]);d.setdefault('ocr',[])
            no,ng,nk=dnorm(o),dnorm(gd),dnorm(ks)
            import difflib as _d
            if ng==nk: d['dev'].append(gd); d['devst'].append('ok' if no==ng else 'same')       # transliteration and KSTS agree
            else:
                rg=_d.SequenceMatcher(None,no,ng,autojunk=False).ratio(); rk=_d.SequenceMatcher(None,no,nk,autojunk=False).ratio()
                if rk>rg: d['dev'].append(ks); d['devst'].append('ksts' if no==nk else 'ksts~')   # the print's Devanagari reads with the KSTS text
                else: d['dev'].append(gd); d['devst'].append('own' if no==ng else 'own~')         # ... with Dyczkowski's transliteration
            d['ocr'].append(o)
    else:
        for v,d in verses.items():
            d['dev']=[to_deva(re.sub(CO+r'[\d:]+'+CC,'',x).replace('ƒ','ḥ')) for x in d['iast']]; d['devst']=['none']*len(d['iast'])
    # --- page of each verse: where its transliteration (or Devanagari) starts
    # (found by looking for the first words of the verse in the S lines)
    spage={}
    Sl=[(it['page'],norm(plain(it['line']))) for it in items if it['kind']=='S' and not it['extra']]
    for v,d in verses.items():
        key=norm(d['iast'][0])[:12]
        for pg,t in Sl:
            if key and (key in t or t and key.startswith(t[:12]) and len(t)>=6):
                spage[v]=pg;break
    # --- translation units and headings
    units=[];heads=[];para=[];paras=[];ppage=None;allbold=True
    def flush_para():
        nonlocal para
        if para:
            t=para[0]
            for x in para[1:]: t=dehyph(t,x)
            paras.append(t); para=[]
    def flush_unit(force=False,why='ref'):
        nonlocal paras,heads,ppage,allbold
        flush_para()
        if not paras: allbold=True; return
        txt='\n\n'.join(paras)
        ms=list(REF.finditer(re.sub(CO+r'[\d:]+'+CC,'',txt.replace(IO,'').replace(IC,''))))
        ref=None
        if ms:
            tail=re.sub(CO+r'[\d:]+'+CC,'',txt.replace(IO,'').replace(IC,''))
            m=ms[-1]
            if len(tail)-m.end()<=12: ref=parse_ref(m)
        if ref is None and not force: return
        if ref is None and allbold and len(txt)<150:
            heads.append(md(txt.replace(IO,'').replace(IC,'').replace('\n\n',' '))); paras=[]; ppage=None; allbold=True; return
        units.append(dict(text=txt,ref=ref,page=ppage,heads=heads,why=why)); paras=[];heads=[];ppage=None;allbold=True
    pbold=None
    def lbold(it): return all(x[0][0] in 'BSO' or not x[1].strip() for x in it['line']['segs'])
    def endpara():
        """close the paragraph; a short all-bold one standing on its own is a heading"""
        nonlocal para,pbold,paras,heads,ppage,allbold
        if para and pbold:
            t=' '.join(x.strip() for x in para); tp=re.sub(CO+r'[\d:]+'+CC,'',t.replace(IO,'').replace(IC,''))
            prevok = (not paras) or bool(re.search(r'[.!?:”’")\]]\s*$',re.sub(CO+r'[\d:]+'+CC,'',paras[-1].replace(IO,'').replace(IC,''))))
            if len(tp)<90 and not REF.search(tp) and prevok and not re.search(r'[,;]\s*$',tp) and re.match(r'\s*[A-ZĀĪŪŚṢ0-9(“‘]',tp):
                para=[]
                if paras: flush_unit(force=True,why='H')
                heads.append(md(tp)); pbold=None; return
        flush_para(); pbold=None
    for ii,it in enumerate(items):
        k=it['kind']
        nx=items[ii+1] if ii+1<len(items) else None
        cont = nx is not None and nx['kind']=='E' and nx['indent']<=10 and it.get('rgap',99)<=8 and lbold(nx)==lbold(it)      # the next line runs on in the same paragraph
        if k=='E':
            lb=lbold(it)
            if para and it['indent']>10: endpara()
            if para and lb!=pbold: pbold=False
            if ppage is None and not paras and not para: ppage=it['page']
            if not para: pbold=lb
            para.append(linetext(it['line']))
            if not lb: allbold=False
            t=re.sub(CO+r'[\d:]+'+CC,'',para[-1].replace(IO,'').replace(IC,'')).rstrip()
            if REF.search(t) and len(t)-list(REF.finditer(t))[-1].end()<=3 and not cont:
                endpara(); flush_unit()
        elif k in('K','S'):
            endpara(); flush_unit(force=True,why='KS')
        elif k=='H':
            endpara(); flush_unit(force=True,why='H')
            heads.append(md(linetext(it['line'],italics=False)))
    endpara()
    flush_unit(force=True,why='end')
    # a paragraph cut from its continuation only by a heading is one unit with it
    i=0
    while i<len(units)-1:
        u,nx=units[i],units[i+1]
        if u['ref'] is None and u['why']=='H' and nx['heads'] and (i>0 or True) and any(x['ref'] for x in units[:i]):
            nx['text']=u['text']+'\n\n'+IO+IC+'**'+' '.join(nx['heads'])+'**\n\n'+nx['text']; nx['heads']=u['heads']; nx['page']=u['page']; units.pop(i); continue
        i+=1
    # footnotes: page -> list, continuation lines go to the previous page's last note
    pages=sorted(notes)
    fn={}
    lastkey=None
    for pg in pages:
        if notes[pg]['cont'] and lastkey: fn[lastkey]+=' '+notes[pg]['cont']
        for num,t in notes[pg]['items']:
            lastkey=(pg,num); fn[lastkey]=t
    units=[u for u in units if not (u['ref'] is None and re.match(r'\s*(\(?To be continued|\[?\.\.\. ?continued|[–-] *(Rajanaka )?Mark Dyczkowski)',re.sub('['+IO+IC+']','',u['text'])))]
    for i,u in enumerate(units[:-1]):      # a stray heading fragment before the next paragraph
        if u['ref'] is None and u['why']=='KS' and len(u['text'])<120 and i>0 and not re.search(r'[.!?]\s*$',u['text']):
            units[i+1]['heads']=[md(u['text'].replace('\n\n',' '))]+units[i+1]['heads']; u['drop']=True
    units=[u for u in units if not u.get('drop')]
    # a translation paragraph printed without its reference takes the verses left uncovered between its neighbours
    cov=set()
    for u in units:
        if u['ref']: cov.update(range(u['ref'][0],u['ref'][2]+1))
    for i,u in enumerate(units):
        if u['ref'] is not None: continue
        prev=[x['ref'][2] for x in units[:i] if x['ref']]; nxt=[x['ref'][0] for x in units[i+1:] if x['ref']]
        if not prev or not nxt: continue
        gap=[v for v in verses if prev[-1]<v<nxt[0] and v not in cov]
        if gap: u['ref']=(min(gap),'',max(gap),''); u['inferred']=True; cov.update(gap)
    # a verse left between two referenced paragraphs goes with the one that follows it
    R=[u for u in units if u['ref']]
    for a,b in zip(R,R[1:]):
        gap=[v for v in verses if a['ref'][2]<v<b['ref'][0] and v not in cov]
        if gap: b['printed']=b['ref']; b['ref']=(min(gap),'',b['ref'][2],b['ref'][3]); b['inferred']=True; cov.update(gap)
    return dict(intro=intro,notes=notes,n=n,segs=segs,ch=ch,items=items,verses=verses,units=units,fn=fn,foots=foots,colophon=colophon,tailheads=heads,spage=spage)
if __name__=='__main__':
    n,ch,p0,p1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
    D=build(n,ch,p0,p1,720 if n=='f1' else 648,bold_is_head=(n=='f3'))
    V=D['verses']
    import collections
    print('verses',len(V),'dev status',collections.Counter(s for d in V.values() for s in d['devst']))
    print('iast != ksts:',[v for v,d in V.items() if min(d['sim'])<0.999])
    print('extras:',{v:d['extra'] for v,d in V.items() if d['extra']})
    for v,d in V.items():
        for i,s in enumerate(d['devst']):
            if s not in('ok','same'): print(' DEV',v,i,s,'\n    ocr',d['ocr'][i],'\n    gen',d['dev'][i],'\n    kst',to_deva(d['ks'][i]))
    cov=collections.Counter()
    for u in D['units']:
        r=u['ref']; print('UNIT p',u['page'],r,u['heads'],'|',md(u['text'])[:70].replace('\n',' '),'…',md(u['text'])[-40:].replace('\n',' '))
        if r:
            for v in range(r[0],r[2]+1): cov[v]+=1
    print('uncovered verses',[v for v in V if v not in cov]); print('colophon',D['colophon'],'tail heads',D['tailheads'])
    print('footnotes',len(D['fn']))
