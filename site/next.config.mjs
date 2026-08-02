import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');

/** @type {import('next').NextConfig} */
export default {
  // The component library and token output live above site/, so tracing has to
  // start at the repo root rather than at the Next app directory.
  outputFileTracingRoot: repoRoot,

  // Emit a fully static site to site/out. Every route is statically known --
  // generateStaticParams covers portfolio/[slug], and nothing here uses route
  // handlers, server actions, cookies()/headers() or next/image -- so there is
  // no server runtime to give up. This also lets Vercel build from the repo
  // root: a static output needs no framework detection, which cannot succeed
  // at the root anyway because next is a dependency of site/, not of the root
  // package.json.
  output: 'export',
};
