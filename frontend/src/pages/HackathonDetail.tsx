import { useState } from 'react'
import { Link, useParams, useNavigate, useLocation } from 'react-router-dom'
import Header from '../components/layout/Header'
import Footer from '../components/layout/Footer'
import RequestChangeModal from '../components/hackathons/RequestChangeModal'
import { getHackathon } from '@/lib/store'
import { hackathonState, applicationBadge } from '@/lib/hackathons'
import { dateRangeFull, relativeGreek } from '@/lib/date'
import { cn } from '@/lib/utils'
import type { Hackathon } from '@/types/hackathon'
import { MoveLeft, MoveRight } from 'lucide-react'

const DISCORD_INVITE = 'https://discord.gg/zENTyrbJh'
const MODE_LABEL: Record<NonNullable<Hackathon['mode']>, string> = {
  'in-person': 'In person',
  online: 'Online',
  hybrid: 'Hybrid',
}

function NotFound() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Header />
      <main className="flex-1">
        <section className="mx-auto w-full max-w-[1140px] px-6 py-24 text-center md:px-10">
          <h1 className="font-serif text-3xl font-semibold text-foreground">
            Δεν βρέθηκε το hackathon
          </h1>
          <p className="mt-3 text-muted-foreground">
            Ίσως έχει αφαιρεθεί ή ο σύνδεσμος είναι λάθος.
          </p>
          <Link
            to="/hackathons"
            className="relative inline-flex items-center gap-2 text-sm font-semibold text-accent-blue transition-colors after:absolute after:inset-x-0 after:-bottom-0.5 after:h-px after:origin-left after:scale-x-0 after:bg-accent-blue after:transition-transform after:duration-300 after:ease-out hover:after:scale-x-100"
          >
            <MoveLeft/> Πίσω στη λίστα
          </Link>
        </section>
      </main>
      <Footer />
    </div>
  )
}

