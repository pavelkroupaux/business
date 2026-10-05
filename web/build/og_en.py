#!/usr/bin/env python3
"""Obrázky pro sdílení (1200 × 630) pro anglickou verzi, stejně jako og.py pro českou.

Kresby (úvodní linka, ilustrace služeb, loga případů) bere z vyrobených stránek v kořeni repozitáře,
takže popisky v nich jsou už přeložené. Proto se spouští až po pages.py:

    python3 web/build/pages.py
    python3 web/build/og_en.py              # -> og/en/
    python3 web/build/og_en.py --lang cs --out /tmp/og-kontrola   # česká kontrola proti og.py

Potřebuje cairosvg, Pillow a fontTools (requirements.txt) a písma z build/fonts nainstalovaná
v systému (Inter 500/600/700, Shantell Sans), stejně jako og.py.
"""
import argparse
import base64
import html
import io
import os
import re
import sys

import cairosvg
from PIL import Image, ImageFont

BUILD = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, BUILD)
from lockup import mark as _pk_mark  # noqa: E402

PUBLIC = os.path.abspath(BUILD + "../..") + "/"   # kořen repozitáře, ten publikuje GitHub Pages
FONTDIR = BUILD + "fonts/"
F700 = FONTDIR + "Inter-700-full.ttf"
F500 = FONTDIR + "Inter-500-full.ttf"
INK, MUTED, FAINT, YEL = "#111111", "#5B5B55", "#8E8E93", "#FFCE1B"
W, H = 1200, 630

TEXTS = {
    "en": dict(
        pages="en/",
        home=("I help teams decide\nwhat to build.", "decide",
              "A working prototype and a finished spec. With AI, in days, not weeks."),
        services=[("og-decision-prototype", "dp", "services/decision-prototype/index.html", "Decision Prototype",
                   "A working prototype\nin a few days.", "working prototype", "1 day, 2 days, or a week.\nFrom CZK 49,000."),
                  ("og-audit", "au", "services/audit/index.html", "Decision Audit",
                   "Find out what's\nholding back your\nproduct. In 5 days.", "holding back",
                   "A narrated screen recording and a\nprioritized list. From CZK 29,000."),
                  ("og-fractional", "fr", "services/fractional/index.html", "Fractional product and design leadership",
                   "A product lead\nuntil you hire one.", "product lead",
                   "2 days a week on your team.\nFrom CZK 120,000 per month.")],
        portfolio=("Portfolio", "4 companies.\n4 stuck products.", "stuck",
                   "Case studies from regulated crypto, healthcare, and e-commerce."),
        names={"home": "og-home", "portfolio": "og-portfolio"},
    ),
    # jen pro kontrolu, že výstup odpovídá og.py
    "cs": dict(
        pages="",
        home=("Pomáhám týmům rozhodnout, co postavit.", "rozhodnout",
              "Funkční prototyp a hotové zadání. S AI za dny, ne týdny."),
        services=[("og-decision-prototype", "dp", "services/decision-prototype/index.html", "Decision Prototype",
                   "Funkční prototyp\nza pár dní.", "Funkční prototyp", "Jeden den, dva, nebo týden.\nOd 49 000 Kč."),
                  ("og-audit", "au", "services/audit/index.html", "Audit rozhodnutí",
                   "Zjistěte, co váš produkt brzdí.\nZa pět dní.", "brzdí",
                   "Nahrávka obrazovky a seznam podle priority.\nOd 29 000 Kč."),
                  ("og-vedeni-produktu", "fr", "services/fractional/index.html", "Vedení produktu a designu na část úvazku",
                   "Vedení produktu, dokud nenajdete stálého člověka.", "Vedení produktu",
                   "Dva dny v týdnu ve vašem týmu.\nOd 120 000 Kč měsíčně.")],
        portfolio=("Portfolio", "Čtyři firmy. Čtyři zaseknuté produkty.", "zaseknuté",
                   "Případy z regulovaného krypta, zdravotnictví a e-commerce."),
        names={"home": "og-uvod", "portfolio": "og-portfolio"},
    ),
}

VARS = {"var(--ink)": INK, "var(--muted)": "#6e6e73", "var(--faint)": FAINT, "var(--fix)": YEL, "var(--ground)": "#ffffff",
        "var(--raise)": "#ffffff", "var(--surface)": "#F2F2F0", "var(--line)": "#E2E2DC", "var(--lap-frame)": "#2c2c2e",
        "var(--lap-base)": "#d4d4d9", "var(--lap-notch)": "#b4b4ba", "var(--lap-scr)": "#ffffff", "var(--display)": "Inter",
        "var(--hand)": "Shantell Sans Light"}
