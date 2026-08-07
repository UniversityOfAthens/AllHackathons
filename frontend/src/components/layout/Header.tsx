import Discord from '@/assets/icons/discord'
import { Link } from 'react-router-dom'

// Real community invite (from README). Member count / presence stays a static
// placeholder — live Discord data is deferred (see issue #12/#16).
const DISCORD_INVITE = 'https://discord.gg/zENTyrbJh'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-muted/80 backdrop-blur">
      <div className="mx-auto flex w-full max-w-[1140px] items-center justify-between gap-4 px-6 py-4 md:px-10">
        {/* Logo + community tagline */}
        <div className="flex items-baseline gap-4">
          <Link
            to="/"
            className="font-serif text-xl font-semibold tracking-tight text-foreground"
          >
            GreekHackathons
          </Link>
          <span className="hidden font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground lg:inline">
            maintained by the community
          </span>
        </div>

        {/* Right cluster: nav sits next to the Discord CTA */}
        <div className="flex items-center gap-8">
          <nav className="hidden items-center gap-7 md:flex">
            <Link
              to="/hackathons"
              className="text-sm font-medium text-foreground transition-colors hover:text-accent-blue"
            >
              Hackathons
            </Link>
            <a
              href="#submit"
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-accent-blue"
            >
              Submit a hackathon
            </a>
          </nav>

          <a
            href={DISCORD_INVITE}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-[9px] bg-discord px-4 py-2 text-sm font-semibold text-white transition-opacity hover:opacity-90"
          >
            <Discord />
            Join Discord
          </a>
        </div>
      </div>
    </header>
  )
}
