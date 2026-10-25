# Night pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof5/lib-bundle.json).
# Needs pymupdf, the wamerican-large/wbritish-large word lists and tesseract-ocr-script-latn (the Latin-script model).
# For each [illegible] placeholder: find its page (^pgK marker), match the neighbouring words in the PDF text layer, and take what lies between.
import sys,json,re,collections,difflib,unicodedata,random
sys.path.insert(0,"/home/claude/pf")
from slips_common import T,tok,ENGL,P,L
import crops
crops.T=T
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def norm(s): return re.sub(r"[^a-z0-9]","",strip(s).lower())
IL=re.compile(r"\\\[illegible\\\]")
MK=re.compile(r"\*\[p\. [^\]]*\]\* \^pg(\d+)")
WRX=re.compile(rf"[{L}0-9]+")
def ctxwords(t,s,e,n=3):
    b=[w for w in WRX.findall(IL.sub(" ",t[max(0,s-120):s]))][-n:]
    a=[w for w in WRX.findall(IL.sub(" ",t[e:e+120]))][:n]
    return b,a
out=[]; stats=collections.Counter()
items=[]
for p,t in sorted(T.items()):
    v=int(re.search(r"vol (\d\d)",p).group(1)); mks=[(m.start(),int(m.group(1))) for m in MK.finditer(t)]
    for m in IL.finditer(t):
        # a run of placeholders counts as one gap
        if IL.match(t, max(0,m.start()-14)) and t[max(0,m.start()-14):m.start()].strip().endswith("\\]"): continue
        e=m.end(); k=1
        while True:
            m2=IL.match(t,e+1) if t[e:e+1]==" " else None
            if not m2: break
            e=m2.end(); k+=1
        ks=[K for s0,K in mks if s0<m.start()]
        if not ks: stats["no page"]+=1; continue
        items.append((p,v,ks[-1],m.start(),e,k))
random.seed(1)
def find(p,v,K,s,e,k):
    t=T[p]; b,a=ctxwords(t,s,e)
    if len(b)<2 or len(a)<2: return None,"few neighbours"
    nb=[norm(x) for x in b]; na=[norm(x) for x in a]
    best=None
    for i in (K-1,K,K-2):
        if i<0 or i>=crops.doc(v).page_count: continue
        ws=crops.words(v,i); nw=[norm(w[4]) for w in ws]
        for j in range(len(ws)):
            # before words end at j-1
            sb=sum(1 for q in range(1,len(nb)+1) if j-q>=0 and nw[j-q]==nb[-q])
            if sb<2: continue
            for g in range(1,k+4):
                if j+g+len(na)>len(nw): break
                sa=sum(1 for q in range(len(na)) if nw[j+g+q]==na[q])
                if sa>=2:
                    sc=sb+sa-0.3*(i!=K-1)
                    if not best or sc>best[0]: best=(sc,i,j,g)
                    break
    if not best: return None,"not matched"
    sc,i,j,g=best; ws=crops.words(v,i)
    return {"score":sc,"page":i,"j":j,"g":g,"words":[ws[j+q][4] for q in range(g)]},"ok"
S=random.sample(items,400) if "sample" in sys.argv else items
res=[]
for it in S:
    r,why=find(*it); stats[why]+=1
    if r: res.append((it,r))
print(len(items),"gaps;",stats)
cls=collections.Counter(); ex=collections.defaultdict(list)
for it,r in res:
    w=" ".join(r["words"]); ws=[x for x in re.findall(rf"[{L}]+",w)]
    if not ws: c="no letters"
    elif all(x.lower() in ENGL or x.lower() in P.STOP for x in ws): c="english words"
    elif all(tok.get(x,0)>=3 for x in ws): c="attested in the copy"
    else: c="other"
    cls[c]+=1
    if len(ex[c])<12: ex[c].append(w)
print(cls)
for c,v in ex.items(): print(c,"|"," ¦ ".join(v))
json.dump([[list(it),r] for it,r in res],open("illeg-sample.json" if "sample" in sys.argv else "illeg-all.json","w"),ensure_ascii=False)
