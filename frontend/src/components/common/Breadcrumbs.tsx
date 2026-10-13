import { Link } from 'react-router-dom';
import { ChevronRight, MoveLeft } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface Crumb {
  /** Visible text. The last crumb is treated as the current page. */
  label: string;
  /** Route to link to. Omit on the final crumb — the current page isn't a link. */
  to?: string;
}

/**
 * Breadcrumb trail. The last item is the current page: rendered as plain text,
 * marked aria-current, and never linked.
 *
 * Replaces the ad-hoc "Πίσω στην αρχική" links that were duplicated per page.
 * Trade-off: those back-links used history (`navigate(-1)`) so they returned you
 * to wherever you'd come from; breadcrumbs are absolute, so they always point at
 * the parent route. That's the point of a trail — it shows where you *are*.
 */
export default function Breadcrumbs({ items, className }: { items: Crumb[]; className?: string }) {
  // A single crumb is the root — nothing to navigate up to, so render nothing.
  if (items.length < 2) return null;

  return (
    <nav aria-label="Breadcrumb" className={cn('min-w-0', className)}>
      <ol className="flex flex-wrap items-center gap-x-1.5 gap-y-1 text-sm">
        {items.map((item, i) => {
          const isLast = i === items.length - 1;

          return (
            <li key={`${item.label}-${i}`} className="flex min-w-0 items-center gap-1.5">
              {i > 0 && (
                <ChevronRight aria-hidden className="size-3.5 shrink-0 text-muted-foreground/50" />
              )}

              {isLast || !item.to ? (
                <span
                  aria-current={isLast ? 'page' : undefined}
                  // The current page's label is usually long (a hackathon name);
                  // truncate it so one crumb can't wrap the whole trail.
                  className={cn('truncate', isLast ? 'text-foreground' : 'text-muted-foreground')}
                >
                  {item.label}
                </span>
              ) : (
                <Link
                  to={item.to}
                  className="truncate font-medium text-muted-foreground transition-colors hover:text-accent-blue"
                >
                  {item.label}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

/** Trail that starts at the home page — the root every page hangs off. */
export function fromHome(...rest: Crumb[]): Crumb[] {
  return [{ label: 'Αρχική', to: '/' }, ...rest];
}

/**
 * Root-only trail: renders a single "back to home" affordance instead of a
 * one-item trail. Used by top-level pages (/hackathons, /feedback, /credits).
 */
export function HomeBreadcrumb({ className }: { className?: string }) {
  return (
    <Link
      to="/"
      className={cn(
        'relative inline-flex items-center gap-2 text-sm font-semibold text-accent-blue transition-colors after:absolute after:inset-x-0 after:-bottom-0.5 after:h-px after:origin-left after:scale-x-0 after:bg-accent-blue after:transition-transform after:duration-300 after:ease-out hover:after:scale-x-100',
        className,
      )}
    >
      <MoveLeft className="size-4" /> Πίσω στην αρχική
    </Link>
  );
}
