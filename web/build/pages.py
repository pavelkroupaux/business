#!/usr/bin/env python3
"""Rozdělí web z jednoho souboru na samostatné stránky, česky i anglicky.

Zdroj:  web/src/index.html  (celý web v jednom souboru, sekce za #/, otevře se i jako náhled;
        je to index.html z buildu ve vaultu, build_v5b.py s koly až po v5_round18.py)
Výstup: web/public/…            české stránky (/, /portfolio, /services/audit …)
        web/public/en/…         anglické stránky (/en/, /en/portfolio …)
        web/public/assets/      styl, skripty a obrázky vytažené ze souboru
        web/public/sitemap.xml

Spuštění z kořene repozitáře:
    python3 web/build/pages.py

Odkud se co bere:
- české titulky, popisy, obrázky pro sdílení a klíčová slova: PAGES a KEYWORDS ve v5_round16.py,
  stejné jako ve webu v jednom souboru,
- anglické texty a metadata: en.py,
- otázky a odpovědi ve strukturovaných datech: přímo z textu stránky, takže vždy sedí.

Skript skončí chybou, když něco nesedí: chybí anglický překlad, cena ve strukturovaných datech
není vidět na stránce, stránka nemá právě jeden nadpis h1, zůstal odkaz #/ nebo zástupný text.
Ruční soubory ve web/public (robots.txt, llms.txt, 404.html, ikony, og/, logo/, _headers) nemění.
"""
import ast
import base64
import datetime
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD))
import i18n  # noqa: E402
import en as EN  # noqa: E402

WEB = BUILD.parent
SRC = WEB / "src" / "index.html"
OUT = WEB / "public"
ASSETS = OUT / "assets"
SITE = "https://www.pavelkroupa.com"
TODAY = datetime.date.today().isoformat()

# Struktura webu. route = klíč ze zdrojového #/ routeru, path = adresa české stránky
# (anglická má před ní /en). Texty jsou v kole 16 (česky) a v en.py (anglicky).
ROUTES = [
    dict(route="/", view="v-home", path="/", nav="/", kind="home", services=["dp", "audit", "fractional"]),
    dict(route="/portfolio", view="v-portfolio", path="/portfolio", nav="/portfolio", kind="collection",
         crumbs=["portfolio"]),
    dict(route="/work/heirloom", view="v-case-heirloom", path="/portfolio/heirloom", nav="/portfolio", kind="case",
         client="Heirloom", crumbs=["portfolio", "Heirloom"]),
    dict(route="/work/coinmate", view="v-case-coinmate", path="/portfolio/coinmate", nav="/portfolio", kind="case",
         client="Coinmate", crumbs=["portfolio", "Coinmate"]),
    dict(route="/work/leeaf", view="v-case-leeaf", path="/portfolio/leeaf", nav="/portfolio", kind="case",
         client="Leeaf", crumbs=["portfolio", "Leeaf"]),
    dict(route="/work/breno", view="v-case-breno", path="/portfolio/breno", nav="/portfolio", kind="case",
         client="BRENO", crumbs=["portfolio", "BRENO"]),
    dict(route="/services", view="v-services", path="/services", nav="/services", kind="collection",
         crumbs=["services"], services=["dp", "audit", "fractional"], faq=True),
    dict(route="/services/decision-prototype", view="v-svc-dp", path="/services/decision-prototype", nav="/services",
         kind="page", crumbs=["services", "svc:dp"], services=["dp"], faq=True),
    dict(route="/services/audit", view="v-svc-audit", path="/services/audit", nav="/services", kind="page",
         crumbs=["services", "svc:audit"], services=["audit"]),
    dict(route="/services/fractional", view="v-svc-fractional", path="/services/fractional", nav="/services",
         kind="page", crumbs=["services", "svc:fractional"], services=["fractional"]),
    dict(route="/about", view="v-about", path="/about", nav="/about", kind="profile", crumbs=["about"]),
    dict(route="/contact", view="v-contact", path="/contact", nav="/contact", kind="contact", crumbs=["contact"]),
]
NAV = ["/", "/portfolio", "/services", "/about", "/contact"]


