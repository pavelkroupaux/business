# Components

React components built strictly on `/tokens`. No component hard-codes a hex
value, pixel size, radius or duration — every visual value arrives as a
token-derived Tailwind utility.

That constraint is what makes a re-skin a token edit. If you ever need a value
that isn't in `/tokens`, add it there rather than inlining it here.

## Inventory

| Component | Role | Notes |
|---|---|---|
| `Container` | Measure + responsive gutters | The only place page width is decided |
| `Section` | Full-bleed band + contained column | Owns vertical rhythm |
| `SectionHeader` | Titles a band | Eyebrow / title / description / action |
| `Nav` | Sticky primary nav | Collapses to a disclosure below `md` |
| `Hero` | Page opening statement | Steps across the type ramp |
| `Button` | Every interactive affordance | 4 variants × 3 sizes |
| `Card` | Project / content card | Optional stretched link |
| `Tag` | Metadata chip | Non-interactive |
| `Prose` | Long-form body copy | Styles raw HTML by element |
| `Footer` | Contact + secondary nav | |

## Conventions

**Semantic tokens, not ramp values.** Components use `text-text-secondary`, not
`text-neutral-600`. The alias layer is what a brand change edits.

**Variants are lookup tables.** Each variant map is a plain object at the top of
the file, so the full set of states is readable at a glance and adding one is a
single line.

**Links stay links.** `Button` renders an `<a>` when given `href`, so navigation
works without JS. `Card`'s stretched link puts only the title in the tab order,
giving keyboard users one stop with a meaningful accessible name rather than a
card-sized anonymous target.

**Server-first.** Only `Nav` is a client component, because only it holds state.

**Focus is never removed.** Every interactive element carries a
`focus-visible:outline-*` using the `focus.ring` token.

## Status

The component API and structure here are real and reviewable. What they are
*not* yet is a match for the live site's appearance — the site could not be
reached from the build environment, so proportions, weights and density are
reasonable defaults rather than observed values. See the root `README.md`.
