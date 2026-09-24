# TODO: Make `frontend/src/lib/api.ts` scalable

Goal: keep #7 working, prep for 100+ hackathons / multiple consumers without rewrite.

## 1. Contract (source of truth)
- [ ] Generate `Hackathon` type from `docs/API.md` / `backend/database.py:108` (OpenAPI or `openapi-typescript`); remove duplicate `Record<string,unknown>` casts in `api.ts:32`.
- [ ] Typed `ApiError { error: string, status: number }` + `Result<T>` instead of raw `throw new Error`.

## 2. Transport (`frontend/src/lib/client.ts` — new, keep `api.ts` thin)
- [ ] Central `request(path, {method, body, signal})` with `VITE_API_BASE_URL` runtime validation + `/api/v1` prefix.
- [ ] `AbortController` + timeout (10s) + retry (1x backoff) + `Authorization` header hook for future auth.
- [ ] Parse `{error:string}` shape consistently (`api.ts:121,147`).

## 3. Pagination (breaks first at scale)
- [ ] Backend: `GET /api/hackathons` `backend/main.py:306` add `?page&limit` + `X-Total-Count` (or `{data, total}`); stop returning unbounded array.
- [ ] Frontend: `listHackathons({status,tag,q,sort,page,limit})` pass through; `AllHackathons.tsx:86` remove client-side `slice`/`PAGE_SIZE=6` fallback, rely on server page.

## 4. Query / Cache
- [ ] Adopt `TanStack Query` — keys `['hackathons', params]`, `staleTime 60s`, dedup, `getHackathon(id)` cached; `submitHackathon` invalidates list.
- [ ] Remove manual `loading`/`error`+retry in `Home.tsx:65` / `AllHackathons.tsx` in favor of `isPending`/`error`/`refetch`.

## 5. Mock isolation
- [ ] Move `api.ts:77` mock (`sampleHackathons`) to `frontend/src/mocks/handlers.ts` (MSW), only bundled when `VITE_API_BASE_URL=mock`; make mock filtering mirror `backend/main.py:299,309` (`ilike`, `upcoming`/`past` date logic).

## 6. Perf / UX
- [ ] Debounce `q` input in `AllHackathons.tsx` (250ms) before calling `listHackathons`.
- [ ] Re-validate `VITE_API_BASE_URL` on HMR (don't cache at module load `api.ts:5` only).

## Out of scope (defer)
- Auth refresh, rate-limit UI, infinite scroll — add when list > 200 or second consumer needs `listHackathons`.

Verify: `npm run build` (`tsc --noEmit && vite build`) passes, `VITE_API_BASE_URL=mock` demo still works, `GET /api/hackathons?page=1&limit=6` returns `total`.
