'use client';

import { usePathname } from 'next/navigation';
import { Nav } from '@ds/Nav';
import { site, navLinks, navCta } from '@/content/site';

/**
 * Binds the design system's Nav to Next's router.
 *
 * Keeping the route awareness here means the Nav component itself stays
 * framework-agnostic — it takes `currentPath` as data rather than reaching for
 * a Next-specific hook, so it remains usable outside this app.
 */
export function SiteNav() {
  const pathname = usePathname();

  return (
    <Nav
      brand={site.brand}
      links={navLinks}
      currentPath={pathname}
      cta={navCta}
    />
  );
}
