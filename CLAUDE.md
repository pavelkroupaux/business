# Pokyny pro AI nástroje

Web pavelkroupa.com, obyčejné HTML v češtině (`/`) a angličtině (`/en/`). Jak web funguje a co změnit spolu s textem: `NAVOD.md`.

## Texty

Než napíšeš nebo upravíš jakýkoli text na webu, přečti `_brand/prompt.md` a drž se ho. Podrobnosti a schválené vzory jsou ve složce `_brand/`.

Nejdůležitější:
- Přepsaný text nesmí mít víc znaků než původní. Rozložení webu je pevné.
- Žádné vzorce ze `_brand/zakazane-vzorce.md` (úderné protiklady, řady fragmentů, „Otherwise,“, dlouhé pomlčky, slova typická pro AI).
- Citace doporučení a `og:image:alt` neměň.
- Ke každé změně textu ukaž tabulku: před | po | znaky před → po.

Po každé změně anglického textu spusť a oprav, co najde:

```
python3 _tools/copy-lint.py --against HEAD
```
