# OG / meta obrázky 1200×630 (+ @2x 2400×1260) ze stejných kreseb jako web.
import re, os, io, html
import cairosvg
from PIL import Image, ImageFont
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import R, FONTDIR
SITE = open(R + 'Career/05 Web/verze/site-v5.html').read()
OUT = R + 'Career/07 Assets/og/'
REPO = R + 'Career/05 Web/repo/og/'
os.makedirs(OUT, exist_ok=True); os.makedirs(REPO, exist_ok=True)
F700 = FONTDIR + 'Inter-700-full.ttf'
F500 = FONTDIR + 'Inter-500-full.ttf'
INK, MUTED, FAINT, YEL = '#111111', '#5B5B55', '#8E8E93', '#FFCE1B'
W, H = 1200, 630
VARS = {'var(--ink)': INK, 'var(--muted)': '#6e6e73', 'var(--faint)': FAINT, 'var(--fix)': YEL, 'var(--ground)': '#ffffff',
        'var(--raise)': '#ffffff', 'var(--surface)': '#F2F2F0', 'var(--line)': '#E2E2DC', 'var(--lap-frame)': '#2c2c2e',
        'var(--lap-base)': '#d4d4d9', 'var(--lap-notch)': '#b4b4ba', 'var(--lap-scr)': '#ffffff', 'var(--display)': 'Inter', 'var(--hand)': 'Shantell Sans Light'}
def devar(s):
    s = re.sub(r'style=([^"\s>]+)', r'style="\1"', s)
    s = s.replace('&nbsp;', '&#160;').replace('&middot;', '&#183;').replace('&ndash;', '&#8211;')
    for k, v in VARS.items(): s = s.replace(k, v)
    s = s.replace('Shantell Sans, ', 'Shantell Sans Light, ')
    return s.replace('currentColor', INK)

def hero_svg():
    s = re.search(r'<svg class="hx".*?</svg>', SITE, re.S).group(0)
    s = re.sub(r'stroke-dashoffset:[^;"]+;?', '', s)              # konečný stav animace
    s = re.sub(r'<text[^>]*class="hx-cs"[^>]*>.*?</text>', '', s)  # druhá jazyková varianta pryč
    s = re.sub(r'<g class="hx-bulb" transform="translate\(([\d.]+) ([\d.]+)\)', r'<g class="hx-bulb" transform="translate(\1 \2)', s)
    s = devar(s)
    return re.sub(r'^<svg class="hx"', '<svg', s)

def ill(kind):
    m = re.search(r'<div class="svc-hero-ill"><svg class="ill ill-' + kind + r'".*?</svg></div>', SITE, re.S)
    s = m.group(0)[len('<div class="svc-hero-ill">'):-len('</div>')]
    return devar(re.sub(r'^<svg class="[^"]*"', '<svg', s))
ILL_CSS = '''.ill-t{font-family:Shantell Sans Light;font-size:14px;fill:#6e6e73}.ill-d{font-family:Inter;font-size:13px;font-weight:700;fill:#6e6e73}
.don{fill:#111111}.ill-off{fill:#F2F2F0;stroke:#E2E2DC;stroke-width:1.5}.ill-soft{opacity:.35}.ill-node,.ill-scr{fill:#ffffff}
.lap-frame{fill:#2c2c2e}.lap-base{fill:#d4d4d9}.lap-scr{fill:#ffffff}.ill-q{font-family:Inter;font-size:18px;font-weight:700;fill:#111111}
.num{fill:#FFCE1B;stroke:#FFCE1B}.numt{fill:#111111}.wk{display:none}'''

def logo_src(alt):
    m = re.search(r'<img class="card-logo" src="(data:[^"]+)" alt="' + alt + '">', SITE)
    return m.group(1) if m else None

def wrap_lines(text, font, size, maxw, ls=0.0):
    f = ImageFont.truetype(font, size); lines = []
    for para in text.split('\n'):
        cur = ''
        for w_ in para.split(' '):
            t = (cur + ' ' + w_).strip()
            if f.getlength(t) + ls * len(t) <= maxw or not cur: cur = t
            else: lines.append(cur); cur = w_
        lines.append(cur)
    return lines, f

def headline(text, mark, x, y, size, maxw):
    """Vrátí SVG s nadpisem; slovo/fráze `mark` dostane žlutý podklad jako na webu."""
    ls = -size * 0.035
    lines, f = wrap_lines(text, F700, size, maxw, ls)
    out = []; lh = size * 1.08
    L = lambda t: f.getlength(t) + ls * len(t)
    for i, ln in enumerate(lines):
        by = y + i * lh
        if mark and mark in ln:
            pre = ln[:ln.index(mark)]; x0 = x + L(pre); wd = L(mark)
            out.append(f'<rect x="{x0-6:.1f}" y="{by-size*0.52:.1f}" width="{wd+12:.1f}" height="{size*0.46:.1f}" fill="{YEL}"/>')
        out.append(f'<text x="{x}" y="{by:.1f}" font-family="Inter" font-weight="700" font-size="{size}" letter-spacing="{-size*0.035:.2f}" fill="{INK}">{html.escape(ln)}</text>')
    return ''.join(out), y + (len(lines) - 1) * lh

