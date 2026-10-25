# Night pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof5/lib-bundle.json).
# Needs pymupdf, the wamerican-large/wbritish-large word lists and tesseract-ocr-script-latn (the Latin-script model).
# Accept a re-OCR'd gap only if, after mapping Tesseract's Latin-model quirks to IAST, every word occurs at least 3 times elsewhere in the copy.
import json,re,sys,collections,unicodedata
from slips_common import tok,ENGL,L,T
NFC=lambda s: unicodedata.normalize("NFC",s)
MAP=str.maketrans({"ş":"ṣ","Ş":"Ṣ","ņ":"ṇ","Ņ":"Ṇ","ţ":"ṭ","Ţ":"Ṭ","ŝ":"ś","Ŝ":"Ś","ħ":"ṅ"})
V="aāiīuūeoṛ"
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def marks(s): return sum(1 for ch in unicodedata.normalize('NFD',s) if unicodedata.combining(ch))
VAR=collections.defaultdict(list)
for w,c in tok.items(): VAR[strip(w).lower()].append((w,c))
def dominated(w):
    c=tok.get(w,0)
    return any(v!=w and vc>=c and marks(v)>marks(w) for v,vc in VAR[strip(w).lower()])
def fix(w):
    w=NFC(w).translate(MAP)
    w=re.sub(r"ñ(?=[gk])","ṅ",w)
    w=re.sub(rf"(?<=[{V}])r[hn](?=[^aāiīuūeoṛ]|$)","ṁ",w)
    return w
SHAPE=re.compile(rf"^[(\[‘'“\"]?[{L}’'\- ]+[)\]’'”\"]?[.,;:]?[)\]]?[.,;:]?$")
def accept(o,k):
    o=o.strip()
    if not o or not SHAPE.match(o): return None
    ws=re.findall(rf"[{L}]+",o)
    if not ws or len(ws)>k+2: return None
    fw=[fix(w) for w in ws]
    if all(w.lower() in ENGL for w in fw): return None
    if not all(tok.get(w,0)>=3 for w in fw): return None
    if any(re.search("nṇ|ṇn|ṁṁ|rn$|ñ$|rh|hn(?=[^aāiīuūeo])|m$|q|[aāiīuūeo]r$",w) or dominated(w) or len(w)<3 for w in fw): return None
    if re.search(r"[^A-Za-zāīūṛṝḷṅñṭḍṇśṣḥṁĀĪŪṚŚṢṬḌṆṄ’'\-\s(\[)\].,;:‘“”\"]",NFC(o).translate(MAP)): return None
    if any(w[0].isupper() and tok.get(w[0].lower()+w[1:],0)>=tok.get(w,0) for w in fw): return None
    out=o
    for w,f in zip(ws,fw): out=out.replace(w,f,1)
    out=NFC(out).replace("[","\\[").replace("]","\\]")
    return out
if __name__=="__main__":
    R=json.load(open(sys.argv[1])); acc=[]; c=collections.Counter()
    for r in R:
        p,v,K,s,e,k=r["it"]
        if not r.get("ocr"): c["no ocr"]+=1; continue
        a=accept(r["ocr"],k)
        if a: acc.append({"path":p,"s":s,"e":e,"w":T[p][s:e],"prop":a,"ocr":r["ocr"],"box":r["box"],"kind":"G"}); c["accepted"]+=1
        else: c["rejected"]+=1
    print(c); json.dump(acc,open(sys.argv[2],"w"),ensure_ascii=False)
    for a in acc[:25]: print(repr(a["ocr"]),"->",a["prop"])
