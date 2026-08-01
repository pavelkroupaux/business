/**
 * Minimal class joiner. Kept dependency-free on purpose — the component layer
 * should not pull a package in for something this small.
 */
export function cn(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(' ');
}
