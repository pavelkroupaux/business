/**
 * Minimal class joiner. Kept dependency-free on purpose — the component layer
 * should not pull a package in for something this small.
 *
 * Accepts `unknown` because the common guard `someNode && 'class'` yields
 * whatever falsy value the left side held, and a ReactNode may legitimately be
 * `0` or `0n`. Filtering to strings rather than to truthiness means a stray
 * number can never leak into the class list as "0".
 */
export function cn(...parts: unknown[]): string {
  return parts.filter((p): p is string => typeof p === 'string' && p !== '').join(' ');
}
