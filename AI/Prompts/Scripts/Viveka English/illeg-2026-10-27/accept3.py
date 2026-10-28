# Acceptance by vote (version 3, with Monier-Williams headwords as the clean spelling list): at least two of the three OCR readings (page, 600-dpi crop without dictionary, 450-dpi crop with dictionary)
# agree on the letters; the spelling is a reading's own if every word is attested in the copy (3+ times, no commoner marked form);
# otherwise the copy's dominant spelling with the same macrons, only if the readings' marks are a subset of it. Tiers are kept for the check.
import json,sys,re,collections,unicodedata
from common import *
items={i["id"]:i for i in json.load(open("items.json"))}
OKP=set("()‘’“”'\",.;:-—–?! ")
MAC="̄"
def macrons(s): return "".join(ch for ch in unicodedata.normalize("NFD",s.lower()) if (not unicodedata.combining(ch) and ch.isalpha()) or ch==MAC)
MW=set(json.load(open("mw-heads.json")))
MWS=collections.defaultdict(set)
for h in MW: MWS[strip(h)].add(h)
def attested(w): return tok.get(w,0)>=3 and not dominated(w)
def submarks(a,b):
    om=[ch for ch in unicodedata.normalize("NFD",a) if unicodedata.combining(ch)]
    tm=[ch for ch in unicodedata.normalize("NFD",b) if unicodedata.combining(ch)]
    return all(om.count(m)<=tm.count(m) for m in set(om))
def spell(w,inpar=False):
    """(spelling, how) for one OCR word, or (None, why)"""
    lw=w.lower(); case=(lambda a: a[0].upper()+a[1:]) if w[:1].isupper() else (lambda a:a)
    if len(w)>1 and w.isupper(): return None,"capitals"
    if lw in ENGL and not re.search("[^a-z]",lw) and not (inpar and strip(lw) in MWS): return w,"english"
    # Monier-Williams spellings with the same letters and macrons, carrying at least the OCR's marks
    mc=[h for h in MWS.get(strip(lw),()) if macrons(h)==macrons(lw) and submarks(lw,h)]
    if len(mc)==1: return case(mc[0]),("mw as read" if mc[0]==lw else "mw spelling")
    if len(mc)>1:
        sc=sorted(((tok.get(h,0)+tok.get(h[:1].upper()+h[1:],0),h) for h in mc),reverse=True)
        if sc[0][0]>=3 and sc[0][0]>=3*sc[1][0]: return case(sc[0][1]),"mw, copy decides"
        return None,"mw ambiguous"
    if attested(w): return w,"copy only"
    return None,"unattested"
def copyspell(w):
    vs=sorted([(a,c) for a,c in VAR[strip(w).lower()] if c>=3 and macrons(a)==macrons(w)],key=lambda x:-x[1])
    if not vs: return None
    top=vs[0]
    if len(vs)>1 and top[1]<3*vs[1][1]: return None
    om=[ch for ch in unicodedata.normalize("NFD",w) if unicodedata.combining(ch)]
    tm=[ch for ch in unicodedata.normalize("NFD",top[0]) if unicodedata.combining(ch)]
    if not all(om.count(m)<=tm.count(m) for m in set(om)): return None
    a=top[0]; return (a[0].upper()+a[1:]) if w[:1].isupper() else (a[0].lower()+a[1:])
