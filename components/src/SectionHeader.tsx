import type { ReactNode } from 'react';
import { cn } from './cn';

export interface SectionHeaderProps {
  title: string;
  eyebrow?: string;
  description?: string;
  /** Trailing slot — usually a "view all" link. */
  action?: ReactNode;
  align?: 'left' | 'center';
  /** Heading level. Defaults to h2; drop to h3 when nested. */
  as?: 'h2' | 'h3';
  className?: string;
}

/** Titles a band of content. Keeps section intros consistent across pages. */
export function SectionHeader({
  title,
  eyebrow,
  description,
  action,
  align = 'left',
  as: Heading = 'h2',
  className,
}: SectionHeaderProps) {
  const centered = align === 'center';

  return (
    <div
      className={cn(
        'mb-8 flex flex-col gap-5 md:mb-9',
        action && !centered && 'md:flex-row md:items-end md:justify-between',
        centered && 'items-center text-center',
        className
      )}
    >
      <div className={cn(centered && 'flex flex-col items-center')}>
        {eyebrow && (
          <p className="mb-3 text-sm font-medium tracking-wider uppercase text-text-muted">
            {eyebrow}
          </p>
        )}
        <Heading className="max-w-[24ch] text-2xl leading-snug font-semibold tracking-tight text-balance text-text-primary md:text-3xl">
          {title}
        </Heading>
        {description && (
          <p className="mt-4 max-w-[56ch] text-lg leading-relaxed text-pretty text-text-secondary">
            {description}
          </p>
        )}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}
