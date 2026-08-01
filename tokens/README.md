# Tokens

Single source of truth for every visual value in the system. Nothing downstream
hard-codes a colour, size, or duration — components and pages read these only.

## ⚠️ Current values are PLACEHOLDERS

**These are not yet Pavel's brand values.** The live site could not be reached
from the build environment (see the Status section in the root `README.md`), so
this set is a neutral, deliberately unopinionated scaffold: greyscale-forward,
one indigo accent, a 4px spacing rhythm, a conventional type ramp.

It exists so the *pipeline*, *component API*, and *page structure* could be
built and reviewed while the real values were still unavailable. Treat every
number here as "shape is right, value is pending."

## Swapping in the real values

This is the payoff of the token layer — a re-skin is a data edit, not a refactor:

1. Edit the JSON in `src/`. Only the `value` fields change; the key names stay.
2. Run `npm run tokens` from the repo root.
3. Every consumer — the style guide, all components, the whole site — updates.

No component file needs touching to re-skin the system. If a real brand value
turns out to need a token that doesn't exist yet (a second accent, a gradient,
a display face), add it to `src/` rather than inlining it at the call site.

## Layout

| File | Holds |
|---|---|
| `src/color.json` | Palette ramps + semantic aliases |
| `src/typography.json` | Families, weights, size ramp, line heights, tracking |
| `src/space.json` | Spacing scale, container widths, gutters |
| `src/radius.json` | Corner radii |
| `src/shadow.json` | Elevation, motion durations/easings, z-index |
| `src/breakpoint.json` | Responsive breakpoints |

## Two-tier colour

Ramps (`color.neutral.700`) are raw material. Semantic aliases
(`color.text.secondary`, `color.action.primary`) are what components consume.

Components should reference **semantic** tokens almost always. That way a brand
change edits the alias layer once instead of every component that happened to
pick `neutral.700` by eye.

## Generated output

`dist/` is generated — never edit it, and it is not committed.

| Artifact | Purpose |
|---|---|
| `dist/variables.css` | `:root` custom properties, with references preserved |
| `dist/theme.css` | Tailwind v4 `@theme` block — utilities derive from tokens |
| `dist/tokens.js` | ES module export, for JS that needs a raw value |
| `dist/tokens.json` | Flat map, for tooling and the style guide |

### Why a Tailwind `@theme` block

Tailwind v4 is configured in CSS rather than JS. Emitting `@theme` directly from
style-dictionary means Tailwind's utilities *are* the tokens — `bg-bg-subtle` and
`text-text-secondary` exist because those tokens exist. There is no second scale
in a `tailwind.config.js` to drift out of sync, which is the usual way design
systems quietly rot.
