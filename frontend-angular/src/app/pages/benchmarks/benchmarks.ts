import { Component } from '@angular/core';
import { DatePipe } from '@angular/common';

import { BenchmarkApi, BenchmarkRun } from '../../services/benchmark-api';

@Component({
  selector: 'app-benchmarks',
  imports: [DatePipe],
  templateUrl: './benchmarks.html',
  styleUrl: './benchmarks.css',
})
export class Benchmarks {
  runs: BenchmarkRun[] = [];
  loading = true;
  errorMessage = '';

  constructor(private readonly benchmarkApi: BenchmarkApi) {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    this.errorMessage = '';

    this.benchmarkApi.list().subscribe({
      next: (runs) => {
        this.runs = runs;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Could not load benchmark runs.';
        this.loading = false;
      },
    });
  }

  statusCount(status: BenchmarkRun['status']): number {
    return this.runs.filter((run) => run.status === status).length;
  }
}
