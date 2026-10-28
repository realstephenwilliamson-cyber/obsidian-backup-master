import json, sys
R = json.load(open(sys.argv[1]))
print('agree %d / %d' % (R['agree'], R['total']))
for r in R['rows']:
    if r.get('ok_call') and r.get('ok_def'): continue
    print(r['task'], r.get('n'), 'call', r.get('ok_call'), 'def', r.get('ok_def'), '| chk:', (r.get('checker_before') or r.get('checker_carry') or '')[-45:], '| ours:', (r.get('ours_before') or r.get('ours_carry') or '')[-50:], '| f:', (r.get('checker_first') or '')[:25], '/', (r.get('ours_first') or '')[:25])
