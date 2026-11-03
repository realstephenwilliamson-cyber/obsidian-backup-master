import re, glob
D='/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Tantraloka (Dyczkowski)/'
def note(code):
    v,n=code.split()
    return glob.glob(D+f'Tantraloka vol {v} (Dyczkowski)/Tantraloka Dyczkowski v{v} {n} - *.md')[0]
def ctx(code, pat, w=120, regex=False):
    p=note(code); t=open(p,encoding='utf-8').read(); out=[]
    for m in (re.finditer(pat,t) if regex else re.finditer(re.escape(pat),t)):
        K=re.findall(r'\^pg(\d+)', t[:m.start()]); out.append((int(K[-1]) if K else None, t.count('\n',0,m.start())+1, t[max(0,m.start()-w):m.end()+w]))
    return out
