import type { Hackathon } from '@/types/hackathon';
import { sampleHackathons } from '@/mocks/sample-hackathons';

// Base URL via Vite env var, not hardcoded (issue #7). Supports VITE_API_BASE_URL per spec,
// falls back to VITE_API_URL and then to relative /api (proxied to localhost:5000 in dev).
const API_BASE =
  (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, '') ??
  (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, '') ??
  '';

function normalizeMode(mode?: string | null): Hackathon['mode'] | undefined {
  if (!mode) return undefined;
  if (mode === 'in_person' || mode === 'in-person') return 'in-person';
  if (mode === 'online' || mode === 'hybrid') return mode as Hackathon['mode'];
  return undefined;
}

function normalizeTags(tags?: string | string[] | null): string[] | undefined {
  if (!tags) return undefined;
  if (Array.isArray(tags)) return tags.filter(Boolean);
  const str = tags.trim();
  if (!str) return undefined;
  return str
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean);
}

function normalizeStatus(status?: string | null): Hackathon['status'] {
  if (status === 'needs_changes') return 'needs-changes';
  if (
    status === 'draft' ||
    status === 'pending' ||
    status === 'published' ||
    status === 'needs-changes'
  ) {
    return status;
  }
  return 'published';
}

export function mapBackendToFrontend(raw: Record<string, unknown>): Hackathon {
  return {
    id: String(raw['id']),
    name: raw['name'] as string,
    description: (raw['description'] as string) || undefined,
    url: (raw['url'] as string) || undefined,
    startDate: (raw['startDate'] as string)?.slice(0, 10) || undefined,
    endDate: (raw['endDate'] as string)?.slice(0, 10) || undefined,
    location: (raw['location'] as string) || undefined,
    mode: normalizeMode(raw['mode'] as string | null),
    organizer: (raw['organizer'] as string) || undefined,
    hasPrize: (raw['hasPrize'] as boolean) ?? undefined,
    prizeDetails: (raw['prizeDetails'] as string) || undefined,
    tags: normalizeTags(raw['tags'] as string | string[] | null),
    status: normalizeStatus(raw['status'] as string | null),
    submittedAt: (raw['submittedAt'] as string) || undefined,
    updatedAt: (raw['updatedAt'] as string) || undefined,
    interestCount: (raw['interestCount'] as number) ?? undefined,
  };
}

function toApiDate(date?: string): string | undefined {
  if (!date) return undefined;
  const trimmed = date.trim();
  if (!trimmed) return undefined;
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) return `${trimmed} 00:00:00`;
  return trimmed;
}

function toBackendMode(mode?: string): string | undefined {
  if (!mode) return undefined;
  if (mode === 'in-person') return 'in_person';
  return mode;
}

function buildUrl(path: string): string {
  if (!API_BASE || API_BASE === 'mock') return path;
  return `${API_BASE}${path}`;
}

// Mock handler reusing sample-hackathons.ts as seed fixtures (issue #7) when VITE_API_BASE_URL=mock
function mockListHackathons(params: ListHackathonsParams = {}): Hackathon[] {
  let data = [...sampleHackathons];
  if (params.status) data = data.filter((h) => h.status === params.status);
  if (params.tag) {
    const needle = params.tag.toLowerCase();
    data = data.filter((h) => (h.tags ?? []).some((t) => t.toLowerCase().includes(needle)));
  }
  if (params.q) {
    const needle = params.q.trim().toLowerCase();
    if (needle) {
      data = data.filter((h) =>
        [h.name, h.description, h.url, h.location, h.organizer, ...(h.tags ?? [])]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()
          .includes(needle),
      );
    }
  }
  if (params.sort === 'date' || params.sort === 'startDate') {
    data = [...data].sort((a, b) => (a.startDate ?? '').localeCompare(b.startDate ?? ''));
  }
  // upcoming/past are date-filtered against today; sample dates are already realistic
  return data;
}

function mockGetHackathon(id: string): Hackathon | undefined {
  return sampleHackathons.find((h) => h.id === id);
}

export interface ListHackathonsParams {
  status?: string;
  upcoming?: boolean;
  past?: boolean;
  tag?: string; // per issue #7 contract (backend also accepts tags)
  q?: string;
  sort?: string; // e.g. sort=date
  // accept alias for compatibility
  tags?: string;
}

