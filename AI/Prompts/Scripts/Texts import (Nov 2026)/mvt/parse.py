"""Parse the ordered lines of the Dyczkowski Malinivijayottara PDFs into chapters:
headings, Sanskrit (IAST) lines, translation paragraphs with their verse references, footnotes, printed pages.
The Sanskrit lines are recognised and cut into verses by aligning them with the KSTS text (Muktabodha M00160)."""
import json,re,sys,difflib,unicodedata,collections
sys.path.insert(0,'scripts')
from order import ordered
CO,CC='',''      # footnote call brackets inside text
IO,IC='',''      # italic on/off
MK=json.load(open('work/mk.json'))
STOP=set('the of and is to in that by with which who are as it this be from for on one should has have his or an at was not were said called then there thus all these those he she they its their you also when what how if into will been but great seers'.split())
REF=re.compile(r'\(\s*(\d+)\s*([a-f]{0,3})\s*(?:[-–—]\s*(\d*)\s*([a-f]{0,3})\s*)?\)')
def norm(s):
    s=unicodedata.normalize('NFC',s.lower()).replace('ṁ','ṃ').replace('ƒ','ḥ')
    s=re.sub(CO+r'[\d:]+'+CC,'',s)
    s=re.sub(r'[ṅñṇnmṃ]','n',s)
    return re.sub(r'[^a-zāīūṛṝḷḹśṣṭḍḥ]','',s)
def grams(s,n=5): return {s[i:i+n] for i in range(len(s)-n+1)}
def linetext(l, italics=True):
    out=[]
    for st,t in l['segs']:
        if st=='K': continue
        if st=='S': out.append(CO+str(l['page'])+':'+re.sub(r'\D','',t)+CC); continue
        if italics and st in('I','FI','SI'): out.append(IO+t+IC)
        else: out.append(t)
    return ''.join(out)
def plain(l): return ''.join(t for st,t in l['segs'] if st not in('K','S'))
def insert_calls(lines):
    """call lines (all segs 'S') are put into the body line they sit on"""
    body=[l for l in lines if not all(s[0]=='S' for s in l['segs'])]
    for c in lines:
        if not all(s[0]=='S' for s in c['segs']): continue
        num=''.join(s[1] for s in c['segs']); cx=c['x0']
        host=None;best=1e9
        for l in body:
            if l['page']!=c['page'] or l.get('foot'): continue
            if l['x0']-6<=cx<=l['x1']+12 and l['y']-9<=c['y']<=l['y1']-2:
                d=abs(c['y']-l['y'])
                if d<best: best=d;host=l
        if host is None: c['orphan']=True; continue
        # position by character x
        done=False
        for si,(seg,xs) in enumerate(zip(host['segs'],host['xs'])):
            for i,x in enumerate(xs):
                if x is not None and x>cx+0.5:
                    t=seg[1]
                    # do not split a word: move to the previous position if inside letters
                    host['segs'][si:si+1]=[[seg[0],t[:i]],['S',num],[seg[0],t[i:]]]
                    host['xs'][si:si+1]=[xs[:i],[cx]*len(num),xs[i:]]
                    done=True;break
            if done:break
        if not done:
            host['segs'].append(['S',num]); host['xs'].append([cx]*len(num))
    return [l for l in body]
def dehyph(a,b):
    return _dehyph(a,b)
def footnotes(lines, pageH):
    """split off the footnote zone of each page; returns body lines and {page: [(num, text)], cont: text}"""
    bypage=collections.defaultdict(list)
    for l in lines: bypage[l['page']].append(l)
    body=[]; notes={}
    for pg,L in bypage.items():
        fl=[]
        Fy=[l['y'] for l in L if any(x[0].startswith('F') for x in l['segs'])]
        for l in L:
            segs=[x for x in l['segs'] if x[1].strip()]
            if segs and not l['foot'] and re.match(r'^\s*\d+\s*\.?\s*$',plain(l)) and not all(x[0]=='S' for x in segs) and any(abs(l['y']-y)<4.5 for y in Fy):
                fl.append(l); continue
            isF = bool(segs) and all(x[0].startswith('F') or x[0]=='S' for x in segs) and any(x[0].startswith('F') for x in segs)
            if isF and not l['foot']: fl.append(l)
            else: body.append(l)
        fl.sort(key=lambda l:(round(l['y']/3),l['x0']))
        items=[];cont=[]
        for l in fl:
            t=linetext(l)
            m=re.match(r'\s*(\d+)\s*\.\s*(.*)',t,re.S) or (re.match(r'\s*(\d+)\s*()$',t) if not l['segs'][0][0].startswith('F') else None)
            if m: items.append([m.group(1),m.group(2)])
            elif items: items[-1][1]=dehyph(items[-1][1],t) if items[-1][1] else t
            else: cont.append(t)
        notes[pg]=dict(items=items,cont=' '.join(cont))
    return body,notes
def md(t):
    """internal marks -> markdown: italics and calls"""
    t=t.replace(IC+IO,'').replace(IC+' '+IO,' ')
    t=re.sub(IO+r'(\s*)([^'+IC+r']*?)(\s*)'+IC, lambda m: m.group(1)+('*'+m.group(2)+'*' if m.group(2).strip() else m.group(2))+m.group(3), t)
    t=re.sub(CO+r'\d+:(\d+)'+CC,r'[^\1]',t)
    t=re.sub(r'[ \t]+',' ',t)
    t=re.sub(r'\s+([,.;:)])',r'\1',t)
    t=re.sub(r'(?<=[^\s(])\s+(\[\^\d)',r'\1',t)
    t=t.replace('( ','(')
    return t.strip()
