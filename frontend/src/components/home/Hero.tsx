import { Link } from 'react-router-dom'
import type { Hackathon } from '@/types/hackathon'
import { dayMonth } from '@/lib/date'
import Avatar from '@/components/common/Avatar'
import { MoveRight } from 'lucide-react'

const DISCORD_INVITE = 'https://discord.gg/zENTyrbJh'

function isUpcoming(h: Hackathon, today: string) {
  const d = h.endDate || h.startDate
  return d ? d >= today : true
}

export default function Hero({ hackathons }: { hackathons: Hackathon[] }) {
  const today = new Date().toISOString().slice(0, 10)
  const active = hackathons.filter((h) => h.status === 'published' && isUpcoming(h, today))
  const openApplications = hackathons.filter(
    (h) => h.status === 'published' && !!h.applicationDeadline && h.applicationDeadline >= today,
  ).length

  // Contributors = distinct people who added a hackathon (generated avatars, no accounts).
  const submitters = Array.from(
    new Set(hackathons.map((h) => h.submittedByName).filter((n): n is string => !!n)),
  )
  const shownSubmitters = submitters.slice(0, 6)
  const extraSubmitters = submitters.length - shownSubmitters.length

  const stats: { value: string; label: string }[] = [
    { value: String(active.length), label: 'ενεργά hackathons' },
    { value: String(openApplications), label: 'ανοιχτές αιτήσεις' },
    { value: '0', label: 'μέλη στο Discord' }, // no community yet — live Discord data deferred
    { value: dayMonth(today), label: 'τελευταία ενημέρωση' },
  ]

  return (
    <section className="border-b border-border">
      <div className="mx-auto grid w-full max-w-[1140px] items-center gap-12 px-6 py-16 md:grid-cols-[1.4fr_1fr] md:gap-28 md:px-10 md:py-20 lg:gap-40">
        {/* Pitch */}
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-accent-blue/80">
            Ένα μέρος για όλα
          </p>
          <h1 className="mt-5 font-serif text-3xl font-medium leading-[1.08] text-foreground md:text-5xl">
            Κάθε hackathon στην Ελλάδα, σε μία λίστα.
          </h1>
          <p className="mt-6 max-w-xl text-base leading-relaxed text-muted-foreground">
            Φτιαγμένη και ενημερωμένη από κόσμο που πάει σε hackathons, όχι από
            αλγόριθμο. Βρες το επόμενό σου hackathon, μπες στο Discord, και αν λείπει
            κάτι, πρόσθεσέ το.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-5">
            <Link
              to="/hackathons"
              className="inline-flex items-center rounded-[10px] bg-primary px-7 py-3.5 text-base font-semibold text-primary-foreground transition-opacity hover:opacity-90"
            >
              Δες τα hackathons
            </Link>
            <a
              href={DISCORD_INVITE}
              target="_blank"
              rel="noopener noreferrer"
              className="relative inline-flex items-center gap-2 text-base font-semibold text-accent-blue transition-colors after:absolute after:inset-x-0 after:-bottom-0.5 after:h-px after:origin-left after:scale-x-0 after:bg-accent-blue after:transition-transform after:duration-300 after:ease-out hover:after:scale-x-100"
            >
              ή μπες στην κοινότητα <span><MoveRight /></span>
            </a>
          </div>
        </div>

        {/* Stats card */}
        <div className="rounded-3xl border border-border bg-card p-7 shadow-[0_1px_2px_rgba(60,50,20,0.05)]">
          {submitters.length > 0 && (
            <div className="flex items-center gap-3">
              <div className="flex -space-x-2">
                {shownSubmitters.map((name) => (
                  <Avatar key={name} name={name} className="size-8 border-2 border-card text-[10px]" />
                ))}
              </div>
              {extraSubmitters > 0 && (
                <span className="text-sm text-muted-foreground">+ {extraSubmitters} ακόμη</span>
              )}
            </div>
          )}
          <dl className={`grid grid-cols-2 gap-x-6 gap-y-6 ${submitters.length > 0 ? 'mt-6' : ''}`}>
            {stats.map((s) => (
              <div key={s.label}>
                <dd className="font-serif text-3xl font-semibold text-foreground">{s.value}</dd>
                <dt className="mt-1 text-sm text-muted-foreground">{s.label}</dt>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </section>
  )
}
