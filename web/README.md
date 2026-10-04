# pavelkroupa.com, verze 5

Statický web v jednom souboru. `public/index.html` obsahuje všechno: styly, skripty, fotky a loga (vložené přímo do souboru).

## Spuštění
Otevřete `public/index.html` v prohlížeči. Žádný build není potřeba.

## Nasazení (Cloudflare Pages)
Cloudflare publikuje jen složku `public/`, takže README a skripty ve `build/` na webu vidět nejsou.

Nastavení projektu v Cloudflare Pages:
- Production branch: `main`
- Framework preset: None
- Build command: prázdné (nebo `exit 0`)
- Root directory: `web`
- Build output directory: `public`

Každý push do `main` web automaticky znovu nasadí.

## SEO a AI
Hlavní adresa je `https://www.pavelkroupa.com/`. Na ni míří canonical, `og:url`, sitemap i strukturovaná data.

- `index.html`, hlavička: titulek, popis, canonical, Open Graph, ikony a JSON-LD (osoba, firma, tři služby s cenami, otázky a odpovědi). Ceny a texty v JSON-LD musí odpovídat textu na webu. Když se změní na webu, změňte je i tady.
- `robots.txt`: povoluje vyhledávače i AI crawlery.
- `sitemap.xml`: jedna adresa, protože sekce jsou za `#/` a vyhledávače je jako samostatné stránky neberou.
- `llms.txt`: shrnutí webu pro AI asistenty. Při změně služeb, cen nebo případů ho upravte taky.
- `_redirects`: staré adresy z předchozího webu (`/contact`, `/portfolio/coinmate` a další) vedou na nové sekce.
- `_headers`: náhledová adresa `*.pages.dev` se neindexuje.
- `404.html`: stránka pro neexistující adresy.
- `og.jpg`: obrázek pro sdílení (1200 × 630).
- `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `site.webmanifest`: ikony.
- `pavel-kroupa.jpg`: portrét pro strukturovaná data.

## Co zatím nefunguje
- Kontaktní formulář nic neodesílá (jen ukáže potvrzení). Je potřeba napojit službu pro formuláře.
- Anglická verze zatím není.

## Složka build
Skripty, kterými se web generoval (z verze 4 a kol úprav). Cesty uvnitř vedou na pracovní prostředí, ve kterém vznikly, takže slouží hlavně jako záznam změn.
