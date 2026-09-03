export interface Hackathon {
  id: string; // backend/database.py:37 is Integer autoincrement; frontend/src/lib/api.ts maps number -> string to match docs/API.md:9
  name: string;
  description?: string;
  url?: string;
  startDate?: string; // ISO 8601, backend/database.py:41-42 DateTime -> to_dict:114 isoformat
  endDate?: string;
  location?: string;
  // backend/database.py:30-31 stores "in_person" (ModeEnum.in_person) while UI/docs/API.md:16 uses "in-person"; api.ts normalizes to this union
  mode?: 'in-person' | 'online' | 'hybrid';
  organizer?: string;
  hasPrize?: boolean;
  prizeDetails?: string;
  // backend/database.py:48 is String(200) CSV (to_dict:121), frontend uses string[]; api.ts splits/joins
  tags?: string[];
  // backend/database.py:24-28 stores "needs_changes" (underscore) vs docs/API.md:21 / UI "needs-changes" (hyphen); api.ts normalizes to hyphen
  status: 'draft' | 'pending' | 'published' | 'needs-changes';
  submittedAt?: string;
  updatedAt?: string;
  // Proposed (frontend, pending data-model ratification — see the #3 avatar note):
  // optional self-provided submitter display name. No accounts/auth; avatars are
  // generated from this string, never uploaded or stored as images.
  submittedByName?: string;
  // Proposed (frontend, pending ratification): application/registration deadline (ISO 8601 date).
  applicationDeadline?: string;
  // Proposed (frontend): true when entry is free/open with no application to submit.
  noApplication?: boolean;
  // Proposed (frontend, placeholder for Q&A which is owned by #17): curated FAQ entries.
  faq?: { q: string; a?: string }[];
  interestCount?: number;
  discordChannelId?: string;
}
