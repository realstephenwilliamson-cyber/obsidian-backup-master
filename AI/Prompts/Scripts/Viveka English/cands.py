# Second proofreading pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace with the work in /home/claude/pf/:
# done-in/ and other-in/ hold the 123 chapter notes and the 43 other notes as they were; other-proof/ the 43 after clean.py and proof.py;
# the PDFs and lib-bundle.json staged from the vault. Change the paths to run it elsewhere.
"""Candidates for the second proofreading pass (23 Oct 2026). Work text: the 123 chapter notes as they are; the 43 other notes after clean.py + proof.py."""
import json,re,collections,glob,unicodedata,random,os,importlib.util
spec=importlib.util.spec_from_file_location("proof","proof.py"); P=importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
L=r"A-Za-zÀ-ɏḀ-ỿ"
T={}
for d in ("done-in","other-proof"):
    for f in glob.glob(d+"/*/*.md"): T[f.split("/",1)[1]]=open(f,encoding="utf-8").read()
tok=collections.Counter()
for t in T.values():
    for w in re.findall(rf"[{L}]+",t): tok[w]+=1
ENGL=set()
for f in ('/usr/share/dict/american-english-large','/usr/share/dict/british-english-large'):
    ENGL|={w.strip().lower() for w in open(f,encoding='utf-8',errors='ignore')}
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
var=collections.defaultdict(collections.Counter)
for w,c in tok.items():
    if strip(w)!=w: var[strip(w).lower()][w]+=c
V="aāiīuūeoṛ"
# A: words whose initial Ś/ś may be lost
A=set(P.WORDS)
for w,c in tok.items():
    if w[0] in "śŚ" or len(w)<3 or w.lower() in P.STOP or w.lower() in ENGL: continue
    for pre in "śŚ":
        v=pre+w
        if tok.get(v,0)>=3 and tok[v]>=3*c: A.add(w)
# B: ṁ read as ri / r
Bm={}
for w,c in tok.items():
    if w.lower() in ENGL or len(w)<3: continue
    for m in re.finditer(rf"(?<=[{V}])(ri|r)(?=[^aāiīuūeoṛ]|$)", w):
        v=w[:m.start()]+"ṁ"+w[m.end():]
        if tok.get(v,0)>=3 and tok[v]>=3*c: Bm[w]=v; break
# C: plain-ASCII parenthesised terms with a much commoner diacritic spelling
Cm={}
for w in set(re.findall(r"\(([a-z]+)\)","\n".join(T.values()))):
    vs=var.get(w)
    if not vs: continue
    v,vc=vs.most_common(1)[0]
    if vc>=3 and vc>=3*tok[w]: Cm[w]=v
TOKRX=re.compile(rf"(?<![{L}\\])[{L}]+(?![{L}])")
def skip(t,s):
    a=t.rfind("\n",0,s)+1; line=t[a:t.find("\n",s) if t.find("\n",s)>=0 else len(t)]
    if line.lstrip().startswith(("#","*[p.","^","*[PDF")) : return True
    o=t.rfind("[[",0,s); c=t.rfind("]]",0,s)
    if o>c and t.find("\n",o,s)<0: return True
    fm=re.match(r"^---\n.*?\n---\n",t,re.S)
    if fm and s<fm.end(): return True
    return False
out=[]
for p,t in sorted(T.items()):
    for m in TOKRX.finditer(t):
        w=m.group(0); s=m.start()
        k=None
        if w in Bm: k=("B",Bm[w])
        elif w in A: k=("A",None)
        elif w in Cm and t[s-1:s]=="(" and t[m.end():m.end()+1]==")": k=("C",Cm[w])
        if not k or skip(t,s): continue
        out.append({"path":p,"s":s,"e":m.end(),"w":w,"kind":k[0],"prop":k[1],"ctx":t[max(0,s-70):m.end()+50].replace("\n"," ⏎ ")})
c=collections.Counter(x["kind"] for x in out); print(c)
json.dump(out,open("cands.json","w"),ensure_ascii=False)
