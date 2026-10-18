"""Spouštět z kořene repozitáře: python3 _tools/case-diagrams.py
Diagramy případů: jak to proběhlo. Každý případ má verzi pro počítač (dg-d) a pro mobil (dg-m), CS a EN.
Barvy jen z proměnných webu (.dg třídy), animace z .ill (.ia, .ln, .pop, .grow)."""
import math, re, sys, html

def esc(s): return html.escape(s, quote=False)

class D:
    def __init__(s, w, h, cls, aria, t0=0.2, step=0.32):
        s.w, s.h, s.cls, s.aria, s.t, s.step, s.o = w, h, cls, aria, t0, step, []
    def tick(s, k=1.0):
        v = s.t; s.t += s.step * k; return f"{v:.2f}s"
    def add(s, x): s.o.append(x)
    def svg(s):
        return (f'<svg class="ill dg cdg {s.cls}" viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{esc(s.aria)}">'
                + "".join(s.o) + "</svg>")

def rr(x, y, w, h, r=14):
    return f"M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z"

def texts(cx, y, lines, cls, anchor="middle"):
    return "".join(f'<text x="{cx}" y="{y+i*18}" text-anchor="{anchor}" class="{cls}">{esc(t)}</text>' for i, t in enumerate(lines))

def box(d, x, y, w, h, title, sub=None, kind="n", num=None, i=None, extra=""):
    """kind: n běžný krok, knot kde se to zaseklo, alt cesta, kterou se nešlo, end výsledek"""
    i = i or d.tick()
    rc = {"n": "dg-n", "knot": "cdg-knot", "alt": "cdg-alt", "end": "dg-end"}[kind]
    tc = "dg-name dg-on" if kind == "end" else ("dg-name cdg-faint" if kind == "alt" else "dg-name")
    sc = "dg-sub dg-on" if kind == "end" else ("dg-sub cdg-faint" if kind == "alt" else "dg-sub")
    tl = title if isinstance(title, list) else [title]
    sl = [] if sub is None else (sub if isinstance(sub, list) else [sub])
    n = len(tl) * 19 + len(sl) * 17
    ty = y + h / 2 - n / 2 + 14
    g = f'<g class="ia" style="--i:{i}"><path d="{rr(x, y, w, h)}" class="{rc}"/>'
    g += "".join(f'<text x="{x+w/2:.1f}" y="{ty+k*19:.1f}" text-anchor="middle" class="{tc}">{esc(t)}</text>' for k, t in enumerate(tl))
    sy = ty + len(tl) * 19 + 2
    g += "".join(f'<text x="{x+w/2:.1f}" y="{sy+k*17:.1f}" text-anchor="middle" class="{sc}">{esc(t)}</text>' for k, t in enumerate(sl))
    if num:
        g += f'<circle cx="{x+16}" cy="{y}" r="11" class="cdg-num"/><text x="{x+16}" y="{y+4}" text-anchor="middle" class="cdg-numt">{num}</text>'
    g += extra + "</g>"
    d.add(g)
    # odhad šířky textu, ať nic nepřeteče
    for t in tl:
        if len(t) * 16 * .56 > w - 16: print("  ! široké:", t, w, file=sys.stderr)
    for t in sl:
        if len(t) * 13 * .52 > w - 14: print("  ! široké:", t, w, file=sys.stderr)

def head(x2, y2, ang, size=7):
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    return f"M{x2+size*math.cos(a1):.1f} {y2+size*math.sin(a1):.1f} L{x2:.1f} {y2:.1f} L{x2+size*math.cos(a2):.1f} {y2+size*math.sin(a2):.1f}"

def arrow(d, path, end, ang, kind="ok", i=None, k=1.0):
    """path: d atribut, end: (x,y) hrot, ang: směr hrotu v radiánech"""
    i = i or d.tick(k)
    if kind == "ok":
        d.add(f'<path class="ln dg-ln" style="--i:{i}" pathLength="1" d="{path}"/>')
        j = f"{float(i[:-1])+.4:.2f}s"
        d.add(f'<path class="ia dg-ln" style="--i:{j}" d="{head(end[0], end[1], ang)}"/>')
    elif kind == "bad":
        d.add(f'<g class="ia" style="--i:{i}"><path class="dg-ln dg-bad" d="{path}"/></g>')
    elif kind == "soft":
        d.add(f'<g class="ia" style="--i:{i}"><path class="dg-ln dg-soft" d="{path}"/></g>')

def xmark(d, x, y, i=None):
    i = i or d.tick(.6)
    d.add(f'<g class="ia dg-x" style="--i:{i}"><circle cx="{x}" cy="{y}" r="10"/><path d="M{x-4} {y-4} L{x+4} {y+4} M{x+4} {y-4} L{x-4} {y+4}"/></g>')

def band(d, x, y, t, i=None, anchor="start"):
    i = i or d.tick(.3)
    d.add(f'<text class="ia dg-band" style="--i:{i}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(t)}</text>')

def note(d, x, y, lines, i=None, anchor="middle", cls="cdg-hand"):
    i = i or d.tick(.4)
    d.add(f'<g class="ia" style="--i:{i}">' + texts(x, y, lines, cls, anchor) + "</g>")

R, L, U, Dn = 0, math.pi, -math.pi / 2, math.pi / 2

# ------------------------------------------------------------------ Heirloom
def heirloom(T, mobile):
    if not mobile:
        d = D(960, 370, "dg-d", T["aria"])
        box(d, 12, 216, 176, 84, T["start"], T["start_s"], "knot")
        # cesta, kterou se nešlo
        band(d, 250, 34, T["alt_band"])
        box(d, 250, 50, 210, 72, T["alt"], T["alt_s"], "alt")
        arrow(d, "M100 216 C100 120 150 86 244 86", None, 0, "bad")
        xmark(d, 138, 128)
        arrow(d, "M188 258 H208", (210, 258), R)
        box(d, 214, 216, 170, 84, T["s1"], T["s1_s"], "n", 1)
        arrow(d, "M384 258 H412", (414, 258), R)
        box(d, 418, 216, 170, 84, T["s2"], T["s2_s"], "n", 2)
        arrow(d, "M588 258 H622", (624, 258), R)
        cx, cy, r = 690, 258, 62
        ring(d, cx, cy, r, T)
        iters(d, cx - 33, cy - r - 30)
        arrow(d, f"M{cx+r} {cy} H786", (788, cy), R)
        box(d, 792, 208, 150, 100, T["end"], T["end_s"], "end")
        return d.svg()
    d = D(340, 600, "dg-m", T["aria"])
    box(d, 20, 16, 300, 66, T["start"], T["start_s"], "knot")
    arrow(d, "M268 82 V120", None, 0, "bad")
    xmark(d, 268, 101)
    box(d, 222, 124, 98, 66, T["alt_m"], T["alt_m_s"], "alt")
    arrow(d, "M100 82 V118", (100, 120), Dn)
    box(d, 20, 124, 186, 66, T["s1_m"], T["s1_s"], "n", 1)
    arrow(d, "M100 190 V226", (100, 228), Dn)
    box(d, 20, 232, 300, 66, T["s2"], T["s2_s"], "n", 2)
    arrow(d, "M170 298 V320", (170, 322), Dn)
    ring(d, 170, 384, 58, T)
    iters(d, 252, 384)
    arrow(d, "M170 442 V476", (170, 478), Dn)
    box(d, 20, 482, 300, 84, T["end"], T["end_s"], "end")
    return d.svg()

