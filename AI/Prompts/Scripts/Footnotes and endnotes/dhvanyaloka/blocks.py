# Dhvanyaloka, PDF side: the stream of layer fragments split into blocks (K/A/L margin letters), each block into
# its text and its notes run; the chain of note labels 1, 2, 3 ...; the call digits in the text.
import json, os, re, sys, unicodedata
LAY = json.load(open(os.path.expanduser(r'~\fnwork\dhv\layer.json'), encoding='utf-8'))

def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)

def fragments(K):
    """layer lines of a page minus running head and page number: dict(K, y, x, toks, pitch)"""
    out = []; prev_y = None
    for l in LAY[K - 1]['lines']:
        t = ' '.join(w['t'] for w in l['w']).strip()
        if l['y'] < 40 and (re.search(r'[§S\]\[]', t) or re.fullmatch(r'[\dlI]{1,3}', t) or len(t) < 25): continue   # running head
        if re.fullmatch(r'[\dlI]{1,3}', t) and l['y'] > 250: continue                                              # page number
        toks = t.split()
        if len(toks) >= 2 and re.fullmatch(r'[\dIl]{1,2}', toks[0]) and toks[1] == '.':
            toks = [toks[0] + '.'] + toks[2:]          # a label set as '1 .'
        out.append(dict(K=K, y=l['y'], x=l['x'], toks=toks, sz=l['w'][0]['sz']))
    return out

def stream(a, b):
    S = []
    for K in range(a, b + 1): S += fragments(K)
    return S

MARKER = re.compile(r'^[KAL]\.?$')
LABEL = re.compile(r'^([\dIl]{1,2})\.$')
LOOK = {'I': '1', 'l': '1'}
def labnum(t):
    m = LABEL.match(t)
    if not m or not re.search(r'\d', m.group(1)) and m.group(1) not in ('I', 'l'): return None
    return int(''.join(LOOK.get(c, c) for c in m.group(1)))

MARKER2 = re.compile(r'^(?:T|I|Z)?([KAL])\.?$')        # 'TA', 'ZL', 'IL': the margin letter misread

def blocks(S):
    """split the stream at margin letters K / A / L (a fragment that is only the letter, left of the text column, or
    the letter starting a fragment after a large gap); a lone section number ('4.4') or a chapter head ends a block"""
    B = []; cur = None; prev = None
    for f in S:
        gap = (f['y'] - prev['y']) if prev and prev['K'] == f['K'] else 99
        prev = f
        if f['x'] < 48 and (len(f['toks']) == 1 or (len(f['toks']) == 2 and re.fullmatch(r'[^\w]+', f['toks'][0]))) \
                and MARKER2.match(f['toks'][-1]):
            cur = dict(letter=MARKER2.match(f['toks'][-1]).group(1), K=f['K'], frags=[]); B.append(cur); continue
        if len(f['toks']) > 1 and MARKER2.match(f['toks'][0]) and f['x'] < 45 and gap > 12:
            cur = dict(letter=MARKER2.match(f['toks'][0]).group(1), K=f['K'], frags=[]); B.append(cur)
            cur['frags'].append(f); continue          # kept whole: token positions must match the alignment
        if len(f['toks']) == 1 and re.fullmatch(r'\d{1,2}\.\d{1,2}[a-z]?', f['toks'][0]) and gap > 12:
            cur = None; continue                                  # a section heading
        if re.match(r'^CHAPTER\b', ' '.join(f['toks'])) and len(f['toks']) <= 3:
            cur = None; continue
        if cur is None:
            cur = dict(letter='?', K=f['K'], frags=[]); B.append(cur)
        cur['frags'].append(f)
    return B

def split_block(b):
    """text part and notes part: the notes begin at a fragment starting '1.' after a vertical gap or indented"""
    fr = b['frags']
    for i, f in enumerate(fr):
        if f['toks'] and labnum(f['toks'][0]) == 1 and (f['toks'][0] == '1.' or len(f['toks']) > 1) and i > 0:
            gap = f['y'] - fr[i - 1]['y'] if f['K'] == fr[i - 1]['K'] else 99
            if gap > 8 or f['x'] > 34:
                return fr[:i], fr[i:]
    return fr, []

def label_chain(notes):
    """positions (fragment index, token index) of the labels 1, 2, 3 ... in reading order (consecutive only)"""
    toks = [(i, j, t) for i, f in enumerate(notes) for j, t in enumerate(f['toks'])]
    chain = []; want = 1
    for k, (i, j, t) in enumerate(toks):
        if labnum(t) != want: continue
        at_start = j == 0
        after_sentence = k > 0 and re.search(r'[.)\]”"’!?]$', toks[k - 1][2])
        nxt = toks[k + 1][2] if k + 1 < len(toks) else ''
        if (at_start or after_sentence) and nxt and (nxt[0].isupper() or nxt[0] in '“"‘\'([*'):
            chain.append((i, j, want)); want += 1
    return chain

CALL = re.compile(r'^(.*?[^\W\d_][\'’”")\].,;:!?]*|.*?[)\]][\'’”".,;:]*)(\d{1,2})([.,;:)\]*’”"\']*)$')

def calls_in(text):
    """call candidates in the block's text: (fragment index, token index, digits, kind)"""
    out = []
    for i, f in enumerate(text):
        for j, t in enumerate(f['toks']):
            t = re.split(r'[—–]', t)[0] if re.search(r'\d[—–]\w', t) else t      # 'properties10—and'
            m = CALL.match(t)
            if m and norm(m.group(1)):
                out.append((i, j, int(m.group(2)), 'glued'))
            elif m and re.search(r'[)\]]', m.group(1)) and (j > 0 or i > 0):
                out.append((i, j, int(m.group(2)), 'separate'))             # '7.7).10': anchored on the word before
            elif re.fullmatch(r'[.,;:)\]’”"\'*]*\d{1,2}[.,;:]?', t) and (j > 0 or i > 0):
                out.append((i, j, int(re.search(r'\d+', t).group()), 'separate'))
    return out

def match_calls(cands, m):
    """calls 1..m in order: longest run of candidates whose digits are 1, 2, 3 ... (each number once, in order)"""
    best = {}; want = 1; res = []
    for c in cands:
        if c[2] == want: res.append(c); want += 1
    return res

if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    tot = dict(blocks=0, notes=0, calls=0)
    for blk in blocks(stream(a, b)):
        text, notes = split_block(blk)
        ch = label_chain(notes)
        calls = match_calls(calls_in(text), len(ch))
        tot['blocks'] += 1; tot['notes'] += len(ch); tot['calls'] += len(calls)
        first = ' '.join(text[0]['toks'][:6]) if text else ''
        print(blk['letter'], blk['K'], 'notes', len(ch), 'calls', len(calls), '| raw call digits', [c[2] for c in calls_in(text)][:25], '|', first[:40])
    print(tot)
