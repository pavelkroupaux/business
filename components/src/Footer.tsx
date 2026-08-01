import { Container } from './Container';
import type { NavLink } from './Nav';

export interface FooterProps {
  brand: string;
  tagline?: string;
  links?: NavLink[];
  social?: NavLink[];
  email?: string;
}

/** Site footer: contact, secondary navigation, colophon. */
export function Footer({ brand, tagline, links, social, email }: FooterProps) {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border-subtle bg-bg-subtle">
      <Container>
        <div className="flex flex-col gap-9 py-10 md:flex-row md:justify-between">
          <div className="max-w-[36ch]">
            <p className="text-base font-semibold tracking-tight text-text-primary">
              {brand}
            </p>
            {tagline && (
              <p className="mt-2 text-sm leading-relaxed text-text-secondary">
                {tagline}
              </p>
            )}
            {email && (
              <a
                href={`mailto:${email}`}
                className="mt-5 inline-block rounded-sm text-base text-text-primary underline underline-offset-4 hover:no-underline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus-ring"
              >
                {email}
              </a>
            )}
          </div>

          <div className="flex gap-11">
            {links && links.length > 0 && (
              <FooterColumn heading="Site" items={links} />
            )}
            {social && social.length > 0 && (
              <FooterColumn heading="Elsewhere" items={social} external />
            )}
          </div>
        </div>

        <div className="border-t border-border-subtle py-6">
          <p className="text-xs text-text-muted">
            © {year} {brand}
          </p>
        </div>
      </Container>
    </footer>
  );
}

function FooterColumn({
  heading,
  items,
  external = false,
}: {
  heading: string;
  items: NavLink[];
  external?: boolean;
}) {
  return (
    <nav aria-label={heading}>
      <h2 className="mb-4 text-xs font-medium tracking-wider uppercase text-text-muted">
        {heading}
      </h2>
      <ul className="flex flex-col gap-3">
        {items.map((item) => (
          <li key={item.href}>
            <a
              href={item.href}
              {...(external
                ? { target: '_blank', rel: 'noopener noreferrer' }
                : {})}
              className="rounded-sm text-sm text-text-secondary transition-colors duration-fast ease-standard hover:text-text-primary focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus-ring"
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