def paren_bal(s): return s.count("(")-s.count(")")
def decide(x,W2):
    it=items[x["id"]]; r=x["r"]; w=W2.get(str(x["id"]),{})
    if "ocr3" not in w: return None,w.get("why","no crop witnesses")
    tier=[]
    if min(r["sb"],r["sa"])<2:
        if min(r["sb"],r["sa"])<1 or r["sb"]+r["sa"]<5: return None,"weak anchors"
        tier.append("weak anchors")
    C=[fix(" ".join(r["words"])),fix(w["ocr"]),fix(w["ocr3"])]
    N=[norm(c) for c in C]
    cnt=collections.Counter(n for n in N if n)
    if not cnt: return None,"no letters"
    maj,mc=cnt.most_common(1)[0]
    if mc<2: return None,"witnesses differ"
    tier.append("3 of 3" if mc==3 else "2 of 3")
    cands=[c for c,n in zip(C,N) if n==maj]
    if len({macrons(c) for c in cands})>1: return None,"macrons differ"
    best=None; why=None; outs=[]
    for c in cands:
        out=c; hows=[]; inpar=c.strip().startswith("(")
        for q in WRD.findall(c):
            sp,h=spell(q,inpar)
            if not sp: why=h; out=None; break
            hows.append(h); out=out.replace(q,sp,1)
        if out: outs.append((sum(marks(q) for q in WRD.findall(out)),-len(outs),out,hows))
    if not outs: return None,why or "no spelling"
    outs.sort(reverse=True); best=outs[0][2]; tier.append("+".join(sorted(set(outs[0][3]))))
    if len({o[2] for o in outs})>1: tier.append("readings differ in marks")
    tail=re.sub(rf"^.*[{L}]","",best)
    if not re.fullmatch(r"[)’”'\"]*[,.;:]?[)’”'\"]*",tail): return None,"odd punctuation"
    if re.search(r"\d",best): return None,"digits"
    if [ch for ch in best if not (re.match(rf"[{L}]",ch) or ch in OKP or unicodedata.combining(ch))]: return None,"junk characters"
    ws=WRD.findall(best)
    if not ws or len(ws)>it["k"]+2: return None,"word count"
    if any(len(strip(q))<2 for q in ws): return None,"short word"
    eng=all(q.lower() in ENGL for q in ws)
    if eng:
        tier.append("english")
        if min(r["sb"],r["sa"])<3: return None,"english, weak anchors"
    Wp=tsv(it["v"],r["K"]); line=[q for q in Wp if list(q["ln"])==list(r["lines"][0])]
    cw=sum(q["w"] for q in line)/max(1,sum(len(q["t"]) for q in line))
    wratio=(r["box"][2]-r["box"][0])/max(1,len(best.strip())*cw)
    t=NOTES[it["note"]]; pre=t[it["s"]-1:it["s"]]; post=t[it["e"]:it["e"]+1]
    out=best.strip()
    # a closing quote with no opening quote before it on the line is most likely a footnote number the OCR misread
    # a closing quote stays only where two readings have it
    for qc in "”’":
        if out.endswith(qc) and sum(1 for c in C if c.rstrip().endswith(qc))<2: out=out[:-1]; tier.append("quote dropped")
    if pre and pre in "(‘“'\"" and out.startswith(pre): out=out[1:]
    if post and post in ")’”'\".,;:" and out.endswith(post): out=out[:-1]
    if pre and not (pre.isspace() or pre in "(‘“'\"[—–-"): return None,"joined to the word before"
    if post and post.isalpha(): return None,"joined to the word after"
    # the line's brackets must not get less balanced
    ls=it["ls"]; le=t.find("\n",it["e"]); le=len(t) if le<0 else le
    before=t[ls:it["s"]]+t[it["e"]:le]; after=t[ls:it["s"]]+out+t[it["e"]:le]
    if abs(paren_bal(IL.sub("",after)))>abs(paren_bal(IL.sub("",before))): return None,"brackets"
    out=out.replace("[","\\[").replace("]","\\]")
    if not out: return None,"empty"
    return {"id":x["id"],"fill":out,"C":C,"tier":tier,"english":eng,"wratio":round(wratio,2)},"accepted"
if __name__=="__main__":
    P=json.load(open(sys.argv[1])); W2=json.load(open("w2.json"))
    c=collections.Counter(); acc=[]; tiers=collections.Counter()
    for x in P:
        if x["why"]!="ok": c[x["why"]]+=1; continue
        d,why=decide(x,W2); c[why]+=1
        if d: acc.append(d); tiers[" / ".join(d["tier"])]+=1
    print(dict(c)); print(dict(tiers))
    json.dump(acc,open(sys.argv[2] if len(sys.argv)>2 else "accepted.json","w"),ensure_ascii=False)
