import { cn } from '@/lib/utils'

export type ModeFilter = 'all' | 'in-person' | 'online'

const PILLS: { key: ModeFilter; label: string }[] = [
  { key: 'all', label: 'Όλα' },
  { key: 'in-person', label: 'In person' },
  { key: 'online', label: 'Online' },
]

// Design-pass filter row (issue #3). The full upcoming/past/tag/search logic and
// server-side query params are owned by #14 — this is the visual control + a basic
// client-side mode filter.
export default function HackathonFilters({
  mode,
  onModeChange,
}: {
  mode: ModeFilter
  onModeChange: (m: ModeFilter) => void
}) {
  return (
    <div className="flex flex-wrap items-center gap-3">
      {/* Region — static for now; region filtering is a later enhancement. */}
      <div className="inline-flex items-center gap-2 rounded-full border border-input bg-card px-4 py-2 text-sm text-foreground">
        <span aria-hidden>🌐</span>
        Όλη η Ελλάδα
        <span className="text-muted-foreground" aria-hidden>▾</span>
      </div>
      <div className="hidden h-5 w-px bg-border sm:block" />
      <div className="flex items-center gap-2">
        {PILLS.map((p) => (
          <button
            key={p.key}
            onClick={() => onModeChange(p.key)}
            className={cn(
              'cursor-pointer rounded-full px-4 py-2 text-sm font-medium transition-colors',
              mode === p.key
                ? 'bg-primary text-primary-foreground'
                : 'border border-input text-foreground hover:bg-accent',
            )}
          >
            {p.label}
          </button>
        ))}
      </div>
    </div>
  )
}