def round16():
    """PAGES a KEYWORDS z kola 16 (jen hodnoty, kolo se nespouští)."""
    tree = ast.parse((BUILD / "v5_round16.py").read_text(encoding="utf-8"))
    vals = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", "") in ("PAGES", "KEYWORDS"):
            vals[n.targets[0].id] = ast.literal_eval(n.value)
    assert {"PAGES", "KEYWORDS"} <= set(vals), "v5_round16.py: chybí PAGES nebo KEYWORDS"
    return vals["PAGES"], vals["KEYWORDS"]


PAGES16, KEYWORDS16 = round16()

CS = dict(
    lang="cs", prefix="", locale="cs_CZ", keywords=KEYWORDS16,
    meta={r: dict(title=t, desc=d, og=img) for r, (t, d, img) in PAGES16.items()},
    nav={"/": "Úvod", "/portfolio": "Portfolio", "/services": "Služby", "/about": "O mně", "/contact": "Kontakt"},
    crumbs={"home": "Úvod", "portfolio": "Portfolio", "services": "Služby", "about": "O mně", "contact": "Kontakt"},
    og_dir="/og/",
    og_alt={"og-uvod": "Pavel Kroupa: Pomáhám týmům rozhodnout, co postavit.",
            "og-portfolio": "Portfolio: Čtyři firmy. Čtyři zaseknuté produkty.",
            "og-decision-prototype": "Decision Prototype: Funkční prototyp za pár dní.",
            "og-audit": "Audit rozhodnutí: Zjistěte, co váš produkt brzdí. Za pět dní.",
            "og-vedeni-produktu": "Vedení produktu, dokud nenajdete stálého člověka."},
    person=dict(jobTitle="Definice produktu a vedení designu",
                description="Třináct let dovádím týmy k rozhodnutí. Přicházím tam, kde se o produktu ještě nerozhodlo, "
                            "nebo kde se tým cyklí a potřebuje se pohnout dál.",
                knowsAbout=["funkční prototyp", "product discovery", "UX audit", "design systém", "vedení produktu",
                            "fintech", "zdravotnictví"],
                workLocation=["Praha", "Amsterdam"]),
    business=dict(description=None,  # = popis úvodní stránky z kola 16
                  areaServed=["Česká republika", "Nizozemsko", "online"], catalog="Služby",
                  address=dict(streetAddress="Mezno 88", postalCode="257 86", addressLocality="Mezno",
                               addressCountry="CZ")),
    services={
        "dp": dict(name="Decision Prototype",
                   desc="Rozhodnutí, na které se dá kliknout. Přinesete nerozhodnutou věc, odnesete rozhodnutí a funkční "
                        "prototyp na webu, podle kterého se dá stavět.",
                   offers=[("Jeden den", "Jeden workshop a první verze prototypu.", 49000, None),
                           ("Dva dny", "Jedna nerozhodnutá věc, dotažená do konce.", 125000, None),
                           ("Týden", "Celá oblast produktu, víc rozhovorů a workshopů.", 220000, None)]),
        "audit": dict(name="Audit rozhodnutí",
                      desc="Projdu váš produkt a na nahrávce obrazovky ukážu, co nefunguje a v jakém pořadí bych to "
                           "opravoval. Bez schůzek.",
                      offers=[(None, "Pět pracovních dní, bez schůzek.", 29000, None)]),
        "fractional": dict(name="Vedení produktu a designu na část úvazku",
                           desc="Dva dny v týdnu sedím ve vašem týmu. Rozhoduju s vámi u porad vedení i produktu a "
                                "držím směr, aby se vývoj necyklil.",
                           offers=[(None, "Dva dny v týdnu, nejméně tři měsíce.", 120000, "MON")]),
    },
    price=lambda v: f"{v:,}".replace(",", " ") + " Kč",
    price_range="od 29 000 Kč",
    unit_text="měsíčně",
    switch=dict(label="EN", hreflang="en", aria="English version"),
    notfound=dict(title="Stránka nenalezena · Pavel Kroupa", eyebrow="Chyba 404",
                  h1='Tahle stránka tu <span class="fix">není</span>.',
                  lede="Web má novou podobu a některé staré adresy zmizely. Začněte na úvodu, nebo mi rovnou napište, "
                       "kde jste se zasekli.",
                  home="Na úvod", contact="Napsat mi"),
)
EN_ = dict(
    lang="en", prefix="/en", locale="en_US", keywords=EN.KEYWORDS, meta=EN.META, nav=EN.NAV, crumbs=EN.CRUMBS,
    og_dir="/og/en/", og_alt=EN.OG_ALT, person=EN.PERSON, business=EN.BUSINESS, services=EN.SERVICES,
    price=EN.price, price_range=EN.PRICE_RANGE, unit_text="per month",
    switch=dict(label="CS", hreflang="cs", aria="Česká verze"), notfound=EN.NOTFOUND,
)
LANGS = [CS, EN_]
SERVICE_IDS = {"dp": "#decision-prototype", "audit": "#audit", "fractional": "#fractional"}
SERVICE_PATHS = {"dp": "/services/decision-prototype", "audit": "/services/audit", "fractional": "/services/fractional"}


