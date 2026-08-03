const DISCORD_INVITE = 'https://discord.gg/zENTyrbJh'
const REPO_URL = 'https://github.com/UniversityOfAthens/AllHackathons'

export default function Footer() {
  return (
    <footer className="mt-auto border-t border-border bg-muted/50">
      <div className="mx-auto flex w-full max-w-[1140px] flex-col items-center justify-between gap-3 px-6 py-6 text-sm sm:flex-row md:px-10">
        <span className="font-serif text-base font-semibold text-foreground">GreekHackathons</span>
        <p className="flex flex-wrap items-center justify-center gap-x-2 gap-y-1 text-muted-foreground">
          <span>Φτιαγμένο από την κοινότητα, για την κοινότητα</span>
          <span aria-hidden>·</span>
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="underline-offset-4 transition-colors hover:text-foreground hover:underline"
          >
            Open source
          </a>
          <span aria-hidden>·</span>
          <a
            href={DISCORD_INVITE}
            target="_blank"
            rel="noopener noreferrer"
            className="underline-offset-4 transition-colors hover:text-foreground hover:underline"
          >
            Discord
          </a>
        </p>
      </div>
    </footer>
  )
}
