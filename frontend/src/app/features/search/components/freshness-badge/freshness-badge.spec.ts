import { TestBed } from '@angular/core/testing';

import { FreshnessBadge } from './freshness-badge';

describe('FreshnessBadge', () => {
  it('renders the supplied state', async () => {
    const fixture = TestBed.createComponent(FreshnessBadge);
    fixture.componentRef.setInput('state', 'stale');

    fixture.detectChanges();
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain('stale');
  });
});
