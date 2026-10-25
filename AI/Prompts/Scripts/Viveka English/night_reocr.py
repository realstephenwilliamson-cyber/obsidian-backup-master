# Night pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof5/lib-bundle.json).
# Needs pymupdf, the wamerican-large/wbritish-large word lists and tesseract-ocr-script-latn (the Latin-script model).
# Re-OCR each matched placeholder gap with Tesseract's Latin-script model (IAST diacritics), on a 4x crop of the gap's word boxes.
import sys,json,re,collections,subprocess,os,io,unicodedata
sys.path.insert(0,"/home/claude/pf")
from slips_common import T,tok,ENGL,P,L
import crops, pymupdf as fitz
from PIL import Image
NFC=lambda s: unicodedata.normalize("NFC",s)
res=json.load(open(sys.argv[1])); outp=sys.argv[2]; lim=int(sys.argv[3]) if len(sys.argv)>3 else None
os.makedirs("/home/claude/p4/gap",exist_ok=True)
out=[]
for n,(it,r) in enumerate(res[:lim]):
    p,v,K,s,e,k=it; ws=crops.words(v,r["page"]); g=ws[r["j"]:r["j"]+r["g"]]
    if len({(w[5],w[6]) for w in g})>1: out.append({"it":it,"ocr":None,"why":"spans lines"}); continue
    x0=min(w[0] for w in g)-3; x1=max(w[2] for w in g)+3; y0=min(w[1] for w in g)-3; y1=max(w[3] for w in g)+3
    pg=crops.doc(v)[r["page"]]; pix=pg.get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(x0,y0,x1,y1))
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples).convert("L")
    fn=f"/home/claude/p4/gap/g{n:05d}.png"; im.save(fn)
    o=subprocess.run(["tesseract",fn,"-","-l","Latin","--psm","7"],capture_output=True,text=True,env=dict(os.environ,OMP_THREAD_LIMIT="1")).stdout.strip()
    out.append({"it":it,"ocr":NFC(o),"box":[v,r["page"],x0,y0,x1,y1],"png":fn})
json.dump(out,open(outp,"w"),ensure_ascii=False)
print(len(out))
