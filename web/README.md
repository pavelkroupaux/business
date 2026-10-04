# pavelkroupa.com, verze 5

Statický web. Zdroj je pořád jeden soubor, ze kterého se vyrobí samostatné stránky.

```
src/index.html      celý web v jednom souboru (sekce za #/), tady se upravuje obsah
build/pages.py      z něj vyrobí stránky do public/
public/             to, co Cloudflare publikuje
build/v5_*.py       skripty, kterými web vznikal (záznam změn)
```

## Úprava webu
1. Upravte `src/index.html`. Otevřený v prohlížeči slouží jako náhled celého webu.
2. Z kořene repozitáře spusťte `python3 web/build/pages.py`. Skript vyrobí stránky, vytáhne obrázky do `public/assets/img` a obnoví `public/sitemap.xml`.
3. Commitněte `src/` i `public/` a pushněte do `main`. Cloudflare web nasadí sám.

Skript hlídá, aby se nic nerozjelo: každá stránka má jeden nadpis `h1`, ceny a otázky ve strukturovaných datech musí být vidět na stránce a nesmí zůstat žádný odkaz `#/`. Když něco nesedí, skončí chybou a nic nevyrobí.

Náhled vyrobených stránek: `python3 -m http.server --directory web/public`, pak `http://localhost:8000`. Soubory v `public/` se otevřením přímo z disku nezobrazí správně, protože odkazují na `/assets/`.

## Stránky
| Adresa | Sekce ve zdroji |
|---|---|
| `/` | `#/` |
| `/portfolio` | `#/portfolio` |
| `/portfolio/heirloom`, `/coinmate`, `/leeaf`, `/breno` | `#/work/…` |
| `/services` | `#/services` |
| `/services/decision-prototype`, `/audit`, `/fractional` | `#/services/…` |
| `/about` | `#/about` |
| `/contact` | `#/contact`, služba se předvyplní přes `/contact?service=audit` |

`/contact`, `/about`, `/portfolio`, `/portfolio/coinmate` a `/portfolio/leeaf` jsou stejné adresy jako na předchozím webu, takže odkazy z Googlu a odjinud fungují dál. Staré odkazy s `#/` skript přesměruje na novou stránku.

Nová stránka: přidejte sekci `<div id="v-…">` do zdroje a záznam do `PAGES` v `build/pages.py` (adresa, titulek, popis do 160 znaků).

## Nasazení (Cloudflare Pages)
- Production branch: `main`
- Framework preset: None
- Build command: prázdné (nebo `exit 0`)
- Root directory: `web`
- Build output directory: `public`

## SEO a AI
Hlavní adresa je `https://www.pavelkroupa.com`. Na ni míří canonical, `og:url`, sitemap i strukturovaná data.

- Titulky, popisy a JSON-LD každé stránky jsou v `build/pages.py`. Když se na webu změní cena nebo otázka, změňte ji i tam. Skript nesoulad zachytí.
- `public/robots.txt`: povoluje vyhledávače i AI crawlery.
- `public/llms.txt`: shrnutí webu pro AI asistenty. Při změně služeb, cen nebo případů ho upravte ručně.
- `public/_headers`: `*.pages.dev` se neindexuje, soubory v `assets/` se cachují napořád (v názvu mají otisk obsahu).
- `public/404.html`, `og.jpg` (obrázek pro sdílení), `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `site.webmanifest`: ruční soubory, skript je nemění.

## Co zatím nefunguje
- Kontaktní formulář nic neodesílá (jen ukáže potvrzení). Je potřeba napojit službu pro formuláře.
- Anglická verze zatím není.
- Případ Heirloom zatím nemá citaci. Doplní se do `src/index.html` za odstavec „Jak to dopadlo“, ve stejném tvaru jako `case-ref` u ostatních případů.
