# Night pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof5/lib-bundle.json).
# Needs pymupdf, the wamerican-large/wbritish-large word lists and tesseract-ocr-script-latn (the Latin-script model).
from slips_common import *
import random
V="aāiīuūeoṛ"; NAMES={"Silburn","Coburn","Bjorn","Osborn","Auburn","Byrn"}
R=[]
for p,t in sorted(T.items()):
    for m in TOKRX.finditer(t):
        w=m.group(0)
        if not re.search(rf"(?<=[{V}])rn$",w) or w.lower() in ENGL or w in NAMES or len(w)<3 and False: continue
        line=skipline(t,m.start())
        if line is None: continue
        R.append({"path":p,"s":m.start(),"e":m.end(),"w":w,"prop":w[:-2]+"ṁ","kind":"N2","eng":P.english_line(line)})
c=collections.Counter(x["w"] for x in R); print(len(R),len(c),"eng",sum(x["eng"] for x in R))
print([w for w in c if w[0].isupper()])
random.seed(21); smp=random.sample(R,40)
json.dump(R,open("rn2.json","w"),ensure_ascii=False); json.dump(smp,open("rn2-sample.json","w"),ensure_ascii=False)
