#!/bin/bash
# render.sh K : PDF page K at 300 dpi grey -> img300/p-KKK.png, Tesseract TSV -> tsv/p-KKK.tsv
P="/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. 06.pdf"
k=$1; f=$(printf 'p-%03d' $k); D=/home/claude/lost/ch09
[ -s $D/tsv/$f.tsv ] && exit 0
pdftoppm -f $k -l $k -r 300 -gray -png -singlefile "$P" $D/img300/$f
OMP_THREAD_LIMIT=1 tesseract $D/img300/$f.png $D/tsv/$f -l eng tsv >/dev/null 2>&1