def path_for(route, lang):
    """#/ route ze zdroje -> skutečná adresa v daném jazyce."""
    if route == "/reference":
        p = "/portfolio#refs"
    elif route.startswith("/work/"):
        p = "/portfolio/" + route[len("/work/"):]
    elif route.startswith("/contact/"):
        p = "/contact?service=" + route[len("/contact/"):]
    else:
        p = route
    if lang["prefix"]:
        p = lang["prefix"] + ("/" if p == "/" else p)
    return p


def url_for(path):
    return SITE + path


def file_for(path):
    if path.endswith("/"):
        return OUT / path.lstrip("/") / "index.html"
    return OUT / (path.lstrip("/") + ".html")


def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "img"


def fingerprint(data):
    return hashlib.sha1(data).hexdigest()[:8]


# ---------------------------------------------------------------- obrázky
EXT = {"image/svg+xml": "svg", "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif"}
images = {}      # sha1 -> /assets/img/...
by_alt = {}      # alt -> /assets/img/...


def extract_images(markup):
    """data: URI v src/href -> soubory v assets/img, stejné obrázky jen jednou."""
    def repl(m):
        tag = m.group(0)

        def one(a):
            attr, mime, b64 = a.group(1), a.group(2), a.group(3)
            data = base64.b64decode(b64)
            key = hashlib.sha1(data).hexdigest()
            if key not in images:
                alt = re.search(r'\balt="([^"]*)"', tag)
                name = slug(alt.group(1)) if alt and alt.group(1) else "img"
                fname = f"{name}-{key[:8]}.{EXT[mime]}"
                (ASSETS / "img").mkdir(parents=True, exist_ok=True)
                (ASSETS / "img" / fname).write_bytes(data)
                images[key] = "/assets/img/" + fname
            alt = re.search(r'\balt="([^"]+)"', tag)
            if alt:
                by_alt.setdefault(alt.group(1), images[key])
            return f'{attr}="{images[key]}"'
        return re.sub(r'\b(src|href)="data:([a-z]+/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)"', one, tag)
    return re.sub(r"<(?:img|image)\b[^>]*>", repl, markup)


def map_links(markup, lang):
    out = re.sub(r'href="#(/[^"]*)"', lambda m: f'href="{path_for(m.group(1), lang)}"', markup)
    assert 'href="#/' not in out
    return out


# ---------------------------------------------------------------- JSON-LD
def offer(name, desc, price, unit, lang):
    spec = {"@type": "UnitPriceSpecification" if unit else "PriceSpecification", "minPrice": price, "priceCurrency": "CZK"}
    if unit:
        spec.update(unitCode=unit, unitText=lang["unit_text"])
    o = {"@type": "Offer", "description": desc, "priceSpecification": spec}
    if name:
        o["name"] = name
    return o


def faq_from(body):
    """Otázky a odpovědi tak, jak jsou na stránce (sekce <details> bez třídy)."""
    out = []
    for q, a in re.findall(r"<details><summary><span>(.*?)</span></summary><p>(.*?)</p></details>", body, re.S):
        clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
        out.append((clean(q), clean(a)))
    return out