ILL_CSS = """.ill-t{font-family:Shantell Sans Light;font-size:14px;fill:#6e6e73}.ill-d{font-family:Inter;font-size:13px;font-weight:700;fill:#6e6e73}
.don{fill:#111111}.ill-off{fill:#F2F2F0;stroke:#E2E2DC;stroke-width:1.5}.ill-soft{opacity:.35}.ill-node,.ill-scr{fill:#ffffff}
.lap-frame{fill:#2c2c2e}.lap-base{fill:#d4d4d9}.lap-scr{fill:#ffffff}.ill-q{font-family:Inter;font-size:18px;font-weight:700;fill:#111111}
.num{fill:#FFCE1B;stroke:#FFCE1B}.numt{fill:#111111}.wk{display:none}"""


def devar(s):
    s = re.sub(r'style=([^"\s>]+)', r'style="\1"', s)
    s = s.replace("&nbsp;", "&#160;").replace("&middot;", "&#183;").replace("&ndash;", "&#8211;")
    for k, v in VARS.items():
        s = s.replace(k, v)
    s = s.replace("Shantell Sans, ", "Shantell Sans Light, ")
    return s.replace("currentColor", INK)


def inline_images(svg):
    """Obrázky ve vyrobených stránkách jsou soubory, cairosvg potřebuje data: URI."""
    def one(m):
        path = PUBLIC + m.group(2).lstrip("/")
        ext = path.rsplit(".", 1)[1]
        data = open(path, "rb").read()
        if ext == "webp":   # cairosvg WebP neumí, převést na PNG
            b = io.BytesIO()
            Image.open(io.BytesIO(data)).save(b, "PNG")
            data, ext = b.getvalue(), "png"
        mime = {"svg": "image/svg+xml", "jpg": "image/jpeg", "png": "image/png"}[ext]
        return f'{m.group(1)}="data:{mime};base64,{base64.b64encode(data).decode()}"'
    return re.sub(r'\b(href|xlink:href|src)="(/assets/img/[^"]+)"', one, svg)


def wrap_lines(text, font, size, maxw, ls=0.0):
    f = ImageFont.truetype(font, size)
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w_ in para.split(" "):
            t = (cur + " " + w_).strip()
            if f.getlength(t) + ls * len(t) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w_
        lines.append(cur)
    return lines, f


def headline(text, mark, x, y, size, maxw):
    """SVG s nadpisem; slovo nebo fráze `mark` dostane žlutý podklad jako na webu."""
    ls = -size * 0.035
    lines, f = wrap_lines(text, F700, size, maxw, ls)
    out = []
    lh = size * 1.08
    L = lambda t: f.getlength(t) + ls * len(t)
    for i, ln in enumerate(lines):
        by = y + i * lh
        if mark and mark in ln:
            pre = ln[:ln.index(mark)]
            x0 = x + L(pre)
            wd = L(mark)
            out.append(f'<rect x="{x0-6:.1f}" y="{by-size*0.52:.1f}" width="{wd+12:.1f}" height="{size*0.46:.1f}" fill="{YEL}"/>')
        out.append(f'<text x="{x}" y="{by:.1f}" font-family="Inter" font-weight="700" font-size="{size}" '
                   f'letter-spacing="{-size*0.035:.2f}" fill="{INK}">{html.escape(ln)}</text>')
    return "".join(out), y + (len(lines) - 1) * lh


def sub(text, x, y, size=27, maxw=600, col=MUTED):
    lines, f = wrap_lines(text, F500, size, maxw)
    return "".join(f'<text x="{x}" y="{y + i*size*1.35:.1f}" font-family="Inter" font-weight="500" font-size="{size}" '
                   f'fill="{col}">{html.escape(l)}</text>' for i, l in enumerate(lines))


PK_VB = tuple(float(v) for v in re.search(r'viewBox="([^"]+)"', open(PUBLIC + "logo/pk/pk-svetle.svg").read()).group(1).split())
PK_BODY = _pk_mark(INK, INK)
PK_H = 66


def frame(inner, extra_css=""):
    dots = "".join(f'<circle cx="{cx}" cy="{cy}" r="1.3" fill="#E6E6E0"/>' for cx in range(14, W, 26) for cy in range(14, H, 26))
    bw = PK_H * PK_VB[2] / PK_VB[3]
    brand = (f'<svg x="58" y="40" width="{bw:.1f}" height="{PK_H}" viewBox="{" ".join(map(str, PK_VB))}">{PK_BODY}</svg>'
             f'<text x="{58 + bw + 14:.1f}" y="79" font-family="Inter" font-weight="700" font-size="24" letter-spacing="-0.5" fill="{INK}">Pavel Kroupa</text>'
             f'<text x="{W-64}" y="79" text-anchor="end" font-family="Inter" font-weight="500" font-size="20" fill="{FAINT}">pavelkroupa.com</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<style>{ILL_CSS}{extra_css}</style><rect width="{W}" height="{H}" fill="#ffffff"/>{dots}{brand}{inner}</svg>')


