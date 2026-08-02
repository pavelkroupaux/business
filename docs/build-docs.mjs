/**
 * Generates the token reference at docs/dist/index.html.
 *
 * Every swatch, ramp row and spacing bar is derived from tokens.docs.json, so
 * the page cannot fall out of step with the token set — adding a token to
 * tokens/src makes it appear here with no edit to this file.
 *
 * Component previews deliberately live in the Next app at /styleguide, where
 * they can import the real components. Reimplementing component markup here
 * would create a second copy free to drift from the first.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const tokens = JSON.parse(
  readFileSync(resolve(root, 'tokens/dist/tokens.docs.json'), 'utf8')
);
const variablesCss = readFileSync(
  resolve(root, 'tokens/dist/variables.css'),
  'utf8'
);

const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const byPath = (prefix) =>
  tokens.filter((t) => prefix.every((p, i) => t.path[i] === p));

/** Groups tokens by their second path segment (the ramp / sub-scale name). */
const subgroups = (prefix) => {
  const out = new Map();
  for (const t of byPath(prefix)) {
    const key = t.path[prefix.length] ?? '_';
    if (!out.has(key)) out.set(key, []);
    out.get(key).push(t);
  }
  return out;
};

const row = (t, preview) => `
  <div class="row">
    <div class="row-preview">${preview}</div>
    <div class="row-meta">
      <code class="row-name">${esc(t.cssVar)}</code>
      <span class="row-value">${esc(t.value)}</span>
      ${
        t.tailwindVar !== t.cssVar
          ? `<span class="row-tw">tailwind ${esc(t.tailwindVar)}</span>`
          : ''
      }
    </div>
  </div>`;

const section = (id, title, blurb, body) => `
  <section class="section" id="${id}">
    <h2>${esc(title)}</h2>
    ${blurb ? `<p class="blurb">${blurb}</p>` : ''}
    ${body}
  </section>`;

/* ---------------------------------------------------------------- colour */
const colorBlocks = [...subgroups(['color'])]
  .map(([name, list]) => {
    const swatches = list
      .map(
        (t) => `
      <figure class="swatch">
        <div class="chip" style="background: var(${t.cssVar})"></div>
        <figcaption>
          <code>${esc(t.path.slice(1).join('.'))}</code>
          <span>${esc(t.value)}</span>
        </figcaption>
      </figure>`
      )
      .join('');
    const semantic = !['neutral', 'accent'].includes(name);
    return `
    <h3>${esc(name)} ${
      semantic ? '<span class="badge">semantic</span>' : '<span class="badge badge-muted">ramp</span>'
    }</h3>
    <div class="swatches">${swatches}</div>`;
  })
  .join('');

/* ------------------------------------------------------------ typography */
const typeRamp = byPath(['font', 'size'])
  .map(
    (t) => `
  <div class="type-row">
    <div class="type-sample" style="font-size: var(${t.cssVar})">Ag</div>
    <div class="row-meta">
      <code class="row-name">${esc(t.cssVar)}</code>
      <span class="row-value">${esc(t.value)}</span>
      <span class="row-tw">tailwind ${esc(t.tailwindVar)}</span>
    </div>
  </div>`
  )
  .join('');

const families = byPath(['font', 'family'])
  .map(
    (t) => `
  <div class="type-row">
    <div class="type-sample-sm" style="font-family: var(${t.cssVar})">
      The quick brown fox jumps over the lazy dog
    </div>
    <div class="row-meta">
      <code class="row-name">${esc(t.cssVar)}</code>
      <span class="row-tw">tailwind ${esc(t.tailwindVar)}</span>
    </div>
  </div>`
  )
  .join('');

const weights = byPath(['font', 'weight'])
  .map((t) =>
    row(
      t,
      `<span style="font-weight: var(${t.cssVar}); font-size: 1.125rem">Aa</span>`
    )
  )
  .join('');

const lineHeights = byPath(['font', 'lineHeight'])
  .map(
    (t) => `
  <div class="row">
    <div class="row-preview lh" style="line-height: var(${t.cssVar})">
      Design leadership<br />and innovation
    </div>
    <div class="row-meta">
      <code class="row-name">${esc(t.cssVar)}</code>
      <span class="row-value">${esc(t.value)}</span>
      <span class="row-tw">tailwind ${esc(t.tailwindVar)}</span>
    </div>
  </div>`
  )
  .join('');

const tracking = byPath(['font', 'letterSpacing'])
  .map((t) =>
    row(
      t,
      `<span style="letter-spacing: var(${t.cssVar}); font-size: 1rem">Typography</span>`
    )
  )
  .join('');

