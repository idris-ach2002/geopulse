import { Routes } from '@angular/router';

import { Home } from './features/home/home';
import { Imports } from './features/imports/imports';
import { Resources } from './features/resources/resources';
import { Search } from './features/search/search';
import { System } from './features/system/system';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'search', component: Search },
  { path: 'resources', component: Resources },
  { path: 'imports', component: Imports },
  { path: 'system', component: System },
  { path: '**', redirectTo: '' },
];
