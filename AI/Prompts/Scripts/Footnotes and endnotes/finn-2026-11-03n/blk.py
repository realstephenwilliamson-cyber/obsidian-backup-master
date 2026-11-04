# blk.py K[:from] ... : print page K's block in full (from non-empty line index 'from' on), lines numbered
import sys, re
sys.path.insert(0, '/home/claude/finn')
from view import P
for a in sys.argv[1:]:
    K, fr = (a.split(':') + ['0'])[:2]; K = int(K); fr = int(fr)
    print(f'----- K{K} p.{P[K]["pp"]}')
    for i, l in enumerate(P[K]['lines']):
        if i >= fr and l.strip(): print(f'{i:3}| {l}')
