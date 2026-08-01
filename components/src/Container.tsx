import type { ReactNode, ElementType } from 'react';
import { cn } from './cn';

export type ContainerWidth = 'narrow' | 'text' | 'wide' | 'bleed';

/**
 * These map to Tailwind's `--container-*` namespace, so the utility is
 * `max-w-wide`, not `max-w-container-wide`.
 */
const WIDTH: Record<ContainerWidth, string> = {
  narrow: 'max-w-narrow',
  text: 'max-w-text',
  wide: 'max-w-wide',
  bleed: 'max-w-bleed',
};

export interface ContainerProps {
  children: ReactNode;
  /** Measure cap. `text` is the reading measure; `wide` is the default layout. */
  width?: ContainerWidth;
  as?: ElementType;
  className?: string;
}

/**
 * Horizontal measure + responsive gutters. The single place page width is
 * decided, so nothing else needs to know the container values.
 */
export function Container({
  children,
  width = 'wide',
  as: Tag = 'div',
  className,
}: ContainerProps) {
  return (
    <Tag
      className={cn(
        'mx-auto w-full px-5 md:px-6 lg:px-8',
        WIDTH[width],
        className
      )}
    >
      {children}
    </Tag>
  );
}
