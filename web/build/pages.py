#!/usr/bin/env python3
"""Rozdělí web z jednoho souboru na samostatné stránky.

Zdroj:  web/src/index.html  (celý web v jednom souboru, sekce za #/, otevře se i jako náhled)
Výstup: web/public/*.html, web/public/portfolio/*.html, web/public/services/*.html,
        web/public/assets/ (styly, skript a obrázky vytažené ze souboru), web/public/sitemap.xml

Spuštění z kořene repozitáře:
    python3 web/build/pages.py

Titulky, popisy a strukturovaná data jednotlivých stránek jsou níže v PAGES a v jsonld().
Ceny a odpovědi ve strukturovaných datech musí sedět s textem na stránce, skript to kontroluje.
Ruční soubory ve web/public (robots.txt, llms.txt, 404.html, ikony, og.jpg, _headers) nemění.
"""
import base64
import datetime
import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
SRC = WEB / "src" / "index.html"
OUT = WEB / "public"
ASSETS = OUT / "assets"
SITE = "https://www.pavelkroupa.com"
HOME = SITE + "/"
TODAY = datetime.date.today().isoformat()
BRAND = " · Pavel Kroupa"

# route = klíč ze zdrojového #/ routeru, path = skutečná adresa stránky
PAGES = [
    dict(route="/", view="v-home", path="/", nav="/", kind="home",
         title="Pavel Kroupa · Definice produktu a vedení designu",
         og="Pomáhám týmům rozhodnout, co postavit.",
         desc="Pomáhám týmům rozhodnout, co postavit. Workshop s lidmi, kteří rozhodují, a funkční prototyp za dny, ne týdny. Praha, Amsterdam nebo online.",
         services=["dp", "audit", "fractional"]),
    dict(route="/portfolio", view="v-portfolio", path="/portfolio", nav="/portfolio", kind="collection",
         title="Portfolio a reference" + BRAND,
         og="Čtyři firmy. Čtyři zaseknuté produkty.",
         desc="Čtyři firmy, čtyři zaseknuté produkty. Co bylo zaseknuté, co jsem udělal a jak to dopadlo. A co říkají lidé, se kterými jsem pracoval.",
         crumbs=[("Portfolio", "/portfolio")]),
    dict(route="/work/heirloom", view="v-case-heirloom", path="/portfolio/heirloom", nav="/portfolio", kind="case",
         client="Heirloom",
         title="Heirloom: nový business směr za čtyři iterace" + BRAND,
         og="Heirloom: Nový business směr za čtyři iterace.",
         desc="Digitální dědictví, nový produkt od nuly. Místo obrazovek ve Figmě funkční prototyp v každé iteraci. Nový směr uzavřený za čtyři sezení.",
         crumbs=[("Portfolio", "/portfolio"), ("Heirloom", "/portfolio/heirloom")]),
    dict(route="/work/coinmate", view="v-case-coinmate", path="/portfolio/coinmate", nav="/portfolio", kind="case",
         client="Coinmate",
         title="Coinmate: nejdřív design systém, potom nová identita" + BRAND,
         og="Coinmate: Nejdřív design systém, potom nová identita.",
         desc="Regulovaná kryptoburza. Externě, dva dny v týdnu. Nejdřív jeden design systém pro desktop, iOS i Android, potom na něm nová identita.",
         crumbs=[("Portfolio", "/portfolio"), ("Coinmate", "/portfolio/coinmate")]),
    dict(route="/work/leeaf", view="v-case-leeaf", path="/portfolio/leeaf", nav="/portfolio", kind="case",
         client="Leeaf",
         title="Leeaf: jedna aplikace pro mnoho klinik" + BRAND,
         og="Leeaf: Jedna aplikace pro mnoho klinik.",
         desc="Léčba neplodnosti. Jeden design systém pro web, portál pro lékaře a mobilní aplikaci. Nová klinika je konfigurace, další kliniky běžely beze mě.",
         crumbs=[("Portfolio", "/portfolio"), ("Leeaf", "/portfolio/leeaf")]),
    dict(route="/work/breno", view="v-case-breno", path="/portfolio/breno", nav="/portfolio", kind="case",
         client="BRENO",
         title="BRENO: dvoudenní prioritizace business backlogu" + BRAND,
         og="BRENO: Dvoudenní prioritizace business backlogu.",
         desc="Maloobchod a e-shopy. Všechno mělo vysokou prioritu. Po dvoudenním workshopu se vedení, vývoj i marketing shodli na pořadí priorit.",
         crumbs=[("Portfolio", "/portfolio"), ("BRENO", "/portfolio/breno")]),
    dict(route="/services", view="v-services", path="/services", nav="/services", kind="collection",
         title="Služby a ceny" + BRAND,
         og="Tři způsoby, jak spolupracovat.",
         desc="Tři způsoby, jak spolupracovat: Decision Prototype od 49 000 Kč, Audit rozhodnutí od 29 000 Kč a vedení produktu na část úvazku od 120 000 Kč měsíčně.",
         crumbs=[("Služby", "/services")], services=["dp", "audit", "fractional"], faq="services"),
    dict(route="/services/decision-prototype", view="v-svc-dp", path="/services/decision-prototype", nav="/services", kind="page",
         title="Decision Prototype: funkční prototyp za pár dní" + BRAND,
         og="Decision Prototype: Funkční prototyp za pár dní.",
         desc="Rozhodnutí, na které se dá kliknout. Workshop s lidmi, kteří rozhodují, funkční prototyp na webu a zápis, co jsme rozhodli a proč. Od 49 000 Kč.",
         crumbs=[("Služby", "/services"), ("Decision Prototype", "/services/decision-prototype")], services=["dp"], faq="dp"),
    dict(route="/services/audit", view="v-svc-audit", path="/services/audit", nav="/services", kind="page",
         title="Audit rozhodnutí: co váš produkt brzdí" + BRAND,
         og="Audit rozhodnutí: Zjistěte, co váš produkt brzdí. Za pět dní.",
         desc="Projdu váš produkt a na nahrávce obrazovky ukážu, co nefunguje a v jakém pořadí bych to opravoval. Pět pracovních dní, bez schůzek. Od 29 000 Kč.",
         crumbs=[("Služby", "/services"), ("Audit rozhodnutí", "/services/audit")], services=["audit"]),
    dict(route="/services/fractional", view="v-svc-fractional", path="/services/fractional", nav="/services", kind="page",
         title="Vedení produktu a designu na část úvazku" + BRAND,
         og="Vedení produktu, dokud nenajdete stálého člověka.",
         desc="Dva dny v týdnu ve vašem týmu, dokud nenajdete stálého člověka. Jasný směr každý týden a rozsah dřív, než se staví. Od 120 000 Kč měsíčně.",
         crumbs=[("Služby", "/services"), ("Vedení produktu a designu na část úvazku", "/services/fractional")],
         services=["fractional"]),
    dict(route="/about", view="v-about", path="/about", nav="/about", kind="profile",
         title="O mně: třináct let dovádím týmy k rozhodnutí" + BRAND,
         og="Třináct let dovádím týmy k rozhodnutí.",
         desc="Praha a Amsterdam. Přicházím tam, kde se o produktu ještě nerozhodlo, nebo kde se tým cyklí. Jak pracuju, kde jsem pracoval a co říkají lidé.",
         crumbs=[("O mně", "/about")]),
    dict(route="/contact", view="v-contact", path="/contact", nav="/contact", kind="contact",
         title="Kontakt" + BRAND,
         og="Kde jste se zasekli?",
         desc="Napište mi pár vět o tom, kde jste se zasekli. Ozvu se a domluvíme třicetiminutový hovor. V Praze, v Amsterdamu nebo online.",
         crumbs=[("Kontakt", "/contact")]),
]

