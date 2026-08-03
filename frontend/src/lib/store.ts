import { sampleHackathons } from '@/mocks/sample-hackathons'
import type { Hackathon } from '@/types/hackathon'

// Browser-local store (no backend yet — the real API is issue #5/#7).
// User-submitted hackathons live in localStorage and are merged ahead of the seed samples.
const USER_KEY = 'allhackathons_user'

export function loadHackathons(): Hackathon[] {
  try {
    const raw = localStorage.getItem(USER_KEY)
    const user: Hackathon[] = raw ? JSON.parse(raw) : []
    return [...user, ...sampleHackathons]
  } catch {
    return [...sampleHackathons]
  }
}

export function saveUserHackathons(all: Hackathon[]) {
  const user = all.filter((h) => !sampleHackathons.some((s) => s.id === h.id))
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function getHackathon(id: string): Hackathon | undefined {
  return loadHackathons().find((h) => h.id === id)
}
