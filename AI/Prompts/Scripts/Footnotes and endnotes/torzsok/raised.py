# Raised-ink test on the page image: is the tail of a word (the call) printed above the word's baseline?
import pymupdf,statistics as st
DPI=300; Z=DPI/72
class Img:
    def __init__(s,doc,i):
        s.p=doc[i].get_pixmap(matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csGRAY,alpha=False); s.W=s.p.width; s.H=s.p.height; s.b=s.p.samples
    def col(s,x,ya,yb):
        """(top,bottom) of dark pixels in column x between ya and yb, or None"""
        top=bot=None
        for y in range(max(0,ya),min(s.H,yb)):
            if s.b[y*s.W+x]<120:
                if top is None: top=y
                bot=y
        return (top,bot) if top is not None else None
    def region(s,x0,x1,ya,yb):
        out=[]
        for x in range(max(0,int(x0*Z)),min(s.W,int(x1*Z))):
            c=s.col(x,int(ya*Z),int(yb*Z))
            if c: out.append(c)
        return out
def raised(img,w,nlet,njunk,ntrail):
    """w: layer word (x,x1,y0,y1); nlet/njunk/ntrail: char counts of letters part, call part, trailing punctuation.
    Returns (verdict, detail): verdict True if the call part's ink lies above the letters' baseline."""
    n=nlet+njunk+ntrail; cw=(w['x1']-w['x'])/max(n,1)
    xs=w['x']+cw*nlet; xe=w['x']+cw*(nlet+njunk)
    ya=w['y0']-2; yb=w['y1']+2
    let=img.region(max(w['x'],xs-cw*4),xs-cw*0.3,ya,yb)
    jun=img.region(xs+cw*0.1,xe+cw*0.2,ya,yb)
    if len(let)<3 or len(jun)<2: return None,'no ink'
    base=st.median([b for t,b in let]); top=min(t for t,b in let)
    h=max(base-top,1)
    jlow=st.median(sorted(b for t,b in jun)[-max(1,len(jun)//2):])   # lower half of the call's columns
    jtop=min(t for t,b in jun)
    return (base-jlow)>0.22*h, f'base {base} top {top} jlow {jlow} jtop {jtop} rise {(base-jlow)/h:.2f}'

def raised_cols(img,w,nlet,ncall,ntrail,prevw=None):
    """Fraction of ink columns in the call part whose lowest ink lies clearly above the baseline of the letters
    before it (the word's own letters, or the previous word for a lone number). Returns (ok, fraction)."""
    n=nlet+ncall+ntrail; cw=(w['x1']-w['x'])/max(n,1)
    ya=w['y0']-2; yb=w['y1']+2
    if nlet:
        xs=w['x']+cw*nlet; xe=w['x']+cw*(nlet+ncall)
        let=img.region(max(w['x'],xs-cw*4),xs-cw*0.4,ya,yb)
        jun=img.region(xs-cw*0.6,xe+cw*0.3,ya,yb)     # a little into the last letter: catches ')2' read as '}'
    else:
        if not prevw: return False,0,None
        pcw=(prevw['x1']-prevw['x'])/max(len(prevw['t']),1)
        let=img.region(prevw['x1']-pcw*4,prevw['x1']-pcw*0.5,ya,yb)
        jun=img.region(w['x'],w['x']+cw*ncall,ya,yb)
    if len(let)<3 or len(jun)<2: return False,0,None
    base=st.median([b for t,b in let]); top=st.median([t for t,b in let])
    h=max(base-top,1)
    up=[1 for t,b in jun if base-b>0.25*h]
    frac=len(up)/len(jun)
    # height of the call's ink against the letters' full height (ascender to baseline): a superscript is smaller
    hr=(max(b for t,b in jun)-min(t for t,b in jun))/max(base-min(t for t,b in let),1)
    return frac>=0.3, round(frac,2), round(hr,2)