def jsonld(r, lang, body, portrait):
    home = SITE + path_for("/", lang)
    url = url_for(path_for(r["route"], lang))
    meta = lang["meta"][r["route"]]
    pid, bid, wid = SITE + "/#pavel", SITE + "/#sluzby", home + "#website"
    person = {"@type": "Person", "@id": pid, "name": "Pavel Kroupa", "url": home,
              "email": "mailto:info@pavelkroupa.com", "image": SITE + portrait,
              "jobTitle": lang["person"]["jobTitle"], "description": lang["person"]["description"],
              "knowsLanguage": ["cs", "en"],
              "workLocation": [{"@type": "Place", "name": n} for n in lang["person"]["workLocation"]],
              "knowsAbout": lang["person"]["knowsAbout"], "sameAs": ["https://www.linkedin.com/in/pavelkroupa/"]}
    business = {"@type": "ProfessionalService", "@id": bid, "name": "Pavel Kroupa", "url": home,
                "logo": SITE + "/logo/pk/pk-svetle-ctverec-400.png", "image": SITE + "/og/og-uvod.png",
                "description": lang["business"]["description"] or lang["meta"]["/"]["desc"],
                "founder": {"@id": pid}, "email": "info@pavelkroupa.com",
                "areaServed": lang["business"]["areaServed"],
                "identifier": {"@type": "PropertyValue", "propertyID": "IČO", "value": "87977753"},
                "priceRange": lang["price_range"], "currenciesAccepted": "CZK",
                "sameAs": ["https://www.linkedin.com/in/pavelkroupa/"],
                "hasOfferCatalog": {"@type": "OfferCatalog", "name": lang["business"]["catalog"],
                                    "itemListElement": [{"@id": SITE + "/" + SERVICE_IDS[k]} for k in SERVICE_IDS]}}
    if r["kind"] == "contact":   # sídlo je vidět jen na kontaktu
        business["address"] = {"@type": "PostalAddress", **lang["business"]["address"]}
    website = {"@type": "WebSite", "@id": wid, "url": home, "name": "Pavel Kroupa", "inLanguage": lang["lang"],
               "publisher": {"@id": pid}}
    ptype = {"home": "WebPage", "collection": "CollectionPage", "case": "WebPage", "page": "WebPage",
             "profile": "ProfilePage", "contact": "ContactPage"}[r["kind"]]
    og = SITE + lang["og_dir"] + meta["og"] + ".png"
    webpage = {"@type": ptype, "@id": url + "#webpage", "url": url, "name": meta["title"], "description": meta["desc"],
               "inLanguage": lang["lang"], "isPartOf": {"@id": wid},
               "primaryImageOfPage": {"@type": "ImageObject", "url": og, "width": 1200, "height": 630}}
    if r["kind"] == "profile":
        webpage["mainEntity"] = {"@id": pid}
    elif r["kind"] == "case":
        webpage["about"] = {"@type": "Organization", "name": r["client"]}
        webpage["author"] = {"@id": pid}
    else:
        webpage["about"] = {"@id": pid}
    graph = [website, webpage, person, business]
    if r.get("crumbs"):
        names = []
        for c in ["home"] + r["crumbs"]:
            if c.startswith("svc:"):
                names.append((lang["services"][c[4:]]["name"], SERVICE_PATHS[c[4:]]))
            elif c in lang["crumbs"]:
                names.append((lang["crumbs"][c], {"home": "/", "portfolio": "/portfolio", "services": "/services",
                                                  "about": "/about", "contact": "/contact"}[c]))
            else:
                names.append((c, r["path"]))
        bc = {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                   "item": url_for(path_for(p, lang) if p != "/" else path_for("/", lang))}
                                  for i, (n, p) in enumerate(names)]}
        webpage["breadcrumb"] = {"@id": bc["@id"]}
        graph.append(bc)
    for key in r.get("services", []):
        s = lang["services"][key]
        # jen ceny, které jsou na téhle stránce vidět (úvod ukazuje jen nejnižší)
        offers = [offer(*o, lang) for o in s["offers"] if lang["price"](o[2]) in body]
        assert offers, (lang["lang"], r["path"], key, "cena není na stránce vidět")
        graph.append({"@type": "Service", "@id": SITE + "/" + SERVICE_IDS[key], "name": s["name"],
                      "url": url_for(path_for(SERVICE_PATHS[key], lang)), "description": s["desc"],
                      "provider": {"@id": bid}, "areaServed": lang["business"]["areaServed"],
                      "offers": offers if len(offers) > 1 else offers[0]})
    if r.get("faq"):
        qa = faq_from(body)
        assert qa, (lang["lang"], r["path"], "otázky na stránce nenalezeny")
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang["lang"],
                      "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                     for q, a in qa]})
    return {"@context": "https://schema.org", "@graph": graph}


