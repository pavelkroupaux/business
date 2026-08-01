import type { ReactNode } from 'react';
import { cn } from './cn';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'accent';
export type ButtonSize = 'sm' | 'md' | 'lg';

const VARIANT: Record<ButtonVariant, string> = {
  primary:
    'bg-action-primary text-action-on-primary hover:bg-action-primary-hover border border-transparent',
  accent:
    'bg-action-accent text-action-on-accent hover:bg-action-accent-hover border border-transparent',
  secondary:
    'bg-bg-canvas text-text-primary border border-border-default hover:border-border-strong hover:bg-bg-subtle',
  ghost:
    'bg-transparent text-text-secondary border border-transparent hover:text-text-primary hover:bg-bg-subtle',
};

const SIZE: Record<ButtonSize, string> = {
  sm: 'text-sm px-4 py-2 gap-2',
  md: 'text-base px-5 py-3 gap-2',
  lg: 'text-lg px-6 py-4 gap-3',
};

export interface ButtonProps {
  children: ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  /** Renders an anchor instead of a button. */
  href?: string;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  className?: string;
  onClick?: () => void;
}

/**
 * Every interactive affordance in the system. Renders `<a>` when given `href`
 * so a link stays a link — navigation should survive JS not loading.
 */
export function Button({
  children,
  variant = 'primary',
  size = 'md',
  href,
  type = 'button',
  disabled,
  className,
  onClick,
}: ButtonProps) {
  const classes = cn(
    'inline-flex items-center justify-center rounded-pill font-medium',
    'transition-colors duration-normal ease-standard',
    'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus-ring',
    disabled && 'pointer-events-none opacity-50',
    VARIANT[variant],
    SIZE[size],
    className
  );

  if (href) {
    return (
      <a href={href} className={classes} aria-disabled={disabled || undefined}>
        {children}
      </a>
    );
  }

  return (
    <button type={type} className={classes} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}
