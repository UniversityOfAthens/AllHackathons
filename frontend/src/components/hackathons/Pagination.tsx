import { cn } from '@/lib/utils'

// Page list with first/last always shown and an ellipsis for the gap, e.g.
// [1, gap, 4, 5, 6, gap, 20]. Scales to many pages.
function pageRange(current: number, total: number): (number | 'gap')[] {
  const range: (number | 'gap')[] = []
  const left = Math.max(2, current - 1)
  const right = Math.min(total - 1, current + 1)
  range.push(1)
  if (left > 2) range.push('gap')
  for (let i = left; i <= right; i++) range.push(i)
  if (right < total - 1) range.push('gap')
  if (total > 1) range.push(total)
  return range
}

const BTN =
  'inline-flex h-9 min-w-9 cursor-pointer items-center justify-center rounded-md px-3 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-40'

export default function Pagination({
  page,
  pageCount,
  onPage,
}: {
  page: number
  pageCount: number
  onPage: (p: number) => void
}) {
  if (pageCount <= 1) return null
  const items = pageRange(page, pageCount)

  return (
    <nav className="flex flex-wrap items-center justify-center gap-1.5" aria-label="Σελιδοποίηση">
      <button
        className={cn(BTN, 'border border-input text-foreground hover:bg-accent')}
        onClick={() => onPage(page - 1)}
        disabled={page === 1}
      >
        ← Προηγ.
      </button>
      {items.map((it, i) =>
        it === 'gap' ? (
          <span key={`gap-${i}`} className="px-1 text-muted-foreground">
            …
          </span>
        ) : (
          <button
            key={it}
            onClick={() => onPage(it)}
            aria-current={it === page ? 'page' : undefined}
            className={cn(
              BTN,
              it === page
                ? 'bg-primary text-primary-foreground'
                : 'border border-input text-foreground hover:bg-accent',
            )}
          >
            {it}
          </button>
        ),
      )}
      <button
        className={cn(BTN, 'border border-input text-foreground hover:bg-accent')}
        onClick={() => onPage(page + 1)}
        disabled={page === pageCount}
      >
        Επόμ. →
      </button>
    </nav>
  )
}
