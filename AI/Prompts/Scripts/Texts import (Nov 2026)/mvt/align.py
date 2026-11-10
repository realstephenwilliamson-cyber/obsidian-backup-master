import difflib,re
def cut(raw, refs, norm, snap=r'\s'):
    """raw: the print's running text; refs: reference pieces in order. Returns the piece of raw that lines up with each ref
    (cut at the nearest space), and the similarity of each."""
    idx=[]; pn=[]
    for i,ch in enumerate(raw):
        n=norm(ch)
        for c in n: pn.append(c); idx.append(i)
    pn=''.join(pn)
    rn=[norm(r) for r in refs]; R=''.join(rn)
    sm=difflib.SequenceMatcher(None,R,pn,autojunk=False)
    blocks=sm.get_matching_blocks()
    def r2p(i):
        prev=None
        for a,b,size in blocks:
            if a<=i<a+size: return b+(i-a)
            if a>i: 
                if prev is None: return b
                pa,pb,ps=prev
                return min(b, pb+ps+ (i-(pa+ps)))   # inside a gap: lean on the previous block
            prev=(a,b,size)
        return len(pn)
    cuts=[0]; pos=0
    for r in rn[:-1]:
        pos+=len(r); j=r2p(pos)
        rawj=idx[j] if j<len(idx) else len(raw)
        # snap to a space at or just before rawj (the boundary falls between words)
        k=rawj
        while k>cuts[-1] and not re.match(snap,raw[k-1]) and rawj-k<25: k-=1
        if rawj-k>=25 or k<=cuts[-1]:
            k=rawj
            while k<len(raw) and not re.match(snap,raw[k]) and k-rawj<25: k+=1
        cuts.append(k)
    cuts.append(len(raw))
    pieces=[raw[a:b].strip() for a,b in zip(cuts,cuts[1:])]
    sims=[difflib.SequenceMatcher(None,norm(p),r,autojunk=False).ratio() if r or norm(p) else 1.0 for p,r in zip(pieces,rn)]
    return pieces,sims
