import sys, re, pickle, glob, os, collections, unicodedata
sys.path.insert(0,'/home/claude/finn')
from mdpages import load
from pdfside import norm
P=load(); R=pickle.load(open('/home/claude/finn/R.pkl','rb'))
os.makedirs('/home/claude/finn/out',exist_ok=True)
report=collections.Counter(); wordiss=[]
for f in sorted(glob.glob('/home/claude/finn/md/The Kulacudamani Tantra [0-9]*.md')):
    L=open(f,encoding='utf-8').read().split('\n')
    pages=sorted([(v['start'],v['end'],k) for k,v in P.items() if v['file']==os.path.basename(f)])
    used=set(re.findall(r'\[\^([\w.-]+)\]', '\n'.join(L))); out=L[:pages[0][0]]
    for (a,b,K) in pages:
        r=R.get(K)
        sec=L[a:b]
        if not r or (not r['out_defs'] and not r['placed']):
            out+=sec; continue
        mk=sec[0]; pnum=re.match(r'^\*\[(?:p|PDF)\.? ([^\]]*)\]\*',mk).group(1)
        lab={}
        for n in sorted({int(x) for x in re.findall(r'\[\^@(\d+)\]', '\n'.join(r['out_body']+r['out_defs']))}):
            l=str(n) if str(n) not in used else f'{n}-p{pnum}'
            l=re.sub(r'[^\w.-]','',l); used.add(l); lab[n]=l
        fix=lambda t: re.sub(r'\[\^@(\d+)\]', lambda m:'[^'+lab[int(m.group(1))]+']', t)
        new=[mk,'']
        for t in r['out_body']+r['out_tail']: new+=[fix(t),'']
        if r['out_defs']: new+=[fix(t) for t in r['out_defs']]+['']
        # keep trailing structure: original section ended with blank line(s)?
        out+=new
        report['pages_changed']+=1
        # word check (letters only)
        w0=collections.Counter(norm(w) for w in re.findall(r'\S+','\n'.join(sec[1:])) if norm(w))
        w1=collections.Counter(norm(w) for w in re.findall(r'\S+','\n'.join(new[1:])) if norm(w))
        d0=w0-w1; d1=w1-w0
        if d0 or d1: wordiss.append((K,dict(d0),dict(d1)))
    txt='\n'.join(out)
    if 'footnotes restored' not in txt:
        txt=re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1)+(m.group(2)[:-1]+'; footnotes and verse numbers restored from the PDF text layer 15 Oct 2026"' if m.group(2).endswith('"') else m.group(2)+'; footnotes and verse numbers restored from the PDF text layer 15 Oct 2026'), txt, count=1, flags=re.M)
    open('/home/claude/finn/out/'+os.path.basename(f),'w',encoding='utf-8').write(txt)
    # footnote integrity
    refs=collections.Counter(m.group(1) for m in re.finditer(r'\[\^([\w.-]+)\]',txt) if not (m.start()==0 or txt[m.start()-1]=='\n')); defs=collections.Counter(re.findall(r'^\[\^([\w.-]+)\]:',txt,flags=re.M))
    bad=[k for k in set(refs)|set(defs) if refs[k]!=1 or defs[k]!=1]
    report['refs']+=sum(refs.values()); report['defs']+=sum(defs.values()); report['bad_pairs']+=len(bad)
    if bad: print(os.path.basename(f),'bad',bad[:10])
    # markers unchanged
    m0=[l for l in L if re.match(r'^\*\[(?:p|PDF)',l)]; m1=[l for l in txt.split('\n') if re.match(r'^\*\[(?:p|PDF)',l)]
    if m0!=m1: print('MARKERS CHANGED',f)
print(report); print('pages with word differences:',len(wordiss))
for x in wordiss[:25]: print(x)
