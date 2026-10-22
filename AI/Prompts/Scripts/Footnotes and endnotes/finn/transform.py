import re, json, difflib, sys, collections
sys.path.insert(0,'/home/claude/finn')
from pdfside import page, norm
from mdpages import load
P=load()
LABEL_MD=re.compile(r'^([^\s]{1,5}?)\\?([.*])(\s+|$)')
JUNKCH=set('0123456789?°ŝćĆ*#»™^\\ʻ`~ºª¹²³⁰⁴⁵⁶⁷⁸⁹&$%@')
def toks(t):
    return [(m.start(),m.end(),m.group(0)) for m in re.finditer(r'\S+',t)]
def num(s):
    s=re.sub(r'[\\.*,^ ]','',s or '')
    s=s.replace('O','0').replace('o','0').replace('l','1').replace('I','1')
    return int(s) if re.fullmatch(r'\d{1,3}',s) else None
def is_numpara(t): return bool(re.fullmatch(r'(\s*[\dOolIS]{1,4}\\?\.)+\s*',t.strip()))
def lnums(t): return [num(x) for x in re.findall(r'([\dOolIS]{1,4})\\?\.',t)]
def dp_assign(clusters, notes):
    # monotonic assignment of ref clusters (in order) to note numbers (in order); score by digit agreement
    def sc(c,n):
        d=re.sub(r'\D','',c); s=str(n)
        if d==s: return 3
        def subseq(a,b):
            it=iter(b); return all(ch in it for ch in a)
        if d and (s.endswith(d) or s.startswith(d) or subseq(d,s) or (len(d)==len(s) and sum(a==b for a,b in zip(d,s))>=len(s)-1)): return 2
        if not d: return 1   # garbled cluster with no digits ('s', '™')
        return 0
    C=len(clusters); N=len(notes)
    best=[[0]*(N+1) for _ in range(C+1)]; ch=[[None]*(N+1) for _ in range(C+1)]
    for i in range(C-1,-1,-1):
        for j in range(N-1,-1,-1):
            opts=[(best[i+1][j],'skipc'),(best[i][j+1],'skipn')]
            s=sc(clusters[i]['raw'],notes[j])
            if s: opts.append((best[i+1][j+1]+s,'take'))
            best[i][j],ch[i][j]=max(opts)
        best[i][N]=0; ch[i][N]='skipc'
    i=j=0; out={}
    while i<C and j<N:
        c=ch[i][j]
        if c=='take': out[notes[j]]=clusters[i]; i+=1; j+=1
        elif c=='skipc': i+=1
        else: j+=1
    return out
