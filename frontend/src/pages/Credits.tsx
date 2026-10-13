import { Link } from 'react-router-dom';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import GitHubAvatar from '@/components/common/GitHubAvatar';
import { HomeBreadcrumb } from '@/components/common/Breadcrumbs';
import Discord from '@/assets/icons/discord';
import { contributors } from '@/data/contributors';
import { MoveRight } from 'lucide-react';

const DISCORD_INVITE = 'https://discord.gg/zENTyrbJh';
const REPO_URL = 'https://github.com/UniversityOfAthens/AllHackathons';

export default function Credits() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Header />
      <main className="flex-1">
        <section className="mx-auto w-full max-w-[1140px] px-6 py-12 md:px-10">
          <HomeBreadcrumb />

          <h1 className="mt-4 font-serif text-4xl font-semibold text-foreground md:text-5xl">
            Συντελεστές
          </h1>
          <p className="mt-3 max-w-2xl leading-relaxed text-muted-foreground">
            Το AllHackathons είναι ένα open source έργο — φτιαγμένο και συντηρούμενο από την
            κοινότητα, για την κοινότητα. Όποιος θέλει να βοηθήσει, είναι ευπρόσδεκτος.
          </p>

          {/* Contributors */}
          <div className="mt-14 flex flex-wrap gap-3">
            {contributors.map((handle) => (
              <a
                key={handle}
                href={`https://github.com/${handle}`}
                target="_blank"
                rel="noopener noreferrer"
                className="group inline-flex items-center gap-3 rounded-full border border-border bg-card py-2 pl-2 pr-5 shadow-[0_1px_2px_rgba(60,50,20,0.04)] transition-colors hover:border-accent-blue/40"
              >
                <GitHubAvatar handle={handle} className="size-9" />
                <span className="font-mono text-sm text-foreground">{handle}</span>
              </a>
            ))}
          </div>

          {/* How to help */}
          <div className="mt-16">
            <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
              Θέλεις να βοηθήσεις;
            </p>
            <h2 className="mt-3 font-serif text-2xl font-semibold text-foreground md:text-3xl">
              Ένα repo, πολλοί τρόποι
            </h2>
            <p className="mt-3 max-w-2xl leading-relaxed text-muted-foreground">
              Δεν χρειάζεται να ξέρεις να γράφεις κώδικα. Ένα λάθος που αναφέρεις, ένα hackathon που
              προσθέτεις, μια μετάφραση — μετράνε.
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-3">
              <a
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex flex-col rounded-2xl border border-border bg-card p-6 transition-colors hover:border-accent-blue/40"
              >
                <p className="font-serif text-lg font-semibold text-foreground">GitHub</p>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  Κώδικας, issues και pull requests. Ξεκίνα από ένα issue με label
                  <span className="whitespace-nowrap"> good first issue</span>.
                </p>
                <span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-accent-blue">
                  Άνοιξε το repo <MoveRight className="size-4" />
                </span>
              </a>

              <a
                href={DISCORD_INVITE}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex flex-col rounded-2xl border border-border bg-card p-6 transition-colors hover:border-discord/40"
              >
                <p className="font-serif text-lg font-semibold text-foreground">Discord</p>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  Ερωτήσεις, ιδέες, συντονισμός. Εκεί συνήθως κάθεται κάποιος από την ομάδα.
                </p>
                <span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-discord">
                  <Discord /> Μπες στο Discord
                </span>
              </a>

              <Link
                to="/feedback"
                className="group flex flex-col rounded-2xl border border-border bg-card p-6 transition-colors hover:border-accent-blue/40"
              >
                <p className="font-serif text-lg font-semibold text-foreground">Feedback</p>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  Βρήκες bug ή έχεις ιδέα; Πες το μας — η σελίδα κρατάει τις καταγραφές στο browser
                  σου.
                </p>
                <span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-accent-blue">
                  Στείλε feedback <MoveRight className="size-4" />
                </span>
              </Link>
            </div>
          </div>

          {/* Credits / attribution */}
          <div className="mt-16 border-t border-border pt-10">
            <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
              Ευχαριστίες
            </p>
            <p className="mt-3 max-w-2xl leading-relaxed text-muted-foreground">
              Το εικονίδιο της Discord στο footer προέρχεται από το{' '}
              <span className="text-foreground">Discord brand mark</span> και διατίθεται υπό την
              άδεια MIT. Λεπτομέρειες στο{' '}
              <a
                href={`${REPO_URL}/blob/main/CREDITS.txt`}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded bg-muted px-1.5 py-0.5 font-mono text-[0.85em] text-foreground underline-offset-4 hover:underline"
              >
                CREDITS.txt
              </a>{' '}
              στο repository.
            </p>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}
