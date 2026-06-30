# Design

This folder is where we think about how the site looks **before** we build it.

The rule: **propose a design, get a nod from the team, _then_ implement.** A wireframe costs an
afternoon; a half-built page that gets thrown away costs a week. If you have an idea for a screen,
post it here and in `#webdev` first.

> **Wireframes are a reference, not a spec.** They're here to get an idea across — the layout and the
> gist of it. The exact text, colours, and spacing are suggestions, not gospel. If you're building one
> and a different choice makes the site better, make it. Match the _idea_, not the pixels.

## What goes here

- `wireframes/` — self-contained HTML mockups (open them in any browser, no build step). These are
  the editable source of a design. Static, fake data, no real logic — just the look and layout.
- `images/` — PNG exports of the wireframes, so they're easy to drop into Discord or attach to an issue.
- `homepage.html` — the original homepage design by **@alexturing** (Claude-generated). Treat it as the
  current source of truth for the visual language.

## How to propose a design

1. Make a wireframe — easiest is to copy an existing file in `wireframes/` and change it. Or just drop
   an image + a short note (which screen, what's new, what you're unsure about).
2. Export a PNG into `images/` and post it in `#webdev`.
3. Discuss and iterate here / in the thread.
4. Once people are happy, link the design from the matching GitHub issue and start building.

Don't open an implementation PR for a screen that doesn't have an agreed design yet.

## Design tokens

Pulled from `homepage.html` so new designs stay consistent. When in doubt, match these.

### Colour

| Role | Hex | Notes |
|------|-----|-------|
| Page background | `#f3efe6` | warm cream |
| Band / alt background | `#f6f2ea` | top bar, footer, callouts |
| Card surface | `#fffdf8` | off-white |
| Border (card) | `#e6dfd0` | |
| Border (divider) | `#e3dccd` | |
| Border (control) | `#d8d0bf` | filter chips, inputs |
| Text — primary | `#23211c` | |
| Text — secondary | `#5d564a` | body copy |
| Text — muted | `#9a917f` | eyebrows, captions |
| Accent — blue | `#2f5d86` | dates, links, featured card |
| Accent — terracotta | `#b9663f` | "Fun" tags, highlights |
| Accent — green | `#3f7d5a` | "reviewed" / success |
| Discord | `#5865f2` | community CTAs |
| Tag pill | bg `#efe9dc`, text `#6f6757` | |

### Type

- **Newsreader** (serif) — headings, logo, big numbers. Weights 400/500/600 (+ italic).
- **Hanken Grotesk** (sans) — body text. 400/500/600.
- **JetBrains Mono** — small uppercase eyebrow labels (letter-spacing ~`.14em`).

Patterns: eyebrow = mono 11px uppercase muted · H1 = Newsreader 500 ~50px · section H2 = Newsreader
600 ~27px · card title = Newsreader 600 ~21px · body = Hanken 15–17px / line-height 1.6 · big
date = Newsreader 600 28–34px in blue.

### Components

- **Card** — `#fffdf8`, 1px `#e6dfd0` border, radius 14–16px, padding 24–32px, faint shadow
  `0 1px 2px rgba(60,50,20,.04)`.
- **Pill tag** — radius 999px, bg `#efe9dc`, text `#6f6757`, 11px.
- **Date block** — serif day (blue) + mono month (uppercase) + tiny countdown.
- **Primary button** — bg `#23211c`, text `#f3efe6`, radius 9px, weight 600.
- **Text link** — `#2f5d86` with a `#c5d4e0` underline.
- **Dashed callout** — 1.5px dashed `#cfc6b2`, radius 16px, bg `#f6f2ea`.
- **Layout** — centered, max-width 1140px, side padding 40px.

## Current designs

| Screen | File | By | Status |
|--------|------|----|--------|
| Homepage | `homepage.html` | @alexturing | source of truth |

More screens (hackathon detail + Q&A, the low-friction submit flow, a survival-guide index) are being
drafted and discussed in `#webdev` first — they'll be added to `wireframes/` once the team is happy with them.

> The homepage shows Discord prominently (join button, member count). There is **no community yet** —
> treat those as placeholders; the real Discord integration is deferred (see the GitHub issues).
