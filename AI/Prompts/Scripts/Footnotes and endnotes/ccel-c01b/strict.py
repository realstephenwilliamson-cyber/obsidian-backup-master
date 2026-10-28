# C-01(b) strict filter (28 Oct 2026): keep a planned cut only where it falls on a clean item boundary.
import json, re, sys, unicodedata
D = json.load(open(sys.argv[1])); PT = json.load(open(sys.argv[2]))['text']; P = json.load(open('plans2.json'))
def pdf(p): return re.search(r'^source_pdf: "?([^"\n]+)"?$', D[p], re.M).group(1)
def vis(s): s = re.sub(r'\[\[([^\]|]*)\|([^\]]*)\]\]', r'\2', s); s = re.sub(r'\[\[([^\]]*)\]\]', r'\1', s); return s.replace('\\', '').replace('*', '')
def norm(s): return ''.join(ch for ch in unicodedata.normalize('NFD', s).lower() if ch.isalnum() and not unicodedata.combining(ch))
def pnorm(t): return re.sub(r'\d', '', norm(re.sub(r'-\n', '', t)))
def ln_(x): return re.sub(r'\d', '', norm(vis(x)))
NUM = re.compile(r'(?<![\w.^#|-])\d{1,4}(?![\w\]|])')
ok, bad = [], []
for r in P:
    nK, nK2 = pnorm(PT[pdf(r['path'])][str(r['K'])]), pnorm(PT[pdf(r['nextpath'])][str(r['nextK'])])
    L = D[r['path']].split('\n'); seg = '\n'.join(L[r['line_a'] + 1:r['line_e']]); before = seg[:r['cut']].rstrip(); run = r['run']
    why = []
    if not re.search(r'[.\]\)”’;]$', before): why.append('before does not end an item')
    # last item before the cut: text since the previous number token
    nb = list(NUM.finditer(before)); last = before[nb[-1].end():] if nb else before[-200:]
    ln = ln_(last)[-30:]
    if len(ln) >= 6 and ln not in nK: why.append('last item before the cut not on page K')
    if len(ln) >= 6 and ln in nK2 and ln not in nK: why.append('last item before is on the next page')
    m = NUM.search(run)
    lead = run[:m.start()] if m else run
    if lead.strip():
        if re.search(r'[A-Za-z]{2,}', vis(lead)): why.append('run starts with Latin-script words')
        elif ln_(lead) not in nK2 or ln_(lead) in nK: why.append('leading Greek not only on next page')
    nr = list(NUM.finditer(run)); first = run[nr[0].end():nr[1].start()] if len(nr) > 1 else run[nr[0].end():] if nr else run
    if len(ln_(first)) >= 6 and ln_(first)[:30] not in nK2: why.append('first item not on next page')
    (bad if why else ok).append({**r, 'why2': why})
json.dump(ok, open('ok.json', 'w'), ensure_ascii=False, indent=1); json.dump(bad, open('hold.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('ok', len(ok), 'hold', len(bad)); print(Counter(w for b in bad for w in b['why2']))
