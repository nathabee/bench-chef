# BenchChef Angular Project Initialization

## Purpose

BenchChef is the developer and administrator workbench for SpaghettiChef.

The initial Angular application will provide tooling for:

- dataset inspection
- benchmark result visualization
- Java/Rust engine comparison
- parameter sweep review
- future experiment registry screens

 

## Prerequisites

Install Node.js and npm.

Check versions:

```bash
node --version
npm --version
```

Install Angular CLI globally:

```bash
npm install -g @angular/cli
```

Check Angular CLI:

```bash
ng version
```

## Initialize the Angular project

From the parent folder of the repository, run:

```bash
ng new bench-chef --routing --style=scss
```

When prompted, choose the default answers unless a specific option is required.

Alternative, if the GitHub repository already exists and is empty:

```bash
cd bench-chef
ng new bench-chef --routing --style=scss --directory .
```

## Start the development server

```bash
cd bench-chef
ng serve --open
```

The application should open at:

```text
http://localhost:4200/
```

## Generate initial structure for 0.1.x — Dataset Workbench

BenchChef 0.1.x focuses on the Dataset Workbench.

Initial scope:

- Angular application shell
- routing
- dataset workbench page
- benchmark dashboard placeholder page
- reusable metric-card component
- reusable dataset-summary component
- reusable validation-warning-list component
- reusable run-comparison-table component
- mock JSON data
- no backend dependency yet



```bash
ng generate component pages/dataset-workbench
ng generate component pages/benchmark-dashboard

ng generate component components/metric-card
ng generate component components/dataset-summary
ng generate component components/validation-warning-list
ng generate component components/run-comparison-table

ng generate service services/dataset-api
ng generate service services/benchmark-api
```


Note : we could have used also short aliases like that :

```bash
ng g c pages/dataset-workbench
ng g s services/dataset-api
```

## Build

```bash
ng build
```

## Test

```bash
ng test
```
  

## Wire the first routes

After generating the pages and components, configure routing so the application shows the Dataset Workbench at startup.

Edit:

```text
src/app/app.routes.ts
```

Expected content:

```ts
import { Routes } from '@angular/router';

import { DatasetWorkbench } from './pages/dataset-workbench/dataset-workbench';
import { BenchmarkDashboard } from './pages/benchmark-dashboard/benchmark-dashboard';

export const routes: Routes = [
  { path: '', redirectTo: 'datasets', pathMatch: 'full' },
  { path: 'datasets', component: DatasetWorkbench },
  { path: 'benchmarks', component: BenchmarkDashboard },
  { path: '**', redirectTo: 'datasets' },
];
```

## Replace the default app shell

Edit:

```text
src/app/app.html
```

Replace the generated content with:

```html
<header>
  <h1>BenchChef</h1>
  <nav>
    <a routerLink="/datasets" routerLinkActive="active">Dataset Workbench</a>
    <a routerLink="/benchmarks" routerLinkActive="active">Benchmark Dashboard</a>
  </nav>
</header>

<main>
  <router-outlet></router-outlet>
</main>
```

## Check the generated pages

Edit:

```text
src/app/pages/dataset-workbench/dataset-workbench.html
```

Temporary content:

```html
<h2>Dataset Workbench</h2>
<p>BenchChef 0.1.x dataset inspection page.</p>
```

Edit:

```text
src/app/pages/benchmark-dashboard/benchmark-dashboard.html
```

Temporary content:

```html
<h2>Benchmark Dashboard</h2>
<p>Placeholder page for benchmark and engine comparison results.</p>
```

## Run the application

```bash
ng serve --open
```

Check:

```text
http://localhost:4200/
http://localhost:4200/datasets
http://localhost:4200/benchmarks
```

Expected result:

```text
/ redirects to /datasets
/datasets shows Dataset Workbench
/benchmarks shows Benchmark Dashboard
```