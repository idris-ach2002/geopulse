import { TestBed } from '@angular/core/testing';

import { Search } from './search';

describe('Search', () => {
  it('renders all V1 local fixtures', async () => {
    const fixture = TestBed.createComponent(Search);

    fixture.detectChanges();
    await fixture.whenStable();

    expect(fixture.componentInstance.resources).toHaveLength(8);
    expect(fixture.nativeElement.textContent).toContain(
      'Parking Bellecour',
    );
  });

  it('contains the four V1 freshness states', () => {
    const fixture = TestBed.createComponent(Search);

    const states = new Set(
      fixture.componentInstance.resources.map(
        (resource) => resource.freshness.state,
      ),
    );

    expect(states).toEqual(
      new Set(['fresh', 'acceptable', 'stale', 'expired']),
    );
  });
});
