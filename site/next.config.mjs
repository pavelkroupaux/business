import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');

/** @type {import('next').NextConfig} */
export default {
  // The component library and token output live above site/, so tracing has to
  // start at the repo root rather than at the Next app directory.
  outputFileTracingRoot: repoRoot,
};
