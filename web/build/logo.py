# Logo P✓: písmeno P (Inter 700, převedené na křivky) + check kreslený tužkou.
# Check stojí na účaří jako malé písmeno, takže se čte "Pk".
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import B, R, CAREER, FONTDIR, DRAFT
import math, random, io, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import cairosvg
from PIL import Image

FONTS = {w: TTFont(f'{FONTDIR}Inter-{w}-full.ttf') for w in (600, 700)}
INK, PAPER, YEL, WHITE = '#111111', '#FFFFFF', '#FFCE1B', '#F5F5F7'

def text_path(txt, size, x, y, weight=700, track=0.0):
    """Text jako SVG cesta (bez závislosti na fontu). Vrací (d, šířka)."""
    f = FONTS[weight]; gs = f.getGlyphSet(); cmap = f.getBestCmap(); s = size / f['head'].unitsPerEm
    pen = SVGPathPen(gs); x0 = x
    for ch in txt:
        g = gs[cmap[ord(ch)]]
        g.draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
        x += g.width * s + track * size
    return pen.getCommands(), x - x0

# ---------- check tužkou ----------
def _bez(p0, p1, p2, p3, n):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return out
def _qb(p0, p1, p2, n):
    return [((1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0], (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1])
            for t in (i / n for i in range(n + 1))]
def _sub(a, b): return (a[0]-b[0], a[1]-b[1])
def _len(a): return math.hypot(*a)
def _lerp(a, b, t): return (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)

def check(A, V, E, w, bowA=(0, 0), bowE=(0, 0), r=None, seed=3, rough=1.0, w_start=.6, w_end=.32, taper=.38):
    """Obrys tahu A→V→E s proměnnou šířkou a lehce nerovnými hranami."""
    r = r if r is not None else w * .7
    V1 = _lerp(V, A, r / _len(_sub(A, V))); V2 = _lerp(V, E, r / _len(_sub(E, V)))
    seg1 = _bez(A, _lerp(A, V1, .33) if bowA == (0, 0) else (A[0] + bowA[0], A[1] + bowA[1]), _lerp(A, V1, .7), V1, 40)
    arc = _qb(V1, V, V2, 12)
    mid = _lerp(V2, E, .5)
    seg2 = _bez(V2, _lerp(V2, E, .3), (mid[0] + bowE[0], mid[1] + bowE[1]), E, 90)
    pts = seg1 + arc[1:] + seg2[1:]
    # délka podél tahu
    L = [0.0]
    for i in range(1, len(pts)): L.append(L[-1] + _len(_sub(pts[i], pts[i-1])))
    tot = L[-1]
    rnd = random.Random(seed)
    ph = [rnd.random() * 6.283 for _ in range(6)]
    jit = [rnd.uniform(-1, 1) for _ in pts]
    jit = [(jit[max(i-1, 0)] + jit[i] + jit[min(i+1, len(jit)-1)]) / 3 for i in range(len(jit))]
    left, right = [], []
    for i, p in enumerate(pts):
        s = L[i] / tot
        if s < .12: k = w_start + (1 - w_start) * (s / .12) ** .7
        elif s > 1 - taper: k = 1 - (1 - w_end) * ((s - (1 - taper)) / taper) ** 1.4
        else: k = 1
        a = pts[max(i-1, 0)]; b = pts[min(i+1, len(pts)-1)]
        tx, ty = _sub(b, a); n = _len((tx, ty)) or 1; nx, ny = -ty / n, tx / n
        nl = 1 + rough * (.05 * math.sin(6.283 * 3 * s + ph[0]) + .03 * math.sin(6.283 * 8 * s + ph[1]) + .035 * jit[i])
        nr = 1 + rough * (.05 * math.sin(6.283 * 4 * s + ph[2]) + .03 * math.sin(6.283 * 9 * s + ph[3]) - .035 * jit[i])
        h = w * k / 2
        left.append((p[0] + nx * h * nl, p[1] + ny * h * nl)); right.append((p[0] - nx * h * nr, p[1] - ny * h * nr))
    def cap(c, p_from, p_to, rad, n=10):
        a0 = math.atan2(p_from[1]-c[1], p_from[0]-c[0]); a1 = math.atan2(p_to[1]-c[1], p_to[0]-c[0])
        d = (a1 - a0) % 6.283
        if d > 3.1416: d -= 6.283  # kratší oblouk na vnější stranu
        return [(c[0] + rad*math.cos(a0 + d*j/n), c[1] + rad*math.sin(a0 + d*j/n)) for j in range(1, n)]
    def outward_cap(c, pa, pb, dirv, rad, n=10):
        # půlkruh od pa do pb přes bod c + dirv*rad
        a0 = math.atan2(pa[1]-c[1], pa[0]-c[0]); am = math.atan2(dirv[1], dirv[0])
        d = (am - a0) % 6.283
        if d > 3.1416: d -= 6.283
        return [(c[0] + rad*math.cos(a0 + 2*d*j/n), c[1] + rad*math.sin(a0 + 2*d*j/n)) for j in range(1, n)]
    endc = pts[-1]; d_end = _sub(pts[-1], pts[-4]); de = _len(d_end); d_end = (d_end[0]/de, d_end[1]/de)
    stc = pts[0]; d_st = _sub(pts[0], pts[3]); ds = _len(d_st); d_st = (d_st[0]/ds, d_st[1]/ds)
    poly = left + outward_cap(endc, left[-1], right[-1], d_end, _len(_sub(left[-1], endc))) + right[::-1] \
        + outward_cap(stc, right[0], left[0], d_st, _len(_sub(right[0], stc)))
    return 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in poly) + ' Z', poly

