"""For the page readers: what the notes say, laid out per PDF page (work/pages/<file>-p<NN>.txt)."""
import sys,os,re,io,contextlib,collections
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    import build_all as B
from build_all import *
import ch7
os.makedirs('work/pages',exist_ok=True)
P=collections.defaultdict(list)
def clean(t): 
    t=re.sub(CO+r'\d+:(\d+)'+CC,r'[\1]',t); return md(unital(t))
for ch in sorted(B.CH):
    D=ch7.data() if ch==7 else build(B.CH[ch],ch,ends=B.ENDS.get(ch))
    key=lambda vp:(D['segs'][vp//1000][0],vp%1000)
    for v,d in sorted(D['verses'].items()):
        pg=D['spage'].get(v)
        if pg and any(x.strip() for x in d['iast']):
            P[key(pg)].append((0,v,f'VERSE {ch}.{v} transliteration: '+' | '.join(clean(x.lower().replace("ƒ","ḥ")) for x in d['iast'])+(' ; extra lines after it: '+' '.join(clean(x) for x in d['extra']) if d['extra'] else '')))
    for u in D['units']:
        r=u['ref']; lab=(f'{r[0]}{r[1]}'+(f'-{r[2]}{r[3]}' if (r[2]!=r[0] or r[3]) else '')) if r else 'none'
        P[key(u['page'])].append((1,r[0] if r else 999,f'TRANSLATION for {ch}.{lab}'+(' [reference supplied by the importer]' if u.get('inferred') else '')+(f' [heading before it: {" / ".join(u["heads"])}]' if u['heads'] else '')+':\n'+clean(u['text'])))
    for (pg,num),t in D['fn'].items():
        P[key(pg)].append((2,int(num),f'FOOTNOTE {num}: '+clean(t)))
for (n,pg),L in P.items():
    L.sort(key=lambda x:(x[0],x[1]))
    open(f'work/pages/{n}-p{pg:02d}.txt','w').write('\n\n'.join(x[2] for x in L)+'\n')
print(len(P),'page files', sorted(collections.Counter(n for n,_ in P).items()))
