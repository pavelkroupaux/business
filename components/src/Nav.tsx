'use client';

import { useState } from 'react';
import { Container } from './Container';
import { cn } from './cn';

export interface NavLink {
  label: string;
  href: string;
}

export interface NavProps {
  brand: string;
  links: NavLink[];
  /** Path of the page currently being viewed, for `aria-current`. */
  currentPath?: string;
  cta?: NavLink;
}

/**
 * Sticky primary navigation. Collapses to a disclosure menu below `md`.
 *
 * The mobile menu is plain conditional rendering rather than a CSS-hidden
 * duplicate, so collapsed links stay out of the accessibility tree entirely.
 */
export function Nav({ brand, links, currentPath, cta }: NavProps) {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-sticky border-b border-border-subtle bg-bg-canvas/85 backdrop-blur-md">
      <Container>
        <div className="flex h-16 items-center justify-between md:h-20">
          <a
            href="/"
            className="rounded-sm text-base font-semibold tracking-tight text-text-primary focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus-ring"
          >
            {brand}
          </a>

          <nav aria-label="Primary" className="hidden items-center gap-6 md:flex">
            {links.map((link) => {
              const active = currentPath === link.href;
              return (
                <a
                  key={link.href}
                  href={link.href}
                  aria-current={active ? 'page' : undefined}
                  className={cn(
                    'rounded-sm text-sm transition-colors duration-fast ease-standard',
                    'focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus-ring',
                    active
                      ? 'text-text-primary'
                      : 'text-text-secondary hover:text-text-primary'
                  )}
                >
                  {link.label}
                </a>
              );
            })}
            {cta && (
              <a
                href={cta.href}
                className="rounded-pill bg-action-primary px-4 py-2 text-sm font-medium text-action-on-primary transition-colors duration-fast ease-standard hover:bg-action-primary-hover focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus-ring"
              >
                {cta.label}
              </a>
            )}
          </nav>

          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="mobile-nav"
            className="-mr-2 rounded-md p-2 text-text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus-ring md:hidden"
          >
            <span className="sr-only">{open ? 'Close menu' : 'Open menu'}</span>
            <MenuIcon open={open} />
          </button>
        </div>
      </Container>

      {open && (
        <nav
          id="mobile-nav"
          aria-label="Primary"
          className="border-t border-border-subtle bg-bg-canvas md:hidden"
        >
          <Container>
            <ul className="flex flex-col py-3">
              {links.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    aria-current={currentPath === link.href ? 'page' : undefined}
                    onClick={() => setOpen(false)}
                    className="block py-3 text-base text-text-primary"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
              {cta && (
                <li className="pt-3 pb-2">
                  <a
                    href={cta.href}
                    onClick={() => setOpen(false)}
                    className="inline-flex rounded-pill bg-action-primary px-5 py-3 text-base font-medium text-action-on-primary"
                  >
                    {cta.label}
                  </a>
                </li>
              )}
            </ul>
          </Container>
        </nav>
      )}
    </header>
  );
}

function MenuIcon({ open }: { open: boolean }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 22 22"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      aria-hidden="true"
    >
      {open ? (
        <>
          <path d="M5 5l12 12" />
          <path d="M17 5L5 17" />
        </>
      ) : (
        <>
          <path d="M3 7h16" />
          <path d="M3 15h16" />
        </>
      )}
    </svg>
  );
}
