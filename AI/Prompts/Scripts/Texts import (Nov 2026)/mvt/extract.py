"""Extract lines from the Dyczkowski Malinivijayottara PDFs (f1, f2: ScaGoudy/KrutiDev glyph-id text layers; f3: Gentium + OCR layer).
Output: work/<f>.lines.json : [{page, col, y, x0, x1, size, segs:[[style,text]], raw}]
style: R roman, I italic, B bold, K devanagari (legacy, undecoded), S superscript (footnote call), F footnote-size roman, FI footnote italic, O other
"""
import pymupdf, json, sys, re, collections
BAL = {'ä':'ā','é':'ī','ü':'ū','å':'ṛ','è':'ṝ','ì':'ṅ','ï':'ñ','ö':'ṭ','ò':'ḍ','ë':'ṇ','ç':'ś','ñ':'ṣ','à':'ṁ','ù':'ḥ','ÿ':'ḷ','ß':'Ḷ',
       'Ä':'Ā','É':'Ī','Ü':'Ū','Å':'Ṛ','È':'Ṝ','Ì':'Ṅ','Ï':'Ñ','Ö':'Ṭ','Ò':'Ḍ','Ë':'Ṇ','Ç':'Ś','Ñ':'Ṣ','À':'Ṁ','Ù':'Ḥ','Ÿ':'Ḷ'}
# glyph-id text: low range gid = code-29; high range per font (roman, italic), found from contexts and checked on the page images
HI_R = {0x96:'Ṁ',0x9a:'Ā',0x9b:'Ṛ',0x9d:'Ś',0x9f:'Ī',0xa1:'Ṇ',0xa2:'Ṅ',0xa7:'Ṣ',0xa8:'Ḍ',0xac:'Ṭ',0xaf:'Ḥ',0xb1:'Ū',0xb5:'ṁ',0xb8:'ā',0xb9:'ṛ',0xbb:'ś',0xbd:'ī',0xbe:'ṇ',0xbf:'ṅ',0xc1:'ñ',0xc3:'ṣ',0xc4:'ḍ',0xc8:'ṭ',0xcb:'ḥ',0xce:'ū',
        0x6c:'‘',0x6d:'’',0x6e:'“',0x6f:'”'}
HI_I = {0x95:'Ṁ',0x99:'Ā',0x9a:'Ṛ',0x9c:'Ś',0x9e:'Ī',0xa0:'Ṇ',0xa6:'Ṣ',0xab:'Ṭ',0xae:'Ḥ',0xb0:'Ū',0xb3:'Ḷ',0xb4:'ṁ',0xb7:'ā',0xb8:'ṛ',0xba:'ś',0xbc:'ī',0xbd:'ṇ',0xbe:'ṅ',0xc0:'ñ',0xc2:'ṣ',0xc3:'ḍ',0xc6:'ṭ',0xc9:'ḥ',0xcc:'ū',0xcf:'ḷ',
        0x6c:'‘',0x6d:'’',0x6e:'“',0x6f:'”',0x71:'–',0x72:'—',0x63:'ƒ'}
HI_R.update({0x70:'•',0x71:'–',0x72:'—',0x73:'˜'})
UNK = collections.Counter()
def dec_shift(t, hi, tag):
    out=[]
    for i,c in enumerate(t):
        o=ord(c)
        if o==0x20: out.append('=' if (0<i<len(t)-1 and t[i-1]=='\x03' and t[i+1]=='\x03') else ' ')
        elif o>0xff: out.append(c)
        elif o in hi: out.append(hi[o])
        elif o+29 < 0x7f: out.append(chr(o+29))
        else:
            UNK[(tag,o)]+=1; out.append('�%02x;'%o)
    return ''.join(out)
def dec_plain(t):
    t=t.replace('\x03',' ')
    t=t.replace('\u02c6','^')
    if re.search(r'[a-w][\^`]|[\^`][a-w]',t):      # capitals typed in a font whose ASCII sits 29 places up (one place: VAJRINE VAJRADHARĀYA, 3.61-64)
        t=''.join(chr(ord(c)-29) if 0x3d<=ord(c)<=0x7a else ('Ä' if c=='ò' else c) for c in t)
    return ''.join(BAL.get(c,c) for c in t)
DESP=[False]
def is_shift(t):
    if any(ord(c)<0x20 and ord(c)!=3 for c in t): return True
    if any(0xe0<=ord(c)<=0xff for c in t): return False
    if sum(c in 'abdefghijkptuvwxyz' for c in t)>=1: return False
    if re.match(r'\s*\d{1,3}\.\s',t): return False
    L=[c for c in t if c.isalpha() and ord(c)<128]
    if len(L)>=3:
        low=sum(1 for c in L if c.islower())
        return None if 0.2<low/len(L)<0.4 else (low/len(L)<0.2)
    return None
