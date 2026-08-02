import type { Metadata } from 'next';
import { Hero } from '@ds/Hero';
import { Section } from '@ds/Section';
import { Card } from '@ds/Card';
import { projects } from '@/content/site';

export const metadata: Metadata = { title: 'Portfolio' };

export default function PortfolioPage() {
  return (
    <>
      <Hero
        eyebrow="Work"
        headline="Selected projects"
        intro="[PLACEHOLDER] Replace with the real portfolio introduction."
      />

      <Section tone="subtle" spacing="lg">
        <div className="grid gap-5 md:grid-cols-2">
          {projects.map((p) => (
            <Card
              key={p.slug}
              title={p.title}
              summary={p.summary}
              href={`/portfolio/${p.slug}`}
              meta={p.meta}
            />
          ))}
        </div>
      </Section>
    </>
  );
}
