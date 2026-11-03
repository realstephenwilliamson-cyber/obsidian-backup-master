# zone.py PDF [Y0] [Y1] [SCALE]: crops a 300 dpi page (default: from its footnote zone to the bottom) into view/z-PDF.png
import sys, json
from PIL import Image
k = int(sys.argv[1]); S = json.load(open('/home/claude/lost/ch28/num_starts3.json'))
im = Image.open('/home/claude/lost/ch28/img300/p-%03d.png' % k); w, h = im.size
y0 = int(sys.argv[2]) if len(sys.argv) > 2 else max(0, (S[str(k)]['zone_y'] or 200) - 60)
y1 = int(sys.argv[3]) if len(sys.argv) > 3 else h
sc = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
c = im.crop((100, y0, w - 80, y1)); c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
c.save('/home/claude/lost/ch28/view/z-%03d.png' % k); print(k, y0, y1, c.size)
