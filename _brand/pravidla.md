---
tags: [brand, copywriting]
---
# Pravidla pro anglické texty

## Věty

1. Piš celé věty. Dvě krátké věty o jedné věci spoj spojkou: „The spec keeps changing, so engineering waits.“
2. Jedna myšlenka na větu. Věta do zhruba 20 slov.
3. Konkrétní podstatná jména místo abstraktních: „a clickable prototype“, ne „a solution“.
4. Činný rod: „People confused the names“, ne „The names got confused“.
5. Každé tvrzení podlož číslem, jménem nebo případovou studií. Když to nejde, tvrzení vyhoď.
6. Úvodní slovo se nesmí opakovat ve dvou větách po sobě a stejná stavba věty ne víc než dvakrát na stránce.

## Délka (tvrdé pravidlo)

Web má pevné rozložení. Delší text ho rozbije.

- Přepsaný text má **stejný nebo menší počet znaků** než původní. Nikdy větší.
- U nadpisů zachovej místo zalomení (`<br>`) a slova v `<span class="fix">`.
- U rotujících slov (`data-words="…"`) nesmí být žádná varianta delší než nejdelší původní.
- Když text nejde zkrátit bez ztráty smyslu, nech ho být a napiš proč.
- Kontrola: `python3 _tools/copy-lint.py --against HEAD`.

## Forma

- **Pravopis:** americký (prioritization, organize, color, center).
- **Čísla:** číslicemi („4 sessions“, „2 days“, „6 months“). Výjimka: začátek věty a ustálené „Thirty minutes“ na stránce Kontakt.
- **Ceny:** „From CZK 49,000“, „From CZK 120,000 per month“. Čárka jako oddělovač tisíců.
- **Výčty:** s čárkou před and/or („Prague, Amsterdam, or online“).
- **Nadpisy na stránce:** jako věta (velké jen první písmeno), s tečkou na konci, jak je zvykem na webu.
- **Titulek stránky (`<title>`):** Title Case („Backlog Prioritization in 2 Days“).
- **Pomlčky:** žádné dlouhé pomlčky (—) ani pomlčky místo čárky ( – ). Použij čárku, dvojtečku nebo novou větu.
- **Uvozovky:** typografické „“ jen v citacích doporučení.

## Co se nemění

- Citace doporučení z LinkedInu. Jsou to slova jiných lidí, nechávají se doslova včetně chyb.
- `og:image:alt`. Musí odpovídat textu, který je přímo v obrázku pro sdílení.
- Jména firem a lidí.

## Co změnit spolu s textem

Když se mění text, který je i v `<meta name="description">`, změň ho stejně v `og:description`, `twitter:description` a ve strukturovaných datech (`application/ld+json`). Popis do 160 znaků. Podrobnosti v `NAVOD.md`.