def do_page(K, prev_last, used_labels, paras_override=None):
    p=page(K-1); md=P[K]
    if not p: return None, prev_last, {}
    lines=md['lines']
    paras=paras_override if paras_override is not None else [l for l in lines if l.strip()]
    if any('[^' in t for t in paras): return None, prev_last, dict(K=K,skip='page already has footnotes')
    # md tokens
    mt=[]
    for pi,t in enumerate(paras):
        for (a,b,w) in toks(t):
            n=norm(w)
            if n: mt.append((pi,a,b,w,n))
    # pdf tokens: body then notes
    pt=[('B',k,w['n'],w['raw']) for k,w in enumerate(p['body'])]
    for j,nn in enumerate(p['notes']):
        pt+= [('N',j,w,None) for w in nn['words']]
    sm=difflib.SequenceMatcher(None,[x[2] for x in pt],[x[4] for x in mt],autojunk=False)
    amap={}
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='equal' or (tag=='replace' and i2-i1==j2-j1):
            for d in range(i2-i1): amap[i1+d]=j1+d
        elif tag=='replace':
            jj=j1
            for ii in range(i1,i2):
                for k2 in range(jj,min(j2,jj+3)):
                    if difflib.SequenceMatcher(None,pt[ii][2],mt[k2][4]).ratio()>=0.75: amap[ii]=k2; jj=k2+1; break
    # classify md paragraphs
    votes=collections.defaultdict(collections.Counter)
    for i,j in amap.items():
        kind,idx,_,_=pt[i]; votes[mt[j][0]][('B',) if kind=='B' else ('N',idx)]+=1
    cls=[]
    for pi,t in enumerate(paras):
        if is_numpara(t): cls.append(('L',)); continue
        v=votes.get(pi)
        cls.append(v.most_common(1)[0][0] if v else ('?',))
    if paras_override is None:
        newp=[]; changed=False
        jt=collections.defaultdict(list)
        for i,j in amap.items():
            if pt[i][0]=='N': jt[mt[j][0]].append((j,pt[i][1]))
        for pi,t in enumerate(paras):
            seq=sorted(jt.get(pi,[]))
            cnt=collections.Counter(x[1] for x in seq)
            if len([k for k,v in cnt.items() if v>=2])<2: newp.append(t); continue
            cuts=[]; cur=None
            for (j,nj) in seq:
                if cnt[nj]<2: continue
                if cur is not None and nj!=cur and nj>cur: cuts.append(mt[j][1])
                cur=nj if cur is None or nj>cur else cur
            cuts=[c for c in cuts if c>0]
            if not cuts: newp.append(t); continue
            prev=0
            for c in cuts: newp.append(t[prev:c].strip()); prev=c
            newp.append(t[prev:].strip()); changed=True
        if changed: return do_page(K, prev_last, used_labels, [x for x in newp if x])
    info=dict(K=K)
    notes_pdf=[n for n in p['notes']]
    lab_idx=[j for j,n in enumerate(notes_pdf) if n['label'] is not None]
    if not lab_idx:
        return None, prev_last, info
    # note numbers: vote for base
    base_votes=collections.Counter()
    for r,j in enumerate(lab_idx):
        x=num(notes_pdf[j]['label'])
        if x is not None: base_votes[x-r]+=1
        # md prefix of the first paragraph of this note
        firstp=[pi for pi,c in enumerate(cls) if c==('N',j)]
        if firstp:
            m=LABEL_MD.match(paras[firstp[0]])
            if m:
                y=num(m.group(1))
                if y is not None: base_votes[y-r]+=1
    if prev_last is not None: base_votes[prev_last+1]+=1.5
    if not base_votes: return None, prev_last, dict(info,skip='no note numbers')
    base=base_votes.most_common(1)[0][0]
    numbers={}; prev=base-1
    for r,j in enumerate(lab_idx):
        cand=[num(notes_pdf[j]['label'])]
        firstp=[pi for pi,c in enumerate(cls) if c==('N',j)]
        if firstp:
            m=LABEL_MD.match(paras[firstp[0]]); cand.append(num(m.group(1)) if m else None)
        pick=None
        for x in cand:
            if x is not None and prev<x<=prev+3:
                # a jump must be confirmed: the skipped numbers must not appear as labels later on this page
                pick=x; break
        if pick is None: pick=prev+1
        numbers[j]=pick; prev=pick
    # sanity: every note's paragraphs must lie after all body paragraphs
    note_pis=[pi for pi,c in enumerate(cls) if c[0]=='N']
    body_pis=[pi for pi,c in enumerate(cls) if c==('B',)]
    if not note_pis: return None, base+len(lab_idx)-1, dict(info,skip='notes not found in md')
    first_note=min(note_pis)
    if body_pis and max(body_pis)>first_note: return None, base+len(lab_idx)-1, dict(info,skip='body after notes')
    # tail paragraphs with a label prefix matching an unfound note
    found={c[1] for c in cls if c[0]=='N'}
    lastbody=max(body_pis) if body_pis else -1
    numinv={v:k for k,v in numbers.items()}
    for pi in range(lastbody+1,len(paras)):
        if cls[pi]==('L',):
            if all(v in numinv for v in lnums(paras[pi])): cls[pi]=('LN',None)
            continue
        if cls[pi][0]=='?':
            m=LABEL_MD.match(paras[pi]); y=num(m.group(1)) if m else None
            if y in numinv and numinv[y] not in found:
                if cls[pi]==('L',): cls[pi]=('LN',numinv[y])
                else: cls[pi]=('N',numinv[y]); found.add(numinv[y])
            elif cls[pi]==('L',) and y in numinv: cls[pi]=('LN',numinv[y])
            elif cls[pi]==('?',) and pi>first_note:
                # unclassified paragraph inside the notes: belongs to the note before it
                prevn=[cls[q] for q in range(pi-1,first_note-1,-1) if cls[q][0]=='N']
                if prevn: cls[pi]=prevn[0]
    note_pis=[pi for pi,c in enumerate(cls) if c[0]=='N']
    first_note=min(note_pis)
    # notes must be in order and contiguous blocks
    seq=[cls[pi][1] for pi in range(first_note,len(paras)) if cls[pi][0]=='N']
    if seq!=sorted(seq): return None, base+len(lab_idx)-1, dict(info,skip='notes out of order')
    notepar={j:[pi for pi in range(len(paras)) if cls[pi]==('N',j)] for j in lab_idx}
    # refs
    refmap=dp_assign(p['refs'], [numbers[j] for j in lab_idx])
    refmap={n:c for n,c in refmap.items() if notepar[numinv[n]]}
    new_paras=list(paras); edits=[]; done_refs={}
    rev={}  # md token idx -> pdf token idx
    for i,j in amap.items(): rev[j]=i
    for n,c in refmap.items():
        a=c['after']
        if a<0 or a not in amap or c.get('trail'): continue
        j=amap[a]; pi,s,e,w,nw=mt[j]
        if pi>=first_note: continue
        praw=p['body'][a]['raw']; pn=norm(praw)
        cut=None
        for k in range(1,len(w)+1):
            if w[k-1].isalpha() and norm(w[:k])==pn: cut=k; break
        if cut is None: continue
        rest=w[cut:]
        ptl=re.sub(r'^.*[^\W\d_]','',praw)
        keep=''
        for ch_ in rest:
            if ch_ in '.,;:)]…' or (ch_ in ptl and ch_ not in '0123456789'): keep+=ch_
            else: break
        junk=rest[len(keep):]
        t=paras[pi]; endpos=e
        m3=re.match(r'\s+(\S+)',t[e:])
        nxtj = m3 and re.fullmatch(r'["“”’\']*[\d?°ŝćĆ*#»™^\\!|+%]+[.,;:)]*',m3.group(1)) and any(ch_.isdigit() or ch_ in '°' for ch_ in m3.group(1))
        tail=''
        mlet=re.match(r'([^\W\d_]+)(?=\d)',junk)
        if mlet:
            LM={'t':'1','l':'1','I':'1','i':'1','z':'2','Z':'2','s':'58','S':'58','o':'0','O':'0','b':'6','g':'9','q':'9'}
            sn=str(n); ok=len(mlet.group(1))<len(sn) and all(sn[k] in LM.get(ch_,'') for k,ch_ in enumerate(mlet.group(1)))
            if not ok: keep=keep+mlet.group(1); junk=junk[len(mlet.group(1)):]
        QU='"“”’\''
        quotes=''.join(ch_ for ch_ in junk if ch_ in QU)
        core=''.join(ch_ for ch_ in junk if ch_ not in QU)
        if core and not (any(ch_.isdigit() for ch_ in core) or set(core.rstrip('.,;:)'))<=JUNKCH|set('zZ!|')):
            if junk.isalpha():          # letters the PDF word lacks: keep them, put the reference after them
                keep=keep+junk; junk=''; quotes=''
            else: continue
        m2=re.search(r'[.,;:)\]]+$',core)
        tail=quotes+(m2.group(0) if m2 else '')
        how='glued' if junk else 'inserted'
        if nxtj:
            q_=re.match(r'["“”’\']*',m3.group(1)).group(0)
            endpos=e+m3.end(); how='separate'
            if q_ and not junk: keep=keep+q_      # closing quote printed before the raised number
            tail=(tail if junk else '')+re.search(r'[.,;:)]*$',m3.group(1)).group(0)
        edits.append((pi,s,endpos,w[:cut]+keep+'[^@'+str(n)+']'+tail,how))
        done_refs[n]=edits[-1][4]
    # apply edits per paragraph (right to left)
    byp=collections.defaultdict(list)
    for e_ in edits: byp[e_[0]].append(e_)
    for pi,es in byp.items():
        t=new_paras[pi]
        for (_,s,e,nw,_) in sorted(es,key=lambda x:-x[1]): t=t[:s]+nw+t[e:]
        new_paras[pi]=t
    # ---- verse labels on pages whose margin numbers were read as separate paragraphs
    floating=[pi for pi,c in enumerate(cls) if c==('L',) and pi<first_note]
    placed=set(); lab_ins=collections.defaultdict(list)
    if floating:
        fl_nums={v for pi in floating for v in lnums(paras[pi])}
        pl=[]
        for L in p['labels']:
            m_=re.match(r'^(\d{1,3})\s*&$',L['text'])
            if m_: pl.append(((int(m_.group(1)),int(m_.group(1))+1),L)); continue
            if pl and isinstance(pl[-1][0],tuple) and num(L['text'])==pl[-1][0][1]: continue
            pl.append((num(L['text']),L))
        for q,(v,L) in enumerate(pl):
            if isinstance(v,tuple):
                nx=pl[q+1][0] if q+1<len(pl) else None; pv=pl[q-1][0] if q>0 else None
                nx=nx[0] if isinstance(nx,tuple) else nx; pv=pv[1] if isinstance(pv,tuple) else pv
                ok = v[0] in fl_nums or v[1] in fl_nums or nx==v[1]+1 or pv==v[0]-1
            else:
                def _v(x): return x[1] if isinstance(x,tuple) else x
                ok = v is not None and (v in fl_nums or (q>0 and _v(pl[q-1][0])==v-1) or (q+1<len(pl) and (pl[q+1][0][0] if isinstance(pl[q+1][0],tuple) else pl[q+1][0])==v+1))
            if not ok or L['tok'] not in amap: continue
            jt=amap[L['tok']]; pi,s_,e_,w,_n=mt[jt]
            if pi>=first_note: continue
            if s_==0 and LABEL_MD.match(paras[pi]): continue
            lab_ins[pi].append((s_,v))
            for x in (v if isinstance(v,tuple) else (v,)): placed.add(x)
    # rebuild paragraphs: apply label splits to new_paras (positions in original para; edits only touched refs after these
    # positions within words, so recompute by locating the original word text)
    out=[]
    for pi in range(first_note):
        if cls[pi]==('L',):
            rest_=[v for v in lnums(paras[pi]) if not (v in placed or v in numbers.values())]
            if not rest_: continue
            if len(rest_)==len(lnums(paras[pi])): out.append(new_paras[pi])
            else: out.append(' '.join(f'{v}\\.' for v in rest_))
            continue
        t=new_paras[pi]
        if lab_ins.get(pi):
            # map original offsets to new text: edits only lengthen/shorten words; find each split word in new text in order
            cuts=sorted(lab_ins[pi]); pieces=[]; pos=0
            orig=paras[pi]
            for (s_,v) in cuts:
                # same prefix text in new paragraph: count words before s_
                nwords=len(re.findall(r'\S+',orig[:s_]))
                mm=list(re.finditer(r'\S+',t))
                cpos=mm[nwords].start() if nwords<len(mm) else len(t)
                pieces.append((cpos,v))
            prev=0; segs=[]
            for (cpos,v) in pieces:
                segs.append(t[prev:cpos].strip()); prev=cpos
            segs.append(t[prev:].strip())
            first=segs[0]
            if first: out.append(first)
            for (cpos,v),sg in zip(pieces,segs[1:]): out.append((f'{v[0]} & {v[1]}' if isinstance(v,tuple) else f'{v}')+'\\. '+sg)
        else: out.append(t)
    defs=[]; vis=[]
    for pi in range(first_note,len(paras)):
        c=cls[pi]
        if c[0]=='LN': continue
        if c[0]=='L':
            rest_=[v for v in lnums(paras[pi]) if not (v in placed or v in numbers.values())]
            if not rest_: continue
        if c[0]!='N' or c[1] not in lab_idx: vis.append(('x',paras[pi])); continue
    for j in lab_idx:
        ps=notepar[j]
        if not ps: continue
        n=numbers[j]
        txt=' '.join(paras[q] for q in ps)
        m=LABEL_MD.match(txt)
        if m and num(m.group(1)) is not None or (m and len(m.group(1))<=4 and re.search(r'\d',m.group(1))): txt=txt[m.end():]
        if n in done_refs: defs.append(f'[^@{n}]: '+txt.strip())
        else: vis.append(('n',f'{n}\\. '+txt.strip()))
    # order: body, unclassified tail paragraphs (continuations), visible notes, definitions
    tail=[t for k,t in vis if k=='x']+[t for k,t in vis if k=='n']
    return dict(paras=paras,new_paras=new_paras,cls=cls,numbers=numbers,lab_idx=lab_idx,refs=done_refs,first_note=first_note,p=p,
                out_body=out,out_tail=tail,out_defs=defs,placed=sorted(placed),floating=len(floating)), base+len(lab_idx)-1, info
if __name__=='__main__':
    last=None
    for K in [13,101,161,261,331]:
        r,last,info=do_page(K,None,set())
        print('== K',K,info)
        if r:
            print(' numbers',r['numbers'],'refs',r['refs'],'placed',r['placed'])
            for t in r['out_body']: print('   B|',t[:160])
            for t in r['out_tail']: print('   T|',t[:160])
            for t in r['out_defs']: print('   D|',t[:160])
