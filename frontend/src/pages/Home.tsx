import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Header from '../components/layout/Header'
import Footer from '../components/layout/Footer'
import Hero from '../components/home/Hero'
import Highlights from '../components/home/Highlights'
import HackathonCard from '../components/hackathons/HackathonCard'
import HackathonFilters, { type ModeFilter } from '../components/hackathons/HackathonFilters'
import SubmitHackathonModal from '../components/hackathons/SubmitHackathonModal'
import { loadHackathons, saveUserHackathons } from '@/lib/store'
import { compareForList, highlightSelection } from '@/lib/hackathons'
import type { Hackathon } from '@/types/hackathon'

// The homepage shows a teaser of the list; the full paginated list lives at /hackathons.
const HOME_LIST_LIMIT = 6

export default function Home() {
  const [hackathons, setHackathons] = useState<Hackathon[]>(loadHackathons)
  const [modalOpen, setModalOpen] = useState(false)
  const [modeFilter, setModeFilter] = useState<ModeFilter>('all')

  useEffect(() => {
    saveUserHackathons(hackathons)
  }, [hackathons])

  function addHackathon(h: Hackathon) {
    setHackathons((prev) => [h, ...prev])
  }

  // Whatever the highlight already spotlights is excluded from the list below,
  // so a hackathon never appears twice.
  const highlightedIds = new Set(highlightSelection(hackathons).items.map((h) => h.id))

  // Published items: live → upcoming (soonest first) → past (most recent first).
  const visible = hackathons
    .filter((h) => h.status === 'published')
    .filter((h) => !highlightedIds.has(h.id))
    .filter((h) => (modeFilter === 'all' ? true : h.mode === modeFilter))
    .sort((a, b) => compareForList(a, b))

  const teaser = visible.slice(0, HOME_LIST_LIMIT)

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Header />
      <main className="flex-1">
        <Hero hackathons={hackathons} />

        {/* Highlight: live now (green) if any, else coming soon (blue) */}
        <Highlights hackathons={hackathons} />

        {/* Full list (teaser) */}
        <section id="list" className="mx-auto w-full max-w-[1140px] px-6 py-16 md:px-10">
          <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
            <div>
              <h2 className="font-serif text-2xl font-semibold text-foreground md:text-3xl">
                Όλα τα hackathons
              </h2>
              <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted-foreground">
                <span className="flex items-center gap-1.5">
                  <span className="size-2 rounded-full bg-green-500" />
                  Live τώρα
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="size-2 rounded-full bg-accent-blue" />
                  Προσεχή
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="size-2 rounded-full bg-muted-foreground/50" />
                  Έληξαν
                </span>
              </div>
            </div>
            <HackathonFilters mode={modeFilter} onModeChange={setModeFilter} />
          </div>

          {teaser.length === 0 ? (
            <div className="mt-12 flex flex-col items-center justify-center py-16 text-center text-muted-foreground">
              <p className="text-lg">Δεν βρέθηκαν hackathons.</p>
              <p className="text-sm">Δοκίμασε άλλο φίλτρο ή πρόσθεσε το πρώτο.</p>
            </div>
          ) : (
            <>
              <div className="mt-8 grid gap-4 sm:grid-cols-2">
                {teaser.map((h) => (
                  <HackathonCard key={h.id} hackathon={h} />
                ))}
              </div>
              <div className="mt-10 text-center">
                <Link
                  to="/hackathons"
                  className="text-sm font-semibold text-accent-blue underline-offset-4 hover:underline"
                >
                  Δες περισσότερα →
                </Link>
              </div>
            </>
          )}
        </section>

        {/* Submit band — low-friction dashed callout (owns the add modal trigger) */}
        <section id="submit" className="mx-auto w-full max-w-[1140px] px-6 pb-20 md:px-10">
          <div className="rounded-3xl border-2 border-dashed border-[#cfc6b2] bg-muted/60 px-8 py-12 text-center">
            <h2 className="font-serif text-2xl font-semibold text-foreground md:text-3xl">
              Λείπει κάποιο hackathon;
            </h2>
            <p className="mx-auto mt-3 max-w-md text-muted-foreground">
              Δεν χρειάζεται να το διοργανώνεις, ένα link αρκεί. Πρόσθεσέ το και το
              συμπληρώνουμε εμείς.
            </p>
            <button
              onClick={() => setModalOpen(true)}
              className="mt-7 inline-flex cursor-pointer items-center rounded-[10px] bg-primary px-7 py-3.5 text-base font-semibold text-primary-foreground transition-opacity hover:opacity-90"
            >
              Πρόσθεσε hackathon
            </button>
          </div>
        </section>
      </main>
      <Footer />
      <SubmitHackathonModal
        open={modalOpen}
        onOpenChange={setModalOpen}
        onSubmit={addHackathon}
      />
    </div>
  )
}
