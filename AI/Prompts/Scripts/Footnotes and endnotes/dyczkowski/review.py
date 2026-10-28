# review.py ID [ID ...]: apply the reader's ops (apply_ops.py --renumber) and print a compact summary for the lead.
import sys, json, subprocess, os
H = '/home/claude/dyfn'
START = {a.split('=')[0]: a.split('=')[1] for a in sys.argv[1:] if '=' in a}
for nid in [a.split('=')[0] for a in sys.argv[1:]]:
    ops = f'{H}/rd/{nid}/ops.json'
    if not os.path.exists(ops): print(nid, 'NO ops.json'); continue
    r = subprocess.run(['python3', f'{H}/scripts/apply_ops.py', f'{H}/src/{nid}.md', f'{H}/work/{nid}/pre.md', ops,
                        f'{H}/work/{nid}/out.md', f'{H}/work/{nid}/rep.json', ] + (['--map=' + START[nid][4:]] if START.get(nid, '').startswith('map:') else [] if START.get(nid) == '0' else ['--renumber']) + (['--start=' + START[nid]] if START.get(nid, '0').isdigit() and START.get(nid, '0') != '0' else []), capture_output=True, text=True)
    if r.returncode: print(nid, 'ERROR', r.stderr[-800:]); continue
    R = json.load(open(f'{H}/work/{nid}/rep.json', encoding='utf-8'))
    O = json.load(open(ops, encoding='utf-8'))
    kinds = {}
    for o in O['ops']: k = (o.get('kind'), o.get('op')); kinds['%s/%s' % k] = kinds.get('%s/%s' % k, 0) + 1
    pre = json.load(open(f'{H}/work/{nid}/pre.json', encoding='utf-8'))
    print('==', nid, '| calls', R['calls'], 'defs', R['defs'], 'range', R['numbers'], '| plain before', pre['plain_found'], 'real before', len(pre['real_defs_before']))
    print('   not_once', R['not_once'][:12], '| order', R['calls_in_order'], '| struct', all(R['struct'].values()), R['struct'] if not all(R['struct'].values()) else '',
          '| pg_blank', R['pg_blank_after'], '| illegible', R['illegible'], '| paren', R['space_before_paren'])
    print('   ops', kinds, '| apply problems', R['problems'][:5], '| relabelled', len(R['relabelled']), dict(list(R['relabelled'].items())[:6]))
    rl = R['relabelled']; mm = {}
    for e in O.get('per_note', []):
        if not str(e.get('printed', '')).isdigit(): continue
        new = rl.get(str(e['n']), str(e['n']))
        if new.isdigit() and int(new) != int(e['printed']): mm[int(new) - int(e['printed'])] = mm.get(int(new) - int(e['printed']), 0) + 1
    nm = sum(mm.values()); big = sum(v for k, v in mm.items() if abs(k) > 50)
    print('   label minus printed (per_note %d):' % len(O.get('per_note', [])), 'all equal' if not mm else ('printed looks like page numbers' if big > nm / 2 else sorted(mm.items())[:6]))
    print('   removed', R['words_removed'])
    print('   added', R['words_added'])
    print('   reader problems (%d):' % len(O.get('problems', [])))
    for p in O.get('problems', []): print('    -', str(p)[:260])
