# Round 16 (5. 10. 2026): SEO a AI: meta značky, obrázky pro sdílení, JSON-LD, titulek a popis podle stránky,
# robots.txt, sitemap.xml, llms.txt do repa.
import json as _json
SITE_URL = 'https://www.pavelkroupa.com/'
PAGES = {  # route: (titulek, popis, og obrázek)
    '/': ('Pavel Kroupa · Definice produktu a funkční prototypy', 'Pomáhám týmům rozhodnout, co postavit. Workshop s lidmi, kteří rozhodují, funkční prototyp a hotové zadání. S AI za dny, ne týdny.', 'og-uvod'),
    '/portfolio': ('Portfolio · Pavel Kroupa', 'Čtyři firmy, čtyři zaseknuté produkty. Coinmate, Leeaf, Heirloom a BRENO. Co se rozhodlo a jak to dopadlo.', 'og-portfolio'),
    '/reference': ('Reference · Pavel Kroupa', 'Doporučení od lidí, se kterými jsem pracoval. V původním znění z LinkedInu.', 'og-portfolio'),
    '/work/heirloom': ('Heirloom: nový business směr za čtyři iterace', 'Digitální dědictví. Nejdřív funkční prototyp, potom zadání. Nový směr jsme uzavřeli za čtyři sezení.', 'og-portfolio'),
    '/work/coinmate': ('Coinmate: design systém a nová identita', 'Regulovaná kryptoburza. Nejdřív design systém, potom nová identita. Rebranding spuštěn 1. 10. 2026.', 'og-portfolio'),
    '/work/leeaf': ('Leeaf: jedna aplikace pro mnoho klinik', 'Léčba neplodnosti. Škálovatelný design systém a white label. Další kliniky běžely na stejném systému.', 'og-portfolio'),
    '/work/breno': ('BRENO: dvoudenní prioritizace backlogu', 'Maloobchod a e-shop. Dvoudenní workshop přes WPP. Vedení, vývoj i marketing se shodli na pořadí priorit.', 'og-portfolio'),
    '/services': ('Služby · Decision Prototype, audit, vedení produktu', 'Tři způsoby spolupráce. Decision Prototype od 49 000 Kč, audit od 29 000 Kč, vedení produktu od 120 000 Kč měsíčně.', 'og-decision-prototype'),
    '/services/decision-prototype': ('Decision Prototype: funkční prototyp za pár dní', 'Workshop s lidmi, kteří rozhodují, a funkční prototyp na webu. Jeden den, dva, nebo týden. Od 49 000 Kč.', 'og-decision-prototype'),
    '/services/audit': ('Audit produktu za pět dní · Pavel Kroupa', 'Nahrávka obrazovky s komentářem a seznam, co opravit dřív. Bez schůzek. Od 29 000 Kč.', 'og-audit'),
    '/services/fractional': ('Vedení produktu a designu na část úvazku', 'Dva dny v týdnu ve vašem týmu, nejméně tři měsíce. Dokud nenajdete stálého člověka. Od 120 000 Kč měsíčně.', 'og-vedeni-produktu'),
    '/about': ('O mně · Pavel Kroupa', 'Třináct let dovádím týmy k rozhodnutí. Banky, zdravotnictví, krypto. Praha a Amsterdam.', 'og-uvod'),
    '/contact': ('Kontakt · Pavel Kroupa', 'Napište mi, kde jste se zasekli. Třicetiminutový hovor v Praze, v Amsterdamu nebo online.', 'og-uvod'),
}
KEYWORDS = ('funkční prototyp, prototyp aplikace, zadání pro vývoj, specifikace aplikace, product discovery workshop, design sprint, UX audit, '
            'audit produktu, vedení produktu na část úvazku, fractional CPO, fractional product lead, produktový design, design systém, '
            'UX konzultant Praha, fintech, kryptoburza, bankovnictví, zdravotnictví, decision prototype, product definition')
