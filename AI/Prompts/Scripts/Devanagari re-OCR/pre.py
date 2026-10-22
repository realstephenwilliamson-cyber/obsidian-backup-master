import json,sys,re
import pymupdf as fitz
sys.path.insert(0,'.')
V='/mnt/user-data/uploads/Obsidian Vault/'
def stats(fn):
    doc=fitz.open(fn); I=J=inj=0
    for pg in doc:
        t=pg.get_text()
        for m in re.finditer('\u093f(.)',t):
            I+=1;c=m.group(1)
            if not('\u0900'<=c<='\u097f' or c in ' \n.,;:-|\u0964\u0965()'):J+=1
    return len(doc),I,J
for b in ['b2','b3']:
    for dev in json.load(open(f'/home/claude/d09/{b}.json')):
        rel=dev.replace('C:\\Vaults\\Obsidian Vault\\','').replace('\\','/')
        try: n,I,J=stats(V+rel); print(b,n,I,J,rel.split('/')[-1][:70],flush=True)
        except Exception as e: print(b,'ERR',e,rel)
