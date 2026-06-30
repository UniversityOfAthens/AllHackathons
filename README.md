# AllHackathons

**A community-maintained list of hackathons — starting with Greece — that anyone can add to.**

Find your next hackathon, see what's coming up, and if one's missing, submit it in seconds (a link is enough). Built and kept current by people who actually go to hackathons, not an algorithm.

> The site UI is **Greek-first** — that's our audience. This README is in English for anyone landing on the repo from outside.

> 🚧 **Early days.** This is being built in the open, mostly by students at the University of Athens. There's plenty to grab — see [Contributing](#contributing), and come say hi on our [Discord](https://discord.gg/zENTyrbJh).

## What it is

- A browsable list of **upcoming (and past) hackathons** — date, location, mode (in-person / online / hybrid), prize, tags, and a link to the official page.
- **Anyone can add a hackathon** with as little as a URL. The team (and a Claude-API check) fills in and verifies the rest, so good submissions go live without friction.
- **Detail pages with a no-login Q&A** — ask the things the official site never makes clear.
- A **survival guide** — the practical stuff you only learn after a few of these (including what to eat at 3am).

## Tech stack

- **Frontend** — React 19 · TypeScript · Vite · Tailwind CSS v4 · shadcn/ui · React Router
- **Backend** — Python · Flask (REST API)
- **AI** — Anthropic Claude API to validate/normalize submissions so they can auto-publish *(planned — see [#11](../../issues/11))*

## Repository layout

```
frontend/                 React + Vite app
  src/
    components/           UI components  (ui/ = shadcn primitives)
    pages/                Home, Feedback  (more to come)
    lib/                  types, sample data, helpers
backend/                  Flask API  (a stub today — real API in #5)
  main.py
  requirements.txt
design/                   design-first workspace: wireframes + design tokens
```

## Getting started

Two terminals — one for the frontend, one for the backend.

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

The backend is currently a stub (`/health`, `/ping`); the real hackathon API is tracked in [#5](../../issues/5).

## Contributing

A student community project — **contributors welcome**, especially from UoA. The short version:

1. **Pick something** from the [issues](../../issues). They're in dependency order, each with a `Depends on: #…` note, so start with one whose dependencies are done. New here? Look for [`good first issue`](../../labels/good%20first%20issue).
2. **Design before you build (UI).** Check the [`design/`](design) folder. Changing how a screen looks? Sketch a wireframe and float it in Discord `#webdev` first — designs there are a *reference for the idea, not a pixel-perfect spec*.
3. **Fork → branch → PR.** Most contributors won't have push access: fork, work on a branch, open a pull request. Keep each PR focused on one issue.
4. **Match what's there** — the existing TypeScript / Tailwind / shadcn patterns on the frontend, and the [API contract (#2)](../../issues/2) for data shapes.

Full guide in **[CONTRIBUTING.md](CONTRIBUTING.md)**. Questions? Join our **[Discord](https://discord.gg/zENTyrbJh)** and chat in `#hackathons` or `#webdev`.

## Roadmap

The build-out lives in issues [#2–#18](../../issues), grouped into waves: data model & API → backend & submit → frontend, review & AI → detail & search → Q&A & SEO. Discord integration (interest counts, a review bot) is intentionally **deferred** until there's a community server.

## License

Open source — MIT intended. A `LICENSE` file is on the to-do list ([#4](../../issues/4)).
