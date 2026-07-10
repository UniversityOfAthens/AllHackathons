// Deterministic avatars from a name/handle — no accounts, no stored images.
// The picture is DERIVED from the string, so nothing is fetched or persisted.
// (Future: if the Discord bot lands (#16), real Discord avatars can override this.)

const AVATAR_COLORS = [
  '#2f5d86', // blue
  '#b9663f', // terracotta
  '#3f7d5a', // green
  '#9a7b3f', // ochre
  '#5865f2', // discord indigo
  '#b3402f', // rust
  '#5d564a', // taupe
]

function hash(str: string): number {
  let h = 0
  for (let i = 0; i < str.length; i++) {
    h = (h * 31 + str.charCodeAt(i)) | 0
  }
  return Math.abs(h)
}

/** Stable background colour picked from the palette by hashing the seed. */
export function avatarColor(seed: string): string {
  return AVATAR_COLORS[hash(seed) % AVATAR_COLORS.length]
}

/** 1–2 letter initials from a handle/name (leading "@" ignored). */
export function initials(name: string): string {
  const clean = name.replace(/^@/, '').trim()
  if (!clean) return '?'
  const parts = clean.split(/[\s_.-]+/).filter(Boolean)
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
}