# ---------------------------------------------------------------- skript
BLOCK = "\n/*<<block>>*/\n"
SHIM = ("/* staré odkazy s #/ vedou na samostatné stránky */\n(function(){var h=location.hash;if(h.indexOf(\"#/\")!==0)return;"
        "var r=h.slice(1),p=r===\"/reference\"?\"/portfolio#refs\":r.indexOf(\"/work/\")===0?\"/portfolio/\"+r.slice(6):"
        "r.indexOf(\"/contact/\")===0?\"/contact?service=\"+r.slice(9):r;location.replace(p);})();\n")


def build_js(scripts, swaps=()):
    # Titulek podle sekce potřebuje jen web v jednom souboru, tady má titulek každá stránka.
    blocks = [s for s in scripts if "document.title" not in s]
    assert len(blocks) == len(scripts) - 1, "čekal jsem právě jeden skript s titulkem podle sekce"
    js = BLOCK.join(blocks)

    def swap(old, new):
        nonlocal js
        assert js.count(old) == 1, old
        js = js.replace(old, new)
    # Router: stránka nese svou trasu v <html data-route>, sekce se neskrývají a nescrolluje se nahoru,
    # aby fungovaly kotvy jako /portfolio#refs.
    swap('var h=(location.hash||"#/").slice(1);', 'var h=document.documentElement.getAttribute("data-route")||"/";')
    swap("window.scrollTo(0,0);", "")
    # Kontakt: služba se předvyplní z /contact?service=audit
    swap('function pick(){var m=(location.hash||"").match(/^#\\/contact\\/([a-z-]+)$/);if(m){sel.value=m[1];}}',
         'function pick(){var s=new URLSearchParams(location.search).get("service");'
         '[].some.call(sel.options,function(o){if(o.value===s){sel.value=s;return true;}});}')
    # Jazyk: přepínač je odkaz na stejnou stránku v druhém jazyce, jazyk stránky určuje <html lang>.
    swap('var lang="cs"; document.documentElement.lang="cs";', 'var lang=document.documentElement.lang||"cs";')
    swap('document.getElementById("lang").addEventListener("click",function(){\n    setLang(lang==="cs"?"en":"cs");\n  });', "")
    for old, new in swaps:
        swap(old, new)
    return SHIM + "\n".join("try{\n" + b + "\n}catch(e){console.error(e);}" for b in js.split(BLOCK))


EXTRA_CSS = """
/* ---------- samostatné stránky: přepínač jazyka je odkaz ---------- */
.ctl a.lang{font-family:var(--display);font-size:11.5px;font-weight:550;letter-spacing:.05em;
  background:transparent;color:var(--faint);border-radius:999px;text-decoration:none;
  padding:6px 11px;line-height:1.3;min-width:34px;text-align:center;box-sizing:border-box;
  transition:background .25s ease,color .25s ease}
.ctl a.lang:hover{background:var(--surface);color:var(--ink)}
@media(max-width:340px){.top #theme{display:none}}
.notfound .wrap{padding-block:120px 140px}
"""

PLACEHOLDER = re.compile(r"\[(?:[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]{3,}[^\]]*)\]")


