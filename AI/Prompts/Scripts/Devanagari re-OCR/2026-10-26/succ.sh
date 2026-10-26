#!/bin/bash
# wait for the old loop (pid $1) to end, then run the given loop script ($2)
while kill -0 "$1" 2>/dev/null; do sleep 10; done
echo "SUCC start $2 $(date +%H:%M)" >> /home/claude/dz/succ.log
exec "$2"
