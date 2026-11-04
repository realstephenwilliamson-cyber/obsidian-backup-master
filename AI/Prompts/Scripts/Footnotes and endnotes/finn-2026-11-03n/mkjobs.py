# mkjobs.py NNN kind spec-name : make a runner job from the kept templates. kind = dry | apply | check
import sys, re
num, kind, spec = sys.argv[1], sys.argv[2], sys.argv[3]
BKX = sys.argv[4] if len(sys.argv) > 4 else None
SPEC = '.work/edits/finn-2026-11-03n/' + spec; BK = BKX or '.work/backup-finn-2026-11-03n/'
name = 'pf%s-%s-%s' % (num, spec.replace('-spec.json', ''), kind)
if kind in ('dry', 'apply'):
    s = open('/home/claude/finn/tpl-apply.js', encoding='utf-8').read()
    s = s.replace("SPEC = '.work/edits/audit-2026-11-04/fixes-1.json', BK = '.work/backup-audit-fixes-2026-11-03/'", "SPEC = '%s', BK = '%s'" % (SPEC, BK))
    s = s.replace("// pf591-audfix-apply (3 Nov 2026, audit corrections, safe fixes)", "// %s (3 Nov 2026, night; from the pf591 template): Finn's footnotes" % name)
    s = s.replace('.work/out/pf591-audfix-apply.json', '.work/out/%s.json' % name).replace('`pf591-audfix-apply:', '`%s:' % name)
    if kind == 'dry': s = s.split('\n', 1)[1]
    assert SPEC in s and name in s
else:
    s = open('/home/claude/finn/tpl-check.js', encoding='utf-8').read()
    s = s.replace("SPEC = '.work/edits/fnleft-2026-11/gaps-spec.json', BK = '.work/backup-gaps-2026-11-03/'", "SPEC = '%s', BK = '%s'" % (SPEC, BK))
    s = s.replace('// pf680-gaps-check (3 Nov 2026; kept as a template: copy, rename to a new pfNNN, set SPEC and BK)', '// %s (3 Nov 2026, night; from the pf680 template)' % name)
    s = s.replace('.work/out/pf680-gaps-check.json', '.work/out/%s.json' % name).replace('`pf680-gaps-check:', '`%s:' % name)
    assert SPEC in s and name in s
open('/home/claude/finn/jobs/%s.js' % name, 'w', encoding='utf-8', newline='\n').write(s); print(name)
