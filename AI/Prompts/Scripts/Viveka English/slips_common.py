# Last slips pass, 23 Oct 2026, evening (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for proof.py, crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof4/lib-bundle.json).
import json,re,collections,importlib.util
spec=importlib.util.spec_from_file_location("proof","/home/claude/pf/proof.py"); P=importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
B=json.load(open("/mnt/user-data/uploads/Obsidian Vault/.work/pe-proof4/lib-bundle.json"))
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
TOKRX=re.compile(rf"(?<![{L}\\])[{L}]+(?![{L}])")
def skipline(t,s):
    a=t.rfind("\n",0,s)+1; e=t.find("\n",s); line=t[a:e if e>=0 else len(t)]
    if line.lstrip().startswith(("#","*[p.","^","*[PDF")): return None
    o=t.rfind("[[",0,s); c=t.rfind("]]",0,s)
    if o>c and t.find("\n",o,s)<0: return None
    fm=re.match(r"^---\n.*?\n---\n",t,re.S)
    if fm and s<fm.end(): return None
    return line
