# Jak pracovat na webu pavelkroupa.com

Web je sada obyčejných HTML souborů. Nic se nestaví, nic se neinstaluje. Upravíš soubor, uložíš ho do větve `main` a GitHub Pages ho do minuty publikuje.

Nejjednodušší je dát úpravu Claudovi: „V repozitáři pavelkroupaux/business změň na stránce Služby cenu auditu na 35 000 Kč, česky i anglicky, a podle NAVOD.md zkontroluj, co s tím souvisí.“

## Kde co je

| Cesta | Co to je |
|---|---|
| `index.html` | úvod |
| `portfolio/index.html`, `portfolio/coinmate/index.html` … | portfolio a případy (heirloom, coinmate, wpp, leeaf, breno) |
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
- **Hlavička a patička** jsou v každé stránce zvlášť (31 souborů). Změna menu nebo patičky = najít a nahradit ve všech.
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

Na počítači s myší jde po úvodní sekci kreslit. Kód je na konci `assets/site-cs.js` / `site-en.js` (blok „Kreslení fixou…“), vzhled v `assets/site.css` (`.hx-pen`). Fix kreslí červeně, barva je proměnná `--marker` v `assets/site.css`.

## Štítek u kurzoru

U tužky v úvodu a u lepíku v sekci s otázkami jde za myší malý červený štítek jako u spolupracovníka ve Figmě: „Nakresli“ a „Nalep“ (anglicky „Draw“ a „Stick it“). Nad odkazy se schová a po prvním tahu nebo nalepení zmizí. Jen myš na počítači. Skript na konci `site-cs.js` / `site-en.js` (hledej `mp-tag`), vzhled v `assets/site.css`.

## Lepítka s otázkami

V sekci „Kdy týmy potřebují moji pomoc“ je na počítači s myší kurzor malé lepítko a klik kamkoli nalepí větší lepítko s další otázkou (najednou jich je nejvýš šest). Otázky jsou ve skriptu (`site-cs.js` / `site-en.js`, blok „Lepítka s otázkami…“), vzhled v `assets/site.css` (`.pq`).

## Časová osa v případech

Každý případ (`portfolio/…/index.html`, `en/portfolio/…/index.html`) má pod nadpisem svislou časovou osu (`ol.tl`): červený bod je místo, kde se to zaseklo, prázdné body jsou kroky a žlutý bod je výsledek. Pod ní je tabulka „Ve zkratce“ (`dl.tl-facts`) s klientem, obdobím, oborem a rolí. Vzhled je v `assets/site.css` pod „případy: časová osa“. Pod tabulkou je výzva k hovoru (`.case-cta`). Dole jsou vždy dva další případy v pořadí Heirloom, Coinmate, WPP, Leeaf, BRENO.

## Diagram „Jak to proběhlo“ v případech

Heirloom, Coinmate, Leeaf a BRENO mají nad časovou osou diagram (`section.case-dg`), který se po zobrazení postupně nakreslí. Je dvakrát: široký pro počítač (`svg.dg-d`) a svislý pro mobil (`svg.dg-m`). Barvy jsou jen z proměnných webu, takže funguje ve světlém i tmavém režimu. Vzhled je v `assets/site.css` pod „případy: diagram“.

Diagramy se nepíšou ručně. Texty (česky i anglicky) a rozložení jsou v `_tools/case-diagrams.py`. Po změně spusť v kořeni `python3 _tools/case-diagrams.py`, skript diagramy ve všech osmi stránkách nahradí. Složky s podtržítkem GitHub Pages nepublikuje.

Heirloom má pod prvním diagramem ještě druhý, „Pipeline pro definici produktu“: facilitace, AI prototyp z repozitáře a design systému, hosting na Vercelu, komentáře v prototypu a zpětná vazba zpátky do další iterace. Texty jsou ve stejném skriptu (klíče `p_…`). Čtyři iterace v prvním diagramu se rozsvítí jedna po druhé v řadě nad kruhem, na mobilu vedle něj.

