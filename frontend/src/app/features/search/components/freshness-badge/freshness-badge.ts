import { Component, input } from '@angular/core';

import { FreshnessState } from '../../../../core/models/resource.dto';

@Component({
  selector: 'app-freshness-badge',
  standalone: true,
  template: `
    <span class="badge" [attr.data-state]="state()">
      {{ state() }}
    </span>
  `,
  styles: `
    .badge {
      border: 1px solid currentColor;
      border-radius: 999px;
      display: inline-block;
      padding: 0.2rem 0.55rem;
      text-transform: capitalize;
    }
  `,
})
export class FreshnessBadge {
  readonly state = input.required<FreshnessState>();
}
