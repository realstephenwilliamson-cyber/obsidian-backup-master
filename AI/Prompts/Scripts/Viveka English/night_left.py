# The ~190 leftovers, 23 Oct 2026, late (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the current text rebuilt from .work/pe-proof5/lib-bundle.json plus the night patches.
# The ~190 left by the evening pass and the 23 Oct second pass: rebuild the current text, find the items, place them by their neighbours.
import json,glob,re,sys,collections,difflib,unicodedata
sys.path.insert(0,"/home/claude/pf")
from slips_common import T as T5,tok,ENGL,P,L,skipline,TOKRX
import crops
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def norm(s): return re.sub(r"[^a-z0-9]","",strip(s).lower())
# current text = pe-proof5 bundle + pf35 (apply5-n2) + pf38 (apply6)
def apply_edits(TT,ed):
    by=collections.defaultdict(list)
    for e in ed: by[e[0]].append(e[1:5])
    out={}
    for p,t in TT.items():
        u=t
        for s,e,w,v in sorted(by.get(p,[]),reverse=True): assert u[s:e]==w,(p,s,w,u[s:e]); u=u[:s]+v+u[e:]
        out[p]=u
    return out,by
T4,b1=apply_edits(T5,json.load(open("apply5-n2.json")))
T3,b2=apply_edits(T4,json.load(open("apply6.json")))
def shift(by,p,s): return s+sum(len(v)-len(w) for s0,e0,w,v in by.get(p,[]) if s0<s)
items=[]
# (1) evening leftovers: positions in the pe-proof4 bundle -> through the evening patch (apply.json) and the two night patches
reads={}
for f in glob.glob("/home/claude/pf/read/P-*.jsonl"):
    for l in open(f):
        l=l.strip()
        if l:
            try: r=json.loads(l); reads[r["id"]]=r
            except: pass
b0=collections.defaultdict(list)
for p,s,e,w,v,k in json.load(open("apply.json")): b0[p].append((s,e,w,v))
done={(a[0],a[1]) for a in json.load(open("apply.json"))}
retried={x["id"] for x in json.load(open("q-items.json"))["U"]}
for x in json.load(open("items-placed.json")):
    if x["kind"].startswith("S") or (x["path"],x["s"]) in done or x["id"] in retried: continue
    r=reads.get(x["id"]); pr=(r or {}).get("printed","").strip("-–()[];:,.'’‘\"> !?|")
    if r and pr==x["w"] and r.get("conf")=="high": continue
    if r and r.get("conf")=="high" and pr and "other reading" and len(pr)>len(x["w"])+2: continue
    p=x["path"]; s=shift(b2,p,shift(b1,p,shift(b0,p,x["s"]))); e=s+len(x["w"])
    if T3[p][s:e]!=x["w"]: continue
    items.append({"src":"E"+x["kind"],"path":p,"s":s,"e":e,"w":x["w"],"prop":x.get("prop")})
# (2) second pass: A (lost Ś in Sanskrit lines) and C (plain bracketed terms), on the current text
toks=collections.Counter()
for t in T3.values():
    for w in re.findall(rf"[{L}]+",t): toks[w]+=1
var=collections.defaultdict(collections.Counter)
for w,c in toks.items():
    if strip(w)!=w: var[strip(w).lower()][w]+=c
A=set(P.WORDS)
for w,c in toks.items():
    if w[0] in "śŚ" or len(w)<3 or w.lower() in P.STOP or w.lower() in ENGL: continue
    for pre in "śŚ":
        if toks.get(pre+w,0)>=3 and toks[pre+w]>=3*c: A.add(w)
Cm={}
for w in set(re.findall(r"\(([a-z]+)\)","\n".join(T3.values()))):
    vs=var.get(w)
    if vs:
        v,vc=vs.most_common(1)[0]
        if vc>=3 and vc>=3*toks[w]: Cm[w]=v