SERVICES = {
    "dp": dict(id="#decision-prototype", name="Decision Prototype", path="/services/decision-prototype",
               desc="Rozhodnutí, na které se dá kliknout. Přinesete nerozhodnutou věc, odnesete rozhodnutí a funkční prototyp na webu, podle kterého se dá stavět.",
               offers=[("Jeden den", "Jeden workshop a první verze prototypu.", 49000, None),
                       ("Dva dny", "Jedna nerozhodnutá věc, dotažená do konce.", 125000, None),
                       ("Týden", "Celá oblast produktu, víc rozhovorů a workshopů.", 220000, None)]),
    "audit": dict(id="#audit", name="Audit rozhodnutí", path="/services/audit",
                  desc="Projdu váš produkt a na nahrávce obrazovky ukážu, co nefunguje a v jakém pořadí bych to opravoval. Bez schůzek.",
                  offers=[(None, "Pět pracovních dní, bez schůzek.", 29000, None)]),
    "fractional": dict(id="#fractional", name="Vedení produktu a designu na část úvazku", path="/services/fractional",
                       desc="Dva dny v týdnu sedím ve vašem týmu. Rozhoduju s vámi u porad vedení i produktu a držím směr, aby se vývoj necyklil.",
                       offers=[(None, "Dva dny v týdnu, nejméně tři měsíce.", 120000, "MON")]),
}

