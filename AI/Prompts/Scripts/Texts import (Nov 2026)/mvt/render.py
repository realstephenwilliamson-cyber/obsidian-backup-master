"""Render the notes of one chapter of Texts/Malinivijayottara from the assembled data."""
import re,sys,json
sys.path.insert(0,'scripts')
from parse import md,norm,CO,CC,IO,IC,REF
ROOT='Texts/Malinivijayottara'
PDF={'f4':'Library/Trika/Malini (journal), January-April 2024.pdf','f5':'Library/Trika/Malini (journal), July-September 2022.pdf',
     'f1':'Library/Trika/Dyczkowski - Malinivijayottaratantra, chapters 1-5 (2022-2023).pdf',
     'f2':'Library/Trika/Dyczkowski - Malinivijayottaratantra, chapter 6 (2023).pdf',
     'f3':'Library/Trika/Dyczkowski - Malinivijayottaratantra, chapters 7-8 (2024-2025).pdf'}
def vname(ch,v): return f'Malinivijayottara {ch:02d}.{v:03d}'
def cname(ch): return f'Malinivijayottara {ch:02d}'
def issue_of(foots,pg):
    f=foots.get(pg,[])
    iss=[x for x in f if re.search(r'\d{4}',x)]; num=[x for x in f if re.fullmatch(r'\d+',x)]
    if len(iss)>1:      # a page that carries two issue lines: take the one its neighbours in the same file have
        import collections
        c=collections.Counter(y for p,g in foots.items() if p//1000==pg//1000 for y in g if re.search(r'\d{4}',y) and len([z for z in g if re.search(r'\d{4}',z)])==1)
        iss=sorted(iss,key=lambda y:c[y])
    return (iss[-1].replace(' - ',' – ') if iss else ''), (max(num,key=int) if num else '')
def unital(t):
    """a paragraph set wholly in italics is given upright"""
    plain=re.sub(CO+r'[\d:]+'+CC,'',t)
    it=sum(len(m) for m in re.findall(IO+'([^'+IC+']*)'+IC,plain)); tot=len(plain.replace(IO,'').replace(IC,''))
    return t.replace(IO,'').replace(IC,'') if tot and it/tot>0.6 else t
def reflabel(ch,r):
    v1,p1,v2,p2=r
    return f'{ch}.{v1}{p1}' + (f'–{v2}{p2}' if (v2!=v1 or p2) and not (v2==v1 and not p2) else '')
def pdflink(D,vp):
    n,_,_=D['segs'][vp//1000]; return f'<{PDF[n]}#page={vp%1000}>'
def fnkey(D,page,num):
    for pg in range(page,page+3):
        if (pg,num) in D['fn']: return (pg,num)
    for pg in range(page-1,page-3,-1):
        if (pg,num) in D['fn']: return (pg,num)
    return None
def resolve_calls(D,t,used):
    """[page:num] marks -> markdown calls; records the notes used"""
    def rep(m):
        pg,num=int(m.group(1)),m.group(2); k=fnkey(D,pg,num)
        if k is None: used.setdefault('missing',[]).append((pg,num)); return f' [n. {num}]'
        used.setdefault('keys',[])
        if k not in used['keys']: used['keys'].append(k)
        return CO+f'{k[0]}:{num}'+CC
    return re.sub(CO+r'(\d+):(\d+)'+CC,rep,t)
def render_chapter(D,meta,prev_ch=None,next_ch=None):
    ch=D['ch']; V=D['verses']; out={}; report=[]
    vs=sorted(V)
    # units -> verses
    cover={v:[] for v in vs}; last=None; chap_open=[]; chap_close=[]
    for u in D['units']:
        if u['ref'] is None:
            if last is None: chap_open.append(u); continue
            u['attach']=last['ref'][2]; u['label']=None
        else: last=u
    trailing=[]
    U=[u for u in D['units'] if u not in chap_open]
    # a last unit without a reference after the final verse is the chapter's closing words
    while U and U[-1]['ref'] is None and U[-1].get('attach')==vs[-1] and re.search(r'chapter',U[-1]['text'],re.I): chap_close.insert(0,U.pop())
    for u in U:
        if u['ref']:
            for v in range(u['ref'][0],u['ref'][2]+1):
                if v in cover: cover[v].append(u)
                else: report.append(f'unit ref {u["ref"]} names verse {v}, not in the chapter')
        else: cover[u['attach']].append(u)
    for i,v in enumerate(vs):
        d=V[v]; used={}
        prev=f'[[{vname(ch,vs[i-1])}|← {ch}.{vs[i-1]}]]' if i>0 else (f'[[{cname(prev_ch)}|← Chapter {prev_ch}]]' if prev_ch else f'[[Malinivijayottara|← Mālinīvijayottara]]')
        nxt=f'[[{vname(ch,vs[i+1])}|{ch}.{vs[i+1]} →]]' if i+1<len(vs) else (f'[[{cname(next_ch)}|Chapter {next_ch} →]]' if next_ch else f'[[Malinivijayottara|Mālinīvijayottara →]]')
        nav=f'{prev} · [[{cname(ch)}|Chapter {ch}]] · {nxt}'
        L=['---','type: "text"','work: "Mālinīvijayottaratantra"','translator: "Mark S. G. Dyczkowski"',f'chapter: {ch}',f'verse: {v}',
           f'edition: "{meta["edition"]}"','aliases:',f'  - "MVT {ch}.{v}"',f'  - "MV {ch}.{v}"',f'  - "Mālinīvijayottara {ch}.{v}"','---',nav,'','## Mūla','']
        noiast = not any(re.sub(CO+r'[\d:]+'+CC,'',x).strip() for x in d['iast'])
        if noiast or meta.get('mula_from_ksts'):
            from deva import to_deva
            d['dev']=[to_deva(x) for x in d['ks']]
        if d.get('dev'):
            n=len(d['dev'])
            L+=[x+(' ।' if j<n-1 else ' ॥ ^mula') for j,x in enumerate(d['dev'])]+['']
        ia=[resolve_calls(D,x.lower().replace('ƒ','ḥ'),used) for x in d['iast']]; n=len(ia)
        if noiast or meta.get('mula_from_ksts'):
            L+=[x+(' |' if j<n-1 else ' || ^iast') for j,x in enumerate(d['ks'])]+['','*'+(meta.get('mula_from_ksts') or meta['noiast'])+'*','']
        else:
            L+=[md(x)+(' |' if j<n-1 else ' || ^iast') for j,x in enumerate(ia)]+['']
            if any(s<0.999 for s in d['sim']):
                L+=['*Muktabodha\'s e-text of the KSTS edition (M00160) has:* '+' | '.join(d['ks'])+' ||','']
        for x in d['extra']:
            x=resolve_calls(D,x.lower().replace('ƒ','ḥ'),used)
            L+=['*After this verse Dyczkowski\'s text has lines that are not in the KSTS edition:*','']+[md(y.strip())+' |' for y in x.split('|') if re.sub(CO+r'[\d:]+'+CC,'',y).strip()]
            tailcall=''.join(re.findall(CO+r'[\d:]+'+CC, x.split('|')[-1])) if not re.sub(CO+r'[\d:]+'+CC,'',x.split('|')[-1]).strip() else ''
            if tailcall: L[-1]=L[-1]+md(tailcall)
            L+=['']
        L+=['## Translation','']
        if not cover[v]: report.append(f'{ch}.{v}: no translation unit'); L+=['*'+meta.get('notrans','No translation of this verse is printed in the source.')+'*','']
        for u in cover[v]:
            i2,p2=issue_of(D['foots'],u['page'])
            src=f'> [!source] Dyczkowski, *Mālinī*, {i2}' if i2 else '> [!source] Dyczkowski'
            L.append(src)
            L.append(f'> p. {p2} ([pdf]({pdflink(D,u["page"])}))' if p2 else f'> PDF page {u["page"]%1000} ([pdf]({pdflink(D,u["page"])}))')
            L.append('>')
            hs=[h for h in u['heads'] if h not in meta.get('title_lines',[])]
            for h in ([' '.join(hs)] if hs else []): L+=[f'> **{h}**','>']
            t=unital(u['text']); t=resolve_calls(D,t,used); t=md(t)
            if u['ref']:
                lab=reflabel(ch,u['ref'])
                whole = (u['ref'][0]==u['ref'][2]==v and not u['ref'][1] and not u['ref'][3])
                t=re.sub(r'\s*\*{0,2}\(\s*\d+\s*[a-f]{0,3}\s*(?:[-–—]\s*\d*\s*[a-f]{0,3}\s*)?\)\*{0,2}((?:\[\^[^\]]+\])*)[\s*]*$',r'\1',t)
                if u.get('inferred'): lab+= '; the print has '+('('+reflabel(ch,u['printed']).split('.',1)[1]+')' if u.get('printed') else 'no reference')
                if not whole or u.get('inferred'): t+=f' (with {lab})'
            for j,para in enumerate(t.split('\n\n')):
                if j: L.append('>')
                L.append('> '+para.strip())
            L.append('')
        # footnotes
        keys=used.get('keys',[])
        nums=[k[1] for k in keys]
        body='\n'.join(L)
        for k in keys:
            lab=k[1] if nums.count(k[1])==1 else f'{k[1]}-p{k[0]}'
            body=body.replace(md(CO+f'{k[0]}:{k[1]}'+CC) if False else CO+f'{k[0]}:{k[1]}'+CC, f'[^{lab}]')
        body=body.replace('\\[^','[^')
        defs=[]
        for k in keys:
            lab=k[1] if nums.count(k[1])==1 else f'{k[1]}-p{k[0]}'
            defs.append(f'[^{lab}]: '+md(re.sub(CO+r'[\d:]+'+CC,'',D['fn'][k])))
        if defs: body+='\n'+'\n'.join(defs)+'\n'
        if used.get('missing'): report.append(f'{ch}.{v}: footnote text not found for {used["missing"]}')
        out[f'{ROOT}/Adhikara {ch:02d}/{vname(ch,v)}.md']=body.rstrip('\n')+'\n'
    return out,report,dict(open=chap_open,close=chap_close,cover=cover)
