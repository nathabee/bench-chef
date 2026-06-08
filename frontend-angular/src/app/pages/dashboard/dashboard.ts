import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { BackendApi } from '../../services/backend-api';
import { ConnectionApi, ConnectionProfile } from '../../services/connection-api';
import { ErrorSummary, LatencySummary, ProbeApi } from '../../services/probe-api';

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard {
  connections: ConnectionProfile[] = [];
  latencySummary: LatencySummary | null = null;
  errorSummary: ErrorSummary | null = null;
  loading = true;
  errorMessage = '';

  constructor(
    readonly backendApi: BackendApi,
    private readonly connectionApi: ConnectionApi,
    private readonly probeApi: ProbeApi,
  ) {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    this.errorMessage = '';

    this.connectionApi.list().subscribe({
      next: (connections) => {
        this.connections = connections;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'BenchChef backend is not reachable.';
        this.loading = false;
      },
    });

    this.probeApi.latencySummary().subscribe({
      next: (summary) => {
        this.latencySummary = summary;
      },
    });

    this.probeApi.errorSummary().subscribe({
      next: (summary) => {
        this.errorSummary = summary;
      },
    });
  }
}
