import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import B, R, CAREER, FONTDIR, DRAFT
import io, os, shutil, sys
from logo_postit import *
M = CAREER
DIRS = [M + '05 Web/repo/logo/', M + '07 Assets/moje logo/post-it/']
FAV = svg_doc(note_svg(wf=.15, rough=0))          # favicon: silnější check, bez nerovností
def save(name, data):
    for d in DIRS:
        os.makedirs(d + os.path.dirname(name), exist_ok=True)
        (open(d + name, 'w').write(data) if isinstance(data, str) else open(d + name, 'wb').write(data))
def pngbytes(im, opaque=None):
    if opaque:
        bg = Image.new('RGBA', im.size, opaque); bg.alpha_composite(im); im = bg.convert('RGB')
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True); return b.getvalue()
save('logo.svg', LOGO)            # malé použití: hlavička, ikony
save('logo-pk.svg', LOGO_PK)      # velké použití: s iniciálami
save('logo-512.png', pngbytes(png(LOGO, 512)))
save('logo-pk-1024.png', pngbytes(png(LOGO_PK, 1024)))
save('logo-stin-1024.png', pngbytes(with_shadow(1024)))
for name, bg in (('logo-na-bile-1024.png', '#ffffff'), ('logo-na-cerne-1024.png', '#111111')):
    t = Image.new('RGBA', (1024, 1024), bg); im = with_shadow(760) if bg == '#ffffff' else png(LOGO_PK, 760)
    t.alpha_composite(im, ((1024 - im.width) // 2, (1024 - im.height) // 2)); save(name, pngbytes(t))
# favicon sada
save('favicon/favicon.svg', FAV)
sizes = [png(FAV, s) for s in (16, 32, 48)]
b = io.BytesIO(); sizes[2].save(b, 'ICO', sizes=[(16, 16), (32, 32), (48, 48)], append_images=sizes[:2]); save('favicon/favicon.ico', b.getvalue())
t = Image.new('RGBA', (180, 180), '#ffffff'); im = png(FAV, 150); t.alpha_composite(im, (15, 15)); save('favicon/apple-touch-icon.png', pngbytes(t))
save('favicon/icon-512.png', pngbytes(png(FAV, 512)))
if os.path.exists(DRAFT + 'postit-nahled.png'): shutil.copy(DRAFT + 'postit-nahled.png', DIRS[1] + 'nahled.png')
for d in DIRS: print(d, sorted(os.listdir(d)), sorted(os.listdir(d + 'favicon')))