FAQ = [('Kolik to stojí?', 'Platíte za projekt, ne za hodiny. Audit od 29 000 Kč, Decision Prototype od 49 000 Kč, část úvazku od 120 000 Kč měsíčně.'),
       ('Nabízíte balíčky?', 'Ano, tři výše. Když se nehodí ani jeden, upravím rozsah. Sazbu ne.'),
       ('Jak poznám, co se hodí pro mě?', 'Napište mi, kde jste se zasekli. Na třicetiminutovém hovoru vám řeknu, co dává smysl. Klidně i to, že nic z toho.'),
       ('Pracujete s malými firmami, nebo jen s velkými?', 'Obojí. Rozhoduje, jestli je co rozhodnout a jestli u stolu sedí někdo, kdo o tom smí rozhodnout.'),
       ('Sahá prototyp na náš produkční kód?', 'Ne. Používá vaše komponenty, ale produkční kód to není. Vývoj podle něj staví až po rozhodnutí.'),
       ('Komu prototyp potom patří?', 'Vám. Pokud jsem repozitář založil u sebe, převedu ho na vás.')]
def _offer(name, desc, price, url, unit=None):
    ps = {'@type': 'PriceSpecification', 'minPrice': price, 'priceCurrency': 'CZK'}
    if unit: ps['unitText'] = unit
    return {'@type': 'Offer', 'url': SITE_URL + url, 'priceSpecification': ps,
            'itemOffered': {'@type': 'Service', 'name': name, 'description': desc, 'provider': {'@id': SITE_URL + '#pavel'}}}
LD = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'Person', '@id': SITE_URL + '#pavel', 'name': 'Pavel Kroupa', 'url': SITE_URL, 'email': 'mailto:info@pavelkroupa.com',
     'image': SITE_URL + 'og/og-uvod.png', 'jobTitle': 'Definice produktu a vedení designu', 'knowsLanguage': ['cs', 'en'],
     'workLocation': [{'@type': 'Place', 'name': 'Praha'}, {'@type': 'Place', 'name': 'Amsterdam'}],
     'knowsAbout': ['funkční prototyp', 'product discovery', 'UX audit', 'design systém', 'vedení produktu', 'fintech', 'zdravotnictví'],
     'sameAs': ['https://www.linkedin.com/in/pavelkroupa/']},
    {'@type': 'ProfessionalService', '@id': SITE_URL + '#sluzby', 'name': 'Pavel Kroupa', 'url': SITE_URL, 'image': SITE_URL + 'og/og-uvod.png',
     'description': PAGES['/'][1], 'founder': {'@id': SITE_URL + '#pavel'}, 'areaServed': ['Česká republika', 'Nizozemsko', 'online'],
     'identifier': {'@type': 'PropertyValue', 'propertyID': 'IČO', 'value': '87977753'},
     'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Služby', 'itemListElement': [
         _offer('Decision Prototype', 'Workshop s lidmi, kteří rozhodují, a funkční prototyp na webu. Jeden den, dva, nebo týden.', 49000, '#/services/decision-prototype'),
         _offer('Audit rozhodnutí', 'Nahrávka obrazovky s komentářem a seznam, co opravit dřív. Pět pracovních dní, bez schůzek.', 29000, '#/services/audit'),
         _offer('Vedení produktu a designu na část úvazku', 'Dva dny v týdnu ve vašem týmu, nejméně tři měsíce.', 120000, '#/services/fractional', 'MONTH')]}},
    {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
]}
t, d, img = PAGES['/']
HEAD_SEO = f'''<meta name="description" content="{d}">
<meta name="keywords" content="{KEYWORDS}">
<meta name="author" content="Pavel Kroupa">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE_URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pavel Kroupa">
<meta property="og:locale" content="cs_CZ">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{SITE_URL}og/{img}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Pavel Kroupa: Pomáhám týmům rozhodnout, co postavit.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE_URL}og/{img}.png">
<script type="application/ld+json">{_json.dumps(LD, ensure_ascii=False)}</script>
'''
TITLE_JS = '''<script>
(function(){var P=''' + _json.dumps({k: [v[0], v[1]] for k, v in PAGES.items()}, ensure_ascii=False) + ''';
  var md=document.querySelector('meta[name="description"]');
  function set(){var h=(location.hash||"#/").slice(1);if(h.indexOf("/contact")===0)h="/contact";var p=P[h]||P["/"];document.title=p[0];if(md)md.setAttribute("content",p[1]);}
  window.addEventListener("hashchange",set);set();})();
</script>'''

