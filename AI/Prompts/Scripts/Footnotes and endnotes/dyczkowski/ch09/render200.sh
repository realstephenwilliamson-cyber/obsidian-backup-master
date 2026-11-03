#!/bin/bash
# render200.sh K: PDF page K at 200 dpi grey, margins trimmed as packet.py does -> img200/p-KKK.png (the readers' images)
P="/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. 06.pdf"
k=$1; f=$(printf 'p-%03d' $k); D=/home/claude/lost/ch09/img200
[ -s $D/$f.png ] && exit 0
pdftoppm -f $k -l $k -r 200 -gray -png -singlefile "$P" $D/_t$k
python3 -c "
from PIL import Image, ImageOps
import os
im = Image.open('$D/_t$k.png').convert('L'); bb = ImageOps.invert(im).point(lambda v: 255 if v > 60 else 0).getbbox()
if bb: im = im.crop((max(0, bb[0] - 12), max(0, bb[1] - 12), min(im.width, bb[2] + 12), min(im.height, bb[3] + 12)))
im.save('$D/$f.png', optimize=True); os.remove('$D/_t$k.png')"
