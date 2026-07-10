import { Link } from 'react-router-dom'
import { dayOf, monthUpper, dayRange, relativeGreek } from '@/lib/date'
import { hackathonState, todayISO, applicationBadge } from '@/lib/hackathons'
import { cn } from '@/lib/utils'
import type { Hackathon } from '@/types/hackathon'

const MODE_LABEL: Record<NonNullable<Hackathon['mode']>, string> = {
  'in-person': 'In person',
  online: 'Online',
  hybrid: 'Hybrid',
}

function prizeLabel(h: Hackathon): string | null {
  if (!h.hasPrize) return null
  const d = h.prizeDetails?.trim()
  return d && d.length <= 16 ? d : 'με έπαθλο'
}

export default function HackathonCard({ hackathon }: { hackathon: Hackathon }) {
  const today = todayISO()
  const state = hackathonState(hackathon, today)
  const isPast = state === 'past'

  const meta = [
    hackathon.location,
    hackathon.mode ? MODE_LABEL[hackathon.mode] : null,
    prizeLabel(hackathon),
  ].filter(Boolean)

  const appBadge = applicationBadge(hackathon, isPast)

  // Top-right status pill.
  const statePill =
    state === 'live'
      ? { text: 'Live τώρα', cls: 'bg-accent-green/15 text-accent-green' }
      : state === 'past'
        ? { text: 'Έληξε', cls: 'bg-muted text-muted-foreground' }
        : { text: relativeGreek(hackathon.startDate), cls: 'bg-accent-blue/10 text-accent-blue' }

  const range = dayRange(hackathon.startDate, hackathon.endDate)

  return (
    <Link
      to={`/hackathon/${hackathon.id}`}
      className={cn(
        'flex gap-5 rounded-2xl border border-border bg-card p-6 shadow-[0_1px_2px_rgba(60,50,20,0.04)] transition-colors hover:border-accent-blue/50',
        isPast && 'opacity-65',
      )}
    >
      {/* Date block */}
      {hackathon.startDate && (
        <div className="shrink-0 text-center">
          <div
            className={cn(
              'font-serif text-3xl font-semibold leading-none',
              isPast ? 'text-muted-foreground' : 'text-accent-blue',
            )}
          >
            {dayOf(hackathon.startDate)}
          </div>
          <div className="mt-1 font-mono text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
            {monthUpper(hackathon.startDate)}
          </div>
          {range && <div className="mt-2 text-[11px] text-muted-foreground">{range}</div>}
        </div>
      )}

      {/* Body */}
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-3">
          <h3 className="font-serif text-xl font-semibold text-foreground">{hackathon.name}</h3>
          <span
            className={cn(
              'shrink-0 rounded-full px-2.5 py-1 text-[11px] font-medium',
              statePill.cls,
            )}
          >
            {statePill.text}
          </span>
        </div>

        {meta.length > 0 && (
          <p className="mt-1 text-sm text-muted-foreground">{meta.join('  ·  ')}</p>
        )}

        {appBadge && (
          <div className="mt-3">
            <span
              className={cn(
                'inline-block rounded-md px-3 py-1.5 text-xs font-medium',
                appBadge.cls,
              )}
            >
              {appBadge.text}
            </span>
          </div>
        )}

        {hackathon.tags && hackathon.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {hackathon.tags.map((t) => (
              <span
                key={t}
                className="rounded-full bg-secondary px-3 py-1 text-xs text-secondary-foreground"
              >
                {t}
              </span>
            ))}
          </div>
        )}

        <div className="mt-4 flex flex-wrap items-center gap-x-1.5 gap-y-1 text-xs text-muted-foreground">
          {hackathon.submittedByName && (
            <>
              <span>added by</span>
              <span className="font-medium text-foreground">{hackathon.submittedByName}</span>
            </>
          )}
          {hackathon.status === 'published' && (
            <span className="text-accent-green">✓ reviewed</span>
          )}
        </div>
      </div>
    </Link>
  )
}
