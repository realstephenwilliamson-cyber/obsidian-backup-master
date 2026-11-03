#!/bin/bash
# render PDF 16-224 at 300 dpi grey and run Tesseract TSV on each (ch05 pre-pass)
P="/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. 04.pdf"
cd /home/claude/lost/ch05
pdftoppm -f 16 -l 224 -r 300 -gray -png "$P" img300/p
ls img300/*.png | OMP_THREAD_LIMIT=1 xargs -P 2 -I{} sh -c 'b=$(basename {} .png); [ -s tsv/$b.tsv ] || tesseract {} tsv/$b tsv >/dev/null 2>&1'
echo DONE
