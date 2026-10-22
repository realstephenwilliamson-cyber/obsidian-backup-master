import json,re,unicodedata
LAY=json.load(open('/home/claude/finn/layer.json'))
def norm(w):
    w=unicodedata.normalize('NFKD',w); w=''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]','',w)
def page(i):
    """i = 0-based pdf page index. Returns dict with body words, notes, labels."""
    lines=[l for l in LAY[i] if l['y']>35]          # drop running head (page number)
    if not lines: return None
    # merge lines at the same y into one row
    rows=[]
    for l in sorted(lines,key=lambda l:(l['y'],l['x'])):
        if rows and abs(l['y']-rows[-1]['y'])<3.5: rows[-1]['spans']+=l['spans']
        else: rows.append(dict(y=l['y'],spans=list(l['spans'])))
    for r in rows: r['spans'].sort(key=lambda s:s['x'])
    xs=sorted(s['x'] for r in rows for s in r['spans'] if s['sz']>=7 and len(s['t'].strip())>8)
    left=xs[len(xs)//10] if xs else 30
    def is_label(s):
        t=s['t'].strip()
        return s['sz']>=7 and len(t)<=5 and re.search(r'\d',t) and (re.match(r'^\d{1,3}$',t) or re.match(r'^[\w?]{1,4}[.*,^]$',t))
    def gap_ok(sp): 
        big=[x for x in sp[1:] if x['sz']>=7]
        return bool(big) and big[0]['x']-sp[0]['x1']>8
    # note zone: first row (from top) that starts with an oblique label, with oblique text, after which rows are mostly oblique
    def obl(r): 
        tot=sum(len(s['t']) for s in r['spans']); o=sum(len(s['t']) for s in r['spans'] if s['f']=='O'); return tot and o/tot>0.6
    def oc(r): return sum(len(s['t']) for s in r['spans'] if s['f']=='O' and s['sz']>=7)
    def rc(r): return sum(len(s['t']) for s in r['spans'] if s['f']=='R' and s['sz']>=7 and not (s is r['spans'][0] and is_label(s)))
    O=[oc(r) for r in rows]; R=[rc(r) for r in rows]
    best=(0,len(rows))   # score of "no notes" = 0
    for j in range(len(rows)):
        s0=rows[j]['spans'][0]
        haslab=is_label(s0) and s0['x']<left+15 and gap_ok(rows[j]['spans'])
        dy=rows[j]['y']-rows[j-1]['y'] if j else 99
        if not (haslab or (O[j]>R[j] and dy>=16)): continue
        o=sum(O[j:]); r_=sum(R[j:])
        if o<0.6*(o+r_) or o==0: continue
        sc=(o-r_)+(sum(R[:j])-sum(O[:j]))*0.0 + 0
        # prefer the earliest split that keeps the zone mostly oblique and has no long roman paragraph rows with body spacing above a label
        if sc>best[0]+0 and (best[1]==len(rows) or True): best=(sc,j)
    zone=best[1]
    cont_from=zone
    body=[]; labels=[]; refs=[]
    for j,r in enumerate(rows[:cont_from]):
        sp=list(r['spans'])
        # join leading margin-column spans ('5', ' &') into one label span
        k=0
        while k<len(sp) and sp[k]['x1']<left-6 and sp[k]['sz']>=7: k+=1
        if k>=2:
            sp=[dict(sp[0],t=''.join(x['t'] for x in sp[:k]).strip(),x1=sp[k-1]['x1'])]+sp[k:]
        if sp and re.match(r'^\d{1,3}\s*&$',sp[0]['t'].strip()) and sp[0]['x']<left+15 and gap_ok(sp):
            labels.append(dict(row=j,text=sp[0]['t'].strip(),tok=len(body))); sp=sp[1:]
        elif sp and is_label(sp[0]) and sp[0]['x']<left+15 and gap_ok(sp):
            labels.append(dict(row=j,text=sp[0]['t'].strip(),tok=len(body))); sp=sp[1:]
        for s in sp:
            if s['sz']<7:
                refs.append(dict(after=len(body)-1,raw=s['t'].strip(),y=r['y'],x=s['x'],trail=body[-1]['trail'] if body else 0)); continue
            for w in s['t'].split():
                n=norm(w)
                if n: body.append(dict(n=n,raw=w,row=j,trail=0))
                elif body: body[-1]['trail']+=1
    # merge adjacent small spans into one ref cluster (same row, close x)
    cl=[]
    for f in refs:
        if cl and cl[-1]['after']==f['after'] and abs(cl[-1]['y']-f['y'])<12: cl[-1]['raw']+=f['raw']
        else: cl.append(dict(f))
    notes=[]
    for r in rows[cont_from:]:
        sp=r['spans']
        k=0
        while k<len(sp) and sp[k]['x1']<left-5: k+=1
        mtxt=''.join(x['t'] for x in sp[:k]).strip()
        if k and re.search(r'\d',mtxt) and len(mtxt)<=7 and len(sp)>k:
            notes.append(dict(label=mtxt,words=[])); sp=sp[k:]
        elif sp and is_label(sp[0]) and sp[0]['x']<left+15 and gap_ok(sp):
            notes.append(dict(label=sp[0]['t'].strip(),words=[])); sp=sp[1:]
        if not notes: notes.append(dict(label=None,words=[]))   # continuation from previous page
        for s in sp:
            if s['sz']<7: continue
            notes[-1]['words']+= [norm(w) for w in s['t'].split() if norm(w)]
    return dict(body=body,labels=labels,refs=cl,notes=notes,left=left)
if __name__=='__main__':
    for i in [12,100,160,260,330]:
        p=page(i)
        print(i,'left',p['left'],'labels',[l['text'] for l in p['labels']],'refs',[(p['body'][r['after']]['raw'] if r['after']>=0 else None,r['raw']) for r in p['refs']],'notes',[(n['label'],' '.join(n['words'][:5])) for n in p['notes']])
