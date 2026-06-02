import { Routes } from '@angular/router';

import { Dashboard } from './pages/dashboard/dashboard';
import { Connections } from './pages/connections/connections';
import { Probes } from './pages/probes/probes';
import { Benchmarks } from './pages/benchmarks/benchmarks';
import { Reports } from './pages/reports/reports';
import { Settings } from './pages/settings/settings';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: Dashboard },
  { path: 'connections', component: Connections },
  { path: 'probes', component: Probes },
  { path: 'benchmarks', component: Benchmarks },
  { path: 'reports', component: Reports },
  { path: 'settings', component: Settings },
  { path: '**', redirectTo: 'dashboard' },
];