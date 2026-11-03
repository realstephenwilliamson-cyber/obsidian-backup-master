import sys, subprocess
P = dict(l.rstrip('\n').split('=', 1) for l in open('/home/claude/dyfn/paths.txt', encoding='utf-8') if '=' in l)
B, first, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
r = subprocess.run(['python3', '/home/claude/dyfn/scripts/batch.py', B, first] + [f'{i}={P[i]}' for i in ids], capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-1500:])
