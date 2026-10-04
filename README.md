# business

Design system and site rebuild for [pavelkroupa.com](https://www.pavelkroupa.com).

**The live site is `web/`** (version 5, Czech and English static pages generated
from one source file, deployed with Cloudflare Pages, see `web/README.md`). Everything else in this repo is the
earlier Next.js rebuild and is not what the domain serves.

```
web/          Live site v5 (source in web/src, pages in web/public)
tokens/       JSON token sources + style-dictionary build
components/   React components, built strictly on tokens
docs/         Generated token reference
site/         Next.js 15 + Tailwind v4 rebuild
```

## Status — read this first

**Phase 1 (scrape) did not happen.** The live site could not be reached from the
build environment, by any available route:

| Route | Result |
|---|---|
| Playwright / curl / Firecrawl in-container | Egress proxy rejects the host at CONNECT with `403` (policy denial) |
| `WebFetch` (runs outside the container) | `403` for **every** host, including `example.com` — blocked session-wide |
| `WebSearch` | Works, but returns only titles and snippets |

Because of that, three things are **not** what the original brief asked for, and
should be treated as pending rather than done:

1. **Token values are placeholders.** A neutral scaffold — greyscale plus one
   indigo accent, a 4px rhythm, a conventional type ramp. Not the brand values.
2. **Component appearance is provisional.** Structure, API and behaviour are
   real; proportions, weight and density are defaults, not observed values.
3. **Copy is not preserved.** Phase 3 asked for the existing copy to be kept
   exactly. It could not be read. Every string in `site/content/site.ts` is
   tagged `[SEARCH]` (recovered from public search metadata — real but
   second-hand, verify it) or `[PLACEHOLDER]` (written to fill the layout, not
   Pavel's words). Nothing is a paraphrase passed off as original copy.

What *is* real and reviewable: the token pipeline, the component architecture
and its accessibility behaviour, the page structure and routing, the style
guide, and the build.

### Finishing the job

Two ways to unblock, either is enough:

- **Screenshots.** Five pages at desktop and mobile width, plus a paste of the
  computed styles from devtools. Enough to derive the real values.
- **Open the network policy** for `pavelkroupa.com`, `www.pavelkroupa.com` and
  `framerusercontent.com` (Framer serves images and fonts from the last one),
  then start a fresh session so Playwright can crawl properly.

Then the re-skin is a data edit — rewrite the `value` fields in `tokens/src`,
run `npm run tokens`, and every component, page and doc updates. No component
file changes to re-skin.

## Getting started

```bash
npm install
npm --prefix site install

npm run tokens   # build token artifacts into tokens/dist
npm run docs     # + generate docs/dist/index.html
npm run dev      # + run the site at localhost:3000
npm run build    # + production build
```

`tokens/dist` and `docs/dist` are generated and not committed — run `npm run
tokens` after cloning.

## Preview

`preview.html` is a self-contained snapshot — the home page, the component
gallery and all 116 tokens in one file, with the CSS inlined. Open it directly
in a browser; it needs no server and no network.

It is generated output, captured from a production build of `site/`. Treat the
running app as the source of truth and regenerate the snapshot after visual
changes rather than editing it by hand.

One thing worth knowing if you regenerate it: Tailwind v4 strips unused theme
variables from its CSS bundle, so the bundle alone does not define every token.
The snapshot therefore emits a complete `:root` block from `tokens.docs.json`
first — without it, swatches for unused tokens silently render transparent.

## How the layers fit

Tokens are the only source of visual values. Components consume the **semantic**
aliases (`text-text-secondary`), never the raw ramps (`text-neutral-600`), so a
brand change edits the alias layer once instead of every call site. Pages
compose components and hold no styling of their own beyond layout.

Tailwind v4 is configured in CSS, and the generated `@theme` block *is* that
configuration — utilities exist because tokens exist. There is no parallel scale
in a JS config to drift out of sync.

### One trap worth knowing about

Token names are emitted into Tailwind's namespaces, so a token whose last
segment is a Tailwind keyword silently redefines a core utility. `container.full`
did exactly this: it emitted `--container-full`, which redefined `w-full` from
`100%` to `88rem` and broke full-width layout across the whole site. It is now
named `container.bleed`, and `tokens/build.mjs` fails the build on that class of
collision rather than letting it through as a mystery layout bug.

## Verification

The build is clean and all 10 routes prerender. Rendering was checked in
Chromium at 1280px and 390px: tokens resolve to their intended computed values,
the container caps at its token width, the nav collapses and its disclosure
menu toggles with correct `aria-expanded`, and no console or page errors.
