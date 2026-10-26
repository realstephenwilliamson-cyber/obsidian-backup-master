#!/bin/bash
# keep re-running pipe.py until all 11 volumes have an 'after' entry in the manifest
cd /home/claude/dz
while true; do
  n=$(python3 -c "import json;m=json.load(open('rb/manifest.json'));print(sum(1 for v in m.values() if 'after' in v))" 2>/dev/null || echo 0)
  [ "$n" -ge 11 ] && echo "LOOPDONE $(date +%H:%M)" >> pipe.log && break
  if ! pgrep -f "python3 pipe.py" >/dev/null; then
    todo=$(python3 -c "
import json,glob,os
m=json.load(open('rb/manifest.json'))
print(sum(1 for p in glob.glob('pdf/*.pdf') if 'after' not in m.get(os.path.basename(p),{})))")
    [ "$todo" -gt 0 ] && python3 pipe.py >> pipe.log 2>&1
  fi
  sleep 20
done
