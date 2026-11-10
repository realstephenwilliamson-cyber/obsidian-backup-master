"""IAST -> Devanagari (words joined as in a Devanagari print: a word-final consonant joins the next word)."""
import re,unicodedata
V={'a':'','ā':'ा','i':'ि','ī':'ी','u':'ु','ū':'ू','ṛ':'ृ','ṝ':'ॄ','ḷ':'ॢ','ḹ':'ॣ','e':'े','ai':'ै','o':'ो','au':'ौ'}
VI={'a':'अ','ā':'आ','i':'इ','ī':'ई','u':'उ','ū':'ऊ','ṛ':'ऋ','ṝ':'ॠ','ḷ':'ऌ','ḹ':'ॡ','e':'ए','ai':'ऐ','o':'ओ','au':'औ'}
C={'kh':'ख','gh':'घ','ch':'छ','jh':'झ','ṭh':'ठ','ḍh':'ढ','th':'थ','dh':'ध','ph':'फ','bh':'भ','k':'क','g':'ग','ṅ':'ङ','c':'च','j':'ज','ñ':'ञ','ṭ':'ट','ḍ':'ड','ṇ':'ण','t':'त','d':'द','n':'न','p':'प','b':'ब','m':'म','y':'य','r':'र','l':'ल','v':'व','ś':'श','ṣ':'ष','s':'स','h':'ह'}
TOK=re.compile('ai|au|kh|gh|ch|jh|ṭh|ḍh|th|dh|ph|bh|[aāiīuūṛṝḷḹeo]|[kgṅcjñṭḍṇtdnpbmyrlvśṣsh]|[ṃṁ]|ḥ|\'|’|\\s+|.',re.S)
def to_deva(s, join=True):
    s=unicodedata.normalize('NFC',s.lower())
    toks=TOK.findall(s)
    if join:   # drop the space after a word-final consonant
        out=[]
        for i,t in enumerate(toks):
            if t.isspace() and out and out[-1] in C and i+1<len(toks) and (toks[i+1] in C or toks[i+1] in VI): continue
            if t.isspace() and i+1<len(toks) and toks[i+1] in("'",'’'): continue
            out.append(t)
        toks=out
    res=[]; prevC=False
    for t in toks:
        if t in C:
            if prevC: res.append('्')
            res.append(C[t]); prevC=True
        elif t in VI:
            if prevC: res.append(V[t])
            else: res.append(VI[t])
            prevC=False
        else:
            if prevC: res.append('्')
            prevC=False
            if t in('ṃ','ṁ'): res.append('ं')
            elif t=='ḥ': res.append('ः')
            elif t in("'",'’'): res.append('ऽ')
            elif t.isspace(): res.append(' ')
            else: res.append(t)
    if prevC: res.append('्')
    return ''.join(res)
def dnorm(s):
    """Devanagari compared loosely: no spaces, dandas, digits; a class nasal before a consonant counts as anusvara"""
    s=re.sub(r'[\s।॥|0-9०-९‌‍‌.,/]','',s)
    s=re.sub(r'[ङञणनम]्(?=[क-ह])','ं',s)
    return s
if __name__=='__main__':
    for x in ["yogam icchadbhiḥ sa tair evam udāhṛtaḥ","sakalo niṣkalo 'nantaḥ śaktir apy asya tadvidhā","evam etan mahādeva nānyathā samudāhṛtam","oṁ aiṁ kḷpta auṣadha"]:
        print(to_deva(x))