/* --------------------------------------------------------------- spacing */
const spacing = byPath(['space'])
  .map(
    (t) => `
  <div class="row">
    <div class="row-preview">
      <div class="bar" style="width: var(${t.cssVar})"></div>
    </div>
    <div class="row-meta">
      <code class="row-name">${esc(t.cssVar)}</code>
      <span class="row-value">${esc(t.value)}</span>
      <span class="row-tw">tailwind ${esc(t.tailwindVar)}</span>
    </div>
  </div>`
  )
  .join('');

const containers = byPath(['size', 'container'])
  .map((t) => row(t, `<code>${esc(t.path.join('.'))}</code>`))
  .join('');

/* -------------------------------------------------- radius / shadow / etc */
const radii = byPath(['radius'])
  .map(
    (t) =>
      row(t, `<div class="radius-chip" style="border-radius: var(${t.cssVar})"></div>`)
  )
  .join('');

const shadows = byPath(['shadow'])
  .map(
    (t) =>
      row(t, `<div class="shadow-chip" style="box-shadow: var(${t.cssVar})"></div>`)
  )
  .join('');

const motion = byPath(['motion'])
  .map((t) => row(t, `<code>${esc(t.path.slice(1).join('.'))}</code>`))
  .join('');

const breakpoints = byPath(['breakpoint'])
  .map((t) => row(t, `<code>${esc(t.path.join('.'))}</code>`))
  .join('');

/* ------------------------------------------------------------------ page */
const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Token reference — pavelkroupa.com design system</title>
<style>
${variablesCss}

*, *::before, *::after { box-sizing: border-box; }
body {
  margin: 0;
  font-family: var(--font-family-sans);
  color: var(--color-text-primary);
  background: var(--color-bg-canvas);
  line-height: var(--font-line-height-normal);
}
.wrap { max-width: var(--size-container-wide); margin: 0 auto; padding: var(--space-8) var(--space-5) var(--space-12); }
header.page { border-bottom: 1px solid var(--color-border-subtle); padding-bottom: var(--space-7); margin-bottom: var(--space-8); }
h1 { font-size: var(--font-size-3xl); letter-spacing: var(--font-letter-spacing-tighter); margin: 0 0 var(--space-3); }
h2 { font-size: var(--font-size-2xl); letter-spacing: var(--font-letter-spacing-tight); margin: 0 0 var(--space-3); }
h3 { font-size: var(--font-size-base); text-transform: uppercase; letter-spacing: var(--font-letter-spacing-wider);
     color: var(--color-text-muted); margin: var(--space-7) 0 var(--space-4); font-weight: var(--font-weight-medium); }
.lede { color: var(--color-text-secondary); font-size: var(--font-size-lg); max-width: 60ch; margin: 0; }
.notice { margin-top: var(--space-6); padding: var(--space-5); border-radius: var(--radius-lg);
          background: var(--color-accent-50); color: var(--color-accent-900); max-width: 72ch; font-size: var(--font-size-sm); }
.notice strong { display: block; margin-bottom: var(--space-2); }
nav.toc { display: flex; flex-wrap: wrap; gap: var(--space-3); margin-top: var(--space-6); }
nav.toc a { font-size: var(--font-size-sm); color: var(--color-text-secondary); text-decoration: none;
            border: 1px solid var(--color-border-default); border-radius: var(--radius-pill); padding: var(--space-2) var(--space-4); }
nav.toc a:hover { color: var(--color-text-primary); border-color: var(--color-border-strong); }
.section { padding: var(--space-8) 0; border-top: 1px solid var(--color-border-subtle); }
.blurb { color: var(--color-text-secondary); max-width: 68ch; margin: 0 0 var(--space-5); }
.badge { font-size: var(--font-size-xs); background: var(--color-accent-100); color: var(--color-accent-800);
         border-radius: var(--radius-pill); padding: 2px var(--space-2); text-transform: none; letter-spacing: 0; }
.badge-muted { background: var(--color-neutral-100); color: var(--color-text-secondary); }
.swatches { display: grid; grid-template-columns: repeat(auto-fill, minmax(148px, 1fr)); gap: var(--space-4); }
.swatch { margin: 0; }
.chip { height: 68px; border-radius: var(--radius-md); border: 1px solid var(--color-border-subtle); }
.swatch figcaption { display: flex; flex-direction: column; gap: 2px; margin-top: var(--space-2); }
.swatch code { font-size: var(--font-size-xs); font-family: var(--font-family-mono); }
.swatch span { font-size: var(--font-size-xs); color: var(--color-text-muted); font-family: var(--font-family-mono); }
.row, .type-row { display: flex; align-items: center; gap: var(--space-5); padding: var(--space-3) 0;
                  border-bottom: 1px solid var(--color-border-subtle); }
