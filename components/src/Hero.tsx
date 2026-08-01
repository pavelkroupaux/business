import type { ReactNode } from 'react';
import { Container } from './Container';
import { cn } from './cn';

export interface HeroProps {
  /** Small line above the headline. */
  eyebrow?: string;
  headline: string;
  intro?: string;
  actions?: ReactNode;
  align?: 'left' | 'center';
  tone?: 'canvas' | 'subtle' | 'inverse';
}

const TONE = {
  canvas: 'bg-bg-canvas text-text-primary',
  subtle: 'bg-bg-subtle text-text-primary',
  inverse: 'bg-bg-inverse text-text-inverse',
} as const;

/**
 * Opening statement of a page.
 *
 * The headline steps across four sizes rather than using viewport units, so it
 * stays on the type ramp at every width instead of landing between steps.
 */
export function Hero({
  eyebrow,
  headline,
  intro,
  actions,
  align = 'left',
  tone = 'canvas',
}: HeroProps) {
  const centered = align === 'center';

  return (
    <section className={cn(TONE[tone], 'py-11 md:py-12')}>
      <Container>
        <div className={cn('flex flex-col', centered && 'items-center text-center')}>
          {eyebrow && (
            <p
              className={cn(
                'mb-5 text-sm font-medium tracking-wider uppercase',
                tone === 'inverse' ? 'text-neutral-300' : 'text-text-muted'
              )}
            >
              {eyebrow}
            </p>
          )}

          <h1 className="max-w-[16ch] text-3xl leading-tight font-semibold tracking-tighter text-balance md:text-4xl lg:text-5xl">
            {headline}
          </h1>

          {intro && (
            <p
              className={cn(
                'mt-6 max-w-[52ch] text-lg leading-relaxed text-pretty md:text-xl',
                tone === 'inverse' ? 'text-neutral-300' : 'text-text-secondary'
              )}
            >
              {intro}
            </p>
          )}

          {actions && (
            <div
              className={cn(
                'mt-8 flex flex-wrap gap-4',
                centered && 'justify-center'
              )}
            >
              {actions}
            </div>
          )}
        </div>
      </Container>
    </section>
  );
}