V tabulce „Ve zkratce“ je u každého případu poslední řádek „Služba“ nebo „Služby“ s odkazy na služby, které případu odpovídají.

## Infografika Vedení produktu na část úvazku

Dny v týdnu, rozsvítí se úterý a čtvrtek, pak čára od otazníku (vedení) ke kompasu, střelka se roztočí, kompas se rozsvítí žlutě, čára do vývoje a zaškrtnutí. Je na úvodu, na Službách a na stránce služby, česky i anglicky. Generuje ji `_tools/fractional-diagram.py`.

## Přepínač vzhledu

Jen světlý a tmavý. Dokud návštěvník neklikne, web se řídí nastavením systému. Po kliknutí se volba uloží (`pk-theme` v prohlížeči). Ikona je slunce nebo měsíc (`svg.tg` v tlačítku `#theme` ve všech stránkách): slunce vyjde zespodu a rozzáří paprsky, měsíc připluje zleva zdola, rozsvítí se a zablikají hvězdy. Styl v `assets/site.css` pod „přepínač vzhledu“, skript v `site-cs.js` / `site-en.js` (hledej `theme:`). Stejný přepínač je v portfoliu a v labu.

## Kouzlo před nadpisem a spinner

V úvodu u nadpisu „Pak z toho postavím funkční prototyp“ se nejdřív kolem rozsvítí drobné hořčicové jiskry a uprostřed na chvilku prokmitne „MAGIC“ s pruhem světla, pak se nadpis zaostří. Přehraje se jednou, když je nadpis vidět. Skript je na konci `site-cs.js` / `site-en.js` (hledej `mg-burst`), vzhled v `assets/site.css` pod „kouzlo před nadpisem“. S omezeným pohybem je nadpis vidět rovnou.

Spinner `.pk-spin` je zjednodušená úvodní kresba: zamotaná linka, rovná čára a lepík s fajfkou jako v logu. Vzor HTML je na `/ds/` v části Pohyb. Na webu zatím nic nenačítá, v portfoliu se ukáže při odemykání.

Tlačítko „Jak to probíhá podrobně“ po rozbalení i sbalení plynule sjede k prvnímu kroku (hledej `proc-toggle`).

## Patička

Uprostřed patičky je odkaz na lab.pavelkroupa.com s baňkou (`a.foot-lab`). Při najetí myší zčervená a baňka bublá, stejně jako odkaz Lab v hlavičce portfolia.

## Tlačítko Reference

Tlačítko Reference na úvodu vede na `/portfolio/#reference`. Skript (hledej `toRefs`) ukáže portfolio a pak plynule sjede na reference. Pod referencemi je odkaz na lab.pavelkroupa.com (`.lab-note`).

## Náhled před uložením

V kořeni repozitáře `python3 -m http.server` a otevřít `http://localhost:8000`. Nebo soubor rovnou uložit do `main` a za minutu se podívat na web.

## Měření návštěvnosti

Web měří Cloudflare Web Analytics, bez cookies, takže nepotřebuje cookie lištu. Skript je na konci každé stránky před `</html>` (hledej `cloudflareinsights`). Nová stránka ho potřebuje taky. Čísla jsou v Cloudflare → Web Analytics → pavelkroupa.com. Google Analytics byl odstraněn. Portfolio a lab mají vlastní tokeny ve svých repozitářích.

## Hosting

- GitHub Pages: Settings → Pages → Deploy from a branch, `main`, `/ (root)`, vlastní doména `pavelkroupa.com`, Enforce HTTPS.
- Cloudflare: jen DNS (záznamy A na GitHub Pages, `www` jako CNAME na `pavelkroupaux.github.io`, šedý obláček).
- Průběh nasazení je na GitHubu v záložce Actions („pages build and deployment“).

## Historie

Web vznikl v Claude Chat jako jeden HTML soubor a skript v Pythonu ho rozdělil na stránky. Od 5. 10. 2026 se stránky upravují přímo a Python už není potřeba. Původní build je v historii gitu (složka `web/`), kdyby bylo potřeba se k němu vrátit.