.row-preview { flex: 0 0 220px; display: flex; align-items: center; }
.type-sample { flex: 0 0 220px; line-height: 1; letter-spacing: var(--font-letter-spacing-tight); }
.type-sample-sm { flex: 0 0 420px; font-size: var(--font-size-lg); }
.row-meta { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--space-3); }
.row-name { font-family: var(--font-family-mono); font-size: var(--font-size-sm); }
.row-value { font-family: var(--font-family-mono); font-size: var(--font-size-sm); color: var(--color-text-muted); }
.row-tw { font-family: var(--font-family-mono); font-size: var(--font-size-xs); color: var(--color-text-accent); }
.bar { height: 18px; background: var(--color-accent-400); border-radius: var(--radius-sm); min-width: 1px; }
.radius-chip { width: 68px; height: 68px; background: var(--color-neutral-100); border: 1px solid var(--color-border-default); }
.shadow-chip { width: 96px; height: 56px; background: var(--color-bg-canvas); border-radius: var(--radius-md); margin: var(--space-3); }
.lh { font-size: var(--font-size-sm); }
code { font-family: var(--font-family-mono); }
@media (max-width: 700px) {
  .row, .type-row { flex-direction: column; align-items: flex-start; gap: var(--space-2); }
  .row-preview, .type-sample, .type-sample-sm { flex: none; }
}
</style>
</head>
<body>
<div class="wrap">
  <header class="page">
    <h1>Token reference</h1>
    <p class="lede">
      Every visual value in the system, generated directly from
      <code>tokens/src</code>. ${tokens.length} tokens.
    </p>
    <div class="notice">
      <strong>These values are placeholders.</strong>
      The live site could not be reached from the build environment, so this set
      is a neutral scaffold — the structure is real, the specific values are
      pending. Swapping in the brand values is an edit to <code>tokens/src</code>
      plus <code>npm run tokens</code>; nothing downstream changes.
    </div>
    <nav class="toc">
      <a href="#color">Colour</a>
      <a href="#type">Typography</a>
      <a href="#space">Spacing</a>
      <a href="#radius">Radius</a>
      <a href="#shadow">Elevation</a>
      <a href="#motion">Motion</a>
      <a href="#breakpoint">Breakpoints</a>
    </nav>
  </header>

  ${section(
    'color',
    'Colour',
    'Two tiers. <strong>Ramps</strong> are raw material; <strong>semantic</strong> aliases are what components actually consume. Components reference the semantic layer, so a brand change edits aliases once rather than every call site.',
    colorBlocks
  )}

  ${section(
    'type',
    'Typography',
    'Families, size ramp, weights, line heights and tracking.',
    `<h3>Families</h3>${families}
     <h3>Size ramp</h3>${typeRamp}
     <h3>Weights</h3>${weights}
     <h3>Line height</h3>${lineHeights}
     <h3>Letter spacing</h3>${tracking}`
  )}

  ${section(
    'space',
    'Spacing & measure',
    'A 4px-based rhythm. Container widths cap the measure at each layout tier.',
    `<h3>Scale</h3>${spacing}<h3>Containers</h3>${containers}`
  )}

  ${section('radius', 'Radius', '', radii)}
  ${section('shadow', 'Elevation', 'Shadows are tinted with the darkest neutral rather than pure black, so they sit against the palette instead of greying it.', shadows)}
  ${section('motion', 'Motion', 'Durations and easing curves.', motion)}
  ${section('breakpoint', 'Breakpoints', 'Consumed by Tailwind directly as responsive variants.', breakpoints)}

  <section class="section">
    <h2>Components</h2>
    <p class="blurb">
      Component previews live in the Next app at <code>/styleguide</code>, where
      they import the real components. Reimplementing their markup here would
      create a second copy free to drift from the first.
      Run <code>npm run dev</code> and open <code>/styleguide</code>.
    </p>
  </section>
</div>
</body>
</html>
`;

mkdirSync(resolve(root, 'docs/dist'), { recursive: true });
writeFileSync(resolve(root, 'docs/dist/index.html'), html);
console.log(
  `docs/dist/index.html — ${tokens.length} tokens across ${
    new Set(tokens.map((t) => t.group)).size
  } groups`
);
