#!/bin/bash
cd /home/claude/dz
while true; do
  python3 fix/post.py >> post.log 2>&1
  n=$(python3 -c "import json;print(len(json.load(open('rb/post.json'))))" 2>/dev/null || echo 0)
  [ "$n" -ge 11 ] && echo "POSTDONE $(date +%H:%M)" >> post.log && break
  sleep 60
done
