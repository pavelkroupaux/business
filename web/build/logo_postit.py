# Logo: nakloněný žlutý post-it, na něm check fixou.
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import B, R, CAREER, FONTDIR, DRAFT
import math, io, os, sys
from logo import check, png, INK, YEL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
_HAND = TTFont(FONTDIR + 'ShantellSans-500-full.ttf')
def hand_path(txt, size, x, y):
    gs = _HAND.getGlyphSet(); cm = _HAND.getBestCmap(); sc = size / _HAND['head'].unitsPerEm
    pen = SVGPathPen(gs); x0 = x
    for ch in txt:
        g = gs[cm[ord(ch)]]; g.draw(TransformPen(pen, (sc, 0, 0, -sc, x, y))); x += g.width * sc
    return pen.getCommands(), x - x0

S = 400            # strana lístku
TILT = -6          # náklon lístku (stupně)
C = 256            # střed plátna 512
def note_svg(shadow=False, check_col=INK, note_col=YEL, wf=.105, rough=.55, pk=False):
    x0 = C - S / 2; y0 = C - S / 2
    u = lambda fx, fy: (x0 + fx * S, y0 + fy * S)
    d, _ = check(A=u(.25, .53), V=u(.43, .73), E=u(.77, .27), w=S * wf, bowE=(-S * .02, S * .012),
                 r=S * .045, rough=rough, w_start=.86, w_end=.78, taper=.25, seed=21)
    note = f'<rect x="{x0}" y="{y0}" width="{S}" height="{S}" rx="{S*.018:.1f}" fill="{note_col}"/>'
    inner = f'{note}<path d="{d}" fill="{check_col}" transform="rotate(-3 {C} {C})"/>'
    if pk:  # iniciály v pravém dolním rohu, ručním písmem jako popisky na webu
        px, py = u(.9, .9)
        dd, wd = hand_path('pk', S * .1, 0, 0)
        inner += f'<path d="{dd}" fill="{check_col}" transform="translate({px - wd:.1f} {py:.1f}) rotate(-2)"/>'
    return f'<g transform="rotate({TILT} {C} {C})">{inner}</g>'

# těsný výřez kolem nakloněného lístku
half = S / 2 * (math.cos(math.radians(abs(TILT))) + math.sin(math.radians(abs(TILT)))) + 6
VB = (C - half, C - half, 2 * half, 2 * half)
def svg_doc(body, vb=VB, bg=None):
    x, y, w, h = vb
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}">{b}{body}</svg>'

LOGO = svg_doc(note_svg())
LOGO_PK = svg_doc(note_svg(pk=True))

def with_shadow(px, bg=None):
    """PNG se stínem pod lístkem (stín v PIL, ať je měkký i bez SVG filtrů)."""
    pad = int(px * .08); W = px + 2 * pad
    base = Image.new('RGBA', (W, W), bg or (0, 0, 0, 0))
    lg = png(LOGO_PK, px)
    a = lg.split()[3]
    sh = Image.new('RGBA', (W, W), (0, 0, 0, 0)); m = Image.new('L', (W, W), 0)
    m.paste(a, (pad, pad + int(px * .025))); m = m.filter(ImageFilter.GaussianBlur(px * .028))
    sh.putalpha(m.point(lambda v: int(v * .28)))
    base = Image.alpha_composite(base, sh)
    base.alpha_composite(lg, (pad, pad))
    return base

if __name__ == '__main__':
    DRAFT = DRAFT; os.makedirs(DRAFT, exist_ok=True)
    open(DRAFT + 'postit.svg', 'w').write(LOGO)
    F = lambda s: ImageFont.truetype(FONTDIR + 'Inter-600-full.ttf', s)
    sh = Image.new('RGB', (1500, 900), '#e9e9e6'); d = ImageDraw.Draw(sh)
    # velký na bílé a na černé
    for k, bg in enumerate(('#ffffff', '#111111')):
        t = Image.new('RGBA', (440, 440), bg); im = with_shadow(340) if k == 0 else png(LOGO, 340)
        t.alpha_composite(im, ((440 - im.width) // 2, (440 - im.height) // 2)); sh.paste(t.convert('RGB'), (30 + k * 470, 40))
    d.text((32, 10), 'Logo, se stínem a bez', font=F(20), fill='#333')
    # hlavička světlá a tmavá
    for k, (bg, fg) in enumerate((('#ffffff', '#111111'), ('#111111', '#f5f5f7'))):
        hdr = Image.new('RGBA', (500, 200), bg); dh = ImageDraw.Draw(hdr)
        for j, hh in enumerate((18, 24)):
            im = png(LOGO, hh); y = 40 + j * 80; hdr.alpha_composite(im, (24, y))
            dh.text((24 + hh + 10, y + hh * .5), 'Pavel Kroupa', font=F(int(hh * .7)), fill=fg, anchor='lm')
        sh.paste(hdr.convert('RGB'), (970, 40 + k * 230))
    d.text((972, 10), 'Hlavička 18 a 24 px', font=F(20), fill='#333')
    # favicony
    tab = Image.new('RGB', (500, 200), '#dfe1e5'); dt = ImageDraw.Draw(tab)
    for j, px in enumerate((16, 32, 48)):
        im = png(LOGO, px); tab.paste(im, (30 + j * 90, 60), im)
        big = im.resize((px * 3, px * 3), Image.NEAREST)
    dt.text((30, 140), '16      32      48', font=F(16), fill='#555')
    sh.paste(tab, (970, 520)); d.text((972, 490), 'Favicon v reálné velikosti', font=F(20), fill='#333')
    # zvětšené 16 a 32 px, ať je vidět, co z toho zbude
    for j, px in enumerate((16, 32)):
        im = png(LOGO, px).resize((160, 160), Image.NEAREST)
        t = Image.new('RGBA', (160, 160), '#ffffff'); t.alpha_composite(im); sh.paste(t.convert('RGB'), (30 + j * 190, 540))
    d.text((32, 510), '16 a 32 px zvětšené', font=F(20), fill='#333')
    sh.save(DRAFT + 'postit-nahled.png'); print('ok', VB)
