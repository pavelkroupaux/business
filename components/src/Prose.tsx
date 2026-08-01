import type { ReactNode } from 'react';
import { cn } from './cn';

export interface ProseProps {
  children: ReactNode;
  className?: string;
}

/**
 * Long-form body copy. Styles raw HTML children by element so page content can
 * stay plain markup (or come from a CMS) without every tag needing a class.
 *
 * Written as explicit descendant rules rather than a typography plugin, so the
 * reading styles stay on the same tokens as the rest of the system.
 */
export function Prose({ children, className }: ProseProps) {
  return (
    <div
      className={cn(
        'max-w-[68ch] text-base leading-relaxed text-text-secondary',
        '[&_h2]:mt-10 [&_h2]:mb-4 [&_h2]:text-2xl [&_h2]:font-semibold [&_h2]:tracking-tight [&_h2]:text-text-primary',
        '[&_h3]:mt-8 [&_h3]:mb-3 [&_h3]:text-xl [&_h3]:font-semibold [&_h3]:tracking-tight [&_h3]:text-text-primary',
        '[&_p]:mb-5',
        '[&_ul]:mb-5 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:mb-5 [&_ol]:list-decimal [&_ol]:pl-5',
        '[&_li]:mb-2',
        '[&_strong]:font-semibold [&_strong]:text-text-primary',
        '[&_a]:text-text-accent [&_a]:underline [&_a]:underline-offset-2 hover:[&_a]:no-underline',
        '[&_blockquote]:border-l-2 [&_blockquote]:border-border-strong [&_blockquote]:pl-5 [&_blockquote]:text-text-primary [&_blockquote]:italic',
        '[&_img]:rounded-lg',
        className
      )}
    >
      {children}
    </div>
  );
}
