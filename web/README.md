# pavelkroupa.com, verze 5

Statický web, česky a anglicky. Zdroj je jeden soubor, ze kterého se vyrobí samostatné stránky.

| Cesta | Co to je |
|---|---|
| `src/index.html` | celý web v jednom souboru (sekce za `#/`). Je to `index.html` z buildu ve vaultu. Otevřený v prohlížeči slouží jako náhled. |
| `build/` | build ve vaultu (`build_v5b.py`, kola `v5_round2.py` až `v5_round18.py`, loga, `og.py`, písma) a skripty pro samostatné stránky (`pages.py`, `i18n.py`, `en.py`, `og_en.py`) |
| `public/` | to, co Cloudflare publikuje |
| `public/og/` | obrázky pro sdílení, 1200 × 630 px a `@2x`. České z `og.py`, anglické v `og/en/` z `og_en.py` |
| `public/logo/` | logo: `logo/pk/` je pk s linkou, `logo/` je samotný post-it, `logo/favicon/` favicona |
| `public/favicon.*`, `apple-touch-icon.png`, `icon-*.png` | favicona (post-it s checkem), kopie z `logo/favicon/` |

## Jak se web mění

1. Obsah se upravuje ve vaultu, build vyrobí `index.html` (`python3 build_v5b.py`, viz níž).
2. Ten `index.html` se zkopíruje do `web/src/index.html`.
3. Z kořene repozitáře se spustí `python3 web/build/pages.py`. Vyrobí české i anglické stránky, vytáhne obrázky do `public/assets/img` a obnoví `public/sitemap.xml`.
4. Když se změnila úvodní kresba, ilustrace služeb nebo loga případů: `python3 web/build/og_en.py` (anglické obrázky pro sdílení).
5. Commit a push do `main`. Cloudflare web nasadí sám.

Kolo 18 obsahuje opravy, které vznikly v repozitáři (roky Leeaf, galerie v O mně, hlavička na mobilu a další, popis je v souboru). Musí být i ve vaultu, jinak je další build vrátí zpátky. Ve vaultu stačí zkopírovat `v5_round18.py`, `build_v5b.py` a `src/img/mapa-prototypu.jpg`.

`pages.py` hlídá, aby se nic nerozjelo, a když něco nesedí, skončí chybou:
- každá stránka má právě jeden nadpis `h1` a žádný zástupný text v hranatých závorkách,
- ceny ve strukturovaných datech jsou vidět na stránce,
- nezůstal žádný odkaz `#/`,
- každý český text má anglický překlad.

Náhled vyrobených stránek: `python3 -m http.server --directory web/public`, pak `http://localhost:8000`.

## Anglická verze

Adresy jsou stejné jako české, jen s `/en` na začátku: `/en/`, `/en/services/audit`, `/en/portfolio/coinmate` a tak dál. Přepínač CS/EN v hlavičce vede na stejnou stránku v druhém jazyce.

Texty jsou v `build/en.py` jako dvojice `cs:` a `en:`. Jsou psané podle zásad Nielsen Norman Group: krátké věty, činný rod, nejdůležitější informace na začátku, čísla jako číslice („2 days a week“), americký pravopis. Ceny jsou v korunách („From CZK 49,000“).

Když se změní český text, `pages.py` vypíše, který anglický překlad chybí. Stačí doplnit dvojici do `en.py`. Doporučení z LinkedInu jsou v originále anglicky a zůstávají beze změny.

## Stránky

| Česky | Anglicky | Sekce ve zdroji |
|---|---|---|
| `/` | `/en/` | `#/` |
| `/portfolio` | `/en/portfolio` | `#/portfolio` |
| `/portfolio/heirloom`, `/coinmate`, `/leeaf`, `/breno` | `/en/portfolio/…` | `#/work/…` |
| `/services` | `/en/services` | `#/services` |
| `/services/decision-prototype`, `/audit`, `/fractional` | `/en/services/…` | `#/services/…` |
| `/about` | `/en/about` | `#/about` |
| `/contact` | `/en/contact` | `#/contact`, služba se předvyplní přes `?service=audit` |

`/contact`, `/about`, `/portfolio`, `/portfolio/coinmate` a `/portfolio/leeaf` jsou stejné adresy jako na předchozím webu na Frameru, takže odkazy z Googlu fungují dál. Staré odkazy s `#/` skript přesměruje na novou stránku.

## SEO a AI

Hlavní adresa je `https://www.pavelkroupa.com`.

- Titulky, popisy, klíčová slova a obrázky pro sdílení české verze: `PAGES` a `KEYWORDS` ve `build/v5_round16.py`. `pages.py` je čte odtud, takže web v jednom souboru i samostatné stránky mají stejné.
- Anglická metadata: `META` a `KEYWORDS` v `build/en.py`.
- Strukturovaná data (JSON-LD) vyrábí `pages.py` pro každou stránku: osoba, firma s IČO, služby s cenami, drobečková navigace a otázky a odpovědi tak, jak jsou na stránce.
- Každá stránka odkazuje na svou druhou jazykovou verzi (`hreflang`). Pro ostatní jazyky (`x-default`) vede na anglickou.
- `public/robots.txt`: povoluje vyhledávače i AI crawlery.
- `public/llms.txt`: shrnutí webu pro AI asistenty, česky a na konci anglicky. Při změně služeb, cen nebo případů ho upravte ručně.
- `public/_headers`: `*.pages.dev` se neindexuje, soubory v `assets/` se cachují napořád (v názvu mají otisk obsahu).

## Nasazení (Cloudflare Pages)

- Production branch: `main`
- Framework preset: None
- Build command: prázdné (nebo `exit 0`)
- Root directory: `web`
- Build output directory: `public`

## Build ve vaultu

Build běží z Obsidianu. Cesty se počítají od složky `build/`.

```bash
cd build
pip3 install -r requirements.txt
python3 build_v5b.py      # index.html + kopie v ../verze/site-v5.html
python3 og.py             # obrázky pro sdílení
python3 export_pk.py      # logo pk
python3 export_logo.py    # post-it a favicona
```

- `build_v5b.py` vezme `src/site-v4.html` a texty z `src/v5src/` a postupně spustí `v5_round2.py` až `v5_round18.py`. Každé kolo je jedna sada úprav.
- Loga klientů čte z `Career/07 Assets/loga klientů/`. Ta složka v repu není, build proto funguje jen uvnitř vaultu.
- Písma jsou v `build/fonts/` (Inter a Shantell Sans, licence SIL OFL 1.1, texty licencí jsou vedle).
- `qa.py` vyrobí náhledovou stránku s webem v několika šířkách. Ukládá do `build/_draft/`, a ta složka se do gitu nenahrává.

## Co zatím nefunguje

- Kontaktní formulář nic neodesílá, jen ukáže potvrzení. Je potřeba napojit službu pro formuláře.
- Případ Heirloom zatím nemá citaci. Doplní se do zdroje za odstavec „Jak to dopadlo“, ve stejném tvaru jako `case-ref` u ostatních případů.
