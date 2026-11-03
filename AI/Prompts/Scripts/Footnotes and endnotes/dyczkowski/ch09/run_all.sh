#!/bin/bash
# run_all.sh: the Chapter Nine pre-pass from starts5.json to work/ID (prepass.py on ID-named copies of the numbered notes)
cd /home/claude/lost/ch09
python3 scripts/prepass_ch09.py starts5.json num $(for i in 3 4 5 6 7 8 9; do echo v06-0$i=/home/claude/dyfn/src/v06-0$i.md; done) > prepass.log 2>&1
head -1 prepass.log
for i in 3 4 5 6 7 8 9; do
  cp num/v06-0$i.num.md num/byid/v06-0$i.md
  python3 /home/claude/dyfn/scripts/prepass.py num/byid/v06-0$i.md /home/claude/dyfn/work/v06-0$i > /dev/null
  python3 -c "
import json; R=json.load(open('/home/claude/dyfn/work/v06-0$i/pre.json')); print('v06-0$i', R['converted'], min(R['numbers']), max(R['numbers']), [(f['line'],f['number'],f['why'][:20]) for f in R['flags']], R['clash'], R['indented'])"
done
