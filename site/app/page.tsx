import { Hero } from '@ds/Hero';
import { Section } from '@ds/Section';
import { SectionHeader } from '@ds/SectionHeader';
import { Card } from '@ds/Card';
import { Button } from '@ds/Button';
import { home, projects } from '@/content/site';

export default function HomePage() {
  return (
    <>
      <Hero
        eyebrow={home.eyebrow}
        headline={home.headline}
        intro={home.intro}
        actions={
          <>
            <Button href="/portfolio">View work</Button>
            <Button href="/contact" variant="secondary">
              Get in touch
            </Button>
          </>
        }
      />

      <Section tone="subtle" spacing="lg">
        <SectionHeader
          eyebrow={home.work.eyebrow}
          title={home.work.title}
          description={home.work.description}
          action={
            <Button href="/portfolio" variant="ghost" size="sm">
              All work →
            </Button>
          }
        />
        <div className="grid gap-5 md:grid-cols-2">
          {projects.map((p) => (
            <Card
              key={p.slug}
              title={p.title}
              summary={p.summary}
              href={`/portfolio/${p.slug}`}
              meta={p.meta}
              featured={p.featured}
            />
          ))}
        </div>
      </Section>

      <Section tone="inverse" spacing="lg" width="text">
        <div className="flex flex-col items-start gap-6">
          <h2 className="text-2xl leading-snug font-semibold tracking-tight text-balance md:text-3xl">
            {home.cta.title}
          </h2>
          <p className="max-w-[48ch] text-lg leading-relaxed text-neutral-300">
            {home.cta.description}
          </p>
          <Button href="/contact" variant="secondary">
            {home.cta.action}
          </Button>
        </div>
      </Section>
    </>
  );
}
