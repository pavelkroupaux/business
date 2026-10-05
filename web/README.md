# pavelkroupa.com, verze 5

Statický web, česky a anglicky. Zdroj je jeden soubor, ze kterého se vyrobí samostatné stránky. Hotové stránky leží v kořeni repozitáře, odkud je publikuje GitHub Pages.

| Cesta | Co to je |
|---|---|
| `src/index.html` | celý web v jednom souboru (sekce za `#/`). Je to `index.html` z buildu ve vaultu. Otevřený v prohlížeči slouží jako náhled. |
| `build/` | build ve vaultu (`build_v5b.py`, kola `v5_round2.py` až `v5_round18.py`, loga, `og.py`, písma) a skripty pro samostatné stránky (`pages.py`, `i18n.py`, `en.py`, `ds.py`, `og_en.py`) |
| `build/fonts/web/` | písmo Shantell Sans pro web (woff2, stejné soubory jako na Google Fonts a malý český výřez) |
| `public/` | stará kopie webu pro Cloudflare Pages. Nepoužívá se, dá se smazat. |

V kořeni repozitáře:

| Cesta | Co to je |
|---|---|
| `index.html`, `about/`, `contact/`, `portfolio/`, `services/`, `en/`, `ds/`, `404.html`, `assets/`, `sitemap.xml` | vyrábí `pages.py`, ručně se neupravují |
| `og/` | obrázky pro sdílení, 1200 × 630 px. České z `og.py` ve vaultu, anglické v `og/en/` z `og_en.py` |
| `logo/` | logo: `logo/pk/` je pk s linkou, `logo/` je samotné lepítko |
| `favicon.*`, `apple-touch-icon.png`, `icon-*.png`, `site.webmanifest` | favikona a ikony aplikace (lepítko s fajfkou) |
| `robots.txt`, `llms.txt` | pro vyhledávače a AI asistenty, upravují se ručně |
| `CNAME`, `_config.yml` | doména pro GitHub Pages a seznam toho, co se nepublikuje (`web/`, README) |

## Jak se web mění

1. Obsah se upravuje ve vaultu, build vyrobí `index.html` (`python3 build_v5b.py`, viz níž).
2. Ten `index.html` se zkopíruje do `web/src/index.html`.
3. Z kořene repozitáře se spustí `python3 web/build/pages.py`. Vyrobí české i anglické stránky, stránku 404, design systém na `/ds/`, vytáhne obrázky do `assets/img` a obnoví `sitemap.xml`. Všechno v kořeni repozitáře.
4. Když se změnila úvodní kresba, ilustrace služeb nebo loga případů: `python3 web/build/og_en.py` (anglické obrázky pro sdílení).
5. Commit a push do `main`. GitHub Pages web nasadí sám, průběh je vidět v záložce Actions.

Knihovny pro krok 3 a 4 jsou v `build/requirements.txt` (`pip3 install -r web/build/requirements.txt`). Bez nich se stránky vyrobí taky, jen bez zmenšeného stylu a skriptu a bez fotek ve WebP. `pages.py` to na konci vypíše.

Kolo 18 obsahuje opravy, které vznikly v repozitáři (roky Leeaf, galerie v O mně, hlavička na mobilu, nadpisy na nejmenších telefonech, notebook a infografiky při omezeném pohybu a další, popis je v souboru). Musí být i ve vaultu, jinak je další build vrátí zpátky. Ve vaultu stačí zkopírovat `v5_round18.py`, `build_v5b.py` a `src/img/mapa-prototypu.jpg`.

`pages.py` hlídá, aby se nic nerozjelo, a když něco nesedí, skončí chybou:
- každá stránka má právě jeden nadpis `h1` a žádný zástupný text v hranatých závorkách,
- ceny ve strukturovaných datech jsou vidět na stránce,
- nezůstal žádný odkaz `#/`,
- každý český text má anglický překlad.

Náhled vyrobených stránek: v kořeni repozitáře `python3 -m http.server`, pak `http://localhost:8000/`. Stránky a odkazy fungují jako na GitHub Pages, jen místo stránky 404 se ukáže obyčejná chyba.

## Adresy

Každá stránka je složka s `index.html`, adresy proto končí lomítkem: `/about/`, `/portfolio/coinmate/`. Tak je GitHub Pages obslouží vždy. Starou adresu bez lomítka (`/about`, `/portfolio/coinmate` z webu na Frameru) GitHub Pages přesměruje na tu s lomítkem, takže odkazy z Googlu fungují dál. Staré odkazy s `#/` přesměruje skript webu.

GitHub Pages má jen jednu stránku 404, českou v kořeni. Na adresách `/en/…` sama přejde na anglickou (`/en/404.html`).

| Česky | Anglicky | Sekce ve zdroji |
|---|---|---|
| `/` | `/en/` | `#/` |
| `/portfolio/` | `/en/portfolio/` | `#/portfolio` |
| `/portfolio/heirloom/`, `/coinmate/`, `/leeaf/`, `/breno/` | `/en/portfolio/…/` | `#/work/…` |
| `/services/` | `/en/services/` | `#/services` |
| `/services/decision-prototype/`, `/audit/`, `/fractional/` | `/en/services/…/` | `#/services/…` |
| `/about/` | `/en/about/` | `#/about` |
| `/contact/` | `/en/contact/` | `#/contact`, služba se předvyplní přes `?service=audit` |
| `/ds/` | | design systém, jen česky a jen pro vnitřní potřebu |

