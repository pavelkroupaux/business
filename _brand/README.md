---
tags: [brand, copywriting]
---
# Copywriting: Pavel Kroupa

Zásady pro všechny texty webu pavelkroupa.com a pro AI nástroje, které je píšou nebo upravují. Cíl je, aby nové texty zněly stejně jako ty schválené a nesklouzávaly do „AI stylu“.

## Soubory

| Soubor | K čemu |
|---|---|
| [hlas.md](hlas.md) | Kdo jsem, pro koho píšu, jak to má znít |
| [pravidla.md](pravidla.md) | Pravidla pro anglické texty: věty, forma, délka |
| [zakazane-vzorce.md](zakazane-vzorce.md) | Vzorce, podle kterých se pozná AI, a kalky z češtiny |
| [slovnik.md](slovnik.md) | Pojmy, které používám, a čím je nenahrazovat |
| [priklady.md](priklady.md) | Schválené přepisy před → po |
| [prompt.md](prompt.md) | Hotový prompt v angličtině pro ChatGPT, Claude a další |

## Jak to používat

S AI v chatu: vlož celý [prompt.md](prompt.md) na začátek konverzace, nebo ho dej do vlastních instrukcí projektu. Potom napiš, co potřebuješ.

V repozitáři: Claude Code si pravidla načte sám přes `CLAUDE.md`. Po každé změně anglického textu spusť kontrolu:

```
python3 _tools/copy-lint.py --against HEAD
```

Vypíše zakázané vzorce a texty, které jsou delší než předtím.

V Obsidianu: zkopíruj složku `_brand` do vaultu. Odkazy mezi soubory fungují i tam.

## Když se pravidla mění

Uprav je tady v repozitáři a zkopíruj znovu do Obsidianu, ne naopak. Jedna verze pravdy je v GitHubu. Když rodilý mluvčí něco opraví, přidej to do [priklady.md](priklady.md) a případně do [zakazane-vzorce.md](zakazane-vzorce.md).
