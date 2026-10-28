# ledger.py: add an agent's tokens: ledger.py "what" model tokens [HH:MM]
import json, sys, os
f = '/home/claude/dyfn/ledger.json'
L = json.load(open(f)) if os.path.exists(f) else {'agents': []}
if len(sys.argv) > 3:
    L['agents'].append({'what': sys.argv[1], 'model': sys.argv[2], 'tokens': int(sys.argv[3]), 'at': sys.argv[4] if len(sys.argv) > 4 else ''})
    json.dump(L, open(f, 'w'), indent=1)
a = sum(x['tokens'] for x in L['agents']); fb = sum(x['tokens'] for x in L['agents'] if x['model'] == 'fable')
print('all %d (cap 10M, %.0f%%); fable %d (cap 2.5M, %.0f%%); agents %d' % (a, a / 10e6 * 100, fb, fb / 2.5e6 * 100, len(L['agents'])))