export async function listHackathons(params: ListHackathonsParams = {}): Promise<Hackathon[]> {
  if (API_BASE === 'mock') return mockListHackathons(params);

  const search = new URLSearchParams();
  if (params.status) search.set('status', params.status);
  if (params.upcoming !== undefined) search.set('upcoming', String(params.upcoming));
  if (params.past !== undefined) search.set('past', String(params.past));
  // issue uses `tag`, backend uses `tags` — send both
  if (params.tag) search.set('tag', params.tag);
  if (params.tags) search.set('tags', params.tags);
  if (params.tag && !params.tags) search.set('tags', params.tag);
  if (params.q) search.set('q', params.q);
  if (params.sort) search.set('sort', params.sort);

  const qs = search.toString();
  const url = buildUrl(`/api/hackathons${qs ? `?${qs}` : ''}`);

  const res = await fetch(url, { headers: { Accept: 'application/json' } });
  if (!res.ok) {
    const body = (await res.json().catch(() => ({}))) as { error?: string };
    throw new Error(body.error || `Failed to fetch hackathons (${res.status})`);
  }
  const data = (await res.json()) as Record<string, unknown>[];
  return data.map(mapBackendToFrontend);
}

export async function getHackathon(id: string): Promise<Hackathon> {
  if (API_BASE === 'mock') {
    const found = mockGetHackathon(id);
    if (!found) throw new Error('Hackathon not found');
    return found;
  }
  const url = buildUrl(`/api/hackathons/${encodeURIComponent(id)}`);
  const res = await fetch(url, { headers: { Accept: 'application/json' } });
  if (!res.ok) {
    const body = (await res.json().catch(() => ({}))) as { error?: string };
    throw new Error(body.error || `Failed to fetch hackathon ${id} (${res.status})`);
  }
  const raw = (await res.json()) as Record<string, unknown>;
  return mapBackendToFrontend(raw);
}

export type SubmitHackathonPayload = {
  name?: string;
  url?: string;
  description?: string;
  startDate?: string;
  endDate?: string;
  location?: string;
  mode?: Hackathon['mode'];
  organizer?: string;
  hasPrize?: boolean;
  prizeDetails?: string;
  tags?: string[] | string;
  status?: string;
};

export async function submitHackathon(
  payload: SubmitHackathonPayload,
): Promise<Hackathon & { status: Hackathon['status'] }> {
  if (!payload.name?.trim() && !payload.url?.trim()) {
    throw new Error('One of name or url is required');
  }

  if (API_BASE === 'mock') {
    const created: Hackathon = {
      id: crypto.randomUUID(),
      name: payload.name?.trim() || payload.url!.trim(),
      description: payload.description,
      url: payload.url,
      startDate: payload.startDate,
      endDate: payload.endDate,
      location: payload.location,
      mode: payload.mode,
      organizer: payload.organizer,
      hasPrize: payload.hasPrize,
      prizeDetails: payload.prizeDetails,
      tags: Array.isArray(payload.tags)
        ? payload.tags
        : payload.tags?.split(',').map((t) => t.trim()),
      status: 'published',
    };
    return created;
  }

  const body: Record<string, unknown> = {};
  if (payload.name?.trim()) body['name'] = payload.name.trim();
  if (payload.url?.trim()) body['url'] = payload.url.trim();
  if (payload.description !== undefined) body['description'] = payload.description;
  if (payload.startDate !== undefined) body['startDate'] = toApiDate(payload.startDate);
  if (payload.endDate !== undefined) body['endDate'] = toApiDate(payload.endDate);
  if (payload.location !== undefined) body['location'] = payload.location;
  if (payload.mode !== undefined) body['mode'] = toBackendMode(payload.mode);
  if (payload.organizer !== undefined) body['organizer'] = payload.organizer;
  if (payload.hasPrize !== undefined) body['hasPrize'] = String(payload.hasPrize);
  if (payload.prizeDetails !== undefined) body['prizeDetails'] = payload.prizeDetails;
  if (payload.tags !== undefined)
    body['tags'] = Array.isArray(payload.tags) ? payload.tags.join(',') : payload.tags;
  if (payload.status !== undefined) body['status'] = payload.status;

  for (const [k, v] of Object.entries(body)) {
    if (v === '' || v === undefined) delete body[k];
  }

  const url = buildUrl('/api/hackathons');
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(body),
  });
  const json = (await res.json().catch(() => ({}))) as Record<string, unknown> & {
    error?: string;
    status?: string;
  };
  if (!res.ok) {
    throw new Error((json.error as string) || `Failed to create hackathon (${res.status})`);
  }
  // backend returns {success:string} today; mock returns full resource. Normalize to Hackathon.
  if (json['id'] && json['name']) return mapBackendToFrontend(json);
  return {
    id: String(json['id'] ?? crypto.randomUUID()),
    name: (json['name'] as string) ?? payload.name!,
    url: json['url'] as string | undefined,
    status: (json['status'] as Hackathon['status']) ?? 'published',
  } as Hackathon;
}

// Backward-compat aliases for previous names (cleanly deprecated — prefer spec names above)
export const fetchHackathons = listHackathons;
export const fetchHackathonById = getHackathon;
export const createHackathon = submitHackathon;
export type FetchHackathonsParams = ListHackathonsParams;
export type CreateHackathonPayload = SubmitHackathonPayload & { name: string; url: string };