def ring(d, cx, cy, r, T):
    i = d.tick()
    d.add(f'<path class="ln dg-ln" style="--i:{i}" pathLength="1" d="M{cx} {cy-r} A{r} {r} 0 1 1 {cx-0.01} {cy-r}"/>')
    # šipky po směru hodin nahoře a dole, vlevo vstup, vpravo výstup
    for a in (0, 180):
        ang = math.radians(a - 90 + 8)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        d.add(f'<path class="ia dg-ln" style="--i:{float(i[:-1])+.5:.2f}s" d="{head(x, y, ang + math.pi/2, 6)}"/>')
    d.add(f'<g class="ia" style="--i:{d.tick(.5)}">' + texts(cx, cy - 3, T["ring"], "dg-sub") + "</g>")

def iters(d, x0, y, n=4, gap=22):
    """Iterace jedna po druhé: žlutá kolečka s čísly v řadě, každé se objeví po předchozím."""
    for k in range(n):
        x = x0 + k * gap
        j = d.tick(1.1)
        d.add(f'<circle class="pop dg-end cdg-it" style="--i:{j}" cx="{x}" cy="{y}" r="12"/>'
              f'<text class="ia cdg-numt2" style="--i:{j}" x="{x}" y="{y+4}" text-anchor="middle">{k+1}</text>')

def heirloom_pipe(T, mobile):
    """Jak fungovala AI pipeline pro prototyp: facilitace, pipeline z repozitáře a design systému,
    hosting na Vercelu, komentáře v prototypu a zpětná vazba zpátky do další verze."""
    if not mobile:
        d = D(960, 316, "dg-d", T["p_aria"])
        box(d, 20, 120, 176, 84, T["p1"], T["p1_s"], "n", 1)
        arrow(d, "M196 162 H212", (214, 162), R)
        i = d.tick()
        for k, (x, w, t) in enumerate(((190, 104, T["p_in"][0]), (306, 124, T["p_in"][1]))):
            d.add(f'<g class="ia" style="--i:{float(i[:-1])+k*.15:.2f}s"><path d="{rr(x, 28, w, 34, 17)}" class="cdg-chip"/>'
                  f'<text x="{x+w/2}" y="50" text-anchor="middle" class="dg-s cdg-ink">{esc(t)}</text></g>')
        d.t = float(i[:-1]) + .3
        arrow(d, "M242 62 C242 92 290 90 296 114", (297, 116), math.radians(70))
        arrow(d, "M368 62 C368 92 322 90 316 114", (315, 116), math.radians(110))
        box(d, 218, 120, 176, 84, T["p2"], T["p2_s"], "n", 2)
        arrow(d, "M394 162 H410", (412, 162), R)
        box(d, 416, 120, 176, 84, T["p3"], T["p3_s"], "n", 3)
        arrow(d, "M592 162 H608", (610, 162), R)
        box(d, 614, 120, 176, 84, T["p4"], T["p4_s"], "n", 4)
        arrow(d, "M702 204 C702 266 504 266 504 210", (504, 208), U)
        note(d, 603, 288, T["p_loop"])
        arrow(d, "M790 162 H808", (810, 162), R)
        box(d, 814, 108, 126, 108, T["p_end"], T["p_end_s"], "end")
        return d.svg()
    d = D(340, 580, "dg-m", T["p_aria"])
    box(d, 20, 16, 276, 64, T["p1"], T["p1_s"], "n", 1)
    arrow(d, "M158 80 V140", (158, 142), Dn)
    i = d.tick()
    for k, (x, t) in enumerate(((20, T["p_in"][0]), (196, T["p_in"][1]))):
        d.add(f'<g class="ia" style="--i:{float(i[:-1])+k*.15:.2f}s"><path d="{rr(x, 94, 124 if k else 110, 32, 16)}" class="cdg-chip"/>'
              f'<text x="{x+(62 if k else 55)}" y="115" text-anchor="middle" class="dg-s cdg-ink">{esc(t)}</text></g>')
    d.t = float(i[:-1]) + .3
    arrow(d, "M75 126 C75 138 110 136 122 142", None, 0, "soft", k=.3)
    arrow(d, "M258 126 C258 138 206 136 194 142", None, 0, "soft", k=.3)
    box(d, 20, 148, 276, 64, T["p2"], T["p2_s"], "n", 2)
    arrow(d, "M158 212 V240", (158, 242), Dn)
    box(d, 20, 248, 276, 64, T["p3"], T["p3_s"], "n", 3)
    arrow(d, "M158 312 V340", (158, 342), Dn)
    box(d, 20, 348, 276, 64, T["p4"], T["p4_s"], "n", 4)
    arrow(d, "M296 380 C334 380 334 280 300 280", (298, 280), L)
    note(d, 158, 436, T["p_loop"])
    arrow(d, "M158 446 V466", (158, 468), Dn)
    box(d, 20, 472, 276, 96, T["p_end"], T["p_end_s"], "end")
    return d.svg()

