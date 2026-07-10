import { Link } from 'react-router-dom'
import type { Hackathon } from '@/types/hackathon'
import { dayMonth, relativeGreek } from '@/lib/date'
import { applicationBadge } from '@/lib/hackathons'
import LiveDot from './LiveDot'

const MODE_LABEL: Record<NonNullable<Hackathon['mode']>, string> = {
  'in-person': 'In person',
  online: 'Online',
  hybrid: 'Hybrid',
}

export type HighlightState = 'live' | 'soon'
export type HighlightVariant = 'featured' | 'grid'

function prizeLabel(h: Hackathon): string | null {
  if (!h.hasPrize) return null
  const d = h.prizeDetails?.trim()
  return d && d.length <= 16 ? d : 'με έπαθλο'
}

function addedByLabel(h: Hackathon): string | null {
  if (h.submittedByName) return `added by ${h.submittedByName} ✓`
  return h.status === 'published' ? 'reviewed ✓' : null
}

function LiveLabel() {
  return (
    <span className="inline-flex items-center gap-2">
      <LiveDot className="bg-green-300" />
      <span className="font-medium">
        Live <span className="font-serif italic">τώρα</span>
      </span>
    </span>
  )
}

// On the coloured highlight card the application status is plain white text on a
// translucent chip — not the coloured pills used on the cream list cards.
function AppChip({ text }: { text: string }) {
  return (
    <span className="inline-block rounded-md bg-white/15 px-3 py-1.5 text-xs font-medium text-white">
      {text}
    </span>
  )
}

export default function HighlightCard({
  hackathon,
  state,
  variant,
  showTags = true,
}: {
  hackathon: Hackathon
  state: HighlightState
  variant: HighlightVariant
  showTags?: boolean
}) {
  const bg = state === 'live' ? 'bg-[#2f6a47]' : 'bg-accent-blue'
  const mode = hackathon.mode ? MODE_LABEL[hackathon.mode] : null
  const addedBy = addedByLabel(hackathon)
  const endsIn = `τελειώνει ${relativeGreek(hackathon.endDate ?? hackathon.startDate)}`
  const appText = state === 'soon' ? (applicationBadge(hackathon, false)?.text ?? null) : null
  const prize = prizeLabel(hackathon)
  const to = `/hackathon/${hackathon.id}`

  // ---- Featured (single item): application status sits on the right, under the date ----
  if (variant === 'featured') {
    const meta = [mode, hackathon.location, addedBy].filter(Boolean)
    return (
      <Link
        to={to}
        className={`block rounded-3xl ${bg} px-8 py-8 text-white transition hover:brightness-105 md:px-10 md:py-9`}
      >
        <div className="flex items-start justify-between gap-6">
          <div>
            <div className="flex flex-wrap items-center gap-x-2.5 gap-y-1 text-sm text-white/80">
              {state === 'live' && (
                <>
                  <LiveLabel />
                  <span aria-hidden className="text-white/40">·</span>
                </>
              )}
              <span>{meta.join('  ·  ')}</span>
            </div>
            <h3 className="mt-3 font-serif text-3xl font-semibold md:text-4xl">{hackathon.name}</h3>
            {showTags && hackathon.tags && hackathon.tags.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {hackathon.tags.map((t) => (
                  <span key={t} className="rounded-full border border-white/30 px-3 py-1 text-xs">
                    {t}
                  </span>
                ))}
              </div>
            )}
          </div>
          {hackathon.startDate && (
            <div className="flex shrink-0 flex-col items-end text-right">
              <div className="font-serif text-3xl font-semibold md:text-4xl">
                {dayMonth(hackathon.startDate)}
              </div>
              <div className="mt-1 text-sm text-white/70">
                {state === 'live' ? endsIn : relativeGreek(hackathon.startDate)}
                {prize && ` · ${prize}`}
              </div>
              {state === 'live' && (
                <span className="mt-3 inline-block rounded-full border border-white/30 px-3 py-1 text-xs text-white/90">
                  Σε εξέλιξη, καλή επιτυχία!
                </span>
              )}
              {appText && (
                <div className="mt-3">
                  <AppChip text={appText} />
                </div>
              )}
            </div>
          )}
        </div>
      </Link>
    )
  }

  // ---- Grid (2+ items) ----
  const metaLine = [hackathon.location, mode, prizeLabel(hackathon), addedBy]
    .filter(Boolean)
    .join(' · ')

  return (
    <Link to={to} className={`block rounded-2xl ${bg} p-6 text-white transition hover:brightness-105`}>
      <div className="flex items-center justify-between gap-3">
        {state === 'live' ? (
          <span className="text-sm">
            <LiveLabel />
          </span>
        ) : (
          <span className="font-serif text-lg font-semibold">{dayMonth(hackathon.startDate)}</span>
        )}
        <span className="text-xs text-white/70">
          {state === 'live' ? endsIn : relativeGreek(hackathon.startDate)}
        </span>
      </div>
      <h3 className="mt-3 font-serif text-xl font-semibold">{hackathon.name}</h3>
      {metaLine && <p className="mt-1.5 text-sm text-white/70">{metaLine}</p>}
      {appText && (
        <div className="mt-3">
          <AppChip text={appText} />
        </div>
      )}
      {showTags && hackathon.tags && hackathon.tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {hackathon.tags.map((t) => (
            <span key={t} className="rounded-full border border-white/30 px-3 py-1 text-xs">
              {t}
            </span>
          ))}
        </div>
      )}
    </Link>
  )
}
