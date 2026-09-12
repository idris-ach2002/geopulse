import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { App } from './app';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideRouter([])],
    }).compileComponents();
  });

  it('creates the application', () => {
    const fixture = TestBed.createComponent(App);

    expect(fixture.componentInstance).toBeTruthy();
  });

  it('renders the V0 navigation', () => {
    const fixture = TestBed.createComponent(App);

    fixture.detectChanges();

    const content = fixture.nativeElement.textContent;

    expect(content).toContain('GeoPulse');
    expect(content).toContain('Search');
    expect(content).toContain('Resources');
    expect(content).toContain('Imports');
    expect(content).toContain('System');
  });
});