# ------------------------------------------------------------------ Coinmate
def coinmate(T, mobile):
    if not mobile:
        d = D(960, 404, "dg-d", T["aria"])
        box(d, 20, 40, 170, 84, T["start"], T["start_s"], "knot")
        arrow(d, "M105 124 V300", (105, 302), Dn)
        note(d, 116, 214, T["first"], anchor="start")
        i = d.tick()
        d.add(f'<g class="ia" style="--i:{i}"><path d="{rr(20, 308, 920, 76, 16)}" class="grow cdg-base" style="--i:{i}"/></g>')
        d.add(f'<g class="ia" style="--i:{d.tick(1.5)}"><circle cx="36" cy="308" r="11" class="cdg-num cdg-num-on"/><text x="36" y="312" text-anchor="middle" class="cdg-numt cdg-numt-on">1</text><text x="44" y="341" class="dg-band cdg-on-base">{esc(T["ds"])}</text><text x="44" y="363" class="dg-sub cdg-on-base2">{esc(T["ds_s"])}</text></g>')
        xs = [(230, T["s1"], T["s1_s"], 2), (420, T["s2"], T["s2_s"], 3), (610, T["s3"], T["s3_s"], 4)]
        for x, t, s, n in xs:
            box(d, x, 170, 160, 84, t, s, "n", n)
            arrow(d, f"M{x+80} 254 V306", None, 0, "soft", k=.4)
        arrow(d, "M390 212 H414", (416, 212), R)
        arrow(d, "M580 212 H604", (606, 212), R)
        # rebrand: víc konceptů za dny
        band(d, 800, 34, T["rb_band"])
        i = d.tick()
        for k, (dx, rot) in enumerate(((0, -6), (22, 0), (44, 6))):
            d.add(f'<g class="ia" style="--i:{float(i[:-1])+k*.15:.2f}s"><g transform="rotate({rot} {830+dx} 80)"><path d="{rr(800+dx, 48, 60, 64, 10)}" class="dg-n"/>'
                  f'<circle cx="{830+dx}" cy="72" r="9" class="{"dg-end" if k == 2 else "cdg-dot"}"/><path d="M{816+dx} 94 H{844+dx}" class="dg-ln cdg-thin"/></g></g>')
        note(d, 786, 72, T["rb"], anchor="end")
        arrow(d, "M770 212 H794", (796, 212), R)
        arrow(d, "M870 126 V164", (870, 166), Dn, k=.3)
        box(d, 800, 170, 140, 84, T["end"], T["end_s"], "end")
        arrow(d, "M870 254 V306", None, 0, "soft", k=.4)
        return d.svg()
    d = D(340, 760, "dg-m", T["aria"])
    box(d, 20, 16, 300, 66, T["start"], T["start_s"], "knot")
    arrow(d, "M42 82 V118", (42, 120), Dn)
    i = d.tick()
    d.add(f'<g class="ia" style="--i:{i}"><path d="{rr(20, 124, 44, 616, 14)}" class="cdg-base"/></g>')
    d.add(f'<g class="ia" style="--i:{d.tick()}"><text transform="rotate(-90 48 430)" x="48" y="430" text-anchor="middle" class="dg-band cdg-on-base">{esc(T["ds"])}</text></g>')
    note(d, 84, 108, T["first_m"], anchor="start")
    ys = [(150, T["s1"], T["s1_s"], 2), (262, T["s2"], T["s2_s"], 3), (374, T["s3"], T["s3_s"], 4)]
    for y, t, s, n in ys:
        arrow(d, f"M66 {y+33} H84", None, 0, "soft", k=.3)
        box(d, 84, y, 236, 66, t, s, "n", n)
    arrow(d, "M202 216 V258", (202, 260), Dn); arrow(d, "M202 328 V370", (202, 372), Dn)
    arrow(d, "M202 440 V478", (202, 480), Dn)
    i = d.tick()
    for k, (dx, rot) in enumerate(((0, -6), (22, 0), (44, 6))):
        d.add(f'<g class="ia" style="--i:{float(i[:-1])+k*.15:.2f}s"><g transform="rotate({rot} {130+dx} 520)"><path d="{rr(100+dx, 490, 60, 60, 10)}" class="dg-n"/>'
              f'<circle cx="{130+dx}" cy="512" r="9" class="{"dg-end" if k == 2 else "cdg-dot"}"/><path d="M{116+dx} 534 H{144+dx}" class="dg-ln cdg-thin"/></g></g>')
    note(d, 222, 512, T["rb"], anchor="start")
    arrow(d, "M202 562 V598", (202, 600), Dn)
    arrow(d, "M66 637 H84", None, 0, "soft", k=.3)
    box(d, 84, 604, 236, 84, T["end"], T["end_s"], "end")
    return d.svg()

# ------------------------------------------------------------------ Leeaf
def leeaf(T, mobile):
    if not mobile:
        d = D(960, 380, "dg-d", T["aria"])
        band(d, 20, 30, T["plan"])
        box(d, 20, 48, 160, 64, T["app"], None, "knot")
        for k, (x, t) in enumerate(zip((250, 420, 590), T["copies"])):
            arrow(d, f"M100 112 V132 H{x+75} V116", None, 0, "bad", k=.3)
            box(d, x, 48, 150, 64, t, T["copy_s"], "alt", i=d.tick(.4))
            xmark(d, x + 75, 132)
        note(d, 766, 74, T["plan_n"], anchor="start")
        d.add(f'<path class="ia dg-div" style="--i:{d.tick(.3)}" d="M20 160 H940"/>')
        band(d, 20, 186, T["built"])
        box(d, 20, 206, 170, 96, T["s1"], T["s1_s"], "n", 1)
        arrow(d, "M190 254 H216", (218, 254), R)
        sw = "".join(f'<circle cx="{279+k*22}" cy="286" r="7" class="cdg-sw{k}"/>' for k in range(3))
        box(d, 222, 206, 170, 96, T["s2"], T["s2_s"], "n", 2, extra=sw)
        arrow(d, "M392 254 H418", (420, 254), R)
        box(d, 424, 206, 170, 96, T["s3"], T["s3_s"], "n", 3)
        i = d.tick()
        for k, y in enumerate((196, 240, 284)):
            j = f"{float(i[:-1])+k*.2:.2f}s"
            d.add(f'<path class="ln dg-ln" style="--i:{j}" pathLength="1" d="M594 254 C620 254 618 {y+17} 640 {y+17}"/>')
            d.add(f'<g class="ia" style="--i:{float(j[:-1])+.35:.2f}s"><path d="{rr(646, y, 118, 34, 17)}" class="dg-n"/><circle cx="666" cy="{y+17}" r="6" class="cdg-sw{k}"/>'
                  f'<text x="680" y="{y+22}" class="dg-s cdg-ink">{esc(T["clinic"])} {k+1}</text></g>')
            d.add(f'<path class="ln dg-ln" style="--i:{float(j[:-1])+.7:.2f}s" pathLength="1" d="M764 {y+17} C786 {y+17} 784 254 804 254"/>')
        d.t = float(i[:-1]) + 1.4
        d.add(f'<path class="ia dg-ln" style="--i:{d.tick()}" d="{head(806, 254, R)}"/>')
        box(d, 812, 200, 130, 108, T["end"], T["end_s"], "end")
        note(d, 704, 346, T["admin"], anchor="middle")
        return d.svg()
    d = D(340, 800, "dg-m", T["aria"])
    band(d, 20, 22, T["plan"])
    box(d, 20, 36, 300, 52, T["app"], None, "knot")
    for k, x in enumerate((20, 125, 230)):
        arrow(d, f"M170 88 C170 108 {x+45} 104 {x+45} 124", None, 0, "bad", k=.3)
        box(d, x, 128, 90, 56, T["copies_m"][k], None, "alt", i=d.tick(.3))
    xmark(d, 170, 104)
    d.add(f'<path class="ia dg-div" style="--i:{d.tick(.3)}" d="M20 214 H320"/>')
    band(d, 20, 246, T["built"])
    box(d, 20, 262, 300, 70, T["s1"], T["s1_s"], "n", 1)
    arrow(d, "M170 332 V356", (170, 358), Dn)
    sw = "".join(f'<circle cx="{268+k*18}" cy="397" r="6" class="cdg-sw{k}"/>' for k in range(3))
    box(d, 20, 362, 300, 70, T["s2"], T["s2_s"], "n", 2, extra=sw)
    arrow(d, "M170 432 V456", (170, 458), Dn)
    box(d, 20, 462, 300, 70, T["s3"], T["s3_s"], "n", 3)
    i = d.tick()
    for k, x in enumerate((20, 125, 230)):
        j = f"{float(i[:-1])+k*.2:.2f}s"
        d.add(f'<path class="ln dg-ln" style="--i:{j}" pathLength="1" d="M170 532 C170 552 {x+45} 548 {x+45} 566"/>')
        d.add(f'<g class="ia" style="--i:{float(j[:-1])+.35:.2f}s"><path d="{rr(x, 570, 90, 40, 20)}" class="dg-n"/><circle cx="{x+18}" cy="590" r="6" class="cdg-sw{k}"/>'
              f'<text x="{x+30}" y="595" class="dg-s cdg-ink">{esc(T["clinic_m"])} {k+1}</text></g>')
        d.add(f'<path class="ln dg-ln" style="--i:{float(j[:-1])+.7:.2f}s" pathLength="1" d="M{x+45} 610 C{x+45} 628 170 626 170 646"/>')
    d.t = float(i[:-1]) + 1.4
    d.add(f'<path class="ia dg-ln" style="--i:{d.tick()}" d="{head(170, 648, Dn)}"/>')
    box(d, 20, 654, 300, 90, T["end"], T["end_s"], "end")
    return d.svg()

