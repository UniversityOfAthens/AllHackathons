import type { Hackathon } from '@/types/hackathon'
import { daysUntil, relativeGreek, dayMonth } from './date'

export type HackathonState = 'live' | 'upcoming' | 'past'

export function todayISO(): string {
  return new Date().toISOString().slice(0, 10)
}

/** live = happening now, upcoming = starts in the future, past = already ended. */
export function hackathonState(h: Hackathon, today: string = todayISO()): HackathonState {
  const start = h.startDate
  const end = h.endDate ?? h.startDate
  if (start && end && start <= today && end >= today) return 'live'
  if (start && start > today) return 'upcoming'
  return 'past'
}

const GROUP_ORDER: Record<HackathonState, number> = { live: 0, upcoming: 1, past: 2 }

/** Sort: live → upcoming (soonest first) → past (most recent first). */
export function compareForList(a: Hackathon, b: Hackathon, today: string = todayISO()): number {
  const ga = GROUP_ORDER[hackathonState(a, today)]
  const gb = GROUP_ORDER[hackathonState(b, today)]
  if (ga !== gb) return ga - gb
  const cmp = (a.startDate ?? '').localeCompare(b.startDate ?? '')
  return ga === GROUP_ORDER.past ? -cmp : cmp // past newest-first
}

export type HighlightSelection = { state: 'live' | 'soon' | null; items: Hackathon[] }

/**
 * What the homepage highlight spotlights: all live hackathons, else the soonest
 * upcoming ones (those sharing the earliest start date). Shared so the list can
 * exclude whatever the highlight already shows (no duplicates).
 */
export function highlightSelection(
  hackathons: Hackathon[],
  today: string = todayISO(),
): HighlightSelection {
  const published = hackathons.filter((h) => h.status === 'published' && !!h.startDate)
  const byStart = (a: Hackathon, b: Hackathon) =>
    (a.startDate ?? '').localeCompare(b.startDate ?? '')

  const live = published.filter((h) => hackathonState(h, today) === 'live').sort(byStart)
  if (live.length) return { state: 'live', items: live }

  const upcoming = published.filter((h) => hackathonState(h, today) === 'upcoming').sort(byStart)
  if (!upcoming.length) return { state: null, items: [] }

  const soonest = upcoming[0].startDate
  return { state: 'soon', items: upcoming.filter((h) => h.startDate === soonest) }
}

/** Application status pill: free entry / closed / closing-soon / open. Null when unknown or past. */
export function applicationBadge(
  h: Hackathon,
  isPast: boolean,
): { text: string; cls: string } | null {
  if (isPast) return null
  if (h.noApplication) {
    return { text: 'Ελεύθερη είσοδος, χωρίς αίτηση', cls: 'bg-[#e3ece2] text-[#356a4b]' }
  }
  const days = daysUntil(h.applicationDeadline)
  if (days === null) return null
  if (days < 0) return { text: 'Οι αιτήσεις έκλεισαν', cls: 'bg-[#f4ddd6] text-[#b3402f]' }
  if (days <= 7) {
    return {
      text: `Αιτήσεις: λήγουν ${relativeGreek(h.applicationDeadline)}`,
      cls: 'bg-[#f2e6c4] text-[#8a6a2c]',
    }
  }
  return {
    text: `Αιτήσεις έως ${dayMonth(h.applicationDeadline)}`,
    cls: 'bg-[#eaf0dd] text-[#5a7a35]',
  }
}
