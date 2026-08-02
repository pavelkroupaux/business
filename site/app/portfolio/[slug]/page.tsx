import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { Hero } from '@ds/Hero';
import { Section } from '@ds/Section';
import { Prose } from '@ds/Prose';
import { Tag } from '@ds/Tag';
import { Button } from '@ds/Button';
import { projects } from '@/content/site';

export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const project = projects.find((p) => p.slug === slug);
  return project
    ? { title: project.title, description: project.summary }
    : {};
}

export default async function ProjectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const project = projects.find((p) => p.slug === slug);

  if (!project) notFound();

  return (
    <>
      <Hero eyebrow="Case study" headline={project.title} intro={project.summary} />

      <Section width="text">
        {project.meta.length > 0 && (
          <div className="mb-8 flex flex-wrap gap-2">
            {project.meta.map((m) => (
              <Tag key={m}>{m}</Tag>
            ))}
          </div>
        )}

        <Prose>
          {project.body.map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </Prose>

        <div className="mt-10 border-t border-border-subtle pt-8">
          <Button href="/portfolio" variant="ghost" size="sm">
            ← All work
          </Button>
        </div>
      </Section>
    </>
  );
}