Přepínač CS/EN v hlavičce vede na stejnou stránku v druhém jazyce.

## Rychlost

- Písmo Shantell Sans je z vlastního serveru, ne z Google Fonts. Odpadly dva cizí servery a styl, který blokoval vykreslení. Česká stránka stáhne latinku a malý výřez s háčky a čárkami (8 kB), anglická jen latinku.
- Styl a skripty jsou zmenšené, fotky ve WebP (jen když vyjdou aspoň o 10 % menší, jinak zůstává JPEG). SVG bez balastu z editoru.
- Soubory v `assets/` mají v názvu otisk obsahu. Po změně dostanou nový název, takže prohlížeč nikdy nepoužije starou verzi.
- Zvolený světlý nebo tmavý režim se nastaví hned na začátku stránky, takže při přechodu mezi stránkami nic neproblikne.

## Design systém

Stránka `/ds/` ukazuje identitu, hlas, loga, ikony, barvy, písmo, vizuální jazyk, pohyb a komponenty. Vyrábí ji `build/ds.py` ze skutečného stylu a kusů stránek, takže se změny na webu propíšou i tam. Když z webu zmizí text nebo zásada, kterou stránka cituje, `pages.py` vypíše upozornění.

Stránka je schovaná, ne zamčená: nevede na ni žádný odkaz, není v `sitemap.xml` ani v `llms.txt`, má `noindex` a `robots.txt` ji zakazuje. Kdo zná adresu, otevře ji. GitHub Pages neumí stránku zamknout heslem.

## Anglická verze

Adresy jsou stejné jako české, jen s `/en` na začátku: `/en/`, `/en/services/audit/`, `/en/portfolio/coinmate/` a tak dál.

Texty jsou v `build/en.py` jako dvojice `cs:` a `en:`. Jsou psané podle zásad Nielsen Norman Group: krátké věty, činný rod, nejdůležitější informace na začátku, čísla jako číslice („2 days a week“), americký pravopis. Ceny jsou v korunách („From CZK 49,000“).

Když se změní český text, `pages.py` vypíše, který anglický překlad chybí. Stačí doplnit dvojici do `en.py`. Doporučení z LinkedInu jsou v originále anglicky a zůstávají beze změny.

## SEO a AI

Hlavní adresa je `https://pavelkroupa.com`. `www.pavelkroupa.com` na ni přesměruje GitHub.

- Titulky, popisy, klíčová slova a obrázky pro sdílení české verze: `PAGES` a `KEYWORDS` ve `build/v5_round16.py`. `pages.py` je čte odtud, takže web v jednom souboru i samostatné stránky mají stejné.
- Anglická metadata: `META` a `KEYWORDS` v `build/en.py`.
- Strukturovaná data (JSON-LD) vyrábí `pages.py` pro každou stránku: osoba, firma s IČO, služby s cenami, drobečková navigace a otázky a odpovědi tak, jak jsou na stránce.
- Každá stránka odkazuje na svou druhou jazykovou verzi (`hreflang`). Pro ostatní jazyky (`x-default`) vede na anglickou.
- `robots.txt`: povoluje vyhledávače i AI crawlery, kromě `/ds`.
- `llms.txt`: shrnutí webu pro AI asistenty, česky a na konci anglicky. Při změně služeb, cen nebo případů ho upravte ručně.

## Nasazení (GitHub Pages)

- GitHub, Settings, Pages: Deploy from a branch, větev `main`, složka `/ (root)`.
- Custom domain: `pavelkroupa.com` (zapisuje se do souboru `CNAME`), zapnuté Enforce HTTPS.
- Cloudflare: jen DNS. Čtyři záznamy A pro `pavelkroupa.com` (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153) a `www` jako CNAME na `pavelkroupaux.github.io`, vše DNS only (šedý obláček).
- `_config.yml` říká, že se nepublikuje složka `web/` a `README.md`. Bez něj by na webu byl i zdroj a build.

## Build ve vaultu

Build běží z Obsidianu. Cesty se počítají od složky `build/`.

```bash
cd build
pip3 install -r requirements.txt
python3 build_v5b.py      # index.html + kopie v ../verze/site-v5.html
python3 og.py             # obrázky pro sdílení
python3 export_pk.py      # logo pk
python3 export_logo.py    # lepítko a favikona
```

- `build_v5b.py` vezme `src/site-v4.html` a texty z `src/v5src/` a postupně spustí `v5_round2.py` až `v5_round18.py`. Každé kolo je jedna sada úprav.
- Loga klientů čte z `Career/07 Assets/loga klientů/`. Ta složka v repu není, build proto funguje jen uvnitř vaultu.
- Písma jsou v `build/fonts/` (Inter a Shantell Sans, licence SIL OFL 1.1, texty licencí jsou vedle).
- `qa.py` vyrobí náhledovou stránku s webem v několika šířkách. Ukládá do `build/_draft/`, a ta složka se do gitu nenahrává.

## Co zatím nefunguje

- Kontaktní formulář nic neodesílá, jen ukáže potvrzení. Je potřeba napojit službu pro formuláře.
- Případ Heirloom zatím nemá citaci. Doplní se do zdroje za odstavec „Jak to dopadlo“, ve stejném tvaru jako `case-ref` u ostatních případů.
