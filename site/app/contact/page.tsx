import type { Metadata } from 'next';
import { Hero } from '@ds/Hero';
import { Section } from '@ds/Section';
import { Button } from '@ds/Button';
import { contact, site, socialLinks } from '@/content/site';

export const metadata: Metadata = { title: 'Contact' };

export default function ContactPage() {
  return (
    <>
      <Hero
        eyebrow={contact.eyebrow}
        headline={contact.headline}
        intro={contact.intro}
        actions={<Button href={`mailto:${site.email}`}>{site.email}</Button>}
      />

      <Section tone="subtle" width="text">
        <dl className="grid gap-8 sm:grid-cols-2">
          <div>
            <dt className="text-xs font-medium tracking-wider uppercase text-text-muted">
              Email
            </dt>
            <dd className="mt-2">
              <a
                href={`mailto:${site.email}`}
                className="rounded-sm text-base text-text-primary underline underline-offset-4 hover:no-underline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus-ring"
              >
                {site.email}
              </a>
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium tracking-wider uppercase text-text-muted">
              Based in
            </dt>
            <dd className="mt-2 text-base text-text-primary">{site.location}</dd>
          </div>
          {socialLinks.length > 0 && (
            <div>
              <dt className="text-xs font-medium tracking-wider uppercase text-text-muted">
                Elsewhere
              </dt>
              <dd className="mt-2 flex flex-col gap-2">
                {socialLinks.map((s) => (
                  <a
                    key={s.href}
                    href={s.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="rounded-sm text-base text-text-primary underline underline-offset-4 hover:no-underline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus-ring"
                  >
                    {s.label}
                  </a>
                ))}
              </dd>
            </div>
          )}
        </dl>
      </Section>
    </>
  );
}