export default function HackathonDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const [hackathon] = useState<Hackathon | undefined>(() => (id ? getHackathon(id) : undefined))
  const [changeOpen, setChangeOpen] = useState(false)

  if (!hackathon) return <NotFound />

  const state = hackathonState(hackathon)
  const isPast = state === 'past'
  const appBadge = applicationBadge(hackathon, isPast)
  const modeLabel = hackathon.mode ? MODE_LABEL[hackathon.mode] : null

  const statePill =
    state === 'live'
      ? { text: 'Live τώρα', cls: 'bg-accent-green/15 text-accent-green' }
      : state === 'past'
        ? { text: 'Έληξε', cls: 'bg-muted text-muted-foreground' }
        : { text: relativeGreek(hackathon.startDate), cls: 'bg-accent-blue/10 text-accent-blue' }

  const metaLine = [
    hackathon.location,
    hackathon.organizer,
    hackathon.hasPrize ? hackathon.prizeDetails || 'Έπαθλο' : null,
  ]
    .filter(Boolean)
    .join(' · ')

  const details: { label: string; value: string }[] = [
    hackathon.mode ? { label: 'Τρόπος', value: MODE_LABEL[hackathon.mode] } : null,
    hackathon.location ? { label: 'Πόλη', value: hackathon.location } : null,
    hackathon.hasPrize ? { label: 'Έπαθλο', value: hackathon.prizeDetails || 'Ναι' } : null,
    hackathon.organizer ? { label: 'Διοργανωτής', value: hackathon.organizer } : null,
  ].filter(Boolean) as { label: string; value: string }[]

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Header />
      <main className="flex-1">
        <section className="mx-auto w-full max-w-[1140px] px-6 py-12 md:px-10">
          <button
            onClick={() => (location.key !== 'default' ? navigate(-1) : navigate('/hackathons'))}
            className="cursor-pointer text-sm text-muted-foreground underline-offset-4 transition-colors hover:text-accent-blue hover:underline"
          >
            ← Πίσω στη λίστα
          </button>

          <div className="mt-6 grid gap-10 md:grid-cols-[1.6fr_1fr]">
            {/* Main */}
            <div>
              <div className="flex flex-wrap items-center gap-3">
                <span className={cn('rounded-full px-3 py-1 text-xs font-medium', statePill.cls)}>
                  {statePill.text}
                </span>
                {modeLabel && (
                  <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-muted-foreground">
                    {modeLabel}
                  </span>
                )}
              </div>

              <h1 className="mt-4 font-serif text-4xl font-semibold text-foreground md:text-5xl">
                {hackathon.name}
              </h1>

              {metaLine && <p className="mt-3 text-muted-foreground">{metaLine}</p>}

              <div className="mt-2 flex flex-wrap items-center gap-x-1.5 text-sm text-muted-foreground">
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

              {appBadge && (
                <div className="mt-4">
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
                <div className="mt-4 flex flex-wrap gap-2">
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

              {hackathon.description && (
                <p className="mt-6 max-w-xl leading-relaxed text-muted-foreground">
                  {hackathon.description}
                </p>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-5">
              {/* Details */}
              <div className="rounded-2xl border border-border bg-card p-6 shadow-[0_1px_2px_rgba(60,50,20,0.04)]">
                <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
                  Στοιχεία
                </p>
                <p className="mt-4 font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
                  Ημερομηνία
                </p>
                <p className="mt-1 font-serif text-xl font-semibold text-foreground">
                  {dateRangeFull(hackathon.startDate, hackathon.endDate)}
                </p>
                <div className="my-4 h-px bg-border" />
                <dl className="space-y-2.5 text-sm">
                  {details.map((d) => (
                    <div key={d.label} className="flex items-center justify-between gap-4">
                      <dt className="text-muted-foreground">{d.label}</dt>
                      <dd className="text-right font-medium text-foreground">{d.value}</dd>
                    </div>
                  ))}
                </dl>
                {hackathon.url && (
                  <a
                    href={hackathon.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="relative mt-5 flex items-center justify-center gap-2 rounded-[10px] bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground transition-opacity after:absolute after:inset-x-0 after:-bottom-0.5 after:h-px after:origin-left after:scale-x-0 after:bg-accent-blue after:transition-transform after:duration-300 after:ease-out hover:opacity-90 hover:after:scale-x-100"
                  >
                    Επίσημη σελίδα <MoveRight className="size-4" />
                  </a>
                )}
              </div>

              {/* Report an issue */}
              <div className="rounded-2xl border border-border bg-card p-6">
                <h2 className="font-serif text-lg font-semibold text-foreground">
                  Βλέπεις κάτι λάθος;
                </h2>
                <p className="mt-2 text-sm text-muted-foreground">
                  Οτιδήποτε: στοιχεία του event ή κάποια απάντηση στις ερωτήσεις. Πες μας
                  τι πρέπει να αλλάξει, με δικά σου λόγια.
                </p>
                <button
                  onClick={() => setChangeOpen(true)}
                  className="mt-4 inline-flex cursor-pointer items-center gap-2 rounded-[10px] border border-input px-4 py-2.5 text-sm font-medium text-foreground transition-colors hover:bg-accent"
                >
                  ✎ Πρότεινε διόρθωση
                </button>
              </div>
            </div>
          </div>

          {/* Q&A */}
          <div className="mt-16">
            <h2 className="font-serif text-3xl font-semibold text-foreground">Συχνές ερωτήσεις</h2>

            {hackathon.faq && hackathon.faq.length > 0 ? (
              <>
                <div className="mt-6 space-y-4">
                  {hackathon.faq.map((item, i) => (
                    <div key={i} className="rounded-2xl border border-border bg-card p-6">
                      <h3 className="font-serif text-lg font-semibold text-foreground">{item.q}</h3>
                      {item.a && <p className="mt-2 text-muted-foreground">{item.a}</p>}
                    </div>
                  ))}
                </div>
                <p className="mt-5 text-sm text-muted-foreground">
                  Άλλη ερώτηση;{' '}
                  <a
                    href={DISCORD_INVITE}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-accent-blue underline-offset-4 hover:underline"
                  >
                    Ρώτα την κοινότητα στο Discord →
                  </a>
                </p>
              </>
            ) : (
              <div className="mt-6 rounded-2xl border-2 border-dashed border-[#cfc6b2] px-6 py-12 text-center">
                <p className="font-serif text-xl font-semibold text-foreground">
                  Δεν υπάρχουν ακόμα ερωτήσεις εδώ
                </p>
                <p className="mx-auto mt-2 max-w-md text-sm text-muted-foreground">
                  Έχεις κάποια απορία για αυτό το hackathon; Ρώτα στο Discord. Η κοινότητα
                  και οι διοργανωτές απαντούν συνήθως γρήγορα.
                </p>
                <a
                  href={DISCORD_INVITE}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-5 inline-flex items-center gap-2 rounded-[10px] bg-discord px-4 py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90"
                >
                  <span className="size-2 rounded-full bg-green-400" aria-hidden />
                  Ρώτα στο Discord
                </a>
              </div>
            )}
          </div>
        </section>
      </main>
      <Footer />
      <RequestChangeModal
        open={changeOpen}
        onOpenChange={setChangeOpen}
        hackathonName={hackathon.name}
      />
    </div>
  )
}
