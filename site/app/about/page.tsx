import type { Metadata } from 'next';
import { Hero } from '@ds/Hero';
import { Section } from '@ds/Section';
import { Prose } from '@ds/Prose';
import { Button } from '@ds/Button';
import { about, site } from '@/content/site';

export const metadata: Metadata = { title: 'About' };

export default function AboutPage() {
  return (
    <>
      <Hero
        eyebrow={about.eyebrow}
        headline={about.headline}
        intro={about.intro}
      />

      <Section width="text">
        <Prose>
          {about.body.map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </Prose>

        <div className="mt-9 flex flex-wrap items-center gap-4">
          <Button href="/contact">Get in touch</Button>
          <span className="text-sm text-text-muted">{site.location}</span>
        </div>
      </Section>
    </>
  );
}