second=[]
for p,t in sorted(T3.items()):
    for m in TOKRX.finditer(t):
        w=m.group(0); s=m.start(); line=None
        if w in Cm and t[s-1:s]=="(" and t[m.end():m.end()+1]==")":
            if skipline(t,s) is not None: second.append({"src":"C","path":p,"s":s,"e":m.end(),"w":w,"prop":Cm[w]})
        elif w in A:
            line=skipline(t,s)
            if line is not None and not P.english_line(line): second.append({"src":"A","path":p,"s":s,"e":m.end(),"w":w,"prop":None})
crops.T=T3
MK=re.compile(r"\*\[p\. [^\]]*\]\* \^pg(\d+)")
WRX=re.compile(rf"[{L}0-9]+")
def ctx(t,s,e,n=3):
    return [norm(w) for w in WRX.findall(t[max(0,s-100):s])][-n:],[norm(w) for w in WRX.findall(t[e:e+100])][:n]
def oldstyle_ok(c):
    # the second pass's test: two of the three neighbours on each side match, and for a gloss the brackets are in the text layer
    b=crops.locate(c)
    if not b: return False
    sc,v,i,j=b; ws=crops.words(v,i); nw=[norm(w[4]) for w in ws]; bb,aa=ctx(T3[c["path"]],c["s"],c["e"])
    nb=sum(1 for q in range(1,len(bb)+1) if j-q>=0 and nw[j-q]==bb[-q]); na=sum(1 for q in range(len(aa)) if j+1+q<len(nw) and nw[j+1+q]==aa[q])
    br=c["src"]!="C" or ("(" in ws[j][4] and ")" in ws[j][4])
    return nb>=2 and na>=2 and br
def place(c):
    t=T3[c["path"]]; v=int(re.search(r"vol (\d\d)",c["path"]).group(1)); ks=[int(m.group(1)) for m in MK.finditer(t) if m.start()<c["s"]]
    if not ks: return None
    K=ks[-1]; bb,aa=ctx(t,c["s"],c["e"]); target=norm(c["w"]); best=None
    for i in (K-1,K,K-2,K-3,K+1):
        if i<0 or i>=crops.doc(v).page_count: continue
        ws=crops.words(v,i); nw=[norm(w[4]) for w in ws]
        R=lambda a,b: a==b or (len(a)>2 and difflib.SequenceMatcher(None,a,b).ratio()>0.7)
        for j in range(len(ws)):
            sb=sum(1 for q in range(1,len(bb)+1) if j-q>=0 and R(nw[j-q],bb[-q]))
            if sb<1: continue
            for g in (1,2,3):
                if j+g+len(aa)>len(nw): break
                sa=sum(1 for q in range(len(aa)) if R(nw[j+g+q],aa[q]))
                if sa>=1 and sb+sa>=3:
                    sim=difflib.SequenceMatcher(None,"".join(nw[j:j+g]),target).ratio()
                    sc=sb+sa+sim-0.3*(i!=K-1)
                    if sim>=0.3 and (not best or sc>best[0]): best=(sc,v,i,j,g)
                    break
    return best
unres=[c for c in second if not oldstyle_ok(c)]
print("evening leftovers",len(items),collections.Counter(x["src"] for x in items)); print("second-pass candidates",len(second),collections.Counter(x["src"] for x in second),"not placed by the old test",len(unres),collections.Counter(x["src"] for x in unres))
allc=items+unres; placed=[]
for n,c in enumerate(allc):
    b=place(c)
    if not b: continue
    sc,v,i,j,g=b; ws=crops.words(v,i)[j:j+g]
    if len({(w[5],w[6]) for w in ws})>1: continue
    c["box"]=[v,i,min(w[0] for w in ws)-4,min(w[1] for w in ws),max(w[2] for w in ws)+2,max(w[3] for w in ws)]; c["id"]=f"L{len(placed)+1:03d}"; placed.append(c)
print("placed",len(placed),collections.Counter(x["src"] for x in placed))
json.dump(placed,open("l190.json","w"),ensure_ascii=False)
import pickle; pickle.dump(T3,open("T3.pkl","wb"))