from lockup import mark as _pk_mark
PK_VB = tuple(float(v) for v in re.search(r'viewBox="([^"]+)"', open(R + 'Career/05 Web/repo/logo/pk/pk-svetle.svg').read()).group(1).split())
PK_BODY = _pk_mark(INK, INK); PK_H = 66
def frame(inner, extra_css=''):
    dots = ''.join(f'<circle cx="{cx}" cy="{cy}" r="1.3" fill="#E6E6E0"/>' for cx in range(14, W, 26) for cy in range(14, H, 26))
    # logo pk (písmo + linka + post-it) a jméno
    bw = PK_H * PK_VB[2] / PK_VB[3]
    brand = (f'<svg x="58" y="40" width="{bw:.1f}" height="{PK_H}" viewBox="{" ".join(map(str, PK_VB))}">{PK_BODY}</svg>'
             f'<text x="{58 + bw + 14:.1f}" y="79" font-family="Inter" font-weight="700" font-size="24" letter-spacing="-0.5" fill="{INK}">Pavel Kroupa</text>'
             f'<text x="{W-64}" y="79" text-anchor="end" font-family="Inter" font-weight="500" font-size="20" fill="{FAINT}">pavelkroupa.com</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<style>{ILL_CSS}{extra_css}</style><rect width="{W}" height="{H}" fill="#ffffff"/>{dots}{brand}{inner}</svg>')

def render(name, svg):
    for scale, suf in ((2, '@2x'), (1, '')):
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=W * scale, output_height=H * scale)
        if scale == 1:  # 1× zmenšit z 2×, ať jsou hrany čisté
            png2 = cairosvg.svg2png(bytestring=svg.encode(), output_width=W * 2, output_height=H * 2)
            im = Image.open(io.BytesIO(png2)).convert('RGB').resize((W, H), Image.LANCZOS)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=True); png = b.getvalue()
        else:
            im = Image.open(io.BytesIO(png)).convert('RGB'); b = io.BytesIO(); im.save(b, 'PNG', optimize=True); png = b.getvalue()
        for d in (OUT, REPO):
            open(f'{d}{name}{suf}.png', 'wb').write(png)

def sub(text, x, y, size=27, maxw=600, col=MUTED):
    lines, f = wrap_lines(text, F500, size, maxw)
    return ''.join(f'<text x="{x}" y="{y + i*size*1.35:.1f}" font-family="Inter" font-weight="500" font-size="{size}" fill="{col}">{html.escape(l)}</text>' for i, l in enumerate(lines))

# 1) úvod
h, yb = headline('Pomáhám týmům rozhodnout, co postavit.', 'rozhodnout', 64, 205, 74, 1060)
s = sub('Funkční prototyp a hotové zadání. S AI za dny, ne týdny.', 64, yb + 62, 28, 1000)
hero = hero_svg().replace('<svg ', '<svg x="40" y="360" width="1120" height="246" preserveAspectRatio="xMidYMid meet" ', 1)
render('og-uvod', frame(h + s + hero))

# 2–4) služby: text vlevo, infografika vpravo
SVCS = [('og-decision-prototype', 'dp', 'Decision Prototype', 'Funkční prototyp\nza pár dní.', 'Funkční prototyp', 'Jeden den, dva, nebo týden.\nOd 49 000 Kč.'),
        ('og-audit', 'au', 'Audit rozhodnutí', 'Zjistěte, co váš produkt brzdí.\nZa pět dní.', 'brzdí', 'Nahrávka obrazovky a seznam podle priority.\nOd 29 000 Kč.'),
        ('og-vedeni-produktu', 'fr', 'Vedení produktu a designu na část úvazku', 'Vedení produktu, dokud nenajdete stálého člověka.', 'Vedení produktu', 'Dva dny v týdnu ve vašem týmu.\nOd 120 000 Kč měsíčně.')]
for name, kind, eyebrow, title, mark, lede in SVCS:
    eb = f'<text x="64" y="186" font-family="Inter" font-weight="600" font-size="24" fill="{FAINT}">{html.escape(eyebrow)}</text>'
    h, yb = headline(title, mark, 64, 268, 66, 640)
    s = sub(lede, 64, yb + 64, 26, 600)
    ill_svg = ill(kind).replace('<svg ', '<svg x="720" y="150" width="440" height="380" preserveAspectRatio="xMidYMid meet" ', 1)
    render(name, frame(eb + h + s + ill_svg))

# 5) portfolio: loga případů
eb = f'<text x="64" y="186" font-family="Inter" font-weight="600" font-size="24" fill="{FAINT}">Portfolio</text>'
h, yb = headline('Čtyři firmy. Čtyři zaseknuté produkty.', 'zaseknuté', 64, 268, 70, 1000)
s = sub('Případy z regulovaného krypta, zdravotnictví a e-commerce.', 64, yb + 62, 27, 1000)
logos = ''; x = 64
for alt, hgt, wd in (('Coinmate', 64, 112), ('Leeaf', 36, 86), ('Heirloom', 30, 168)):
    src = logo_src(alt)
    if src:
        logos += f'<image x="{x}" y="{520 - hgt/2:.0f}" width="{wd}" height="{hgt}" preserveAspectRatio="xMinYMid meet" xlink:href="{src}"/>'
        x += wd + 70
logos += f'<text x="{x}" y="531" font-family="Inter" font-weight="700" font-size="30" letter-spacing="1" fill="#8e8e93">BRENO</text>'
render('og-portfolio', frame(eb + h + s + logos))
print(sorted(os.listdir(OUT)))
