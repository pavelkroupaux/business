import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import B, R, CAREER, FONTDIR, DRAFT
import io, os, shutil, sys, re
from lockup import *
M = CAREER
DIRS = [M + '05 Web/repo/logo/pk/', M + '07 Assets/moje logo/pk/']
for d in DIRS: os.makedirs(d, exist_ok=True)
def save(name, data):
    for d in DIRS:
        (open(d + name, 'w').write(data) if isinstance(data, str) else open(d + name, 'wb').write(data))
def pb(im):
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True); return b.getvalue()
# těsný výřez pro průhledné verze (z obsahu vykresleného v 2000 px)
def crop_vb(body, pad=14):
    im = png(doc(body), 2000); x0, y0, x1, y1 = im.getbbox(); k = 500 / 2000
    x0, y0, x1, y1 = x0 * k - pad, y0 * k - pad, x1 * k + pad, y1 * k + pad
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {x1-x0:.1f} {y1-y0:.1f}">{body}</svg>'
SETS = {'svetle': ('#FFFFFF', INK, INK), 'tmave': ('#111111', '#FFFFFF', '#5C5C60')}
for name, (bg, tc, lc) in SETS.items():
    body = mark(tc, lc)
    t = crop_vb(body); save(f'pk-{name}.svg', t)
    save(f'pk-{name}-1024.png', pb(png(t, 1024)))
    sq = doc(body, bg); save(f'pk-{name}-ctverec.svg', sq)
    for px in (1024, 400): save(f'pk-{name}-ctverec-{px}.png', pb(png(sq, px).convert('RGB')))
if os.path.exists(DRAFT + 'pk-varianty.png'): shutil.copy(DRAFT + 'pk-varianty.png', DIRS[1] + 'varianty.png')
print(sorted(os.listdir(DIRS[0])))
# náhled
from PIL import Image
a = Image.open(DIRS[0] + 'pk-svetle-ctverec-400.png').convert('RGB'); b = Image.open(DIRS[0] + 'pk-tmave-ctverec-400.png').convert('RGB')
c = Image.open(DIRS[0] + 'pk-svetle-1024.png').convert('RGBA')
s = Image.new('RGB', (1260, 420), '#e9e9e6'); s.paste(a, (10, 10)); s.paste(b, (420, 10))
bgw = Image.new('RGBA', c.size, '#ffffff'); bgw.alpha_composite(c); bgw = bgw.convert('RGB'); bgw.thumbnail((400, 400)); s.paste(bgw, (830, 10))
s.save(DIRS[1] + 'nahled.png'); s.save(DRAFT + 'pk-final.png')
