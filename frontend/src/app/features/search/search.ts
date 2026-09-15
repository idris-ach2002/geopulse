import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { ResourceCategory } from '../../core/models/resource.dto';
import { ResourceCard } from './components/resource-card/resource-card';
import { RESOURCE_FIXTURES } from './data/resource.fixtures';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [ReactiveFormsModule, ResourceCard],
  template: `
    <section class="page">
      <h1>Recherche GeoPulse</h1>
      <p>V1 - formulaire local alimenté uniquement par des fixtures.</p>

      <form class="search-form">
        <label>
          Latitude
          <input type="number" value="45.7578" />
        </label>

        <label>
          Longitude
          <input type="number" value="4.832" />
        </label>

        <label>
          Catégorie
          <select>
            @for (category of categories; track category) {
              <option [value]="category">{{ category }}</option>
            }
          </select>
        </label>

        <label>
          Rayon (km)
          <input type="number" min="0.1" max="100" value="5" />
        </label>

        <label>
          Disponibilité minimale
          <input type="number" min="0" value="0" />
        </label>

        <label>
          Fraîcheur maximale
          <select>
            <option value="fresh">fresh</option>
            <option value="acceptable">acceptable</option>
            <option value="stale">stale</option>
          </select>
        </label>

        <button type="button">Rechercher</button>
      </form>

      <h2>{{ resources.length }} fixtures locales</h2>

      <div class="results">
        @for (resource of resources; track resource.id) {
          <app-resource-card [resource]="resource" />
        }
      </div>
    </section>
  `,
  styles: `
    .page {
      display: grid;
      gap: 1.5rem;
    }

    .search-form {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }

    label {
      display: grid;
      gap: 0.3rem;
    }

    input,
    select,
    button {
      font: inherit;
      padding: 0.6rem;
    }

    .results {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }
  `,
})
export class Search {
  readonly categories: readonly ResourceCategory[] = [
    'parking',
    'ev_charging',
    'pharmacy',
    'shop',
  ];

  readonly resources = RESOURCE_FIXTURES;
}