# ------------------------------------------------------------------ BRENO
def breno(T, mobile):
    cards = T["cards"]
    def card(d, x, y, rot, t, i):
        d.add(f'<g class="ia" style="--i:{i}"><g transform="rotate({rot} {x+68} {y+17})"><path d="{rr(x, y, 136, 34, 9)}" class="dg-n"/>'
              f'<text x="{x+12}" y="{y+22}" class="dg-s cdg-ink">{esc(t)}</text>'
              f'<circle cx="{x+120}" cy="{y+17}" r="9" class="cdg-bang"/><text x="{x+120}" y="{y+21.5}" text-anchor="middle" class="cdg-bangt">!</text></g></g>')
    if not mobile:
        d = D(960, 400, "dg-d", T["aria"])
        band(d, 20, 34, T["b_band"])
        pos = [(20, 56, -3), (172, 62, 4), (34, 108, 3), (178, 116, -4), (18, 160, -2), (166, 170, 3)]
        i = d.tick()
        for k, ((x, y, r), t) in enumerate(zip(pos, cards)):
            card(d, x, y, r, t, f"{float(i[:-1])+k*.12:.2f}s")
        d.t = float(i[:-1]) + .9
        note(d, 166, 244, T["b_note"])
        note(d, 166, 268, T["roles"], cls="dg-sub")
        arrow(d, "M322 148 H348", (350, 148), R)
        # workshop, dva dny
        i = d.tick()
        d.add(f'<g class="ia" style="--i:{i}"><path d="{rr(356, 40, 250, 232, 20)}" class="cdg-alt"/>'
              f'<text x="376" y="66" class="dg-band">{esc(T["ws"])}</text></g>')
        box(d, 376, 84, 210, 76, T["d1"], T["d1_s"], "n", 1)
        arrow(d, "M481 160 V178", (481, 180), Dn, k=.5)
        box(d, 376, 184, 210, 76, T["d2"], T["d2_s"], "n", 2)
        arrow(d, "M606 148 H630", (632, 148), R)
        # pořadí s argumenty
        band(d, 636, 34, T["order_band"])
        i = d.tick()
        for k in range(5):
            y = 50 + k * 44
            j = f"{float(i[:-1])+k*.15:.2f}s"
            d.add(f'<g class="ia" style="--i:{j}"><path d="{rr(636, y, 154, 34, 9)}" class="{"dg-end" if k == 0 else "dg-n"}"/>'
                  f'<text x="652" y="{y+22}" class="cdg-numt2">{k+1}</text><path d="M672 {y+17} H{766-k*14}" class="dg-ln cdg-thin {"cdg-on-end" if k == 0 else ""}"/></g>')
        d.t = float(i[:-1]) + 1
        note(d, 713, 292, T["order_n"])
        arrow(d, "M790 148 H818", (820, 148), R)
        box(d, 824, 96, 118, 104, T["end"], T["end_s"], "end")
        box(d, 636, 322, 306, 58, T["next"], T["next_s"], "n", 3)
        arrow(d, "M883 200 V316", (883, 318), Dn)
        return d.svg()
    d = D(340, 820, "dg-m", T["aria"])
    band(d, 20, 24, T["b_band"])
    pos = [(20, 40, -3), (180, 46, 4), (30, 88, 3), (174, 96, -4), (18, 138, -2), (184, 144, 3)]
    i = d.tick()
    for k, ((x, y, r), t) in enumerate(zip(pos, cards)):
        card(d, x, y, r, t, f"{float(i[:-1])+k*.12:.2f}s")
    d.t = float(i[:-1]) + .9
    note(d, 170, 212, T["b_note_m"])
    arrow(d, "M170 228 V256", (170, 258), Dn)
    i = d.tick()
    d.add(f'<g class="ia" style="--i:{i}"><path d="{rr(20, 264, 300, 218, 20)}" class="cdg-alt"/>'
          f'<text x="40" y="290" class="dg-band">{esc(T["ws"])}</text></g>')
    box(d, 40, 304, 260, 70, T["d1"], T["d1_s"], "n", 1)
    arrow(d, "M170 374 V390", (170, 392), Dn, k=.5)
    box(d, 40, 396, 260, 70, T["d2"], T["d2_s"], "n", 2)
    arrow(d, "M170 482 V506", (170, 508), Dn)
    i = d.tick()
    for k in range(5):
        y = 514 + k * 40
        j = f"{float(i[:-1])+k*.15:.2f}s"
        d.add(f'<g class="ia" style="--i:{j}"><path d="{rr(20, y, 150, 32, 9)}" class="{"dg-end" if k == 0 else "dg-n"}"/>'
              f'<text x="36" y="{y+21}" class="cdg-numt2">{k+1}</text><path d="M56 {y+16} H{140-k*12}" class="dg-ln cdg-thin {"cdg-on-end" if k == 0 else ""}"/></g>')
    d.t = float(i[:-1]) + 1
    arrow(d, "M170 594 H186", (188, 594), R)
    box(d, 192, 540, 128, 108, T["end"], T["end_s"], "end")
    arrow(d, "M256 648 V720", (256, 722), Dn)
    box(d, 20, 728, 300, 66, T["next"], T["next_s"], "n", 3)
    return d.svg()


# ------------------------------------------------------------------ BRENO: před a po workshopu
def chip(d, x, y, w, h, t, kind="n", i=None):
    box(d, x, y, w, h, t, None, kind, None, i)

