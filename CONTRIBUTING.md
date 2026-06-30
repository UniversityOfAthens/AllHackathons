# Contributing to AllHackathons

Thanks for wanting to help. This is a community project — built mostly by University of Athens
students — and it only works if it's easy to jump in. Here's how.

**First stop:** join our [Discord](https://discord.gg/zENTyrbJh) and say hi in `#hackathons` or `#webdev`.
That's where we coordinate who's working on what.

## Ways to contribute

- **Build a feature** from the issues.
- **Add or fix a hackathon** — you can do that on the site itself, no code needed.
- **Propose a design** (see [Design-first](#design-first) below).
- **Write a survival-guide entry.**
- **Report a bug or suggest an idea** by opening an issue.

## Finding something to work on

- The [issue tracker](../../issues) is the backlog. Issues are written in **dependency order** —
  each lists `Depends on: #…`. Pick one whose dependencies are already done.
- Brand new to the project? Filter for [`good first issue`](../../labels/good%20first%20issue).
- The foundation issue is [#2 — the data model + API contract](../../issues/2). It's the source of
  truth for data shapes; skim it before touching frontend or backend data code.
- **Comment on an issue to claim it** so two people don't build the same thing.

## Design-first

We sketch a screen before building it — a wireframe costs an afternoon, a rebuilt page costs a week.

- Look in [`design/`](design): the homepage design plus the design tokens (palette, fonts,
  components) in [`design/README.md`](design/README.md).
- New screen or a redesign? Make a quick wireframe (copy an existing one in `design/wireframes/`)
  and post it in Discord `#webdev` to get a nod **before** you start coding.
- Wireframes are a **reference for the idea, not a strict spec** — change text, colours, and spacing
  where it makes the site better.

## Dev setup

**Frontend**
```bash
cd frontend
bun install        # or: npm install
bun run dev        # or: npm run dev   →  http://localhost:5173
```

**Backend**
```bash
cd backend
pip install -r requirements.txt
flask --app main run        #  →  http://localhost:5000
```

## Workflow

1. **Fork** the repo (most contributors aren't collaborators).
2. Create a branch: `git checkout -b feature/short-name`.
3. Make your change — keep it scoped to one issue.
4. Match the existing style: TypeScript + Tailwind + shadcn on the frontend, small components, and the
   [API contract (#2)](../../issues/2) for data shapes.
5. Open a **pull request** against `main` and reference the issue (e.g. `Closes #13`). A maintainer
   reviews and merges.

## Commit & PR style

- Small, focused PRs beat big ones.
- Imperative commit messages: *"Add hackathon detail page"*, not *"added stuff"*.
- **Greek-first** for user-facing copy; **English** for code, comments, and docs.

## Good to know

- **No accounts** on the site, by design — submissions and the "my submissions" list live in the
  browser. Keep that constraint in mind.
- **Discord integration** (interest counts, review bot) is **deferred** until there's a server —
  don't build against it yet.
- Keep friction low for everyone: both people submitting a hackathon and people contributing code.

## Communication

- Day-to-day: our [Discord](https://discord.gg/zENTyrbJh) — `#hackathons` or `#webdev`.
- Decisions worth keeping: write them on the relevant issue.
