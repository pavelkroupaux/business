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

## Co zatím nefunguje
- Kontaktní formulář nic neodesílá (jen ukáže potvrzení). Je potřeba napojit službu pro formuláře.
- Anglická verze zatím není.

## Složka build
Skripty, kterými se web generoval (z verze 4 a kol úprav). Cesty uvnitř vedou na pracovní prostředí, ve kterém vznikly, takže slouží hlavně jako záznam změn.
