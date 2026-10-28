# Lists every [illegible] run in the library copy of Dyczkowski's Tantraloka with its note, PDF page and context.
import os,re,json,glob,collections
IL=re.compile(r"\\\[illegible\\\](?: \\\[illegible\\\])*")
MK=re.compile(r"\*\[p\. [^\]]*\]\* \^pg(\d+)")
items=[]
for p in sorted(glob.glob("notes/lib/*/*.md")):
    rel=p[len("notes/lib/"):]
    t=open(p,encoding="utf-8").read()
    m=re.search(r" v(\d\d) \d\d - ",p)
    if not m: continue
    v=int(m.group(1))
    mks=[(mm.start(),int(mm.group(1))) for mm in MK.finditer(t)]
    for m in IL.finditer(t):
        ks=[K for s0,K in mks if s0<m.start()]
        nxt=[K for s0,K in mks if s0>m.end()]
        ls=t.rfind("\n",0,m.start())+1; le=t.find("\n",m.end()); le=len(t) if le<0 else le
        items.append({"id":len(items),"note":rel,"v":v,"K":ks[-1] if ks else None,"Knext":nxt[0] if nxt else None,
                      "s":m.start(),"e":m.end(),"k":m.group(0).count("illegible"),"line":t[ls:le],"ls":ls})
json.dump(items,open("items.json","w"),ensure_ascii=False)
c=collections.Counter(i["v"] for i in items); print(len(items),"runs",sum(i["k"] for i in items),"placeholders",dict(sorted(c.items())))
pages={(i["v"],i["K"]) for i in items if i["K"]}
print("pages",len(pages),"no page",sum(1 for i in items if not i["K"]))
json.dump(sorted(pages),open("pages.json","w"))
