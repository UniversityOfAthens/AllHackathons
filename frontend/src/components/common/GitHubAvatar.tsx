import { cn } from '@/lib/utils';
import { avatarColor, initials } from '@/lib/avatar';

/**
 * A GitHub profile avatar that falls back to generated initials.
 *
 * The image comes from GitHub's CDN (`github.com/<handle>.png`) — no API call,
 * no token, no accounts. If it fails to load (offline, blocked, no avatar set)
 * we render the same deterministic initials avatar the rest of the site uses, so
 * a dead network never shows a broken image.
 *
 * The <img> is decorative (alt="") — the handle is already the accessible text
 * next to it, so announcing the avatar again would just be noise.
 */
export default function GitHubAvatar({
  handle,
  className,
}: {
  handle: string;
  /** Outer box; drives the size. */
  className?: string;
}) {
  return (
    <span className={cn('relative inline-flex shrink-0', className)}>
      <img
        src={`https://github.com/${handle}.png?size=160`}
        alt=""
        loading="lazy"
        decoding="async"
        onError={(e) => {
          // Swap to the initials avatar. The <img> stays mounted but hidden
          // rather than being unmounted, so a re-render can't reload a bad URL.
          e.currentTarget.style.display = 'none';
          const fallback = e.currentTarget.nextElementSibling as HTMLElement | null;
          if (fallback) fallback.style.display = '';
        }}
        className="size-full rounded-full object-cover"
      />
      <span
        aria-hidden
        className="absolute inset-0 hidden items-center justify-center rounded-full font-mono font-semibold text-white"
        style={{ backgroundColor: avatarColor(handle) }}
      >
        {initials(handle)}
      </span>
    </span>
  );
}
