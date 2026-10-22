# Torzsok, PDF side: notes zone, notes (label/number), body words and call candidates per page.
import json,re,sys,os,unicodedata,statistics as st
HERE=os.path.dirname(os.path.abspath(__file__))
LAY=json.load(open(os.path.join(HERE,'layer.json'),encoding='utf-8'))
def norm(w):
    w=unicodedata.normalize('NFKD',w); w=''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]','',w)
JUNK='0123456789?!%°*^'
CALL=re.compile(r'^(.*?[^\W\d_][\'’”"\)\]\.,;:]*|.*?\])(['+re.escape(JUNK)+r']{1,3})([.,;:)\]]*)$')
def rows(i):
    R=[]
    for l in LAY[i]['lines']:
        if R and abs(l['y']-R[-1]['y'])<4: R[-1]['w']+=l['w']; R[-1]['y1']=max(R[-1]['y1'],l['y1'])
        else: R.append(dict(y=l['y'],y1=l['y1'],w=list(l['w'])))
    for r in R:
        r['w'].sort(key=lambda w:w['x']); r['sz']=st.median([w['sz'] for w in r['w']]); r['x']=r['w'][0]['x']
        r['t']=' '.join(w['t'] for w in r['w'])
    H=LAY[i]['H']
    # drop a bare page number at the top or bottom
    R=[r for r in R if not (re.fullmatch(r'[\dxivlcXIVLC]{1,6}',r['t']) and (r['y']<110 or r['y']>H-110))]
    return R
def num(s):
    s=re.sub(r'[^\dOolI]','',s or ''); s=s.replace('O','0').replace('o','0').replace('l','1').replace('I','1')
    return int(s) if re.fullmatch(r'\d{1,3}',s) else None
def page(i):
    R=rows(i)
    if len(R)<2: return None
    # notes zone: the longest tail of rows, after a gap >= 18, in which every row's pitch is < 12.8
    zone=len(R)
    pit=[R[k]['y']-R[k-1]['y'] for k in range(1,len(R))]   # pit[k-1] = pitch above row k
    for j in range(1,len(R)):
        if pit[j-1]<18: continue
        tail=pit[j:]
        if tail and max(tail)<14 and st.median(tail)<11.5: zone=j; break
    # single-row zone at the bottom: small type after a gap
    if zone==len(R) and R[-1]['y']-R[-2]['y']>=18 and R[-1]['sz']<7.9 and re.match(r'\d',R[-1]['t']): zone=len(R)-1
    Z=R[zone:]
    body=[]
    for j,r in enumerate(R[:zone]):
        for w in r['w']:
            for t in w['t'].split():
                body.append(dict(raw=t,n=norm(t),row=j))
    notes=[]
    if Z:
        maxx1=max(r['w'][-1]['x1'] for r in Z)
        info=[]
        for q,r in enumerate(Z):
            ws=[t for w in r['w'] for t in w['t'].split()]
            first=ws[0] if ws else ''
            lab=None
            if re.fullmatch(r'\d{1,3}',first) and len(ws)>1: lab=first; ws=ws[1:]
            info.append(dict(r=r,ws=ws,lab=lab))
        # indent against the local column (median x of the neighbouring rows: the scans are skewed)
        for q,it in enumerate(info):
            nb=[info[k]['r']['x'] for k in range(max(0,q-3),min(len(info),q+4)) if k!=q]
            col=st.median(nb) if nb else it['r']['x']
            prev_short = q>0 and info[q-1]['r']['w'][-1]['x1'] < maxx1-15
            it['score']=(it['r']['x']-col)+(3 if prev_short else 0) if len(' '.join(it['ws']))>=12 else -9
            it['start']=it['lab'] is not None
        # between two read labels a<b (b-a small), exactly b-a-1 unlabelled starts: take the best-scoring rows
        labs=[q for q,it in enumerate(info) if it['lab'] is not None]
        segs=[]
        for a,b in zip(labs,labs[1:]):
            na,nb_=num(info[a]['lab']),num(info[b]['lab'])
            if na is not None and nb_ is not None and 0<=nb_-na-1<=6: segs.append((a+1,b,nb_-na-1))
            else: segs.append((a+1,b,None))
        if labs: segs=[(0,labs[0],None)]+segs+[(labs[-1]+1,len(info),None)]
        else: segs=[(0,len(info),None)]
        for a,b,need in segs:
            rows_=sorted(range(a,b),key=lambda q:-info[q]['score'])
            if need is not None:
                for q in rows_[:need]:
                    if info[q]['score']>2: info[q]['start']=True
            else:
                for q in rows_:
                    if info[q]['score']>=5.5 or (info[q]['score']>=4 and q>0 and info[q-1]['r']['w'][-1]['x1']<maxx1-15): info[q]['start']=True
        for it in info:
            if it['start'] or not notes: notes.append(dict(label=it['lab'],start=it['start'],words=[],rows=0))
            notes[-1]['words']+=it['ws']; notes[-1]['rows']+=1
    for n in notes: n['n']=[norm(w) for w in n['words'] if norm(w)]
    cands=[]
    for k,b in enumerate(body):
        m=CALL.match(b['raw'])
        if m and norm(m.group(1)): cands.append(dict(tok=k,junk=m.group(2),raw=b['raw']))
        elif re.fullmatch(r'\d{1,3}[.,;:)]*',b['raw']) and k>0: cands.append(dict(tok=k,junk=re.match(r'\d+',b['raw']).group(0),raw=b['raw'],alone=True))
    return dict(body=body,notes=notes,cands=cands,zone=zone,nrows=len(R))
if __name__=='__main__':
    for K in [int(x) for x in sys.argv[1].split(',')]:
        p=page(K-1); print('== PDF',K,'zone row',p['zone'],'of',p['nrows'])
        for n in p['notes']: print('  note',repr(n['label']),n['start'],' '.join(n['words'][:8]))
        print('  cands',[(c['raw']) for c in p['cands']])