def despace(l):
    chars=[(c,s) for s in l['spans'] for c in s['chars']]
    vis=[(c,s) for c,s in chars if c['c'] not in ' \x03']
    if len(vis)<6 or len(chars)-len(vis) < 0.42*len(chars): return
    gaps=sorted(b[0]['bbox'][0]-a[0]['bbox'][2] for a,b in zip(vis,vis[1:]))
    med=gaps[len(gaps)//2]
    if med<0.6: return   # ordinary line with many spaces
    thr=med*1.75+0.8
    for s in l['spans']: s['text']=''
    prev=None
    for c,s in vis:
        if prev is not None and c['bbox'][0]-prev['bbox'][2]>thr: s['text']+='\x03'
        s['text']+=c['c']; prev=c
    l['spans'][-1]['text']+='\x03'
    return True
def regap(l):
    """Gentium pages (f3): a justified, letter-spaced line may carry no space characters at all, or one after every letter;
    its words are then found from the gaps between glyphs."""
    chars=[(c,s) for s in l['spans'] for c in s['chars']]
    if not chars or not all(s['font'].startswith('GentiumBookPlus') for c,s in chars): return
    vis=[(c,s) for c,s in chars if c['c'].strip()]
    txt=''.join(c['c'] for c,s in chars); nsp=len(chars)-len(vis)
    if len(vis)<4 or any(s['size']<7.2 for c,s in vis): return
    singles=[w for w in txt.split() if len(w)==1 and w.islower() and w!='a']
    if not ((len(vis)>=14 and nsp<len(vis)/14) or nsp>=0.42*len(chars) or len(singles)>=1): return
    gaps=sorted(b[0]['bbox'][0]-a[0]['bbox'][2] for a,b in zip(vis,vis[1:]))
    med=gaps[len(gaps)//2]; thr=med+1.4
    for s in l['spans']: s['text']=''
    prev=None
    for c,s in vis:
        if prev is not None and c['bbox'][0]-prev['bbox'][2]>thr: s['text']+=' '
        s['text']+=c['c']; prev=c
    l['spans'][-1]['text']+=' '
    for s in l['spans']: s['chars']=[]
def run(n):
    d=pymupdf.open(f'src/{n}.pdf'); out=[]
    for pn,p in enumerate(d,1):
        W=p.rect.width; mid=W/2
        pv=collections.defaultdict(list)
        for b in p.get_text('rawdict')['blocks']:
            for l in b.get('lines',[]):
                for sp in l['spans']:
                    if sp['font'].startswith('ScaGoudy'):
                        m=is_shift(''.join(c['c'] for c in sp['chars']))
                        if m is not None: pv[sp['font']].append(m)
        pmaj={f:(sum(v)*2>=len(v)) for f,v in pv.items()}
        for b in p.get_text('rawdict')['blocks']:
            for l in b.get('lines',[]):
                for s in l['spans']: s['text']=''.join(c['c'] for c in s['chars'])
                regap(l)
                DESP[0]=bool(despace(l))
                spans=[s for s in l['spans'] if s['text']]
                if not spans: continue
                # decide shift mode per span, ambiguous ones follow the line majority
                modes=[]
                for s in spans:
                    f=s['font']
                    modes.append(is_shift(s['text']) if f.startswith('ScaGoudy') else None)
                votes=[m for m,sp in zip(modes,spans) if m is not None and 'Bold' not in sp['font']]
                maj = (sum(votes)*2>=len(votes)) if votes else is_shift(''.join(sp['text'] for sp in spans if sp['font'].startswith('ScaGoudy') and 'Bold' not in sp['font']))
                segs=[]; xs=[]
                for s,m in zip(spans,modes):
                    f=s['font']; t=s['text']; sz=s['size']
                    if sz<7.2:
                        dg=''.join(ch for ch in (dec_shift(t,{},'c') if any(ord(ch)<0x20 for ch in t) else t) if ch.isdigit())
                        if dg and not any(ch.isalpha() for ch in t):
                            segs.append(['S',dg]); xs.append([s['chars'][0]['bbox'][0]]*len(dg)); continue
                    if f=='KrutiDev010' or f=='Krishna': segs.append(['K',t]); xs.append([c['bbox'][0] for c in s['chars']] if len(s['chars'])==len(t) else [None]*len(t)); continue
                    if f.startswith('ScaGoudy'):
                        if m is None: m = (maj if maj is not None else pmaj.get(f,False)) if 'Bold' not in f else False
                        it = 'Italic' in f; bd='Bold' in f
                        txt = dec_shift(t, HI_I if it else HI_R, 'I' if it else ('B' if bd else 'R')) if m else dec_plain(t)
                        st = 'I' if it else ('B' if bd else 'R')
                    elif f.startswith('GentiumBookPlus'):
                        txt=t; st='I' if 'Ital' in f else ('B' if 'Bold' in f else 'R')
                        if 'BoldItal' in f: st='B'
                    elif f=='GlyphLessFont': txt=t; st='R'
                    else: txt=''.join(c if ord(c)>=0x20 else ' ' for c in t); st='O:'+f
                    if st in('R','I') and sz<7.2: st='S' if st=='R' else 'SI'
                    elif st in('R','I','B') and sz<9.2: st='F'+('' if st=='R' else st)
                    cx=[c['bbox'][0] for c in s['chars']] if len(s['chars'])==len(txt) else [None]*len(txt)
                    if segs and segs[-1][0]==st: segs[-1][1]+=txt; xs[-1]+=cx
                    else: segs.append([st,txt]); xs.append(cx)
                for sg in segs:       # the same repair on the joined run (the PDF may store such a word in pieces)
                    if sg[0] in('B','R','I') and re.search(r'[a-w][\^`][a-w]',sg[1]) and not re.search(r'[A-Z]{2}',sg[1]):
                        sg[1]=''.join(chr(ord(c)-29) if 0x3d<=ord(c)<=0x7a else ('Ā' if c=='ḍ' else c) for c in sg[1])
                x0,y0,x1,y1=l['bbox']
                out.append(dict(page=pn,x0=round(x0,1),x1=round(x1,1),y=round(y0,1),y1=round(y1,1),size=round(max(s['size'] for s in spans),1),segs=segs,xs=[[None if v is None else round(v,1) for v in a] for a in xs]))
    json.dump(out,open(f'work/{n}.lines.json','w'),ensure_ascii=False)
    return out
if __name__=='__main__':
    import os; os.makedirs('work',exist_ok=True)
    for n in sys.argv[1:]:
        o=run(n); print(n,len(o),'lines')
    print('UNKNOWN', sorted(UNK.items(), key=lambda x:-x[1]))
