import type { Hackathon } from '@/types/hackathon';

// My submissions tracker only — modeled on Feedback.tsx Previous Submissions (issue #7).
// Public list is fetched via api.ts (GET /api/hackathons); localStorage MUST NOT back it.
const MY_SUBMISSIONS_KEY = 'allhackathons_my_submissions';

export type MySubmission = Pick<Hackathon, 'id' | 'name' | 'url' | 'status'> & {
  submittedAt: string;
};

export function loadMySubmissions(): MySubmission[] {
  try {
    const raw = localStorage.getItem(MY_SUBMISSIONS_KEY);
    return raw ? (JSON.parse(raw) as MySubmission[]) : [];
  } catch {
    return [];
  }
}

export function addMySubmission(h: Hackathon): void {
  const list = loadMySubmissions();
  const entry: MySubmission = {
    id: h.id,
    name: h.name,
    url: h.url,
    status: h.status,
    submittedAt: new Date().toISOString(),
  };
  localStorage.setItem(MY_SUBMISSIONS_KEY, JSON.stringify([entry, ...list]));
}

export function clearMySubmissions(): void {
  localStorage.removeItem(MY_SUBMISSIONS_KEY);
}