FAQ = {
    "services": [
        ("Kolik to stojí?", "Platíte za projekt, ne za hodiny. Audit od 29 000 Kč, Decision Prototype od 49 000 Kč, část úvazku od 120 000 Kč měsíčně."),
        ("Nabízíte balíčky?", "Ano, tři výše. Když se nehodí ani jeden, upravím rozsah. Sazbu ne."),
        ("Jak poznám, co se hodí pro mě?", "Napište mi, kde jste se zasekli. Na třicetiminutovém hovoru vám řeknu, co dává smysl. Klidně i to, že nic z toho."),
        ("Pracujete s malými firmami, nebo jen s velkými?", "Obojí. Rozhoduje, jestli je co rozhodnout a jestli u stolu sedí někdo, kdo o tom smí rozhodnout."),
    ],
    "dp": [
        ("Sahá to na náš produkční kód?", "Ne. Používá vaše komponenty, ale produkční kód to není. Vývoj podle něj staví až po rozhodnutí."),
        ("Kde to běží?", "Na GitHubu, za odkazem s heslem."),
        ("Komu to potom patří?", "Vám. Pokud jsem repozitář založil u sebe, převedu ho na vás."),
        ("Co od nás potřebujete?", "Hlavně čas toho, kdo rozhoduje. Přístup k repozitáři nebo design systému pomůže, pokud to vaše bezpečnostní pravidla dovolí."),
    ],
}

NAV_LABELS = {"/": "Úvod", "/portfolio": "Portfolio", "/services": "Služby", "/about": "O mně", "/contact": "Kontakt"}


def path_for(route):
    """#/ route ze zdroje -> skutečná adresa."""
    if route == "/reference":
        return "/portfolio#refs"
    if route.startswith("/work/"):
        return "/portfolio/" + route[len("/work/"):]
    if route.startswith("/contact/"):
        return "/contact?service=" + route[len("/contact/"):]
    return route


def file_for(path):
    return OUT / "index.html" if path == "/" else OUT / (path.lstrip("/") + ".html")


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


def map_links(markup):
    out = re.sub(r'href="#(/[^"]*)"', lambda m: f'href="{path_for(m.group(1))}"', markup)
    assert 'href="#/' not in out
    return out


# ---------------------------------------------------------------- JSON-LD
def offer(name, desc, price, unit):
    spec = {"@type": "UnitPriceSpecification" if unit else "PriceSpecification", "minPrice": price, "priceCurrency": "CZK"}
    if unit:
        spec.update(unitCode=unit, unitText="měsíčně")
    o = {"@type": "Offer", "description": desc, "priceSpecification": spec}
    if name:
        o["name"] = name
    return o


AREAS = [{"@type": "City", "name": "Praha"}, {"@type": "City", "name": "Amsterdam"}]


def price_text(value):
    return f"{value:,}".replace(",", " ") + " Kč"


