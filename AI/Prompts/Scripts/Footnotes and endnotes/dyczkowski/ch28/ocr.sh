#!/bin/bash
# render PDF pages at 300 dpi grey and run tesseract TSV (eng), 2 in parallel
PDF="/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. 10.pdf"
O=/home/claude/lost/ch28
one() { k=$1; p=$(printf '%03d' $k)
  [ -f $O/img300/p-$p.png ] || pdftoppm -f $k -l $k -r 300 -gray -png -singlefile "$PDF" $O/img300/p-$p
  [ -f $O/tsv/p-$p.tsv ] || OMP_THREAD_LIMIT=1 tesseract $O/img300/p-$p.png $O/tsv/p-$p -l eng tsv >/dev/null 2>&1; }
export -f one; export PDF O
seq $1 $2 | xargs -P 2 -I{} bash -c 'one {}'
echo done
