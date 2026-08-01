import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { Section } from '@ds/Section';
import { Container } from '@ds/Container';
import { Button } from '@ds/Button';
import { Card } from '@ds/Card';
import { Tag } from '@ds/Tag';
import { Prose } from '@ds/Prose';
import { SectionHeader } from '@ds/SectionHeader';

export const metadata: Metadata = { title: 'Style guide' };

/**
 * Component gallery. Imports the real components, so what renders here is
 * exactly what renders on the site — there is no second copy to drift.
 *
 * Token values are documented separately at docs/dist/index.html.
 */
export default function StyleguidePage() {
  return (
    <>
      <Section spacing="sm">
        <h1 className="text-3xl font-semibold tracking-tighter md:text-4xl">
          Component gallery
        </h1>
        <p className="mt-4 max-w-[60ch] text-lg text-text-secondary">
          Every component, rendered from the same source the site uses. For token
          values — colour, type, spacing, elevation — see{' '}
          <code className="rounded-sm bg-bg-muted px-1.5 py-0.5 text-sm">
            docs/dist/index.html
          </code>
          .
        </p>
        <div className="mt-6 rounded-lg bg-accent-50 p-5 text-sm text-accent-900">
          <strong className="mb-1 block">Appearance is provisional.</strong>
          The live site was unreachable from the build environment, so
          proportions and colour are reasonable defaults rather than observed
          values. Structure and behaviour are real.
        </div>
      </Section>

      <Row title="Button" note="4 variants × 3 sizes. Renders <a> when given href.">
        <div className="flex flex-col gap-5">
          <div className="flex flex-wrap items-center gap-3">
            <Button variant="primary">Primary</Button>
            <Button variant="accent">Accent</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="ghost">Ghost</Button>
            <Button disabled>Disabled</Button>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Button size="sm">Small</Button>
            <Button size="md">Medium</Button>
            <Button size="lg">Large</Button>
          </div>
        </div>
      </Row>

      <Row title="Tag" note="Non-interactive metadata chip.">
        <div className="flex flex-wrap gap-2">
          <Tag>Default</Tag>
          <Tag tone="accent">Accent</Tag>
          <Tag tone="inverse">Inverse</Tag>
        </div>
      </Row>

      <Row title="Card" note="Optional stretched link; only the title takes focus.">
        <div className="grid gap-5 md:grid-cols-2">
          <Card
            title="Card with link and metadata"
            summary="The whole card is clickable, but only the title is in the tab order — one keyboard stop carrying a meaningful name."
            href="#"
            meta={['Product design', '2024']}
          />
          <Card
            title="Card without a link"
            summary="Renders as a plain article when no href is supplied."
            meta={['Static']}
          />
        </div>
      </Row>

      <Row title="SectionHeader" note="Eyebrow, title, description, trailing action.">
        <SectionHeader
          eyebrow="Eyebrow"
          title="A section header with an action"
          description="Used to title a band of content consistently across pages."
          action={
            <Button variant="ghost" size="sm">
              Action →
            </Button>
          }
        />
      </Row>

      <Row title="Prose" note="Styles raw HTML by element, for long-form copy.">
        <Prose>
          <h2>A heading inside prose</h2>
          <p>
            Body copy at the reading measure, capped at 68 characters. Inline{' '}
            <a href="#">links</a> and <strong>strong text</strong> pick up their
            colour from tokens.
          </p>
          <ul>
            <li>Unordered list item</li>
            <li>Another item</li>
          </ul>
          <blockquote>A blockquote, marked with a left rule.</blockquote>
        </Prose>
      </Row>

      <Row title="Section tones" note="canvas · subtle · inverse">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-lg border border-border-subtle bg-bg-canvas p-5">
            <p className="text-sm font-medium">canvas</p>
          </div>
          <div className="rounded-lg border border-border-subtle bg-bg-subtle p-5">
            <p className="text-sm font-medium">subtle</p>
          </div>
          <div className="rounded-lg bg-bg-inverse p-5 text-text-inverse">
            <p className="text-sm font-medium">inverse</p>
          </div>
        </div>
      </Row>

      <Section spacing="sm" tone="subtle">
        <h2 className="text-2xl font-semibold tracking-tight">Nav & Footer</h2>
        <p className="mt-3 max-w-[60ch] text-base text-text-secondary">
          Both are rendered live on this page — the sticky nav above and the
          footer below. Narrow the viewport past the <code>md</code> breakpoint
          (768px) to see the nav collapse to a disclosure menu.
        </p>
      </Section>
    </>
  );
}

function Row({
  title,
  note,
  children,
}: {
  title: string;
  note?: string;
  children: ReactNode;
}) {
  return (
    <section className="border-t border-border-subtle py-9">
      <Container>
        <div className="mb-6">
          <h2 className="text-xl font-semibold tracking-tight">{title}</h2>
          {note && <p className="mt-1 text-sm text-text-muted">{note}</p>}
        </div>
        {children}
      </Container>
    </section>
  );
}
