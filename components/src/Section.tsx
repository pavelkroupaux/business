import type { ReactNode } from 'react';
import { Container, type ContainerWidth } from './Container';
import { cn } from './cn';

export type SectionTone = 'canvas' | 'subtle' | 'inverse';
export type SectionSpacing = 'sm' | 'md' | 'lg';

const TONE: Record<SectionTone, string> = {
  canvas: 'bg-bg-canvas text-text-primary',
  subtle: 'bg-bg-subtle text-text-primary',
  inverse: 'bg-bg-inverse text-text-inverse',
};

/** Vertical rhythm steps up at wider viewports rather than scaling linearly. */
const SPACING: Record<SectionSpacing, string> = {
  sm: 'py-9 md:py-10',
  md: 'py-10 md:py-11',
  lg: 'py-11 md:py-12',
};

export interface SectionProps {
  children: ReactNode;
  tone?: SectionTone;
  spacing?: SectionSpacing;
  width?: ContainerWidth;
  id?: string;
  className?: string;
  /** Accessible name, when the section has no visible heading. */
  ariaLabel?: string;
}

/**
 * A full-bleed band with a contained inner column. Owns vertical rhythm so
 * pages compose sections instead of hand-tuning margins.
 */
export function Section({
  children,
  tone = 'canvas',
  spacing = 'md',
  width = 'wide',
  id,
  className,
  ariaLabel,
}: SectionProps) {
  return (
    <section
      id={id}
      aria-label={ariaLabel}
      className={cn(TONE[tone], SPACING[spacing], className)}
    >
      <Container width={width}>{children}</Container>
    </section>
  );
}
