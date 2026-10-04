# Logo "pk + linka + post-it": staré logo pk s linkou, čtvereček na konci je nakloněný post-it s checkem.
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import B, R, CAREER, FONTDIR, DRAFT
import math, os, sys, io
from logo import text_path, check, png, INK, YEL
from PIL import Image, ImageDraw, ImageFont

F = 230                      # velikost písma pk
TRACK = -0.035
ASC, DESC = F * 1490 / 2048, F * 418 / 2048
TXT_W = (1291 + 1179 - 128) / 2048 * F + TRACK * F
LINE_T = 18                  # tloušťka linky
NOTE = 58                    # strana lístku
GAP = 20                     # mezera mezi linkou a lístkem
TILT = -6

def note(cx, cy, s, ink=INK, rough=.3):
    x0, y0 = cx - s / 2, cy - s / 2
    u = lambda fx, fy: (x0 + fx * s, y0 + fy * s)
    d, _ = check(A=u(.22, .54), V=u(.43, .76), E=u(.8, .24), w=s * .15, bowE=(-s * .02, s * .012),
                 r=s * .05, rough=rough, w_start=.9, w_end=.82, taper=.2, seed=21)
    return (f'<g transform="rotate({TILT} {cx:.1f} {cy:.1f})"><rect x="{x0:.1f}" y="{y0:.1f}" width="{s}" height="{s}" '
            f'rx="{s*.04:.1f}" fill="{YEL}"/><path d="{d}" fill="{ink}" transform="rotate(-3 {cx:.1f} {cy:.1f})"/></g>')

def mark(txt_col, line_col, box=500):
    left = (box - TXT_W) / 2 - 128 / 2048 * F
    block = ASC + DESC + 48 + LINE_T / 2 + NOTE / 2 + 4
    yb = (box - block) / 2 + ASC
    d, _ = text_path('pk', F, left, yb, 700, TRACK)
    x_l = left + 128 / 2048 * F; x_r = x_l + TXT_W
    ly = yb + DESC + 48
    nx = x_r - NOTE / 2 + 2
    x_line_end = x_r - NOTE - GAP
    line = f'<rect x="{x_l:.1f}" y="{ly - LINE_T/2:.1f}" width="{x_line_end - x_l:.1f}" height="{LINE_T}" fill="{line_col}"/>'
    return f'<path d="{d}" fill="{txt_col}"/>{line}{note(nx, ly, NOTE)}'

def doc(body, bg=None, box=500):
    b = f'<rect width="{box}" height="{box}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box} {box}">{b}{body}</svg>'

DARK, WHITE, GREY = '#111111', '#FFFFFF', '#5C5C60'
VARIANTS = [
    ('1  tmavé, žlutá linka', DARK, WHITE, YEL),
    ('2  tmavé, šedá linka', DARK, WHITE, GREY),
    ('3  světlé, černá linka', WHITE, INK, INK),
    ('4  světlé, žlutá linka', WHITE, INK, YEL),
]

if __name__ == '__main__':
    OUT = DRAFT
    Fn = lambda s: ImageFont.truetype(FONTDIR + 'Inter-600-full.ttf', s)
    sh = Image.new('RGB', (4 * 330 + 20, 560), '#e9e9e6'); d = ImageDraw.Draw(sh)
    for i, (name, bg, tc, lc) in enumerate(VARIANTS):
        s = doc(mark(tc, lc), bg); x = 20 + i * 330
        sh.paste(png(s, 310).convert('RGB'), (x, 50)); d.text((x, 18), name, font=Fn(18), fill='#333')
        for j, px in enumerate((96, 48, 32)):
            im = png(s, px).convert('RGB'); sh.paste(im, (x + [0, 110, 172][j], 390))
        open(OUT + f'pk-varianta-{i+1}.svg', 'w').write(s)
    d.text((20, 500), 'Malé velikosti: 96, 48 a 32 px', font=Fn(16), fill='#555')
    sh.save(OUT + 'pk-varianty.png'); print('ok')
