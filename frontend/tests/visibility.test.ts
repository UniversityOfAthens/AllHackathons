import { describe, it, expect } from 'vitest';
import { isVisible, highlightSelection } from '@/lib/hackathons';
import type { Hackathon } from '@/types/hackathon';

function h(overrides: Partial<Hackathon> & { id: string }): Hackathon {
  return { name: overrides.id, status: 'published', ...overrides };
}

describe('isVisible', () => {
  it('treats only published hackathons as publicly visible', () => {
    expect(isVisible(h({ id: 'a', status: 'published' }))).toBe(true);
    expect(isVisible(h({ id: 'b', status: 'pending' }))).toBe(false);
    expect(isVisible(h({ id: 'c', status: 'draft' }))).toBe(false);
    expect(isVisible(h({ id: 'd', status: 'needs-changes' }))).toBe(false);
  });
});

describe('highlightSelection', () => {
  it('never spotlights an unpublished hackathon', () => {
    const items = [
      h({ id: 'live-published', startDate: '2026-10-10', endDate: '2026-10-20' }),
      h({ id: 'live-draft', status: 'draft', startDate: '2026-10-10', endDate: '2026-10-20' }),
      h({ id: 'live-pending', status: 'pending', startDate: '2026-10-10', endDate: '2026-10-20' }),
    ];

    // Today is fixed at 2026-10-13 in the "today" argument, so all three are live.
    const { items: picked } = highlightSelection(items, '2026-10-13');

    expect(picked.map((x) => x.id)).toEqual(['live-published']);
  });

  it('falls through to the soonest upcoming published hackathon', () => {
    const items = [
      h({ id: 'soon-draft', status: 'draft', startDate: '2026-11-01' }),
      h({ id: 'soon-published', startDate: '2026-11-05' }),
      h({ id: 'later-published', startDate: '2026-12-01' }),
    ];

    const { state, items: picked } = highlightSelection(items, '2026-10-13');

    expect(state).toBe('soon');
    expect(picked.map((x) => x.id)).toEqual(['soon-published']);
  });
});
