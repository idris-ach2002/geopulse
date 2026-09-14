import { TestBed } from '@angular/core/testing';

import { RESOURCE_FIXTURES } from '../../data/resource.fixtures';
import { ResourceCard } from './resource-card';

describe('ResourceCard', () => {
  it('renders resource information', async () => {
    const fixture = TestBed.createComponent(ResourceCard);
    fixture.componentRef.setInput('resource', RESOURCE_FIXTURES[0]);

    fixture.detectChanges();
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain(
      'Parking Bellecour',
    );
    expect(fixture.nativeElement.textContent).toContain('fresh');
  });
});
