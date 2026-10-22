import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks as BL
S = BL.stream(56, 745)
shown = 0; tot = 0
for b in BL.blocks(S):
    if b['letter'] == '?': continue
    text, notes = BL.split_block(b)
    if not notes: continue
    m = len(BL.label_chain(notes))
    got = {c[2] for c in BL.calls_in(text)}
    miss = [n for n in range(1, m + 1) if n not in got]
    tot += len(miss)
    if miss and shown < 10:
        shown += 1
        digs = [t for f in text for t in f['toks'] if re.search(r'\d', t)][:25]
        print(b['letter'], b['K'], 'm', m, 'missing', miss, '| digit tokens:', digs)
print('missing calls', tot)