def jsonld(page, portrait, body):
    url = SITE + page["path"]
    person = {"@type": "Person", "@id": HOME + "#person", "name": "Pavel Kroupa", "url": HOME,
              "image": SITE + portrait, "jobTitle": "Definice produktu a vedení designu",
              "description": "Třináct let dovádím týmy k rozhodnutí. Přicházím tam, kde se o produktu ještě nerozhodlo, nebo kde se tým cyklí a potřebuje se pohnout dál.",
              "email": "info@pavelkroupa.com",
              "workLocation": [{"@type": "Place", "name": "Praha"}, {"@type": "Place", "name": "Amsterdam"}],
              "knowsAbout": ["Definice produktu", "Vedení produktu a designu", "Produktový design", "Design systémy",
                             "Facilitace workshopů", "Prototypování s AI"],
              "sameAs": ["https://www.linkedin.com/in/pavelkroupa/"]}
    business = {"@type": "ProfessionalService", "@id": HOME + "#business", "name": "Pavel Kroupa", "url": HOME,
                "image": SITE + "/og.jpg", "logo": SITE + "/icon-512.png",
                "description": "Definice produktu a vedení designu. Workshopy s lidmi, kteří rozhodují, funkční prototypy a vedení produktu na část úvazku. V Praze, v Amsterdamu nebo online.",
                "founder": {"@id": HOME + "#person"}, "email": "info@pavelkroupa.com",
                "areaServed": AREAS, "priceRange": "od 29 000 Kč", "currenciesAccepted": "CZK",
                "sameAs": ["https://www.linkedin.com/in/pavelkroupa/"]}
    if page["kind"] == "contact":   # sídlo a IČO jsou vidět jen na kontaktu
        business.update(address={"@type": "PostalAddress", "streetAddress": "Mezno 88", "postalCode": "257 86",
                                 "addressLocality": "Mezno", "addressCountry": "CZ"},
                        identifier={"@type": "PropertyValue", "propertyID": "IČO", "value": "87977753"})
    website = {"@type": "WebSite", "@id": HOME + "#website", "url": HOME, "name": "Pavel Kroupa", "inLanguage": "cs",
               "publisher": {"@id": HOME + "#person"}}
    ptype = {"home": "WebPage", "collection": "CollectionPage", "case": "WebPage", "page": "WebPage",
             "profile": "ProfilePage", "contact": "ContactPage"}[page["kind"]]
    webpage = {"@type": ptype, "@id": url + "#webpage", "url": url, "name": page["title"], "description": page["desc"],
               "inLanguage": "cs", "isPartOf": {"@id": HOME + "#website"},
               "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/og.jpg", "width": 1200, "height": 630}}
    if page["kind"] == "profile":
        webpage["mainEntity"] = {"@id": HOME + "#person"}
    else:
        webpage["about"] = {"@id": HOME + "#person"}
    if page["kind"] == "case":
        webpage["about"] = {"@type": "Organization", "name": page["client"]}
        webpage["author"] = {"@id": HOME + "#person"}
    graph = [website, webpage, person, business]
    if page.get("crumbs"):
        items = [("Úvod", "/")] + page["crumbs"]
        bc = {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                                  for i, (n, p) in enumerate(items)]}
        webpage["breadcrumb"] = {"@id": bc["@id"]}
        graph.append(bc)
    for key in page.get("services", []):
        s = SERVICES[key]
        # jen ceny, které jsou na téhle stránce vidět (úvod ukazuje jen nejnižší)
        offers = [offer(*o) for o in s["offers"] if price_text(o[2]) in body]
        assert offers, (page["path"], key)
        graph.append({"@type": "Service", "@id": HOME + s["id"], "name": s["name"], "url": SITE + s["path"],
                      "description": s["desc"], "provider": {"@id": HOME + "#business"}, "areaServed": AREAS,
                      "offers": offers if len(offers) > 1 else offers[0]})
    if page.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "cs",
                      "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                     for q, a in FAQ[page["faq"]]]})
    return {"@context": "https://schema.org", "@graph": graph}


# ---------------------------------------------------------------- skript
BLOCK = "\n/*<<block>>*/\n"


def build_js(scripts):
    # titulek podle sekce potřebuje jen náhled v jednom souboru, tady má titulek každá stránka
    js = BLOCK.join(s for s in scripts if "titulek okna podle zobrazené sekce" not in s)

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
    shim = ("/* staré odkazy s #/ vedou na samostatné stránky */\n(function(){var h=location.hash;if(h.indexOf(\"#/\")!==0)return;"
            "var r=h.slice(1),p=r===\"/reference\"?\"/portfolio#refs\":r.indexOf(\"/work/\")===0?\"/portfolio/\"+r.slice(6):"
            "r.indexOf(\"/contact/\")===0?\"/contact?service=\"+r.slice(9):r;location.replace(p);})();\n")
    # Každý blok zvlášť v try/catch, jako dřív samostatné <script>: chyba v jednom nezastaví ostatní.
    return shim + "\n".join("try{\n" + b + "\n}catch(e){console.error(e);}" for b in js.split(BLOCK))


