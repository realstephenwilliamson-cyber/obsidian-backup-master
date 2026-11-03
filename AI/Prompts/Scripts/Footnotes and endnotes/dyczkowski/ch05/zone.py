# zone.py PDF Y0 Y1 OUT [SCALE]: crop rows Y0-Y1 of the 300 dpi page image (for the lead's look at a footnote zone)
import sys
from PIL import Image
k, y0, y1, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; sc = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
im = Image.open('/home/claude/lost/ch05/img300/p-%03d.png' % k).convert('L'); im = im.crop((100, y0, im.width - 100, y1))
im.resize((int(im.width * sc), int(im.height * sc))).save(out)
