#!/bin/bash
cd /home/claude/lost/ch05
ls img300/*.png | OMP_THREAD_LIMIT=1 xargs -P 2 -I{} sh -c 'b=$(basename {} .png); [ -s tsv/$b.tsv ] || { tesseract {} tsv/_$b tsv >/dev/null 2>&1 && mv tsv/_$b.tsv tsv/$b.tsv; }'
echo DONE