def grain(poly, density, seed=7, rmin=.18, rmax=.42):
    """Drobné průsvitné tečky uvnitř tahu = zrno tužky (jen pro velké formáty)."""
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    rnd = random.Random(seed); out = []
    def inside(x, y):
        c = False; j = len(poly) - 1
        for i in range(len(poly)):
            xi, yi = poly[i]; xj, yj = poly[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: c = not c
            j = i
        return c
    step = 1 / math.sqrt(density)
    y = min(ys)
    while y < max(ys):
        x = min(xs)
        while x < max(xs):
            px, py = x + rnd.uniform(0, step), y + rnd.uniform(0, step)
            if inside(px, py) and rnd.random() < .55:
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{rnd.uniform(rmin, rmax):.2f}"/>')
            x += step
        y += step
    return ''.join(out)

# ---------- varianty ----------
SIZE = 100; B = 100  # velikost písma, účaří
P_D, P_W = text_path('P', SIZE, 0, B, 700)
CAP = SIZE * 1490 / 2048; XH = SIZE * 1118 / 2048

VARIANTS = {
    # A: check jako písmeno - stejná váha jako P, stojí na účaří, dlouhé rameno do výšky verzálky (jako dřík k)
    'A': dict(A=(70, B - 38), V=(84.5, B + 1), E=(121, B - CAP - 1), w=13.4, bowE=(-2.5, 1.5), r=7, rough=.55, w_start=.78, w_end=.62, taper=.3),
    # B: gesto tužkou - tenčí, přetažené nad verzálku, ostřejší konec
    'B': dict(A=(70, B - 34), V=(84, B + 2), E=(128, B - CAP - 12), w=8.2, bowE=(-4, 2.5), r=4.5, rough=1.25, w_start=.7, w_end=.45, taper=.45, seed=11),
    # E: dřík malého k jako písmo + check tužkou místo ramen k
    'E': dict(A=(81.5, B - 40), V=(95, B + 1.5), E=(126, B - XH - 9), w=8.6, bowE=(-3, 2), r=4.5, rough=1.2, w_start=.75, w_end=.45, taper=.42, seed=5),
}
STEM_X = P_W + 6.25; STEM_W = 13.3
def mark(v, p_fill, c_fill, marker=False, grain_on=False, pad=8):
    cfg = VARIANTS[v]; d, poly = check(**cfg)
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    x0 = min(0, min(xs)) - pad; x1 = max(xs) + pad; y0 = min(B - CAP, min(ys)) - pad; y1 = max(B, max(ys)) + pad
    m = ''
    if marker:
        m = f'<path d="M{-4} {B-31} L{max(xs)+3} {B-34} L{max(xs)+5} {B-3} L{-3} {B-1} Z" fill="{YEL}"/>'
    g = ''
    if grain_on:
        g = f'<g fill="{grain_on}" fill-opacity=".42">{grain(poly, 1.6)}</g>'
    if marker == 'check':
        m = f'<path d="M{min(xs)-4:.1f} {B-40} L{max(xs)+2:.1f} {B-44} L{max(xs)+4:.1f} {B-6} L{min(xs)-3:.1f} {B-3} Z" fill="{YEL}"/>'
    st = f'<rect x="{STEM_X:.2f}" y="{B-CAP:.2f}" width="{STEM_W}" height="{CAP:.2f}" fill="{p_fill}"/>' if v == 'E' else ''
    body = f'{m}<path d="{P_D}" fill="{p_fill}"/>{st}<path d="{d}" fill="{c_fill}"/>{g}'
    return body, (x0, y0, x1 - x0, y1 - y0)

def svg(body, box, bg=None, w=None, h=None, extra=''):
    x, y, bw, bh = box
    bgr = f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="{bg}"/>' if bg else ''
    wh = f' width="{w}" height="{h}"' if w else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.2f} {y:.2f} {bw:.2f} {bh:.2f}"{wh}>{bgr}{body}{extra}</svg>'

