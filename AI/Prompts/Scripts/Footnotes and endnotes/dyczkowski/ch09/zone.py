# zone.py K [SCALE] [Y0] [Y1]: crop of PDF page K (300 dpi) from Y0 (default: the footnote zone) to Y1, scaled, to view/zK.png
import sys, json
from PIL import Image
k = int(sys.argv[1]); sc = float(sys.argv[2]) if len(sys.argv) > 2 else 0.45
S = json.load(open('/home/claude/lost/ch09/starts.json'))
im = Image.open('/home/claude/lost/ch09/img300/p-%03d.png' % k)
y0 = int(sys.argv[3]) if len(sys.argv) > 3 else max(0, (S[str(k)]['zone_y'] or 1500) - 60)
y1 = int(sys.argv[4]) if len(sys.argv) > 4 else im.height
c = im.crop((100, y0, im.width - 100, y1)); c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
c.save('/home/claude/lost/ch09/view/z%d.png' % k); print(c.size)
