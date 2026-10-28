# Shared helpers for the [illegible] pass of 27 Oct 2026: the notes, the copy's word counts, OCR TSV pages, the Latin-model quirk map.
import re,json,glob,unicodedata,collections,os
NFC=lambda s: unicodedata.normalize("NFC",s)
L="A-Za-zĀāĪīŪūṚṛṜṝḶḷḸḹṄṅÑñṬṭḌḍṆṇŚśṢṣḤḥṀṁṂṃ"
WRD=re.compile(rf"[{L}]+")
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def norm(s): return re.sub(r"[^a-z0-9]","",strip(NFC(s)).lower().replace("ı","i"))
def marks(s): return sum(1 for ch in unicodedata.normalize('NFD',s) if unicodedata.combining(ch))
NOTES={}
for p in sorted(glob.glob(os.path.join(os.path.dirname(__file__),"notes/lib/*/*.md"))):
    NOTES[p.split("notes/lib/")[1]]=open(p,encoding="utf-8").read()
IL=re.compile(r"\\\[illegible\\\]")
def clean(t):
    t=re.sub(r"\[\^[^\]]+\]","",t)                 # footnote calls
    t=re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]",r"\1",t)  # labelled links
    t=re.sub(r"\[\[([^\]]*)\]\]",r"\1",t)
    t=re.sub(r"\*\[p\. [^\]]*\]\* \^pg\d+","\n",t)
    t=re.sub(r"(?m)^#+ .*$","\n",t)
    t=re.sub(r"\s\^[A-Za-z0-9-]+\s*$","",t,flags=re.M)
    return t.replace("\\","")
tok=collections.Counter()
for t in NOTES.values():
    for w in WRD.findall(clean(IL.sub(" ",t))): tok[NFC(w)]+=1
VAR=collections.defaultdict(list)
for w,c in tok.items(): VAR[strip(w).lower()].append((w,c))
ENGL=set()
for f in ("/usr/share/dict/american-english-large","/usr/share/dict/british-english-large"):
    for l in open(f,encoding="utf-8",errors="ignore"):
        l=l.strip()
        if l and "'" not in l: ENGL.add(l.lower())
MAP=str.maketrans({"ü":"ū","Ü":"Ū","ï":"ī","Ï":"Ī","à":"ā","À":"Ā","å":"ā","Å":"Ā","š":"ś","Š":"Ś","ä":"ā","Ä":"Ā","ė":"e","è":"e","ʻ":"‘","Ț":"Ṭ","ț":"ṭ","ș":"ṣ","Ș":"Ṣ","ş":"ṣ","Ş":"Ṣ","ņ":"ṇ","Ņ":"Ṇ","ţ":"ṭ","Ţ":"Ṭ","ŝ":"ś","Ŝ":"Ś","ħ":"ṅ","ã":"ā","ă":"ā","}":")","{":"(","ı":"i"})
V="aāiīuūeoṛ"
def fix(w):
    w=NFC(w)
    w=re.sub(rf"(?<=[{V}])rı(?=[^aāiīuūeoṛ]|$)","ṁ",w)
    w=w.translate(MAP)
    w=re.sub(r"ñ(?=[gk])","ṅ",w)
    w=re.sub(r"ń(?=$|[^a-zA-Z])","ṁ",w)
    w=re.sub(r"(^|[\s(‘“])\$",r"\1Ś",w)
    w=re.sub(r"[™®°*^]+(?=[)’”'\".,;:]*$)","",w)
    w=re.sub(rf"(?<=[{V}])r[hn](?=[^aāiīuūeoṛ]|$)","ṁ",w)
    return NFC(w)
def dominated(w):
    c=tok.get(w,0)
    return any(v!=w and vc>=c and marks(v)>marks(w) for v,vc in VAR[strip(w).lower()])
def tsv(v,K):
    fn=os.path.join(os.path.dirname(__file__),f"ocr/v{v:02d}-p{K:04d}.tsv")
    if not os.path.exists(fn): return None
    out=[]
    for l in open(fn,encoding="utf-8").read().split("\n")[1:]:
        f=l.split("\t")
        if len(f)<12 or f[0]!="5" or not f[11].strip(): continue
        out.append({"t":NFC(f[11]),"n":norm(f[11]),"x":int(f[6]),"y":int(f[7]),"w":int(f[8]),"h":int(f[9]),"c":float(f[10]),"ln":(int(f[2]),int(f[3]),int(f[4]))})
    return out
