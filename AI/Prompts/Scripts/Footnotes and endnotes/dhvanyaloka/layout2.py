# Layout check that allows the one intended change: an unconverted note's label escaped ('4\.') when it now opens a paragraph.
import sys, glob, os, re
O = r'C:\Vaults\Obsidian Vault\.work\backup-footnotes-2026-10-18\Dhvanyaloka\Library\Trika\The Dhvanyaloka of Anandavardhana with the Locana (Anandavardhana)'
N = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
def paras(t):
    out, cur = [], []
    for l in t.split('\n'):
        if l.strip(): cur.append(l.rstrip())
        elif cur: out.append('\n'.join(cur)); cur = []
    if cur: out.append('\n'.join(cur))
    return out
esc = 0; other = []; tot = 0
for f in glob.glob(os.path.join(N, '*.md')):
    a = paras(open(os.path.join(O, os.path.basename(f)), encoding='utf-8').read()); J = '\n\n'.join(a)
    for p in paras(open(f, encoding='utf-8').read()):
        if '[^' in p or p.startswith('---'): continue
        tot += 1
        if p in a or p.strip() in J: continue
        q = re.sub(r'^(\s*\d{1,3})\\\.', r'\1.', p)
        if q != p and (q in a or q.strip() in J): esc += 1; continue
        other.append(p[:120])
print('paragraphs without footnotes', tot, '| differing only by the added escape', esc, '| other differences', len(other))
for o in other[:8]: print('  ', o)
