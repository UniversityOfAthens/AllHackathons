import { useState, type ReactNode } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import Header from '../components/layout/Header'
import Footer from '../components/layout/Footer'
import HackathonCard from '../components/hackathons/HackathonCard'
import Pagination from '../components/hackathons/Pagination'
import { loadHackathons } from '@/lib/store'
import { compareForList, hackathonState, type HackathonState } from '@/lib/hackathons'
import { dayMonth } from '@/lib/date'
import { cn } from '@/lib/utils'
import type { Hackathon } from '@/types/hackathon'

const PAGE_SIZE = 6

type StateFilter = 'all' | HackathonState
type ModeFilter = 'all' | NonNullable<Hackathon['mode']>

const STATE_PILLS: { key: StateFilter; label: string }[] = [
  { key: 'all', label: 'Όλα' },
  { key: 'live', label: 'Live τώρα' },
  { key: 'upcoming', label: 'Προσεχή' },
  { key: 'past', label: 'Έληξαν' },
]

const MODE_PILLS: { key: ModeFilter; label: string }[] = [
  { key: 'all', label: 'Όλα' },
  { key: 'in-person', label: 'In person' },
  { key: 'online', label: 'Online' },
  { key: 'hybrid', label: 'Hybrid' },
]

const STATE_KEYS = STATE_PILLS.map((p) => p.key) as string[]
const MODE_KEYS = MODE_PILLS.map((p) => p.key) as string[]

function matchesQuery(h: Hackathon, q: string): boolean {
  const needle = q.trim().toLowerCase()
  if (!needle) return true
  const hay = [h.name, h.location, h.organizer, ...(h.tags ?? [])]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()
  return hay.includes(needle)
}

function Pill({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: ReactNode
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'cursor-pointer rounded-full px-4 py-2 text-sm font-medium transition-colors',
        active
          ? 'bg-primary text-primary-foreground'
          : 'border border-input text-foreground hover:bg-accent',
      )}
    >
      {children}
    </button>
  )
}

export default function AllHackathons() {
  const [all] = useState<Hackathon[]>(() =>
    loadHackathons().filter((h) => h.status === 'published'),
  )
  // Filters/search/page live in the URL so navigating away and back restores them.
  const [searchParams, setSearchParams] = useSearchParams()
  const query = searchParams.get('q') ?? ''
  const stateFilter = (STATE_KEYS.includes(searchParams.get('state') ?? '')
    ? searchParams.get('state')
    : 'all') as StateFilter
  const modeFilter = (MODE_KEYS.includes(searchParams.get('mode') ?? '')
    ? searchParams.get('mode')
    : 'all') as ModeFilter
  const page = Math.max(1, Number(searchParams.get('page')) || 1)

  function patch(entries: Record<string, string>) {
    const next = new URLSearchParams(searchParams)
    for (const [k, v] of Object.entries(entries)) {
      if (!v || v === 'all' || (k === 'page' && v === '1')) next.delete(k)
      else next.set(k, v)
    }
    setSearchParams(next, { replace: true })
  }

  const filtered = all
    .filter((h) => (stateFilter === 'all' ? true : hackathonState(h) === stateFilter))
    .filter((h) => (modeFilter === 'all' ? true : h.mode === modeFilter))
    .filter((h) => matchesQuery(h, query))
    .sort((a, b) => compareForList(a, b))

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const safePage = Math.min(page, pageCount)
  const pageItems = filtered.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE)

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Header />
      <main className="flex-1">
        <section className="mx-auto w-full max-w-[1140px] px-6 py-12 md:px-10">
          <Link
            to="/"
            className="text-sm text-muted-foreground underline-offset-4 transition-colors hover:text-accent-blue hover:underline"
          >
            ← Πίσω στην αρχική
          </Link>
          <h1 className="mt-4 font-serif text-4xl font-semibold text-foreground md:text-5xl">
            Όλα τα hackathons
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            {all.length} events · maintained by the community · τελευταία ενημέρωση{' '}
            {dayMonth(new Date().toISOString())}
          </p>

          {/* Search + region */}
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <div className="relative flex-1">
              <svg
                className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="11" cy="11" r="7" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <input
                value={query}
                onChange={(e) => patch({ q: e.target.value, page: '1' })}
                placeholder="Αναζήτηση: όνομα, πόλη, tech, organizer…"
                className="w-full rounded-full border border-input bg-card py-3 pl-11 pr-4 text-sm text-foreground outline-none placeholder:text-muted-foreground focus:border-accent-blue"
              />
            </div>
            <div className="inline-flex items-center gap-2 rounded-full border border-input bg-card px-4 py-3 text-sm text-foreground">
              <span aria-hidden>🌐</span> Όλη η Ελλάδα{' '}
              <span className="text-muted-foreground" aria-hidden>
                ▾
              </span>
            </div>
          </div>

          {/* Filters */}
          <div className="mt-4 flex flex-wrap items-center gap-2">
            {STATE_PILLS.map((p) => (
              <Pill
                key={p.key}
                active={stateFilter === p.key}
                onClick={() => patch({ state: p.key, page: '1' })}
              >
                {p.label}
              </Pill>
            ))}
            <span className="mx-1 hidden h-6 w-px bg-border sm:block" />
            {MODE_PILLS.map((p) => (
              <Pill
                key={p.key}
                active={modeFilter === p.key}
                onClick={() => patch({ mode: p.key, page: '1' })}
              >
                {p.label}
              </Pill>
            ))}
          </div>

          {/* Top pagination */}
          <div className="mt-8">
            <Pagination
              page={safePage}
              pageCount={pageCount}
              onPage={(p) => patch({ page: String(p) })}
            />
          </div>

          {/* Grid */}
          {pageItems.length === 0 ? (
            <div className="mt-12 py-16 text-center text-muted-foreground">
              <p className="text-lg">Δεν βρέθηκαν hackathons.</p>
              <p className="text-sm">Δοκίμασε άλλη αναζήτηση ή φίλτρο.</p>
            </div>
          ) : (
            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              {pageItems.map((h) => (
                <HackathonCard key={h.id} hackathon={h} />
              ))}
            </div>
          )}

          {/* Bottom pagination */}
          <div className="mt-10">
            <Pagination
              page={safePage}
              pageCount={pageCount}
              onPage={(p) => patch({ page: String(p) })}
            />
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
