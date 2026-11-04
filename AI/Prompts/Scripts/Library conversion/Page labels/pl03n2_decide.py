# pl03n2_decide.py (3 Nov 2026, night, second round): marker, page_range and index-label edits from two blind readings (and a follow-up round of zoomed strips) under Stephen's rule. Inputs: the pf757 survey (every marker of the books), the image keys, the readings; writes the pf591 spec, the decisions and the list of what is left. Paths are those of the cloud session.
# decide2.py (3 Nov 2026, night, second round): from the image key, two blind readings and the vault's current markers (pf757 survey),
# the marker, page_range and index-label edits that Stephen's rule allows. Writes spec3.json (pf591 form), decided3.json and left3.json.
import json, re, glob, os, collections
PL='/home/claude/pl/'
S=json.load(open(PL+'survey2.json')); plan=json.load(open(PL+'plan2.json')); B=plan['books']
key=json.load(open(PL+'key2.json'))
R={1:{},2:{}}
for f in glob.glob(PL+'r2/b*-r*.json'):
    r=int(f[-6])
    for e in json.load(open(f)): R[r][e['img'].replace('.png','')]=e
ROM={'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
def rom2int(s):
    s=s.lower()
    if not s or any(c not in ROM for c in s): return None
    t=0
    for i,c in enumerate(s): v=ROM[c]; t+= -v if i+1<len(s) and ROM[s[i+1]]>v else v
    return t if int2rom(t)==s else None
def int2rom(n):
    o=''
    for v,s in [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: o+=s; n-=v
    return o
def norm(p):
    p=str(p).strip().translate(str.maketrans('०१२३४५६७८९','0123456789'))
    if p.lower() in ('none','unclear','?',''): return p.lower() or '?'
    p=re.sub(r'(?i)^page\s+','',p).strip(' .-–—()[]')
    p=re.sub(r'\s*[-–—]\s*','–',p)
    if re.fullmatch(r'\d+(–\d+)?',p): return p
    if rom2int(p): return p.lower()
    return 'odd:'+p
def val(lab):
    if lab is None or lab=='-': return None
    if re.fullmatch(r'\d+',lab): return ('a',int(lab))
    m=re.fullmatch(r'(\d+)–(\d+)',lab)
    if m: return ('s',int(m.group(1)),int(m.group(2)))
    r=rom2int(lab)
    if r: return ('r',r)
    return None
# current markers per book: K -> (note, label or '-')
cur={}; notes={}
for b,d in B.items():
    folder=[k for k in S if k.endswith('/'+d)][0]; cur[b]={}; notes[b]={}
    for f,v in S[folder].items():
        if not v['ms']: notes[b]['__index__']=(folder+'/'+f,v); continue
        notes[b][f]=(folder+'/'+f,v)
        for t in v['ms'].split():
            k,l=t.split(':',1); cur[b][int(k)]=(f,l)
reads={b:{} for b in B}
for img,(b,k,bt) in key.items():
    i=img.replace('.png',''); a=norm(R[1].get(i,{}).get('printed','?')); c=norm(R[2].get(i,{}).get('printed','?'))
    reads[b][k]=(a,c)
# earlier round (3 Nov night, first): pages-read
for row in json.load(open('/mnt/user-data/outputs/pl/data/pages-read.json')):
    b,k=row[0],row[1]; bb={'cyr':'cy1','cyc':'cyc','hir':'hir'}.get(b)
    if bb and k not in reads[bb]: reads[bb][k]=(norm(row[5]),norm(row[6]))
reads['cy1'][56]=('lii','lii')
kz=json.load(open(PL+'keyZ2.json')); Z1={e['img']:e for e in json.load(open(PL+'r2/z2-r1.json'))}; Z2={e['img']:e for e in json.load(open(PL+'r2/z2-r2.json'))}
for img,(b,k,m) in kz.items():
    i=img[:-4]; a=norm(Z1[i]['printed']); c=norm(Z2[i]['printed'])
    old=reads[b].get(k)
    if b=='kin' and a=='none': a=c='unclear'  # the 18 % top strip cut Kinsley's running head
    if a==c and a not in ('?','unclear') and not a.startswith('odd'): reads[b][k]=(a,c)
    elif old is None: reads[b][k]=(a,c)
    else: reads[b][k]=('unclear','unclear') if old[0]!=old[1] or old[0] in ('unclear','?') else old
for k,v in ((62,'52'),(110,'100'),(177,'167')): reads['pb'][k]=(v,v)  # reader 2 saw the head (PDF page) and the foot; the foot is the numbering the markers use
SKIP={'gan'}; HOLD={('kin',62)}; ONLY={'idel':{1,2,3}}
E=[]; D=[]; L=[]
def lab_line(k,l): return f'*[PDF {k}]* ^pg{k}' if l=='-' else f'*[p. {l}]* ^pg{k}'
for b in B:
    if b not in cur or b in SKIP: continue
    C=cur[b]; RD=reads[b]; new={}; fixed=set()
    agreed={k:a for k,(a,c) in RD.items() if a==c and not a.startswith('odd') and a not in ('?','unclear')}
    for k,(a,c) in RD.items():
        if k not in agreed: L.append(dict(book=b,K=k,cur=C.get(k,('',''))[1],r1=a,r2=c,why='readers differ or unclear'))
    for k,a in agreed.items():
        if a!='none': new[k]=a; fixed.add(k)
    # printed reference labels: agreed numbers, else current non-placeholder markers
    def ref(k):
        if k in agreed: return agreed[k] if agreed[k]!='none' else None
        if k in RD: return None
        l=C.get(k,(None,None))[1]
        if l in (None,'-') or l==str(k): return None
        return l
    Ks=sorted(C)
    for k,a in agreed.items():
        if a!='none' or k not in C: continue
        before=next((j for j in sorted(C,reverse=True) if j<k and ref(j)),None); after=next((j for j in Ks if j>k and ref(j)),None)
        fill='-'
        if before and after:
            vb,va=val(ref(before)),val(ref(after))
            if vb and va and vb[0]==va[0] and vb[0] in 'ar' and va[1]-vb[1]==after-before:
                n=vb[1]+(k-before); fill=str(n) if vb[0]=='a' else int2rom(n)
                if before in agreed and after in agreed: fixed.add(k)
                elif C.get(k,('', ''))[1]==fill: fixed.add(k)
        new[k]=fill
        if fill=='-': fixed.add(k)
    # marker edits
    final={k:C[k][1] for k in C}
    for k,l in new.items():
        if k not in C: continue
        if b in ONLY and k not in ONLY[b]: continue
        if (b,k) in HOLD: L.append(dict(book=b,K=k,cur=C[k][1],why='held: readers read '+l+', the run gives '+C[k][1])); continue
        if '–' in C[k][1] and '–' not in l: continue
        if l!=C[k][1]:
            f=C[k][0]; E.append(dict(path=notes[b][f][0],old=lab_line(k,C[k][1]),new=lab_line(k,l),book=b,K=k,why=f'read {RD[k][0]}/{RD[k][1]}' if k in RD else 'run'))
            final[k]=l
    # ranges
    for f,(path,v) in notes[b].items():
        if f=='__index__': continue
        ks=[int(t.split(':')[0]) for t in v['ms'].split()]
        touched=any(e['path']==path for e in E) or any(k in RD for k in ks)
        if not touched: continue
        pr=[(k,final[k]) for k in ks if final[k]!='-']
        if not pr:
            ends_ok=(ks[0] in agreed and agreed[ks[0]]=='none') and (ks[-1] in agreed and agreed[ks[-1]]=='none')
            newr=''; ok=ends_ok
        else:
            runs=[]; 
            for k,l in pr:
                v2=val(l)
                if runs and v2 and val(runs[-1][-1][1]) and v2[0]==val(runs[-1][-1][1])[0] and v2[1]>val(runs[-1][-1][1])[-1]: runs[-1].append((k,l))
                else: runs.append([(k,l)])
            def endlab(l,first):
                m=re.fullmatch(r'(\d+)–(\d+)',l); return (m.group(1) if first else m.group(2)) if m else l
            newr='; '.join(endlab(r[0][1],True) if len(r)==1 and '–' not in r[0][1] else f'{endlab(r[0][1],True)}–{endlab(r[-1][1],False)}' for r in runs)
            ok=(pr[0][0] in fixed) and (pr[-1][0] in fixed) and all(r[0][0] in fixed and q[-1][0] in fixed for q,r in zip(runs,runs[1:]))
            if b=='ab' and f.startswith('Abhinavabharati - 05'): newr='123–173'
        old=v['pr']; oldv=old.strip('"')
        if not ok:
            if newr!=oldv: L.append(dict(book=b,note=f,why=f'range {old} would be "{newr}" but an end is not fixed (first PDF {pr[0][0] if pr else ks[0]}, last PDF {pr[-1][0] if pr else ks[-1]})'))
            continue
        if newr!=oldv: E.append(dict(path=path,old='page_range: '+old,new=f'page_range: "{newr}"',book=b,why='range from the markers'))
        ip,iv=notes[b]['__index__']; stem=f[:-3]
        lines=[l for l in (iv['idx'] or []) if ('[['+stem+'|') in l or ('[['+stem+']]') in l]
        if len(lines)!=1: L.append(dict(book=b,note=f,why=f'index line not found ({len(lines)})')); continue
        l0=lines[0]; m=re.search(r'\((pp?\.|PDF) [^()]*\)\s*$',l0)
        if not m: L.append(dict(book=b,note=f,why='index label has no page part')); continue
        pp=v['pp'].strip('"')
        lab=f'(PDF {pp})' if newr=='' else (f'(pp. {newr})' if ('–' in newr or ';' in newr) else f'(p. {newr})')
        have=re.sub(r'^\((pp?\.) ','',l0[m.start():].strip()).rstrip(')'); want=re.sub(r'^\((pp?\.) ','',lab).rstrip(')')
        if have.replace('(','')!=want.replace('(',''): E.append(dict(path=ip,old=l0,new=l0[:m.start()]+lab,book=b,why='index label as page_range'))
# check uniqueness of olds per file
cnt=collections.Counter((e['path'],e['old']) for e in E)
dup=[k for k,c in cnt.items() if c>1]
for i,e in enumerate(E): e['id']=f'r{i+1:03d}'
json.dump([{k:e[k] for k in ('id','path','old','new')} for e in E],open(PL+'spec3.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(E,open(PL+'decided3.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(L,open(PL+'left3.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('edits',len(E),'dups',len(dup),'left',len(L))
print(collections.Counter(e['book'] for e in E))
