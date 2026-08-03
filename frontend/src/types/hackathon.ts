export interface Hackathon {
  id: string
  name: string
  description?: string
  url?: string
  startDate?: string
  endDate?: string
  location?: string
  mode?: "in-person" | "online" | "hybrid"
  organizer?: string
  hasPrize?: boolean
  prizeDetails?: string
  tags?: string[]
  status: "draft" | "pending" | "published" | "needs-changes"
  submittedAt?: string
  updatedAt?: string
  // Proposed (frontend, pending data-model ratification — see the #3 avatar note):
  // optional self-provided submitter display name. No accounts/auth; avatars are
  // generated from this string, never uploaded or stored as images.
  submittedByName?: string
  // Proposed (frontend, pending ratification): application/registration deadline (ISO 8601 date).
  applicationDeadline?: string
  // Proposed (frontend): true when entry is free/open with no application to submit.
  noApplication?: boolean
  // Proposed (frontend, placeholder for Q&A which is owned by #17): curated FAQ entries.
  faq?: { q: string; a?: string }[]
  interestCount?: number
  discordChannelId?: string
}
