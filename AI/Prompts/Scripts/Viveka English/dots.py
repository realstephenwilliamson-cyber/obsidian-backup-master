# Dots-below pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/dots/ for the work,
# /home/claude/pf/ for proof.py, crops.py and the sheets; the library copy from a read-only bundle job (.work/pe-proof3/lib-bundle.json).
"""Dots-below pass (23 Oct 2026): words in the library copy of Dyczkowski's Tantraloka whose dotted spelling (ṛ ṇ ḍ ṭ ḥ ṣ ḷ) is far commoner in the
same copy. Tiers: T1 the word has other diacritics (partly marked); T2 an all-ASCII word in a Sanskrit line; T3 an all-ASCII word in an English line
(the print itself often leaves glosses unmarked)."""
import json,re,collections,sys,importlib.util,random,os
spec=importlib.util.spec_from_file_location("proof","/home/claude/pf/proof.py"); P=importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
B=json.load(open("/mnt/user-data/uploads/Obsidian Vault/.work/pe-proof3/lib-bundle.json"))
PFX="Library/Trika/Tantraloka (Dyczkowski)/"
T={p[len(PFX):]:t for p,t in B.items() if not p.split("/")[-1].startswith("Tantraloka vol ")}
L=r"A-Za-zÀ-ɏḀ-ỿ"
DOT={"ṛ":"r","ṇ":"n","ḍ":"d","ṭ":"t","ḥ":"h","ṣ":"s","ḷ":"l","Ṛ":"R","Ṇ":"N","Ḍ":"D","Ṭ":"T","Ḥ":"H","Ṣ":"S"}
und=lambda w: "".join(DOT.get(c,c) for c in w)
tok=collections.Counter()
for t in T.values():
    for w in re.findall(rf"[{L}]+",t): tok[w]+=1
ENGL=set()
for f in ('/usr/share/dict/american-english-large','/usr/share/dict/british-english-large'):
    ENGL|={w.strip().lower() for w in open(f,encoding='utf-8',errors='ignore')}
byk=collections.defaultdict(list)
for w,c in tok.items(): byk[und(w)].append((c,w))
fix={}
for w,c in tok.items():
    if len(w)<3 or w.lower() in ENGL or w.lower() in P.STOP or any(ch in DOT for ch in w) and False: continue
    best=None
    for vc,v in byk[und(w)]:
        if v==w or len(v)!=len(w): continue
        # v may add dots only where w has the plain letter
        if all(a==b or (a in DOT and DOT[a]==b) for a,b in zip(v,w)) and vc>=3 and vc>=3*c:
            if not best or vc>best[0]: best=(vc,v)
    if best: fix[w]=best[1]
TOKRX=re.compile(rf"(?<![{L}\\])[{L}]+(?![{L}])")
def skipline(t,s):
    a=t.rfind("\n",0,s)+1; e=t.find("\n",s); line=t[a:e if e>=0 else len(t)]
    if line.lstrip().startswith(("#","*[p.","^","*[PDF")): return None
    o=t.rfind("[[",0,s); c=t.rfind("]]",0,s)
    if o>c and t.find("\n",o,s)<0: return None
    fm=re.match(r"^---\n.*?\n---\n",t,re.S)
    if fm and s<fm.end(): return None
    return line
out=[]
for p,t in sorted(T.items()):
    for m in TOKRX.finditer(t):
        w=m.group(0)
        if w not in fix: continue
        line=skipline(t,m.start())
        if line is None: continue
        tier="T1" if re.search(r"[^\x00-\x7f]",w) else ("T3" if P.english_line(line) else "T2")
        out.append({"path":p,"s":m.start(),"e":m.end(),"w":w,"prop":fix[w],"kind":tier})
c=collections.Counter(x["kind"] for x in out); print("forms",len(fix),"occurrences",len(out),dict(c))
json.dump(out,open("dcands.json","w"),ensure_ascii=False)
for k in ("T1","T2","T3"):
    ex=collections.Counter((x["w"],x["prop"]) for x in out if x["kind"]==k).most_common(12); print(k,ex)

# Rules from Sanskrit spelling (no attestation needed): r between consonants (or word-initial before a consonant) is ṛ; a final h after a vowel is ḥ.
CONS="bcdfghjklmnpqstvwxyzḍḥḷṁṅṇñṭṣśBCDFGHJKLMNPQSTVWXYZŚṢṬḌṆ"
VOW="aāiīuūeoṛAĀIĪUŪEO"
RR=re.compile(rf"(?<=[{CONS}])r(?=[{CONS.replace('y','').replace('v','')}])")
HH=re.compile(rf"(?<=[{VOW}])h$")
def rules(w):
    if len(w)<3 or w.lower() in ENGL or w.lower() in P.STOP: return None
    v=RR.sub("ṛ",w); v=HH.sub("ḥ",v)
    return v if v!=w else None
seen={(x["path"],x["s"]) for x in out}; rout=[]
for p,t in sorted(T.items()):
    for m in TOKRX.finditer(t):
        w=m.group(0); v=rules(fix.get(w,w))
        if not v: continue
        line=skipline(t,m.start())
        if line is None or t[max(0,m.start()-2):m.start()].strip().endswith("-"): continue
        eng=P.english_line(line)
        if eng and v.endswith("ḥ") and w[0].isupper() and not re.search(r"[^\x00-\x7f]",w): v=v[:-1]+"h"
        if v==w: continue; kind=("R" if "ṛ" in v.lower() or "Ṛ" in v else "")+("H" if v.endswith("ḥ") else "")
        rout.append({"path":p,"s":m.start(),"e":m.end(),"w":w,"prop":v,"kind":("S" if not eng else ("EM" if re.search(r"[^\x00-\x7f]",w) else "EP")),"also_att":(p,m.start()) in seen})
c=collections.Counter(x["kind"] for x in rout); print("rule occurrences",len(rout),dict(c))
for k in sorted(c): print(k,collections.Counter((x["w"],x["prop"]) for x in rout if x["kind"]==k).most_common(10))
json.dump(rout,open("rcands.json","w"),ensure_ascii=False)