# ---------------------------------------------------------------- stavba
def main():
    src = SRC.read_text(encoding="utf-8")

    head_src = src[:src.index("<style>")]
    fonts = [l for l in re.findall(r"<link\b[^>]*>", head_src) if "fonts.g" in l]
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    header = re.search(r'<header class="top">.*?</header>', src, re.S).group(0)
    footer = re.search(r'<footer class="foot">.*?</footer>', src, re.S).group(0)
    main_html = src[src.index("<main>\n") + len("<main>\n"):src.index("</main>")]
    views = dict(re.findall(r'(?ms)^<div id="(v-[a-z-]+)"(?: hidden)?>\n(.*?)\n^</div>\s*(?=^<div id="v-|\Z)', main_html))
    assert set(views) == {r["view"] for r in ROUTES}, sorted(views)
    tail = src[src.index("</footer>"):]
    scripts = re.findall(r"<script>\n?(.*?)</script>", tail, re.S)
    old_switch = '<button type="button" id="lang" aria-label="Jazyk" hidden>EN</button>'
    assert header.count(old_switch) == 1

    # úklid starého výstupu (jen to, co vyrábí tenhle skript)
    shutil.rmtree(ASSETS, ignore_errors=True)
    for d in ("portfolio", "services"):
        shutil.rmtree(OUT / d, ignore_errors=True)
    for f in OUT.glob("*.html"):
        f.unlink()
    for f in (OUT / "en").glob("**/*.html") if (OUT / "en").exists() else []:
        f.unlink()
    for d in ("portfolio", "services"):
        shutil.rmtree(OUT / "en" / d, ignore_errors=True)
    ASSETS.mkdir(parents=True)

    css_b = (css.strip() + "\n" + EXTRA_CSS).encode()
    css_url = f"/assets/site-{fingerprint(css_b)}.css"
    (OUT / css_url.lstrip("/")).write_bytes(css_b)
    js_urls = {}
    for lang, swaps in ((CS, ()), (EN_, EN.JS)):
        js_b = build_js(scripts, swaps).encode()
        js_urls[lang["lang"]] = f"/assets/site-{lang['lang']}-{fingerprint(js_b)}.js"
        (OUT / js_urls[lang["lang"]].lstrip("/")).write_bytes(js_b)

    for r in ROUTES:
        views[r["view"]] = extract_images(views[r["view"]])
    portrait = by_alt["Pavel Kroupa"]

    report = []
    missing_all = []
    used_all = set()
    for lang in LANGS:
        for r in ROUTES:
            meta = lang["meta"][r["route"]]
            path = path_for(r["route"], lang)
            other = EN_ if lang is CS else CS
            alt_paths = {l["lang"]: path_for(r["route"], l) for l in LANGS}

            sw = lang["switch"]
            body, ftr = views[r["view"]], footer
            hdr = header.replace(old_switch, f'<a id="lang" class="lang" href="{alt_paths[other["lang"]]}" '
                                             f'hreflang="{sw["hreflang"]}" lang="{sw["hreflang"]}" '
                                             f'aria-label="{sw["aria"]}">{sw["label"]}</a>')
            if lang is EN_:
                body, miss, used = i18n.translate(body, EN.UNITS, EN.ATTRS, EN.SAME)
                hdr, miss2, used2 = i18n.translate(hdr, EN.UNITS, EN.ATTRS, EN.SAME)
                ftr, miss3, used3 = i18n.translate(footer, EN.UNITS, EN.ATTRS, EN.SAME)
                missing_all += [(r["path"], m) for m in miss + miss2 + miss3]
                used_all |= used | used2 | used3
            body, hdr, ftr = map_links(body, lang), map_links(hdr, lang), map_links(ftr, lang)

            # strukturovaná data jen o tom, co je na stránce vidět; jeden h1; žádné zástupné texty
            assert len(meta["desc"]) <= 160, (lang["lang"], r["path"], len(meta["desc"]))
            assert body.count("<h1") == 1, (lang["lang"], r["path"], body.count("<h1"))
            visible = re.sub(r"<[^>]+>", " ", body)
            assert not PLACEHOLDER.search(visible), (lang["lang"], r["path"], PLACEHOLDER.search(visible).group(0))

            for target in NAV:
                old = f'<a class="lnk" href="{path_for(target, lang)}" data-nav="{target}">{lang["nav"][target]}</a>'
                assert old in hdr, old
                if target == r["nav"]:
                    hdr = hdr.replace(old, f'<a class="lnk on" href="{path_for(target, lang)}" data-nav="{target}" '
                                           f'aria-current="page">{lang["nav"][target]}</a>')

            ld = json.dumps(jsonld(r, lang, body, portrait), ensure_ascii=False, indent=1).replace("</", "<\\/")
            url = url_for(path)
            og = SITE + lang["og_dir"] + meta["og"] + ".png"
            alternates = "\n".join(f'<link rel="alternate" hreflang="{l["lang"]}" href="{url_for(alt_paths[l["lang"]])}">'
                                   for l in LANGS)
            page_html = f'''<!doctype html>
<html lang="{lang["lang"]}" data-route="{r["route"]}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta["title"]}</title>
<meta name="description" content="{meta["desc"]}">
<meta name="keywords" content="{lang["keywords"]}">
<meta name="author" content="Pavel Kroupa">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{url_for(alt_paths["en"])}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#FFCE1B">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pavel Kroupa">
<meta property="og:locale" content="{lang["locale"]}">
<meta property="og:locale:alternate" content="{other["locale"]}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{meta["title"]}">
<meta property="og:description" content="{meta["desc"]}">
<meta property="og:image" content="{og}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{lang["og_alt"][meta["og"]]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{meta["title"]}">
<meta name="twitter:description" content="{meta["desc"]}">
<meta name="twitter:image" content="{og}">
{chr(10).join(fonts)}
<link rel="stylesheet" href="{css_url}">
<script type="application/ld+json">
{ld}
</script>

{hdr}

<main>
<div id="{r["view"]}">
{body}
</div>
</main>

{ftr}

<script src="{js_urls[lang["lang"]]}"></script>
</html>
'''
            f = file_for(path)
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(page_html, encoding="utf-8")
            assert "data:image" not in page_html and 'href="#/' not in page_html
            report.append((path, f.stat().st_size))

    # Stránka 404 pro každou verzi: hlavička, krátký text a patička webu. Cloudflare Pages
    # pro neexistující adresu vrátí nejbližší 404.html (pro /en/… tu anglickou).
    for lang in LANGS:
        nf = lang["notfound"]
        other = EN_ if lang is CS else CS
        sw = lang["switch"]
        hdr = header.replace(old_switch, f'<a id="lang" class="lang" href="{path_for("/", other)}" hreflang="{sw["hreflang"]}" '
                                         f'lang="{sw["hreflang"]}" aria-label="{sw["aria"]}">{sw["label"]}</a>')
        ftr = footer
        if lang is EN_:
            hdr = i18n.translate(hdr, EN.UNITS, EN.ATTRS, EN.SAME)[0]
            ftr = i18n.translate(footer, EN.UNITS, EN.ATTRS, EN.SAME)[0]
        hdr, ftr = map_links(hdr, lang), map_links(ftr, lang)
        page_html = f'''<!doctype html>
<html lang="{lang["lang"]}" data-route="/404">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{nf["title"]}</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#FFCE1B">
{chr(10).join(fonts)}
<link rel="stylesheet" href="{css_url}">

{hdr}

<main>
<div id="v-404">
  <section class="canvas dots notfound">
    <div class="wrap">
      <p class="eyebrow">{nf["eyebrow"]}</p>
      <h1>{nf["h1"]}</h1>
      <p class="lede">{nf["lede"]}</p>
      <div class="row">
        <a class="btn btn-fill" href="{path_for("/", lang)}">{nf["home"]}</a>
        <a class="btn btn-line" href="{path_for("/contact", lang)}">{nf["contact"]}</a>
      </div>
    </div>
  </section>
</div>
</main>

{ftr}

<script src="{js_urls[lang["lang"]]}"></script>
</html>
'''
        f = OUT / (lang["prefix"].lstrip("/") + "/404.html" if lang["prefix"] else "404.html")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(page_html, encoding="utf-8")

    if missing_all:
        seen = set()
        print("Chybí anglický překlad (doplňte do web/build/en.py):", file=sys.stderr)
        for p, m in missing_all:
            if m not in seen:
                seen.add(m)
                print(f"  {p}: {m!r}", file=sys.stderr)
        sys.exit(1)
    unused = set(EN.UNITS) - used_all
    if unused:
        print(f"Pozor: {len(unused)} anglických textů se nikde nepoužilo (zdroj se změnil?):", file=sys.stderr)
        for u in sorted(unused):
            print(f"  {u[:100]!r}", file=sys.stderr)

    urls = "\n".join(f"  <url>\n    <loc>{url_for(p)}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>" for p, _ in report)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n'
                                     f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
                                     encoding="utf-8")
    print(f"{len(report)} stránek, {len(images)} obrázků, styl {css_url}, skripty {', '.join(js_urls.values())}")
    for p, size in report:
        print(f"  {p:36s} {size / 1024:6.1f} kB")


if __name__ == "__main__":
    main()
