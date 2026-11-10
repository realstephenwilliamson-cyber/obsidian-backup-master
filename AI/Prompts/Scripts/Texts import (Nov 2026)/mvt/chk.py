import sys,collections; sys.path.insert(0,'scripts')
from assemble import *
def chk(segs,ch,verbose=False,**kw):
    D=build(segs,ch,**kw); V=D['verses']
    print(f'== ch{ch} {segs}: verses',len(V),'dev',dict(collections.Counter(s for d in V.values() for s in d.get('devst',[]))))
    low=[(v,d['sim']) for v,d in V.items() if min(d['sim'])<0.9]
    print('  differ from KSTS:',len([v for v,d in V.items() if min(d['sim'])<0.999]),' weak (<0.9):',low[:40])
    print('  extras:',{v:[x[:50] for x in d['extra']] for v,d in V.items() if d['extra']})
    cov=collections.Counter(); nor=[]
    for u in D['units']:
        r=u['ref']
        if r:
            for v in range(r[0],r[2]+1): cov[v]+=1
        if u.get('inferred'): print('  inferred ref',r,md(u['text'])[:50])
        if not r: nor.append((u['page'],md(u['text'])[:60].replace('\n',' ')))
    print('  units',len(D['units']),'uncovered',[v for v in V if v not in cov],'refs outside',sorted(v for v in cov if v not in V))
    print('  no-ref units:',nor[:12]); print('  colophon',D['colophon'],'| footnotes',len(D['fn']))
    if verbose:
        for v,sim in low:
            for a,b in zip(V[v]['iast'],V[v]['ks']): print('    ',v,'D:',a[:110],'\n        K:',b[:110])
    return D
CH={1:[('f1',15,25)],2:[('f5',23,36),('f1',26,34)],3:[('f1',35,53)],4:[('f1',54,64)],5:[('f1',65,81)],6:[('f2',1,7),('f4',28,35)],8:[('f3',11,51)]}
ENDS={2:{0:'Moti Lal Pandit'}}
if __name__=='__main__':
    for c in sys.argv[1].split(','):
        c=int(c); D=chk(CH[c],c,verbose='-v' in sys.argv,ends=ENDS.get(c))
        print('  intro lines',len(D['intro']),'| first text lines:',[md(linetext(it['line']))[:40] for it in D['items'][:4] if it['kind']!='K'])
