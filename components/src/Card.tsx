import { Tag } from './Tag';
import { cn } from './cn';

export interface CardProps {
  title: string;
  summary?: string;
  href?: string;
  /** Metadata chips — discipline, year, client. */
  meta?: string[];
  image?: { src: string; alt: string };
  /** Feature cards span wider and lead with a taller image. */
  featured?: boolean;
  className?: string;
}

/**
 * Project / content card.
 *
 * When `href` is set the whole card is clickable via a stretched overlay link,
 * but only the title is in the tab order — so keyboard users get one stop
 * carrying a meaningful accessible name, not a card-sized anonymous target.
 */
export function Card({
  title,
  summary,
  href,
  meta,
  image,
  featured = false,
  className,
}: CardProps) {
  return (
    <article
      className={cn(
        'group relative flex flex-col overflow-hidden rounded-xl border border-border-subtle bg-bg-canvas',
        'transition-shadow duration-normal ease-standard hover:shadow-lg',
        className
      )}
    >
      {image && (
        <div
          className={cn(
            'overflow-hidden bg-bg-muted',
            featured ? 'aspect-[16/9]' : 'aspect-[4/3]'
          )}
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={image.src}
            alt={image.alt}
            loading="lazy"
            className="h-full w-full object-cover transition-transform duration-slow ease-standard group-hover:scale-[1.03]"
          />
        </div>
      )}

      <div className={cn('flex flex-1 flex-col p-5', featured && 'md:p-6')}>
        {meta && meta.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-2">
            {meta.map((m) => (
              <Tag key={m}>{m}</Tag>
            ))}
          </div>
        )}

        <h3
          className={cn(
            'font-semibold tracking-tight text-text-primary',
            featured ? 'text-2xl' : 'text-xl'
          )}
        >
          {href ? (
            <a
              href={href}
              className="rounded-sm before:absolute before:inset-0 before:content-[''] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus-ring"
            >
              {title}
            </a>
          ) : (
            title
          )}
        </h3>

        {summary && (
          <p className="mt-3 text-base leading-relaxed text-pretty text-text-secondary">
            {summary}
          </p>
        )}
      </div>
    </article>
  );
}
