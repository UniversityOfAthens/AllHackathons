// Greek date helpers for the homepage (date-block cards, countdowns, "last updated").

const MONTHS_SHORT = [
  'Ιαν', 'Φεβ', 'Μαρ', 'Απρ', 'Μάι', 'Ιουν',
  'Ιουλ', 'Αυγ', 'Σεπ', 'Οκτ', 'Νοε', 'Δεκ',
]

function parse(dateStr?: string): Date | null {
  if (!dateStr) return null
  const d = new Date(dateStr)
  return Number.isNaN(d.getTime()) ? null : d
}

/** Day of month, e.g. "30". */
export function dayOf(dateStr?: string): string {
  const d = parse(dateStr)
  return d ? String(d.getDate()) : ''
}

/** Short Greek month, e.g. "Ιουλ". */
export function monthShort(dateStr?: string): string {
  const d = parse(dateStr)
  return d ? MONTHS_SHORT[d.getMonth()] : ''
}

/** Uppercase Greek month for date blocks, e.g. "ΙΟΥΛ". */
export function monthUpper(dateStr?: string): string {
  return monthShort(dateStr).toUpperCase()
}

/** "18 Ιουλ" style. */
export function dayMonth(dateStr?: string): string {
  const d = parse(dateStr)
  return d ? `${d.getDate()} ${MONTHS_SHORT[d.getMonth()]}` : ''
}

/** Relative countdown in Greek, e.g. "σε 3 εβδ." / "σε 2 μήνες". */
export function relativeGreek(dateStr?: string, from: Date = new Date()): string {
  const d = parse(dateStr)
  if (!d) return ''
  const start = new Date(from.getFullYear(), from.getMonth(), from.getDate())
  const days = Math.round((d.getTime() - start.getTime()) / 86_400_000)
  if (days < 0) return 'πέρασε'
  if (days === 0) return 'σήμερα'
  if (days === 1) return 'αύριο'
  if (days < 14) return `σε ${days} μέρες`
  if (days < 60) return `σε ${Math.round(days / 7)} εβδ.`
  return `σε ${Math.round(days / 30)} μήνες`
}

/** Day range within a hackathon, e.g. "26-27" or "30 Σεπ – 2 Οκτ". Empty if single-day. */
export function dayRange(start?: string, end?: string): string {
  if (!start || !end || end === start) return ''
  const s = new Date(start)
  const e = new Date(end)
  if (Number.isNaN(s.getTime()) || Number.isNaN(e.getTime())) return ''
  if (s.getMonth() === e.getMonth()) return `${s.getDate()}-${e.getDate()}`
  return `${s.getDate()} ${MONTHS_SHORT[s.getMonth()]} – ${e.getDate()} ${MONTHS_SHORT[e.getMonth()]}`
}

/** Whole days from today until `dateStr` (negative if already past). Null if unparseable. */
export function daysUntil(dateStr?: string, from: Date = new Date()): number | null {
  const d = parse(dateStr)
  if (!d) return null
  const start = new Date(from.getFullYear(), from.getMonth(), from.getDate())
  return Math.round((d.getTime() - start.getTime()) / 86_400_000)
}

/** Full date range with year, e.g. "16–18 Ιουλ 2026" / "5 Δεκ 2026". */
export function dateRangeFull(start?: string, end?: string): string {
  const s = parse(start)
  if (!s) return ''
  const e = parse(end)
  if (!e || end === start) return `${s.getDate()} ${MONTHS_SHORT[s.getMonth()]} ${s.getFullYear()}`
  if (s.getMonth() === e.getMonth() && s.getFullYear() === e.getFullYear()) {
    return `${s.getDate()}–${e.getDate()} ${MONTHS_SHORT[s.getMonth()]} ${s.getFullYear()}`
  }
  return `${s.getDate()} ${MONTHS_SHORT[s.getMonth()]} – ${e.getDate()} ${MONTHS_SHORT[e.getMonth()]} ${e.getFullYear()}`
}
