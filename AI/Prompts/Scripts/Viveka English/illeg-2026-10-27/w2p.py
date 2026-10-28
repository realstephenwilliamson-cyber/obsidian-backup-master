# Witnesses 2 and 3 (parallel): each placed gap re-read from crops of its word boxes, Tesseract Latin model, one line:
# "ocr" at 600 dpi with no dictionary, "ocr3" at 450 dpi with the dictionary. Results merged into w2.json.
import json,sys,os,subprocess,pymupdf as fitz
from multiprocessing import Pool
import unicodedata
NFC=lambda s: unicodedata.normalize("NFC",s)
items={i["id"]:i for i in json.load(open("items.json"))}
DOCS={}
def one(x):
    r=x["r"]
    if len(r["lines"])!=1: return x["id"],{"why":"spans lines"}
    v=items[x["id"]]["v"]
    if v not in DOCS: DOCS[v]=fitz.open(f"pdfs/Dyczkowski - Tantraloka, vol. {v:02d}.pdf")
    x0,y0,x1,y1=r["box"]; s=72/400
    rect=fitz.Rect((x0-10)*s,(y0-8)*s,(x1+10)*s,(y1+8)*s); res={}
    for tag,dpi,extra in (("ocr",600,["-c","load_system_dawg=0","-c","load_freq_dawg=0"]),("ocr3",450,[])):
        pix=DOCS[v][r["K"]-1].get_pixmap(dpi=dpi,clip=rect,colorspace=fitz.csGRAY)
        fn=f"crops/{tag}-{x['id']:05d}.png"; pix.save(fn)
        res[tag]=NFC(subprocess.run(["tesseract",fn,"-","-l","Latin","--psm","7"]+extra,capture_output=True,text=True,env=dict(os.environ,OMP_THREAD_LIMIT="1")).stdout.strip())
        os.remove(fn)
    return x["id"],res
OUTF=sys.argv[2] if len(sys.argv)>2 else "w2.json"
if __name__=="__main__":
    P=json.load(open(sys.argv[1])); out=json.load(open(OUTF)) if os.path.exists(OUTF) else {}
    todo=[x for x in P if x["why"]=="ok" and not (str(x["id"]) in out and ("ocr3" in out[str(x["id"])] or "why" in out[str(x["id"])]))]
    print("to do",len(todo),flush=True)
    with Pool(2) as pool:
        for n,(i,res) in enumerate(pool.imap_unordered(one,todo,chunksize=8)):
            out[str(i)]=res
            if n%200==0: json.dump(out,open(OUTF,"w"),ensure_ascii=False); print(n,flush=True)
    json.dump(out,open(OUTF,"w"),ensure_ascii=False); print("done",len(out),flush=True)
