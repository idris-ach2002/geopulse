import { Component, input } from '@angular/core';

import { ResourceDto } from '../../../../core/models/resource.dto';
import { FreshnessBadge } from '../freshness-badge/freshness-badge';

@Component({
  selector: 'app-resource-card',
  standalone: true,
  imports: [FreshnessBadge],
  template: `
    <article class="card">
      <div>
        <small>{{ resource().category }}</small>
        <h2>{{ resource().name }}</h2>
      </div>

      <app-freshness-badge [state]="resource().freshness.state" />

      @if (resource().availability?.status === 'available') {
        <p>
          {{ resource().availability?.available ?? '?' }}
          disponibles
          @if (resource().availability?.capacity !== undefined) {
            / {{ resource().availability?.capacity }}
          }
        </p>
      } @else {
        <p>Disponibilité inconnue</p>
      }
    </article>
  `,
  styles: `
    .card {
      border: 1px solid #d8dee9;
      border-radius: 0.75rem;
      display: grid;
      gap: 0.75rem;
      padding: 1rem;
    }

    h2 {
      margin: 0.25rem 0;
    }
  `,
})
export class ResourceCard {
  readonly resource = input.required<ResourceDto>();
}
