# pavelkroupa.com

Web Pavla Kroupy. Statické stránky v češtině a angličtině.

Web publikuje GitHub Pages z větve `main` a složky `/ (root)` na vlastní doméně `pavelkroupa.com` (soubor `CNAME`). Cloudflare spravuje jen DNS: záznamy A vedou na GitHub Pages, `www` je CNAME na `pavelkroupaux.github.io` a všechny jsou bez proxy (šedý obláček). GitHub přesměruje `www.pavelkroupa.com` na `pavelkroupa.com`.

| Cesta | Co to je |
|---|---|
| `index.html`, `about/`, `contact/`, `portfolio/`, `services/`, `en/`, `ds/`, `404.html` | stránky, vyrábí je `web/build/pages.py` |
| `assets/`, `sitemap.xml` | styl, skripty, písmo, obrázky a mapa webu, také z `pages.py` |
| `logo/`, `og/`, favikony, `robots.txt`, `llms.txt`, `site.webmanifest` | ruční soubory webu |
| `CNAME` | doména pro GitHub Pages |
| `_config.yml` | co GitHub Pages nepublikuje: složku `web/` a tento README |
| `web/` | zdroj a build, návod je ve [`web/README.md`](web/README.md) |

Design systém (barvy, písmo, loga, komponenty) je na adrese `/ds/`. Nevede na něj žádný odkaz a vyhledávače ho nemají indexovat.

`web/public/` je stará kopie webu z doby, kdy se počítalo s Cloudflare Pages. Nic ji nepoužívá ani nepublikuje, dá se smazat.