# ---------------------------------------------------------------- stavba
def main():
    src = SRC.read_text(encoding="utf-8")

    head_src = src[:src.index("<style>")]
    links = re.findall(r"<link\b[^>]*>", head_src)
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    header = re.search(r'<header class="top">.*?</header>', src, re.S).group(0)
    footer = re.search(r'<footer class="foot">.*?</footer>', src, re.S).group(0)
    main_html = src[src.index("<main>\n") + len("<main>\n"):src.index("</main>")]
    views = dict(re.findall(r'(?ms)^<div id="(v-[a-z-]+)"(?: hidden)?>\n(.*?)\n^</div>\s*(?=^<div id="v-|\Z)', main_html))
    assert set(views) == {p["view"] for p in PAGES}, sorted(views)
    tail = src[src.index("</footer>"):]
    scripts = re.findall(r"<script>\n?(.*?)</script>", tail, re.S)

    # úklid starého výstupu (jen to, co vyrábí tenhle skript)
    shutil.rmtree(ASSETS, ignore_errors=True)
    for d in ("portfolio", "services"):
        shutil.rmtree(OUT / d, ignore_errors=True)
    for p in PAGES:
        file_for(p["path"]).unlink(missing_ok=True)
    ASSETS.mkdir(parents=True)

    css_b = css.strip().encode()
    css_url = f"/assets/site-{fingerprint(css_b)}.css"
    (OUT / css_url.lstrip("/")).write_bytes(css_b)
    js_b = build_js(scripts).encode()
    js_url = f"/assets/site-{fingerprint(js_b)}.js"
    (OUT / js_url.lstrip("/")).write_bytes(js_b)

    header = map_links(header)
    footer = map_links(footer)
    for p in PAGES:
        views[p["view"]] = map_links(extract_images(views[p["view"]]))
    portrait = by_alt["Pavel Kroupa"]

    for p in PAGES:
        url = SITE + p["path"] if p["path"] != "/" else HOME
        assert len(p["desc"]) <= 160, (p["path"], len(p["desc"]))
        body = views[p["view"]]
        # strukturovaná data jen o tom, co je na stránce vidět
        for q, a in FAQ.get(p.get("faq"), []):
            assert q in body and a in body, (p["path"], q)
        assert body.count("<h1") == 1, (p["path"], body.count("<h1"))

        nav = header
        for target, label in NAV_LABELS.items():
            old = f'<a class="lnk" href="{target}" data-nav="{target}">{label}</a>'
            assert old in nav, old
            if target == p["nav"]:
                nav = nav.replace(old, f'<a class="lnk on" href="{target}" data-nav="{target}" aria-current="page">{label}</a>')

        ld = json.dumps(jsonld(p, portrait, body), ensure_ascii=False, indent=1).replace("</", "<\\/")
        page_html = f'''<!doctype html>
<html lang="cs" data-route="{p["route"]}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<meta name="author" content="Pavel Kroupa">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111111" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pavel Kroupa">
<meta property="og:locale" content="cs_CZ">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{p["og"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:image" content="{SITE}/og.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Pavel Kroupa: Pomáhám týmům rozhodnout, co postavit. Definice produktu a vedení designu.">
<meta name="twitter:card" content="summary_large_image">
{chr(10).join(links)}
<link rel="stylesheet" href="{css_url}">
<script type="application/ld+json">
{ld}
</script>

{nav}

<main>
<div id="{p["view"]}">
{body}
</div>
</main>

{footer}

<script src="{js_url}"></script>
</html>
'''
        f = file_for(p["path"])
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(page_html, encoding="utf-8")
        assert "data:image" not in page_html and 'href="#/' not in page_html

    urls = "\n".join(f"  <url>\n    <loc>{SITE + p['path'] if p['path'] != '/' else HOME}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>"
                     for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n'
                                     f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
                                     encoding="utf-8")
    sizes = {p["path"]: file_for(p["path"]).stat().st_size for p in PAGES}
    print(f"{len(PAGES)} stránek, {len(images)} obrázků, styl {css_url}, skript {js_url}")
    for k, v in sizes.items():
        print(f"  {k:32s} {v / 1024:6.1f} kB")


if __name__ == "__main__":
    main()
