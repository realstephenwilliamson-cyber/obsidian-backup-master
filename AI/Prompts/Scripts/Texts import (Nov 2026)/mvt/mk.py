"""Parse the Muktabodha KSTS e-text of the Malinivijayottara (M00160) into chapters -> verses -> half-lines.
Variant notes in [brackets] are dropped; a verse is the text up to '|| n ||', its halves are split at '|'."""
import re, json
ORD=['prathamo','dvitīyo','tṛtīyo','caturtho','pañcamo','ṣaṣṭho','saptamo','aṣṭamo','navamo','daśamo']
def parse(path='ref/mk_iast.txt'):
    t=open(path,encoding='utf-8').read()
    t=t.split('####################################################')[-1]
    t=re.sub(r'\[[^\]]*\]','',t,flags=re.S)
    t=re.sub(r'(?m)^\s*p\. *\d+\)\s*$','',t)
    # chapter starts
    marks=[]
    for i,o in enumerate(ORD):
        m=re.search(r'(?m)^'+o+r"'?dhikāraḥ\s*\|?\s*$",t)
        if m: marks.append((m.start(),m.end(),i+1))
    marks.sort(); chs={}
    for j,(s,e,ch) in enumerate(marks):
        body=t[e: marks[j+1][0] if j+1<len(marks) else len(t)]
        body=re.sub(r'(?m)^(atha|mālinīvijayottare tantre)\s*$','',body)
        body=' '.join(body.split())
        col=None
        m=re.search(r"iti śrīmālinīvijayottare[^|]*\|\|\s*\d+\s*\|\|\s*$",body)
        if m: col=m.group(0); body=body[:m.start()]
        vs=[]; pos=0
        for m in re.finditer(r'\|\|\s*(\d+)\s*\|\|',body):
            seg=body[pos:m.start()]; pos=m.end()
            halves=[h.strip() for h in seg.split('|') if h.strip()]
            vs.append([int(m.group(1)),halves])
        rest=body[pos:].strip()
        chs[ch]=dict(verses=vs,colophon=col,rest=rest)
    return chs
if __name__=='__main__':
    c=parse()
    for k in sorted(c):
        vs=c[k]['verses']; nums=[v for v,_ in vs]
        print(k,len(vs),'last',nums[-1],'gaps',[(a,b) for a,b in zip(nums,nums[1:]) if b!=a+1][:5],'halves',{n:sum(1 for _,h in vs if len(h)==n) for n in sorted(set(len(h) for _,h in vs))},'| rest:',c[k]['rest'][:60],'|',(c[k]['colophon'] or '')[:70])
    json.dump(c,open('work/mk.json','w'),ensure_ascii=False)