def _dehyph(a,b):
    """join two lines of running prose"""
    a=a.rstrip(); b=b.lstrip()
    m=re.search(r'([A-Za-zāīūṛṝḷśṣṭḍṇṅñṁḥ]+)-(['+IC+']?)$',a)
    if m and re.match('['+IO+']?[a-zāīūṛśṣṭḍṇṅñ]',b):
        keep = m.group(1).lower() in ('non','self','well','all','so','semi','sub','pre','post','re','co','half','ten','one','two','three','four','five','six','seven','eight','nine','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety','world','mantra','sub')
        return (a if keep else a[:m.start()]+m.group(1)+m.group(2))+b
    return a+' '+b
def parse_chapter(segs, ch, bold_is_head=False, starts=None, ends=None):
    """segs: [(file, first page, last page)]; pages of the k-th segment are numbered 1000*k + page"""
    L=[]
    for k,(n,p0,p1) in enumerate(segs):
        for l in ordered(n):
            if p0<=l['page']<=p1:
                l=dict(l); l['n']=n; l['rp']=l['page']; l['page']=1000*k+l['page']; l['pageH']=720 if n=='f1' else 648; L.append(l)
    foots={l['page']:[] for l in L}
    for l in L:
        if l['foot']: foots[l['page']].append(plain(l).strip())
    if starts:
        keep=[];on={k:(k not in starts) for k in range(len(segs))}
        for l in L:
            k=l['page']//1000
            if not on[k] and re.search(starts[k],plain(l)): on[k]=True; l['start']=True
            if on[k] or l['foot'] or all(x[0].startswith('F') for x in l['segs'] if x[1].strip()): keep.append(l)
        L=keep
    if ends:
        keep=[];off={k:False for k in range(len(segs))}
        for l in L:
            k=l['page']//1000
            if k in ends and not off[k] and re.search(ends[k],plain(l)): off[k]=True
            if not off[k] or l['foot']: keep.append(l)
        L=keep
    L=insert_calls(L)
    L,notes=footnotes(L,0)
    L=[l for l in L if not l['foot']]
    mkch=MK[str(ch)]; mktext=norm(' '.join(' '.join(h) for v,h in mkch['verses'])+' '+mkch['rest']); G=grams(mktext)
    items=[]; state='E'
    colleft={};colright={}
    for l in L:
        if l['segs'][0][0]!='K' and plain(l).strip():
            k=(l['page'],l['col'],l.get('full',False)); colleft[k]=min(colleft.get(k,1e9),l['x0']); colright[k]=max(colright.get(k,0),l['x1'])
    for l in L:
        t=plain(l); st=[s[0] for s in l['segs'] if s[1].strip()]; extra=False
        if not st: continue
        kchars=sum(len(s[1]) for s in l['segs'] if s[0]=='K'); 
        if kchars>len(t.strip()) and len(re.findall(r'[A-Za-zāīūṛśṣṭḍṇṅñṁḥ]',t))<3: kind='K'
        elif all(x=='S' for x in st): continue
        elif (all(x[0] in 'BO' for x in st if x!='S') and (l['size']>=12.5 or bold_is_head)): kind='H'
        else:
            tc=' '.join(x for x in re.sub(r'[/|_।॥]+',' ',t).split() if not re.match(r'^(\d+|\d*L+\d*L*)$',x))
            nt=norm(tc); g=grams(nt)
            score=len(g&G)/len(g) if g else (1.0 if (nt and nt in mktext and state in('K','S')) else 0.0)
            eng = bool(re.search(r'[,;:()“”"‘’!?]|\.\s*$|\.\s',t)) or any(w in STOP for w in re.findall(r"[^\W\d_]+",t.lower()))
            extra=False
            allb=all(x[0] in 'BO' for x in st if x!='S')
            if allb: kind='E'
            elif state in('K','S'):
                asc=re.findall(r'[A-Za-z]+',t); eng = eng or (score<0.3 and len(t.split())>=3 and len(asc)==len(t.split()) and t.strip()[0].isupper())
                lets=[c for c in t if c.isalpha()]
                if lets and sum(c.isupper() for c in lets)>0.7*len(lets) and len(lets)>5: eng=True
                kind='E' if eng else 'S'
                extra = kind=='S' and score<0.5 and len(nt)>=5
                if kind=='S' and len(nt)<5 and nt and nt not in mktext: extra=True
            else:
                lets=[c for c in t if c.isalpha()]
                if lets and sum(c.isupper() for c in lets)>0.7*len(lets) and len(lets)>5: eng=True
                kind='S' if (score>=0.6 and not eng) else 'E'
        state=kind if kind!='H' else state
        items.append(dict(kind=kind,score=(score if kind in('S','E') else 0),extra=(kind=='S' and extra),page=l['page'],line=l,rgap=colright.get((l['page'],l['col'],l.get('full',False)),l['x1'])-l['x1'],indent=l['x0']-colleft.get((l['page'],l['col'],l.get('full',False)),l['x0'])))
    # a weakly matched line between two unmatched Sanskrit lines belongs to the unmatched passage
    S=[it for it in items if it['kind']=='S']
    for a,b,c in zip(S,S[1:],S[2:]):
        if a['extra'] and c['extra'] and b['score']<0.8: b['extra']=True
    for a,b in zip(S,S[1:]):
        if a['extra'] and not b['extra'] and b['score']<0.8 and len(norm(plain(b['line'])))<22 and b is S[S.index(b)] and (S.index(b)+1==len(S) or items[items.index(b)+1]['kind']!='S'): b['extra']=True
    return items,notes,foots
if __name__=='__main__':
    n,ch,p0,p1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
    items,notes,foots=parse_chapter([(n,p0,p1)],ch, bold_is_head=(n=='f3'))
    for it in items:
        print(it['page'],it['kind'],'%3d'%it['indent'],md(linetext(it['line']))[:120] if it['kind']!='K' else '')
