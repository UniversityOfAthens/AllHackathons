import type { Hackathon } from '@/types/hackathon'
import HighlightCard from './HighlightCard'
import LiveDot from './LiveDot'
import { highlightSelection } from '@/lib/hackathons'

// The top highlight slot: live hackathons (green) if any are happening now,
// otherwise the soonest upcoming ones (blue). Both adapt to 1 / 2 / 3+ items.
// The selection logic lives in lib/hackathons so the list can exclude these.
export default function Highlights({ hackathons }: { hackathons: Hackathon[] }) {
  const { state, items } = highlightSelection(hackathons)
  if (!state) return null

  const count = items.length
  const variant = count === 1 ? 'featured' : 'grid'
  const showTags = count <= 2
  const gridCols = count === 2 ? 'sm:grid-cols-2' : 'sm:grid-cols-2 lg:grid-cols-3'

  const eyebrow =
    state === 'live'
      ? count === 1
        ? 'Live τώρα'
        : `Live τώρα · ${count}`
      : count === 1
        ? 'Ξεκινάει σύντομα'
        : `Ξεκινάνε σύντομα · ${count}`

  return (
    <section className="mx-auto w-full max-w-[1140px] px-6 pt-14 md:px-10">
      <div className="flex items-center gap-3">
        {state === 'live' && <LiveDot />}
        <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
          {eyebrow}
        </p>
        <div className="h-px flex-1 bg-border" />
      </div>
      <div className={variant === 'featured' ? 'mt-5' : `mt-5 grid gap-4 ${gridCols}`}>
        {items.map((h) => (
          <HighlightCard
            key={h.id}
            hackathon={h}
            state={state}
            variant={variant}
            showTags={showTags}
          />
        ))}
      </div>
    </section>
  )
}
