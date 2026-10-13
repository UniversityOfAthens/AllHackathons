import { describe, it, expect } from 'vitest';
import { renderToStaticMarkup } from 'react-dom/server';
import { MemoryRouter } from 'react-router-dom';
import Breadcrumbs, { fromHome } from '@/components/common/Breadcrumbs';
import { contributors } from '@/data/contributors';

function render(ui: React.ReactElement) {
  return renderToStaticMarkup(<MemoryRouter>{ui}</MemoryRouter>);
}

describe('Breadcrumbs', () => {
  it('renders a nav labelled "Breadcrumb"', () => {
    const html = render(
      <Breadcrumbs items={fromHome({ label: 'Όλα τα hackathons', to: '/hackathons' })} />,
    );
    expect(html).toContain('aria-label="Breadcrumb"');
  });

  it('starts every trail at the home page', () => {
    const html = render(
      <Breadcrumbs items={fromHome({ label: 'Όλα τα hackathons', to: '/hackathons' })} />,
    );
    expect(html).toContain('Αρχική');
    expect(html).toContain('href="/"');
    expect(html).toContain('Όλα τα hackathons');
  });

  it('marks the last crumb as the current page and does not link it', () => {
    const html = render(<Breadcrumbs items={fromHome({ label: 'Ionian Game Jam' })} />);
    expect(html).toContain('aria-current="page"');
    // The current page must not be a link — there is nowhere to navigate to.
    expect(html).not.toContain('href="/hackathon/ionian-game-jam"');
  });

  it('renders a separator before every crumb but the first', () => {
    const html = render(
      <Breadcrumbs
        items={fromHome(
          { label: 'Όλα τα hackathons', to: '/hackathons' },
          { label: 'Ionian Game Jam' },
        )}
      />,
    );
    // two crumbs after the root => two separators
    expect(html.match(/aria-hidden="true"/g)).toHaveLength(2);
  });

  // A one-item trail has nothing to navigate up to, so it renders nothing
  // rather than a lone "Αρχική" crumb on the home page itself.
  it('renders nothing for a single crumb', () => {
    const html = render(<Breadcrumbs items={[{ label: 'Αρχική', to: '/' }]} />);
    expect(html).toBe('');
  });
});

describe('contributors', () => {
  it('lists GitHub handles only — no names, no emails', () => {
    for (const handle of contributors) {
      expect(handle).toMatch(/^[A-Za-z0-9-]+$/);
      expect(handle).not.toContain('@');
    }
  });

  it('has no duplicate handles', () => {
    expect(new Set(contributors).size).toBe(contributors.length);
  });

  it('is not empty', () => {
    expect(contributors.length).toBeGreaterThan(0);
  });
});
