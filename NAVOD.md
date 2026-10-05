# Jak pracovat na webu pavelkroupa.com

Web je sada obyčejných HTML souborů. Nic se nestaví, nic se neinstaluje. Upravíš soubor, uložíš ho do větve `main` a GitHub Pages ho do minuty publikuje.

Nejjednodušší je dát úpravu Claudovi: „V repozitáři pavelkroupaux/business změň na stránce Služby cenu auditu na 35 000 Kč, česky i anglicky, a podle NAVOD.md zkontroluj, co s tím souvisí.“

## Kde co je

| Cesta | Co to je |
|---|---|
| `index.html` | úvod |
| `portfolio/index.html`, `portfolio/coinmate/index.html` … | portfolio a případy (heirloom, coinmate, leeaf, breno) |
| `services/index.html`, `services/audit/index.html` … | služby (decision-prototype, audit, fractional) |
| `about/index.html`, `contact/index.html` | O mně, Kontakt |
| `en/…` | anglická verze, stejné složky |
| `404.html`, `en/404.html` | stránka „nenalezeno“ |
| `ds/index.html` | design systém (barvy, písmo, komponenty), není veřejně odkazovaný |
| `assets/site.css` | celý vzhled webu. Barvy a písmo jsou proměnné na začátku (`:root`) |
| `assets/site-cs.js`, `assets/site-en.js` | chování (přepínač režimu, animace, kreslení v úvodu, formulář). Liší se jen texty |
| `assets/img/`, `assets/fonts/` | obrázky a písmo |
| `og/` | obrázky pro sdílení na sítích (1200 × 630 px), anglické v `og/en/` |
| `logo/`, `favicon.*`, `icon-*.png`, `apple-touch-icon.png` | loga a ikony |
| `robots.txt`, `sitemap.xml`, `llms.txt` | pro vyhledávače a AI asistenty |
| `CNAME`, `_config.yml` | doména a nastavení GitHub Pages, neměnit |

Adresy odpovídají složkám: `services/audit/index.html` je `pavelkroupa.com/services/audit/`.

## Na co nezapomenout při změně

Každá stránka je samostatný soubor, takže co je na víc místech, je potřeba změnit na všech.

- **Text na stránce** změň v české i anglické verzi (`…/index.html` a `en/…/index.html`).
- **Hlavička a patička** jsou v každé stránce zvlášť (27 souborů). Změna menu nebo patičky = najít a nahradit ve všech.
- **Titulek a popis pro Google** jsou v hlavě stránky: `<title>`, `<meta name="description">` a stejný text v `og:title`, `og:description`, `twitter:…`. Popis do 160 znaků.
- **Ceny** jsou i ve strukturovaných datech pro Google (`<script type="application/ld+json">` v hlavě stránky) a v `llms.txt`. Když se mění cena, změň ji i tam.
- **Nová stránka**: zkopíruj podobnou složku, uprav obsah, `<title>`, popis, `<link rel="canonical">` a odkazy na jazykové verze (`hreflang`), a přidej adresu do `sitemap.xml`. V menu ji přidej do všech stránek.
- **Odkazy uvnitř webu** piš s lomítkem na konci: `/services/audit/`.
- **Obrázky** dávej do `assets/img/`, ideálně ve formátu WebP, s popisem v `alt`.
- **Vzhled**: barvy jen z proměnných v `assets/site.css` (`--ink`, `--fix` a další, přehled je na `/ds/`). Vyzkoušet ve světlém i tmavém režimu a na mobilu (320 px).
- Prohlížeč si styl a skripty pamatuje asi 10 minut. Když změna není hned vidět, obnov stránku s Shift.

## Kontakt

Web nemá formulář. Stránka Kontakt (`contact/index.html`, `en/contact/index.html`) nabízí dvě cesty: napsat e-mail a vybrat termín hovoru na `cal.com/pavelkroupa`. Tlačítko „Napsat e-mail“ (`#mail-go`) dostane ve skriptu (`site-cs.js` / `site-en.js`, hledej `mail-go`) předmět a začátek zprávy, bez skriptu je to prostý odkaz.

Nad oběma kartami je malý notebook (`figure.cx` v HTML stránky, styl v `assets/site.css` pod „kontakt: notebooky“, skript hledej `.cx`): u e-mailu se rozbalí zpráva a kurzor klikne na Odeslat, u hovoru se vybere datum a potvrdí. Kalendář se poprvé pustí až po dohrání e-mailu. Přehraje se, když je vidět, a znovu po najetí myší na kartu nebo klepnutí. Při omezeném pohybu se ukáže rovnou konečný stav. Texty v obrázku jsou přímo v HTML, anglické v `en/contact/index.html`.

Telefon na webu není. Kdyby se přidával, nevypisuj ho do HTML, ať ho nenajdou sběrače: skriptem ho slož až po kliknutí na tlačítko „Zobrazit telefon“. To chrání před běžnými roboty, ne před robotem, který umí kliknout.

## Kreslení v úvodu

Na počítači s myší jde po úvodní sekci kreslit. Kód je na konci `assets/site-cs.js` / `site-en.js` (blok „Kreslení fixou…“), vzhled v `assets/site.css` (`.hx-pen`).

## Náhled před uložením

V kořeni repozitáře `python3 -m http.server` a otevřít `http://localhost:8000`. Nebo soubor rovnou uložit do `main` a za minutu se podívat na web.

## Hosting

- GitHub Pages: Settings → Pages → Deploy from a branch, `main`, `/ (root)`, vlastní doména `pavelkroupa.com`, Enforce HTTPS.
- Cloudflare: jen DNS (záznamy A na GitHub Pages, `www` jako CNAME na `pavelkroupaux.github.io`, šedý obláček).
- Průběh nasazení je na GitHubu v záložce Actions („pages build and deployment“).

## Historie

Web vznikl v Claude Chat jako jeden HTML soubor a skript v Pythonu ho rozdělil na stránky. Od 5. 10. 2026 se stránky upravují přímo a Python už není potřeba. Původní build je v historii gitu (složka `web/`), kdyby bylo potřeba se k němu vrátit.
