import json
def ordered(n):
    """lines of file n in reading order: per page, bands split by full-width lines, left column then right"""
    L=json.load(open(f'work/{n}.lines.json'))
    import pymupdf
    d=pymupdf.open(f'src/{n}.pdf')
    out=[]
    for pn in range(1,len(d)+1):
        W=d[pn-1].rect.width; H=d[pn-1].rect.height; mid=W/2
        P=[l for l in L if l['page']==pn]
        for l in P:
            l['foot']= l['y']>H-62 and not any(x[0].startswith('F') for x in l['segs']); l['col']=0; l['full']=False
        # pieces of one printed line that the PDF stores as separate lines (letter-spaced words) are joined
        P.sort(key=lambda l:(l['foot'],round(l['y']),l['x0'])); Q=[]
        for l in P:
            p=Q[-1] if Q else None
            tiny=lambda z: all(s[0]=='S' for s in z['segs'])
            if p and not tiny(l) and not tiny(p) and p['foot']==l['foot'] and abs(p['y']-l['y'])<1.6 and -1.5<=l['x0']-p['x1']<14 and not (p['x1']<=mid+4 and l['x0']>=mid-4) and abs(p['size']-l['size'])<1.6:
                gap=l['x0']-p['x1']
                pt=''.join(s[1] for s in p['segs']); lt=''.join(s[1] for s in l['segs'])
                glue = '' if (p.get('bits',1)>=1 and len(lt.strip())<=2 and len((pt.strip().split() or ['xxxxxxxxxxxx'])[-1])<=p.get('bits',1)+1 and gap<5.5) else ' '
                if glue=='' : p['bits']=p.get('bits',1)+1
                if glue: p['segs'].append([l['segs'][0][0],' ']); p['xs'].append([None])
                p['segs']+=l['segs']; p['xs']+=l['xs']; p['x1']=max(p['x1'],l['x1']); p['y1']=max(p['y1'],l['y1'])
            else: Q.append(l)
        P=Q
        for l in P:
            l['full']= l['x0']<mid-25 and l['x1']>mid+25
            l['col']= 0 if l['full'] else (1 if (l['x0']+min(l['x1'],l['x0']+60))/2>mid-8 else 0)
        body=[l for l in P if not l['foot']]; foot=[l for l in P if l['foot']]
        fulls=sorted([l for l in body if l['full']],key=lambda l:l['y'])
        cuts=[-1]+[l['y'] for l in fulls]+[1e9]
        res=[]
        for i in range(len(cuts)-1):
            if i>0: res.append(fulls[i-1])
            band=[l for l in body if not l['full'] and cuts[i]<l['y']<cuts[i+1]]
            for c in (0,1):
                res+=sorted([l for l in band if l['col']==c],key=lambda l:(round(l['y']/3),l['x0']))
        out+=res+[dict(f,foot=True) for f in sorted(foot,key=lambda l:l['x0'])]
    return out
def txt(l): return ''.join(('⟦%s⟧'%s[0] if s[0] not in('R',) else '')+s[1] for s in l['segs'])
if __name__=='__main__':
    import sys
    n=sys.argv[1]; pages=set(int(x) for x in sys.argv[2].split(','))
    for l in ordered(n):
        if l['page'] in pages:
            print(l['page'],'F' if l.get('full') else l['col'],'%5.0f %4.0f'%(l['y'],l['x0']),l['size'],'FOOT' if l['foot'] else '', txt(l) if l['segs'][0][0]!='K' else '⟦K⟧…')
