"""Running prose (introductions) from parsed lines -> markdown with headings, page marks and footnotes."""
import re,sys
sys.path.insert(0,'scripts')
from parse import *
from render import issue_of,fnkey
def prose(items,D,skip_heads=()):
    out=[];para=[];pb=None;lastpage=None;bullet=False;used=[]
    def fl():
        nonlocal para,pb,bullet
        if not para: return
        t=para[0][1]
        for _,x in para[1:]: t=dehyph(t,x)
        pg=para[0][0]
        tp=re.sub(CO+r'[\d:]+'+CC,'',t.replace(IO,'').replace(IC,'')).strip()
        if pb and len(tp)<110 and not re.search(r'[,;]$',tp):
            if tp not in skip_heads and not re.match(r'(\[?\.\.\. ?continued|[–—-] *(Rajanaka )?Mark Dyczkowski)',tp): out.append(('h',pg,md(tp)))
        else: out.append(('b' if bullet else 'p',pg,t))
        para=[];pb=None;bullet=False
    for it in items:
        l=it['line']; segs=[x for x in l['segs'] if x[1].strip()]
        if not segs: continue
        if all(x[0].startswith('O:') and 'Dingbat' in x[0] for x in segs) or plain(l).strip() in('l','•'):
            fl(); bullet=True; continue
        if it['kind']=='K': fl(); out.append(('p',it['page'],'*[Devanagari in the print]*')); continue
        lb=all(x[0][0] in 'BSO' for x in segs) or it['kind']=='H'
        if para and (lb!=pb or it['indent']>10): 
            keep=bullet and not para
            fl()
        if not para: pb=lb
        para.append((it['page'],linetext(l)))
    fl()
    L=[];keys=[]
    def rc(t):
        def rep(m):
            k=fnkey(D,int(m.group(1)),m.group(2))
            if k is None: return ''
            if k not in keys: keys.append(k)
            return CO+f'{k[0]}:{k[1]}'+CC
        return re.sub(CO+r'(\d+):(\d+)'+CC,rep,t)
    for kind,pg,t in out:
        if pg!=lastpage:
            iss,pp=issue_of(D['foots'],pg); lastpage=pg
            L+=[f'*[p. {pp}]*' if pp else f'*[PDF page {pg%1000}]*','']
        if kind=='h': L+=['## '+t,'']
        else: L+=[('- ' if kind=='b' else '')+md(rc(t)).replace('\n',' '),'']
    body='\n'.join(L)
    nums=[k[1] for k in keys]
    lab=lambda k: k[1] if nums.count(k[1])==1 else f'{k[1]}-p{k[0]%1000}'
    body=re.sub(r'\[\^(\d+)\]',lambda m:m.group(0),body)
    # md() already turned marks into [^num]; relabel duplicates is rare, so definitions follow the printed numbers
    defs=[f'[^{k[1]}]: '+md(re.sub(CO+r'[\d:]+'+CC,'',D['fn'][k])) for k in keys if nums.index(k[1])==keys.index(k)]
    return body+'\n'+'\n'.join(defs)+'\n'