def png(s, width):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=width))).convert('RGBA')

if __name__ == '__main__':
    from PIL import ImageDraw, ImageFont
    OUT = DRAFT; os.makedirs(OUT, exist_ok=True)
    rows = [('A', False, 'A  písmeno: check má váhu písma'), ('B', False, 'B  tužka: tenký tah se zrnem'),
            ('B', 'check', 'C  tužka + žlutá pod checkem')]
    RH = 360; sheet = Image.new('RGB', (1760, 40 + RH * len(rows)), '#e9e9e6')
    dr = ImageDraw.Draw(sheet); lab = ImageFont.truetype(FONTDIR + 'Inter-600-full.ttf', 20)
    def fit(im, h): return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    for i, (v, mk, name) in enumerate(rows):
        y = 20 + i * RH
        dr.text((22, y), name, font=lab, fill='#333')
        for k, (bg, pf, cf, gr) in enumerate(((PAPER, INK, INK, PAPER), ('#111111', WHITE, YEL if not mk else WHITE, '#111111'))):
            body, box = mark(v, pf, cf, marker=mk if k == 0 else False, grain_on=gr if v != 'A' else False)
            tile = Image.new('RGB', (520, 300), bg); im = fit(png(svg(body, box), 1200), 240)
            tile.paste(im, ((520 - im.width) // 2, 30), im); sheet.paste(tile, (20 + k * 540, y + 30))
        hdr = Image.new('RGB', (580, 300), PAPER); d2 = ImageDraw.Draw(hdr)
        hb, hbox = mark(v, INK, INK, marker=mk, pad=1)
        for j, hh in enumerate((16, 22, 34)):
            im = png(svg(hb, hbox), int(hbox[2] * hh / hbox[3] * 1))
            yy = 30 + j * 85; hdr.paste(im, (24, yy), im)
            f2 = ImageFont.truetype(FONTDIR + 'Inter-600-full.ttf', int(hh * .62))
            d2.text((24 + im.width + int(hh * .5), yy + hh * .3), 'Pavel Kroupa', font=f2, fill=INK)
        # favicon 32 a 16
        fb, fbox = mark(v, INK, INK, pad=1)
        for j, px in enumerate((32, 16)):
            fx = 380 + j * 60
            sq = Image.new('RGBA', (px, px), YEL); im = fit(png(svg(fb, fbox), 400), int(px * .62))
            sq.paste(im, ((px - im.width) // 2, (px - im.height) // 2), im); hdr.paste(sq, (fx, 40), sq)
        sheet.paste(hdr, (1100, y + 30))
    sheet.save(OUT + 'varianty.png'); print('ok')
