# Places each [illegible] run in the whole-page Latin OCR of its page by the neighbouring words, and takes the OCR words between (witness 1).
import json,re,sys,collections
from rapidfuzz.distance import Levenshtein as LV
def eq(a,b): return a==b or (len(a)>=4 and len(b)>=4 and LV.normalized_similarity(a,b)>=0.75) or (len(a)>=3 and len(b)>=3 and abs(len(a)-len(b))==1 and (a.endswith(b) or b.endswith(a)) and min(len(a),len(b))>=3)
from common import *
items=json.load(open("items.json"))
def ctx(t,s,e,n=4):
    b=t[max(0,s-300):s]; a=t[e:e+300]
    # stop at another placeholder
    b=IL.split(b)[-1]; a=IL.split(a)[0]
    bw=[norm(w) for w in re.findall(rf"[{L}0-9]+",clean(b))][-n:]
    aw=[norm(w) for w in re.findall(rf"[{L}0-9]+",clean(a))][:n]
    return [w for w in bw if w],[w for w in aw if w]
def place(it):
    t=NOTES[it["note"]]; B,A=ctx(t,it["s"],it["e"]); k=it["k"]
    best=[]
    for K in [it["K"],it["K"]+1,it["K"]-1,it["K"]+2]:
        W=tsv(it["v"],K)
        if W is None: continue
        idx=[i for i,w in enumerate(W) if w["n"]]       # word tokens
        nw=[W[i]["n"] for i in idx]
        for a in range(len(nw)+1):
            sb=0
            for q in range(1,len(B)+1):
                if a-q>=0 and eq(nw[a-q],B[-q]): sb+=1
                else: break
            if sb<1: continue
            for b in range(a,min(len(nw),a+3*k+4)+1):
                sa=0
                for q in range(len(A)):
                    if b+q<len(nw) and eq(nw[b+q],A[q]): sa+=1
                    else: break
                if sa>=1:
                    lo=idx[a-1]+1; hi=idx[b] if b<len(idx) else len(W)
                    best.append((sb+sa,min(sb,sa),K,lo,hi,sb,sa))
                    break
    if not best: return None,"not placed",B,A
    best.sort(key=lambda x:(-x[0],-x[1]))
    top=best[0]
    if len(best)>1 and best[1][0]==top[0] and (best[1][2],best[1][3])!=(top[2],top[3]): return None,"ambiguous",B,A
    sc,mn,K,lo,hi,sb,sa=top
    W=tsv(it["v"],K); g=W[lo:hi]
    if not g: return None,"empty gap",B,A
    return {"K":K,"lo":lo,"hi":hi,"sb":sb,"sa":sa,"words":[w["t"] for w in g],"conf":[w["c"] for w in g],
            "lines":sorted({w["ln"] for w in g}),"box":[min(w["x"] for w in g),min(w["y"] for w in g),max(w["x"]+w["w"] for w in g),max(w["y"]+w["h"] for w in g)]},"ok",B,A
if __name__=="__main__":
    vols=set(int(x) for x in sys.argv[1].split(",")) if len(sys.argv)>1 else None
    out=[]; c=collections.Counter()
    for it in items:
        if vols and it["v"] not in vols: continue
        if tsv(it["v"],it["K"] or 0) is None: c["page not OCR'd yet"]+=1; continue
        r,why,B,A=place(it); c[why]+=1
        if r: c["anchors %d+%d"%(min(r["sb"],3),min(r["sa"],3))]+=1
        out.append({"id":it["id"],"why":why,"r":r,"B":B,"A":A})
    json.dump(out,open("placed.json","w"),ensure_ascii=False)
    print(dict(c))
