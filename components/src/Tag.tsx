import type { ReactNode } from 'react';
import { cn } from './cn';

export interface TagProps {
  children: ReactNode;
  tone?: 'default' | 'accent' | 'inverse';
  className?: string;
}

const TONE = {
  default: 'bg-bg-muted text-text-secondary',
  accent: 'bg-accent-50 text-text-accent',
  inverse: 'bg-neutral-800 text-neutral-200',
} as const;

/** Non-interactive metadata label — discipline, year, role. */
export function Tag({ children, tone = 'default', className }: TagProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-pill px-3 py-1 text-xs font-medium tracking-wide',
        TONE[tone],
        className
      )}
    >
      {children}
    </span>
  );
}