def breno_plan(T, mobile):
    """Plán spolupráce ve třech fázích (analýza před workshopem): setup, UX základy, aplikace a rozvoj."""
    def phase(d, x, n, name, sub, dy=0):
        i = d.tick(.5)
        d.add(f'<g class="ia" style="--i:{i}"><circle cx="{x+11}" cy="{26+dy}" r="11" class="cdg-num"/><text x="{x+11}" y="{30+dy}" text-anchor="middle" class="cdg-numt">{n}</text>'
              f'<text x="{x+30}" y="{31+dy}" class="dg-band">{esc(name)}</text>' + texts(x, 56 + dy, sub, "dg-s", "start") + "</g>")
    if not mobile:
        d = D(960, 520, "dg-d dg-plan", T["pl_aria"], step=.2)
        Y = 266
        d.add(f'<path class="ia dg-div" style="--i:{d.tick(.3)}" d="M282 14 V500"/>')
        phase(d, 12, 1, T["ph1"], T["ph1_s"])
        box(d, 12, Y-50, 128, 100, T["start"], None, "knot")
        arrow(d, f"M140 {Y} H160", (162, Y), R)
        box(d, 164, Y-35, 108, 70, T["audit"], None, "n")
        box(d, 164, 346, 108, 64, T["audits"], T["audits_s"], "alt")
        arrow(d, "M218 301 V344", (218, 346), Dn, k=.6)
        box(d, 296, 346, 100, 64, T["da"], None, "alt")
        arrow(d, "M262 301 C268 326 280 348 292 362", (294, 364), math.radians(40), k=.6)
        phase(d, 296, 2, T["ph2"], T["ph2_s"])
        arrow(d, f"M272 {Y} H292", (294, Y), R)
        box(d, 296, Y-35, 100, 70, T["wsx"], None, "n")
        for cy, t in ((202, T["rolesx"]), (266, T["ds"]), (330, T["ux"])):
            arrow(d, f"M396 {Y} C410 {Y} 410 {cy} 420 {cy}", (422, cy), R, k=.5)
            box(d, 424, cy-28, 116, 56, t, None, "n")
        box(d, 568, 112, 124, 48, T["camp_ops"], None, "alt")
        for cy, t in ((202, T["g1"]), (266, T["g2"]), (330, T["g3"]), (394, T["g4"])):
            arrow(d, f"M540 266 C556 266 556 {cy} 564 {cy}", (566, cy), R, k=.4)
            box(d, 568, cy-28, 124, 56, t, None, "n")
        box(d, 568, 432, 124, 48, T["soc_ops"], None, "alt")
        phase(d, 706, 3, T["ph3"], T["ph3_s"])
        box(d, 706, 200, 112, 56, T["brand"], None, "end")
        box(d, 706, 272, 112, 72, T["concept"], None, "end")
        box(d, 830, 160, 112, 76, T["rev"], None, "n")
        box(d, 830, 250, 112, 60, T["test"], None, "n")
        box(d, 830, 324, 112, 60, T["camp"], None, "n")
        arrow(d, "M218 231 V98 H698 V308 H702", (704, 308), R, "soft", k=.6)
        arrow(d, "M346 410 V492 H760 V348", (760, 346), U, "soft", k=.6)
        return d.svg()
    d = D(340, 1120, "dg-m dg-plan", T["pl_aria"], step=.2)
    phase(d, 20, 1, T["ph1"], T["ph1_s"])
    box(d, 20, 96, 300, 56, T["start_m"], None, "knot")
    arrow(d, "M170 152 V172", (170, 174), Dn)
    box(d, 20, 178, 300, 50, T["audit"], None, "n")
    arrow(d, "M95 228 V250", (95, 252), Dn, k=.5)
    arrow(d, "M245 228 V250", (245, 252), Dn, k=.5)
    box(d, 20, 256, 148, 64, T["audits"], T["audits_s"], "alt")
    box(d, 172, 256, 148, 64, T["da"], None, "alt")
    d.add(f'<path class="ia dg-div" style="--i:{d.tick(.3)}" d="M20 344 H320"/>')
    phase(d, 20, 2, T["ph2"], T["ph2_s"], 358)
    box(d, 20, 474, 300, 50, T["wsx"], None, "n")
    for x in (20, 125, 230):
        arrow(d, f"M170 524 C170 540 {x+45} 536 {x+45} 554", (x + 45, 556), Dn, k=.4)
    for x, t in zip((20, 125, 230), (T["rolesx"], T["ds"], T["ux"])):
        box(d, x, 558, 90, 60, t, None, "n")
    arrow(d, "M170 618 V640", (170, 642), Dn, k=.5)
    for k, t in enumerate((T["g1"], T["g2"], T["g3"], T["g4"])):
        box(d, 20 + (k % 2) * 152, 646 + (k // 2) * 62, 148, 54, t, None, "n")
    d.add(f'<path class="ia dg-div" style="--i:{d.tick(.3)}" d="M20 784 H320"/>')
    phase(d, 20, 3, T["ph3"], T["ph3_s"], 798)
    box(d, 20, 884, 148, 66, T["brand"], None, "end")
    box(d, 172, 884, 148, 66, T["concept"], None, "end")
    for x, t, h in ((20, T["rev"], 76), (122, T["test"], 76), (224, T["camp"], 76)):
        box(d, x, 966, 96, h, t, None, "n")
    box(d, 20, 1056, 148, 48, T["camp_ops"], None, "alt")
    box(d, 172, 1056, 148, 48, T["soc_ops"], None, "alt")
    return d.svg()

def breno_jira(T, mobile):
    """Předání týmu: stavy úkolu v Jiře od backlogu po hotovo, kdo za co odpovídá a smyčky zpět."""
    cols = T["jira"]
    if not mobile:
        d = D(960, 470, "dg-d dg-jira", T["j_aria"], step=.2)
        W, G, X0, Y0, H = 118, 18.5, 14, 70, 262
        xs = [X0 + k * (W + G) for k in range(7)]
        for k, (name, desc, roles) in enumerate(cols):
            i = d.tick(.8)
            end = k == 6
            g = f'<g class="ia" style="--i:{i}"><path d="{rr(xs[k], Y0, W, H, 20)}" class="{"dg-end" if end else "dg-n"}"/>'
            g += f'<text x="{xs[k]+W/2:.1f}" y="{Y0+34}" text-anchor="middle" class="dg-name{" dg-on" if end else ""}">{esc(name)}</text>'
            g += texts(f"{xs[k]+W/2:.1f}", Y0 + 66, desc, "dg-sub" + (" dg-on" if end else ""))
            for r, (rt, hot) in enumerate(roles):
                ry = Y0 + H - 38 - (len(roles) - 1 - r) * 40
                g += f'<path d="{rr(xs[k]+10, ry, W-20, 30, 15)}" class="{"dg-end" if hot else "cdg-chip"}"/>'
                g += f'<text x="{xs[k]+W/2:.1f}" y="{ry+20}" text-anchor="middle" class="dg-s cdg-ink">{esc(rt)}</text>'
            d.add(g + "</g>")
            if k < 6:
                arrow(d, f"M{xs[k]+W+1:.1f} 200 H{xs[k]+W+G-6:.1f}", (xs[k] + W + G - 4, 200), R, k=.4)
        cx = [x + W / 2 for x in xs]
        yb = Y0 + H
        # Review -> Ready for dev, když není potřeba grooming
        arrow(d, f"M{cx[3]:.1f} {Y0} V42 H{cx[5]:.1f} V{Y0-3}", (cx[5], Y0 - 2), Dn, "soft", k=.6)
        d.add(f'<text class="ia dg-s dg-halo" style="--i:{d.tick(.3)}" x="{(cx[3]+cx[5])/2:.1f}" y="46" text-anchor="middle">{esc(T["l_skip"])}</text>')
        loops = [(3, 2, 352, T["l_iter"], 0, 8), (4, 2, 380, T["l_design"], -6, -8), (4, 1, 408, T["l_spec"], 10, 0), (4, 0, 436, T["l_rev"], 26, 0)]
        for src, dst, y, label, so, do in loops:
            xa, xb = cx[src] + so, cx[dst] + do
            arrow(d, f"M{xa:.1f} {yb} V{y} H{xb:.1f} V{yb+3}", (xb, yb + 2), U, "soft", k=.6)
            d.add(f'<text class="ia dg-s dg-halo" style="--i:{d.tick(.3)}" x="{(xa+xb)/2:.1f}" y="{y+4}" text-anchor="middle">{esc(label)}</text>')
        return d.svg()
    d = D(340, 1090, "dg-m dg-jira", T["j_aria"], step=.2)
    y = 16
    for k, (name, desc, roles) in enumerate(cols):
        end = k == 6
        import textwrap
        dl = textwrap.wrap(" ".join(desc), 40)
        rl = " · ".join(r for r, _ in roles)
        h = 40 + 17 * len(dl) + (4 if len(dl) > 1 else 0) + (22 if rl else 0)
        i = d.tick(.8)
        g = f'<g class="ia" style="--i:{i}"><path d="{rr(20, y, 300, h, 16)}" class="{"dg-end" if end else "dg-n"}"/>'
        g += f'<text x="36" y="{y+26}" class="dg-name{" dg-on" if end else ""}">{esc(name)}</text>'
        g += texts(36, y + 46, dl, "dg-sub" + (" dg-on" if end else ""), "start")
        if rl:
            g += f'<text x="36" y="{y+46+17*len(dl)+8}" class="dg-s cdg-ink">{esc(rl)}</text>'
        d.add(g + "</g>")
        if k < 6:
            arrow(d, f"M170 {y+h} V{y+h+14}", (170, y + h + 16), Dn, k=.4)
        y += h + 18
    y += 6
    band(d, 20, y + 10, T["j_loops"])
    y += 22
    for t in (T["l_iter"], T["l_design"], T["l_spec"], T["l_rev"], T["l_skip"]):
        lines = [t] if len(t) < 36 else [t[: t.rfind(" ", 0, 36)], t[t.rfind(" ", 0, 36) + 1:]]
        i = d.tick(.4)
        h = 20 + 17 * len(lines)
        d.add(f'<g class="ia" style="--i:{i}"><path d="{rr(20, y, 300, h, 12)}" class="cdg-alt"/>' + texts(36, y + 25, lines, "dg-s", "start") + "</g>")
        y += h + 10
    d.h = y + 6
    return d.svg()

CASES = {
 "heirloom": (heirloom, {
  "cs": dict(aria="Diagram: pivot z B2C na B2B. Místo čekání na obrazovky ve Figmě rozsah s vedením, AI prototyp z existujícího kódu a čtyři iterace s komentáři v prototypu. Výsledek: nový směr, rozsah a zadání.",
     start="Pivot z B2C na B2B", start_s="rozsah a zadání?", alt_band="Co se čekalo", alt="Obrazovky ve Figmě", alt_s=["čekání, spory až ve vývoji"],
     alt_m="Figma", alt_m_s="čekání", s1="Rozsah s vedením", s1_m="Rozsah s vedením", s1_s="facilitované otázky", s2="AI prototyp z kódu", s2_s="repozitář a design systém",
     ring=["4 iterace", "s komentáři"], end="Nový směr", end_s=["rozsah a zadání", "bez sporů ve vývoji"],
     p_title="Pipeline pro definici produktu",
     p_aria="Diagram pipeline pro definici produktu: facilitace rozsahu s vedením, AI prototyp z repozitáře a design systému, hosting na Vercelu napojený na repozitář a komentáře přímo v prototypu. Zpětná vazba se vrací do další verze. Výsledek: rychlejší iterace a spolupráce bez schůzek.",
     p1="Facilitace", p1_s="rozsah s vedením", p_in=["repozitář", "design systém"], p2="AI prototyp", p2_s="postavený z kódu",
     p3="Hosting na Vercelu", p3_s="napojený repozitář", p4="Komentáře", p4_s="přímo v prototypu",
     p_loop=["zpětná vazba → další iterace"], p_end=["Rychlejší", "iterace"], p_end_s=["asynchronní", "spolupráce"]),
  "en": dict(aria="Diagram: a pivot from B2C to B2B. Instead of waiting for Figma screens: scope with leadership, an AI prototype from the existing code, and 4 iterations with comments in the prototype. Result: a new direction, scope and spec.",
     start="B2C to B2B pivot", start_s="scope and spec?", alt_band="What was expected", alt="Screens in Figma", alt_s=["waiting, conflicts in dev"],
     alt_m="Figma", alt_m_s="waiting", s1="Scope with leaders", s1_m="Scope with leaders", s1_s="facilitated questions", s2="AI prototype", s2_s="from the codebase",
     ring=["4 iterations", "with comments"], end="New direction", end_s=["scope and spec", "no conflicts in dev"],
     p_title="Product definition pipeline",
     p_aria="Diagram of the product definition pipeline: facilitating the scope with leadership, an AI prototype built from the repository and design system, hosting on Vercel connected to the repository, and comments right in the prototype. Feedback goes into the next version. Result: faster iterations and async collaboration.",
     p1="Facilitation", p1_s="scope with leaders", p_in=["repository", "design system"], p2="AI prototype", p2_s="built from code",
     p3="Hosted on Vercel", p3_s="connected repository", p4="Comments", p4_s="right in the prototype",
     p_loop=["feedback → next iteration"], p_end=["Faster", "iterations"], p_end_s=["async", "collaboration"]),
 }),
 "coinmate": (coinmate, {
  "cs": dict(aria="Diagram: bez design systému. Nejdřív design systém ze stávajícího stylu, na něm iOS a Android, analýza burz a bank a nejsložitější obrazovky. Rebrand: víc konceptů za dny místo týdnů. Výsledek: nová identita na stejném systému.",
     start="Bez design systému", start_s="ani designového týmu", first=["nejdřív", "systém"], first_m=["nejdřív systém, pak vše na něm"],
     ds="DESIGN SYSTÉM", ds_s="ze stávajícího stylu · tokeny · komponenty · iOS, Android i web",
     s1="iOS i Android", s1_s="jedna značka všude", s2="Burzy a banky", s2_s="analýza trhu", s3="Složité obrazovky", s3_s="mobil i desktop",
     rb_band="Rebrand", rb=["koncepty za dny,", "ne za týdny"], end="Nová identita", end_s=["logo a barvy,", "stejný systém"]),
  "en": dict(aria="Diagram: no design system. First a design system built on the existing style, then iOS and Android on it, an analysis of exchanges and banks, and the most complex screens. Rebrand: several concepts in days instead of weeks. Result: a new brand on the same system.",
     start="No design system", start_s="and no design team", first=["system", "first"], first_m=["system first, the rest on it"],
     ds="DESIGN SYSTEM", ds_s="from the existing style · tokens · components · iOS, Android and web",
     s1="iOS and Android", s1_s="one system, one brand", s2="Exchanges, banks", s2_s="market analysis", s3="Complex screens", s3_s="mobile and desktop",
     rb_band="Rebrand", rb=["concepts in days,", "not weeks"], end="New brand", end_s=["logo and colors,", "same system"]),
 }),
 "leeaf": (leeaf, {
  "cs": dict(aria="Diagram: plán byl kopie aplikace pro každou kliniku, každá jako nový návrh. Místo toho jeden systém pro web, portál a aplikaci, tokeny pro barvy, písma a logo a nová klinika jako konfigurace v administraci. Výsledek: další kliniky běžely beze mě.",
     plan="Plán: kopie pro každou kliniku", app="Aplikace", copies=["Kopie pro A", "Kopie pro B", "Kopie pro C"], copies_m=["A", "B", "C"], copy_s="nový návrh",
     plan_n=["každá klinika", "= nový projekt"], built="Jeden systém",
     s1="Jeden systém", s1_s=["web · portál pro lékaře", "· aplikace"], s2="Tokeny", s2_s="barvy · písma · logo", s3="Konfigurace", s3_s=["nová klinika", "v administraci"],
     clinic="Klinika", clinic_m="Kl.", admin=["App Store a Google Play"], end="Další kliniky", end_s=["beze mě"]),
  "en": dict(aria="Diagram: the plan was a copy of the app for every clinic, each one a new design. Instead: one system for the website, portal and app, tokens for colors, fonts and logo, and a new clinic as a configuration in the admin. Result: more clinics launched without me.",
     plan="Plan: a copy for every clinic", app="App", copies=["Copy for A", "Copy for B", "Copy for C"], copies_m=["A", "B", "C"], copy_s="a new design",
     plan_n=["every clinic", "= a new project"], built="One system",
     s1="One system", s1_s=["website · doctors' portal", "· app"], s2="Tokens", s2_s="colors · fonts · logo", s3="Configuration", s3_s=["a new clinic", "in the admin"],
     clinic="Clinic", clinic_m="Cl.", admin=["App Store and Google Play"], end="More clinics", end_s=["without me"]),
 }),
 "breno": (breno, {
  "cs": dict(aria="Diagram: dlouhý backlog, kde má všechno vysokou prioritu. Dvoudenní workshop: první den co firma opravdu potřebuje, druhý den role a pořadí. Výsledek: pořadí s argumenty, na kterém se shodli vedení, vývoj i marketing, a jak pracovat dál.",
     b_band="Backlog", cards=["Nový e-shop", "Věrnostní body", "Platby", "Doprava", "Katalog", "Aplikace"],
     b_note=["všechno má vysokou prioritu"], b_note_m=["všechno má vysokou prioritu"], roles=["vedení · vývoj · marketing"],
     ws="Workshop, 2 dny", d1="Co firma potřebuje", d1_s="den 1 · potřeby byznysu", d2="Role a pořadí", d2_s="den 2 · shoda na pořadí",
     order_band="Pořadí", order_n=["s argumenty u každé položky"], end="Shoda", end_s=["vedení,", "vývoj,", "marketing"],
     next="Jak pracovat dál", next_s="backlog · roadmapa · nové funkce",
     x1="Před workshopem: analýza", x2="Během workshopu", x3="Po workshopu: předání týmu",
     photo1_alt="Stěna plná lepítek s otázkami a potřebami, seskupenými do kruhu", photo2_alt="Stůl s lepítky: úkoly s odhady a barevnými tečkami",
     photos_cap="Lepítka z workshopu: otázky a potřeby na stěně, úkoly s odhady na stole.",
     pl_aria="Diagram: plán spolupráce ve třech fázích. Setup: nízký konverzní poměr e-shopu, UX audit, další audity a D&A výzkum. UX základy: UX workshop, role a procesy, design system a UX návrhy, na nich grafika online kampaní, redesign e-shopu, e-mailing a grafika pro sociální sítě. Aplikace a rozvoj: brand strategie, kreativní komunikační koncept, revize UX, UX testování a kreativní řešení kampaní.",
     ph1="Setup", ph1_s=["Analýza problémů","a potřeb, UX audit"], ph2="UX základy", ph2_s=["Role, procesy a priority (workshop),","design system a styleguide"], ph3="Aplikace a rozvoj", ph3_s=["Další rozšíření"],
     start=["Nízký konverzní","poměr e-shopu"], start_m="Nízký konverzní poměr e-shopu", audit="UX audit", audits=["Další audity"], audits_s=["SEO, copy,","analytika"], da=["D&A","výzkum"], wsx="UX workshop",
     rolesx=["Role a","procesy"], ds=["Design","system"], ux=["UX","návrhy"],
     g1=["Grafika online","kampaní"], g2=["Redesign","e-shopu"], g3="E-mailing", g4=["Grafika pro","sociální sítě"], camp_ops=["Správa online","kampaní"], soc_ops=["Správa","social"],
     brand=["Brand","strategie"], concept=["Kreativní","komunikační","koncept"], rev=["Revize UX a","definice","priorit"], test=["UX","testování","a návrhy"], camp=["Kreativní","řešení","kampaní"],
     j_aria="Diagram: proces úkolu v Jiře od backlogu po hotovo. Backlog, Specification, Design, Review, Grooming, Ready for dev a Done, u každého stavu je napsáno, kdo za něj odpovídá. Zpět se vrací iterace z Review do Designu a úpravy designu a specifikace podle zpětné vazby tech leada. Když není potřeba grooming, jde Review rovnou do Ready for dev.",
     jira=[("Backlog", ["Nejasná zadání,","nápady, věci","na později"], []),
           ("Specification", ["Úkoly, které se","musí","specifikovat","pro designery"], [("Design lead", True)]),
           ("Design", ["Jasné zadání","se všemi","podklady,","iterace"], [("Designer", True)]),
           ("Review", ["Koncepty","designerů,","revidované","Design Leadem"], [("Design lead", True)]),
           ("Grooming", ["Hotové designy","ke konzultaci","s tech leadem"], [("Product manager", False), ("Design lead", True)]),
           ("Ready for dev", ["Hotové designy","pro scrum","mastera, který","je převede","do technické","Jiry"], [("Scrum master", True), ("Product manager", False)]),
           ("Done", ["Když je","vyvinuto"], [])],
     l_iter="Iterace", l_design="Úprava designu podle tech leada", l_spec="Úprava specifikace podle tech leada", l_rev="Když je design zcela revoluční a mimo architekturu", l_skip="Když není potřeba grooming", j_loops="Zpětné vazby"),
  "en": dict(aria="Diagram: a long backlog where everything is high priority. A 2-day workshop: day 1 what the business really needs, day 2 roles and order. Result: an order with the reasoning, agreed by leadership, engineering and marketing, and how to keep working.",
     b_band="Backlog", cards=["New e-shop", "Loyalty points", "Payments", "Delivery", "Catalog", "Mobile app"],
     b_note=["everything is high priority"], b_note_m=["everything is high priority"], roles=["leadership · engineering · marketing"],
     ws="Workshop, 2 days", d1="What the business needs", d1_s="day 1 · core needs", d2="Roles and order", d2_s="day 2 · agree on the order",
     order_band="Order", order_n=["with the reasoning for each item"], end="Agreement", end_s=["leadership,", "engineering,", "marketing"],
     next="How to keep working", next_s="backlog · roadmap · new features",
     x1="Before the workshop: analysis", x2="During the workshop", x3="After the workshop: handover to the team",
     photo1_alt="A wall full of sticky notes with questions and needs, grouped in a circle", photo2_alt="A table with sticky notes: tasks with estimates and colored dots",
     photos_cap="Workshop sticky notes: questions and needs on the wall, tasks with estimates on the table.",
     pl_aria="Diagram: a plan in three phases. Setup: low e-shop conversion rate, UX audit, other audits and D&A research. UX foundations: UX workshop, roles and processes, design system and UX designs, and on them online campaign graphics, an e-shop redesign, e-mailing and social media graphics. Application and development: brand strategy, a creative communication concept, UX review, UX testing and creative campaign solutions.",
     ph1="Setup", ph1_s=["Analysis of problems","and needs, UX audit"], ph2="UX foundations", ph2_s=["Roles, processes, priorities (workshop),","design system and style guide"], ph3="Application and growth", ph3_s=["Further expansion"],
     start=["Low conversion","rate of the e-shop"], start_m="Low conversion rate of the e-shop", audit="UX audit", audits=["Other audits"], audits_s=["SEO, copy,","analytics"], da=["D&A","research"], wsx="UX workshop",
     rolesx=["Roles and","processes"], ds=["Design","system"], ux=["UX","designs"],
     g1=["Online campaign","graphics"], g2=["E-shop","redesign"], g3="E-mailing", g4=["Social media","graphics"], camp_ops=["Online campaign","management"], soc_ops=["Social media","management"],
     brand=["Brand","strategy"], concept=["Creative","communication","concept"], rev=["UX review","and current","priorities"], test=["UX testing","and","designs"], camp=["Creative","campaign","solutions"],
     j_aria="Diagram: the task process in Jira from backlog to done. Backlog, Specification, Design, Review, Grooming, Ready for dev and Done, with the owner written under each status. Iterations go back from Review to Design, and design and spec changes go back based on tech lead feedback. When grooming isn't needed, Review goes straight to Ready for dev.",
     jira=[("Backlog", ["Vague tasks,","ideas, things","for later"], []),
           ("Specification", ["Tasks that need","specifying","for designers"], [("Design lead", True)]),
           ("Design", ["Clear brief,","all inputs,","iterations"], [("Designer", True)]),
           ("Review", ["Concepts from","designers,","reviewed by","the Design Lead"], [("Design lead", True)]),
           ("Grooming", ["Finished","designs for a","consult with","the tech lead"], [("Product manager", False), ("Design lead", True)]),
           ("Ready for dev", ["Finished","designs for the","scrum master,","who turns them","into technical","Jira tasks"], [("Scrum master", True), ("Product manager", False)]),
           ("Done", ["When it's built"], [])],
     l_iter="Iteration", l_design="Design changes per tech lead", l_spec="Spec changes per tech lead feedback", l_rev="When the design is radically outside the architecture", l_skip="When grooming isn't needed", j_loops="Feedback loops")
 }),
}

SEC = {"cs": "Jak to proběhlo", "en": "How it happened"}
WAIT = {"cs": "Spustí se po dokončení diagramu výše.", "en": "Starts when the diagram above finishes."}
PHOTOS = {"breno": (("breno-workshop-lepitka-na-stene-f0865732.webp", 1200, 922, "photo1_alt"),
                    ("breno-workshop-lepitka-na-stole-28e586b0.webp", 688, 876, "photo2_alt"))}

def wait(lang):
    return f'        <p class="dg-wait" aria-hidden="true"><span class="dg-wait-d"><i></i><i></i><i></i></span>{WAIT[lang]}</p>\n'

def fig(a, b, lang, waits):
    return f'      <figure class="lf-fig case-fig">\n        {a}\n        {b}\n' + (wait(lang) if waits else "") + '      </figure>\n'

def figure(case, lang):
    fn, T = CASES[case]
    t = T[lang]
    out = (f'  <section class="case-dg">\n    <div class="wrap">\n      <p class="eyebrow tl-h">{SEC[lang]}</p>\n' + fig(fn(t, False), fn(t, True), lang, False))
    if "p_title" in t:
        out += f'      <p class="eyebrow tl-h case-dg-h2">{t["p_title"]}</p>\n' + fig(heirloom_pipe(t, False), heirloom_pipe(t, True), lang, True)
    if case == "breno":
        out += f'      <p class="eyebrow tl-h case-dg-h2">{t["x1"]}</p>\n' + fig(breno_plan(t, False), breno_plan(t, True), lang, True)
        ph = "".join(f'<img src="/assets/img/{n}" width="{w}" height="{h}" alt="{esc(t[k])}" loading="lazy">' for n, w, h, k in PHOTOS[case])
        out += (f'      <p class="eyebrow tl-h case-dg-h2">{t["x2"]}</p>\n      <figure class="lf-fig case-photos">\n        {ph}\n'
                f'        <figcaption>{esc(t["photos_cap"])}</figcaption>\n      </figure>\n')
        out += f'      <p class="eyebrow tl-h case-dg-h2">{t["x3"]}</p>\n' + fig(breno_jira(t, False), breno_jira(t, True), lang, True)
    return out + '    </div>\n  </section>\n'

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    for case in CASES:
        for lang, pre in (("cs", ""), ("en", "en/")):
            f = f"{root}/{pre}portfolio/{case}/index.html"
            s = open(f).read()
            s = re.sub(r' *<section class="case-dg">.*?</section>\n', "", s, flags=re.S)
            anchor = '  <section class="case-mid case-tl">'
            assert anchor in s, f
            s = s.replace(anchor, figure(case, lang) + anchor, 1)
            open(f, "w").write(s)
            print(f, file=sys.stderr)
