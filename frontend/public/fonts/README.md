# Self-hosted fonts

These `.woff2` files are **generated** — do not edit by hand. They are produced by
[`../../scripts/fetch-fonts.mjs`](../../scripts/fetch-fonts.mjs), which pulls the
variable fonts from the Google Fonts API and subsets them to the character sets we
actually render (`latin`, `latin-ext`, `greek`). The matching `@font-face` rules live
in [`../../src/fonts.css`](../../src/fonts.css).

To regenerate (e.g. to add a weight axis or subset), from the `frontend/` dir:

```sh
npm run fonts
```

This file is deliberately served alongside the fonts (it ends up at `/fonts/README.md`)
so the OFL copyright notices below travel with the binaries — see *Fonts & licenses*.

## Why self-hosted

The UI copy is Greek-first. The original design fonts (Newsreader, Hanken Grotesk)
have no Greek glyphs, so they were replaced with Greek-capable variable equivalents,
and we host them ourselves rather than depend on the Google CDN at runtime
(per the PR #22 review).

## Fonts & licenses

All three are licensed under the **SIL Open Font License 1.1**, which permits
redistribution provided the copyright notice and licence travel with the font. The
notices below are reproduced verbatim from each family's `OFL.txt` in
[google/fonts](https://github.com/google/fonts).

| Family | Role | Specimen |
| --- | --- | --- |
| Literata | serif headings (roman + italic) | https://fonts.google.com/specimen/Literata |
| Manrope | body sans | https://fonts.google.com/specimen/Manrope |
| JetBrains Mono | mono labels | https://fonts.google.com/specimen/JetBrains+Mono |

```
Copyright 2017 The Literata Project Authors (https://github.com/googlefonts/literata)
Copyright 2018 The Manrope Project Authors (https://github.com/sharanda/manrope)
Copyright 2020 The JetBrains Mono Project Authors (https://github.com/JetBrains/JetBrainsMono)

This Font Software is licensed under the SIL Open Font License, Version 1.1.
Full licence text: https://openfontlicense.org
```

Only subsets of the upstream fonts are redistributed here; no glyphs were modified and
the families were not renamed, so the OFL's reserved-font-name clause is not engaged.