ROBOTS = f'''# Vyhledávače i AI crawlery smí číst celý web.
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {SITE_URL}sitemap.xml
'''
SITEMAP = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE_URL}</loc><lastmod>2026-10-05</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url>
</urlset>
'''
LLMS = f'''# Pavel Kroupa

> Pomáhám týmům rozhodnout, co postavit. Sednu si s těmi, kdo rozhodují, udělám funkční prototyp a s AI máme hotové zadání za dny, ne týdny. Praha, Amsterdam a online.

English: Pavel Kroupa is a product definition and design lead based in Prague and Amsterdam. He runs decision workshops, builds functional prototypes with AI in days and turns them into specs engineering can build from. Clients include regulated crypto, banking and healthcare.

## Služby

- [Decision Prototype]({SITE_URL}#/services/decision-prototype): workshop s lidmi, kteří rozhodují, a funkční prototyp na webu. Jeden den od 49 000 Kč, dva dny od 125 000 Kč, týden od 220 000 Kč.
- [Audit rozhodnutí]({SITE_URL}#/services/audit): nahrávka obrazovky s komentářem a seznam, co opravit dřív. Pět pracovních dní, bez schůzek. Od 29 000 Kč.
- [Vedení produktu a designu na část úvazku]({SITE_URL}#/services/fractional): dva dny v týdnu ve vašem týmu, nejméně tři měsíce. Od 120 000 Kč měsíčně.

Platí se za projekt, ne za hodiny. Konečnou nabídku posílám po první schůzce. Nejsem plátce DPH.

## Případy

- [Coinmate]({SITE_URL}#/work/coinmate): regulovaná kryptoburza. Nejdřív design systém, potom nová identita. Rebranding spuštěn 1. 10. 2026.
- [Leeaf]({SITE_URL}#/work/leeaf): léčba neplodnosti. Jedna aplikace pro mnoho klinik, škálovatelný design systém a white label.
- [Heirloom]({SITE_URL}#/work/heirloom): digitální dědictví. Nový business směr za čtyři iterace, nejdřív funkční prototyp, potom zadání.
- [BRENO]({SITE_URL}#/work/breno): maloobchod a e-shop. Dvoudenní prioritizace business backlogu přes WPP.

## Klienti

Komerční banka, Česká spořitelna, Modrá pyramida, Centropol, WPP, ESET, SatoshiLabs, Jablotron, Coinmate, Leeaf, BRENO.

## Kontakt

- E-mail: info@pavelkroupa.com
- Termín hovoru: https://cal.com/pavelkroupa
- LinkedIn: https://www.linkedin.com/in/pavelkroupa/
- Firma: Pavel Kroupa, IČO 87977753, Mezno 88, 257 86 Mezno, Česká republika
'''

def post_patch16(out):
    out = rep(out, '<title>pavelkroupa.com v5</title>', f'<title>{PAGES["/"][0]}</title>')
    out = rep(out, '<meta name="theme-color" content="#FFCE1B">\n', '<meta name="theme-color" content="#FFCE1B">\n' + HEAD_SEO)
    out = out.replace('alt="logo-breno-dark"', 'alt="BRENO"')
    out = re.sub(r'(<div class="polaroid-img"><img [^>]*?)alt="[^"]*"', r'\1alt="Pavel Kroupa"', out)
    repo = R + 'Career/05 Web/repo/'
    for fn, txt in (('robots.txt', ROBOTS), ('sitemap.xml', SITEMAP), ('llms.txt', LLMS)):
        open(repo + fn, 'w').write(txt)
    return out + TITLE_JS
