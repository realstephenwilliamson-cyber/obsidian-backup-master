# Whole-page OCR of every PDF page that holds an [illegible] run, with Tesseract's Latin-script model at 400 dpi (TSV with word boxes).
import json,os,subprocess,sys,pymupdf as fitz
from multiprocessing import Pool
pages=[tuple(p) for p in json.load(open("pages.json"))]
def one(vk):
    v,K=vk; base=f"ocr/v{v:02d}-p{K:04d}"
    if os.path.exists(base+".tsv"): return 0
    doc=fitz.open(f"pdfs/Dyczkowski - Tantraloka, vol. {v:02d}.pdf")
    if K-1>=doc.page_count: return 0
    pix=doc[K-1].get_pixmap(dpi=400,colorspace=fitz.csGRAY); fn=f"pages/v{v:02d}-p{K:04d}.png"; pix.save(fn)
    subprocess.run(["tesseract",fn,base,"-l","Latin","--psm","3","tsv"],capture_output=True,env=dict(os.environ,OMP_THREAD_LIMIT="1"))
    os.remove(fn); return 1
if __name__=="__main__":
    todo=[p for p in pages if p[0]!=1]+[p for p in pages if p[0]==1]
    with Pool(2) as pool:
        for n,r in enumerate(pool.imap(one,todo,chunksize=4)):
            if n%100==0: print(n,len(todo),flush=True)
    print("done",flush=True)