def render(name, svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    png2 = cairosvg.svg2png(bytestring=svg.encode(), output_width=W * 2, output_height=H * 2)
    # vykreslit ve 2× a zmenšit, ať jsou hrany čisté; web odkazuje jen na 1200 × 630
    im = Image.open(io.BytesIO(png2)).convert("RGB").resize((W, H), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "PNG", optimize=True)
    open(f"{out_dir}{name}.png", "wb").write(b.getvalue())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en", choices=sorted(TEXTS))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    T = TEXTS[a.lang]
    out_dir = (a.out.rstrip("/") + "/") if a.out else PUBLIC + "og/" + ("en/" if a.lang == "en" else "")
    page = lambda p: open(PUBLIC + T["pages"] + p, encoding="utf-8").read()

    # 1) úvod: nadpis, podnadpis a úvodní kresba z úvodní stránky
    home = page("index.html")
    hero = re.search(r'<svg class="hx".*?</svg>', home, re.S).group(0)
    hero = re.sub(r"stroke-dashoffset:[^;\"]+;?", "", hero)                      # konečný stav animace
    hero = re.sub(r'<text[^>]*class="hx-cs"[^>]*>.*?</text>', "", hero)           # druhá jazyková varianta pryč
    hero = inline_images(devar(re.sub(r'^<svg class="hx"', "<svg", hero)))
    title, mark, lede = T["home"]
    h, yb = headline(title, mark, 64, 205, 74, 1060)
    s = sub(lede, 64, yb + 62, 28, 1000)
    hero = hero.replace("<svg ", '<svg x="40" y="360" width="1120" height="246" preserveAspectRatio="xMidYMid meet" ', 1)
    render(T["names"]["home"], frame(h + s + hero), out_dir)

    # 2–4) služby: text vlevo, ilustrace z hlavičky stránky služby vpravo
    for name, kind, src, eyebrow, title, mark, lede in T["services"]:
        m = re.search(r'<div class="svc-hero-ill"><svg class="ill ill-' + kind + r'".*?</svg></div>', page(src), re.S)
        ill = devar(re.sub(r'^<svg class="[^"]*"', "<svg", m.group(0)[len('<div class="svc-hero-ill">'):-len("</div>")]))
        eb = f'<text x="64" y="186" font-family="Inter" font-weight="600" font-size="24" fill="{FAINT}">{html.escape(eyebrow)}</text>'
        h, yb = headline(title, mark, 64, 268, 66, 640)
        s = sub(lede, 64, yb + 64, 26, 600)
        ill = ill.replace("<svg ", '<svg x="720" y="150" width="440" height="380" preserveAspectRatio="xMidYMid meet" ', 1)
        render(name, frame(eb + h + s + inline_images(ill)), out_dir)

    # 5) portfolio: loga případů z karet na úvodní stránce
    eyebrow, title, mark, lede = T["portfolio"]
    eb = f'<text x="64" y="186" font-family="Inter" font-weight="600" font-size="24" fill="{FAINT}">{eyebrow}</text>'
    h, yb = headline(title, mark, 64, 268, 70, 1000)
    s = sub(lede, 64, yb + 62, 27, 1000)
    logos, x = "", 64
    for alt, hgt, wd in (("Coinmate", 64, 112), ("Leeaf", 36, 86), ("Heirloom", 30, 168)):
        m = re.search(r'<img class="card-logo" src="([^"]+)" alt="' + alt + '">', home)
        if m:
            logos += (f'<image x="{x}" y="{520 - hgt/2:.0f}" width="{wd}" height="{hgt}" preserveAspectRatio="xMinYMid meet" '
                      f'xlink:href="{m.group(1)}"/>')
            x += wd + 70
    logos += f'<text x="{x}" y="531" font-family="Inter" font-weight="700" font-size="30" letter-spacing="1" fill="#8e8e93">BRENO</text>'
    render(T["names"]["portfolio"], frame(eb + h + s + inline_images(logos)), out_dir)
    print(sorted(f for f in os.listdir(out_dir) if f.endswith(".png")))


if __name__ == "__main__":
    main()
