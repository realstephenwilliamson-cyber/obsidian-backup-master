#!/bin/bash
# wait up to $1 seconds for a new part file or for the chain to finish; then print status
end=$((SECONDS+${1:-540}))
n0=$(ls /mnt/user-data/outputs/d09/ | wc -l)
while [ $SECONDS -lt $end ]; do
  n=$(ls /mnt/user-data/outputs/d09/ | wc -l)
  [ "$n" != "$n0" ] && break
  pgrep -f "pipe.py" >/dev/null || break
  sleep 15
done
date +%H:%M; ls /mnt/user-data/outputs/d09/
pgrep -f pipe.py >/dev/null && echo RUNNING || echo STOPPED
python3 -c "
import json;m=json.load(open('/home/claude/d09/rb/manifest.json'));print('manifest',len(m))"
ps -eo args | grep -o "ocrmypdf --redo-ocr.*" | grep -o "Vault/.*\.pdf" | head -1
d=$(ls -d /tmp/ocrmypdf.io.* 2>/dev/null | head -1); [ -n "$d" ] && echo "pages done in current file: $(ls $d | grep -c _ocr_tess.txt)"
