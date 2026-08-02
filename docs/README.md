# Docs

Two surfaces, split by what each can prove.

## Token reference — `docs/dist/index.html`

```bash
npm run docs      # builds tokens, then the page
open docs/dist/index.html
```

Static, dependency-free, opens straight from disk. Every swatch, type row,
spacing bar and shadow chip is generated from `tokens/dist/tokens.docs.json`,
so the page cannot drift from the token set — add a token to `tokens/src` and it
appears here with no edit to `build-docs.mjs`.

Each row shows the CSS custom property, the resolved value, and the Tailwind
variable it maps to where the two differ (`--font-size-4xl` → `--text-4xl`).

## Component gallery — `/styleguide` in the site

```bash
npm run dev       # then open /styleguide
```

Component previews deliberately live in the Next app rather than here, because
there they import the real components. Reimplementing component markup in this
generator would create a second copy free to drift from the first — the exact
failure a design system exists to prevent.

The split is the point: the token page proves the *values*, the gallery proves
the *components*, and neither restates the other.
