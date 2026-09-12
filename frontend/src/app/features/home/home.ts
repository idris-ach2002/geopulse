import { isPlatformBrowser } from '@angular/common';
import {
  Component,
  inject,
  OnInit,
  PLATFORM_ID,
  signal,
} from '@angular/core';

import { HealthService } from '../../core/services/health.service';

@Component({
  selector: 'app-home',
  standalone: true,
  template: `
    <section class="page">
      <h1>GeoPulse</h1>
      <p>Workspace initialisé.</p>

      <div class="status">
        <strong>Backend</strong>

        @switch (backendStatus()) {
          @case ('connected') {
            <span>Backend connected</span>
          }
          @case ('unavailable') {
            <span>Backend unavailable</span>
          }
          @default {
            <span>Checking backend...</span>
          }
        }
      </div>

      <p class="scope">
        V0 - Bootstrap, architecture et chaîne de qualité.
      </p>
    </section>
  `,
})
export class Home implements OnInit {
  private readonly health = inject(HealthService);
  private readonly platformId = inject(PLATFORM_ID);

  readonly backendStatus =
    signal<'checking' | 'connected' | 'unavailable'>('checking');

  ngOnInit(): void {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }

    this.health.getLiveness().subscribe({
      next: (response) => {
        this.backendStatus.set(
          response.status === 'ok' ? 'connected' : 'unavailable',
        );
      },
      error: () => {
        this.backendStatus.set('unavailable');
      },
    });
  }
}
